from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host : str
    db_password : str
    db_name : str
    db_user_name: str
    db_port : str
    secret_key : str
    algorithm : str
    access_token_expires_in_minutes : int
    
    class Config: 
        env_file : str = ".env"

settings = Settings()