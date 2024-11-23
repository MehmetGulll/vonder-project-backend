from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Veritabanı Ayarları
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    DATABASE_NAME: str = "products"
    DATABASE_HOST: str = "postgres"  # Docker kullanıyorsanız, bu 'postgres' olmalı
    DATABASE_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy'nin kullanacağı veritabanı bağlantı URL'si
        """
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"

# Ayarları bir yerden erişilebilir hale getirmek için:
settings = Settings()
