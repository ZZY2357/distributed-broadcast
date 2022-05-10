# "ss": server socket
# "cs": client socket

import socket
from config_reader import ConfigReader
import threading

config_reader = ConfigReader('config.json')
servers_address = config_reader.data['broadcast_servers']

servers = []
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
            print(msg)

def fetching_thread(server):
    while True:
        server.run()

for s in servers_address:
    server = Server((s['ip'], s['port']))
    servers.append(server)
    t = threading.Thread(target=fetching_thread, args=(server, ))
    t.start()

