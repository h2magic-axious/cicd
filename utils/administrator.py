import bcrypt
import jwt

from utils.environments import Env


def build_token():
    data = {
        "username": Env.ADMIN_USER,
        "password": Env.ADMIN_PASS
    }
    return jwt.encode(data, Env.SECRET_KEY, algorithm=Env.ALGORITHM)


def check_admin(username: str, pwd: str):
    return username == Env.ADMIN_USER and bcrypt.checkpw(pwd.encode(), Env.ADMIN_PASS.encode())


def check_token(token):
    try:
        data = jwt.decode(token, Env.SECRET_KEY, algorithms=[Env.ALGORITHM])
        return data["username"] == Env.ADMIN_USER and data["password"] == Env.ADMIN_PASS
    except Exception as e:
        print(e)
        return False
