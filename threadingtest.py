import threading
import time

def x(v):
	for i in range(100):
		time.sleep(v)
		print(i)

th = [
	threading.Thread(target=x,args=(0.1,)),
	threading.Thread(target=x,args=(0.2,))
]
for i in th: i.start()
for i in th: i.join()