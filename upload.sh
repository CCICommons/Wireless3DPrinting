sshpass -p "raspberry" scp *.py pi@10.0.0.1:/home/pi/WirelessPrinting/
sshpass -p "raspberry" scp -r templates/ pi@10.0.0.1:/home/pi/WirelessPrinting/
sshpass -p "raspberry" scp -r miniMover/ pi@10.0.0.1:/home/pi/WirelessPrinting/