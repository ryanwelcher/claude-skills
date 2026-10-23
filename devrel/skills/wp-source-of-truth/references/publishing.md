# Publishing and scheduling

## How deploys work

Spacefast is Automattic's host for agent-built sites (https://spacefast.com/docs). Each release
directory is its own Spacefast site (a "space"), connected to the shared repo with that directory
as its root. The directory's `sf.jsonc` tells Spacefast how to build it:

```jsonc
{ "build": { "installCommand": "npm install", "buildCommand": "npm run build", "outputDirectory": "dist" } }
```

Once the release directory is connected, every push to `trunk` that changes it builds on
Spacefast and moves the live URL to the new version. Pushes that only touch another release are
skipped by the connection's ignored-build command. Other branches, such as proposal PRs, get preview builds with their own
URLs, so a proposal can be reviewed as a rendered page before it's merged. Every publish is
saved as its own version, so `sf rollback` undoes a bad deploy.

The CLI is `spacefast` (short name `sf`). It's fine to run it without installing:
`npx spacefast <command>`. It needs Node 20.3 or newer.

## One-time setup

Confirm each step with the user before you run it. Creating a space and sharing it are visible to
other people.

1. **Sign in:** `npx spacefast login`. This opens the browser for approval. Check it with
   `npx spacefast whoami`.
2. **Push the release directory to `trunk` first** (`wptrainingteam/source-of-truth`).
3. **First publish, which creates the space:** run `npm run build && npx spacefast publish ./dist --prebuilt --json`
   from the release directory. The receipt has the space id and `liveUrl`. Save both in `sot.json` under
   `spacefast`.
4. **Connect GitHub for autodeploy:**
   ```bash
   npx spacefast git connect --space <space> --provider github \
     --repository wptrainingteam/source-of-truth --production-branch trunk \
     --root-directory X.Y --config X.Y/sf.jsonc \
     --ignored-build-command 'git diff --quiet HEAD^ HEAD -- .' --sync
   ```
   `--root-directory` makes Spacefast install and build inside the release directory. The
   ignored-build command exits 0, which skips the build, when the push didn't change that
   directory. Spacefast's GitHub app may ask for repo access the first time, and the
   wptrainingteam org may need to approve it. Check the first build's log to confirm it ran in
   the release directory. After that, push a trivial
   commit and confirm that `npx spacefast versions --space <space>` shows a new version.
5. **Access:** the site has two audiences. Readers get the clean post at `/`. Reviewers get the
   draft at `/draft/`, which shows working notes, so readers' links must not reach it.
   ```bash
   # readers: the clean post and its assets
   npx spacefast share link create --space <space> --name "Source of Truth" --landing / --path '/' --role viewer
   # reviewers: the draft (add --role commenter if reviewers should comment)
   npx spacefast share link create --space <space> --name "SoT draft review" --landing /draft/ --path '/draft/**' --role viewer
   ```
   If the post uses images, give the reader link access to `/assets/**` too. Spacefast's path
   matching decides exactly what each link reaches, so after you create the links, open the
   reader link in a private window and confirm that `/draft/` is refused. Don't hand out a link
   until that check passes. Save both links in `sot.json` → `spacefast.shareLink` and
   `spacefast.draftLink`. Ask before you make the space fully
   public (`npx spacefast share grant --to public --role viewer --path '/' --target live --space <space>`).
   That's a separate decision, usually made once the post is published. A public grant on `/**`
   would also expose `/draft/`, so scope it to `/` and `/assets/**`.

## Fallback: GitHub Actions publish

If the Spacefast git connection isn't available or doesn't build correctly, publish from Actions
instead. Create an API key (`npx spacefast api-keys create --name "SoT CI" --preset ci_deploy`;
the secret is printed only once), store it as the repo secret `SPACEFAST_TOKEN`, and add
`.github/workflows/publish-X-Y.yml` at the repo root:

```yaml
name: Publish X.Y
on:
  push:
    branches: [trunk]
    paths: ['X.Y/**']
jobs:
  publish:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: 'X.Y'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci && npm run build
      - run: npx spacefast publish ./dist --prebuilt --space "$SPACE" --json
        env:
          SPACEFAST_TOKEN: ${{ secrets.SPACEFAST_TOKEN }}
          SPACE: <space id from sot.json>
```

Use only one of the two deploy paths. If both run, every push publishes twice.

## Scheduled sweeps

Two parts, both optional:

1. **The Status workflow** (`.github/workflows/status-X-Y.yml` at the repo root, copied from
   the skill's `assets/status-workflow.yml`) runs `check-status.mjs` in the release directory
   every morning with the repo's own token. It commits `notes/status.json`
   and `notes/status-report.md`. Pushing it doesn't change the post, so the site rebuilds with
   the same content.
2. **A cloud routine** does the judgment step. Use the `schedule` skill to create one on the
   content repo. Run it daily from Beta 1 to the final release, about an hour after the Status
   workflow. Before Beta 1, weekly is enough. Prompt:

   > Run a Source of Truth sweep on the X.Y release in this repo. Work in the X.Y/ directory.
   > Follow X.Y/CLAUDE.md, or the wp-source-of-truth skill's sweep procedure if that skill is
   > available. Use today's X.Y/notes/status-report.md.
   > Commit status-level changes to trunk and open proposal PRs for anything editorial. Don't
   > ask questions: record anything that needs a decision in notes/open-questions.md.

   The routine needs push access to the repo and must be able to open PRs. The release's
   `CLAUDE.md` carries the rules, so the routine works even if the skill isn't installed where
   it runs.

After the release ships, turn off the routine and the Status workflow
(`gh workflow disable "Status X.Y"`).
