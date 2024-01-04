from pydantic import BaseSettings, Field
from dataclasses import dataclass

from app.api import ApiManager
from app.api.google import GoogleApiManager
from app.api.flickr import FlickrApiManager


class RedisSettings(BaseSettings):
    host: str
    port: int
    password: str


class GoogleApiSettings(BaseSettings):
    client_id: str = Field(env='client_id')
    project_id: str = Field(env='project_id')
    client_secret: str = Field(env='client_secret')


class FlickrApiSettings(BaseSettings):
    api_key: str = Field(env='api_key')
    api_secret: str = Field(env='api_secret')


@dataclass
class RegisteredApi:
    name: str
    manager_class: type[ApiManager]
    settings: BaseSettings


@dataclass
class Settings:
    redis: RedisSettings
    apis: list[RegisteredApi]


settings = Settings(
    RedisSettings(_env_file='.env', _env_file_encoding='utf-8'),
    [
        RegisteredApi(
            name='Google Photos',
            manager_class=GoogleApiManager,
            settings=GoogleApiSettings(
                _env_file='.env', _env_file_encoding='utf-8'
            )
        ),
        RegisteredApi(
            name='Flickr',
            manager_class=FlickrApiManager,
            settings=FlickrApiSettings(
                _env_file='.env', _env_file_encoding='utf-8'
            )
        ),
    ]
)
