import flickrapi
from flickrapi.exceptions import FlickrError

import webbrowser
import urllib.request
from PIL import Image
import io
from typing import List

from app.api import ApiManager

from app.models import (
    Album,
    RemotePhoto,
    Metadata,
    Person,
    Comment,
    Location,
    Note
)

from app.utils import get_photo_from_url, get_metadata


# API docs: https://www.flickr.com/services/api/
# flickrapi docs: https://stuvel.eu/flickrapi-doc/index.html
# Get api key and secret from http://www.flickr.com/services/api/keys/

class FlickrApiManager(ApiManager):
    """Flickr API Manager."""

    ALBUM_NAME = "Converted Photos"

    def __init__(self, settings):
        self.flickr = flickrapi.FlickrAPI(
            settings.api_key,
            settings.api_secret,
            format='parsed-json'
        )

        if not self.flickr.token_valid(perms='write'):
            self.authenticate()

    def authenticate(self):
        """Authenticate with Flickr API."""
        self.flickr.get_request_token(oauth_callback='oob')

        authorize_url = self.flickr.auth_url(perms='write')
        webbrowser.open_new_tab(authorize_url)

        verifier = str(input('Verifier code: '))

        self.flickr.get_access_token(verifier)

    def get_photosets(self):
        """Get all user's photosets."""
        return self.flickr.photosets.getList()["photosets"]["photoset"]

    def get_photoset_photos(self, photoset_id):
        """Get all photos from a photoset."""
        return self.flickr.photosets.getPhotos(photoset_id=photoset_id)

    def get_photo_url(self, photo_id: str) -> str:
        """Get the URL of a photo that later can be downloaded."""
        sizes = self.flickr.photos.getSizes(photo_id=photo_id)
        # Find the URL of the original size
        for size in sizes['sizes']['size']:
            if size['label'] == 'Original':
                return size['source']

    def get_photo_title(self, photo_id: str) -> str | None:
        """Get the title of a photo."""
        return self.flickr.photos.getInfo(
            photo_id=photo_id
        ).get('photo').get('title').get('_content')

    def add_photo_title(self, photo_id: str, title: str) -> None:
        """Add a title to a photo."""
        self.flickr.photos.setMeta(photo_id=photo_id, title=title)

    def get_photo_description(self, photo_id: str) -> str | None:
        return self.flickr.photos.getInfo(
            photo_id=photo_id
        ).get('photo').get('description').get('_content')

    def add_photo_description(self, photo_id: str, description: str) -> None:
        """Add a description to a photo."""
        self.flickr.photos.setMeta(photo_id=photo_id, description=description)

    def get_photo_notes(self, photo_id: str) -> list[Note] | None:
        """Get all notes for a photo."""
        notes_api_result = self.flickr.photos.getInfo(
            photo_id=photo_id
        ).get('photo').get('notes').get('note')
        notes = None
        if notes_api_result:
            notes = []
            for note in notes_api_result:
                owner = note.get('authorrealname')
                body = note.get('_content')
                x = float(note.get('x'))
                y = float(note.get('y'))
                w = float(note.get('w'))
                h = float(note.get('h'))
                note = Note(
                    owner=owner,
                    body=body,
                    x=x,
                    y=y,
                    width=w,
                    height=h
                )
                notes.append(note)
        return notes

    def add_photo_note(self, photo_id: str, note: Note) -> None:
        """Add a note to a photo."""
        self.flickr.photos.notes.add(
            photo_id=photo_id,
            note_x=note.x,
            note_y=note.y,
            note_w=note.width,
            note_h=note.height,
            note_text=note.body
        )

    def get_photo_location(self, photo_id: str) -> Location | None:
        """Get the location where a photo was taken."""
        try:
            location_api_result = self.flickr.photos.geo.getLocation(
                photo_id=photo_id
            ).get('photo').get('location')
        except FlickrError:
            return None

        latitude = float(location_api_result.get('latitude'))
        longitude = float(location_api_result.get('longitude'))
        locality = location_api_result.get('locality').get('_content')
        county = location_api_result.get('county').get('_content')
        region = location_api_result.get('region').get('_content')
        country = location_api_result.get('country').get('_content')
        neighbourhood = location_api_result.get(
            'neighbourhood'
        ).get('_content')
        location = Location(
            latitude=latitude,
            longitude=longitude,
            country=country,
            region=region,
            county=county,
            city=locality,
            neighbourhood=neighbourhood)
        return location

    def add_photo_location(self, photo_id: str, location: Location) -> None:
        """Add a location to a photo."""
        self.flickr.photos.geo.setLocation(
            photo_id=photo_id,
            lat=location.latitude,
            lon=location.longitude
        )

    def get_photo_exif(self, photo_id: str) -> dict[str, str | float | int]:
        """Get the exif data of a photo."""
        return self.flickr.photos.getExif(
            photo_id=photo_id
        ).get('photo').get('exif')

    def get_photo_people(self, photo_id: str) -> list[Person] | None:
        """Get all people in a photo."""
        people_api_result = self.flickr.photos.people.getList(
            photo_id=photo_id
        ).get('people').get('person')
        people = None
        if people_api_result:
            people = []
            for person_result in people_api_result:
                name = person_result.get('realname')
                x = person_result.get('x')
                y = person_result.get('y')
                w = person_result.get('w')
                h = person_result.get('h')
                flickr_user_id = person_result.get('nsid')
                person = Person(
                    name=name,
                    x=x, y=y, width=w, height=h,
                    flickr_user_id=flickr_user_id
                )
                people.append(person)
        return people

    def add_photo_person(self, photo_id: str, person: Person) -> None:
        """Add a person to a photo."""
        self.flickr.photos.people.add(
            photo_id=photo_id,
            user_id=person.flickr_user_id,
            person_x=person.x,
            person_y=person.y,
            person_w=person.width,
            person_h=person.height
        )

    def get_photo_comments(self, photo_id: str) -> list[Comment] | None:
        """Get all comments on a photo."""
        comments_api_result = self.flickr.photos.comments.getList(
            photo_id=photo_id
        ).get('comments').get('comment')
        comments = None
        if comments_api_result:
            comments = []
            for comment_result in comments_api_result:
                name = comment_result.get('realname')
                date_timestamp = int(comment_result.get('datecreate'))
                body = comment_result.get('_content')
                comment = Comment(
                    owner=name,
                    created_timestamp=date_timestamp,
                    body=body
                )
                comments.append(comment)
        return comments

    def get_photo_thumb(self, photo_id):
        """Get the thumbnail of a photo."""
        sizes = self.flickr.photos.getSizes(photo_id=photo_id)
        thumb_url = sizes['sizes']['size'][1]['source']
        return get_photo_from_url(thumb_url)

    def get_album_id(self, album_title: str) -> str | None:
        """Get the id of an album."""
        albums = self.get_albums()
        for album in albums:
            if album.title == album_title:
                return album.id
        return None

    def create_album(self, album_title: str, primary_id: str) -> str:
        """Create an album."""
        return self.flickr.photosets.create(
            title=album_title,
            primary_photo_id=primary_id
        ).get('photoset').get('id')

    def get_albums(self) -> List[Album]:
        """Get all user's albums."""
        photosets = self.get_photosets()
        albums = list()
        for p in photosets:
            title = p.get('title')
            cover = self.get_photo_thumb(p.get('primary'))
            album = Album(
                id=p.get('id'), title=title.get('_content'), cover=cover)
            albums.append(album)
        return albums

    def get_album_photos(self, album_id: str) -> List[RemotePhoto]:
        """Get all photos in album."""
        album_photos = list()
        photos = self.get_photoset_photos(album_id)
        for p in photos['photoset']['photo']:
            url = self.get_photo_url(p.get('id'))
            thumb = self.get_photo_thumb(p.get('id'))
            photo = RemotePhoto(
                id=p.get('id'),
                name=p.get('title')+".jpg",
                url=url,
                thumb=thumb
            )
            album_photos.append(photo)
        return album_photos

    def get_photo_metadata(self, photo_id: str, photo_path: str) -> Metadata:
        """Get all metadata for photo."""
        title = self.get_photo_title(photo_id=photo_id)
        description = self.get_photo_description(photo_id=photo_id)

        basic = get_metadata(path=photo_path)
        basic.pop("FileName")
        basic.pop("Directory")
        basic.pop("FileModifyDate")

        return Metadata(
            basic=basic,
            title=title,
            description=description,
            people=self.get_photo_people(photo_id=photo_id),
            comments=self.get_photo_comments(photo_id=photo_id),
            notes=self.get_photo_notes(photo_id=photo_id),
            location=self.get_photo_location(photo_id=photo_id)
        )

    def upload_photo(self, photo_path: str, metadata: Metadata) -> None:
        """Uploads a photo and sets all the metadata."""
        with open(photo_path, 'rb') as f:
            photo_data = f.read()

        upload_response = self.flickr.upload(
            fileobj=photo_data,
            filename=photo_path,
            title=metadata.title,
            description=metadata.description,
            format='etree'
        )
        photo_id = upload_response.find('photoid').text

        if metadata.location:
            self.add_photo_location(
                photo_id=photo_id,
                location=metadata.location
            )
        if metadata.notes:
            for note in metadata.notes:
                self.add_photo_note(photo_id=photo_id, note=note)
        if metadata.people:
            for person in metadata.people:
                self.add_photo_person(photo_id=photo_id, person=person)

        if album_id := self.get_album_id(self.ALBUM_NAME):
            self.flickr.photosets.addPhoto(
                photoset_id=album_id,
                photo_id=photo_id,
                format='etree'
            )
        else:
            self.create_album(self.ALBUM_NAME, photo_id)
