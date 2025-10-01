from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///./spy_cats.db'


config = Config()
