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

from yaspin import yaspin

import settings
import agent.search
import connectors.git
import connectors.github
import connectors.jira


def import_context():
    with yaspin(text="Importing...", color="red") as spinner:
        for repo_path in settings.LOCAL_REPOS:
            spinner.text = "Importing git history from " + repo_path + "..."
            connectors.git.store_history(repo_path)
        if getattr(settings, 'JIRA_PROJECTS', []):
            spinner.text = "Importing Jira project context..."
            connectors.jira.store_issues(
                url=settings.JIRA_URL,
                email=settings.JIRA_EMAIL,
                api_token=settings.JIRA_API_TOKEN,
                projects=settings.JIRA_PROJECTS,
            )
        if getattr(settings, 'GITHUB_REPOS', []):
            spinner.text = "Importing GitHub repository context..."
            for repo_name in settings.GITHUB_REPOS:
                spinner.text = "Importing GitHub repository context for " + repo_name + "..."
                connectors.github.store_prs(repo_name, settings.GITHUB_ACCESS_TOKEN)
        spinner.ok("✔")

def chat():
    agent.search.chat()
