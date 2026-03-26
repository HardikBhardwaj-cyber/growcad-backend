from fastapi import APIRouter, UploadFile, File
from app.services.r2 import upload_file
import uuid

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    url = upload_file(file.file, filename, file.content_type)

    return {
        "success": True,
        "url": url
    }