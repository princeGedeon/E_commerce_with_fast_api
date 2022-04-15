from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from fastapi import status
from models import User

config_credential=dotenv_values(".env")
pwd_Context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password):
    return pwd_Context.hash(password)

async def very_token(token:str):
    try:
        playload=jwt.decode(token,config_credential['SECRET'],algorithm='HS256')
        user=await User.get(id=playload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return user