import sys
import os
import subprocess
import thread
import time
from PyQt4 import QtGui, QtCore
from Frontend.aboutDialog import *
from Frontend.uiDA import *
from Frontend.uiWEP import *
from Frontend.uiWPA import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Widget(QtGui.QMainWindow):

    #Inititating Main Window Parameters
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        
        #Initializing Variables
        self.nics = []
        self.APs = []
        self.VIEW_Y = 70
        self.isMONMODE = False
        self.count = 0

        self.WelcomeText = (_translate("self", '''<span style=\" color: #218cff; font-weight: bold;\">[Notice]:</span>\nWelcome to the Wifi Auditing Tool. This tool is not
        intended for malicious use, it was made strictly for academic purposes. Carleton University and the creators of this application are NOT responsible 
        for any problems this tool may produce. \n''',None))

        #Initializing GUI
        self.initUI()
        self.getIfaces()

        #Setting default-selected interface
        self.ifoi = str(self.comboBox.currentText())

        #Welcome Message
        self.Output.setText(self.WelcomeText)

        self.Output.append("\n")
        self.Output.append(_translate("self",'<span style=\" color:#218cff; font-weight: bold;\">[Information]</span> - Selected Interface:  \n', None) + self.ifoi)

        #Initalizing Background Tasks and scanning APs
        self.checkMode()
        #self.scanforAPs() #The long delay when the screen builds is caused by this method

        #Implementing Signal to update selected interface
        self.comboBox.currentIndexChanged[str].connect(self.setIface)

    def initUI(self):
        self.setGeometry(250,50,650,550)
        self.setMinimumSize(QtCore.QSize(650, 555))
        self.setMaximumSize(QtCore.QSize(650, 700))
        self.setWindowTitle("WAT | Wifi Auditing Tool v0.6")

        #CentralWidget
        self.centralwidget = QtGui.QWidget(self)
        #Main Layout - Vertical Layout
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.line_1 = QtGui.QFrame(self.centralwidget)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_1.setObjectName(_fromUtf8("line_1"))

        self.verticalLayout_2.addWidget(self.line_1)

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(161, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setText("Select a Wireless Interface: ")

        self.horizontalLayout.addWidget(self.label_2, QtCore.Qt.AlignLeft)

        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.setMinimumWidth(140)
        self.horizontalLayout.addWidget(self.comboBox)

        self.toggleButton = QtGui.QPushButton(self.centralwidget)
        self.toggleButton.setObjectName(_fromUtf8("pushButton"))
        self.toggleButton.setText("Toggle Mode")
        self.toggleButton.clicked.connect(self.setMonitorMode)

        self.horizontalLayout.addWidget(self.toggleButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.verticalLayout_2.addWidget(self.line_2)

        self.ifOutLabel = QtGui.QLabel(self.centralwidget)
        self.ifOutLabel.setMinimumSize(QtCore.QSize(600, 200))
        self.ifOutLabel.setObjectName(_fromUtf8("ifOutLabel"))
        self.ifOutLabel.setStyleSheet('color: darkred; ')

        self.verticalLayout_2.addWidget(self.ifOutLabel)

        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.verticalLayout_2.addWidget(self.line)

        self.Output = QtGui.QTextBrowser(self.centralwidget)
        self.Output.setMinimumSize(QtCore.QSize(0, 150))
        self.Output.setObjectName(_fromUtf8("Output"))

        self.verticalLayout_2.addWidget(self.Output)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        #Menu Item Label definitition - Scan
        scanAction = QtGui.QAction(QtGui.QIcon('images/refresh_icon.png'), 'Scan', self)
        scanAction.setShortcut("Ctrl+shift+s")
        scanAction.triggered.connect(self.uiReconnaissance)

        #Menu Item Label definitition - WEP Attack
        wepAction = QtGui.QAction(QtGui.QIcon('images/wep_icon.png'), 'WEP Attack', self)
        wepAction.triggered.connect(self.wepAttack)

        #Menu Item Label definitition - WPA Attack
        wpaAction = QtGui.QAction(QtGui.QIcon('images/wpa_icon.png'), 'WPA Attack', self)
        wpaAction.triggered.connect(self.wpaAttack)

        #Menu Item Label definitition - deauth Attack
        deAuthAction = QtGui.QAction(QtGui.QIcon('images/deAuth_icon.png'), 'deAuth Attack', self)
        deAuthAction.triggered.connect(self.deAuthAttack)

        #Menu Item Label Definition - About Dialog
        aboutAction = QtGui.QAction('About', self)
        aboutAction.setShortcut("Ctrl+shift+b")
        aboutAction.triggered.connect(self.showAboutDialog)

        #Menu Item Label definitition - Exit
        exitAction = QtGui.QAction(QtGui.QIcon('images/exit_icon.png'), 'Exit', self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.triggered.connect(self.close_application)

        self.statusBar()

        #----TOOLBAR/MENU----
        #Menubar Creation
        mainMenu = self.menuBar()
        Menu = mainMenu.addMenu('&File')
        Menu.addAction(scanAction)
        Menu.addAction(deAuthAction)
        Menu.addAction(wepAction)
        Menu.addAction(wpaAction)
        Menu.addAction(exitAction)

        #Adding Menu Item Object to bar - Exit Menu Item
        helpMenu = mainMenu.addMenu("&Help")
        helpMenu.addAction(aboutAction)

        #Adding/Creating Actions to ToolBar
        self.toolbar = self.addToolBar('Scan')
        self.toolbar.setStyleSheet('QToolBar{spacing:5px;}')
        self.toolbar.addAction(scanAction)
        self.toolbar.insertSeparator(wepAction) #-Separator
        self.toolbar.addAction(deAuthAction)
        self.toolbar.addAction(wepAction)
        self.toolbar.addAction(wpaAction)
        self.toolbar.addAction(exitAction)
        self.toolbar.setMovable(False)
        self.toolbar.setOrientation(0x1)

        #Show GUI Items 
        self.show()

    ##UIRECONNAISSANCE FUNCTION
    #1. Re-Acquires Interfaces
    #2. Creates a "Worker Thread" to scan for APs in the area
    #   -Using the Interface of 
    def uiReconnaissance(self):
        self.Output.setText(self.WelcomeText)
        self.checkMode()

    def wepAttack(self):
        self.Output.setText(_translate("self", '<span style=\"color:#218cff; font-weight: bold;\">[Information]</span> - Initializing the WEP Attack...', None))
        if(self.isMONMODE == True):
            self.wepUI = uiWEP(self.ifoi)
            self.wepUI.exec_()
        else:
            self.Output.setText(_translate("self", '<span style=\"color:#FF0000;font-weight: bold;\">[Information]</span> - WEP Attack requires an interface to be in \'Monitor\' mode', None))

    def wpaAttack(self):
        if(self.isMONMODE == True):
            self.Output.setText(_translate("self", '<span style=\"color:#218cff; font-weight: bold;\">[Information]</span> - Initializing the WPA Attack...', None))
            self.wpaUI = uiWPA(self.ifoi)
            self.wpaUI.exec_()
        else:
            self.Output.setText(_translate("self", '<span style=\"color:#FF0000;font-weight: bold;\">[Information]</span> - WPA Attack requires an interface to be in \'Monitor\' mode', None))

    def deAuthAttack(self):
        if(self.isMONMODE == True):
            self.Output.setText(_translate("self", '<span style=\"color:#218cff; font-weight: bold;\">[Information]</span> - Initializing the Deauthentication Attack...', None))
            self.deAuthUI = uiDA(self.ifoi)
            self.deAuthUI.exec_()
        else:
            self.Output.setText(_translate("self", '<span style=\"color:#FF0000;font-weight: bold;\">[Information]</span> - Deauthentication Attack requires an interface to be in \'Monitor\' mode', None))
            
    def showAboutDialog(self):
        #TODO - FIX initation of object uiWEP, since the implementation of package
        self.aboutBox = MyDialog(self)
        self.aboutBox.showImage()
        self.aboutBox.exec_()

    #Close Application Method invoked by the Quit Button
    def close_application(self):
        self.Output.setText(_translate("self", '<span style=\"color:#218cff;font-weight: bold;\">[Information]</span> - Closing the Application...', None))
        choice = QtGui.QMessageBox.question(self, 'Quit Application!', "Are you sure you want to quit this Application?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print "Closing Application..."
            sys.exit()
        else:
            self.Output.setText(_translate("self", '<span style=\"color:#218cff;font-weight: bold;\">[Information]</span> - Exit Cancelled', None))
            pass

    ##GETIFACES METHOD
    #1.Check for the total number of interfaces - using sys/class/net
    #2. for every interface check to see if the 1. iwconfig works (wirless) - 802.11
    #2.5 If successful add it to the ComboBox
    def getIfaces(self):
        i = 0
        self.nics = []
        self.comboBox.clear()
        try:
            #Make REGEX for Detecting Wireless Interfacs that do NOT start with W
            self.nics.append((subprocess.check_output('ls /sys/class/net | egrep "^w|^r|^a"', shell=True)).split())
            print "[+]Wireless Interfaces: "
            for ifaces in self.nics[0]:
                output = subprocess.check_output('iwconfig '+self.nics[0][i], shell=True)
                if("ESSID" in str(output) or "802.11" in str(output)): #Checking to see if int is a Wireless Int
                    self.comboBox.addItem(self.nics[0][i])
                else:
                    print self.nics[0][i]+" is not a Compatible Wireless Interface..."
                print output
                i += 1
        except subprocess.CalledProcessError:
            print ("[+]There are no wireless cards available...")

    ##SETIFACES METHOD
    #Function to deal with received signal from changing the ComboBox Vale
    #Function will handle onChange actions
    #->setting global value of selected interface to self.ifoi
    def setIface(self, selected_Iface):
        self.ifoi  = str(selected_Iface)
        self.uiReconnaissance()
        self.Output.append("\n")
        self.Output.append(_translate("self",'<span style=\" color:#218cff; font-weight: bold;\">[Information]</span> - Selected Interface:  ', None) + self.ifoi)

    ##CHECKMODE METHOD
    #1.Function will check the status of the interface of Interest(ALL STATS)
    #2. Function will check if interface is in Monitor mode
    
    def checkMode(self):
        res = subprocess.check_output(['iwconfig '+ self.ifoi], shell = True)
        if("Monitor" in str(res)):
            self.isMONMODE = True
        else:
            self.isMONMODE = False
        #self.intLabelMon.setText((self.ifoi)+ " - in Monitor mode: "+str(self.isMONMODE))
        self.ifOutLabel.setText(res)
    
    ##SETMONITORMODE METHOD
    #1. Function will Set the Compatible Wireless Interface in to Monitor/Managed Mode
    #2. Fucntion will invoke CheckMode to ensrure that the Interfaces is in Monitor Mode
    def setMonitorMode(self):
        self.uiReconnaissance()
        if(self.isMONMODE == False):
            try:
                output = subprocess.check_output(['sh ./Backend/setintmode.sh -i ' + self.ifoi +' -m mode -t monitor'], shell= True)
                self.isMONMODE = True              
                print"[+]" + str(self.ifoi) +"is Monitor Mode: "+ str(self.isMONMODE)
            except:
                print "Failed to set "+ self.ifoi + " to Monitor Mode"
        elif(self.isMONMODE == True):
            try:
                timer = QtCore.QTimer()
                output = subprocess.check_output(['sh ./Backend/setintmode.sh -i ' + self.ifoi +' -m mode -t managed'], shell= True)
                self.isMONMODE = False
                print"[+]" + str(self.ifoi) +"is Monitor Mode: "+ str(self.isMONMODE)
            except:
                print "Failed to set " + self.ifoi + " to Managed Mode"

        self.checkMode()
    
def run():
    if os.geteuid() != 0: #Checking to see if the user has root privelages
        exit("[Program]:\n[+] WAT | WIFI Auditing Tool\n[+] This program requires root priveleges to run")
    app = QtGui.QApplication(sys.argv)
    GUI = Widget()
    sys.exit(app.exec_())

run()
