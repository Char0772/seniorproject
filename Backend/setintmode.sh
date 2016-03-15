#!/bin/sh

# BY: ITAI MARONGWE
# THIS SCRIPT WILL TURN A CAPABLE INTERFACE INTO MONITOR MODE
# USAGE: sudo sh ./iface.sh -i <interface> -m mode -t <mode> 

#Caputre Arguements as variables
while echo $1 | grep -q ^-; do
  eval $( echo $1 | sed  's/^-//' )=$2
  shift
  shift
done

if [ -z $i ] || [ -z $m ] || [ -z $t ]; then
  echo "Usage: Missing Arguements"
  exit 1
fi

echo i = $i #INTERFACE  (i.e  -i wlp6s0)
echo m = $m #ARGUEMENT  (i.e -m mode ) - Kinda unecessary
echo t = $t #MODE (i.e -t Managed/Monitor)


# '='' in bash is the equivelent of '=='
if [ "$t" = "monitor" ]; then
  echo "Setting to Monitor Mode..."
  ifconfig $i down
  service NetworkManager stop
  systemctl stop NetworkManager.service
  systemctl disable NetworkManager.service
  iwconfig $i $m $t
else
  echo "Setting to Managed Mode..."
  ifconfig $i down
  iwconfig $i $m $t
  service NetworkManager start
  systemctl start NetworkManager.service
  systemctl enable NetworkManager.service
fi

ifconfig $i up

exit
