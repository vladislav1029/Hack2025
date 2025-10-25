# api/v1/files.py
__all__ = ["router"]



from fastapi import APIRouter, File, UploadFile
from structlog import get_logger

from src.core.minio.utils import make_s3_safe_filename
from src.dependency import DepPublicMinioHand

log = get_logger()


router = APIRouter(tags=["file-public"])



@router.post("/upload")
async def upload(
    minio_handler: DepPublicMinioHand,
    file: UploadFile = File(),
):
    contents = await file.read()
    filename = make_s3_safe_filename(file.filename)
    log.info(f"Созданно имя {filename} для объекта с именем {file.filename}" )
    minio_handler.upload_file(filename, contents, len(contents))
    return {"status": "uploaded", "name": filename}


@router.get("/list")
async def list_files(
    minio_handler: DepPublicMinioHand,
):
    return minio_handler.list()
