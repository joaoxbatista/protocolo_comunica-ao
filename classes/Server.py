#coding: utf-8
from comunication.ModelComunication import ModelComunication
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Server(object):

    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)
        #
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048,
        #     backend=default_backend()
        # )

        # print(private_key)
        # print(private_key.public_key())

        # pks = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.PKCS8,
        #     encryption_algorithm=serialization.NoEncryption()
        # )
        #
        # pbs =  private_key.public_key().public_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PublicFormat.SubjectPublicKeyInfo,
        # )
        #
        # print(pbs.splitlines()[0])
        # print(pks.splitlines()[0])

    def accord(self, client):
        return self.comunication.accordComunication(client.comunication)

    def generateKeys(self):
        print(self.comunication)
