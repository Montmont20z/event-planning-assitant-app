from ManagerBase import *

class GuestManager(ManagerBase):
    # manager guest list

    def __init__(self, filename):
        super().__init__(filename)
        self._guest = []

    def print_hello(self):
        print(f"Filename: {self.file}")

    


