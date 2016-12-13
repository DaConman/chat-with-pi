#! /bin/sh

case "$1" in
  start)
    echo "Starting voip"
    seren -d plughw:1,0 -D plughw:1,0 -N -C 0 -a
    ;;
  stop)
    echo "Stopping voip"
    
    killall
    ;;
  *)
    echo "Usage wrong"
    exit 1
    ;;
esac

exit 0

seren -d plughw:1,0 -D plughw:1,0 -N -C 0 -a
