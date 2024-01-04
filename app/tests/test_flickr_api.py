import unittest
from unittest.mock import MagicMock, patch, mock_open

from app.api.flickr import FlickrApiManager
from app.models import (
    RemotePhoto,
    Album,
    Note,
    Comment,
    Location,
    Person,
    Metadata
)


class MockFlickrApiManager(FlickrApiManager):
    def __init__(self):
        # Initialize without authenticating
        self.flickr = MagicMock()


class FlickrApiManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = MockFlickrApiManager()
        self.flickr = self.manager.flickr

    def test_get_photosets(self):
        photosets = {'photosets': {'photoset': [
            {'id': 'photoset1', 'title': {'_content': 'Photoset 1'}},
            {'id': 'photoset2', 'title': {'_content': 'Photoset 2'}}
        ]}}
        self.flickr.photosets.getList.return_value = photosets

        result = self.manager.get_photosets()

        self.assertEqual(result, [
            {'id': 'photoset1', 'title': {'_content': 'Photoset 1'}},
            {'id': 'photoset2', 'title': {'_content': 'Photoset 2'}}
        ])
        self.flickr.photosets.getList.assert_called_once()

    def test_get_photoset_photos(self):
        photos = {'photoset': {'photo': [
            {'id': 'photo1', 'title': 'Photo 1'},
            {'id': 'photo2', 'title': 'Photo 2'}
        ]}}
        self.flickr.photosets.getPhotos.return_value = photos

        result = self.manager.get_photoset_photos('photoset1')

        self.assertEqual(result, photos)
        self.flickr.photosets.getPhotos.assert_called_once_with(
            photoset_id='photoset1'
        )

    def test_get_photo_url(self):
        original = 'http://example.com/photo1.jpg'
        thumb = 'http://example.com/thumb.jpg'
        self.flickr.photos.getSizes.return_value = {
            'sizes': {
                'size': [
                    {'label': 'Original', 'source': original},
                    {'label': 'Thumbnail', 'source': thumb}
                ]
            }
        }

        result = self.manager.get_photo_url('photo1')

        self.assertEqual(result, original)
        self.flickr.photos.getSizes.assert_called_once_with(photo_id='photo1')

    def test_get_photo_title(self):
        photo = {'photo': {'title': {'_content': 'Photo 1'}}}
        self.flickr.photos.getInfo.return_value = photo

        result = self.manager.get_photo_title('photo1')

        self.assertEqual(result, 'Photo 1')
        self.flickr.photos.getInfo.assert_called_once_with(photo_id='photo1')

    def test_add_photo_title(self):
        self.manager.add_photo_title('photo1', 'Photo 1')

        self.flickr.photos.setMeta.assert_called_once_with(
            photo_id='photo1',
            title='Photo 1'
        )

    def test_get_photo_description(self):
        photo = {'photo': {'description': {'_content': 'Description'}}}
        self.flickr.photos.getInfo.return_value = photo

        result = self.manager.get_photo_description('photo1')

        self.assertEqual(result, 'Description')
        self.flickr.photos.getInfo.assert_called_once_with(photo_id='photo1')

    def test_add_photo_description(self):
        self.manager.add_photo_description('photo1', 'Description')

        self.flickr.photos.setMeta.assert_called_once_with(
            photo_id='photo1',
            description='Description'
        )

    def test_get_photo_notes(self):
        notes = {'photo': {'notes': {'note': [
            {
                'id': 'note1',
                'authorrealname': 'Author 1',
                '_content': 'Note 1',
                'x': 1, 'y': 2, 'w': 3, 'h': 4,
            },
            {
                'id': 'note2',
                'authorrealname': 'Author 2',
                '_content': 'Note 2',
                'x': 5, 'y': 6, 'w': 7, 'h': 8,
            }
        ]}}}
        self.flickr.photos.getInfo.return_value = notes

        result = self.manager.get_photo_notes('photo1')

        self.assertEqual(result, [
            Note(
                owner='Author 1',
                body='Note 1',
                x=1, y=2, width=3, height=4
            ),
            Note(
                owner='Author 2',
                body='Note 2',
                x=5, y=6, width=7, height=8
            )
        ])

    def test_add_photo_note(self):
        note = Note(
            owner='Author 1',
            body='Note 1',
            x=1, y=2, width=3, height=4
        )
        self.manager.add_photo_note('photo1', note)

        self.flickr.photos.notes.add.assert_called_once_with(
            photo_id='photo1',
            note_x=1, note_y=2, note_w=3, note_h=4,
            note_text='Note 1'
        )

    def test_get_photo_location(self):
        location = {'photo': {'location': {
            'latitude': 1.0,
            'longitude': 2.0,
            'locality': {'_content': 'Locality'},
            'county': {'_content': 'County'},
            'region': {'_content': 'Region'},
            'country': {'_content': 'Country'},
            'neighbourhood': {'_content': 'Neighbourhood'},
        }}}
        self.flickr.photos.geo.getLocation.return_value = location

        result = self.manager.get_photo_location('photo1')

        self.assertEqual(result, Location(
            latitude=1.0,
            longitude=2.0,
            country='Country',
            region='Region',
            county='County',
            city='Locality',
            neighbourhood='Neighbourhood'
        ))

    def test_add_photo_location(self):
        location = Location(
            latitude=1.0,
            longitude=2.0,
            country='Country',
            region='Region',
            county='County',
            city='Locality',
            neighbourhood='Neighbourhood'
        )
        self.manager.add_photo_location('photo1', location)

        self.flickr.photos.geo.setLocation.assert_called_once_with(
            photo_id='photo1',
            lat=1.0,
            lon=2.0,
        )

    def test_get_photo_exif(self):
        exif = {'photo': {'exif': [{'tag1': 'value1', 'tag2': 'value2'}]}}
        self.flickr.photos.getExif.return_value = exif

        result = self.manager.get_photo_exif('photo1')

        self.assertEqual(result, [{'tag1': 'value1', 'tag2': 'value2'}])
        self.flickr.photos.getExif.assert_called_once_with(photo_id='photo1')

    def test_get_photo_people(self):
        people = {'people': {'person': [
            {
                'nsid': 'person1',
                'realname': 'Person 1',
                'x': 1, 'y': 2, 'w': 3, 'h': 4
            },
            {
                'nsid': 'person2',
                'realname': 'Person 2',
                'x': 5, 'y': 6, 'w': 7, 'h': 8
            },
        ]}}
        self.flickr.photos.people.getList.return_value = people

        result = self.manager.get_photo_people('photo1')

        self.assertEqual(result, [
            Person(
                flickr_user_id='person1',
                name='Person 1',
                x=1,
                y=2,
                width=3,
                height=4
            ),
            Person(
                flickr_user_id='person2',
                name='Person 2',
                x=5,
                y=6,
                width=7,
                height=8
            ),
        ])

    def test_add_photo_person(self):
        person = Person(
            flickr_user_id='person1',
            name='Person 1',
            x=1,
            y=2,
            width=3,
            height=4
        )
        self.manager.add_photo_person('photo1', person)

        self.flickr.photos.people.add.assert_called_once_with(
            photo_id='photo1',
            user_id='person1',
            person_x=1,
            person_y=2,
            person_w=3,
            person_h=4
        )

    def test_get_photo_comments(self):
        comments = {'comments': {'comment': [
            {
                'realname': 'Author 1',
                '_content': 'Comment 1',
                'datecreate': '1234'},
            {
                'realname': 'Author 2',
                '_content': 'Comment 2',
                'datecreate': '4321'
            }
        ]}}
        self.flickr.photos.comments.getList.return_value = comments

        result = self.manager.get_photo_comments('photo1')

        self.assertEqual(result, [
            Comment(
                owner='Author 1',
                created_timestamp=1234,
                body='Comment 1'
            ),
            Comment(
                owner='Author 2',
                created_timestamp=4321,
                body='Comment 2'
            )
        ])

    @patch('app.api.flickr.FlickrApiManager.get_albums')
    def test_get_album_id_exists(self, mock_get_albums):
        albums = [
            Album(id='album1', title='Album 1', cover=None),
            Album(id='album2', title='Album 2', cover=None),
            Album(id='album3', title='Album 3', cover=None)
        ]
        mock_get_albums.return_value = albums

        result = self.manager.get_album_id('Album 1')

        self.assertEqual(result, 'album1')

    @patch('app.api.flickr.FlickrApiManager.get_albums')
    def test_get_album_id_no_album(self, mock_get_albums):
        albums = [
            Album(id='album1', title='Album 1', cover=None),
            Album(id='album2', title='Album 2', cover=None),
            Album(id='album3', title='Album 3', cover=None)
        ]
        mock_get_albums.return_value = albums

        result = self.manager.get_album_id('Album 4')

        self.assertEqual(result, None)

    def test_create_album(self):
        self.manager.create_album('Album 1', 'photo1')

        self.flickr.photosets.create.assert_called_once_with(
            title='Album 1',
            primary_photo_id='photo1'
        )

    @patch('app.api.flickr.urllib.request')
    @patch('app.api.flickr.Image.open')
    def test_get_photo_thumb(self, mock_image_open, mock_urllib_request):
        sizes = {
            'sizes': {
                'size': [
                    {'source': 'http://example.com/thumb_s.jpg'},
                    {'source': 'http://example.com/thumb_m.jpg'},
                    {'source': 'http://example.com/original.jpg'}
                ]
            }
        }
        self.flickr.photos.getSizes.return_value = sizes

        mock_response = MagicMock()
        mock_response.read.return_value = b'Test Image Data'
        mock_response.__enter__.return_value = mock_response
        mock_urllib_request.urlopen.return_value = mock_response

        mock_image = MagicMock()
        mock_image_open.return_value = mock_image

        result = self.manager.get_photo_thumb('photo1')

        self.assertEqual(result, mock_image)
        mock_urllib_request.urlopen.assert_called_once_with(
            'http://example.com/thumb_m.jpg'
        )
        mock_response.read.assert_called_once()

    @patch('app.api.flickr.FlickrApiManager.get_photo_thumb')
    def test_get_albums(self, mock_get_photo_thumb):
        photosets = [
            {
                'id': 'album1',
                'title': {'_content': 'Album 1'},
                'primary': 'photo1'
            },
            {
                'id': 'album2',
                'title': {'_content': 'Album 2'},
                'primary': 'photo2'
            }
        ]

        self.flickr.photosets.getList.return_value = {
            'photosets': {'photoset': photosets}
        }

        mock_image = MagicMock()
        mock_get_photo_thumb.return_value = mock_image

        result = self.manager.get_albums()

        expected_result = [
            Album(id='album1', title='Album 1', cover=mock_image),
            Album(id='album2', title='Album 2', cover=mock_image)
        ]

        self.assertEqual(result, expected_result)

    @patch('app.api.flickr.FlickrApiManager.get_photo_thumb')
    @patch('app.api.flickr.FlickrApiManager.get_photo_url')
    def test_get_album_photos(self, mock_get_photo_url, mock_get_photo_thumb):
        photos = {
            'photoset': {
                'photo': [
                    {
                        'id': 'photo1',
                        'title': 'photo1',
                    },
                    {
                        'id': 'photo2',
                        'title': 'photo2',
                    }
                ]
            }
        }

        self.flickr.photosets.getPhotos.return_value = photos

        mock_get_photo_url.side_effect = [
            "http://example.com/photo1.jpg",
            "http://example.com/photo2.jpg"
        ]

        mock_image = MagicMock()
        mock_get_photo_thumb.return_value = mock_image

        result = self.manager.get_album_photos('album1')

        expected_result = [
            RemotePhoto(
                id='photo1',
                name='photo1.jpg',
                url='http://example.com/photo1.jpg',
                thumb=mock_image
            ),
            RemotePhoto(
                id='photo2',
                name='photo2.jpg',
                url='http://example.com/photo2.jpg',
                thumb=mock_image
            )
        ]

        self.assertEqual(result, expected_result)
        mock_get_photo_thumb.assert_any_call('photo1')
        mock_get_photo_thumb.assert_any_call('photo2')

    @patch('app.api.flickr.get_metadata')
    @patch('app.api.flickr.FlickrApiManager.get_photo_title')
    @patch('app.api.flickr.FlickrApiManager.get_photo_description')
    @patch('app.api.flickr.FlickrApiManager.get_photo_people')
    @patch('app.api.flickr.FlickrApiManager.get_photo_comments')
    @patch('app.api.flickr.FlickrApiManager.get_photo_notes')
    @patch('app.api.flickr.FlickrApiManager.get_photo_location')
    def test_get_photo_metadata(
        self,
        mock_location,
        mock_notes,
        mock_comments,
        mock_people,
        mock_description,
        mock_title,
        mock_get_metadata
    ):
        metadata = {
            'FileName': 'temp.jpg',
            'Directory': '.',
            'FileModifyDate': '2023:01:01 00:00:00',
            'width': 800,
            'height': 600,
        }
        mock_get_metadata.return_value = metadata
        mock_title.return_value = 'Test Photo'
        mock_description.return_value = 'Test Description'

        test_people = [
            Person(name='Person 1', x=1, y=2, width=3, height=4, flickr_user_id='1234'),
            Person(name='Person 2', x=5, y=6, width=7, height=8, flickr_user_id='4321')
        ]
        mock_people.return_value = test_people
        test_comments = [
            Comment(owner='Author 1', created_timestamp=1234, body='Comment 1'),
            Comment(owner='Author 2', created_timestamp=4321, body='Comment 2')
        ]
        mock_comments.return_value = test_comments
        test_notes = [
            Note(owner='Author 1', x=1, y=2, width=3, height=4, body='Note 1'),
            Note(owner='Author 2', x=5, y=6, width=7, height=8, body='Note 2')
        ]
        mock_notes.return_value = test_notes
        test_location = Location(
            latitude=1.0,
            longitude=2.0,
            country='Country',
            region='Region',
            county='County',
            city='City',
            neighbourhood='Neighbourhood',
        )
        mock_location.return_value = test_location

        result = self.manager.get_photo_metadata('photo1', 'temp.jpg')

        expected = Metadata(
            basic={'width': 800, 'height': 600},
            title='Test Photo',
            description='Test Description',
            people=test_people,
            comments=test_comments,
            notes=test_notes,
            location=test_location
        )

        self.assertEqual(result, expected)

    @patch('app.api.flickr.open', new_callable=mock_open, read_data='data')
    @patch('app.api.flickr.FlickrApiManager.add_photo_note')
    @patch('app.api.flickr.FlickrApiManager.add_photo_person')
    @patch('app.api.flickr.FlickrApiManager.add_photo_location')
    @patch('app.api.flickr.FlickrApiManager.get_album_id')
    def test_upload_photo_album_exists(
        self,
        mock_get_album_id,
        mock_add_photo_location,
        mock_add_photo_person,
        mock_add_photo_note,
        mock_open
    ):
        self.flickr.upload().find().text = "photo1"

        meta = Metadata(
            basic={'width': 800, 'height': 600},
            title='Test Photo',
            description='Test Description',
            people=[
                Person(name='Person 1', x=1, y=2, width=3, height=4, flickr_user_id='1234'),
                Person(name='Person 2', x=5, y=6, width=7, height=8, flickr_user_id='4321')
            ],
            comments=[],
            notes=[
                Note(owner='Author 1', x=1, y=2, width=3, height=4, body='Note 1'),
                Note(owner='Author 2', x=5, y=6, width=7, height=8, body='Note 2')
            ],
            location=Location(
                latitude=1.0,
                longitude=2.0,
                country='Country',
                region='Region',
                county='County',
                city='City',
                neighbourhood='Neighbourhood',
            )
        )
        mock_get_album_id.return_value = 'album1'
        self.manager.upload_photo('asd.jpg', meta)

        self.flickr.upload.assert_called_with(
            fileobj='data',
            filename='asd.jpg',
            title='Test Photo',
            description='Test Description',
            format='etree'
        )

        mock_add_photo_location.assert_called_with(
            photo_id='photo1',
            location=meta.location
        )
        mock_add_photo_person.assert_any_call(
            photo_id='photo1',
            person=meta.people[0]
        )
        mock_add_photo_person.assert_any_call(
            photo_id='photo1',
            person=meta.people[1]
        )
        mock_add_photo_note.assert_any_call(
            photo_id='photo1',
            note=meta.notes[0]
        )
        mock_add_photo_note.assert_any_call(
            photo_id='photo1',
            note=meta.notes[1]
        )
        self.flickr.photosets.addPhoto.assert_called_with(
            photoset_id='album1',
            photo_id='photo1',
            format='etree'
        )

    @patch('app.api.flickr.open', new_callable=mock_open, read_data='data')
    @patch('app.api.flickr.FlickrApiManager.add_photo_note')
    @patch('app.api.flickr.FlickrApiManager.add_photo_person')
    @patch('app.api.flickr.FlickrApiManager.add_photo_location')
    @patch('app.api.flickr.FlickrApiManager.get_album_id')
    @patch('app.api.flickr.FlickrApiManager.create_album')
    def test_upload_photo_no_album(
        self,
        mock_create_album,
        mock_get_album_id,
        mock_add_photo_location,
        mock_add_photo_person,
        mock_add_photo_note,
        mock_open
    ):
        self.flickr.upload().find().text = "photo1"

        meta = Metadata(
            basic={'width': 800, 'height': 600},
            title='Test Photo',
            description='Test Description',
            people=[
                Person(name='Person 1', x=1, y=2, width=3, height=4, flickr_user_id='1234'),
                Person(name='Person 2', x=5, y=6, width=7, height=8, flickr_user_id='4321')
            ],
            comments=[],
            notes=[
                Note(owner='Author 1', x=1, y=2, width=3, height=4, body='Note 1'),
                Note(owner='Author 2', x=5, y=6, width=7, height=8, body='Note 2')
            ],
            location=Location(
                latitude=1.0,
                longitude=2.0,
                country='Country',
                region='Region',
                county='County',
                city='City',
                neighbourhood='Neighbourhood',
            )
        )
        mock_get_album_id.return_value = None
        self.manager.upload_photo('asd.jpg', meta)

        self.flickr.upload.assert_called_with(
            fileobj='data',
            filename='asd.jpg',
            title='Test Photo',
            description='Test Description',
            format='etree'
        )

        mock_add_photo_location.assert_called_with(
            photo_id='photo1',
            location=meta.location
        )
        mock_add_photo_person.assert_any_call(
            photo_id='photo1',
            person=meta.people[0]
        )
        mock_add_photo_person.assert_any_call(
            photo_id='photo1',
            person=meta.people[1]
        )
        mock_add_photo_note.assert_any_call(
            photo_id='photo1',
            note=meta.notes[0]
        )
        mock_add_photo_note.assert_any_call(
            photo_id='photo1',
            note=meta.notes[1]
        )
        mock_create_album.assert_called_with(
            'Converted Photos',
            'photo1'
        )

    # @patch('app.api.flickr.FlickrApiManager.upload_photo')
    # def test_upload_photo_to_album(self, mock_upload_photo):
    #     meta = Metadata(
    #         basic={'width': 800, 'height': 600},
    #         title='Test Photo',
    #         description='Test Description',
    #         people=[Person(
    #             name='Person 1',
    #             x=1, y=2, width=3, height=4,
    #             flickr_user_id='1234'
    #         )],
    #         comments=[],
    #         notes=[Note(
    #             owner='Author 1',
    #             x=1, y=2, width=3, height=4,
    #             body='Note 1'
    #         )],
    #         location=None
    #     )
    #     mock_upload_photo.return_value = 'photo1'

    #     self.manager.upload_photo_to_album('temp.jpg', meta, 'album1')
    #     self.flickr.photosets.addPhoto.assert_called_with(
    #         photoset_id='album1',
    #         photo_id='photo1',
    #         format='etree'
    #     )


if __name__ == '__main__':
    unittest.main()
