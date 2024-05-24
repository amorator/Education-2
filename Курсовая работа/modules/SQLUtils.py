from sqlite3 import connect, IntegrityError

from classes.worker import Worker
from classes.project import Project
from modules.settings import Config

class SQL(Config):
    def __init__(self):
        super().__init__()

    def with_conn(func):
        def _with_conn(self, command, args=[]):
            self.conn = connect(self.config['db']['path'])
            self.cur = self.conn.cursor()
            data = func(self, command, args)
            self.cur.close()
            self.conn.close()
            return data
        return _with_conn

    @with_conn
    def execute_non_query(self, command, args=[]):
        self.cur.execute(command, args)
        self.conn.commit()

    @with_conn
    def execute_scalar(self, command, args=[]):
        self.cur.execute(command, args)
        return self.cur.fetchone()

    @with_conn
    def execute_query(self, command, args=[]):
        self.cur.execute(command, args)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

class SQLUtils(SQL):
    def __init__(self):
        super().__init__()
        self.init_tables()

    def init_tables(self):
        self.execute_non_query(f"CREATE TABLE IF NOT EXISTS {self.config['db']['prefix']}Workers (id INTEGER UNIQUE, name TEXT NOT NULL UNIQUE, speciality TEXT NOT NULL, experience REAL NOT NULL, PRIMARY KEY (id AUTOINCREMENT));")
        self.execute_non_query(f"CREATE TABLE IF NOT EXISTS {self.config['db']['prefix']}Projects (id INTEGER UNIQUE, name TEXT NOT NULL UNIQUE, wid INTEGER NOT NULL, description TEXT DEFAULT \"\", stage TEXT NOT NULL, PRIMARY KEY (id AUTOINCREMENT), FOREIGN KEY(wid) REFERENCES {self.config['db']['prefix']}Workers(id) ON DELETE RESTRICT);")

    def project_all(self, json=True):
        data = self.execute_query(f"SELECT * FROM {self.config['db']['prefix']}Projects;")
        if json:
            return [Project(*i).json() for i in data] if data else None
        else:
            return [Project(*i) for i in data] if data else None

    def project_by_id(self, id, json=False):
        data = self.execute_query(f"SELECT * FROM {self.config['db']['prefix']}Projects WHERE id = (?);", [id])
        return Project(*data[0]).json() if json and data else Project(*data[0]) if data else None

    def project_add(self, p):
        try:
            self.execute_non_query(f"INSERT INTO {self.config['db']['prefix']}Projects(name, wid, description, stage) VALUES((?), (?), (?), (?));", [p.name, p.wid, p.description, p.stage])
            return True
        except IntegrityError:
            self.close()
            return False

    def project_update(self, p):
        try:
            self.execute_non_query(f"UPDATE {self.config['db']['prefix']}Projects SET name = (?), wid = (?), description = (?), stage = (?) WHERE id = (?);", [p.name, p.wid, p.description, p.stage, p.id])
            return True
        except IntegrityError:
            self.close()
            return False

    def project_delete(self, id):
        try:
            self.execute_non_query(f"DELETE FROM {self.config['db']['prefix']}Projects WHERE id = (?);", [id])
            return True
        except IntegrityError:
            self.close()
            return False

    def project_by_wid(self, wid):
        data = self.execute_query(f"SELECT * FROM {self.config['db']['prefix']}Projects WHERE wid = (?);", [wid])
        return [Project(*i) for i in data] if data else None

    def worker_all(self, json=True):
        data = self.execute_query(f"SELECT * FROM {self.config['db']['prefix']}Workers;")
        if json:
            return [Worker(*i).json() for i in data] if data else None
        else:
            return [Worker(*i) for i in data] if data else None

    def worker_by_id(self, id, json=False):
        data = self.execute_query(f"SELECT * FROM {self.config['db']['prefix']}Workers WHERE id = (?);", [id])
        return Worker(*data[0]).json() if json and data else Worker(*data[0]) if data else None

    def worker_add(self, w):
        try:
            self.execute_non_query(f"INSERT INTO {self.config['db']['prefix']}Workers(name, speciality, experience) VALUES((?), (?), (?));", [w.name, w.speciality, w.experience])
            return True
        except IntegrityError:
            self.close()
            return False

    def worker_update(self, w):
        try:
            self.execute_non_query(f"UPDATE {self.config['db']['prefix']}Workers SET name = (?), speciality = (?), experience = (?) WHERE id = (?);", [w.name, w.speciality, w.experience, w.id])
            return True
        except IntegrityError:
            self.close()
            return False

    def worker_delete(self, id):
        try:
            self.execute_non_query(f"DELETE FROM {self.config['db']['prefix']}Workers WHERE id = (?);", [id])
            return True
        except IntegrityError:
            self.close()
            return False
