#!/bin/sh
set 127.0.0.1

xterm -e "python3 tp.py 1883; $SHELL" &
sleep 1 
xterm -e "python3 tp.py 16000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 2000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 3000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 4000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 5000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 6000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 7000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 8000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 17000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 10000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 11000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 12000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 13000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 18000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 19000 $1 1883; $SHELL" &

sleep 10
for ((c=1;c<=100;c++))
do
    xterm -e "python3 put.py" &
    sleep 1
done


#sleep 2
#xterm -e "python3 tp.py 40000 $1 1883; $SHELL" &
#sleep 5

for ((c=1;c<=100;c++))
do
    xterm -e "python3 get.py" &
    sleep 1
done

sleep 5

xterm -e "python3 quit.py" &
