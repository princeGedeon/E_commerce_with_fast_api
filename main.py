from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import User, user_pydanticIn, user_pydantic, Business, business_pydantic
from authentication import (get_hashed_password)

#Signal
from tortoise.signals import post_save
from typing import List,Optional,Type
from tortoise import BaseDBAsyncClient
app=FastAPI()

@post_save(User)
async def create_business(
        sender:"Type[User]",
        instance:User,
        created:bool,
        using_db:'Optional[BaseDBAsyncClient]',
        update_fields:List[str]
)->None:
    if created:
        busness_obj=await Business.create(
            name=instance.username,owner=instance
        )
        await business_pydantic.from_tortoise_orm(busness_obj)
        #Send email
@app.get("/")
async def index():
    return {"Message":"Hello world"}

register_tortoise(
                  app,
                  db_url="sqlite://database.sqlite3",
                  modules={"models" : ["models"]},
                  add_exception_handlers=True,
                  generate_schemas=True
                  )

@app.post("/user/registration")
async def user_registration(user:user_pydanticIn):
    user_info=user.dict(exclude_unset=True)
    user_info["password"]=get_hashed_password(user_info["password"])
    user_obj=await  User.create(**user_info)
    new_user=await  user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status":"ok",
        "data":f"Hello {new_user.username}, thanks for choosing our Services.Please check your email inbox and click link to confirm your registration."
    }
