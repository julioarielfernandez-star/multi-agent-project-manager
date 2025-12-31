from notion_client import Client
from config.settings import settings
from datetime import datetime

class NotionManager:
    """Manages interactions with Notion API for project management"""

    def __init__(self):
        self.client = Client(auth=settings.NOTION_API_KEY)
        self.database_id = settings.NOTION_DATABASE_ID

    def create_task(self, title, description, status="Not Started", priority="Medium", assigned_to=None):
        """Create a new task in Notion database"""
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Status": {"status": {"name": status}},
            "Priority": {"select": {"name": priority}},
            "Description": {"rich_text": [{"text": {"content": description}}]}
        }

        if assigned_to:
            properties["Assigned To"] = {"rich_text": [{"text": {"content": assigned_to}}]}

        try:
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            return response
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

    def update_task_status(self, page_id, status):
        """Update the status of a task"""
        try:
            response = self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {"status": {"name": status}}
                }
            )
            return response
        except Exception as e:
            print(f"Error updating task: {e}")
            return None

    def get_tasks(self, filter_by_status=None):
        """Retrieve tasks from Notion database"""
        query = {"database_id": self.database_id}

        if filter_by_status:
            query["filter"] = {
                "property": "Status",
                "status": {"equals": filter_by_status}
            }

        try:
            response = self.client.databases.query(**query)
            return response.get("results", [])
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def add_comment(self, page_id, comment):
        """Add a comment to a Notion page"""
        try:
            response = self.client.comments.create(
                parent={"page_id": page_id},
                rich_text=[{"text": {"content": comment}}]
            )
            return response
        except Exception as e:
            print(f"Error adding comment: {e}")
            return None
