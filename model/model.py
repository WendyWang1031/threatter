from pydantic import BaseModel, Field , field_validator , model_validator
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

# error
class ErrorResponse(BaseModel):
    error : bool = Field(True, description = "指示是否為錯誤響應")
    message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")

# 登入相關Error Response
class ServiceError(BaseModel):
    error : bool
    status : int 
    message :str

# 共用
class SuccessfulRes(BaseModel):
    success : bool = Field(..., description = "成功")
    

# Member 會員
class MemberBase(BaseModel):
    name: str = Field(..., example="王黑喵")
    account_id: str = Field(... , example="abc123456")
    avatar: Optional[str]= Field(None, example="http://123456789/images/92-0.jpg")

    @field_validator("name" , "account_id")
    def validate_space(cls , v):
        if v is not None and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v  

class MemberDetail(MemberBase):
    self_intro: Optional[str] = Field(None, example="安安你好我是黑貓")
    fans_counts: int = Field(default=0, example=1456000)
    visibility: str = Field(..., example="public", description="帳號的權限，例如 public, private")

class MemberUpdateReq(BaseModel):
    name: Optional[str] = Field(None, example="王黑喵")
    visibility: str = Field(..., example="public", description="帳號的權限，例如 public, private")
    self_intro: Optional[str] = Field(None, example="安安你好我是黑貓")
    avatar: Optional[str]= Field(None, example="http://123456789/images/92-0.jpg")
    
    @field_validator("self_intro" , "name")
    def check_length(cls, v):
        if v and len(v) > 100:
            raise ValueError("自我介紹或名字不能超過100個字")
        return v

# Follow 追蹤  
class FollowReq(BaseModel):
    follow: bool
    account_id: str

class FollowAns(BaseModel):
    accept: bool
    account_id: str

class FollowMember(BaseModel):
    user: MemberBase
    follow_state: str = Field(default="None", example="following, pending, beingFollow ,None") # following, pending, beingFollow

class FollowMemberListRes(BaseModel):
    next_page: Optional[int] = Field(None, description="下一頁的頁面，如果沒有更多頁為None")
    fans_counts: int = Field(default=0, example=368)
    data: List[FollowMember]

# Post 貼文  
class Media(BaseModel):
    images: Optional[str] = None
    videos: Optional[str] = None
    audios: Optional[str] = None
    



class PostContent(BaseModel):
    text: Optional[str] = Field(None,example="這是貼文的內容，有什麼想說的？", max_length=500)
    media: Optional[Media] = None

    # 驗證一整個 Model CLASS model_validator，所以可以抓取所有欄位
    @model_validator(mode='after')
    def check(cls, values):

        if not values.text and not values.media:
            raise ValueError('text and media cannot both be empty')
        
        return values
    


class PostCounts(BaseModel):
    like_counts: int = Field(default=0, example=6568)
    reply_counts: int = Field(default=0, example=590)
    forward_counts: int = Field(default=0, example=56)
    
    @field_validator("*")
    def check_positive(cls, v):
        if v < 0:
            raise ValueError("計數不能為負數")
        return v

class PostCreateReq(BaseModel):
    post_parent_id: Optional[str] = Field(None,example="abc123456", description="回覆該貼文的id，如果是None則是自己的貼文")
    content: PostContent
    visibility: str = Field(...,example="public" , description="觀賞貼文的權限，例如 public, private, friends")

class ParentPostId(BaseModel):
    account_id: str = Field(... , example="abc123456")
    post_id: str = Field(... , example="ec-abc123456")
    
class Post(BaseModel):
    post_id: str = Field(... , example="ec-abc123456")
    parent: Optional[ParentPostId]
    created_at: datetime = Field(... , example="2024/07/28:00:15:43:56")
    user: MemberBase  
    content: PostContent
    visibility: str = Field(..., example="public", description="觀賞貼文的權限，例如 public, private, friends")
    like_state: bool = Field(default=False , example="未按讚")
    counts: PostCounts

    
class PostListRes(BaseModel):
    next_page: Optional[int] = Field(None, description="下一頁的頁面，如果沒有更多頁為None")
    data: List[Post]

class Comment(BaseModel):
    comment_id: str = Field(... , example="ec-abc45678")
    user: MemberBase
    content: PostContent
    created_at: datetime = Field(... , example="2024/07/28:00:15:43:56")
    like_state: bool = Field(default=False , example="未按讚")
    counts: PostCounts

class CommentDetail(BaseModel):
    comment: Comment
    replies: Optional[List[Comment]] = None

class CommentDetailListRes(BaseModel):
    next_page: Optional[int] = Field(None, description="下一頁的頁面，如果沒有更多頁為None")
    data: List[CommentDetail]

class LikeReq(BaseModel):
    like: bool = Field(... , example="對貼文按讚")

class LikeRes(BaseModel):
    total_likes: int = Field(... , example="1")


class CommentReq(BaseModel):
    content:PostContent
    visibility: str = Field(... , example="public")

# User 用戶
class MemberDataRequest(BaseModel):
    name: Optional[str] = Field(None, example="王黑喵")
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

