from datetime import datetime

from tortoise import Model, fields
from pydantic import BaseModel

class User(Model):
    id=fields.IntField(pk=True,index=True)
    username=fields.CharField(max_length=20,null=False)
    email=fields.CharField(max_length=200,null=False)
    password=fields.CharField(max_length=100,null=False)
    is_verified=fields.BooleanField(default=False)
    join_data=fields.DatetimeField(default=datetime.utcnow)

class Busness(Model):
    id=fields.IntField(pk=True,index=True)
    name=fields.CharField(max_length=20,null=False,unique=True)
    city=fields.CharField(max_length=100,null=False,default="Non spécifié")
    region=fields.CharField(max_length=100,null=False,default="Non spécifié")
    description=fields.TextField(null=True)
    logo=fields.CharField(max_length=200,null=False,default="default.jpg")
    owner=fields.ForeignKeyField("models.User",related_name="busness")

class Product(Model):
    id=fields.IntField(pk=True,index=True)
    name=fields.CharField(max_length=100,null=False,index=True)
    category=fields.CharField(max_length=30,index=True)
    original_price=fields.DecimalField(max_digits=12,decimal_places=2)
    new_price=fields.DecimalField(max_digits=12,decimal_places=2)
    percentage_discount=fields.IntField()
    offer_expiration=fields.DateField(default=datetime.utcnow)
    image=fields.CharField(max_length=200,null=False,default="default.jpg")
