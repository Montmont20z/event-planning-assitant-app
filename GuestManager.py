from BaseTracker import *

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
