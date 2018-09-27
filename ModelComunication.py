# coding: utf-8
class ModelComunication(object):

    def __init__(self):

        self.comunication = {
            "suport": {
                "simetric": false,
                "assimetric": false,
                "hash": false
            },
            "default": None
        }
        self.comunication_selected = self.comunication["default"]

        self.encryptation = {
            "suport": [""]
            "default": None
        }
        self.encryptation_selected = self.encryptation["default"]


    
