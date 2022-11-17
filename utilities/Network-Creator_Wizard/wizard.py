from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import *
from PyQt5.QtGui import *
import sys

app = QApplication(sys.argv)
window = QWidget()

def can():
    app.exit(0)

def next():
    window.hide()
    page2.show()

def back():
    page2.hide()
    window.show()

window.setObjectName("Dialog")
window.setWindowModality(QtCore.Qt.NonModal)
window.setFixedSize(400, 300)
window.setWindowIcon(QIcon('icon.png'))
sizePolicy = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
sizePolicy.setHorizontalStretch(0)
sizePolicy.setVerticalStretch(0)
sizePolicy.setHeightForWidth(window.sizePolicy().hasHeightForWidth())
window.setSizePolicy(sizePolicy)
window.setStatusTip("")
window.setWhatsThis("")
Cancel = QtWidgets.QPushButton(window)
Cancel.setGeometry(QtCore.QRect(320, 270, 75, 23))
Cancel.setObjectName("Cancel")
Cancel.clicked.connect(can)
btnNext = QtWidgets.QPushButton(window)
btnNext.setGeometry(QtCore.QRect(230, 270, 75, 23))
btnNext.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
btnNext.setObjectName("btnNext")
btnNext.clicked.connect(next)
btnBack = QtWidgets.QPushButton(window)
btnBack.setEnabled(False)
btnBack.setGeometry(QtCore.QRect(150, 270, 75, 23))
btnBack.setCheckable(False)
btnBack.setChecked(False)
btnBack.setAutoRepeat(False)
btnBack.setAutoDefault(True)
btnBack.setDefault(False)
btnBack.setFlat(False)
btnBack.setObjectName("btnBack")
line = QtWidgets.QFrame(window)
line.setGeometry(QtCore.QRect(10, 250, 381, 20))
line.setFrameShape(QtWidgets.QFrame.HLine)
line.setFrameShadow(QtWidgets.QFrame.Sunken)
line.setObjectName("line")
label = QtWidgets.QLabel(window)
label.setGeometry(QtCore.QRect(10, 10, 121, 231))
label.setText("")
label.setPixmap(QtGui.QPixmap("image.jpg"))
label.setObjectName("label")
label_2 = QtWidgets.QLabel(window)
label_2.setGeometry(QtCore.QRect(150, -10, 251, 61))
font = QtGui.QFont()
font.setPointSize(11)
font.setBold(True)
font.setWeight(75)
label_2.setFont(font)
label_2.setObjectName("label_2")
label_3 = QtWidgets.QLabel(window)
label_3.setGeometry(QtCore.QRect(150, 20, 241, 151))
label_3.setObjectName("label_3")
radioButton = QtWidgets.QRadioButton(window)
radioButton.setEnabled(True)
radioButton.setGeometry(QtCore.QRect(150, 170, 181, 17))
radioButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
radioButton.setChecked(True)
radioButton.setObjectName("radioButton")
radioButton_2 = QtWidgets.QRadioButton(window)
radioButton_2.setEnabled(False)
radioButton_2.setGeometry(QtCore.QRect(150, 190, 171, 17))
radioButton_2.setObjectName("radioButton_2")


window.setTabOrder(btnNext, Cancel)
window.setTabOrder(Cancel, btnBack)

_translate = QtCore.QCoreApplication.translate
window.setWindowTitle(_translate("Dialog", "Network-Creation Wizard"))
Cancel.setText(_translate("Dialog", "Cancel"))
btnNext.setText(_translate("Dialog", "Next >"))
btnBack.setText(_translate("Dialog", "< Back"))
label_2.setText(_translate("Dialog", "Welcome to Network-Creator"))
label_3.setText(_translate("Dialog", " This Wizard will help you create a new Network \n"
                           " from Development-Network. \n"
                           "\n"
                           " To create a network you\'ll need following things: \n"
                           " - Network-IP  \n"
                           "\n"
                           " To create new Network select Create new Nework below. \n"
                           " If you want to create a copied Network select \n"
                           " Create copied Network below."))
radioButton.setText(_translate("Dialog", "Create new Network"))
radioButton_2.setText(_translate("Dialog", "Create copied Network"))

def enableNextButton():
    btnNext2.setEnabled(True)

window.show()

def finish():
    networkAD = lineEdit.text()

    print(networkAD)
    sys.exit(0)

page2 = QWidget()
page2.setObjectName("Dialog")
page2.setWindowIcon(QIcon('icon.png'))
page2.setFixedSize(400, 300)
btnNext2 = QtWidgets.QPushButton(page2)
btnNext2.setEnabled(False)
btnNext2.setGeometry(QtCore.QRect(230, 270, 75, 23))
btnNext2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
btnNext2.setObjectName("btnNext")
btnNext2.clicked.connect(finish)
Cancel2 = QtWidgets.QPushButton(page2)
Cancel2.setGeometry(QtCore.QRect(320, 270, 75, 23))
Cancel2.setObjectName("Cancel")
Cancel2.clicked.connect(can)
line2 = QtWidgets.QFrame(page2)
line2.setGeometry(QtCore.QRect(10, 250, 381, 20))
line2.setFrameShape(QtWidgets.QFrame.HLine)
line2.setFrameShadow(QtWidgets.QFrame.Sunken)
line2.setObjectName("line")

btnBack2 = QtWidgets.QPushButton(page2)
btnBack2.setEnabled(True)
btnBack2.setGeometry(QtCore.QRect(150, 270, 75, 23))
btnBack2.setCheckable(False)
btnBack2.setChecked(False)
btnBack2.setAutoRepeat(False)
btnBack2.setAutoDefault(True)
btnBack2.setDefault(False)
btnBack2.setFlat(False)
btnBack2.setObjectName("btnBack")
btnBack2.clicked.connect(back)
label_4 = QtWidgets.QLabel(page2)
label_4.setGeometry(QtCore.QRect(10, 10, 121, 231))
label_4.setText("")
label_4.setPixmap(QtGui.QPixmap(
    "image.jpg"))
label_4.setObjectName("label_4")
label_2 = QtWidgets.QLabel(page2)
label_2.setGeometry(QtCore.QRect(150, -10, 251, 61))
font = QtGui.QFont()
font.setPointSize(11)
font.setBold(True)
font.setWeight(75)
label_2.setFont(font)
label_2.setObjectName("label_2")
label2 = QtWidgets.QLabel(page2)
label2.setGeometry(QtCore.QRect(150, 30, 241, 151))
label2.setObjectName("label")
lineEdit = QtWidgets.QLineEdit(page2)
lineEdit.setGeometry(QtCore.QRect(150, 210, 113, 20))
lineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
lineEdit.setAcceptDrops(False)
lineEdit.setAutoFillBackground(False)
lineEdit.setInputMask("")
lineEdit.setText("")
lineEdit.setMaxLength(11)
lineEdit.setFrame(True)
lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
lineEdit.setObjectName("lineEdit")
lineEdit.textChanged[str].connect(enableNextButton)
label_3 = QtWidgets.QLabel(page2)
label_3.setGeometry(QtCore.QRect(150, 190, 111, 16))
label_3.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
label_3.setObjectName("label_3")

QtCore.QMetaObject.connectSlotsByName(page2)
page2.setTabOrder(lineEdit, btnNext2)
page2.setTabOrder(btnNext2, btnBack2)
page2.setTabOrder(btnBack2, Cancel2)
_translate = QtCore.QCoreApplication.translate
page2.setWindowTitle(_translate("Dialog", "Network-Creation Wizard"))
btnNext2.setText(_translate("Dialog", "Finish"))
Cancel2.setText(_translate("Dialog", "Cancel"))
btnBack2.setText(_translate("Dialog", "< Back"))
label_2.setText(_translate("Dialog", "Network-Address"))
label2.setText(_translate("Dialog", " Now you need to specify the network address \n"
                              " (eg. 10.10.10).The network \n"
                              " address must be in range of 2 and 254 \n"
                              " Exceptions (these cannot be used): \n"
                              " - 255.255.255 \n"
                              " - 0.0.0 \n"
                              " - 1.1.1 \n"
                              "\n"
                              " If you\'ve already a network (eg. 192.168.178) \n"
                              " it\'s *not* recommended to use it here."))
label_3.setText(_translate("Dialog", "Network Address:"))

sys.exit(app.exec_())