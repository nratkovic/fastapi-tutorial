from pydantic import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    project_name: str
    project_version: str

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_port: str
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"


settings = Settings()
