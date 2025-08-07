from common.models.task import Task
from datetime import datetime
from common.repositories.factory import RepositoryFactory, RepoType

class TaskService:
    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.task_repo = self.repository_factory.get_repository(RepoType.TASK)

    def create_task(self, title, description, assigned_to_id, priority, organization_id=None, due_date=None):
        task_data = {
            "title": title,
            "description": description,
            "assigned_to_id": assigned_to_id,
            "organization_id": organization_id,
            "due_date": due_date,
            "priority": priority,
            "status": "incomplete"
        }
        task = Task.from_dict(task_data)
        task.prepare_for_save(changed_by_id=assigned_to_id)
        return self.task_repo.save(task)

    def get_tasks_by_user(self, user_id, status_filter=None, priority_filter=None, title=None):
        """Get all tasks assigned to a specific user, optionally filtered by status and priority"""
        query_params = {"assigned_to_id": user_id}
        
        # Apply status filter
        if status_filter and status_filter.lower() != 'all':
            if status_filter.lower() == 'completed':
                query_params["status"] = "completed"
            elif status_filter.lower() == 'incomplete':
                query_params["status"] = "incomplete"
        
        # Apply priority filter
        if priority_filter and priority_filter.lower() != 'all':
            if priority_filter.lower() in ['low', 'medium', 'high']:
                query_params["priority"] = priority_filter.lower()
        
        # Use LIKE query for title search if title is provided
        if title:
            return self.task_repo.get_tasks_with_title_like(query_params, title)
        else:
            return self.task_repo.get_many(query_params)

    def get_task_by_id(self, task_id, user_id=None):
        """Get a specific task by ID, optionally filtered by user"""
        if user_id:
            return self.task_repo.get_one({"entity_id": task_id, "assigned_to_id": user_id})
        else:
            return self.task_repo.get_one({"entity_id": task_id})

    def update_task(self, task_id, user_id, title=None, description=None, status=None, due_date=None, priority=None):
        """Update a task owned by the user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if due_date is not None:
            task.due_date = due_date
        if priority is not None:
            task.priority = priority
        
        task.prepare_for_save(changed_by_id=user_id)
        return self.task_repo.save(task)

    def delete_task(self, task_id, user_id):
        """Delete a task owned by the user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False
        
        self.task_repo.delete(task)
        return True
