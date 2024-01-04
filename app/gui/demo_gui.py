import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, QtWidgets
from PIL.ImageQt import ImageQt

from app.models import RemotePhoto, LocalPhoto
from app.gui.gui_demo import Ui_MainWindow
from app.gui.gui_elems import Img_Button, Dir_Button


class MainWin():
    """Main Window of the GUI."""

    def __init__(self, availableAPIs: list):
        # self.mainProgram = mainProgram
        self.mainWin = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWin)

        self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)

        # Populate API selection lists
        self.ui.SourceList.addItems(availableAPIs)
        self.ui.DestinationList.addItems(availableAPIs)

        # Set Buttons actions
        self.ui.ContinueBtnSet.clicked.connect(self.continueSet)

        self.ui.BackButAuth.clicked.connect(self.backAuth)

        self.ui.ContinueBtnSrc.clicked.connect(self.continueSrc)
        self.ui.BackBtnSrc.clicked.connect(self.backSrc)

        self.ui.SelectFileBtn.clicked.connect(self.selectFile)
        self.ui.ContinueSrcLocalBtn.clicked.connect(self.continueSrc)

        self.src_album = ""
        self.remote_image_id = ""
        self.img_buttons = []

        # for idx, dirs in enumerate(albums.keys()):
        #     img_button = Dir_Button(dirs,self.ui.scrollAreaWidgetContents)
        #     img_button.clicked.connect(lambda _, name = img_button.objectName(): self.selectsrc_album(name))
        #     self.ui.gridSrc.addWidget(img_button, idx // 5, idx % 5, 1, 1)
        #     self.img_buttons.append(img_button)

        # for row in range(self.ui.gridSrc.rowCount()):
        #     self.ui.gridSrc.setRowMinimumHeight(row, 150)
        # for column in range(self.ui.gridSrc.columnCount()):
        #     self.ui.gridSrc.setColumnMinimumWidth(column, 150)

        # for row in range(6):
        #     for column in range(5):
        #         self.img_buttons.append(Img_Button(str(row) + "_" + str(column),self.ui.scrollAreaWidgetContents))
        #         self.img_buttons[len(self.img_buttons)-1].clicked.connect(lambda _, name = self.img_buttons[len(self.img_buttons)-1].objectName(): self.selectSrc(name))
        #         # self.ui.gridSrc.addWidget(self.img_buttons[len(self.img_buttons)-1], row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #         self.ui.gridSrc.addWidget(self.img_buttons[len(self.img_buttons)-1], row, column, 1, 1)
        #         # print(self.ui.gridSrc.itemAtPosition(row, column))
        #         # self.ui.gridSrc.itemAtPosition(row, column).
        #         # self.ui.gridSrc.itemAtPosition(row, column).clicked.connect(self.selectSrc)

        self.ui.ContinueBtnCompl.clicked.connect(self.continueCompl)

    def setProgram(self, program):
        """Sets the main program to the GUI."""
        self.mainProgram = program

    def show(self):
        """Shows the GUI."""
        self.mainWin.show()

    def populateGridImg(self, items: list, grid):
        """Populates the grid with images."""
        for but in self.img_buttons:
            grid.removeWidget(but)
            but.deleteLater()
            del but
        self.img_buttons = []
        for idx, elem in enumerate(items):
            img_button = Img_Button(elem, self.ui.scrollAreaWidgetContents)
            img_button.clicked.connect(lambda _, name = img_button.text(), id = img_button.objectName(): self.selectSrc(id, name))
            grid.addWidget(img_button, idx // 5, idx % 5, 1, 1)
            self.img_buttons.append(img_button)

        for row in range(grid.rowCount()):
            grid.setRowMinimumHeight(row, 150)
        for column in range(grid.columnCount()):
            grid.setColumnMinimumWidth(column, 150)

    def populateGridDirs(self, items: list, grid):
        """Populates the grid with directories."""
        for but in self.img_buttons:
            grid.removeWidget(but)
            but.deleteLater()
            del but
        self.img_buttons = []
        for idx, elem in enumerate(items):
            img_button = Dir_Button(elem, self.ui.scrollAreaWidgetContents)
            if grid == self.ui.gridSrc:
                img_button.clicked.connect(lambda _, id = img_button.objectName(), name = img_button.text(): self.selectsrc_album(id, name))
            grid.addWidget(img_button, idx // 5, idx % 5, 1, 1)
            self.img_buttons.append(img_button)

        for row in range(grid.rowCount()):
            grid.setRowMinimumHeight(row, 150)
        for column in range(grid.columnCount()):
            grid.setColumnMinimumWidth(column, 150)

    def continueSet(self):
        """
        Continues to the next step after selecting the source and destination.
        """
        if self.ui.SourceList.currentText() == 'Local Disk':
            self.ui.stackedWidget.setCurrentWidget(self.ui.srcLocal)
        else:
            self.mainProgram.setSrcApi(self.ui.SourceList.currentText())
            self.ui.SrcLabel.setText(str(self.ui.SourceList.currentText()))
            self.ui.stackedWidget.setCurrentWidget(self.ui.AuthWindow)
            self.populateGridDirs(self.mainProgram.get_src_albums(), self.ui.gridSrc)
            self.ui.stackedWidget.setCurrentWidget(self.ui.SrcWindow)

    def backAuth(self):
        """Goes back to the source and destination selection."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings)

    def continueSrc(self):
        """Continues to the next step after selecting the source image."""
        self.local_image: LocalPhoto = self.mainProgram.select_src(
            self.remote_image_id
        )
        # self.ui.ComplLabel.setPixmap(QtGui.QPixmap.fromImage(ImageQt(self.local_image.image)))
        # print(self.srcInfo[1].metadata.keys())
        self.ui.MetadataLabel.setText("")
        for key in self.local_image.metadata.basic.keys():
            print(f'{key}: {self.local_image.metadata.basic[key]}')
            # if i == 5:
            #     break
            # i += 1
            if key in ['FileSize', 'ImageWidth', 'ImageHeight', 'Megapixels', 'FileType', 'MIMEType']:
                self.ui.MetadataLabel.setText(
                    self.ui.MetadataLabel.text() + f"{key}: {self.local_image.metadata.basic[key]}\n"
                )
        if self.ui.DatabaseTrigger.isChecked():
            self.mainProgram.save_meta_to_db(str(self.remote_image_id), self.local_image.metadata)
        
        if self.ui.DestinationList.currentText() == "Local Disk":
            self.mainProgram.save_to_local(self.remote_image_id, self.local_image.metadata.title)
        else:
            self.mainProgram.setDstApi(self.ui.DestinationList.currentText())
            self.mainProgram.dst_manager.upload_photo(self.local_image.file_path, self.local_image.metadata)

        self.ui.stackedWidget.setCurrentWidget(self.ui.Complete)
        self.src_album = ""
        self.local_image = ""

    def backSrc(self):
        """Goes back to the source selection."""
        self.ui.SrcSelectedLabel.setText("Select Image")
        self.ui.ContinueBtnSrc.setEnabled(False)
        if self.src_album == "":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)
        else:
            # self.populateGridDirs(albums.keys(), self.ui.gridSrc)
            self.populateGridDirs(self.mainProgram.get_src_albums(), self.ui.gridSrc)
            self.src_album = ""

    def selectsrc_album(self, id, name):
        """Selects the source album."""
        self.populateGridImg(self.mainProgram.get_src_images(id), self.ui.gridSrc)
        self.ui.SrcSelectedLabel.setText(f"Select Image ({name})")
        self.src_album = name

    def selectSrc(self, id, name):
        """Selects the source image."""
        self.ui.SrcSelectedLabel.setText(self.src_album+"/"+name)
        self.ui.ContinueBtnSrc.setEnabled(True)
        self.remote_image_id = id

    def selectFile(self):
        """Selects the source image from local disk."""
        self.ui.SelectedFileLabel.setText(
            QtWidgets.QFileDialog.getOpenFileName()[0]
        )

    def continueCompl(self):
        self.ui.SrcSelectedLabel.setText("Select Image")
        self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)
        self.ui.ContinueBtnSrc.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    api = ['Google Photos', 'Flickr']

    mainWin = MainWin(api)
    mainWin.show()
    sys.exit(app.exec_())
