from typing import Iterator, List
from minio import Minio
from minio.datatypes import Object


class MinioHandler:
    def __init__(self, client: Minio, bucket: str):
        self.client = client
        self.bucket = bucket

    def upload_file(self, name: str, data: bytes, length: int):
        """Принимает bytes, а не BinaryIO — проще и надёжнее."""
        from io import BytesIO

        self.client.put_object(self.bucket, name, BytesIO(data), length=length)

    def list(self) -> List[dict]:
        objects = self.client.list_objects(self.bucket)
        return [
            {"name": obj.object_name, "last_modified": obj.last_modified}
            for obj in objects
        ]

    def stats(self, name: str) -> Object:
        return self.client.stat_object(self.bucket, name)

    def download_file(self, name: str) -> Iterator[bytes]:
        """Возвращает генератор байтов. Автоматически закрывает соединение."""
        response = self.client.get_object(self.bucket, name)
        try:
            # Стримим блоками (например, 32 КБ)
            for chunk in response.stream(32 * 1024):
                yield chunk
        finally:
            # Обязательно закрываем!
            response.close()
            response.release_conn()
