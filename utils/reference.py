import os
import subprocess

from fastapi.templating import Jinja2Templates

from tortoise.models import Model
from tortoise import fields

Template = Jinja2Templates(directory="templates")


class AbstractBaseModel(Model):
    id: int = fields.IntField(pk=True)

    class Meta:
        abstract = True


class AbstractCreateAtModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


def try_to_do(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            print(e)
            return False, str(e)

    return inner


def random_string(length=6):
    return os.urandom(length).hex()


def response_result(code, result):
    return {"code": code, "result": result}


def execute(cmd):
    print(f"Exec: {cmd}")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line.decode().strip())

    p.wait()
