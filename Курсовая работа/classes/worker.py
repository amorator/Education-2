from re import match

class Worker():
    def __init__(self, id, name, speciality, experience=0):
        self.name = name
        self.speciality = speciality
        self.experience = float(experience)
        self.id = int(id)

    def json(self):
        return {"id": self.id, "name": self.name, "speciality": self.speciality, "experience": self.experience}

    def merge(self, w):
        if w.name != " ":
            self.name = w.name
        if w.speciality != " ":
            self.speciality = w.speciality
        if w.experience > self.experience:
            self.experience = w.experience
        return True

    def is_exp(x):
        return not (match(r'^\d+(?:\.\d+)?$', x) is None)
