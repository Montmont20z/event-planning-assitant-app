# base_tracker.py - Base class for inheritance
import json
import os
from datetime import datetime

class BaseTracker:
    """Base class for all tracker components - demonstrates inheritance"""
    
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.load_data()
    
    def load_data(self):
        """Load data from file - demonstrates file processing and exception handling"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    self.data = json.load(file)
            else:
                self.data = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = []
    
    def save_data(self):
        """Save data to file - demonstrates file processing and exception handling"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def search_items(self, search_term):
        """Search functionality - demonstrates string processing and loops"""
        if not search_term:  # Selection - if condition
            return self.data
        
        results = []
        for item in self.data:  # Loop through data
            # String processing - convert to lowercase for case-insensitive search
            if search_term.lower() in str(item).lower():
                results.append(item)
        return results

