#!/bin/bash

IPS="10.30.20.5"
PORTS=`seq 50000 50008`
PIDS=""
OUTDIR="/tmp"

for ip in $IPS; do
    for port in $PORTS; do
	python socket_capture.py $ip $port -o /$OUTDIR/$ip_$port.dat &
	PIDS="$! $PIDS"
    done
done

sleep 1
echo "After capture is completed, execute kill -9 "$PIDS
