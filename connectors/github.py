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

# Monitors PRs and issues
# Extracts: PR descriptions, review comments, issue discussions

from github import Github

from storage.store import store_event

def watch_prs(repo_name):
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    
    for pr in repo.get_pulls(state='all'):
        # Store PR context
        store_event(
            type='pr_context',
            source='github',
            project=repo.full_name,
            content=pr.title,
            metadata={
                'description': pr.body,
                'comments': [c.body for c in pr.get_comments()],
                'review_comments': [c.body for c in pr.get_review_comments()],

            'decision': 'merged' if pr.merged else 'closed'
        })

