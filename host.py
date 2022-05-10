# "ss": server socket
# "cs": client socket

import socket
from config_reader import ConfigReader
import threading
import time

config_reader = ConfigReader('config.json')

ss = socket.socket()
host = config_reader.data['host_server']['ip']
port = int(input('port: ')) # config_reader.data['host_server']['port']

ss.bind((host, port))
ss.listen()

clients = []

class Client:
    def __init__(self, addr, cs):
        self.addr = addr
        self.cs = cs
        self.alive = True

    def send_to_it(self, message):
        self.cs.send(bytes(message, encoding='utf-8'))

    def run(self):
        while self.alive:
            pass
        self.cs.close()

def new_client(addr, cs):
    c = Client(addr, cs)
    clients.append(c)
    c.run()

def read_input():
    while True:
        i = input()
        for c in clients:
            c.send_to_it(time.asctime(time.localtime(time.time())) + ' ' + i)

read_input_thread = threading.Thread(target=read_input)
read_input_thread.start()

while True:
    cs, addr = ss.accept()
    t = threading.Thread(target=new_client, args=(addr, cs))
    t.start()
