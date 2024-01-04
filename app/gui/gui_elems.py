from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.ImageQt import ImageQt
from app.models import RemotePhoto, Album


class Button(QtWidgets.QToolButton):
    def __init__(self, image, id, name, parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        self.setFixedSize(150, 150)

        self.pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.pixmap = self.pixmap.scaled(
            130,
            130,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )
        self.icon = QtGui.QIcon(self.pixmap)
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(130, 130))

        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setText(name)
        self.setObjectName(id)


class Img_Button(Button):
    def __init__(self, image: RemotePhoto, parent: QtWidgets.QWidget = None):
        super().__init__(image.thumb, image.id, image.name, parent)


class Dir_Button(Button):
    def __init__(self, album: Album, parent: QtWidgets.QWidget = None):
        super().__init__(album.cover, album.id, album.title, parent)
