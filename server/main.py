import os
import shutil
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models 
import schemas
from typing import List
# --- IMPORTANT: NEW CORS IMPORTS ---
from starlette.middleware.cors import CORSMiddleware 


# database initialization
models.Base.metadata.create_all(bind=engine)


# FILE STORAGE SETUP
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FASTAPI APP INITIALIZATION
app = FastAPI()

# -----------------
# CORS MIDDLEWARE FIX - THIS IS THE CRITICAL SECTION
# -----------------
# Match the origin to your frontend's running address (http://127.0.0.1:5500)
origins = [
    "http://127.0.0.1:5500",  # <--- YOUR FRONTEND ADDRESS
    "http://localhost:5500", 
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Allow requests from the defined list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API ROUTE 1: UPLOAD DOCUMENT (POST endpoint for file uploads)
@app.post("/upload-document", response_model=schemas.FileUploadResponse)
async def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Generating unique system filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    now = datetime.now()
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not save file to disk. Error: {e}")
    finally:
        await file.close()

    try:
        db_file = models.FileMetadata(
            original_filename=file.filename,
            system_filename=unique_filename,
            file_size_bytes=file_size,
            uploaded_at=now
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return {
            "message": "File uploaded successfully",
            "id": db_file.id,
            "original_filename": db_file.original_filename,
            "system_filename": db_file.system_filename,
            "file_size_bytes": db_file.file_size_bytes,
            "uploaded_at": db_file.uploaded_at
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File saved but metadata failed to save. Error: {e}")
        
# API ROUTE 2: FILE HISTORY (GET endpoint to fetch uploaded files)
@app.get("/files", response_model=schemas.FileHistoryResponse)
def get_files_history(db: Session = Depends(get_db)):
    files = db.query(models.FileMetadata).all()
    return {"files": files}

# BASE ROUTE
@app.get("/")
def read_root():
    return {"message": "Server running and Database initialized! Ready for Uploads."}