#-*- coding: utf-8 -*-
import socket
import json
import os

DEST = ('localhost' , 5000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(DEST)

FILE_PATH = input("Insira o caminho do arquivo: \n")

try:
  FILE = open(FILE_PATH, 'r')
  file_name, file_extension = os.path.splitext(FILE_PATH)

  file_info = {}
  file_info['name'] =  str(file_name.split('/')[-1])
  file_info['extension'] = file_extension.strip('.')

  file_info = json.dumps(file_info, ensure_ascii=False)

  print(file_info)

  server.send(file_info)

  for line in FILE:
    server.send(line)

  end_msg = {}
  end_msg['close'] = 1
  end_msg = json.dumps(end_msg, ensure_ascii=False)
  server.send(end_msg)

  server.close()

except Exception as e:
  print(e)
