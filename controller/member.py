from model.model import *
from service.security import security_get_current_user
from db.member import *

from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse
import boto3


# def upload_file_to_s3(file: UploadFile , user_id: str):
#     s3_client = boto3.client('s3')
#     bucket_name = "taipei-day-trip-images"

#     file_key = f"avatars/{user_id}-avatar.jpg"
#     content_type = file.content_type
#     try:
#         s3_client.upload_fileobj(
#             file.file,
#             bucket_name,
#             file_key,
#             ExtraArgs={
#                 'ContentType': content_type  
#             }
#         )
#         return f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def update_member_data(
        member_data: MemberUpdateReq ,
        current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        
        if not current_user:
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response
        
        member_id = current_user["account_id"]
        fields_updated = False
       
        # 檢查是否有效的欄位更新
        if (member_data.name and member_data.name.strip()) or \
            (member_data.visibility and member_data.visibility.strip()) or \
            (member_data.self_intro and member_data.self_intro.strip()) or \
            (member_data.avatar and member_data.avatar.strip()):
                fields_updated = True
        print("member_data:",member_data)
        print("fields_updated:",fields_updated)
    

        if not fields_updated:
            error_response = ErrorResponse(error=True, message="At least one field must be updated")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response 

        
        result = db_update_member_data(member_id , member_data)
        if result is True:
            success_response = SuccessfulRes(success=True)
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=success_response.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to create member data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    
    
async def get_member_data(current_user: Optional[dict] , account_id : str ) -> JSONResponse :
    try:
        member_id = current_user["account_id"] if current_user else None
       
        member_detail = db_get_member_data(member_id , account_id)

        if member_detail is not None:
            response = JSONResponse(
            status_code = status.HTTP_200_OK,
            content=member_detail.dict()
            )
            return response
            
        else:
            error_response = ErrorResponse(error=True, message="No Member Data details found for user")
            response = JSONResponse (
                status_code=status.HTTP_404_NOT_FOUND, 
                content=error_response.dict())
            return response

        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response