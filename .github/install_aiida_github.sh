#!/bin/bash
git clone https://github.com/aiidateam/aiida_core ../aiida_core
cd ../aiida_core
git checkout "$AIIDA_DEVELOP_GIT_HASH"
# shellcheck disable=SC2102
pip install -e .[docs,pre-commit,testing]
cd "$TRAVIS_BUILD_DIR" || exit
