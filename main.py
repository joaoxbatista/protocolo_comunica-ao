# coding: utf-8

from classes.Server import Server
from classes.Client import Client

client = Client(['fernet'], ['rsa','diffie-helman'])
server = Server(['fernet'], ['rsa'])

client.request(server)

print("Public Key of Server")
print(client.public_key_request)
print("Public Key of Client")
print(client.getPublicKey())
print("Simetric key of client ")
print(client.simetric_key)
print("Simetric key of client encrypted")
print(client.send_key())
server.recepet()
