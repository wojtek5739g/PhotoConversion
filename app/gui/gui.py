# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(908, 639)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(30, 20, 841, 591))
        self.stackedWidget.setObjectName("stackedWidget")
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Settings)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 821, 571))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(100, 0, 100, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.SourceLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SourceLabel.sizePolicy().hasHeightForWidth())
        self.SourceLabel.setSizePolicy(sizePolicy)
        self.SourceLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.SourceLabel.setObjectName("SourceLabel")
        self.verticalLayout.addWidget(self.SourceLabel)
        self.SourceList = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.SourceList.setObjectName("SourceList")
        self.verticalLayout.addWidget(self.SourceList)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.DestinationLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.DestinationLabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DestinationLabel.sizePolicy().hasHeightForWidth())
        self.DestinationLabel.setSizePolicy(sizePolicy)
        self.DestinationLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.DestinationLabel.setObjectName("DestinationLabel")
        self.verticalLayout.addWidget(self.DestinationLabel)
        self.DestinationList = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.DestinationList.setEnabled(True)
        self.DestinationList.setObjectName("DestinationList")
        self.verticalLayout.addWidget(self.DestinationList)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.DatabaseTrigger = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.DatabaseTrigger.setEnabled(True)
        self.DatabaseTrigger.setObjectName("DatabaseTrigger")
        self.verticalLayout.addWidget(self.DatabaseTrigger)
        self.ContinueBtnSet = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ContinueBtnSet.setMaximumSize(QtCore.QSize(300, 16777215))
        self.ContinueBtnSet.setCheckable(False)
        self.ContinueBtnSet.setAutoRepeat(False)
        self.ContinueBtnSet.setAutoExclusive(False)
        self.ContinueBtnSet.setAutoDefault(False)
        self.ContinueBtnSet.setDefault(False)
        self.ContinueBtnSet.setFlat(False)
        self.ContinueBtnSet.setObjectName("ContinueBtnSet")
        self.verticalLayout.addWidget(self.ContinueBtnSet, 0, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.Settings)
        self.AuthWindow = QtWidgets.QWidget()
        self.AuthWindow.setObjectName("AuthWindow")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.AuthWindow)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 821, 571))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_5.setContentsMargins(100, 0, 100, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.AuthLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AuthLabel.sizePolicy().hasHeightForWidth())
        self.AuthLabel.setSizePolicy(sizePolicy)
        self.AuthLabel.setMaximumSize(QtCore.QSize(1000, 20))
        self.AuthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AuthLabel.setObjectName("AuthLabel")
        self.verticalLayout_5.addWidget(self.AuthLabel)
        spacerItem5 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem5)
        self.BackButAuth = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.BackButAuth.setMaximumSize(QtCore.QSize(300, 16777215))
        self.BackButAuth.setCheckable(False)
        self.BackButAuth.setAutoRepeat(False)
        self.BackButAuth.setAutoExclusive(False)
        self.BackButAuth.setAutoDefault(False)
        self.BackButAuth.setDefault(False)
        self.BackButAuth.setFlat(False)
        self.BackButAuth.setObjectName("BackButAuth")
        self.verticalLayout_5.addWidget(self.BackButAuth, 0, QtCore.Qt.AlignHCenter)
        spacerItem6 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.stackedWidget.addWidget(self.AuthWindow)
        self.SrcWindow = QtWidgets.QWidget()
        self.SrcWindow.setObjectName("SrcWindow")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.SrcWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(19, 550, 821, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BackBtnSrc = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.BackBtnSrc.setObjectName("BackBtnSrc")
        self.horizontalLayout.addWidget(self.BackBtnSrc)
        self.ContinueBtnSrc = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.ContinueBtnSrc.setEnabled(False)
        self.ContinueBtnSrc.setObjectName("ContinueBtnSrc")
        self.horizontalLayout.addWidget(self.ContinueBtnSrc)
        self.SrcLabel = QtWidgets.QLabel(self.SrcWindow)
        self.SrcLabel.setGeometry(QtCore.QRect(20, 10, 211, 20))
        self.SrcLabel.setObjectName("SrcLabel")
        self.SrcSelectedLabel = QtWidgets.QLabel(self.SrcWindow)
        self.SrcSelectedLabel.setGeometry(QtCore.QRect(330, 10, 511, 20))
        self.SrcSelectedLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SrcSelectedLabel.setObjectName("SrcSelectedLabel")
        self.scrollArea = QtWidgets.QScrollArea(self.SrcWindow)
        self.scrollArea.setGeometry(QtCore.QRect(20, 39, 821, 501))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 20, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridSrc = QtWidgets.QGridLayout()
        self.gridSrc.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridSrc.setContentsMargins(0, -1, 0, -1)
        self.gridSrc.setObjectName("gridSrc")
        self.verticalLayout_2.addLayout(self.gridSrc)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.stackedWidget.addWidget(self.SrcWindow)
        self.srcLocal = QtWidgets.QWidget()
        self.srcLocal.setObjectName("srcLocal")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.srcLocal)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(20, 20, 821, 571))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_8.setContentsMargins(100, 0, 100, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem7 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem7)
        self.SelectFileBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.SelectFileBtn.setObjectName("SelectFileBtn")
        self.verticalLayout_8.addWidget(self.SelectFileBtn)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_8.addItem(spacerItem8)
        self.SelectedFileLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.SelectedFileLabel.setText("")
        self.SelectedFileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SelectedFileLabel.setObjectName("SelectedFileLabel")
        self.verticalLayout_8.addWidget(self.SelectedFileLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BackBtnSrcLocal = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.BackBtnSrcLocal.setObjectName("BackBtnSrcLocal")
        self.horizontalLayout_2.addWidget(self.BackBtnSrcLocal)
        self.ContinueSrcLocalBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.ContinueSrcLocalBtn.setEnabled(False)
        self.ContinueSrcLocalBtn.setObjectName("ContinueSrcLocalBtn")
        self.horizontalLayout_2.addWidget(self.ContinueSrcLocalBtn)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem9)
        self.stackedWidget.addWidget(self.srcLocal)
        self.DstWindow = QtWidgets.QWidget()
        self.DstWindow.setObjectName("DstWindow")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.DstWindow)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 40, 821, 501))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_16 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_16.setGeometry(QtCore.QRect(0, 0, 20, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_16.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_16.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_16.setObjectName("scrollAreaWidgetContents_16")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_16)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.gridDst = QtWidgets.QGridLayout()
        self.gridDst.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridDst.setContentsMargins(0, -1, 0, -1)
        self.gridDst.setObjectName("gridDst")
        self.verticalLayout_20.addLayout(self.gridDst)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_16)
        self.DstSelectedLabel = QtWidgets.QLabel(self.DstWindow)
        self.DstSelectedLabel.setGeometry(QtCore.QRect(330, 11, 511, 20))
        self.DstSelectedLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DstSelectedLabel.setObjectName("DstSelectedLabel")
        self.DstLabel = QtWidgets.QLabel(self.DstWindow)
        self.DstLabel.setGeometry(QtCore.QRect(20, 11, 211, 20))
        self.DstLabel.setObjectName("DstLabel")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.DstWindow)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(19, 551, 821, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.BackBtnDst = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.BackBtnDst.setObjectName("BackBtnDst")
        self.horizontalLayout_16.addWidget(self.BackBtnDst)
        self.ContinueBtnDst = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.ContinueBtnDst.setEnabled(False)
        self.ContinueBtnDst.setObjectName("ContinueBtnDst")
        self.horizontalLayout_16.addWidget(self.ContinueBtnDst)
        self.stackedWidget.addWidget(self.DstWindow)
        self.Complete = QtWidgets.QWidget()
        self.Complete.setObjectName("Complete")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.Complete)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 20, 821, 571))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_4.setContentsMargins(100, 0, 100, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem10 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem10)
        self.ComplLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComplLabel.sizePolicy().hasHeightForWidth())
        self.ComplLabel.setSizePolicy(sizePolicy)
        self.ComplLabel.setMaximumSize(QtCore.QSize(1000, 1000))
        self.ComplLabel.setStyleSheet("font-size: 20px;")
        self.ComplLabel.setText("")
        self.ComplLabel.setObjectName("ComplLabel")
        self.verticalLayout_4.addWidget(self.ComplLabel, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem11)
        self.MetadataLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.MetadataLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MetadataLabel.setObjectName("MetadataLabel")
        self.verticalLayout_4.addWidget(self.MetadataLabel)
        self.ContinueBtnCompl = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.ContinueBtnCompl.setMaximumSize(QtCore.QSize(300, 16777215))
        self.ContinueBtnCompl.setCheckable(False)
        self.ContinueBtnCompl.setAutoRepeat(False)
        self.ContinueBtnCompl.setAutoExclusive(False)
        self.ContinueBtnCompl.setAutoDefault(False)
        self.ContinueBtnCompl.setDefault(False)
        self.ContinueBtnCompl.setFlat(False)
        self.ContinueBtnCompl.setObjectName("ContinueBtnCompl")
        self.verticalLayout_4.addWidget(self.ContinueBtnCompl, 0, QtCore.Qt.AlignHCenter)
        spacerItem12 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem12)
        self.stackedWidget.addWidget(self.Complete)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.SourceList, self.DestinationList)
        MainWindow.setTabOrder(self.DestinationList, self.DatabaseTrigger)
        MainWindow.setTabOrder(self.DatabaseTrigger, self.ContinueBtnSet)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Converter Demo"))
        self.SourceLabel.setText(_translate("MainWindow", "Source"))
        self.DestinationLabel.setText(_translate("MainWindow", "Destination"))
        self.DatabaseTrigger.setText(_translate("MainWindow", "Save in Databse"))
        self.ContinueBtnSet.setText(_translate("MainWindow", "Continue"))
        self.AuthLabel.setText(_translate("MainWindow", "Waiting For authentication"))
        self.BackButAuth.setText(_translate("MainWindow", "Back"))
        self.BackBtnSrc.setText(_translate("MainWindow", "Back"))
        self.ContinueBtnSrc.setText(_translate("MainWindow", "Continue"))
        self.SrcLabel.setText(_translate("MainWindow", "TextLabel"))
        self.SrcSelectedLabel.setText(_translate("MainWindow", "Select Image"))
        self.SelectFileBtn.setText(_translate("MainWindow", "SelectFile"))
        self.BackBtnSrcLocal.setText(_translate("MainWindow", "Back"))
        self.ContinueSrcLocalBtn.setText(_translate("MainWindow", "Continue"))
        self.DstSelectedLabel.setText(_translate("MainWindow", "Select Image"))
        self.DstLabel.setText(_translate("MainWindow", "TextLabel"))
        self.BackBtnDst.setText(_translate("MainWindow", "Back"))
        self.ContinueBtnDst.setText(_translate("MainWindow", "Continue"))
        self.MetadataLabel.setText(_translate("MainWindow", "TextLabel"))
        self.ContinueBtnCompl.setText(_translate("MainWindow", "Continue"))
