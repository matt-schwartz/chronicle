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

# Monitors Jira projects for stories, tasks, subtasks, and comments
# Extracts: issue summaries, descriptions, comments, status, assignees

from dateutil import parser as dateutil_parser

from jira import JIRA

from storage.store import store_event


def connect(url, email, api_token):
    """Create an authenticated JIRA client."""
    return JIRA(server=url, basic_auth=(email, api_token))


def store_issues(url, email, api_token, projects):
    """Import issues and comments from one or more Jira projects."""
    client = connect(url, email, api_token)

    for project_key in projects:
        start_at = 0
        batch_size = 50

        while True:
            issues = client.search_issues(
                f'project={project_key} ORDER BY created ASC',
                startAt=start_at,
                maxResults=batch_size,
                fields='summary,description,issuetype,status,assignee,creator,priority,created,updated,comment',
            )

            if not issues:
                break

            for issue in issues:
                _store_issue(issue, project_key)
                _store_comments(client, issue, project_key)

            start_at += len(issues)
            if len(issues) < batch_size:
                break


def _store_issue(issue, project_key):
    """Store a single Jira issue as an event."""
    fields = issue.fields
    content = f"{issue.key}: {fields.summary}"
    if fields.description:
        content += f"\n\n{fields.description}"

    store_event(
        type='jira_issue',
        source='jira',
        project=project_key,
        content=content,
        metadata={
            'issue_key': issue.key,
            'issue_type': fields.issuetype.name,
            'status': fields.status.name,
            'assignee': fields.assignee.displayName if fields.assignee else None,
            'creator': fields.creator.displayName if fields.creator else None,
            'priority': fields.priority.name if fields.priority else None,
        },
        timestamp=dateutil_parser.parse(fields.created),
    )


def _store_comments(client, issue, project_key):
    """Store all comments for a Jira issue as individual events."""
    for comment in client.comments(issue.key):
        store_event(
            type='jira_comment',
            source='jira',
            project=project_key,
            content=comment.body,
            metadata={
                'issue_key': issue.key,
                'comment_id': comment.id,
                'author': comment.author.displayName if comment.author else None,
            },
            timestamp=dateutil_parser.parse(comment.created),
        )
