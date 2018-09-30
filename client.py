#-*- coding: utf-8 -*-
import socket
import json
import base64
import os
from classes.Client import Client

cm = Client(['fernet'], ['rsa'])

local_address = ('localhost', 5001)
dest_address = ('localhost' , 8000)
dest_address = ('localhost' , 5000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 1 - Enviar a primeira requisição para o acordo de comunicação
server.connect(dest_address)
server.send(cm.comunication.getSuport(True))
server.close()

# 2 - Escuta repostas do servidor 

client.bind(local_address)
client.listen(1)
conn_server, add_server = client.accept()

while True:
	message = conn_server.recv(1024).decode('utf-8')
	
	if(message != b''):
		try:
			if(json.loads(message)):
				response = json.loads(message)
				cm.comunication.keys['public_key'] = base64.decodestring(response["key"].encode('utf-8'))
				cm.comunication.selected = response["selected"]
				

		except Exception as e:
			print(e)

		# print("Mensagem recebida: " + message)
		break
conn_server.close		


# 3 - Envia a chave simetrica encriptada para o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(dest_address)
print("Enviando chave simetrica")
print(cm.getSimetricKey())
server.send(cm.getSimetricKey())
server.close()

while True:
	input()

# print("request for www.server.com ... ")
# print("-------------------------------")
# print("insert exit to exit program.")
# print("-------------------------------\n")

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.connect(dest_address)

# while True:
#     try:
#         message_to_server = input("insert your text: \n")

#         if(message_to_server == 'exit'):
#         	break

#         if(server.send(message_to_server.encode('utf-8'))):
#         	print("* your message is sended!\n")

        

#     except Exception as e:
#       print(e)
#       break

# server.close()