#coding: utf-8
import socket
import json
import os
import sys
from classes.Server import Server

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

cm = Server(['fernet'], ['rsa'])
	

local_address = ('localhost', 8000)
local_address = ('localhost', 5000)
dest_address = ('localhost' , 5001)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Escuta respotas do cliente
server.bind(local_address)
server.listen(1)

print("wwww.server.com -> waiting for client comunication \n")

while True:
	
	client, client_address = server.accept()
	pid = os.fork()

	if(pid == 0):
	
		server.close()
		print(str(client_address) + "connected")

		while True:
			message = client.recv(1024).decode('utf-8')

			# Caso a mensagem enviada seja um JSON
			if(is_json(message)):
				data = json.loads(message)

				if("assimetric" in data.keys()):
					cm.accord(message, True)
					print(cm.private_key)
					print("make accord with client pattern successfuly!")
					server_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					server_sender.connect(dest_address)
					server_sender.send(cm.getResponseAccord())
					server_sender.close()
					
				if("simetric_key" in data.keys()):
					print("simetric key for comunication: ")
					print(cm.private_key)


			elif(message and not is_json(message)):
				print("new message: " + str(message))

		print("wwww.server.com -> close connection with " + str(client_address) +" \n ")
	else:
		client.close()
	