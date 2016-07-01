#!/bin/bash

<<<<<<< HEAD
<<<<<<< HEAD
st=0.005

taskset -c 19 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2000.dat  10.0.0.100 2000  & 
sleep ${st}
taskset -c 20 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2001.dat  10.0.0.100 2001  &
sleep ${st}
taskset -c 23 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2002.dat  10.0.0.100 2002  &
sleep ${st}
taskset -c 24 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2003.dat  10.0.0.100 2003  &
sleep ${st}

taskset -c 6 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2004.dat  10.4.0.100 2004  &
sleep ${st}
taskset -c 7 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2005.dat  10.4.0.100 2005  &
sleep ${st}
taskset -c 10 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2006.dat  10.4.0.100 2006 &
sleep ${st}
taskset -c 11 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2007.dat  10.4.0.100 2007 &
sleep ${st}

taskset -c 22 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2008.dat  10.0.0.100 2008 & 
sleep ${st}
taskset -c 23 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2009.dat  10.0.0.100 2009 &
sleep ${st}
taskset -c 26 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2010.dat  10.0.0.100 2010 &
sleep ${st}
taskset -c 28 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2011.dat  10.0.0.100 2011 &
sleep ${st}

taskset -c 8 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2012.dat  10.4.0.100 2012 &
sleep ${st}
taskset -c 9 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2013.dat  10.4.0.100 2013 &
sleep ${st}
taskset -c 12 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2014.dat  10.4.0.100 2014 &
sleep ${st}
taskset -c 13 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2015.dat  10.4.0.100 2015 &
sleep ${st}
=======
taskset -c 19 python socket_replay.py 10.0.0.100_2000.dat  10.0.0.100 2000  & 
sleep 0.05
taskset -c 20 python socket_replay.py 10.0.0.100_2001.dat  10.0.0.100 2001  &
sleep 0.05
taskset -c 23 python socket_replay.py 10.0.0.100_2002.dat  10.0.0.100 2002  &
sleep 0.05
taskset -c 24 python socket_replay.py 10.0.0.100_2003.dat  10.0.0.100 2003  &
sleep 0.05
=======
st=0.005
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07

taskset -c 19 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2000.dat  10.0.0.100 2000  & 
sleep ${st}
taskset -c 20 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2001.dat  10.0.0.100 2001  &
sleep ${st}
taskset -c 23 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2002.dat  10.0.0.100 2002  &
sleep ${st}
taskset -c 24 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2003.dat  10.0.0.100 2003  &
sleep ${st}

taskset -c 6 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2004.dat  10.4.0.100 2004  &
sleep ${st}
taskset -c 7 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2005.dat  10.4.0.100 2005  &
sleep ${st}
taskset -c 10 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2006.dat  10.4.0.100 2006 &
sleep ${st}
taskset -c 11 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2007.dat  10.4.0.100 2007 &
sleep ${st}

<<<<<<< HEAD
taskset -c 8 python socket_replay.py 10.4.0.100_2012.dat  10.4.0.100 2012 &
sleep 0.05
taskset -c 9 python socket_replay.py 10.4.0.100_2013.dat  10.4.0.100 2013 &
sleep 0.05
taskset -c 12 python socket_replay.py 10.4.0.100_2014.dat  10.4.0.100 2014 &
sleep 0.05
taskset -c 13 python socket_replay.py 10.4.0.100_2015.dat  10.4.0.100 2015 &
sleep 0.05
>>>>>>> 4c02664... wip
=======
taskset -c 22 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2008.dat  10.0.0.100 2008 & 
sleep ${st}
taskset -c 23 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2009.dat  10.0.0.100 2009 &
sleep ${st}
taskset -c 26 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2010.dat  10.0.0.100 2010 &
sleep ${st}
taskset -c 28 python socket_replay.py /scratch/leo/Gigafrost_noise/10.0.0.100_2011.dat  10.0.0.100 2011 &
sleep ${st}

taskset -c 8 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2012.dat  10.4.0.100 2012 &
sleep ${st}
taskset -c 9 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2013.dat  10.4.0.100 2013 &
sleep ${st}
taskset -c 12 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2014.dat  10.4.0.100 2014 &
sleep ${st}
taskset -c 13 python socket_replay.py /scratch/leo/Gigafrost_noise/10.4.0.100_2015.dat  10.4.0.100 2015 &
sleep ${st}
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07

