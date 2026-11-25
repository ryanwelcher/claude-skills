#!/usr/bin/env python3
"""Tell the stream-trim page when Claude is waiting on Ryan in the terminal.

Claude Code hooks call it (in ~/.claude/settings.json on Ryan's Mac, and in the
devrel plugin's hooks/hooks.json for a plugin install). They run in every
session, so each page server records the session that started it, and a hook
only reaches pages from its own session (its "session_id" on stdin):

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


def register(port, pid, raw, session=None):
    """session: the Claude Code session that started the server (its
    CLAUDE_CODE_SESSION_ID), so hooks from other sessions leave this page alone."""
    os.makedirs(servers_dir(), exist_ok=True)
    with open(os.path.join(servers_dir(), f"{port}.json"), "w") as f:
        json.dump({"port": port, "pid": pid, "raw": raw, "session": session}, f)


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


def log(line):
    """hooks.log in the servers folder: one line per call, trimmed to the last 500."""
    path = os.path.join(servers_dir(), "hooks.log")
    try:
        os.makedirs(servers_dir(), exist_ok=True)
        with open(path, "a") as f:
            f.write(line + "\n")
        if os.path.getsize(path) > 100_000:
            with open(path) as f:
                keep = f.readlines()[-500:]
            with open(path, "w") as f:
                f.writelines(keep)
    except OSError:
        pass


def send(body, session=None):
    """Post to every live server started by this session (or by no known session).
    Returns how many it reached."""
    data = json.dumps(body).encode()
    sent = 0
    for s in live_servers():
        if session and s.get("session") and s["session"] != session:
            continue
        req = urllib.request.Request(f"http://127.0.0.1:{s['port']}/api/attention", data=data, method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=1).close()
            sent += 1
        except Exception:
            pass
    return sent


def main(argv):
    cmd = argv[0] if argv else None
    # Hooks pass their event on stdin; always read it so the writer never hits a closed pipe.
    stdin = "" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
    try:
        event = json.loads(stdin or "{}")
    except ValueError:
        event = {}
    if not isinstance(event, dict):
        event = {}
    session = event.get("session_id")
    sent = None
    if cmd == "set" and len(argv) > 1:
        sent = send({"waiting": True, "reason": argv[1]}, session)
    elif cmd == "clear":
        sent = send({"waiting": False}, session)
    elif cmd == "notify":
        reason = NOTIFY.get(event.get("notification_type"))
        if reason:
            sent = send({"waiting": True, "reason": reason}, session)
    if sent is not None:
        import time
        log("%s %s %s %s sent=%d" % (time.strftime("%H:%M:%S"), event.get("hook_event_name") or "-", cmd,
                                     session or "-", sent))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception:
        pass
    sys.exit(0)
