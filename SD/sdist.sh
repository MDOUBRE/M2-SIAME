#!/bin/sh
set 127.0.0.1

xterm -e "python3 tp.py 1883; $SHELL" &
sleep 1 
xterm -e "python3 tp.py 10000 $1 1883; $SHELL" &
sleep 1
xterm -e "python3 tp.py 20000 $1 10000; $SHELL" &
sleep 1
xterm -e "python3 tp.py 30000 $1 1883; $SHELL" &

sleep 10
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &
sleep 1
xterm -e "python3 put.py" &

sleep 2
xterm -e "python3 tp.py 40000 $1 1883; $SHELL" &

sleep 10
xterm -e "python3 get.py" &
sleep 5
xterm -e "python3 get.py" &
sleep 15

xterm -e "python3 quit.py" &
