from dataclasses import dataclass
from PIL import Image


@dataclass
class Album:
    """An album of photos."""
    id: str
    title: str
    cover: Image.Image


@dataclass
class Person:
    """A person on a photo."""
    name: str
    x: float
    y: float
    width: float
    height: float
    flickr_user_id: str


@dataclass
class Comment:
    """A comment on a photo."""
    owner: str
    created_timestamp: int
    body: str


@dataclass
class Note:
    """A user's note left on a photo."""
    owner: str
    body: str
    x: float
    y: float
    width: float
    height: float


@dataclass
class Location:
    """A location of a photo"""
    latitude: float
    longitude: float
    country: str
    region: str
    county: str
    city: str
    neighbourhood: str


@dataclass
class Metadata:
    """
    Metadata for a photo.
    Contains basic metadata (that can be extracted from the image file)
    and other metadata extracted from APIs.
    """
    basic: dict[str, str | int | float]
    title: str
    description: str | None = None
    people: list[Person] | None = None
    comments: list[Comment] | None = None
    notes: list[Note] | None = None
    location: Location | None = None


@dataclass
class RemotePhoto:
    """Represents a photo on a remote server."""
    id: str
    name: str
    url: str
    thumb: Image.Image


@dataclass
class LocalPhoto:
    """A photo on the local filesystem."""
    file_path: str
    metadata: Metadata
    remote: RemotePhoto | None = None

    @property
    def image(self):
        return Image.open(self.file_path)
