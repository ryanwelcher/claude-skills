# Researching a release

Use this guide to decide what belongs in a release, and where to confirm it.

## Sources, in order of authority

Replace `X-Y` with the release slug (for example `7-3`):

1. **Make Core posts for the release.** Start with the development cycle page
   (`https://make.wordpress.org/core/X-Y/`), the "Roadmap to X.Y" post, and the release squad
   announcement. Then read everything tagged for the release, via the RSS feed
   `https://make.wordpress.org/core/tag/X-Y/feed/`, and the dev notes tag
   (`https://make.wordpress.org/core/tag/dev-notes+X-Y/`). Beta and RC announcement posts state
   which Gutenberg version each package contains.
2. **Gutenberg release posts** ("What's new in Gutenberg NN.N") and the GitHub release notes for
   every plugin version in the range: `gh release view vNN.N.0 -R WordPress/gutenberg`.
3. **Iteration and tracking issues**, filtered with
   `gh issue list -R WordPress/gutenberg --label "[Type] Iteration" --state open`, plus the
   release's GitHub project board, which the roadmap links.
4. **Trac** for Core-only work: the "next major release" report
   (`https://core.trac.wordpress.org/report/6`) and tickets on the release milestone. Trac puts
   a JavaScript browser check in front of scripted requests. Get the same facts from the GitHub
   mirror instead: commits in `WordPress/wordpress-develop` whose message says `Fixes #N` or
   `See #N`, and PRs there that reference the ticket. `scripts/check-status.mjs` already does
   this.
5. **The previous release's punted list and backlog.** Items carried over from the last release
   are the most likely to slip again, so check each one.

The What's new for developers posts on developer.wordpress.org/news and Gutenberg Times are good
for finding items, but confirm each item against sources 1–4 before you rely on it.

## Deciding the Gutenberg range

A release contains the Gutenberg plugin versions released since the previous Core release's
cutoff, up to whatever the Beta 1 pin points at. Don't assume that's the last plugin release
before Beta 1: 7.2 Beta 1 pinned the tip of `wp/7.2`, which was the next version's RC1 plus
cherry-picks, so 24.3 was in the range even though 24.2 was the last final release. Read the
pin commit (next section) and the Beta 1 post, and until then mark the range 🔍 in the intro.

Expect one version to straddle two releases. For example, 23.8 shipped during the 7.1 cycle:
some of its PRs were backported to 7.1, and the rest wait for 7.2. For any PR in a straddling
version, check whether it was already in the previous release before you call it new. If it
was, leave it out.

## The fastest proof: the Gutenberg pin in wordpress-develop

Core takes Gutenberg as a pinned build of the `wp/X.Y` branch. Each Beta and RC has a
wordpress-develop commit that updates that pin, and the commit message lists every Gutenberg PR
included since the previous pin. Find it with:

```bash
gh api -X GET search/commits -f q='repo:WordPress/wordpress-develop Gutenberg wp/X.Y' -f sort=committer-date --jq '.items[] | .commit.committer.date[:10] + " " + .sha[:10] + " " + (.commit.message | split("\n")[0])'
```

The commit subject reads "General: Bump the pinned hash for Gutenberg to <hash>", and its body
says which Gutenberg version or branch tip it pins. The one just before the "WordPress X.Y Beta
1." commit is the Beta 1 pin.

Then read the full message with `gh api repos/WordPress/wordpress-develop/commits/<sha> --jq .commit.message`.
If a PR number is in a pin commit, the PR is in that Beta or RC. Nothing else gives as direct an
answer, so check it before the milestone heuristics below.

The same method answers "did this already ship in the previous release?". Search the commit
subjects on the previous release's branch in Gutenberg (`wp/X.Y-1`) for the PR number:
`gh api 'repos/WordPress/gutenberg/commits?sha=wp/7.1&since=<date>&per_page=100' --paginate --jq '.[].commit.message | split("\n")[0]' | grep '(#NNNNN)'`.
If that finds nothing, search for the PR's title too, because a cherry-pick sometimes carries a
different PR number (7.2's shareable revision URLs, #79934, reached `wp/7.1` as #81205). Don't
use a compare or ancestry check (`compare/wp/7.1...<sha>`): cherry-picks are new commits, so a
PR that did ship still shows as "diverged".

## Deciding whether a PR is in the release

The milestone that Gutenberg sets on a merged PR (`Gutenberg 24.3`) is the plugin version it
first ships in:

| PR state | Means |
|---|---|
| merged, milestone inside the range | In the release |
| merged, milestone after the range | Not in Beta 1 unless it's backported. Look for the `Backport to WP Beta/RC` label and a matching commit to the `wp/X.Y` branch, or a later Beta/RC post that lists it. Keep 🔍 until one of them confirms it. |
| merged, milestone before the range | Probably shipped in the previous release. Check that release's SoT and remove the item if it's there. |
| open or draft | Not in the release yet. It's only a candidate before Beta 1. After Beta 1, it gets in only as a blessed feature 🙏 or a bug fix. |
| closed, not merged | Not happening in this form. Look for a replacement PR. |

For Trac tickets, a `Fixes #N` commit to `trunk` before the branch point means it's in. GitHub's
commit search doesn't match `#NNNNN` reliably, so search a local partial clone instead:

```bash
git clone --filter=blob:none --no-checkout --shallow-since=<cycle start> https://github.com/WordPress/wordpress-develop.git wpdev
git -C wpdev log origin/trunk --format='%cd %h %s' --date=short -E --grep='#NNNNN([^0-9]|$)'
```

Git's `-E` has no `\b`, so end the pattern with `([^0-9]|$)`. The same clone answers "is it on
the previous release's branch?" (`git fetch --filter=blob:none origin X.Y-1`, then
`git show FETCH_HEAD:<file> | grep <function>`), and lets you read merged code with
`git show origin/trunk:<file>`. Check for reverts too: a ticket can have a commit and a later
"Revert" commit. After
the branch point, the fix also needs a commit to the `X.Y` branch. When the `fixed` status comes
from the GitHub mirror, read the commit subject to make sure it's the main change and not a test
or a follow-up.

## What makes an item

Include work that changes something a reader will notice or has to act on: new UI, new or
changed APIs, deprecations, breaking changes, defaults that changed, and features that ship. Fold
related small PRs into one item, or into a "quality of life" bullet list. Leave out internal
refactors, test-only changes, TypeScript conversions and dependency bumps, unless they break
something for extenders. Record skipped items in the sweep log's "Merged but not added" line, so
the next sweep doesn't re-research them.
