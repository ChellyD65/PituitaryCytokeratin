# gui.py
# Marcello DiStasio
# October 2019

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QFileDialog, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5.QtGui import QPixmap, QImage, qRgb

import os
import numpy as np

class MainGUI(QDialog):

    def __init__(self, parent=None, imageoperator=None):
        super(MainGUI, self).__init__(parent)

        self.imageoperator = imageoperator

        self.originalPalette = QApplication.palette()

        # styleComboBox = QComboBox()
        # styleComboBox.addItems(QStyleFactory.keys())

        # styleLabel = QLabel("&Style:")
        # styleLabel.setBuddy(styleComboBox)

        self.btnFileOpen = QPushButton("Choose image file...")
        self.btnFileOpen.clicked.connect(self.getfile)

        self.leInputImage = QLabel()
        self.leInputImage.setPixmap(QPixmap(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','..','resources','emptyspace.png'))).scaledToHeight(400))

        self.leOutputImage = QLabel()
        self.leOutputImage.setPixmap(QPixmap(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','..','resources','emptyspace.png'))).scaledToHeight(400))

        #self.createTopLeftGroupBox()
        #self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomLeftGroupBox()
        self.createProgressBar()

        # Top row of GUI, with image displays
        topLeftLayout = QGroupBox("Input Image")
        layout = QVBoxLayout()
        layout.addWidget(self.leInputImage)
        layout.addWidget(self.btnFileOpen)
        layout.addStretch(1)
        topLeftLayout.setLayout(layout)

        topRightLayout = QGroupBox("Output Image")
        layout = QVBoxLayout()
        layout.addWidget(self.leOutputImage)
        layout.addStretch(1)
        topRightLayout.setLayout(layout)

        topLayout = QHBoxLayout()
        topLayout.addWidget(topLeftLayout)
        topLayout.addWidget(topRightLayout)



        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Pituitary Cytokeratin Spatial Frequency")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Processing")
        # self.bottomLeftGroupBox.setCheckable(True)
        # self.bottomLeftGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        #lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomLeftGroupBox)
        spinBox.setValue(50)

        #dateTimeEdit = QDateTimeEdit(self.bottomLeftGroupBox)
        #dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomLeftGroupBox)
        slider.setValue(40)

        # scrollBar = QScrollBar(Qt.Horizontal, self.bottomLeftGroupBox)
        # scrollBar.setValue(60)

        dial = QDial(self.bottomLeftGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        self.btnProcess = QPushButton("Process!")
        self.btnProcess.clicked.connect(self.processInputImage)

        layout = QGridLayout()
        #layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        #layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        #layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.addWidget(self.btnProcess)
        layout.setRowStretch(5, 1)
        self.bottomLeftGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        #timer = QTimer(self)
        #timer.timeout.connect(self.advanceProgressBar)
        #timer.start(1000)

    def getfile(self):
        self.inputfname = QFileDialog.getOpenFileName(self, 'Open file', 
                                                      '~',"Image files (*.*)")
        if os.path.isfile(self.inputfname[0]):
            self.inputfile = self.inputfname[0]
            self.leInputImage.setPixmap(QPixmap(self.inputfile).scaledToHeight(400))





    def processInputImage(self):

        print("Processing")
        r = self.imageoperator.processImage(self.inputfile)

        imout = np.int8(np.floor(255*np.stack((r,)*3, axis=-1)))
        h, w, c = imout.shape
        bytesPerLine = w * 3

        qpix = QPixmap.fromImage(QImage(imout, w, h, bytesPerLine, QImage.Format_RGB888))
        self.leOutputImage.setPixmap(qpix.scaledToHeight(400))
