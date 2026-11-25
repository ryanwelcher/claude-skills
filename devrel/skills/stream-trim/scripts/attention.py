#!/usr/bin/env python3
"""Tell the stream-trim page when Claude is waiting on Ryan in the terminal.

Claude Code hooks (declared in SKILL.md, active while the skill runs) call:

  attention.py set "<reason>"   Claude is waiting: show a banner with the reason
  attention.py notify           a Notification hook: the reason comes from its
                                notification_type on stdin
  attention.py clear            Ryan answered (a tool ran, or he typed)

Every running page server registers itself in the servers folder, so this
reaches whichever pages are open. It never fails and never prints: a hook
must not get in Claude's way.
"""
import json
import os
import sys
import urllib.request

NOTIFY = {
    "permission_prompt": "Claude needs you in the terminal: approve a command",
    "elicitation_dialog": "Claude needs you in the terminal",
    "idle_prompt": "Claude has finished its turn and may be waiting for your reply in the terminal",
}


def servers_dir():
    return os.environ.get("STREAM_TRIM_SERVERS") or os.path.expanduser("~/Library/Caches/stream-trim/servers")


def register(port, pid, raw):
    os.makedirs(servers_dir(), exist_ok=True)
    with open(os.path.join(servers_dir(), f"{port}.json"), "w") as f:
        json.dump({"port": port, "pid": pid, "raw": raw}, f)


def unregister(port):
    try:
        os.remove(os.path.join(servers_dir(), f"{port}.json"))
    except FileNotFoundError:
        pass


def _alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except (OSError, TypeError):
        return False


def live_servers():
    """The registered servers whose process is still running. Drops the rest."""
    out = []
    try:
        names = sorted(os.listdir(servers_dir()))
    except FileNotFoundError:
        return out
    for name in names:
        path = os.path.join(servers_dir(), name)
        try:
            with open(path) as f:
                s = json.load(f)
        except (OSError, ValueError):
            continue
        if isinstance(s, dict) and _alive(s.get("pid")):
            out.append(s)
        else:
            try:
                os.remove(path)
            except OSError:
                pass
    return out


def send(body):
    data = json.dumps(body).encode()
    for s in live_servers():
        req = urllib.request.Request(f"http://127.0.0.1:{s['port']}/api/attention", data=data, method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=1).close()
        except Exception:
            pass


def main(argv):
    cmd = argv[0] if argv else None
    # Hooks pass their event on stdin; always read it so the writer never hits a closed pipe.
    stdin = "" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
    if cmd == "set" and len(argv) > 1:
        send({"waiting": True, "reason": argv[1]})
    elif cmd == "clear":
        send({"waiting": False})
    elif cmd == "notify":
        try:
            event = json.loads(stdin or "{}")
        except ValueError:
            return
        reason = NOTIFY.get(event.get("notification_type")) if isinstance(event, dict) else None
        if reason:
            send({"waiting": True, "reason": reason})


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception:
        pass
    sys.exit(0)
