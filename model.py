from datetime import datetime

from tortoise import Model, fields
from pydantic import BaseModel

class User(Model):
    id=fields.IntField(pk=True,index=True)
    username=fields.CharField(max_length=20,null=False)
    email=fields.CharField(max_length=200,null=False)
    password=fields.CharField(max_length=100,null=False)
    is_verified=fields.BooleanField(default=False)
    join_data=fields.DatetimeField(default=datetime.utcnow())

class Busness(Model):
    id=fields.IntField(pk=True,index=True)
    name=fields.CharField(max_length=20,null=False,unique=True)
    city=fields.CharField(max_length=100,null=False,default="Non spécifié")
    region=fields.CharField(max_length=100,null=False,default="Non spécifié")
