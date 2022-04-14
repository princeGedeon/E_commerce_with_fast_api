from fastapi import (BackgroundTasks,UploadFile,File,Form,Depends,HTTPException,status)
from  fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from pydantic.typing import List

from models import User

conf_creditials=dotenv_values(".env")
conf=ConnectionConfig(
    MAIL_USERNAME=conf_creditials["EMAIL"],
    MAIL_PASSWORD=conf_creditials["PASS"],
    MAIL_FROM=conf_creditials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

class EMailSchema(BaseModel):
    email:List[EmailStr]

async def send_email(email:EMailSchema,instance:User):
    pass