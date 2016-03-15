import os
import sys
import signal
from multiprocessing import Process

from scapy.all import *

interface='wlp6s0'
APs ={}
chanDict = {}
Outputlist = []

def sniffAP(packet):

	if((packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp)
		and not APs.has_key(packet[Dot11].addr3))):
		ssid = packet[Dot11Elt].info
		bssid = packet[Dot11].addr3
		channel = str(ord(packet[Dot11Elt:3].info))

		APs[ssid] = bssid

		if ssid == "\x00": #\x00 truncated```	 
			ssid = "<Hidden>"

		if(str(packet[Dot11].addr3) not in Outputlist):
			Outputlist.append(ssid)
			Outputlist.append(bssid)
			Outputlist.append(channel)

	
i = 1
while i <12:
	subprocess.check_output(['iwconfig ' + interface + " channel " + str(i)], shell=True)
	sniff(iface=interface, prn=sniffAP,timeout=0.1)
	i += 1

print "------RESULTS------"
print "Number of SSIDs: ", len(APs)
print "Format: SSID,\tBSSID,\tCHANNEL"
#print ssid +"\t"+ bssid +"\t"+ channel
print Outputlist
print "[+]Complete"

