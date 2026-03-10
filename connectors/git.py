# Copyright 2026 Matthew Schwartz
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Monitors Git hooks for commits and branches
# Extracts: commit messages, branch names, file changes

import git
import sys

from storage.store import store_event


def on_commit(repo_path):
    repo = git.Repo(repo_path)
    commit = repo.head.commit
    
    # Store commit context
    store_event(
        type='git_commit',
        source='git',
        project=repo.working_dir,
        content=commit.message,
        metadata={
            'files_changed': [item.a_path for item in commit.diff()],
            'branch': repo.active_branch.name
        },
        timestamp=commit.committed_datetime
    )


def store_history(repo_path):
    repo = git.Repo(repo_path)
    for commit in repo.iter_commits():
        store_event(
            type='git_commit',
            source='git',
            project=repo.working_dir,
            content=commit.message,
            metadata={
                'files_changed': [item.a_path for item in commit.diff()],
                'branch': repo.active_branch.name
            },
            timestamp=commit.committed_datetime
        )


if __name__ == "__main__":
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    store_history(repo_path)
