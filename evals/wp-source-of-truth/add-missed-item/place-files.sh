#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
# The repo snapshot is stored without .git; recreate the imported state as one commit.
cd source-of-truth
git init -q -b trunk
git add -A
git -c user.name=test -c user.email=test@example.com commit -qm "Import 7.2 draft from Google Docs (Oct 19 sweep)"
