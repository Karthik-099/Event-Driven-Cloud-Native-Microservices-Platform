from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/orders"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    
    class Config:
        env_file = ".env"

settings = Settings()
