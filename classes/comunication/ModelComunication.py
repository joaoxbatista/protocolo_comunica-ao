# coding: utf-8

class ModelComunication(object):



    def __init__(self, simetric = [''], assimetric = [''], hash = ['']):
        self.comunication = {
            "suport": {
                "simetric": simetric,
                "assimetric": assimetric,
                "hash": hash
            },

        }

        self.selected = {
            "simetric": None,
            "assimetric": None,
            "hash": None
        }


    def accordComunication(self, model):
        pass

    '''
    Getters and Setters
    '''
    def selectSimetric(self,model):

        print(model.selected)
        for simetric_type in self.comunication["suport"]["simetric"]:
            for simetric_type_to in model.comunication["suport"]["simetric"]:
                if(simetric_type == simetric_type_to):
                    self.selected["simetric"] = simetric_type
                    model.selected["simetric"] = simetric_type
                    print(model.selected)
                    return True

        return False

    def selectAssimetric(self,assimetric):
        for assimetric_type in self.comunication["suport"]["assimetric"]:
            if(assimetric_type == assimetric):
                self.selected["assimetric"] = assimetric
                return True
        return False

    def selectHash(self,hash):
        for hash_type in self.comunication["suport"]["hash"]:
            if(hash_type == hash):
                self.selected["hash"] = hash
                return True
        return False
