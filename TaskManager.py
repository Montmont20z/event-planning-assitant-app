from BaseTracker import *
# task_manager.py - Task management class
class TaskManager(BaseTracker):
    """Manages event tasks - demonstrates inheritance and encapsulation"""
    
    def __init__(self):
        super().__init__("data/tasks.json")
    
    def add_task(self, description, priority="Medium", due_date=""):
        """Add a new task - demonstrates string processing and validation"""
        # String processing - clean input
        description = description.strip()
        
        if not description:  # Selection - validation
            raise ValueError("Task description is required")
        
        # Collections - dictionary for task data
        task = {
            'id': len(self.data) + 1,
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'completed': False,
            'created_date': datetime.now().strftime("%Y-%m-%d")
        }
        
        self.data.append(task)
        self.save_data()
    
    def mark_completed(self, task_id):
        """Mark task as completed - demonstrates loops and selection"""
        for task in self.data:  # Loop
            if task['id'] == task_id:  # Selection
                task['completed'] = True
                task['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_data()
                return True
        return False
    
    def get_task_summary(self):
        """Get task completion summary - demonstrates collections and loops"""
        total = len(self.data)
        completed = 0
        
        for task in self.data:  # Loop
            if task.get('completed', False):  # Selection
                completed += 1
        
        # Collections - tuple for return values
        return (total, completed, total - completed)
