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
