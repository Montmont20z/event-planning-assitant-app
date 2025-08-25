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

# guest_manager.py - Guest management class
class GuestManager(BaseTracker):
    """Manages guest list - demonstrates inheritance and encapsulation"""
    
    def __init__(self):
        super().__init__("data/guests.json")  # Inheritance - calling parent constructor
    
    def add_guest(self, name, email, phone=""):
        """Add a new guest - demonstrates string processing and collections"""
        # String processing - clean and validate input
        name = name.strip().title()  # Clean whitespace and capitalize
        email = email.strip().lower()  # Clean and normalize email
        
        # Selection - input validation
        if not name or not email:
            raise ValueError("Name and email are required")
        
        # Check for duplicates using loops and string processing
        for guest in self.data:
            if guest['email'].lower() == email.lower():
                raise ValueError("Guest with this email already exists")
        
        # Collections - dictionary for guest data
        guest = {
            'name': name,
            'email': email,
            'phone': phone.strip(),
            'rsvp': 'Pending',
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.data.append(guest)  # Collections - list operations
        self.save_data()
    
    def update_rsvp(self, email, status):
        """Update guest RSVP status - demonstrates loops and selection"""
        for guest in self.data:  # Loop through guests
            if guest['email'].lower() == email.lower():  # String processing
                guest['rsvp'] = status
                self.save_data()
                return True
        return False
    
    def get_rsvp_summary(self):
        """Get RSVP summary - demonstrates collections and loops"""
        summary = {'Confirmed': 0, 'Declined': 0, 'Pending': 0}  # Dictionary collection
        
        for guest in self.data:  # Loop through data
            status = guest.get('rsvp', 'Pending')
            if status in summary:  # Selection
                summary[status] += 1
        
        return summary

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

# budget_manager.py - Budget management class
class BudgetManager(BaseTracker):
    """Manages event budget - demonstrates inheritance and encapsulation"""
    
    def __init__(self):
        super().__init__("data/budget.json")
        # Collections - set of valid categories
        self.categories = {'Venue', 'Food', 'Decorations', 'Entertainment', 'Miscellaneous'}
    
    def add_expense(self, category, description, amount):
        """Add an expense - demonstrates string processing and validation"""
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
        """Get budget summary by category - demonstrates collections and loops"""
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

# main.py - Main application with GUI
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class EventPlannerApp:
    """Main application class - demonstrates GUI and encapsulation"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Event Planning Assistant")
        self.root.geometry("800x600")
        
        # Initialize managers - demonstrates encapsulation
        self.guest_manager = GuestManager()
        self.task_manager = TaskManager()
        self.budget_manager = BudgetManager()
        
        # Event date for countdown
        self.event_date = datetime.now() + timedelta(days=30)  # Default 30 days from now
        
        self.setup_gui()
        self.update_countdown()
    
    def setup_gui(self):
        """Setup the GUI - demonstrates GUI creation"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_guest_tab(notebook)
        self.create_task_tab(notebook)
        self.create_budget_tab(notebook)
        self.create_countdown_tab(notebook)
    
    def create_guest_tab(self, notebook):
        """Create guest management tab - demonstrates GUI and functions"""
        guest_frame = ttk.Frame(notebook)
        notebook.add(guest_frame, text="Guests")
        
        # Input frame
        input_frame = ttk.LabelFrame(guest_frame, text="Add Guest")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        # Entry widgets
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.guest_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.guest_name_var, width=30).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.guest_email_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.guest_email_var, width=30).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Phone:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.guest_phone_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.guest_phone_var, width=30).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="Add Guest", command=self.add_guest).grid(row=3, column=1, pady=5)
        
        # Guest list
        list_frame = ttk.LabelFrame(guest_frame, text="Guest List")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for guest list
        columns = ('Name', 'Email', 'Phone', 'RSVP')
        self.guest_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define column headings
        for col in columns:
            self.guest_tree.heading(col, text=col)
            self.guest_tree.column(col, width=150)
        
        self.guest_tree.pack(fill='both', expand=True)
        
        # RSVP buttons
        rsvp_frame = ttk.Frame(list_frame)
        rsvp_frame.pack(fill='x', pady=5)
        
        ttk.Button(rsvp_frame, text="Mark Confirmed", command=lambda: self.update_rsvp('Confirmed')).pack(side='left', padx=5)
        ttk.Button(rsvp_frame, text="Mark Declined", command=lambda: self.update_rsvp('Declined')).pack(side='left', padx=5)
        ttk.Button(rsvp_frame, text="Refresh", command=self.refresh_guests).pack(side='left', padx=5)
        
        self.refresh_guests()
    
    def create_task_tab(self, notebook):
        """Create task management tab"""
        task_frame = ttk.Frame(notebook)
        notebook.add(task_frame, text="Tasks")
        
        # Input frame
        input_frame = ttk.LabelFrame(task_frame, text="Add Task")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.task_desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.task_desc_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.task_priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.task_priority_var, 
                                     values=["Low", "Medium", "High"], state="readonly")
        priority_combo.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        
        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=2, column=1, pady=5)
        
        # Task list
        list_frame = ttk.LabelFrame(task_frame, text="Task List")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('ID', 'Description', 'Priority', 'Status')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=150)
        
        self.task_tree.pack(fill='both', expand=True)
        
        # Task buttons
        task_btn_frame = ttk.Frame(list_frame)
        task_btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(task_btn_frame, text="Mark Completed", command=self.complete_task).pack(side='left', padx=5)
        ttk.Button(task_btn_frame, text="Refresh", command=self.refresh_tasks).pack(side='left', padx=5)
        
        self.refresh_tasks()
    
    def create_budget_tab(self, notebook):
        """Create budget management tab"""
        budget_frame = ttk.Frame(notebook)
        notebook.add(budget_frame, text="Budget")
        
        # Input frame
        input_frame = ttk.LabelFrame(budget_frame, text="Add Expense")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Category:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.budget_category_var = tk.StringVar()
        category_combo = ttk.Combobox(input_frame, textvariable=self.budget_category_var,
                                     values=list(self.budget_manager.categories), state="readonly")
        category_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.budget_desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.budget_desc_var, width=30).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Amount:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.budget_amount_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.budget_amount_var, width=30).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=1, pady=5)
        
        # Expense list
        list_frame = ttk.LabelFrame(budget_frame, text="Expenses")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('Category', 'Description', 'Amount', 'Date')
        self.budget_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.budget_tree.heading(col, text=col)
            self.budget_tree.column(col, width=150)
        
        self.budget_tree.pack(fill='both', expand=True)
        
        # Summary frame
        summary_frame = ttk.Frame(list_frame)
        summary_frame.pack(fill='x', pady=5)
        
        ttk.Button(summary_frame, text="Refresh", command=self.refresh_budget).pack(side='left', padx=5)
        
        self.total_label = ttk.Label(summary_frame, text="Total: $0.00", font=('Arial', 12, 'bold'))
        self.total_label.pack(side='right', padx=5)
        
        self.refresh_budget()
    
    def create_countdown_tab(self, notebook):
        """Create countdown timer tab"""
        countdown_frame = ttk.Frame(notebook)
        notebook.add(countdown_frame, text="Countdown")
        
        # Event date frame
        date_frame = ttk.LabelFrame(countdown_frame, text="Event Date")
        date_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(date_frame, text="Event Date (YYYY-MM-DD):").pack(pady=5)
        self.event_date_var = tk.StringVar(value=self.event_date.strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(date_frame, textvariable=self.event_date_var, width=20)
        date_entry.pack(pady=5)
        
        ttk.Button(date_frame, text="Update Date", command=self.update_event_date).pack(pady=5)
        
        # Countdown display
        countdown_display = ttk.LabelFrame(countdown_frame, text="Time Remaining")
        countdown_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.countdown_label = ttk.Label(countdown_display, text="", font=('Arial', 24, 'bold'))
        self.countdown_label.pack(expand=True)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(countdown_frame, text="Event Summary")
        summary_frame.pack(fill='x', padx=5, pady=5)
        
        self.summary_text = tk.Text(summary_frame, height=8, width=50)
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.update_summary()
    
    def add_guest(self):
        """Add guest function - demonstrates exception handling"""
        try:
            name = self.guest_name_var.get()
            email = self.guest_email_var.get()
            phone = self.guest_phone_var.get()
            
            self.guest_manager.add_guest(name, email, phone)
            
            # Clear inputs
            self.guest_name_var.set("")
            self.guest_email_var.set("")
            self.guest_phone_var.set("")
            
            self.refresh_guests()
            messagebox.showinfo("Success", "Guest added successfully!")
            
        except Exception as e:  # Exception handling
            messagebox.showerror("Error", str(e))
    
    def update_rsvp(self, status):
        """Update RSVP status"""
        selection = self.guest_tree.selection()
        if not selection:  # Selection - check if item selected
            messagebox.showwarning("Warning", "Please select a guest")
            return
        
        item = self.guest_tree.item(selection[0])
        email = item['values'][1]  # Get email from selected row
        
        if self.guest_manager.update_rsvp(email, status):
            self.refresh_guests()
            messagebox.showinfo("Success", f"RSVP updated to {status}")
        else:
            messagebox.showerror("Error", "Failed to update RSVP")
    
    def refresh_guests(self):
        """Refresh guest list display - demonstrates loops"""
        # Clear existing items
        for item in self.guest_tree.get_children():  # Loop
            self.guest_tree.delete(item)
        
        # Add guests to tree
        for guest in self.guest_manager.data:  # Loop through data
            self.guest_tree.insert('', 'end', values=(
                guest['name'], guest['email'], 
                guest.get('phone', ''), guest.get('rsvp', 'Pending')
            ))
    
    def add_task(self):
        """Add task function"""
        try:
            description = self.task_desc_var.get()
            priority = self.task_priority_var.get()
            
            self.task_manager.add_task(description, priority)
            
            self.task_desc_var.set("")
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task added successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def complete_task(self):
        """Mark task as completed"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = self.task_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        if self.task_manager.mark_completed(task_id):
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task marked as completed!")
        else:
            messagebox.showerror("Error", "Failed to update task")
    
    def refresh_tasks(self):
        """Refresh task list display"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        for task in self.task_manager.data:
            status = "Completed" if task.get('completed', False) else "Pending"
            self.task_tree.insert('', 'end', values=(
                task['id'], task['description'], 
                task.get('priority', 'Medium'), status
            ))
    
    def add_expense(self):
        """Add expense function"""
        try:
            category = self.budget_category_var.get()
            description = self.budget_desc_var.get()
            amount = self.budget_amount_var.get()
            
            self.budget_manager.add_expense(category, description, amount)
            
            self.budget_category_var.set("")
            self.budget_desc_var.set("")
            self.budget_amount_var.set("")
            
            self.refresh_budget()
            messagebox.showinfo("Success", "Expense added successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_budget(self):
        """Refresh budget display"""
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)
        
        total = 0
        for expense in self.budget_manager.data:
            self.budget_tree.insert('', 'end', values=(
                expense['category'], expense['description'],
                f"${expense['amount']:.2f}", expense['date']
            ))
            total += expense['amount']
        
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def update_event_date(self):
        """Update event date"""
        try:
            date_str = self.event_date_var.get()
            self.event_date = datetime.strptime(date_str, "%Y-%m-%d")
            messagebox.showinfo("Success", "Event date updated!")
            self.update_countdown()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
    
    def update_countdown(self):
        """Update countdown timer - demonstrates loops and selection"""
        now = datetime.now()
        
        if self.event_date > now:  # Selection - check if event is in future
            delta = self.event_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            countdown_text = f"{days} days, {hours} hours, {minutes} minutes"
        else:  # Selection - else condition
            countdown_text = "Event has passed!"
        
        self.countdown_label.config(text=countdown_text)
        self.update_summary()
        
        # Schedule next update in 60 seconds
        self.root.after(60000, self.update_countdown)
    
    def update_summary(self):
        """Update event summary - demonstrates string processing and functions"""
        # Get summaries from managers
        guest_summary = self.guest_manager.get_rsvp_summary()
        task_total, task_completed, task_pending = self.task_manager.get_task_summary()
        budget_summary, budget_total = self.budget_manager.get_budget_summary()
        
        # String processing - build summary text
        summary_text = f"""EVENT PLANNING SUMMARY
========================

GUESTS:
• Total Invited: {len(self.guest_manager.data)}
• Confirmed: {guest_summary.get('Confirmed', 0)}
• Declined: {guest_summary.get('Declined', 0)}
• Pending: {guest_summary.get('Pending', 0)}

TASKS:
• Total Tasks: {task_total}
• Completed: {task_completed}
• Remaining: {task_pending}

BUDGET:
• Total Expenses: ${budget_total:.2f}
"""
        
        # Add budget breakdown if there are expenses
        if budget_summary:  # Selection
            summary_text += "\nBudget by Category:\n"
            for category, amount in budget_summary.items():  # Loop through dictionary
                summary_text += f"• {category}: ${amount:.2f}\n"
        
        # Update summary display
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', summary_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    try:
        app = EventPlannerApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
