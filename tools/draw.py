import pygame
import numpy as np

def bar(vl,sz,col1,col2,type='regular',stacksize=10,stackspacing=2):
	srf = pygame.Surface(sz,pygame.SRCALPHA)
	srf.fill(col1)
	if vl[0] > 0:
		if isinstance(type,int):
			type = ('regular','levels','stack')[type]

		if type in ('regular','levels'):
			if sz[0] > sz[1]: rct = pygame.Rect(0,0,int(sz[0]/(vl[1]/vl[0])),sz[1]) #HORIZONTAL BAR
			else: rct = pygame.Rect(0,sz[1] - int(sz[1]/(vl[1]/vl[0])),sz[0],int(sz[1]/(vl[1]/vl[0]))) #VERTICAL BAR
			pygame.draw.rect(srf,col2,rct)
			szadd = 0
			shdrng = 6
			for r in range(shdrng):
				col = [col2[0] - int((40 * shdrng)/(r + 1)),col2[1] - int((40 * shdrng)/(r + 1)),col2[2] - int((40 * shdrng)/(r + 1))]
				for i in range(len(col)):
					if col[i] < 0: col[i] = 0
				brsz = int(((rct.height/5)/shdrng) * (r + 1))
				if sz[0] > sz[1]:pygame.draw.rect(srf,tuple(col),pygame.Rect(0,szadd,rct.width,brsz))
				pygame.draw.rect(srf,tuple(col),pygame.Rect(0,sz[1] - brsz - szadd,rct.width,brsz))
				szadd += brsz

		if type == 'stack':
			for i in range(stacksize):
				if float(vl[0]/(vl[1]/stacksize)) >= i + 1:
					if sz[0] > sz[1]:
						stsz = int(sz[1]/(stacksize - 1))
						rct = pygame.Rect(stackspacing + (i * (stsz + stackspacing)),stackspacing,stsz,sz[1] - (stackspacing * 2)) #HORIZONTAL BAR
					else:
						stsz = int(sz[0]/(stacksize - 1))
						rct = pygame.Rect(stackspacing,sz[1] - ((i + 1) * (stsz + stackspacing)),sz[0] - (stackspacing * 2),stsz) #VERTICAL BAR
					pygame.draw.rect(srf,col2,rct)

	if type == 'levels':
		lvls = 3
		for i in range(lvls):
			if sz[0] > sz[1]: rct = pygame.Rect(int((sz[0]/lvls)/2) + (int(sz[0]/lvls) * i),0,2,sz[1]) #HORIZONTAL BAR
			else: rct = pygame.Rect(0,int((sz[1]/lvls)/2) + (int(sz[1]/lvls) * i),sz[0],2) #VERTICAL BAR
			pygame.draw.rect(srf,(200,200,200),rct)

	return srf

def transiction(size, limit, speed=5, type='fade', col=(0,0,0)):
	lst = []
	if limit < 1: limit = 1
	trs = int(100/limit)
	sq = [(x,y) for x in range(10) for y in range(10)]
	sd = None
	while abs(trs) != limit:
		srf = pygame.Surface(size,pygame.SRCALPHA)
		if type == 'fade':
			#print((col[0],col[1],col[2],int(250 * (trs/100))))
			srf.fill((col[0],col[1],col[2],int(250 * (trs/100))))
		elif type == 'bars':
			pygame.draw.rect(srf,col,pygame.Rect(0,0,size[0],int(trs * ((size[1]/2)/100))))
			pygame.draw.rect(srf,col,pygame.Rect(0,size[1] - int(trs * ((size[1]/2)/100)),size[0],int(trs * ((size[1]/2)/100))))
		elif type.startswith('side'):
			if type.endswith('top'): pygame.draw.rect(srf,col,pygame.Rect(0,0,size[0],int(trs * (size[1]/100))))
			if type.endswith('left'): pygame.draw.rect(srf,col,pygame.Rect(0,0,int(trs * (size[0]/100)),size[1]))
			if type.endswith('bottom'): pygame.draw.rect(srf,col,pygame.Rect(0,size[1] - int(trs * (size[1]/100)),size[0],int(trs * (size[1]/100))))
			if type.endswith('right'): pygame.draw.rect(srf,col,pygame.Rect(size[0] - int(trs * (size[0]/100)),0,int(trs * (size[0]/100)),size[1]))
		elif type in ['hole','aim']:
			srf.fill(col)
			c = pygame.Surface((int(trs * (size[0]/80)),int(trs * (size[0]/80))),pygame.SRCALPHA)
			pygame.draw.ellipse(c,(200,0,0),pygame.Rect(0,0,c.get_width(),c.get_height()))
			srf.blit(c,(int(size[0]/2) - int(c.get_width()/2),int(size[1]/2) - int(c.get_height()/2)),None,pygame.BLEND_RGBA_SUB)
			if type == 'aim':
				pygame.draw.line(srf,col,(int(size[0]/2),int(size[1]/2) + int(c.get_height()/2)),(int(size[0]/2),int(size[1]/2) - int(c.get_height()/2)),5)
				pygame.draw.line(srf,col,(int(size[0]/2) + int(c.get_width()/2),int(size[1]/2)),(int(size[0]/2) - int(c.get_width()/2),int(size[1]/2)),5)
		elif type == 'cover':
			for y in range(int(size[0]/10)):
				for x in range(int(size[1]/10)):
					if x + (y * 10) < trs: pygame.draw.rect(srf,col,pygame.Rect(x * int(size[0]/10),y * int(size[1]/10),int(size[0]/10),int(size[1]/10)))
		elif type == 'squares':
			prb = np.random.randint(0,len(sq)-1)
			if sd: srf = sd.copy()
			pygame.draw.rect(srf,col,pygame.Rect(sq[prb][0] * int(size[0]/10),sq[prb][1] * int(size[1]/10),int(size[0]/10),int(size[1]/10)))
			sd = srf.copy()
			del sq[prb]
		lst.append(srf)
		trs += int(100/speed)
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