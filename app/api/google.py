import os
import pickle
import mimetypes

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from app.api import ApiManager
from app.models import Album, Metadata, RemotePhoto
from app.utils import get_photo_from_url, get_metadata, write_metadata

import requests


# API docs: https://developers.google.com/photos/library/reference/rest
class GoogleApiManager(ApiManager):
    """Google Photos API Manager."""

    ALBUM_NAME = "Converted Photos"

    THUMB_WIDTH = 150
    THUMB_HEIGHT = 150

    def __init__(self, settings):
        secrets_config = {
            "installed": {
                "client_id":
                    settings.client_id,
                "project_id":
                    settings.project_id,
                "auth_uri":
                    "https://accounts.google.com/o/oauth2/auth",
                "token_uri":
                    "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":
                    "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":
                    settings.client_secret,
                "redirect_uris":
                    ["http://localhost"]
            }
        }
        scopes = ['https://www.googleapis.com/auth/photoslibrary']

        self.flow = InstalledAppFlow.from_client_config(
            secrets_config,
            scopes=scopes
        )

        self.authenticate()

        self.service = build(
            'photoslibrary',
            'v1',
            credentials=self.credentials,
            static_discovery=False
        )

    def authenticate(self):
        """Authenticate with Google Photos API."""
        credentials = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if (
                credentials and
                credentials.expired and
                credentials.refresh_token
            ):
                credentials.refresh(Request())
            else:

                credentials = self.flow.run_local_server(
                    port=0,
                    prompt='consent',
                    authorization_prompt_message=''
                )

            with open("token.pickle", "wb") as f:
                pickle.dump(credentials, f)

        self.credentials = credentials

    def get_albums(self) -> list[Album]:
        """Returns a list of albums from Google Photos."""
        albums = self.service.albums().list().execute().get('albums', [])
        return [Album(
            id=album['id'],
            title=album['title'],
            cover=get_photo_from_url(
                album['coverPhotoBaseUrl']+self.size_param(
                    width_px=self.THUMB_WIDTH,
                    height_px=self.THUMB_HEIGHT
                )
            )
        ) for album in albums]

    def get_album_photos(self, album_id: str) -> list[RemotePhoto]:
        """Returns a list of photos from the given album."""
        photos = self.service.mediaItems().search(
            body={"albumId": album_id}
        ).execute().get('mediaItems', [])

        return [RemotePhoto(
            id=photo['id'],
            name=photo['filename'],
            url=photo['baseUrl']+self.size_param(
                width_px=photo["mediaMetadata"]["width"],
                height_px=photo["mediaMetadata"]["height"]
            ),
            thumb=get_photo_from_url(
                photo['baseUrl']+self.size_param(
                    width_px=self.THUMB_WIDTH,
                    height_px=self.THUMB_HEIGHT
                )
            )
        ) for photo in photos]

    def get_photo_metadata(self, photo_id: str, photo_path: str) -> Metadata:
        """Returns metadata for the given photo."""
        photo = self.service.mediaItems().get(mediaItemId=photo_id).execute()
        metadata = photo['mediaMetadata']
        description = photo.get('description')
        filename = photo.get('filename')

        basic_meta = get_metadata(photo_path)
        new_meta = {}
        new_meta["DateTimeOriginal"] = metadata["creationTime"]
        if "cameraMake" in metadata["photo"]:
            new_meta["Make"] = metadata["photo"]["cameraMake"]
        if "cameraModel" in metadata["photo"]:
            new_meta["Model"] = metadata["photo"]["cameraModel"]
        if "focalLength" in metadata["photo"]:
            new_meta["FocalLength"] = metadata["photo"]["focalLength"]
        if "apertureFNumber" in metadata["photo"]:
            new_meta["FNumber"] = metadata["photo"]["apertureFNumber"]
        if "isoEquivalent" in metadata["photo"]:
            new_meta["ISO"] = metadata["photo"]["isoEquivalent"]
        if "exposureTime" in metadata["photo"]:
            new_meta["ExposureTime"] = metadata["photo"]["exposureTime"]
        new_meta["FileName"] = filename
        write_metadata(photo_path, new_meta)
        basic_meta.update(new_meta)

        return Metadata(
            basic=basic_meta,
            title=filename,
            description=description
        )

    def upload_photo(self, photo_path: str, metadata: Metadata) -> None:
        album_id = self.create_album_if_not_exists(self.ALBUM_NAME)

        upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'

        mime = mimetypes.guess_type(photo_path)

        headers = {
            'Authorization': f'Bearer {self.credentials.token}',
            'Content-type': 'application/octet-stream',
            'X-Goog-Upload-Content-Type': mime[0],
            'X-Goog-Upload-Protocol': 'raw',
            'X-Goog-Upload-File-Name': metadata.title
        }

        photo = open(photo_path, 'rb').read()
        response = requests.post(upload_url, data=photo, headers=headers)

        if response.status_code == requests.codes.ok:
            upload_token = response.text
            payload = {
                "albumId": album_id,
                "newMediaItems": [
                    {
                        "description": metadata.description,
                        "simpleMediaItem": {
                            "fileName": metadata.title,
                            "uploadToken": upload_token
                            }
                    }
                ]
            }

            self.service.mediaItems().batchCreate(body=payload).execute()
        else:
            response.raise_for_status()

    def create_album_if_not_exists(self, album_name: str) -> str:
        """Creates an album if it doesn't exist, and returns its ID."""
        albums = self.service.albums().list().execute().get('albums', [])
        for album in albums:
            if album['title'] == album_name:
                return album['id']

        payload = {
            "album": {
                "title": album_name
            }
        }

        response = self.service.albums().create(body=payload).execute()
        return response['id']

    def size_param(self, width_px: int, height_px: int) -> str:
        """Returns a string to be appended to an image URL to resize it."""
        return f'=w{width_px}-h{height_px}'
