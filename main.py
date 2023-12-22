#!/bin/env python3
import subprocess
from pathlib import Path

import github

g = github.Github()
user = g.get_user('lee-cq')
starred = user.get_starred()

repos = [_.full_name for _ in starred]
SRC_DIR = Path(__file__).parent
GIT_DIR_BASE = SRC_DIR.joinpath("git-dirs")
REMOTE_TARGET = []

print(f'{GIT_DIR_BASE = }')
print("同步仓库：\n\t", '\n\t'.join(repos))

"""
git clone --mirror                      初次同步
git --git-dir=设置GIT位置 fetch --prune  增量同步
"""

for repo in repos:
    git_local = GIT_DIR_BASE.joinpath(repo + '.git')
    git_remote = 'https://github.com/' + repo

    subprocess.run(
        [f'{SRC_DIR}/update_repo.sh', git_local, git_remote, *REMOTE_TARGET],

    )
