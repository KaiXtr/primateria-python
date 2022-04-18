import socket
import threading
import secret
import sys
import os

import resources as res

BYTES = 256
PORT = 5050
HOST = socket.gethostname()
SERVER = socket.gethostbyname(HOST)
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
INFO = {'connect': '{} foi conectado','disconnect': '{} foi desconectado.'}
UPDATE = ''

print(f'HOST: {HOST} | SERVER: {SERVER}')

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try: server.bind(ADDR)
except socket.error:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

def handleClient(conn,addr):
	global UPDATE
	cliname = addr[1]
	print(INFO['connect'].format(cliname))
	cht = []
	for i in res.CHAT: cht.append(i)

	connect = True
	while connect:
		#RECEIVE MESSAGES
		if UPDATE: cht.append(UPDATE)
		for i in cht:
			msg = i.encode(FORMAT)
			msg_lenght = len(msg)
			send_lenght = str(msg_lenght).encode(FORMAT)
			#send_lenght += b' ' * (BYTES - len(send_lenght))
			conn.send(msg)

		#GET MESSAGES
		msg_lenght = conn.recv(BYTES).decode(FORMAT)
		if msg_lenght:
			msg = conn.recv(int(msg_lenght)).decode(FORMAT)
			if msg == '!disconnect':
				print(INFO['disconnect'].format(cliname))
				connect = False
			elif msg == '!server': print(f'Server is {SERVER}')
			else:
				msg = f'@{cliname}: {msg}'
				UPDATE = msg
	conn.close()

def getClients():
	print('Starting...')
	server.listen(16)
	print(f'Listening in {SERVER}')
	while True:
		os.system('cls')
		conn, addr = server.accept()
		th = [
			threading.Thread(target=handleClient,args=(conn,addr)),
			threading.Thread(target=print,args=(f'Clients: {threading.active_count() - 1}\n',))
		]
		for i in th: i.start()
		for i in th: i.join()

getClients()