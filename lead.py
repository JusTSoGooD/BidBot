import string, random


class Lead:
    id = None
    name = None
    time = None
    price = None
    description = None
    photo = None
    video = None

    # TODO:придумать айди для каждого лида
    def __init__(self, id):
        letters = string.ascii_uppercase
        self.id = ''.join(random.choice(letters) for i in range(12))


class LeadManager:
    leads = []

    def add_lead(self, lead):
        self.leads.append(lead)

    def get_lead(self, id):
        pass
