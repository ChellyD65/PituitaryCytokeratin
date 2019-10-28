# gui.py
# Marcello DiStasio
# October 2019

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QFileDialog, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QHeaderView)
from PyQt5.QtGui import QPixmap, QImage, qRgb

import os
import numpy as np
import csv


class MainGUI(QDialog):

    def __init__(self, parent=None, imageoperator=None):
        super(MainGUI, self).__init__(parent)

        self.inputfile = None
        self.batchfilenames = None

        self.imageoperator = imageoperator

        self.originalPalette = QApplication.palette()

        self.btnFileOpen = QPushButton("Choose image file...")
        self.btnFileOpen.clicked.connect(self.getfile)

        self.leInputImage = QLabel()
        self.leInputImage.setPixmap(QPixmap(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','..','resources','emptyspace.png'))).scaledToHeight(400))

        self.leOutputImage = QLabel()
        self.leOutputImage.setPixmap(QPixmap(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','..','resources','emptyspace.png'))).scaledToHeight(400))

        self.createBottomLeftTabWidget()
        self.createBottomRightTabWidget()
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


        # Bottom row of GUI, with processing functions
        bottomLeftLayout = QGroupBox("Processing")
        layout = QVBoxLayout()
        layout.addWidget(self.bottomLeftTabWidget)
        layout.addStretch(1)
        bottomLeftLayout.setLayout(layout)

        bottomRightLayout = QGroupBox("Results")
        layout = QVBoxLayout()
        layout.addWidget(self.bottomRightTabWidget)
        layout.addStretch(1)
        bottomRightLayout.setLayout(layout)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(bottomLeftLayout)
        bottomLayout.addWidget(bottomRightLayout)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(bottomLayout, 1, 0, 1, 2)
        mainLayout.addWidget(self.bottomLeftTabWidget, 1, 0)
        mainLayout.addWidget(self.bottomRightTabWidget, 1, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowMinimumHeight(1, 200)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Pituitary Cytokeratin Spatial Frequency")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())


    def createBottomLeftTabWidget(self):

        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.btnProcess = QPushButton("Process!")
        self.btnProcess.clicked.connect(self.processInputImage)
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.btnProcess)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        self.batchTableWidget = QTableWidget(10,1)
        self.batchTableWidget.setHorizontalHeaderLabels(["Filename"])
        header = self.batchTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(self.batchTableWidget)
        self.buttonBatchLoad = QPushButton("Load Files")
        self.buttonBatchLoad.clicked.connect(self.handleBatchLoad)
        tab2hbox.addWidget(self.buttonBatchLoad)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Processing")
        self.bottomLeftTabWidget.addTab(tab2, "&Batch")


    def createBottomRightTabWidget(self):
        self.bottomRightTabWidget = QTabWidget()
        self.bottomRightTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.tableWidget = QTableWidget(10, 2)
        self.tableWidget.setHorizontalHeaderLabels(["Filename", "Density Index"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.TableRowCursor = 0

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.tableWidget)

        self.buttonSave = QPushButton("Save CSV")
        self.buttonSave.clicked.connect(self.handleSave)
        tab1hbox.addWidget(self.buttonSave)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("The Magi\n"
                              "W. B. Yeats - 1865-1939\n"
                              "\n"
                              "Now as at all times I can see in the mind's eye,\n"
                              "In their stiff, painted clothes, the pale unsatisfied ones\n"
                              "Appear and disappear in the blue depth of the sky\n"
                              "With all their ancient faces like rain-beaten stones,\n"
                              "And all their helms of silver hovering side by side,\n"
                              "And all their eyes still fixed, hoping to find once more,\n"
                              "Being by Calvary's turbulence unsatisfied,\n"
                              "The uncontrollable mystery on the bestial floor.\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomRightTabWidget.addTab(tab1, "&Results")
        self.bottomRightTabWidget.addTab(tab2, "Free &Text")



    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)


    def getfile(self):
        self.inputfname = QFileDialog.getOpenFileName(self, 'Open file', 
                                                      '~',"Image files (*.*)")
        if os.path.isfile(self.inputfname[0]):
            self.inputfile = self.inputfname[0]
            self.leInputImage.setPixmap(QPixmap(self.inputfile).scaledToHeight(400))


    def handleBatchLoad(self):
        userlist = QFileDialog.getOpenFileNames(self, 'Open file', 
                                                      '~',"Image files (*.*)")
        self.batchfilenames = userlist[0]
        self.batchTableWidget.setRowCount(len(self.batchfilenames))
        self.batchTableWidget.clear()
        for row in range(len(self.batchfilenames)):
            self.inputfile = None
            self.batchTableWidget.setItem(row-1,1,QTableWidgetItem(os.path.basename(self.batchfilenames[row])))


    def processInputImage(self):

        if (self.inputfile):
            filelist = [self.inputfile]
            display_output_image = True
        elif (self.batchfilenames):
            filelist = self.batchfilenames
            display_output_image = False
        else:
            filelist = []
            print("No input file(s) specified!")
            return(0)

        self.progressBar.setRange(0, len(filelist))
        self.progressBar.setValue(0)
        for row in range(len(filelist)):
            infl = filelist[row]
            r = self.imageoperator.processImage(infl)
            di = r['density_index']
            
            if (display_output_image):
                imout = np.int8(np.floor(255*np.stack((r['bpdiffim'],)*3, axis=-1)))
                h, w, c = imout.shape
                bytesPerLine = w * 3
                qpix = QPixmap.fromImage(QImage(imout, w, h, bytesPerLine, QImage.Format_RGB888))
                self.leOutputImage.setPixmap(qpix.scaledToHeight(400))
                
                #print("Density index: {0:.2f}".format(di))

            nr = self.tableWidget.rowCount()
            if nr <= self.TableRowCursor:
                self.tableWidget.insertRow(nr)
            self.tableWidget.setItem(self.TableRowCursor, 0, QTableWidgetItem(os.path.basename(infl)))
            self.tableWidget.setItem(self.TableRowCursor, 1, QTableWidgetItem(str(di)))
            self.TableRowCursor = self.TableRowCursor + 1
            self.progressBar.setValue(row+1)



    def handleSave(self):
        p = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'CSV(*.csv)')
        path = p[0]
        if len(path):
            with open(path, 'w') as stream:
                writer = csv.writer(stream)
                for row in range(self.tableWidget.rowCount()):
                    rowdata = []
                    emptyrow = True
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                            emptyrow = False
                        else:
                            rowdata.append('')
                    if not emptyrow:
                        writer.writerow(rowdata)
