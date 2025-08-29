from BaseTracker import *
# budget_manager.py - Budget management class
class BudgetManager(BaseTracker):
    """Manages event budget - inheritance and encapsulation"""
    
    def __init__(self):
        super().__init__("data/budget.json")
        # Collections - set of valid categories
        self.categories = {'Venue', 'Food', 'Decorations', 'Entertainment', 'Miscellaneous'}
    
    def add_expense(self, category, description, amount):
        """Add an expense - string processing and validation"""
        # String processing - clean inputs
        category = category.strip().title()
        description = description.strip()
        
        # Selection - validation
        if category not in self.categories:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(self.categories)}")
        
        if not description:
            raise ValueError("Description is required")
        
        try:
            amount = float(amount)  # Exception handling for conversion
        except ValueError:
            raise ValueError("Amount must be a valid number")
        
        if amount <= 0:  # Selection
            raise ValueError("Amount must be positive")
        
        # Collections - dictionary for expense
        expense = {
            'id': len(self.data) + 1,
            'category': category,
            'description': description,
            'amount': amount,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        
        self.data.append(expense)
        self.save_data()
    
    def get_budget_summary(self):
        """Get budget summary by category - collections and loops"""
        summary = {}  # Dictionary collection
        total = 0
        
        for expense in self.data:  # Loop through expenses
            category = expense['category']
            amount = expense['amount']
            
            # Collections - dictionary operations
            if category not in summary:
                summary[category] = 0
            summary[category] += amount
            total += amount
        
        return summary, total
