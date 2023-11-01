import io

from minio import Minio
from minio.error import S3Error

from core.config import settings, MinioConfig


class MinIOClient:
    def __init__(self, minio_config: MinioConfig):
        self.client = Minio(
            f'{minio_config.host}:{minio_config.port}',
            access_key=minio_config.user,
            secret_key=minio_config.password.get_secret_value(),
            secure=False,
        )
        self.bucket_name = 'pastebin'

    def create_bucket(self) -> bool:
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                return True
            return False
        except S3Error:
            raise

    def upload_text_file(self, text: str, file_name: str) -> str:
        try:
            text_data = text.encode('utf-8')
            data_stream = io.BytesIO(text_data)
            self.client.put_object(
                self.bucket_name,
                file_name,
                data_stream,
                length=len(text_data),
                content_type='text/plain'
            )
            return file_name
        except S3Error:
            raise

    def get_text_file(self, file_name: str) -> str:
        try:
            response = self.client.get_object(self.bucket_name, file_name)
            return response.data.decode('utf-8')
        except S3Error:
            raise
        finally:
            response.close()
            response.release_conn()

    def delete_file(self, file_name: str) -> bool:
        try:
            self.client.remove_object(self.bucket_name, file_name)
            return True
        except S3Error:
            return False


def get_minio_client() -> MinIOClient:
    return MinIOClient(settings.minio)
