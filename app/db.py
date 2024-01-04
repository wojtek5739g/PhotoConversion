import redis
import json

from app.config import settings


class DBManager:
    def __init__(self, db: redis.Redis):
        self.db = db

    def write(self, name: str, data: dict) -> None:
        self.db.set(name, json.dumps(data))

    def read(self, name: str) -> dict:
        data_b = self.db.get(name)
        return json.loads(data_b.decode("utf-8"))


db = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password
)
