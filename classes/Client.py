#coding: utf-8
'''

Client Class

'''

from .ModelComunication import ModelComunication
import json 

class Client(object):

    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)

    def getSimetricKey(self):
        # Gerar a chave simétrica
        if(self.comunication.selected["simetric"] == 'fernet'):
            from cryptography.fernet import Fernet
            self.simetric_key = Fernet.generate_key()

        # Encripta a chave simétrica com a chave pública
        if(self.comunication.selected["assimetric"] == 'rsa'):

            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import padding

            public_key = load_pem_public_key(self.comunication.keys['public_key'], backend=default_backend())

            ciphekey = public_key.encrypt(
                 self.simetric_key,
                 padding.OAEP(
                     mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None
                 )
            )

            response = {
                "simetric_key": ciphekey.decode('latin-1')
            }

            return json.dumps(response).encode("utf-8")
    
    def sendMessage(self, message):
        pass