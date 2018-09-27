# coding: utf-8

from classes.comunication.ModelComunication import ModelComunication

model = ModelComunication(['cesar'], ['rsa'], ['md5'])
model2 = ModelComunication(['cesar'], ['rsa'], ['md5'])

print(model.selectSimetric(model2))
