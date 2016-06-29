LD_PRELOAD=/usr/lib64/libsdp.so  taskset -c 7 python zmq_receiver.py --type PULL --mode CONNECT tcp://192.168.10.12:9998 &

LD_PRELOAD=/usr/lib64/libsdp.so taskset -c 8 python zmq_receiver.py --type PULL --mode CONNECT tcp://192.168.10.12:9999
