#!/bin/bash

taskset -c 19 python socket_capture.py 10.0.0.100 2000 -o /dev/shm/10.0.0.100_2000.dat & 
taskset -c 20 python socket_capture.py 10.0.0.100 2001 -o /dev/shm/10.0.0.100_2001.dat &
taskset -c 23 python socket_capture.py 10.0.0.100 2002 -o /dev/shm/10.0.0.100_2001.dat&
taskset -c 24 python socket_capture.py 10.0.0.100 2003 -o /dev/shm/10.0.0.100_2002.dat &

taskset -c 6 python socket_capture.py 10.4.0.100 2004 -o /dev/shm/10.4.0.100_2004.dat &
taskset -c 7 python socket_capture.py 10.4.0.100 2005 -o /dev/shm/10.4.0.100_2005.dat &
taskset -c 10 python socket_capture.py 10.4.0.100 2006 -o /dev/shm/10.4.0.100_2006.dat &
taskset -c 11 python socket_capture.py 10.4.0.100 2007 -o /dev/shm/10.4.0.100_2007.dat &

taskset -c 22 python socket_capture.py 10.0.0.100 2008 -o /dev/shm/10.0.0.100_2008.dat & 
taskset -c 23 python socket_capture.py 10.0.0.100 2009  -o /dev/shm/10.0.0.100_2009.dat &
taskset -c 26 python socket_capture.py 10.0.0.100 2010  -o /dev/shm/10.0.0.100_2010.dat &
taskset -c 28 python socket_capture.py 10.0.0.100 2011  -o /dev/shm/10.0.0.100_2011.dat &

taskset -c 8 python socket_capture.py 10.4.0.100 2012 -o /dev/shm/10.4.0.100_2012.dat &
taskset -c 9 python socket_capture.py 10.4.0.100 2013 -o /dev/shm/10.4.0.100_2013.dat &
taskset -c 12 python socket_capture.py 10.4.0.100 2014 -o /dev/shm/10.4.0.100_2014.dat &
taskset -c 13 python socket_capture.py 10.4.0.100 2015 -o /dev/shm/10.4.0.100_2015.dat &

