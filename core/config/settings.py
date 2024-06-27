from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    algorithm: str = "HS256"

    sendgrid_key: str

    class Config:
        env_file = ".env"


settings = Settings()
