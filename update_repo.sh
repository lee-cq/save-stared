#!/usr/bin/env bash

# git-dir remote-source  remote-target ...
git_dir="$1"
shift
remote_source="$1"
shift
remote_targets=("$@")

if [ -d "$git_dir" ]; then
    echo "更新现有存储库: ${git_dir}"
    git --git-dir="${git_dir}" fetch --prune --all
else
    mkdir -p "$(dirname "$git_dir")"
    echo "在本地创建新的存储库: ${remote_source} -> ${git_dir}"
    git clone --mirror "$remote_source" "$git_dir"
fi

for target in "${remote_targets[@]}"; do
    git remote remove target || echo "Remote No target..."
    git remote add target "$target"
    echo "推送存储库至远程: ${git_dir} -> ${target}"
    git --git-dir="$git_dir" push --mirror target
done
