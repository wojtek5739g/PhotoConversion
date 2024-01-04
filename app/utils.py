import io
import exiftool
import urllib
from PIL import Image


def get_metadata(path: str) -> dict[str, str | int | float]:
    """Get metadata from a photo."""
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(path)[0]
    return {k.split(":")[1] if ':' in k else k: v for k, v in metadata.items()}


def write_metadata(photo_path, metadata):
    with exiftool.ExifToolHelper() as et:
        tags = [f'-{key}={value}' for key, value in metadata.items()]
        et.execute(*tags, photo_path)


def get_photo_from_url(url: str) -> Image.Image:
    """Get a photo from a URL without saving it to disk."""
    with urllib.request.urlopen(url) as url:
        data = url.read()
        image = Image.open(io.BytesIO(data))
    return image


def download_photo(url: str, path: str) -> None:
    """Download a photo from a URL to a path."""
    urllib.request.urlretrieve(url, path)


def object_to_dict(obj: object) -> dict[str, str | int | float | list | dict]:
    """Recursively convert an object to a dictionary."""
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [object_to_dict(elem) for elem in obj if elem is not None]
    elif hasattr(obj, '__dict__'):
        return object_to_dict(obj.__dict__)
    else:
        return obj
