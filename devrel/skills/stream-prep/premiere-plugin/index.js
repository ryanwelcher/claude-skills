// Stream Prep: headless Premiere plugin. Loads at startup, watches a jobs folder,
// and for each job builds a new project from an OBS recording with the stream
// prep edits applied (drop Full Mix + Music, pull the mic earlier, name tracks).
const ppro = require("premierepro");
const fs = require("fs");
const os = require("os");

// OBS track layout, 1-based track numbers.
const REMOVE = [1, 4]; // Full Mix, Spotify
const SHIFT = 2; // mic
const FRAMES = 9; // pull the mic this many frames earlier
const LEAD_IN = 0.5; // seconds kept before the first word when the intro is cut
const NAMES = ["Full Mix (removed)", "Mic", "Guest", "Music (removed)", "Theme Song", "Firebot"];

const HOME = os.homedir();
const JOBS = `${HOME}/Library/Application Support/stream-prep/jobs`;
const LOG = `${HOME}/Library/Logs/stream-prep-ppro.log`;

let logLines = [];
async function log(msg) {
  logLines.push(`${new Date().toISOString()} ${msg}`);
  logLines = logLines.slice(-500);
  try {
    await fs.writeFile(LOG, logLines.join("\n") + "\n", { encoding: "utf-8" });
  } catch (e) {
    console.error("stream-prep log failed", e);
  }
}

async function runJob(job) {
  const project = await ppro.Project.createProject(job.prproj);
  if (!project) throw new Error(`could not create project ${job.prproj}`);
  try {
    await prep(project, job);
  } finally {
    // Save even on failure, so Premiere never sits on a "save changes?" prompt.
    await project.save();
  }
}

async function prep(project, job) {
  if (!(await project.importFiles([job.video], true))) throw new Error(`import failed: ${job.video}`);
  const root = await project.getRootItem();
  let clip = null;
  for (const item of await root.getItems()) {
    clip = ppro.ClipProjectItem.cast(item);
    if (clip) break;
  }
  if (!clip) throw new Error("imported clip not found in the project");

  const seq = await project.createSequenceFromMedia(job.name, [clip]);
  const count = await seq.getAudioTrackCount();
  if (count !== NAMES.length) throw new Error(`expected ${NAMES.length} audio tracks, found ${count}`);

  const CLIP = ppro.Constants.TrackItemType.CLIP;
  const tracks = [];
  for (let i = 0; i < count; i++) tracks.push(await seq.getAudioTrack(i));
  const items = tracks.map((t) => t.getTrackItems(CLIP, false));
  const video = (await seq.getVideoTrack(0)).getTrackItems(CLIP, false);
  const kept = [...video, ...items.filter((_, i) => !REMOVE.includes(i + 1)).flat()];
  const mic = items[SHIFT - 1][0];
  if (!mic) throw new Error(`no clip on A${SHIFT}`);

  const offset = ppro.TickTime.createWithTicks(String(Number(await seq.getTimebase()) * FRAMES));
  const micIn = (await mic.getInPoint()).add(offset);
  const secs = (s) => ppro.TickTime.createWithSeconds(s);
  const editor = ppro.SequenceEditor.getEditor(seq);

  // Premiere validates every action in a transaction against the timeline as it was
  // before the transaction, so each step that depends on the previous one gets its own.
  const tx = (label, build) => {
    let ok = false;
    project.lockedAccess(() => {
      ok = project.executeTransaction(build, `Stream prep: ${label}`);
    });
    if (!ok) throw new Error(`${label} failed`);
  };

  tx("remove and name tracks", (ca) => {
    ppro.TrackItemSelection.createEmptySelection((sel) => {
      for (const n of REMOVE) for (const it of items[n - 1]) sel.addItem(it);
      ca.addAction(editor.createRemoveItemsAction(sel, false, ppro.Constants.MediaType.AUDIO, false));
    });
    tracks.forEach((t, i) => ca.addAction(t.createSetNameAction(NAMES[i])));
  });
  // A clip at 0 can't move left, so push everything out 1s, resync the mic, then pull it all back.
  tx("push out", (ca) => kept.forEach((it) => ca.addAction(it.createMoveAction(secs(1)))));
  tx("resync mic", (ca) => {
    ca.addAction(mic.createSetInPointAction(micIn));
    ca.addAction(mic.createMoveAction(secs(-offset.seconds)));
  });
  tx("pull back", (ca) => kept.forEach((it) => ca.addAction(it.createMoveAction(secs(-1)))));

  // Cut the "starting soon" intro: trim every clip's head (each then starts at `trim`),
  // then slide everything back to 0. voiceStart (seconds into the recording) comes from the
  // Quick Action's silence detection; the mic now plays `offset` earlier, so account for it.
  const trimStart = (Number(job.voiceStart) || 0) - offset.seconds - LEAD_IN;
  if (trimStart > 0) {
    const tpf = Number(await seq.getTimebase());
    const trim = ppro.TickTime.createWithTicks(String(Math.round((trimStart * 254016000000) / tpf) * tpf));
    const ins = await Promise.all(kept.map((it) => it.getInPoint()));
    tx("trim intro", (ca) => kept.forEach((it, i) => ca.addAction(it.createSetInPointAction(ins[i].add(trim)))));
    tx("close gap", (ca) => kept.forEach((it) => ca.addAction(it.createMoveAction(secs(-trim.seconds)))));
    await log(`  trimmed ${trim.seconds.toFixed(3)}s intro`);
  }

  const pos = async (it) => `start=${(await it.getStartTime()).seconds.toFixed(3)} in=${(await it.getInPoint()).seconds.toFixed(3)}`;
  await log(`  result: V1 ${await pos(video[0])}, Mic ${await pos(mic)}`);
}

let busy = false;
async function poll() {
  if (busy) return;
  busy = true;
  try {
    let files = [];
    try {
      files = (await fs.readdir(JOBS)).filter((f) => f.endsWith(".json"));
    } catch (e) {
      return; // no jobs folder yet
    }
    for (const f of files) {
      const path = `${JOBS}/${f}`;
      const id = f.replace(/\.json$/, "");
      try {
        const job = JSON.parse(await fs.readFile(path, { encoding: "utf-8" }));
        await fs.unlink(path);
        await log(`job ${id}: ${job.video}`);
        await runJob(job);
        await fs.writeFile(`${JOBS}/${id}.done`, job.prproj, { encoding: "utf-8" });
        await log(`job ${id}: done`);
      } catch (e) {
        const msg = e && e.message ? e.message : String(e);
        await log(`job ${id}: ERROR ${msg}`);
        await fs.writeFile(`${JOBS}/${id}.error`, msg, { encoding: "utf-8" });
      }
    }
  } finally {
    busy = false;
  }
}

log(`loaded, watching ${JOBS}`);
setInterval(poll, 2000);
