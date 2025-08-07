from common.repositories.base import BaseRepository
from common.models.task import Task


class TaskRepository(BaseRepository):
    MODEL = Task
    
    def get_tasks_with_title_like(self, query_params, title_search):
        """
        Get tasks with case-insensitive title search using LIKE query
        """
        all_tasks = self.get_many(query_params)
        
        if not title_search:
            return all_tasks
        
        title_search_lower = title_search.lower()
        filtered_tasks = []
        
        for task in all_tasks:
            if title_search_lower in task.title.lower():
                filtered_tasks.append(task)
        
        return filtered_tasks
