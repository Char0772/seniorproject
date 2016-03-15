sudo iwlist wlp6s0 scan > temp.txt # 1 scan into temp Text - Improved performance
cat temp.txt | grep -e Cell | awk '{print $5}' > tempBSSID.txt
cat temp.txt | grep -e ESSID | awk '{print $1}' | cut -d ":" -f2 | sed s/\"//g > tempESSID.txt

#echo 
#echo
#cat tempESSID.txt | tr '\n' ' ' | awk '{print $1}'
#echo
#echo 
#cat tempBSSID.txt | tr '\n' ' '
#echo
#len="wc -l tempESSID.txt | cut -d ' ' -f1 "
#maxline=eval $len

for i in $(seq 1  10)
	do
		cat tempESSID.txt | tr '\n' ' ' | awk -v i="$i" '{print $i}'
		cat tempBSSID.txt | tr '\n' ' ' | awk -v i="$i" '{print $i}'
	done

exit