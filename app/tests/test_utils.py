import unittest
from unittest.mock import MagicMock, patch

from parameterized import parameterized

from app.utils import (
    get_metadata,
    write_metadata,
    get_photo_from_url,
    download_photo,
    object_to_dict
)


class TestUtils(unittest.TestCase):
    @parameterized.expand([
        (
            {
                'EXIF:DateTimeOriginal': '2021:08:01 12:00:00',
                'EXIF:ImageWidth': 800,
                'EXIF:ImageHeight': 600,
                'EXIF:Make': 'Canon',
                'EXIF:Model': 'Canon EOS 5D Mark IV',
            },
            {
                'DateTimeOriginal': '2021:08:01 12:00:00',
                'ImageWidth': 800,
                'ImageHeight': 600,
                'Make': 'Canon',
                'Model': 'Canon EOS 5D Mark IV',
            },),
    ])
    @patch('exiftool.ExifToolHelper.get_metadata')
    def test_get_metadata(self, metadata, expected, mock_get_metadata):
        mock_get_metadata.return_value = [metadata]

        result = get_metadata('test.jpg')

        assert result == expected

    @patch('exiftool.ExifToolHelper.execute')
    def test_write_metadata(self, mock_execute):
        metadata = {
            'DateTimeOriginal': '2021:08:01 12:00:00',
            'ImageWidth': 800,
            'ImageHeight': 600,
            'Make': 'Canon',
            'Model': 'Canon EOS 5D Mark IV',
        }
        write_metadata('test.jpg', metadata)
        mock_execute.assert_called_with(
            *[
                '-DateTimeOriginal=2021:08:01 12:00:00',
                '-ImageWidth=800',
                '-ImageHeight=600',
                '-Make=Canon',
                '-Model=Canon EOS 5D Mark IV'
            ],
            'test.jpg'
        )

    @patch('urllib.request.urlopen')
    @patch('PIL.Image.open')
    def test_get_photo_from_url(
        self,
        mock_image_open,
        mock_urlopen
    ):

        mock_response = MagicMock()
        mock_response.read.return_value = b'url'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        mock_image = MagicMock()
        mock_image_open.return_value = mock_image

        result = get_photo_from_url('http://example.com/photo.jpg')

        self.assertEqual(result, mock_image)
        mock_urlopen.assert_called_once_with(
            'http://example.com/photo.jpg'
        )
        mock_response.read.assert_called_once()

    @patch('urllib.request.urlretrieve')
    def test_download_photo(self, mock_urlretrieve):
        download_photo('http://example.com/photo.jpg', 'test.jpg')
        mock_urlretrieve.assert_called_with(
            'http://example.com/photo.jpg',
            'test.jpg'
        )

    def test_object_to_dict(self):
        class TestObject1:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        class TestObject2:
            def __init__(self, a, b):
                self.a = a
                self.b = TestObject1(a, b)

        test_obj = TestObject2(1, 2)
        result = object_to_dict(test_obj)
        expected = {'a': 1, 'b': {'a': 1, 'b': 2}}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
