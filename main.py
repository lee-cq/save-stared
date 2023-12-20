#!/bin/env python3
import subprocess
from pathlib import Path

import github

g = github.Github()
user = g.get_user('lee-cq')
starred = user.get_starred()

repos = [_.full_name for _ in starred]
GIT_DIR_BASE = Path(__file__).parent.joinpath("git-dirs")

print(f'{GIT_DIR_BASE = }')
print("同步仓库：\n\t", '\n\t'.join(repos))

"""
git clone --mirror                      初次同步
git --git-dir=设置GIT位置 fetch --prune  增量同步
"""

for repo in repos:
    git_local = GIT_DIR_BASE.joinpath(repo + '.git')
    git_remote = 'https://github.com/' + repo
    if git_local.exists():
        print(f"检查增量情况： {repo}")
        subprocess.run(
            [
                'git', 'fetch', '--prune', '-all',
            ],
            check=True,
            cwd=git_local,
        )
    else:
        print(f"新增存储库: {repo}")
        git_local.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--mirror', git_remote, git_local], check=True)
