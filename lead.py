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
        self.id = id


class LeadManager:
    leads = []

    def add_lead(self, lead):
        self.leads.append(lead)

    def get_lead(self, id):
        pass
