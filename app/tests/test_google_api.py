import unittest
from unittest.mock import MagicMock, patch, mock_open
from parameterized import parameterized

from app.api.google import GoogleApiManager
from app.models import Album, Metadata, RemotePhoto


class MockGoogleApiManager(GoogleApiManager):
    def __init__(self):
        # Initialize without authenticating
        self.service = MagicMock()
        self.flow = MagicMock()
        self.credentials = MagicMock()


class GoogleApiManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = MockGoogleApiManager()
        self.service = self.manager.service

    @patch('app.api.google.pickle')
    @patch('app.api.google.os.path.exists', return_value=True)
    @patch('app.api.google.open', mock_open())
    def test_authenticate_with_existing_token_file(
        self,
        mock_path_exists,
        mock_pickle
    ):
        credentials = MagicMock()
        credentials.valid = True
        mock_pickle.load.return_value = credentials

        self.manager.authenticate()

        mock_path_exists.assert_called_once_with('token.pickle')
        self.assertEqual(self.manager.credentials, credentials)
        self.assertFalse(credentials.refresh.called)
        self.assertFalse(self.manager.flow.run_local_server.called)
        self.assertFalse(mock_pickle.dump.called)

    @patch('app.api.google.pickle')
    @patch('app.api.google.os.path.exists', return_value=False)
    @patch('app.api.google.open', mock_open())
    def test_authenticate_with_no_token_file(
        self,
        mock_path_exists,
        mock_pickle,
    ):
        mock_pickle.load.return_value = False

        self.manager.authenticate()

        mock_path_exists.assert_called_once_with('token.pickle')
        self.assertFalse(mock_pickle.load.called)
        self.assertTrue(self.manager.flow.run_local_server.called)
        self.assertTrue(mock_pickle.dump.called)

    @patch('app.api.google.pickle')
    @patch('app.api.google.os.path.exists', return_value=True)
    @patch('app.api.google.open', mock_open())
    def test_authenticate_with_invalid_credentials(
        self,
        mock_path_exists,
        mock_pickle
    ):
        credentials = MagicMock()
        credentials.valid = False
        credentials.expired = True
        credentials.refresh_token = True
        mock_pickle.load.return_value = credentials

        self.manager.authenticate()

        mock_path_exists.assert_called_once_with('token.pickle')
        self.assertTrue(mock_pickle.load.called)
        self.assertTrue(self.manager.credentials.refresh.called)
        self.assertTrue(mock_pickle.dump.called)

    @parameterized.expand([
        ({
            'id': 'album1',
            'title': 'Album 1',
            'coverPhotoBaseUrl': 'http://example.com/cover1.jpg'
        },),
        ({
            'id': 'album2',
            'title': 'Album 2',
            'coverPhotoBaseUrl': 'http://example.com/cover2.jpg'
        },),
        ({
            'id': 'album3',
            'title': 'Album 3',
            'coverPhotoBaseUrl': 'http://example.com/asd.jpg'
        },),
    ])
    @patch('app.api.google.get_photo_from_url')
    def test_get_albums(self, album, mock_get_photo_from_url):
        albums = [album]

        self.service.albums().list().execute.return_value = {'albums': albums}

        mock_image = MagicMock()
        mock_get_photo_from_url.return_value = mock_image

        result = self.manager.get_albums()

        expected_result = [
            Album(id=album["id"], title=album["title"], cover=mock_image),
        ]

        self.assertEqual(result, expected_result)
        mock_get_photo_from_url.assert_called_once_with(
            album["coverPhotoBaseUrl"]+'=w150-h150'
        )

    @parameterized.expand([
        ({
            'id': 'photo1',
            'filename': 'photo1.jpg',
            'baseUrl': 'http://example.com/photo1.jpg',
            'mediaMetadata': {'width': 800, 'height': 600}
        },),
        ({
            'id': 'testImg',
            'filename': 'testImg.jpg',
            'baseUrl': 'http://example.com/testImg.jpg',
            'mediaMetadata': {'width': 456, 'height': 879}
        },),
        ({
            'id': 'img3',
            'filename': 'img3.jpg',
            'baseUrl': 'http://example.com/img3.jpg',
            'mediaMetadata': {'width': 123, 'height': 456}
        },),
        ({
            'id': 'img4',
            'filename': 'img4.jpg',
            'baseUrl': 'http://example.com/img4.jpg',
            'mediaMetadata': {'width': 789, 'height': 123}
        },),
    ])
    @patch('app.api.google.get_photo_from_url')
    def test_get_album_photos(self, photo, mock_get_photo_from_url):
        photos = [photo]

        self.service.mediaItems().search().execute.return_value = {
            'mediaItems': photos
        }

        mock_image = MagicMock()
        mock_get_photo_from_url.return_value = mock_image

        result = self.manager.get_album_photos('album1')

        meta = photo["mediaMetadata"]
        expected_url = f'{photo["baseUrl"]}=w{meta["width"]}-h{meta["height"]}'
        expected_result = [
            RemotePhoto(
                id=photo["id"],
                name=photo["filename"],
                url=expected_url,
                thumb=mock_image
            )
        ]

        self.assertEqual(result, expected_result)
        mock_get_photo_from_url.assert_called_once_with(
            f'{photo["baseUrl"]}=w150-h150'
        )

    @patch('app.api.google.get_metadata')
    @patch('app.api.google.write_metadata')
    def test_get_photo_metadata(
        self,
        mock_write_metadata,
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

        photo = {
            'filename': 'photo1.jpg',
            'description': 'Photo 1',
            'mediaMetadata': {
                'creationTime': '2023-01-01T00:00:00Z',
                'photo': {
                    'cameraMake': 'Canon',
                    'cameraModel': 'Canon EOS 5D Mark II',
                    'focalLength': 50,
                    'apertureFNumber': 1.8,
                    'isoEquivalent': 100,
                    "exposureTime": "0.0015625"
                }
            }
        }

        self.service.mediaItems().get().execute.return_value = photo
        result = self.manager.get_photo_metadata('photo1', 'temp.jpg')

        basic = {
            'FileName': 'photo1.jpg',
            'Directory': '.',
            'FileModifyDate': '2023:01:01 00:00:00',
            'DateTimeOriginal': '2023-01-01T00:00:00Z',
            'width': 800,
            'height': 600,
            'Make': 'Canon',
            'Model': 'Canon EOS 5D Mark II',
            'FocalLength': 50,
            'FNumber': 1.8,
            'ISO': 100,
            'ExposureTime': '0.0015625'
        }
        expected = Metadata(basic, title='photo1.jpg', description='Photo 1')
        self.assertEqual(result, expected)
        mock_get_metadata.assert_called_once_with('temp.jpg')

    @patch('app.api.google.GoogleApiManager.create_album_if_not_exists')
    @patch('app.api.google.mimetypes.guess_type')
    @patch('app.api.google.requests.post')
    @patch('app.api.google.open', new_callable=mock_open, read_data='data')
    def test_upload_photo(
        self,
        mock_open,
        mock_post,
        mock_guess_type,
        mock_create_album_if_not_exists
    ):
        mock_create_album_if_not_exists.return_value = 'album1'
        mock_guess_type.return_value = ('image/jpeg', None)
        mock_post.return_value = MagicMock(
            status_code=200,
            text="token"
        )

        meta = Metadata(
            basic=None,
            title='photo1.jpg',
            description='Photo 1',
        )

        self.manager.upload_photo('tmp.jpg', meta)

        self.service.mediaItems().batchCreate.assert_called_once_with(
            body={
                'albumId': 'album1',
                'newMediaItems': [{
                    "description": "Photo 1",
                    "simpleMediaItem": {
                        "fileName": "photo1.jpg",
                        "uploadToken": "token"
                    }
                }]
            }
        )

    def test_create_album_if_not_exists(self):
        self.service.albums().list().execute.return_value = {
            'albums': [
                {'id': 'album1', 'title': 'Album 1'},
                {'id': 'album2', 'title': 'Album 2'},
            ]
        }

        result = self.manager.create_album_if_not_exists('Album 2')

        self.assertEqual(result, 'album2')

    def test_create_album_if_not_exists_no_album(self):
        self.service.albums().list().execute.return_value = {
            'albums': [
                {'id': 'album1', 'title': 'Album 1'},
                {'id': 'album2', 'title': 'Album 2'},
            ]
        }

        self.manager.create_album_if_not_exists('album3')

        self.service.albums().create.assert_called_once_with(
            body={'album': {'title': 'album3'}}
        )

    def test_size_param(self):
        self.assertEqual(self.manager.size_param(100, 100), '=w100-h100')
        self.assertEqual(self.manager.size_param(73, 64), '=w73-h64')


if __name__ == '__main__':
    unittest.main()
