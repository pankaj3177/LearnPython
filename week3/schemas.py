from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr