import sys
import os
import uuid

from PyQt5.QtWidgets import QApplication

from app.config import settings
from app.gui.interface import Interface
from app.models import Album, LocalPhoto, RemotePhoto, Metadata
from app.db import DBManager, db

from app.utils import download_photo, object_to_dict, get_metadata


class ProgramDemo:
    IMAGE_DIR = os.path.expanduser("~/Pictures/converter")

    def run(self):
        app = QApplication(sys.argv)
        self.api = [api.name for api in settings.apis] + ["Local Disk"]

        self.src_albums = []
        self.src_remote_images = []
        self.src_manager = None
        self.dst_manager = None
        self.db = DBManager(db)
        self.interface = Interface(self.api)
        self.interface.set_program(self)
        self.interface.show()
        sys.exit(app.exec_())

    def set_src_api(self, api: str) -> None:
        for registered_api in settings.apis:
            if registered_api.name == api:
                self.src_manager = registered_api.manager_class(
                    registered_api.settings
                )
                return

    def set_dst_api(self, api: str) -> None:
        for registered_api in settings.apis:
            if registered_api.name == api:
                self.dst_manager = registered_api.manager_class(
                    registered_api.settings
                )
                return

    def get_src_albums(self) -> list[Album]:
        self.src_albums = self.src_manager.get_albums()
        return self.src_albums

    def get_src_images(self, album_id: str) -> list[RemotePhoto]:
        self.src_remote_images = self.src_manager.get_album_photos(album_id)
        return self.src_remote_images

    def select_local_src_img(self) -> LocalPhoto:
        path = self.interface.ui.SelectedFileLabel.text()
        title = os.path.basename(path)
        meta = get_metadata(path)
        meta = Metadata(
            basic=meta,
            title=title
        )
        return LocalPhoto(path, meta)

    def select_remote_src_img(self, id: str) -> LocalPhoto:
        for image in self.src_remote_images:
            if image.id == id:
                if not os.path.exists(self.IMAGE_DIR):
                    os.makedirs(self.IMAGE_DIR)
                path = os.path.join(self.IMAGE_DIR, image.name)
                download_photo(image.url, path)
                meta = self.src_manager.get_photo_metadata(
                    image.id,
                    path
                )
                return LocalPhoto(path, meta)

    def upload_photo(self, path: str, meta: Metadata) -> None:
        self.dst_manager.upload_photo(path, meta)

    def clean_up(self) -> None:
        if self.src_manager and self.dst_manager:
            os.remove(self.interface.local_image.file_path)
        self.src_manager = None
        self.dst_manager = None

    def save_meta_to_db(self, meta: Metadata) -> None:
        data = object_to_dict(meta)
        photo_id = str(uuid.uuid4())
        self.db.write(photo_id, data)


if __name__ == "__main__":
    program = ProgramDemo()
    program.run()
