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

from datetime import datetime
import logging
import json

from . import sql, vector

logger = logging.getLogger(__name__)

sql.init_db()


def store_event(type: str, source: str, project: str, content: str, metadata: dict, timestamp: datetime|None = None) -> None:
    """
    Store an event in the database(s).

    :param type: The type of the event (e.g., 'git_commit', 'file_change').
    :param source: The source of the event (e.g., 'git', 'filesystem').
    :param project: The project associated with the event.
    :param content: The main content of the event (e.g., commit message, file path).
    :param metadata: Additional metadata related to the event (e.g., timestamp, branch name).
    :param timestamp: The timestamp of the event. If None, the current time is used.
    """
    if timestamp is None:
        timestamp = datetime.now(tz=datetime.timezone.utc)
    timestamp = timestamp.isoformat()
    with sql.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (type, source, project, content, metadata, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (type, source, project, content, json.dumps(metadata), timestamp)
        )
        vector.store_with_embedding(id=str(cursor.lastrowid), content=content, type=type, project=project, timestamp=timestamp)
        logger.info(f"Stored event {type} for project {project} with ID {cursor.lastrowid}")


if __name__ == "__main__":
    # List events
    with sql.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT type, source, project, timestamp FROM events")
        events = cursor.fetchall()
        for event in events:
            print(event)
