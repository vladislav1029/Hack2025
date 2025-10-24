# api/v1/files.py
__all__ = ["router"]


import datetime
import mimetypes
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import jwt
from structlog import get_logger

from src.config import settings
from src.core.exceptions import ResourceNotFoundError
from src.core.minio.utils import make_s3_safe_filename
from src.dependensy import DepPrivateMinioHand

log = get_logger()


router = APIRouter(tags=["file-jwt"])




@router.post("/upload")
async def upload(
    minio_handler: DepPrivateMinioHand,
    file: UploadFile = File(),
):
    contents = await file.read()
    filename = make_s3_safe_filename(file.filename)
    log.debug(f"Созданно имя  {filename} для объекта с именем {file.filename}")
    minio_handler.upload_file(filename, contents, len(contents))
    return {"status": "uploaded", "name": filename}


@router.get("/list")
async def list_files(
    minio_handler: DepPrivateMinioHand,
):
    return minio_handler.list()


@router.get("/link/{file}")
async def link(minio_handler: DepPrivateMinioHand, file: str):
    try:
        obj = minio_handler.stats(file)
    except Exception as e:
        raise ResourceNotFoundError()

    expire_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=10
    )
    payload = {
        "filename": obj.object_name,
        "valid_til": expire_at.isoformat(),  # ← Это стандарт ISO 8601
    }
    encoded_jwt = jwt.encode(payload, settings.minio.jwt_secret, algorithm="HS256")
    return {"link": f"/download/{encoded_jwt}"}


@router.get(
    "/download/{temp_link}", description="Выдаёт файл не тестить дока не справиться."
)
async def download(minio_handler: DepPrivateMinioHand, temp_link: str):

    decoded_jwt = jwt.decode(temp_link, settings.minio.jwt_secret, algorithms=["HS256"])
    valid_til = datetime.datetime.fromisoformat(decoded_jwt["valid_til"])

    if valid_til <= datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=400, detail="Link expired or invalid")

    filename = decoded_jwt["filename"]
    media_type, _ = mimetypes.guess_type(filename)
    media_type = media_type or "application/octet-stream"

    return StreamingResponse(
        minio_handler.download_file(filename),
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
    )
