import socket
import json
import random
import sys
import logging as log

IP = "192.168.0.35"
port = 20000

jsonFrame = { }
jsonFrame['type'] = "get"
jsonFrame['ip'] = "192.168.0.35"
jsonFrame['port'] = 10000
jsonFrame['key'] = 65534

# envoi du message et fermeture de la socket
print("\nEnvoi de ", jsonFrame)
print("vers ", IP, " ", port, "\n")

tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tpsoc_envoi.connect((IP, port))
except:
    try:
        tpsoc_envoi.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tpsoc_envoi.connect((IP, port))
    except socket.error as e:
        tpsoc_envoi.close()
        print("ERREUR SEND")
           
tpsoc_envoi.send(bytes(json.dumps(jsonFrame), "utf-8"))
tpsoc_envoi.close()

