# coding: utf-8

'''

ModelComunication Class

'''
class ModelComunication(object):
    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = {
            "suport": {
                "simetric": simetric,
                "assimetric": assimetric
            },

        }
        self.selected = {
            "simetric": None,
            "assimetric": None,
        }

        self.keys = {
            "simetric": "",
            "public_key": "",
            "private_key": ""
        }

    def accordComunication(self, model):
        if (self.selectSimetric(model) and self.selectAssimetric(model)):
            return True
        return False

    def selectSimetric(self,model):
        for simetric_type in self.comunication["suport"]["simetric"]:
            for simetric_type_to in model.comunication["suport"]["simetric"]:
                if(simetric_type == simetric_type_to):
                    self.selected["simetric"] = simetric_type
                    model.selected["simetric"] = simetric_type
                    return True

        return False

    def selectAssimetric(self,model):
        for assimetric_type in self.comunication["suport"]["assimetric"]:
            for assimetric_type_to in model.comunication["suport"]["assimetric"]:
                if(assimetric_type == assimetric_type_to):
                    self.selected["assimetric"] = assimetric_type
                    model.selected["assimetric"] = assimetric_type
                    return True
        return False

'''

Server Class

'''
class Server(object):

    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)

    def accord(self, client):

        # Se foi acordado uma padrão para comunicação
        if(self.comunication.accordComunication(client.comunication)):

            # Gerar a chave privada e pública assimétrica
            if(self.comunication.selected["assimetric"] == 'rsa'):

                # Importa os dados da biblioteca para RSA
                from cryptography.hazmat.backends import default_backend
                from cryptography.hazmat.primitives.asymmetric import rsa
                from cryptography.hazmat.primitives import serialization

                # Gera uma chave privada
                self.__private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend()
                )

                # Gera a chave pública
                self.public_key = self.__private_key.public_key()

                # Retorna a chave públic
                return self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )

        return None

    def getPublicKey(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
'''

Client Class

'''
class Client(object):
    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)

    def request(self,server):
        self.public_key_request = server.accord(self)

        # Gerar a chave simétrica
        if(self.comunication.selected["simetric"] == 'fernet'):
            from cryptography.fernet import Fernet
            self.simetric_key = Fernet.generate_key()

        # Gerar a chave privada e pública assimétrica
        if(self.comunication.selected["assimetric"] == 'rsa'):

            # Importa os dados da biblioteca para RSA
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives.asymmetric import rsa


            # Gera uma chave privada
            self.__private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            # Gera a chave pública
            self.public_key = self.__private_key.public_key()

    def getPublicKey(self):
        from cryptography.hazmat.primitives import serialization
        return self.__private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def send_key(self):
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        key_encripted = self.public_key.encrypt(
            self.simetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return key_encripted
'''

Main

'''

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
