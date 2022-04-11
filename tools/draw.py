import pygame
import numpy as np

def transiction(size, limit, spd=5, typ='fade', col=(0,0,0)):
	lst = []
	if limit < 1: limit = 1
	trs = int(100/limit)
	sq = [(x,y) for x in range(10) for y in range(10)]
	sd = None
	while trs != limit:
		srf = pygame.Surface(size,pygame.SRCALPHA)
		if typ == 'fade':
			srf.fill((col[0],col[1],col[2],trs * (250/100)))
		elif typ == 'bars':
			pygame.draw.rect(srf,col,pygame.Rect(0,0,size[0],int(trs * ((size[1]/2)/100))))
			pygame.draw.rect(srf,col,pygame.Rect(0,size[1] - int(trs * ((size[1]/2)/100)),size[0],int(trs * ((size[1]/2)/100))))
		elif typ.startswith('side'):
			if typ.endswith('top'): pygame.draw.rect(srf,col,pygame.Rect(0,0,size[0],int(trs * (size[1]/100))))
			if typ.endswith('left'): pygame.draw.rect(srf,col,pygame.Rect(0,0,int(trs * (size[0]/100)),size[1]))
			if typ.endswith('bottom'): pygame.draw.rect(srf,col,pygame.Rect(0,size[1] - int(trs * (size[1]/100)),size[0],int(trs * (size[1]/100))))
			if typ.endswith('right'): pygame.draw.rect(srf,col,pygame.Rect(size[0] - int(trs * (size[0]/100)),0,int(trs * (size[0]/100)),size[1]))
		elif typ in ['hole','aim']:
			srf.fill(col)
			c = pygame.Surface((int(trs * (size[0]/80)),int(trs * (size[0]/80))),pygame.SRCALPHA)
			pygame.draw.ellipse(c,(200,0,0),pygame.Rect(0,0,c.get_width(),c.get_height()))
			srf.blit(c,(int(size[0]/2) - int(c.get_width()/2),int(size[1]/2) - int(c.get_height()/2)),None,pygame.BLEND_RGBA_SUB)
			if typ == 'aim':
				pygame.draw.line(srf,col,(int(size[0]/2),int(size[1]/2) + int(c.get_height()/2)),(int(size[0]/2),int(size[1]/2) - int(c.get_height()/2)),5)
				pygame.draw.line(srf,col,(int(size[0]/2) + int(c.get_width()/2),int(size[1]/2)),(int(size[0]/2) - int(c.get_width()/2),int(size[1]/2)),5)
		elif typ == 'cover':
			for y in range(int(size[0]/10)):
				for x in range(int(size[1]/10)):
					if x + (y * 10) < trs: pygame.draw.rect(srf,col,pygame.Rect(x * int(size[0]/10),y * int(size[1]/10),int(size[0]/10),int(size[1]/10)))
		elif typ == 'squares':
			prb = np.random.randint(0,len(sq)-1)
			if sd: srf = sd.copy()
			pygame.draw.rect(srf,col,pygame.Rect(sq[prb][0] * int(size[0]/10),sq[prb][1] * int(size[1]/10),int(size[0]/10),int(size[1]/10)))
			sd = srf.copy()
			del sq[prb]
		lst.append(srf)
		trs += int(100/spd)
	lst.append(None)
	'''
	if type == 'zoom':
		if fade == False:
			acc = 1
			while True:
				self.displayzw += dw * acc
				self.displayzh += dh * acc
				self.cam.x += int(acc * (dw/2))
				self.cam.y += int(acc * (dh/2))
				self.cam.width = self.displayzw
				self.cam.height = self.displayzh
				if self.displayzw < dw * limit:
					self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
				else:
					self.displayzw = dw * limit
					self.displayzh = dh * limit
					self.cam.width = dw * limit
					self.cam.height = dh * limit
					self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					break
				self.run(False)
				acc += 1
		else:
			acc = 1
			while True:
				self.displayzw -= dw * acc
				self.displayzh -= dh * acc
				self.cam.x += int(acc * (dw/2))
				self.cam.y += int(acc * (dh/2))
				self.cam.width = self.displayzw
				self.cam.height = self.displayzh
				if self.displayzw > dw * limit:
					self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
				else:
					self.displayzw = dw * limit
					self.displayzh = dh * limit
					self.cam.width = dw * limit
					self.cam.height = dh * limit
					self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					break
				self.run(False)
				acc += 1'''
	return lst

def noise_img(mean, std, size):
	return pygame.surfarray.make_surface(np.random.normal(mean,std,size))

def gradient(size,top,bottom,value=0,direction='vertical'):
	srf = pygame.Surface(size,pygame.SRCALPHA)
	srf.fill(top)
	if direction == 'vertical':
		if value == 0: number = size[1]; dv = 1
		else: number = value; dv = int(size[0]/value)
		line = (size[0],dv)
	else:
		if value == 0: number = size[1]; dv = 1
		else: number = value; dv = int(size[1]/value)
		line = (dv,size[0])
	for i in range(number):
		ln = pygame.Surface(line,pygame.SRCALPHA)
		ln.fill(tuple([abs(np.floor((top[x] + bottom[x])/(number/(i + 1))) - bottom[x]) for x in range(3)]))
		if direction == 'vertical': srf.blit(ln,(0,i * dv))
		else: srf.blit(ln,(i * dv,0))
	return srf

def get_tiles(self):
	tlsz = (30,30)
	tilset = os.listdir(res.TILES_PATH)
	tilset.remove('files')
	tilset.sort()
	srf = pygame.Surface(tlsz)
	srf.fill((0,0,0))
	tls = [srf]
	for t in tilset:
		tst = pygame.image.load(res.TILES_PATH + t)
		for y in range(int(tst.get_height()/tlsz[1])):
			for x in range(int(tst.get_width()/tlsz[0])):
				rct = pygame.Rect(x * tlsz[0],y * tlsz[1],tlsz[0],tlsz[1])
				tls.append(tst.subsurface(rct).copy())
	return tls