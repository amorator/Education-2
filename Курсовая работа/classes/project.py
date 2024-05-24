from flask import abort

class Project():
    stages = ["Провален", "Анализ", "Проектирование", "Разработка", "Тестирование", "Внедрение", "Сдача проекта", "Завершен"]
    def __init__(self, id, name, wid, description='', stage=1):
        self.name = name
        self.description = description
        self.stage = int(stage)
        self.id = int(id)
        self.wid = int(wid)

    def json(self):
        return {"id": self.id, "wid": self.wid, "name": self.name, "description": self.description, "stage": self.stages[self.stage]}

    def merge(self, p):
        if p.verify_stage():
            self.stage = p.stage
        elif p.stage != -1:
            return False
        if p.wid and p.wid > 0:
            self.wid = p.wid
        if p.name != " ":
            self.name = p.name
        if p.description != " ":
            self.description = p.description
        return True

    def verify_stage(self):
        if self.stage <= 0 or self.stage >= len(self.stages) - 1:
            return False
        return True

    def fail(self):
        if self.verify_stage():
            self.stage = 0
            return True
        return False

    def next_stage(self):
        if self.verify_stage():
            self.stage += 1
            return True
        return False

    def stat(self):
        if self.stage == len(self.stages) - 1:
            return 1
        elif self.stage == 0:
            return -1
        else:
            return 0
