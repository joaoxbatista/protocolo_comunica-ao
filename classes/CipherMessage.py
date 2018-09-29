# coding: utf-8

# 1 - Simetric Encryptation
# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# message = "something there"
# f = Fernet(key)
# token = f.encrypt(message.encode('utf-8'))
# print(token)
# print(f.decrypt(token))


# 2 - Assimetric Encryptation
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
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
