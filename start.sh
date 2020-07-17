/home/pi/.local/bin/hass &
cd MiTemperature2/
nohup python3 LYWSD03MMC.py --callback sendtoMQTT.sh -b 1 --name mimeter -d A4:C1:38:84:A5:63 &
sleep 30
cd /home/pi/client-raspberrypi/bin/
python3 start.py