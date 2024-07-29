from pydantic import BaseModel, Field , field_validator 


# 用戶 / 註冊、登入、確認登入狀況

class UserRegisterReq(BaseModel):
    name: str = Field(... , example="王黑喵")
    account_id: str = Field(... , example="meow20240728")
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")	
    
    @field_validator("*")
    def validate_register_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v
    
    @field_validator("email")
    def validate_email(cls , v):
        if "@" not in v :
             raise ValueError("Email must included '@'")
        return v
    
class UserCheckExistReq(BaseModel):
    account_id: str = Field(... , example="meow20240728")
    email: str = Field(... , example="ply@ply.com")
    
    @field_validator("*")
    def validate_register_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v
    
    @field_validator("email")
    def validate_email(cls , v):
        if "@" not in v :
             raise ValueError("Email must included '@'")
        return v

class UserGetCheck(BaseModel):
    name: str = Field(... , example="王黑喵")
    account_id: str = Field(... , example="meow20240728")		

class UserPutReq(BaseModel):
    account_id: str = Field(... , example="meow20240728")
    password: str = Field(... , example="12345678")
    
    @field_validator("*")
    def validate_login_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Login Input Value can not be blank.")
        return v



class Token(BaseModel):
    token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

class SuccessfulResponseForRegister(BaseModel):
    success : bool = Field(..., description = "註冊成功")
