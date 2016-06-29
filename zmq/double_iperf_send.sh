while [ 1 == 1 ]; do 
    iperf3 A 7 -O 2 -c 192.168.10.12 -p 5201 | grep "0.00-10.00"& 
    iperf3 A 8 -O 2 -c 192.168.10.12 -p 5202 | grep "0.00-10.00" ; 
    sleep 5; 
done
