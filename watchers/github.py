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

