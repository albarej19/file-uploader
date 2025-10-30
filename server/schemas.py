from pydantic import BaseModel
from datetime import datetime
from typing import List

# Individual File Metadata Schema

class FileMetadataBase(BaseModel):
    id: int
    original_filename: str
    system_filename: str
    file_size_bytes: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Schema for the List of All Files (History Response)
class FileHistoryResponse(BaseModel):
    
    files: List[FileMetadataBase]


# Schema for the successful Upload Response
class FileUploadResponse(BaseModel):
    message: str
    id: int # REQUIRED by the schema, hence the error!
    original_filename: str
    system_filename: str
    file_size_bytes: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True