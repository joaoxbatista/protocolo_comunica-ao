#coding: utf-8
from comunication.ModelComunication import ModelComunication

class Client(object):

    def __init__(self, simetric = [''], assimetric = ['']):
        self.comunication = ModelComunication(simetric, assimetric)

    def accord(self, server):
        return self.comunication.accordComunication(server.comunication)
