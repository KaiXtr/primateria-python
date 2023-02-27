import threading
import socket
import secret

BYTES = 256
PORT = 5050
SERVER = secret.SERVER
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def sendMessage(txt):
	msg = txt.encode(FORMAT)
	msg_lenght = len(msg)
	send_lenght = str(msg_lenght).encode(FORMAT)
	send_lenght += b' ' * (BYTES - len(send_lenght))
	client.send(send_lenght)
	client.send(msg)

def receiveMessage():
	msg = client.recv(BYTES).decode(FORMAT)
	txt = ''
	for i in [x for x in msg]:
		if i == '@':
			print(txt)
			txt = ''
		txt += i

txt = ''
msg = client.recv(BYTES)
try:
	while txt != '!disconnect':
		txt = input('> ')
		#conn, addr = client.accept()
		th = [
			threading.Thread(target=receiveMessage,args=()),
			threading.Thread(target=sendMessage,args=(txt,)),
		]
		for i in th: i.start()
		for i in th: i.join()
except: print('Server is disconnected.')