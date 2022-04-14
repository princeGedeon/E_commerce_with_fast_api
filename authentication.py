from passlib.context import CryptContext
pwd_Context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password):
    return pwd_Context.hash(password)

