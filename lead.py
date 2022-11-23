import string, random

<<<<<<< HEAD
=======
import database

>>>>>>> testBrunch

class Lead:
    id = None
    name = None
    time = None
    price = None
    description = None
    photo = None
    video = None


    def __init__(self, id):
        letters = string.ascii_uppercase
        self.id = ''.join(random.choice(letters) for i in range(12))

    def __init__(self):
        letters = string.ascii_uppercase
        self.id = ''.join(random.choice(letters) for i in range(12))

class LeadManager:
    leads = []

    def add_lead(self, lead):
        self.leads.append(lead)

