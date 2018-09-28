# coding: utf-8

from classes.Client import Client
from classes.Server import Server

client = Client(['3des', 'aes'], ['rsa','diffie-helman'])
server = Server(['3des'], ['rsa'])

if(server.accord(client)):
    print("Acordo de comunicação realizado com sucesso!")
