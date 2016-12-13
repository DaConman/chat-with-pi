l#! /bin/sh

case "$1" in
  start)
    echo "Starting voip"
    python /home/pi/Final_Project/voipmenurpi.py
    ;;
  stop)
    echo "Stopping voip"
    
    killall seren
    ;;
  *)
    echo "Usage wrong"
    exit 1
    ;;
esac

exit 0
