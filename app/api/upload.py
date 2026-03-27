from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import uuid

from app.services.r2 import upload_file
from app.api.deps import get_db, get_current_tenant, require_role
from app.constants.roles import INSTITUTE_ADMIN
from app.services.usage_service import log_usage  # 🔥 IMPORTANT

router = APIRouter(prefix="/upload", tags=["Upload"])


# =========================
# 📤 FILE UPLOAD
# =========================
@router.post("/")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    tenant=Depends(get_current_tenant),
    user=Depends(require_role([INSTITUTE_ADMIN]))
):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    url = upload_file(file.file, filename, file.content_type)

    return {
        "success": True,
        "url": url
    }