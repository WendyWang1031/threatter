from typing import Optional
from model.model import *
import uuid

def generate_short_uuid(content_type: str) -> str:
    prefix = {
        'Post': 'P-',
        'Comment': 'C-',
        'Reply': 'R-'
    }.get(content_type, 'O-')
    
    short_uuid = str(uuid.uuid4())[:8]  
    return f"{prefix}{short_uuid}"

def validate(value: Optional[str]) -> Optional[str] :
            if value is None:
                return None
            return value.strip() or None # 避免用戶輸入' '去除空白後沒有值