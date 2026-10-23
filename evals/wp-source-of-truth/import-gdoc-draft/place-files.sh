#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
# An empty clone of the shared repo, with no remote, for the import to land in.
git init -q -b trunk source-of-truth
