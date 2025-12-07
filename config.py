from pydantic_settings import BaseSeettings

class Settings(BaseSettings):
    app_name: str = "API de receitas"
    debug: bool = True
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
   