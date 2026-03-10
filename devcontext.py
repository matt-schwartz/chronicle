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

import argparse
import os

if not os.path.exists('settings.py'):
    raise FileNotFoundError("Please create a settings.py file based on settings_example.py and fill in the required values.")

import settings
import agent.search
import connectors.git


def parse_args():
    parser = argparse.ArgumentParser(description="DevContext CLI")
    parser.add_argument("command", type=str, help="Command to execute (e.g., 'import', 'watch', 'chat')", choices=['import', 'chat'])
    # parser.add_argument("--config", type=str, help="Path to the configuration file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.command == "import":
        print("Import project context...")
        for repo_path in settings.LOCAL_REPOS:
            connectors.git.store_history(repo_path)
    elif args.command == "chat":
        agent.search.chat()

