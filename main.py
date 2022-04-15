from fastapi import FastAPI, Request, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from fastapi import status
from models import User, user_pydanticIn, user_pydantic, Business, business_pydantic
from authentication import (get_hashed_password,very_token)

#Signal
from tortoise.signals import post_save
from typing import List,Optional,Type
from tortoise import BaseDBAsyncClient
from fastapi.responses import HTMLResponse
#Templates
from fastapi.templating import  Jinja2Templates

app=FastAPI()
register_tortoise(
                  app,
                  db_url="sqlite://database.sqlite3",
                  modules={"models" : ["models"]},
                  add_exception_handlers=True,
                  generate_schemas=True
                  )



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

templates=Jinja2Templates(directory="templates")

@app.get('/verification',response_class=HTMLResponse)
async def email_verification(request:Request,token:str):
    user=await very_token(token)
    if user and user.is_verified:
        user.is_verified=True
        await user.save()
        return templates.TemplateResponse("verification.html",{"request":request,"username":user.username})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.get("/")
async def index():
    return {"Message":"Hello world"}



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
