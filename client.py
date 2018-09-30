#-*- coding: utf-8 -*-
import socket
import json
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

'''
Verifica se a mensagem recebida é um JSON
'''
def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except ValueError as e:
		return False
	return True

def formatMessage(type ,key, data):
	result =  {
		"type_message": type,
		"data": {
			key: data
		}
	}
	result = json.dumps(result)
	return result.encode("utf-8")

def generate_keys():
	
	# Gera chave simetrica
	if(selected["simetric"] == "fernet"):
		keys["simetric"] = Fernet.generate_key()

	# Seleção do algoritmo assimétrico
	if(selected["assimetric"] == 'rsa'):
		# Gera uma chave privada
		keys["private_rsa"] = rsa.generate_private_key(
			public_exponent=65537,
			key_size=1028,
			backend=default_backend()
		)

		keys["public_rsa"] = keys["private_rsa"].public_key()
	

def encrypt_simetric_key():
    simetric_key = server_keys["public_key"].encrypt(
         keys["simetric"],
         padding.OAEP(
             mgf=padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )

    return simetric_key.decode("latin-1")

def encrypt_message(message):
	f = Fernet(keys["simetric"])
	encrypt_message = f.encrypt(message)
	return encrypt_message.decode('utf-8')

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
}

keys = {
    "simetric": None,
    "private_rsa": None,
    "public_rsa": None
}

server_keys = {
	"public_key": None
}


# '''
# 	1 - Conexão com o servidor
# '''
local_address = ('localhost', 5000)
dest_address = ('localhost' , 8001)


# '''
# 	2 - Enviar a primeira requisição para o acordo de comunicação
# '''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(dest_address)
server.send(formatMessage("accord_comunication", "suport", suport))

# '''
#   3 - Escuta reposta do tipo de comunicação selecionada 
# '''

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(local_address)
client.listen(1)
conn_server, add_server = client.accept()

while True:
	message = conn_server.recv(1024).decode('utf-8')

	if(is_json(message)):
		data = json.loads(message)

		if("type_message" in data.keys()):
			if(data["type_message"] == "selected_suport"):
				selected = data["data"]["selected"]
				server_keys["public_key"] = load_pem_public_key(selected["public_key"].encode('utf-8'), backend=default_backend())
				generate_keys()	
				server.send(formatMessage("send_simetric_key", "simetric_key", encrypt_simetric_key()))
				# print(formatMessage("send_simetric_key", "simetric_key", encrypt_simetric_key()))
				# server.send(formatMessage("send_simetric_key", "simetric_key", keys["simetric"].decode('utf-8')))
				break		
			
conn_server.close()		


'''
	4 - Envia mensagens para o servidor
'''

print("request for www.server.com ... ")
print("-------------------------------")
print("insert exit to exit program.")
print("-------------------------------\n")


while True:
    try:
        message_to_server = input("insert your text: \n")

        if(message_to_server == 'exit'):
        	break
        else:
        	server.send(formatMessage("message", "message", encrypt_message(message_to_server.encode('utf-8'))))
        	print("* your message is sended!\n")


    except Exception as e:
      print(e)
      break

server.close()