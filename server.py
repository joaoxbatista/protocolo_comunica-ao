#coding: utf-8
import socket
import json
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (('', 5000))

server.bind(orig)
server.listen(1)

print("Servidor Inciado, aguardando arquivos... \n ")

while True:
	message  = conn.recv(1024)
