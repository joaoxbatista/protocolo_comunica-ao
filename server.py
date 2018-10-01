#coding: utf-8
import socket
import json
import os
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding 
from cryptography.hazmat.primitives import hashes

'''
Métodos utilitários
'''
# 1 - Verifica se a string pode ser convertida para json
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

# 1 - Formata mensagens para envio
def formatMessage(type_message ,key, data, counter):
	counter = counter + 1
	result =  {
		"type_message": type_message,
		"data": {
			key: data
		},
		"r": counter
    }
	result = json.dumps(result)
	print("message content: " + result)
	return result.encode("utf-8")

# 2 - Seleciona os tipos em comum de comunicação
def select_comunication(server_suport, client_suport, selected):
	for server_simetric in server_suport["simetric"]:
	    for client_simetric in client_suport["simetric"]:
	    	if(server_simetric == client_simetric):
	        	selected["simetric"] = server_simetric


	for server_assimetric in server_suport["assimetric"]:
	    for client_assimetric in client_suport["assimetric"]:
	        if(server_assimetric == client_assimetric):
	            selected["assimetric"] = server_assimetric

# 3 - Gerar chaves
def generate_keys(selected, keys):

	# Seleção do algoritmo assimétrico
	if(selected["assimetric"] == 'rsa'):

		# Gera uma chave privada
		keys["private_rsa"] = rsa.generate_private_key(
			public_exponent=65537,
			key_size=1028,
			backend=default_backend()
		)

		keys["public_rsa"] = keys["private_rsa"].public_key()

# 4 - Obter chave publica descerializada
def get_public_key():
	return keys["public_rsa"].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')


# 5 - Desencripta mesnsagem com chave simetrica do cliente
def decrypt_message(message):
	f = Fernet(keys["simetric"])	
	#Define o ttl da mensagem
	return f.decrypt(message.encode('utf-8'), 2).decode('utf-8')


'''
Padrão de Comunicação Selecionado
'''
suport = {
    "simetric": ['fernet'],
    "assimetric": ['rsa']
}

selected = {
    "simetric": None,
    "assimetric": None,
    "public_key": None
}

keys = {
    "simetric": "",
    "private_rsa": None,
    "public_rsa": None
}

counter = 0

'''
Definir a chave Privada
'''

local_address = ('localhost', 8001)
dest_address = ('localhost' , 5000)

'''
Espera conexão com o cliente
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

			if(not message):
				print("not message erro")
				
			# Caso a mensagem enviada seja um JSON
			elif(is_json(message)):
				data = json.loads(message)
				print("local_r: " + str(counter) + " r: " + str(data["r"]))
				counter = data["r"]
				# Verifica se o contador está de acordo
				if(counter == data["r"]):
					if("type_message" in data.keys()):
						if(data["type_message"] == "accord_comunication"):
							
							select_comunication(suport, data["data"]["suport"], selected)
							generate_keys(selected, keys)
							selected["public_key"] = get_public_key()

							# Enviar a chave publica para o cliente 
							print(selected)
							server_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							server_sender.connect(dest_address)
							server_sender.send(formatMessage("selected_suport", "selected", selected, counter))
							server_sender.close()
							

						elif(data["type_message"] == "send_simetric_key"):
							keys["simetric"] = data['data']['simetric_key']
							latin1 = keys['simetric'].encode('latin-1')
							keys["simetric"] = keys['private_rsa'].decrypt(
							     latin1,
							     padding.OAEP(
							         mgf=padding.MGF1(algorithm=hashes.SHA256()),
							         algorithm=hashes.SHA256(),
							         label=None
							     )
							)


						elif(data["type_message"] == "message"):
							counter = counter + 1
							print("-----------------------------------------------------------")
							print("\n* message counter: " + str(data["r"]))
							print("\n* message encrypted: " + data["data"]["message"])
							print("\n* message decrypted: " + decrypt_message(data["data"]["message"]))
							print("-----------------------------------------------------------")
							
					else:
						print("server not suport comunication with client")
				else: 
					print("message counter erro")
			else:
				pass
				
		print("wwww.server.com -> close connection with " + str(client_address) +" \n ")
	else:
		client.close()
	