from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 850)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assests/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: #262D37;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainlabel = QtWidgets.QLabel(self.centralwidget)
        self.mainlabel.setGeometry(QtCore.QRect(250, 20, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.mainlabel.setFont(font)
        self.mainlabel.setStyleSheet("color:white;\n"
                                     "font: bold 18px;")
        self.mainlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainlabel.setObjectName("label")

        self.infolabel = QtWidgets.QLabel(self.centralwidget)
        self.infolabel.setGeometry(QtCore.QRect(230, 70, 341, 81))

        self.infolabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infolabel.setObjectName("infolabel")

        self.singlecb = QtWidgets.QCheckBox(self.centralwidget)
        self.singlecb.setGeometry(QtCore.QRect(300, 180, 200, 41))
        self.singlecb.setObjectName("signlerbutton")


        self.single_numberlabel = QtWidgets.QLabel(self.centralwidget)
        self.single_numberlabel.setGeometry(QtCore.QRect(120, 250, 240, 30))
        self.single_numberlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.single_numberlabel.setObjectName("single_numberlabel")

        self.single_accuracylabel = QtWidgets.QLabel(self.centralwidget)
        self.single_accuracylabel.setGeometry(QtCore.QRect(120, 290, 240, 30))
        self.single_accuracylabel.setAlignment(QtCore.Qt.AlignCenter)
        self.single_accuracylabel.setObjectName("single_accuracylabel")

        self.maxthresholdlabel = QtWidgets.QLabel(self.centralwidget)
        self.maxthresholdlabel.setGeometry(QtCore.QRect(120, 330, 240, 30))
        self.maxthresholdlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maxthresholdlabel.setObjectName("maxthreshold")


        self.single_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.single_acc_lineedit.setGeometry(QtCore.QRect(400, 250, 200, 30))
        self.single_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.single_nimage_lineedit.setGeometry(QtCore.QRect(400, 290, 200, 30))
        self.single_acc_lineedit.setEnabled(False)
        self.single_nimage_lineedit.setEnabled(False)

        self.maxthresholdlineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.maxthresholdlineedit.setGeometry(QtCore.QRect(400, 330, 200, 30))

        self.c_label = QtWidgets.QLabel(self.centralwidget)
        self.c_label.setGeometry(QtCore.QRect(100, 400, 241, 41))
        self.c_label.setObjectName("c_label")

        self.acc_label = QtWidgets.QLabel(self.centralwidget)
        self.acc_label.setGeometry(QtCore.QRect(310, 400, 241, 41))
        self.acc_label.setObjectName("acc_label")

        self.numberofimages = QtWidgets.QLabel(self.centralwidget)
        self.numberofimages.setGeometry(QtCore.QRect(550, 400, 241, 41))
        self.numberofimages.setObjectName("numberofimages")

        self.all_cb = QtWidgets.QCheckBox(self.centralwidget)
        self.all_cb.setGeometry(QtCore.QRect(100, 440, 150, 41))
        self.all_cb.setObjectName("all_cb")

        self.long_21cb = QtWidgets.QCheckBox(self.centralwidget)
        self.long_21cb.setGeometry(QtCore.QRect(100, 480, 150, 41))
        self.long_21cb.setObjectName("long_21")

        self.long_23cb = QtWidgets.QCheckBox(self.centralwidget)
        self.long_23cb.setGeometry(QtCore.QRect(100, 520, 150, 41))
        self.long_23cb.setObjectName("long_23")

        self.long_25cb = QtWidgets.QCheckBox(self.centralwidget)
        self.long_25cb.setGeometry(QtCore.QRect(100, 560, 150, 41))
        self.long_25cb.setObjectName("long_25")

        self.short_26cb = QtWidgets.QCheckBox(self.centralwidget)
        self.short_26cb.setGeometry(QtCore.QRect(100, 600, 150, 41))
        self.short_26cb.setObjectName("short_26")

        self.short_27cb = QtWidgets.QCheckBox(self.centralwidget)
        self.short_27cb.setGeometry(QtCore.QRect(100, 640, 150, 41))
        self.short_27cb.setObjectName("short_27")

        self.short_29cb = QtWidgets.QCheckBox(self.centralwidget)
        self.short_29cb.setGeometry(QtCore.QRect(100, 680, 150, 41))
        self.short_29cb.setObjectName("short_29")

        self.all_31_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.all_31_acc_lineedit.setGeometry(QtCore.QRect(340, 450, 100, 31))
        self.all_31_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.all_31_nimage_lineedit.setGeometry(QtCore.QRect(570, 450, 100, 31))
        self.all_31_acc_lineedit.setEnabled(False)
        self.all_31_nimage_lineedit.setEnabled(False)

        self.long21_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.long21_acc_lineedit.setGeometry(QtCore.QRect(340, 490, 100, 31))
        self.long21_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.long21_nimage_lineedit.setGeometry(QtCore.QRect(570, 490, 100, 31))
        self.long21_acc_lineedit.setDisabled(True)
        self.long21_nimage_lineedit.setDisabled(True)

        self.lt_long_23_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.lt_long_23_acc_lineedit.setGeometry(QtCore.QRect(340, 530, 100, 31))
        self.lt_long_23_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.lt_long_23_nimage_lineedit.setGeometry(QtCore.QRect(570, 530, 100, 31))
        self.lt_long_23_acc_lineedit.setDisabled(True)
        self.lt_long_23_nimage_lineedit.setDisabled(True)

        self.rt_long_25_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.rt_long_25_acc_lineedit.setGeometry(QtCore.QRect(340, 570, 100, 31))
        self.rt_long_25_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.rt_long_25_nimage_lineedit.setGeometry(QtCore.QRect(570, 570, 100, 31))
        self.rt_long_25_acc_lineedit.setDisabled(True)
        self.rt_long_25_nimage_lineedit.setDisabled(True)

        self.lt_short_26_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.lt_short_26_acc_lineedit.setGeometry(QtCore.QRect(340, 610, 100, 31))
        self.lt_short_26_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.lt_short_26_nimage_lineedit.setGeometry(QtCore.QRect(570, 610, 100, 31))
        self.lt_short_26_acc_lineedit.setDisabled(True)
        self.lt_short_26_nimage_lineedit.setDisabled(True)

        self.rt_short_27_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.rt_short_27_acc_lineedit.setGeometry(QtCore.QRect(340, 650, 100, 31))
        self.rt_short_27_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.rt_short_27_nimage_lineedit.setGeometry(QtCore.QRect(570, 650, 100, 31))
        self.rt_short_27_acc_lineedit.setDisabled(True)
        self.rt_short_27_nimage_lineedit.setDisabled(True)

        self.short29_acc_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.short29_acc_lineedit.setGeometry(QtCore.QRect(340, 690, 100, 31))
        self.short29_nimage_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.short29_nimage_lineedit.setGeometry(QtCore.QRect(570, 690, 100, 31))
        self.short29_acc_lineedit.setDisabled(True)
        self.short29_nimage_lineedit.setDisabled(True)

        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(330, 760, 120, 31))
        self.start_button.setObjectName("startbutton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mainlabel.setText(_translate("MainWindow", "CLASSIFIER"))
        self.singlecb.setText(_translate("MainWindow", "Set Default Values"))
        self.single_numberlabel.setText(_translate("MainWindow", "Enter Number of Image"))
        self.single_accuracylabel.setText(_translate("MainWindow", "Enter Accuracy (0-100)"))
        self.maxthresholdlabel.setText(_translate("MainWindow", "Set Max Threshold"))
        self.c_label.setText(_translate("MainWindow", "Classifier Labels"))
        self.infolabel.setText(_translate("MainWindow", " VIRTUOZUS"))
        self.acc_label.setText(_translate("MainWindow", "Enter Accuracy (0-100)"))
        self.numberofimages.setText(_translate("MainWindow", "Number of Images"))
        self.all_cb.setText(_translate("MainWindow", "All 31"))
        self.long_21cb.setText(_translate("MainWindow", "Long 21"))
        self.long_23cb.setText(_translate("MainWindow", "LT Long 23"))
        self.long_25cb.setText(_translate("MainWindow", "RT Long 25"))
        self.short_26cb.setText(_translate("MainWindow", "LT Short 26"))
        self.short_27cb.setText(_translate("MainWindow", "RT Short 27"))
        self.short_29cb.setText(_translate("MainWindow", "Short 29"))

        self.start_button.setText(_translate("MainWindow", "START"))
