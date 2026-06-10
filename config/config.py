from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root_password"
    MYSQL_DATABASE: str = "main"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_TTL: int = 100
    TV_MAZE_API_BASE_URL: str = "https://api.tvmaze.com"
    SELLER_SERVICE_BASE_URL: str = "http://localhost:8081"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_TIME: int = 30
    