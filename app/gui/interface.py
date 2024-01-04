import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, QtWidgets
from PIL.ImageQt import ImageQt

from app.models import RemotePhoto, LocalPhoto, Album
from app.gui.gui import Ui_MainWindow
from app.gui.gui_elems import Img_Button, Dir_Button


class Interface:
    """Main GUI class."""

    def __init__(self, api_names: list[str]):
        # self.mainProgram = mainProgram
        self.mainWin = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWin)

        self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)

        self.APIs = api_names

        # Populate API selection lists
        self.ui.SourceList.addItems(api_names)
        self.on_src_api_changed()

        self.ui.SourceList.currentTextChanged.connect(self.on_src_api_changed)

        # Set Buttons actions
        self.ui.ContinueBtnSet.clicked.connect(self.on_continue_api_selected)
        self.ui.ContinueBtnSrc.clicked.connect(self.on_continue_img_selected)
        self.ui.BackBtnSrc.clicked.connect(
            self.on_back_clicked
        )
        self.ui.SelectFileBtn.clicked.connect(self.select_file)
        self.ui.ContinueBtnCompl.clicked.connect(self.on_continue_img_uploaded)
        self.ui.ContinueSrcLocalBtn.clicked.connect(
            self.on_continue_img_selected
        )
        self.ui.BackBtnSrcLocal.clicked.connect(self.on_back_clicked)

        self.src_album = None
        self.remote_image_id = None
        self.local_image = None
        self.img_buttons = []

    def set_program(self, program):
        """Sets the main program to the GUI."""
        self.mainProgram = program

    def show(self):
        """Shows the GUI."""
        self.mainWin.show()

    def show_images(self, images: list[RemotePhoto], grid):
        """Populates the grid with images."""
        for but in self.img_buttons:
            grid.removeWidget(but)
            but.deleteLater()
            del but
        self.img_buttons = []
        for idx, elem in enumerate(images):
            img_button = Img_Button(elem, self.ui.scrollAreaWidgetContents)
            img_button.clicked.connect(
                lambda _,
                name=img_button.text(),
                id=img_button.objectName(): self.select_src_img(id, name)
            )
            grid.addWidget(img_button, idx // 5, idx % 5, 1, 1)
            self.img_buttons.append(img_button)

        for row in range(grid.rowCount()):
            grid.setRowMinimumHeight(row, 150)
        for column in range(grid.columnCount()):
            grid.setColumnMinimumWidth(column, 150)

    def show_albums(self, albums: list[Album], grid):
        """Populates the grid with directories."""
        for but in self.img_buttons:
            grid.removeWidget(but)
            but.deleteLater()
            del but
        self.img_buttons = []
        for idx, elem in enumerate(albums):
            img_button = Dir_Button(elem, self.ui.scrollAreaWidgetContents)
            if grid == self.ui.gridSrc:
                img_button.clicked.connect(
                    lambda _,
                    id=img_button.objectName(),
                    name=img_button.text(): self.select_src_album(id, name)
                )
            grid.addWidget(img_button, idx // 5, idx % 5, 1, 1)
            self.img_buttons.append(img_button)

        for row in range(grid.rowCount()):
            grid.setRowMinimumHeight(row, 150)
        for column in range(grid.columnCount()):
            grid.setColumnMinimumWidth(column, 150)

    def on_continue_api_selected(self):
        """
        Continues to the next step after selecting the source and destination.
        """
        if self.ui.SourceList.currentText() == 'Local Disk':
            self.ui.stackedWidget.setCurrentWidget(self.ui.srcLocal)
        else:
            self.ui.SrcSelectedLabel.setText("Select Album")
            self.mainProgram.set_src_api(self.ui.SourceList.currentText())
            self.ui.SrcLabel.setText(str(self.ui.SourceList.currentText()))
            self.ui.stackedWidget.setCurrentWidget(self.ui.AuthWindow)
            self.show_albums(
                self.mainProgram.get_src_albums(),
                self.ui.gridSrc
            )
            self.ui.stackedWidget.setCurrentWidget(self.ui.SrcWindow)
        self.mainProgram.set_dst_api(self.ui.DestinationList.currentText())

    def on_continue_img_selected(self):
        """Continues to the next step after selecting the source image."""
        if not self.remote_image_id:
            self.local_image = self.mainProgram.select_local_src_img()
        else:
            self.local_image = self.mainProgram.select_remote_src_img(
                self.remote_image_id
            )
        if self.ui.DatabaseTrigger.isChecked():
            self.mainProgram.save_meta_to_db(
                self.local_image.metadata
            )

        if not self.ui.DestinationList.currentText() == "Local Disk":
            try:
                self.mainProgram.upload_photo(
                    self.local_image.file_path,
                    self.local_image.metadata
                )
                self.ui.MetadataLabel.setText("Successfully uploaded")
            except Exception:
                self.ui.MetadataLabel.setText("Error uploading")
        else:
            self.ui.MetadataLabel.setText("Successfully downloaded")

        self.ui.stackedWidget.setCurrentWidget(self.ui.Complete)
        self.mainProgram.clean_up()
        self.clean_up()

    def on_back_clicked(self):
        """Go back to the previous step."""
        self.ui.ContinueBtnSrc.setEnabled(False)
        self.ui.ContinueSrcLocalBtn.setEnabled(False)
        self.ui.SelectedFileLabel.setText("")
        if not self.src_album or self.ui.stackedWidget.currentWidget() == self.ui.srcLocal:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)
        else:
            # self.populateGridDirs(albums.keys(), self.ui.gridSrc)
            self.ui.SrcSelectedLabel.setText("Select Album")
            self.show_albums(
                self.mainProgram.get_src_albums(),
                self.ui.gridSrc
            )
            self.src_album = None

    def select_src_album(self, id: str, name: str):
        """Selects the source album."""
        self.show_images(
            self.mainProgram.get_src_images(id),
            self.ui.gridSrc
        )
        self.ui.SrcSelectedLabel.setText(f"Select Image ({name})")
        self.src_album = name

    def select_src_img(self, id: str, name: str):
        """Selects the source image."""
        self.ui.SrcSelectedLabel.setText(self.src_album+"/"+name)
        self.ui.ContinueBtnSrc.setEnabled(True)
        self.remote_image_id = id

    def select_file(self):
        """Selects the source image from local disk."""
        self.ui.SelectedFileLabel.setText(
            QtWidgets.QFileDialog.getOpenFileName(caption="Select Image",
                                                  directory=os.path.expanduser("~/Pictures"),
                                                  filter="Image files (*.jpg *.png)")[0]
        )
        if self.ui.SelectedFileLabel.text():
            self.ui.ContinueSrcLocalBtn.setEnabled(True)

    def on_continue_img_uploaded(self):
        """Continues to the next step after uploading the image."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)
        self.ui.ContinueBtnSrc.setEnabled(False)
        self.ui.ContinueSrcLocalBtn.setEnabled(False)
        self.ui.SelectedFileLabel.setText("")

    def on_src_api_changed(self):
        """Updates destination combo box content"""
        dstAPIs = self.APIs.copy()
        dstAPIs.remove(self.ui.SourceList.currentText())
        self.ui.DestinationList.clear()
        self.ui.DestinationList.addItems(dstAPIs)

    def clean_up(self):
        self.src_album = None
        self.remote_image_id = None
        self.local_image = None
