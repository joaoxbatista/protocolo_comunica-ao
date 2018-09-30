#coding: utf-8
'''

Server Class

'''

from .ModelComunication import ModelComunication
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization    
import json
import base64

class Server(object):
    private_key = None

    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)

    def accord(self, model, is_json = False):

        if(is_json):
            model = json.loads(model)

        if (self.comunication.accordComunication(model)):
          
            # Gerar a chave privada e pública assimétrica
            if(self.comunication.selected["assimetric"] == 'rsa'):

                # Gera uma chave privada
                self.private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=1028,
                    backend=default_backend()
                )

                from cryptography.hazmat.primitives import serialization

                pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')


        return False

        

    def getPublicKey(self):
        
        print("3 - Send key public")
        print(self.private_key)

        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def getResponseAccord(self):
        print("2 - Send acord with key public")
        print(self.private_key)

        response = {
            "selected": self.comunication.selected,
            "key": base64.encodestring(self.getPublicKey()).decode('utf-8')
        }
        
        return json.dumps(response).encode('utf-8')

    def getSimetricKey(self, encrypted_key):
       pass