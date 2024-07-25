from pydantic import BaseModel, Field , field_validator
from typing import List , Optional 
from datetime import datetime

class PostData(BaseModel):
    content: Optional[str] = Field(default=None, example="這是留言板測試文字內容")
    image_url: Optional[str]= Field(default=None, example="http://123456789/images/92-0.jpg")

class PostDataRequest(BaseModel):
    content: Optional[str] = Field(..., example="這是留言板測試文字內容")

class PostGetResponse(BaseModel):
    ok: bool
    data: List[PostData]

class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str

# 用戶
class UserReadDetail(BaseModel):
    id: str = Field(...,example=1)
    name: str = Field(... , example="彭彭彭")
    email: str = Field(... , example="ply@ply.com")				

class UserLoginRequest(BaseModel):
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")
    
    @field_validator("*")
    def validate_login_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Login Input Value can not be blank.")
        return v

class UserCreateRequest(BaseModel):
    name: str = Field(... , example="彭彭彭")
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

class SuccessfulResponseForMemberRegister(BaseModel):
    ok : bool = Field(..., description = "註冊成功")

class SuccessfulResponseForMember(BaseModel):
    data : UserReadDetail = Field(..., description = "取得當前登入資訊")

class SuccessfulResponseForMemberBase(BaseModel):
    token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

class ErrorResponse(BaseModel):
    error : bool = Field(True, description = "指示是否為錯誤響應")
    message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")



# 登入相關Error Response
class ServiceError(BaseModel):
     error : bool
     status : int 
     error_code : str
     error_message :str

class ForbiddenError(ServiceError):
     error : bool = Field(True , description="錯誤")
     status : int = Field(403 , description = "403-禁止訪問")
     error_code : str = Field("403-001" , description = "403-禁止訪問")
     error_message : str = Field("無權限" , description = "該用戶並無權限")


# 會員頁面
class MemberDataRequest(BaseModel):
    name: Optional[str] = Field(None, example="彭彭彭")
    email: Optional[str] = Field(None, example="ply@ply.com")
    phone: Optional[str] = Field(None, example="0912345678")
    

    @field_validator("*")
    def validate_member_data_space(cls , v):
        if v is not None and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v
    
    @field_validator("email")
    def validate_member_data_email(cls , v):
        if v is not None and "@" not in v:
             raise ValueError("Email must included '@'")
        return v

    @field_validator("phone")
    def validate_member_data_phone(cls , v):
         if v is not None:
            if not v.startswith("09"):
                raise ValueError("Phone number must start with 09")
            if len(v) != 10:
                raise ValueError("Phone number must be 10 digits long")
         return v


class MemberData(BaseModel):
    name: str = Field(..., example="彭彭彭")
    email: str = Field(..., example="ply@ply.com")
    phone_number: Optional[str] = Field(None, example="0912345678")
    avatar: Optional[str]= Field(None, example="http://123456789/images/92-0.jpg")

class MemberGetResponse(BaseModel):
    ok: bool
    data: MemberData

class MemberUpdateResponse(BaseModel):
    ok: bool = Field(..., example="會員更新成功")


