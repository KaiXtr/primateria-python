from PIL import Image
import numpy as np

def texture(file):
	img = Image.open(file)
	pa = [(0,0),(img.size[0],0),img.size,(0,img.size[1])]
	pb = [(0,0),(img.size[0],-200),(img.size[0],img.size[1] + 200),(0,img.size[1])]
	m = []
	for p1, p2 in zip(pa,pb):
		m.append([p1[0],p1[1],1,0,0,0,-p2[0] * p1[0],-p2[0] * p1[1]])
		m.append([0,0,0,p1[0],p1[1],1,-p2[1] * p1[0],-p2[1] * p1[1]])
	A = np.matrix(m, dtype=float)
	B = np.array(pb).reshape(8)
	coffs = np.array(np.dot(np.linalg.inv(A.T * A) * A.T, B)).reshape(8)
	return img.transform(img.size,Image.PERSPECTIVE,coffs,Image.BICUBIC)
	
img = texture()
img.show()