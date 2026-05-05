from pydantic import BaseModel, Field, ConfigDict, EmailStr



class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr 
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes = True)