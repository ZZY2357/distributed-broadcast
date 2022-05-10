# "rss": relay server socket
# "rcs": relay client socket

import socket
from config_reader import ConfigReader
import threading
import time

config_reader = ConfigReader('config.json')

ss = socket.socket()

servers = []
server_address = config_reader.data['broadcast_servers']
clients = []

latest_message = ''

class Server:
    def __init__(self, addr):
        self.addr = addr
        self.ss = socket.socket()
        self.ss.connect(addr)

    def run(self):
        global latest_message
        msg = str(self.ss.recv(1024), encoding='utf-8')
        if msg and msg != latest_message:
            latest_message = msg
            broadcast(msg)

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

def broadcast(msg):
    for c in clients:
        c.send_to_it(time.asctime(time.localtime(time.time())) + ' ' + msg)

def fetching_thread(server):
    while True:
        server.run()

for s in server_address:
    server = Server((s['ip'], s['port']))
    servers.append(server)
    t = threading.Thread(target=fetching_thread, args=(server, ))
    t.start()

port = int(input('port: ')) # config_reader.data['host_server']['port'])

ss.bind((config_reader.data['host_server']['ip'],
    port))
ss.listen()

def new_client(addr, cs):
    c = Client(addr, cs)
    clients.append(c)
    c.run()

while True:
    cs, addr = ss.accept()
    t = threading.Thread(target=new_client, args=(addr, cs))
    t.start()
