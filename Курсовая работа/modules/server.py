from flask import Flask
from flask_cors import CORS

from modules.SQLUtils import SQLUtils

class Server(Flask):
    def __init__(self, name=__name__):
        super().__init__(name)
        CORS(self, resources={r'*': {'origins': '*'}})
        self.secret_key = 'achudwshoiqxjqi@eowe1J2'
        self.config['SESSION_TYPE'] = 'filesystem'
        self.config['JSON_AS_ASCII'] = False
        self.init()

    def check_id(self,id):
        if type(id) != int:
            return 'Идентификатор может быть только целым числом!', 400

    def init(self):
        self.sql = SQLUtils()
        self.port = int(self.sql.config['server']['port'])

    def start(self):
        self.run(host='0.0.0.0', port=self.port, threaded=True, debug=False)
