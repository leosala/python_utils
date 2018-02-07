
for i in 50 100 200 500 1000 1500 2000 2500 3000; do
    #LD_PRELOAD=/usr/lib64/libsdp.so 
    echo $i
    LD_PRELOAD=/usr/lib64/libsdp.so taskset -c 7 python zmq_sender.py --type PUSH --sizes $i --mode BIND  tcp://192.168.10.11:9998 &
    p=$!
    #LD_PRELOAD=/usr/lib64/libsdp.so 
    LD_PRELOAD=/usr/lib64/libsdp.so taskset -c 8 python zmq_sender.py --type PUSH  --sizes $i --mode BIND  tcp://192.168.10.11:9999
    kill -9 $p
done
