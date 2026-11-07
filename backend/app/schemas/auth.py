from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User registration request
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# User login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


# User information returned by the API
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email: EmailStr
    role: str


# JWT token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"