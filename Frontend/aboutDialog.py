# Filename - aboutDialog.py
# Description - Used to display the About dropdown menu
"""
Revised by: Itai Marongwe
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.setWindowTitle("Wifi Auditing Tool v0.2 | About")

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)

        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("The Wifi Auditing Tool was developed by Carleton University.\n")
        self.textBrowser.append("Project Coordinator - Professor Richard Yu")
        self.textBrowser.append("richard.yu@carleton.ca\n")
        self.textBrowser.append("Programmer - Alexandru Viman")
        self.textBrowser.append("Programmer - Itai Marongwe")
        self.textBrowser.append("itaimarongwe@gmail.com")
        self.textBrowser.append("...")

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)


    # Modify this to change what OK does
    def accept(self):
        print ("Display more project info...")
        self.close()

    def showImage(self):
        print ("image is here")
        filename = r'./images/carleton.gif'
        image = QImage(filename)

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.imageLabel)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)


