from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    app_name: str = "Resume Parser"
    model: str = "phi4-mini:latest "
    database_path: str = "data/resume_project.db"



settings = Settings()