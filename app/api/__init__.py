from abc import ABC, abstractmethod

from app.models import Album, RemotePhoto, Metadata


class ApiManager(ABC):
    def __init__(self) -> None:
        self.authenticate()

    @abstractmethod
    def authenticate(self) -> None:
        # Authenticates user
        ...

    @abstractmethod
    def get_albums(self) -> list[Album]:
        # Gets all user's albums
        ...

    @abstractmethod
    def get_album_photos(self, album_id: str) -> list[RemotePhoto]:
        # Gets all photos in album
        ...

    @abstractmethod
    def get_photo_metadata(self, photo_id: str, photo_path: str) -> Metadata:
        # Gets all metadata for photo
        ...

    @abstractmethod
    def upload_photo(self, photo_path: str, metadata: Metadata) -> None:
        # Uploads a photo and sets all the metadata
        ...
