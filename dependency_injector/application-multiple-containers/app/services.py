import logging
import sqlite3

from mypy_boto3_s3 import S3Client


class BaseService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )


class UserService(BaseService):
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        super().__init__()

    def get_user(self, email: str) -> dict[str, str]:
        self.logger.debug("user %s has been found in database", email)
        return {"email": email, "password_hash": "..."}


class AuthService(BaseService):
    def __init__(self, db: sqlite3.Connection, token_ttl: int) -> None:
        self.db = db
        self.token_ttl = token_ttl
        super().__init__()

    def authenticate(self, user: dict[str, str], password: str) -> None:
        assert password is not None
        self.logger.debug("user %s has been authenticated", user["email"])


class PhotoService(BaseService):
    def __init__(self, db: sqlite3.Connection, s3: S3Client) -> None:
        self.db = db
        self.s3 = s3
        super().__init__()

    def upload_photo(self, user: dict[str, str], photo: bytes) -> None:
        self.logger.debug("photo for user %s has been uploaded", user["email"])
