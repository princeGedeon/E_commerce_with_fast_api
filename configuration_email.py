from fastapi import (BackgroundTasks,UploadFile,File,Form,Depends,HTTPException,status)
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from pydantic.typing import List
import jwt
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
    token_data={
        "id":instance.id,
        "username":instance.username
    }
    token=jwt.encode(token_data,conf_creditials['SECRET'],algorithm='HS256')

    template=f"""
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <div style="display:flex;align-items:center;justify-content:center;flex-direction:column">
            
            <h3>Account Verification</h3>
            <br>
            <p>THanks for Choosing PrinceGShop,please click on the button to verify your account</p>
            <a style="margin-top:1rem;padding:1rem;border-raduis:0.5rem;font-size:1rem;text-decoration:none;background:#0275d8;color:white;" href="http://localhost:8000/?token={token}">Verify your email</a>
            
            
            <p>Please kindly ignore this email if you did not register for PrincegShop.Thanks</p>
            </div>
        </body>
    
    </html>
    """

    message=MessageSchema(
        subject="PrinceGShop Account Verification Email",
        recipients=email,#LIST OF EMAIL
        body=template,
        subtype="html"
    )

    fm=FastMail(conf)
    await fm.send_message(message=message)