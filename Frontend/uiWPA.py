'''
# -*- coding: utf-8 -*-

# Dialog implementation generated from reading ui file 'WPA.ui'
#
# Created: Tue Feb  2 16:24:19 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!


import thread
import subprocess
import sys
import os
import time
from scapy.all import *
from PyQt4 import QtCore, QtGui

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

APs ={}
Outputlist = []
ssidlist = []
bssidlist = []
channellist = []

bssidToChannel = {}
bssidToSsid = {}
class uiWPA(QtGui.QDialog):
    def __init__(self, ifoi, parent=None):
        super(uiWPA, self).__init__(parent)

        self.interface = ifoi
        self.Channel = ''
        self.selectedSSID = ''
        self.setupUi(self)
        self.initScan()
        self.populateInfo()
        print "Passed Interface Name: " + self.interface

        #Select current interface
        self.selectedSourceInt = str(self.Source.currentText())
        self.setSourceMacAndChannel(self.selectedSourceInt)

        self.channelBox.setText(self.Channel)

        self.Source.currentIndexChanged[str].connect(self.setSourceMacAndChannel)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(550, 400)
        self.setMaximumSize(QtCore.QSize(550, 400))

        self.srclabel = QtGui.QLabel(Dialog)
        self.srclabel.setGeometry(QtCore.QRect(10, 10, 200, 16))
        self.srclabel.setObjectName(_fromUtf8("srclabel"))

        self.Source = QtGui.QComboBox(Dialog)
        self.Source.setGeometry(QtCore.QRect(10, 30, 525, 22))
        self.Source.setObjectName(_fromUtf8("Source"))

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 55, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.channelBox = QtGui.QLineEdit(Dialog)
        self.channelBox.setGeometry(QtCore.QRect(10, 80, 51, 22))
        self.channelBox.setText(_fromUtf8(""))
        self.channelBox.setMaxLength(2)
        self.channelBox.setEnabled(False)
        self.channelBox.setObjectName(_fromUtf8("channelBox"))

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.Comboboxitem = QtGui.QComboBox(Dialog)
        self.Comboboxitem.setGeometry(QtCore.QRect(10, 130, 201, 22))
        self.Comboboxitem.setObjectName(_fromUtf8("Comboboxitem"))

        self.Output = QtGui.QTextBrowser(Dialog)
        self.Output.setGeometry(QtCore.QRect(10, 190, 525, 160))
        self.Output.setObjectName(_fromUtf8("Output"))

        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 160, 381, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(365, 370, 171, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.pushButton_2.clicked.connect(self.initExecute) 
        self.pushButton_3.clicked.connect(self.closeWindow)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "WAT | WPA ATTACK", None))
        self.srclabel.setText(_translate("Dialog", "Target BSSID: ", None))
        self.label_2.setText(_translate("Dialog", "Channel:", None))
        self.label_3.setText(_translate("Dialog", "Select Dictionary :", None))
        self.pushButton_2.setText(_translate("Dialog", "Execute", None))
        self.pushButton_3.setText(_translate("Dialog", "Close", None))

    def initExecute(self):
        self.setChannel(self.Channel)
        self.Execute()
        #thread.start_new_thread(self.Execute, ()) - BAAAAAD IDEA

   #sudo sh ./WPA.sh -b 20:AA:4B:D9:5C:76 -c 6 -e CISCO_AP -i wlan2 -m wlan2mon
    def Execute(self):
        print "Execute..."
        process = subprocess.Popen('sh ./Backend/WPA.sh -b '+ self.selectedSourceInt +' -c ' + '11' + ' -e ' +self.selectedSSID +' -i ' + self.interface + ' -m ' +self.interface, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''

        for line in iter(process.stdout.readline, ""):
            print line,
            output += line
            #self.Output.append(line)

        process.wait()
        exitCode = process.returncode

        if (exitCode == 0):
            return output
        else:
            raise Exception(exitCode,output)
    

    def initScan(self):
        i = 1
        while i <=11:
            subprocess.check_output(['iwconfig '+ self.interface + ' channel ' + str(i)], shell=True)
            sniff(iface=self.interface, prn=self.sniffAP,timeout=0.3)
            i += 1

    def populateInfo(self):
        i = 0
        print "BSSID: \t\t\t\t\tCH:\tSSID:"
        while i < len(Outputlist):
            try:
                ssid = Outputlist[i]
                bssid = Outputlist[i+1]
                channel = Outputlist[i+2]

                bssidToChannel[bssid] = channel
                bssidToSsid[bssid] = ssid

                ssidlist.append(Outputlist[i])
                bssidlist.append(Outputlist[i+1])
                channellist.append(Outputlist[i+2])
            except:
                pass
            i += 3
            print bssid +"\t\t" + channel + "\t" + ssid
                    #Validating SSID -> BSSID -> Channel match up

        print "---------"
        print "Number of BSSIDs:", len(bssidlist)
        for k,v in bssidToChannel.items():
            print k
            self.Source.addItem(str(k))
        print "----"
        for k in bssidToSsid.items():
            print k 

    def sniffAP(self, packet): #Can be optimized - for faster execution?
        if((packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp))
            and not APs.has_key(packet[Dot11].addr3)):
            ssid = packet[Dot11Elt].info
            bssid = packet[Dot11].addr3
            channel = str(int(ord(packet[Dot11Elt:3].info)))

            if ssid == "\x00": #\x00 truncated```    
                ssid = "<Hidden>"

            if(str(packet[Dot11].addr3) not in Outputlist):
                Outputlist.append(ssid)
                Outputlist.append(bssid)
                Outputlist.append(channel)
            
            APs[ssid] = bssid


    def setSourceMacAndChannel(self, selected_source):
        self.selectedSourceInt = str(selected_source)  #Making focused Comboboxitem the selected item
        for k, v in bssidToSsid.items():
            if str(selected_source) in k:
                self.srclabel.setText("Source BSSID: " + v) #Setting Top Label to New SSID
                self.selectedSSID = str(v) #Setting variable for ssid  to ssid of interest)
                print "------------------//"
                print "Selected egress Interface: " + self.interface
                print "Selected SSID: " + v
                print "Selected BSSID: " + k
                self.Output.setText(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected SSID: </span>", None) + v)
                self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected BSSID: </span>", None) + k)

        for k, v in bssidToChannel.items():
            if(str(selected_source) in k):
                self.channelBox.setText(str(v))
                self.Channel = str(v)

    def setChannel(self, chNumber):
        try:
            subprocess.check_output(['iwconfig ' + self.interface + ' channel ' + str(chNumber)], shell=True)
            output = subprocess.check_output(['iwlist ' + self.interface + ' channel| egrep "Current"|sed s/" "//g'], shell=True)
            self.Frequency = output
        except error:
            print "[+] Could change Channel number...", error
            self.Output.append(_translate("self", "<span style =\"color:#ff000000; font-weight: bold;\">[Error]:</span> Could not set Channel number..." , None) + v)
        print output

    def closeWindow(self):
       	print "[+] Closing WEP attack..."
        self.close()
        return
'''

# -*- coding: utf-8 -*-

# Dialog implementation generated from reading ui file 'uiWPA.ui'
#
# Created: Wed Feb  3 17:04:08 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!
import thread
import multiprocessing
import sys
import os
import time
import re
from scapy.all import *
from PyQt4.QtGui import QFileDialog
from PyQt4 import QtCore, QtGui

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

APs ={}
Outputlist = []
ssidlist = []
bssidlist = []
channellist = []

bssidToChannel = {}
bssidToSsid = {}
class uiWPA(QtGui.QDialog):
    def __init__(self, ifoi, parent=None):
        super(uiWPA, self).__init__(parent)

        self.interface = ifoi
        self.Channel = ''
        self.selectedSSID = ''
        self.setupUi(self)
        self.initScan()
        self.populateInfo()

        print "Passed Interface Name: " + self.interface

        #Select current interface
        self.selectedSourceInt = str(self.Source.currentText())
        self.setSourceMacAndChannel(self.selectedSourceInt)

        self.Execute.clicked.connect(self.initExecute)
        self.Close.clicked.connect(self.closeWin)
        self.Dictionary.clicked.connect(self.selectFile)

        #Implementing Signal to update selected interface
        self.Source.currentIndexChanged[str].connect(self.setSourceMacAndChannel)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(483, 321)

        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.srclabel = QtGui.QLabel(Dialog)
        self.srclabel.setObjectName(_fromUtf8("srclabel"))

        self.verticalLayout_2.addWidget(self.srclabel)

        #DropDown for BSSID
        self.Source = QtGui.QComboBox(Dialog)
        self.Source.setObjectName(_fromUtf8("Source"))
        self.verticalLayout_2.addWidget(self.Source)
    
    #Channel Input
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)

        self.channelBox = QtGui.QLineEdit(Dialog)
        self.channelBox.setObjectName(_fromUtf8("channelBox"))
        self.channelBox.setFixedHeight(25)
        self.channelBox.setMaxLength(2)

        self.channelBox.setEnabled(False)
        self.verticalLayout_2.addWidget(self.channelBox)

    #Select Dictionary)
        self.Dictionary = QtGui.QPushButton(Dialog)
        self.Dictionary.setObjectName(_fromUtf8("Dictionary"))
        self.verticalLayout_2.addWidget(self.Dictionary)
    
    #Other buttons
        self.Execute = QtGui.QPushButton(Dialog)
        self.Execute.setObjectName(_fromUtf8("Execute"))
        self.verticalLayout_2.addWidget(self.Execute)

        self.Output = QtGui.QTextBrowser(Dialog)
        self.Output.setObjectName(_fromUtf8("Output"))

        self.verticalLayout_2.addWidget(self.Output)

        self.Close = QtGui.QPushButton(Dialog)
        self.Close.setObjectName(_fromUtf8("Close"))

        self.verticalLayout_2.addWidget(self.Close)

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "WAT  |  WPA Attack", None))
        self.srclabel.setText(_translate("Dialog", "Target BSSID: ", None))
        self.label_2.setText(_translate("Dialog", "Channel:", None))
        self.Close.setText(_translate("Dialog", "Close", None))
        self.Execute.setText(_translate("Dialog", "Execute", None))
        self.Dictionary.setText(_translate("Dialog", "Select Dictionary", None))

    def initExecute(self):
        self.setChannel(self.Channel)
        print "Channel: ", self.Channel
        #self.Execute()
        #thread.start_new_thread(self.Execute, ()) - BAAAAAD IDEA

   #sudo sh ./WPA.sh -b 20:AA:4B:D9:5C:76 -c 6 -e CISCO_AP -i wlan2 -m wlan2mon
    def Execute(self):
        print "Execute..."
        process = subprocess.Popen('sh ./Backend/WPA.sh -b '+ self.selectedSourceInt +' -c ' + str(self.Channel) + ' -e ' +self.selectedSSID +' -i ' + self.interface + ' -m ' +self.interface, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''

        for line in iter(process.stdout.readline, ""):
            print line,
            output += line
            #self.Output.append(line)

        process.wait()
        exitCode = process.returncode

        if (exitCode == 0):
            return output
        else:
            raise Exception(exitCode,output)
    

    def populateInfo(self):
        i = 0
        print "BSSID: \t\t\t\t\tCH:\tSSID:"
        while i < len(Outputlist):
            try:
                ssid = Outputlist[i]
                bssid = Outputlist[i+1]
                channel = Outputlist[i+2]

                bssidToChannel[bssid] = channel
                bssidToSsid[bssid] = ssid

                ssidlist.append(Outputlist[i])
                bssidlist.append(Outputlist[i+1])
                channellist.append(Outputlist[i+2])
            except:
                pass
            i += 3
            print bssid +"\t\t" + channel + "\t" + ssid
                    #Validating SSID -> BSSID -> Channel match up

        print "---------"
        print "Number of BSSIDs:", len(bssidlist)
        for k,v in bssidToChannel.items():
            print k
            self.Source.addItem(str(k))
        print "----"
        for k in bssidToSsid.items():
            print k 

    def initScan(self):
        i = 1
        while i <=11:
            subprocess.check_output(['iwconfig '+ self.interface + ' channel ' + str(i)], shell=True)
            sniff(iface=self.interface, prn=self.sniffAP,timeout=0.3)
            i += 1

    def setChannel(self, chNumber):
        try:
            subprocess.check_output(['iwconfig ' + self.interface + ' channel ' + str(chNumber)], shell=True)
            output = subprocess.check_output(['iwlist ' + self.interface + ' channel| egrep "Current"|sed s/" "//g'], shell=True)
            self.Frequency = output
        except error:
            print "[+] Could change Channel number...", error
            self.Output.append(_translate("self", "<span style =\"color:#ff000000; font-weight: bold;\">[Error]:</span> Could not set Channel number..." , None) + v)
        print output

    def setSourceMacAndChannel(self, selected_source):
        self.selectedSourceInt = str(selected_source)  #Making focused Comboboxitem the selected item
        for k, v in bssidToSsid.items():
            if str(selected_source) in k:
                self.srclabel.setText("Source BSSID: " + v) #Setting Top Label to New SSID
                self.selectedSSID = str(v) #Setting variable for ssid  to ssid of interest)
                print "------------------//"
                print "Selected egress Interface: " + self.interface
                print "Selected SSID: " + v
                print "Selected BSSID: " + k
                self.Output.setText(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected SSID: </span>", None) + v)
                self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected BSSID: </span>", None) + k)

        for k, v in bssidToChannel.items():
            if(str(selected_source) in k):
                self.channelBox.setText(str(v))
                self.Channel = str(v)
                
    def sniffAP(self, packet): #Can be optimized - for faster execution?
        if((packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp))
            and not APs.has_key(packet[Dot11].addr3)):
            ssid = packet[Dot11Elt].info
            bssid = packet[Dot11].addr3
            channel = str(int(ord(packet[Dot11Elt:3].info)))

            if ssid == "\x00": #\x00 truncated```    
                ssid = "<Hidden>"

            if(str(packet[Dot11].addr3) not in Outputlist):
                Outputlist.append(ssid)
                Outputlist.append(bssid)
                Outputlist.append(channel)
            
            APs[ssid] = bssid
     
    def selectFile(self):
        self.Dictionary.setText(QFileDialog.getOpenFileName())

    def Execute(self):
        print "Execute..."

    def closeWin(self):
        print "[+] Closing WPA attack..."
        self.close()

#Optimization - Use QThread to run attack and Scan
class worker(QtCore.QThread):
    def __init__(self, Parent=None):
        super(worker, self).__init__parent

    def __del__():
        print "lol"

    def run():
        print "lol"

