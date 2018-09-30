# coding: utf-8
import json

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

    def accordComunication(self, model, is_json = False):

        if(is_json):
            model = json.loads(model)

        if (self.selectSimetric(model) and self.selectAssimetric(model)):
            return True
        return False

    def selectSimetric(self,model):
        for simetric_type in self.comunication["suport"]["simetric"]:
            for simetric_type_to in model["simetric"]:
                if(simetric_type == simetric_type_to):
                    self.selected["simetric"] = simetric_type
                    return True
        return False

    def selectAssimetric(self,model):
        for assimetric_type in self.comunication["suport"]["assimetric"]:
            for assimetric_type_to in model["assimetric"]:
                if(assimetric_type == assimetric_type_to):
                    self.selected["assimetric"] = assimetric_type
                    return True
        return False

    def getSuport(self, encode = False):
        if(encode):
            return json.dumps(self.comunication["suport"]).encode('utf-8')
        return json.dumps(self.comunication["suport"])

    def getSelected(self, encode = False):
        if(encode):
            return json.dumps(self.comunication["selected"]).encode('utf-8')
        return json.dumps(self.comunication["selected"])

    
        