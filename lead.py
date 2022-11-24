import string, random
import database


class Lead:
    id = None
    name = None
    end_time = None
    price = None
    description = None
    photo = None
    video = None

    def __init__(self):
        letters = string.ascii_uppercase
        self.id = ''.join(random.choice(letters) for i in range(12))


class LeadManager:
    leads = []

    def add_lead(self, lead):
        self.leads.append(lead)
