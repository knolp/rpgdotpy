nc 10.220.246.68 8888 <<< "usb all off"
nc 10.220.246.68 8888 <<< "relay all off"
sleep 0.1
nc 10.220.246.68 8888 <<< "relay all on"
nc 10.220.246.68 8888 <<< "usb all on"