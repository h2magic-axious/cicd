import datetime

import jwt

from utils.environments import Env
import pickle
import base64


class Administrator:
    def __init__(self):
        self.username = Env.ADMIN_USER
        self.password = Env.ADMIN_PASS

    def check(self, username, password):
        return self.username == username and self.password == password

    def __ne__(self, other):
        return self.username != other.username or self.password != other.password

    @property
    def token(self):
        data = {
            "instance": base64.b64encode(pickle.dumps(self)).decode()
        }
        return jwt.encode(data, Env.SECRET_KEY, algorithm=Env.ALGORITHM)

    @staticmethod
    def parse(token: str):
        data = jwt.decode(token, Env.SECRET_KEY, algorithms=[Env.ALGORITHM])
        return pickle.loads(base64.b64decode(data["instance"]))


administrator = Administrator()
