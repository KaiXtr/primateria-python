import sys
import pygame
#from pygame.locals import *
import plyer
import queue
from queue import LifoQueue
import numpy as np
import os

import tools
import resources as res

if res.FILES != []: exec(f'import databases.database_{res.FILES[0][4]} as dtb')
else: exec(f'import databases.database_{res.MAINLANG} as dtb')

pygame.init()

class Game:
	def __init__(self):
		res.fonts()
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		pygame.mixer.music = pygame.mixer.Channel(1)
		pygame.mixer.music.set_volume(res.MSC)
		for i in range(4):
			res.MIXER.append(pygame.mixer.Channel(i))
			res.MIXER[i].set_volume(res.SFX)
		self.display = pygame.display.set_mode((600, 600),pygame.RESIZABLE | pygame.SRCALPHA)
		self.font = pygame.font.SysFont("Arial", 30)
		self.clock = pygame.time.Clock()
		self.minigame = Snake()
		self.bkg = tools.draw.gradient((800,1280),(100,100,200),(200,100,100))
		pygame.event.set_allowed([pygame.QUIT,pygame.VIDEORESIZE,pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.KEYDOWN,pygame.KEYUP])

		self.mglstg = [[],
			['Pinball','Tetris','Minesweeper','Pong','Differences','Jigsaw','Maze','Pool','Snake','HittheMole','FallingItems','Jumping','FlappyBird','Breakout','BubbleBubble','CannonBattle','ColorMatch','MusicTiles','Footrace','Hops'],
			['Twothousandforthyeight','Memory','Simon','FindtheCup','ImageMatch','Cassino','Roulette','NumberPuzzle','Piano'],
			['Chess','Checkers','Trilha','Blackgammon','Ludo','Reversi','SnakesNLadders'],
			['Solitaire','SpiderSolitaire','Freecell','Mahjong','PegSolitaire'],
			['Dominoes','Truco','Sueca','Cacheta','Pife','Buraco','Poker','Copas','Espadas','Maumau'],
			['Matchingwords','TicTacToe','LinesNBoxes','Nonogram','HuntingWords','Sudoku','Hangman','Yatzy','Stop']
			]
		for i in self.mglstg[1:]: self.mglstg[0] += i
		for i in self.mglstg: i.sort()
		self.bgames = []
		self.bbtt = pygame.Rect(0,0,40,40)
		self.cbts = []
		self.mn = 0
		for i in range(len(self.mglstg)):
			self.bgames.append([])
			self.cbts.append(pygame.Rect(i * int(self.display.get_width()/len(self.mglstg)),0,int(self.display.get_width()/len(self.mglstg)),40))
			for y in range(np.floor(len(self.mglstg[i])/3).astype(int)):
				for x in range(3):
					self.bgames[i].append(pygame.Rect(10 + (x * int((self.display.get_width() - 10)/3)), 50 + (y * 60), int((self.display.get_width() - 10)/3) - 10, 50))
			if len(self.bgames[i]) < len(self.mglstg[i]):
				for x in range(len(self.mglstg[i]) - len(self.bgames[i])): self.bgames[i].append(pygame.Rect(10 + (x * int((self.display.get_width() - 10)/3)), 50 + ((y + 1) * 60), int((self.display.get_width() - 10)/3) - 10, 50))
			
	def run(self):
		#EVENTS
		for event in pygame.event.get():
			pressed, mouse = tools.event.get_pressed(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				exit()
			if event.type == pygame.VIDEORESIZE:
				self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.SRCALPHA)
				self.bkg = tools.draw.gradient((event.w,event.h),(100,100,200),(200,100,100))
			#IN MINIGAME
			if self.minigame:
				self.minigame.inside_events(pressed,mouse)
				if pressed[4][0] and pygame.Rect.colliderect(mouse,self.bbtt):
					self.minigame = None
			#MAIN MENU
			else:
				if pressed[4][0]:
					for i in range(len(self.cbts)):
						if pygame.Rect.colliderect(mouse,self.cbts[i]):
							self.mn = i
					for i in range(len(self.bgames[self.mn])):
						if pygame.Rect.colliderect(mouse,self.bgames[self.mn][i]):
							self.minigame = eval(self.mglstg[self.mn][i])()
		#DISPLAY STUFF
		self.display.fill((100,100,100))
		self.display.blit(self.bkg,(0,0))
		#IN MINIGAME
		if self.minigame:
			self.display.blit(self.minigame.draw(),(0,0))
			pygame.draw.rect(self.display,(200,10,10),self.bbtt)
		#MAIN MENU
		else:
			for i in range(len(self.cbts)):
				if i == self.mn: cc = (100,100,200)
				else: cc = (250,250,250)
				pygame.draw.rect(self.display,cc,self.cbts[i])
			for i in range(len(self.bgames[self.mn])):
				pygame.draw.rect(self.display,(250,250,250),self.bgames[self.mn][i])
				self.display.blit(self.font.render(dtb.MINIGAMES[self.mglstg[self.mn][i]],1,(10,10,10)),(self.bgames[self.mn][i].x + 5,self.bgames[self.mn][i].y + 5))
		
		pygame.display.flip()
		self.clock.tick(res.FPS)

class Template:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(30):
			self.grid.append([])
			for x in range(10):
				self.grid[y].append([pygame.Rect(10 + (x * 22), 50 + (y * 22), 20, 20), None, 0])
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.grid:
				if pygame.Rect.colliderect(mouse,i[0]):
					pass
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(self.txt,1,(200,200,200)), (10,10))
		
		return self.surface

class Piano:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = [pygame.Rect(10 + (x * 22), 220, 20, 50) for x in range(12)]
		self.wave = None
		
	def inside_events(self,pressed,mouse):
		tune = [262,278,294,311,330,349,370,392,415,440,466,494]
		if pressed[4][0]:
			for i in range(len(self.grid)):
				if pygame.Rect.colliderect(mouse,self.grid[i]):
					self.wave = tools.mixer.sound_wave('square',f=tune[i],length=0.2)
					res.MIXER[0].play(self.wave)
		else:
			for i in range(8):
				if pressed[i][0]:
					self.wave = tools.mixer.sound_wave('sine',f=tune[i],length=0.2)
					res.MIXER[0].play(self.wave)
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.wave: self.surface.blit(tools.mixer.audio_display(self.wave,zoomt=1),(0,0))
		for i in range(len(self.grid)):
			if i in [1,3,6,8,10]: col = (50,50,50)
			else: col = (200,200,200)
			pygame.draw.rect(self.surface,col,self.grid[i])
		
		return self.surface

class Footrace:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 40)
		self.buttons = []
		for x in range(2): self.buttons.append(pygame.Rect(10 + (x * 50), 300, 40, 40))
		self.switch = False
		self.dist = 0
		self.speed = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in range(len(self.buttons)):
				if pygame.Rect.colliderect(mouse,self.buttons[i]):
					if i == int(self.switch):
						self.speed += 0.2
						self.switch = not self.switch
						self.dist += self.speed
		elif pressed[2][0] and self.switch == False: self.speed += 1; self.switch = True; self.dist += self.speed
		elif pressed[3][0] and self.switch == True: self.speed += 1; self.switch = False; self.dist += self.speed
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(str(int(self.dist)) + 'm',1,(200,200,200)), (10,10))
		self.surface.blit(self.font.render(str(int(self.speed/10)) + 'km/h',1,(200,200,200)), (10,50))
		if self.speed > 0: self.speed -= 0.1
		dd = self.dist - (int(self.dist/50) * 50)
		for i in range(20): pygame.draw.line(self.surface, (200,200,200), ((i * 50)-dd,200),((i * 50)-dd,220),3)
		for i in self.buttons: pygame.draw.rect(self.surface,(200,200,200),i)
		
		return self.surface

class Hops:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.jump = 0
		self.grvt = -5
		self.score = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.grvt == -5:
			self.grvt = 5
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		if self.grvt > -5:
			self.grvt -= 0.2
			self.jump += self.grvt
		pygame.draw.ellipse(self.surface,(200,100,100),pygame.Rect(100,100 - int(self.jump),30,30))
		
		return self.surface

#ARCADE GAMING
class Pinball:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.ball = {'X': 200,'Y': 200, 'XSPEED': 0, 'YSPEED': 5}
		self.bumpers = [[50,200],[100,300],[100,400]]
		self.tables = [pygame.image.load(res.SPRITES_PATH + 'minigames/tablemask.png')]
	
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			self.ball['XSPEED'] += 2
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		self.ball['X'] += self.ball['XSPEED']
		self.ball['Y'] += self.ball['YSPEED']
		self.ball['YSPEED'] += 0.5
		
		#BALL PHYSICS
		if self.ball['X'] <= 0 or self.ball['X'] >= self.surface.get_width():
			#self.ball['X'] += -self.ball['X'] cool teleport
			if self.ball['X'] <= 0: self.ball['X'] += -self.ball['X']
			if self.ball['X'] >= self.surface.get_width(): self.ball['X'] -= (self.ball['X'] - self.surface.get_width())
			self.ball['XSPEED'] = -(self.ball['XSPEED'] * 0.8)
		if self.ball['Y'] <= 0 or self.ball['Y'] >= int(self.surface.get_height() * 0.5):
			if self.ball['Y'] <= 0: self.ball['Y'] += -self.ball['Y']
			if self.ball['Y'] >= int(self.surface.get_height() * 0.5): self.ball['Y'] -= (self.ball['Y'] - int(self.surface.get_height() * 0.5))
			if self.ball['YSPEED'] > 0: self.ball['YSPEED'] = -(self.ball['YSPEED'] - 2)
			else: self.ball['YSPEED'] = 0
		#MASK COLLISION
		msk = pygame.mask.from_surface(self.tables[0])
		bll = pygame.mask.from_surface(pygame.image.load(res.SPRITES_PATH + 'minigames/ballmask.png'))
		if msk.overlap(bll, (int(self.ball['X']), int(self.ball['Y']))):
			self.ball['XSPEED'] = -(self.ball['XSPEED'] * 0.8)
			self.ball['YSPEED'] = -(self.ball['YSPEED'] - 2)
		if np.floor(self.ball['YSPEED']) == 0 and np.floor(self.ball['XSPEED'] > 0): self.ball['XSPEED'] -= 0.1

		#DRAW
		self.surface.blit(self.tables[0], (0,0))
		for i in self.bumpers:
			rct = pygame.Rect(i[0],i[1],30,30)
			pygame.draw.ellipse(self.surface,(0,200,0),rct)
			if pygame.Rect.colliderect(pygame.Rect(self.ball['X'],self.ball['Y'],30,30),rct):
				self.ball['XSPEED'] = -(self.ball['XSPEED'] * 1.5)
				self.ball['YSPEED'] = -(self.ball['YSPEED'] * 1.5)
		pygame.draw.ellipse(self.surface, (200,0,0), (int(self.ball['X']),int(self.ball['Y']),30,30))
		pygame.draw.line(self.surface,(200,200,200),(0,int(self.surface.get_height() * 0.5)),(self.surface.get_width(),int(self.surface.get_height() * 0.5)),5)
		
		return self.surface

class Tetris:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		self.spn = 0
		for x in range(10):
			for y in range(20):
				self.grid.append([x,y])
		self.pieces = [[0,0,np.random.randint(0,7)]]
		self.bricks = [
			[[0,0],[1,0],[2,0],[3,0]],
			[[0,0],[0,1],[1,1],[2,1]],
			[[0,1],[1,1],[2,1],[2,0]],
			[[0,0],[1,0],[0,1],[1,1]],
			[[0,1],[1,1],[1,0],[2,0]],
			[[0,0],[1,0],[1,1],[2,1]],
			[[0,1],[1,1],[1,0],[2,1]],
		]
		self.endy = 0
		self.spd = 20
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w: self.spn += 1
			if event.key == pygame.K_a: self.pieces[0][0] -= 1
			if event.key == pygame.K_s: self.pieces[0][1] += 1
			if event.key == pygame.K_d: self.pieces[0][0] += 1
			if self.spn > 3: self.spn = 0
			self.endy = 20
			for i in self.pieces[1:]:
				for j in [[b[0] + i[0],b[1] + i[1]] for b in self.bricks[i[2]]]:
					if j[0] == self.pieces[0][0] and self.endy > j[1]: self.endy = j[1] - 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))

		if self.spd > 0: self.spd -= 1
		else:
			ck = [[b[0] + self.pieces[0][0],b[1] + self.pieces[0][1]] for b in self.bricks[self.pieces[0][2]]]
			if 19 in ck or self.endy in ck:
				self.pieces.insert(0,[0,0,np.random.randint(0,7)])
			else: self.pieces[0][1] += 1
			self.spd = 30

		for i in self.grid:
			pygame.draw.rect(self.surface,(100,100,100),pygame.Rect(100 + (20 * i[0]),100 + (20 * i[1]),19,19))
			for p in self.pieces:
				if self.spn == 0: lst = [[p[0] + b[0],p[1] + b[1]] for b in self.bricks[p[2]]]
				if self.spn == 1: lst = [[p[0] + b[1],p[1] + b[0]] for b in self.bricks[p[2]]]
				if self.spn == 2: lst = [[p[0] + b[0],p[1] - b[1]] for b in self.bricks[p[2]]]
				if self.spn == 3: lst = [[p[0] - b[1],p[1] + b[0]] for b in self.bricks[p[2]]]
				if i[0:2] in lst:
					if p[2] == 0: cc = (200,100,100)
					if p[2] == 1: cc = (200,150,100)
					if p[2] == 2: cc = (200,200,100)
					if p[2] == 3: cc = (100,200,100)
					if p[2] == 4: cc = (100,200,200)
					if p[2] == 5: cc = (100,100,200)
					if p[2] == 6: cc = (200,100,200)
					pygame.draw.rect(self.surface,cc,pygame.Rect(100 + (20 * i[0]),100 + (20 * i[1]),19,19))
		
		return self.surface

class Minesweeper:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.num = pygame.font.SysFont("Arial", 15)
		self.grid = []
		self.flgs = 30
		for y in range(30):
			self.grid.append([])
			for x in range(10):
				self.grid[y].append([pygame.Rect(10 + (x * 22), 50 + (y * 22), 20, 20), None, 0])
		self.mines = 0
		while self.mines < self.flgs:
			mx = np.random.randint(0,10)
			my = np.random.randint(0,30)
			if self.grid[my][mx][1] == None:
				self.grid[my][mx][1] = 'X'
				self.mines += 1
				rngx = [mx - 1, mx, mx + 1]
				if mx == 0: rngx[0] = None
				if mx == 9: rngx[2] = None
				rngy = [my - 1, my, my + 1]
				if my == 0: rngy[0] = None
				if my == 29: rngy[2] = None
				if None in rngx: rngx.remove(None)
				if None in rngy: rngy.remove(None)
				for y in rngy:
					for x in rngx:
						if x != mx or y != my:
							if self.grid[y][x][1] == None: self.grid[y][x][1] = 1
							elif self.grid[y][x][1] != 'X': self.grid[y][x][1] += 1
		self.gend = False

	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.gend == False:
				cy = 0
				for y in self.grid:
					cx = 0
					for x in y:
						if pygame.Rect.colliderect(mouse,x[0]):
							if pygame.mouse.get_pressed()[0]:
								x[2] = 1
								if x[1] == 'X': self.gend = True
								elif x[1] == None:
									rd = 0
									while rd < 30:
										for cc in range(cy - rd,cy + rd):
											for rr in range(cx - rd,cx + rd):
												try:
													if self.grid[cc][rr][1] != None: break
													else: self.grid[cc][rr][2] = 1
												except: pass
										rd += 1
							elif pygame.mouse.get_pressed()[2]:
								if x[2] == 2: x[2] = 0; self.flgs += 1
								elif x[2] == 0: x[2] = 2; self.flgs -= 1
								if self.flgs == 0:
									chk = 0
									for chky in self.grid:
										for chkx in chky:
											if chkx[1] == 'X' and chkx[2] == 2: chk += 1
									if chk == 30: self.gend = True
						cx += 1
					cy += 1
			else: self.__init__()
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(str(self.flgs),1,(200,200,200)), (10,10))
		for y in self.grid:
			for x in y:
				if x[2] == 1:
					pygame.draw.rect(self.surface,(200,200,200),x[0])
					if isinstance(x[1],int): self.surface.blit(self.num.render(str(x[1]),1,(10,10,10)), (x[0].x,x[0].y))
				elif x[2] == 2: pygame.draw.rect(self.surface,(100,200,100),x[0])
				else: pygame.draw.rect(self.surface,(100,100,100),x[0])
				if x[2] == 1 or self.gend:
					if x[1] == 'X': pygame.draw.rect(self.surface,(200,0,0),x[0])
				
		return self.surface

class Pong:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.goals = [pygame.Rect(200,200,100,20),pygame.Rect(200,1000,100,20)]
		self.ball = {'X': 100,'Y': int(self.surface.get_height()/2), 'XSPEED': 0, 'YSPEED': 0}
		self.font = pygame.font.SysFont("Arial", 64)
		self.score = [0,0]
	
	def inside_events(self,pressed,mouse):
		mp = pygame.mouse.get_pos()
		if mp[1] < int(self.surface.get_height()/2): self.goals[0].x = mp[0]
		if mp[1] > int(self.surface.get_height()/2): self.goals[1].x = mp[0]
		if pressed[4][0] and self.ball['XSPEED'] == 0 and self.ball['YSPEED'] == 0:
			self.ball['YSPEED'] = 5
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.ball['X'] += self.ball['XSPEED']
		self.ball['Y'] += self.ball['YSPEED']
		for r in self.goals:
			if pygame.Rect.colliderect(pygame.Rect(self.ball['X'],self.ball['Y'],30,30),r):
				if self.ball['X'] < r.x + 50: self.ball['XSPEED'] = -5
				if self.ball['X'] > r.x + 50: self.ball['XSPEED'] = 5
				self.ball['YSPEED'] = -(self.ball['YSPEED'] * 1.2)
		if self.ball['X'] <= 0 or self.ball['X'] >= self.surface.get_width():
			if self.ball['X'] <= 0: self.ball['X'] += -self.ball['X']
			if self.ball['X'] >= self.surface.get_width(): self.ball['X'] -= (self.ball['X'] - self.surface.get_width())
			self.ball['XSPEED'] = -(self.ball['XSPEED'] * 1.2)
		if self.ball['Y'] <= 0:
			self.score[1] += 1
			self.ball = {'X': 100,'Y': int(self.surface.get_height()/2), 'XSPEED': 0, 'YSPEED': 0}
		if self.ball['Y'] >= self.surface.get_height():
			self.score[0] += 1
			self.ball = {'X': 100,'Y': int(self.surface.get_height()/2), 'XSPEED': 0, 'YSPEED': 0}
		pygame.draw.line(self.surface,(200,200,200),(0,int(self.surface.get_height()/2)),(self.surface.get_width(),int(self.surface.get_height()/2)),5)
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
		pygame.draw.ellipse(self.surface, (200,200,200), pygame.Rect(self.ball['X'],self.ball['Y'],30,30))
		for r in self.goals: pygame.draw.rect(self.surface,(0,200,0), r)
		
		return self.surface

class Differences:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.imgs = [pygame.image.load('diff1.png'),pygame.image.load('diff2.png')]
		self.errs = [[pygame.Rect(470,780,30,30),0],[pygame.Rect(440,800,30,30),0],[pygame.Rect(420,600,100,100),0],[pygame.Rect(110,610,50,50),0],
		[pygame.Rect(260,670,60,60),0],[pygame.Rect(120,940,50,50),0],[pygame.Rect(480,920,30,30),0],[pygame.Rect(500,840,30,30),0]]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if len([i for i in self.errs if i[1] == 1]) == len(self.errs): self.__init__()
			for i in self.errs:
				altrct = pygame.Rect(i[0].x,i[0].y - 500,i[0].width,i[0].height)
				if pygame.Rect.colliderect(mouse,i[0]) or pygame.Rect.colliderect(mouse,altrct):
					i[1] = 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.imgs[0], (100,100))
		self.surface.blit(self.imgs[1], (100,600))
		for i in self.errs:
			if i[1] == 1:
				pygame.draw.rect(self.surface,(200,100,100),pygame.Rect(i[0].x,i[0].y - 500,i[0].width,i[0].height),5)
				pygame.draw.rect(self.surface,(200,100,100),i[0],5)
		
		return self.surface

class Jigsaw:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.img = pygame.image.load('diff1.png')
		self.pieces = []
		self.table = []
		self.drgdrp = None
		self.size = 40
		for y in range(int(self.img.get_height()/self.size)):
			for x in range(int(self.img.get_width()/self.size)):
				self.pieces.append([self.img.subsurface(pygame.Rect(x * self.size, y * self.size, self.size, self.size)),pygame.Rect(100 + (x * (self.size + 1)), 100 + (y * (self.size + 1)), self.size, self.size)])
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.MOUSEBUTTONUP and self.drgdrp != None:
			self.table[self.drgdrp][1].x = np.floor(mr.x/self.size) * self.size
			self.table[self.drgdrp][1].y = np.floor(mr.y/self.size) * self.size
			self.drgdrp = None
		if pressed[4][0]:
			if len(self.pieces) > 0:
				self.table.append(self.pieces[-1])
				self.table[-1][1].x = np.floor(mr.x/self.size) * self.size
				self.table[-1][1].y = np.floor(mr.y/self.size) * self.size
				del self.pieces[-1]
			for i in range(len(self.table)):
				if pygame.Rect.colliderect(mouse,self.table[i][1]):
					self.drgdrp = i
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for i in range(len(self.table)):
			if i != self.drgdrp: self.surface.blit(self.table[i][0],(self.table[i][1].x,self.table[i][1].y))
		if self.drgdrp != None:
			mp = pygame.mouse.get_pos()
			self.surface.blit(self.table[self.drgdrp][0],(mp[0],mp[1]))
		
		return self.surface

class Maze:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.generate(100,100)

	def generate(self,width,height):
		self.mz = pygame.Surface((2*width + 1, 2*height + 1))
		pixels = [(0,0,0) for x in range(2 * width + 1) for y in range(2 * height + 1)]

		pixels[1, 0] = (255, 255, 255)
		pixels[-2, -1] = (255, 255, 255)

		stack = []
		cells = np.zeros((width, height))
		cells[0, 0] = 1
		stack.append((0, 0))

		while len(stack) > 0:
			x, y = stack[-1]

			adjacents = []
			if x > 0 and cells[x - 1, y] == 0: adjacents.append((x - 1, y))
			if x < width - 1 and cells[x + 1, y] == 0: adjacents.append((x + 1, y))
			if y > 0 and cells[x, y - 1] == 0: adjacents.append((x, y - 1))
			if y < height - 1 and cells[x, y + 1] == 0: adjacents.append((x, y + 1))

			if adjacents:
				stack.append((x, y))
				neighbour = random.choice(adjacents)
				neighbour_on_img = (neighbour[0]*2 + 1, neighbour[1]*2 + 1)
				current_on_img = (x*2 + 1, y*2 + 1)
				wall_to_remove = (neighbour[0] + x + 1, neighbour[1] + y + 1)

				pixels[neighbour_on_img] = (255, 255, 255)
				pixels[current_on_img] = (255, 255, 255)
				pixels[wall_to_remove] = (255, 255, 255)

				cells[neighbour] = 1
				stack.append(neighbour)
			del stack[0]
		p = 0
		for y in range(2 * width + 1):
			for x in range(2 * height + 1):
				pygame.draw.rect(self.mz,pixels[p],pygame.Rect(x,y,2,2))
				p += 1
		
	def inside_events(self,pressed,mouse):
		pass
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))

		self.surface.blit(self.mz,(50,50))
		
		return self.surface

class Snake:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.size = (60,60)
		self.map = (int(self.surface.get_width()/self.size[0]),int(self.surface.get_height()/self.size[1]))
		self.pos = [[2,4],[2,3],[2,2]]
		for i in range(len(self.pos)):
			for s in range(2): self.pos[i][s] *= self.size[s]
		self.dir = 3
		self.spd = 20
		self.fd = [np.random.randint(0,self.map[0]) * self.size[0],np.random.randint(0,self.map[1]) * self.size[1]]
		self.imgs = {str(i) + '_' + str(d): pygame.image.load(res.SPRITES_PATH + 'head_' + str(i) + '_0.png') for i in range(2) for d in range(4)}
		self.bkg = []
		for i in range(1):
			c = False
			srf = pygame.Surface((self.surface.get_width(),self.surface.get_height()))
			for y in range(self.map[1]):
				for x in range(self.map[0]):
					if c: cl = (10,200,10)
					else: cl = (10,180,10)
					pygame.draw.rect(srf,cl,pygame.Rect(x * self.size[0],y * self.size[1],self.size[0],self.size[1]))
					c = not c
				c = not c
			self.bkg.append(srf)
		
	def inside_events(self,pressed,mouse):
		if pressed[2][0] and self.dir != 2: self.dir = 0
		if pressed[0][0] and self.dir != 3: self.dir = 1
		if pressed[3][0] and self.dir != 0: self.dir = 2
		if pressed[1][0] and self.dir != 1: self.dir = 3
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.bkg[0],(0,0))

		if self.spd > 0: self.spd -= 1
		else:
			del self.pos[-1]
			self.pos.insert(0,self.pos[0].copy())
			if self.dir == 0: self.pos[0][0] -= 1 * self.size[0]
			if self.dir == 1: self.pos[0][1] -= 1 * self.size[1]
			if self.dir == 2: self.pos[0][0] += 1 * self.size[0]
			if self.dir == 3: self.pos[0][1] += 1 * self.size[1]
			self.spd = 20 - np.floor(len(self.pos)/2)
			if self.spd < 1: self.spd = 1
			if self.pos[0] == self.fd:
				self.fd = [np.random.randint(0,self.map[0]) * self.size[0],np.random.randint(0,self.map[1]) * self.size[1]]
				while self.fd in self.pos: self.fd = [np.random.randint(0,self.map[0]) * self.size[0],np.random.randint(0,self.map[1]) * self.size[1]]
				self.pos.append(self.pos[-1].copy())
			if self.pos[0] in self.pos[1:]: self.__init__()
			#self.spd = 0

		for i in range(len(self.pos)):
			cor = (self.pos[i][0],self.pos[i][1])
			if i == 0: self.surface.blit(self.imgs['0_' + str(self.dir)],cor)
			else:
				sz = (int(self.size[0]/(i)) - 1,int(self.size[1]/i) - 1)
				pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(cor[0] + int(self.size[0]/2) - int(sz[0]/2),cor[1] + int(self.size[1]/2) - int(sz[1]/2),sz[0],sz[1]))
		pygame.draw.rect(self.surface,(200,100,100),pygame.Rect(self.fd[0],self.fd[1],self.size[0] - 1,self.size[1] - 1))
		
		return self.surface

class HittheMole:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.holes = []
		for x in range(3):
			for y in range(3):
				self.holes.append([pygame.Rect(100 + (x * 60),200 + (y * 60),50,50),np.random.randint(100,400)])
		self.score = 0
		self.time = 30
	
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.holes:
				if pygame.Rect.colliderect(mouse,i[0]) and i[1] <= 0:
					self.score += 1
					i[1] = np.random.randint(100,400)
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for i in self.holes:
			if i[1] <= 0: pygame.draw.ellipse(self.surface, (0,200,0), i[0])
			pygame.draw.ellipse(self.surface, (0,0,200), i[0], 15)
			i[1] -= 1
			if i[1] < -100: i[1] = np.random.randint(100,400)
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

class FallingItems:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.basket = pygame.Rect(200,700,100,20)
		self.items = []
		self.score = 0
		self.time = 30
	
	def inside_events(self,pressed,mouse):
		self.basket.x = mouse.x
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		if self.time > 0: self.time -= 1
		else:
			self.items.append(pygame.Rect(np.random.randint(0,self.surface.get_width() - 20),-10,20,20))
			self.time = 100 - self.score
			if self.time <= 10: self.time = 10
		for i in self.items:
			pygame.draw.ellipse(self.surface, (200,0,0), i)

			i.y += 2 + np.floor(self.score/10)
			if pygame.Rect.colliderect(i,self.basket):
				self.score += 1
				i.width = 0
		self.items = [i for i in self.items if i.width != 0]
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		pygame.draw.rect(self.surface,(0,200,0), self.basket)
		
		return self.surface

class Jumping:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 22)
		self.ball = {'X': 200,'Y': 100, 'XSPEED': 0, 'YSPEED': 5}
		self.platforms = [[pygame.Rect(0,400,self.surface.get_width(),20),1]]
		for i in range(np.random.randint(2,5)): self.platforms.append([pygame.Rect(10 + np.random.randint(0,self.surface.get_width()), 200 + np.random.randint(0,100), 60, 5), 1])
		self.scroll = 1
		self.height = 1
		
	def inside_events(self,pressed,mouse):
		self.ball['X'] = pygame.mouse.get_pos()[0]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		#SCROLL
		if self.scroll < self.height: self.scroll += int((self.height - self.scroll)/1.5)
		#COLISION
		for p in self.platforms:
			if pygame.Rect.colliderect(pygame.Rect(int(self.ball['X']),int(self.ball['Y']),30,30),pygame.Rect(p[0].x,p[0].y + self.scroll,p[0].width,p[0].height)) and self.ball['YSPEED'] > 0:
				self.ball['Y'] -= self.ball['Y'] - 400
				self.ball['YSPEED'] = -(self.ball['YSPEED'])
				if 400 - p[0].y > self.height:
					self.height += 400 - p[0].y
					for i in range(np.random.randint(2,5)): self.platforms.append([pygame.Rect(10 + np.random.randint(0,self.surface.get_width()), 200 + np.random.randint(0,100) - self.height, 40, 5), 1])
			pygame.draw.rect(self.surface, (200,200,200), pygame.Rect(p[0].x,p[0].y + self.scroll,p[0].width,p[0].height))
		#DRAW BALL
		self.ball['Y'] += self.ball['YSPEED']
		self.ball['YSPEED'] += 0.5
		if self.ball['YSPEED'] >= 50: self.ball['YSPEED'] = 50
		pygame.draw.ellipse(self.surface, (200,0,0), (int(self.ball['X']),int(self.ball['Y']),30,30))

		self.surface.blit(self.font.render(str(int((self.height - 1)/10))+'m',1,(200,200,200)), (50,10))
		
		return self.surface

class FlappyBird:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.bird = {'Y': 0, 'YSPEED': 5}
		self.pipes = [[self.surface.get_width(),np.random.randint(0,650)]]
		self.time = 200
	
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			self.bird['YSPEED'] = -15
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.time > 0: self.time -= 1
		else: self.pipes.append([self.surface.get_width(),np.random.randint(0,650)]); self.time = 200
		self.bird['Y'] += self.bird['YSPEED']
		self.bird['YSPEED'] += 1
		
		#DRAW
		pygame.draw.ellipse(self.surface, (200,0,0), pygame.Rect(200,int(self.bird['Y']),30,30))
		for i in self.pipes:
			rct1 = pygame.Rect(i[0],0,50,i[1])
			rct2 = pygame.Rect(i[0],i[1] + 200,50,400 - i[1])
			pygame.draw.rect(self.surface,(200,200,200),rct1)
			pygame.draw.rect(self.surface,(200,200,200),rct2)
			if pygame.Rect.colliderect(pygame.Rect(200,int(self.bird['Y']),30,30),rct1): self.__init__()
			if pygame.Rect.colliderect(pygame.Rect(200,int(self.bird['Y']),30,30),rct2): self.__init__()
			i[0] -= 3
		self.pipes = [i for i in self.pipes if i[0] > 0]
		
		return self.surface

class Breakout:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.ball = {'X': 100,'Y': 500, 'XSPEED': 10, 'YSPEED': 10}
		self.basket = pygame.Rect(200,800,100,20)
		self.bricks = []
		for x in range(13):
			for y in range(7):
				self.bricks.append([pygame.Rect(x * 50,100 + (y * 20),49,19),6 - y])
	
	def inside_events(self,pressed,mouse):
		mp = pygame.mouse.get_pos()
		self.basket.x = mp[0]
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.ball['X'] += self.ball['XSPEED']
		self.ball['Y'] += self.ball['YSPEED']
		if self.ball['X'] <= 0 or self.ball['X'] >= self.surface.get_width():
			if self.ball['X'] <= 0: self.ball['X'] += -self.ball['X']
			if self.ball['X'] >= self.surface.get_width(): self.ball['X'] -= (self.ball['X'] - self.surface.get_width())
			self.ball['XSPEED'] = -self.ball['XSPEED'] * 0.8
		if self.ball['Y'] <= 0 or self.ball['Y'] >= 1000:
			if self.ball['Y'] <= 0: self.ball['Y'] += -self.ball['Y']
			if self.ball['Y'] >= 1000: self.__init__()
			self.ball['YSPEED'] = -self.ball['YSPEED']
		if pygame.Rect.colliderect(pygame.Rect(self.ball['X'],self.ball['Y'],30,30),self.basket):
			self.ball['XSPEED'] = int((self.ball['X'] - self.basket.x + 50)/5) 
			self.ball['YSPEED'] = -self.ball['YSPEED']
		for i in self.bricks:
			cc = [(200,0,0),(200,100,0),(200,200,0),(0,200,0),(0,200,200),(0,0,200),(200,0,200)]
			pygame.draw.rect(self.surface,cc[i[1]],i[0])
			if pygame.Rect.colliderect(pygame.Rect(self.ball['X'],self.ball['Y'],30,30),i[0]):
				self.ball['YSPEED'] = -self.ball['YSPEED']
				self.ball['Y'] = i[0].y + i[0].height
				i[1] -= 1
		self.bricks = [i for i in self.bricks if i[1] > -1]
		pygame.draw.ellipse(self.surface, (200,0,0), (int(self.ball['X']),int(self.ball['Y']),30,30))
		pygame.draw.rect(self.surface,(0,200,0), self.basket)
		
		return self.surface

class BubbleBubble:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.nxt = [np.random.randint(0,6) for i in range(3)]
		self.mp = [0,0]
		self.balls = []
		self.direction = 0
		for x in range(10): self.balls.append([pygame.Rect(200 + (x * 35),20,30,30),0,0])
		
	def inside_events(self,pressed,mouse):
		self.mp = [mr.x - 200,mr.y - 500]
		if pressed[4][0]:
			self.balls.append([pygame.Rect(200,500,30,30),5,self.nxt[0]])
			del self.nxt[0]
			self.nxt.append(np.random.randint(0,7))
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.balls[len(self.balls)-1][0].x += int(np.cos(self.direction) * 5)
		self.balls[len(self.balls)-1][0].y += int(np.sin(self.direction) * 5)
		cc = [(200,0,0),(200,100,0),(200,200,0),(0,200,0),(0,200,200),(0,0,200),(200,0,200)]
		for i in self.balls: pygame.draw.ellipse(self.surface,cc[i[2]],i[0])
		pygame.draw.circle(self.surface,(200,200,200),(200,500),50,2)
		pygame.draw.line(self.surface,(100,200,100),(200,500),(200 + (np.cos(self.mp[0]) * 90),450 + (np.cos(self.mp[1])) * 90),3)
		
		return self.surface

class ColorMatch:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		bbs = []
		for i in range(20): bbs += [0,1,2,3,4]
		for y in range(10):
			for x in range(10):
				rr = np.random.randint(0,len(bbs))
				self.grid.append([x,y,bbs[rr]])
				del bbs[rr]
		self.select = None
		self.wait = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in range(len(self.grid)):
				if pygame.Rect.colliderect(mouse,pygame.Rect(100 + (self.grid[i][0] * 42), 100 + (self.grid[i][1] * 42), 40, 40)):
					if self.select != None:
						if self.grid[i][0:2] in [[self.grid[self.select][0] - 1,self.grid[self.select][1]],[self.grid[self.select][0] + 1,self.grid[self.select][1]],
							[self.grid[self.select][0],self.grid[self.select][1] - 1],[self.grid[self.select][0],self.grid[self.select][1] + 1]]:
							chg = self.grid[i][2]
							self.grid[i][2] = self.grid[self.select][2]
							self.grid[self.select][2] = chg
							self.select = None
							self.wait = 50
					else: self.select = i
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		cc = [(200,100,100),(200,200,100),(100,200,100),(100,100,200),(200,200,200),(0,0,0)]
		for i in range(len(self.grid)):
			if self.select == i: pygame.draw.ellipse(self.surface,(200,200,200),pygame.Rect(95 + (self.grid[i][0] * 42), 95 + (self.grid[i][1] * 42), 50, 50))
			pygame.draw.ellipse(self.surface,cc[self.grid[i][2]],pygame.Rect(100 + (self.grid[i][0] * 42), 100 + (self.grid[i][1] * 42), 40, 40))
		if self.wait > 0:
			self.wait -= 1
			if self.wait == 0:
				for i in range(len(self.grid)):
					for j in range(len(self.grid)):
						if i != j and self.grid[i][0:2] in [[self.grid[j][0] - 1,self.grid[j][1]],[self.grid[j][0] + 1,self.grid[j][1]],[self.grid[j][0],self.grid[j][1] - 1],[self.grid[j][0],self.grid[j][1] + 1]]:
							for k in range(len(self.grid)):
								if j != k and self.grid[j][0:2] in [[self.grid[k][0] - 1,self.grid[k][1]],[self.grid[k][0] + 1,self.grid[k][1]],[self.grid[k][0],self.grid[k][1] - 1],[self.grid[k][0],self.grid[k][1] + 1]]:
									self.grid[i][2] = 5; self.grid[j][2] = 5; self.grid[k][2] = 5
									self.wait = 50
		
		return self.surface

class MusicTiles:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.tiles = []
		for x in range(7):
			self.tiles.append([pygame.Rect(10 + (x * 65), -80, 60, 80), None, 0])
		self.speed = 3
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.tiles:
				if pygame.Rect.colliderect(mouse,i[0]):
					pass
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		#self.surface.blit(self.font.render(self.txt,1,(200,200,200)), (10,10))
		cc = [(200,100,100),(200,200,100),(150,200,100),(100,200,100),(100,200,200),(100,100,200),(200,100,200)]
		for i in self.tiles:
			pygame.draw.rect(self.surface, cc[int((i[0].x-10)/65)], i[0])
			i[0].y += self.speed
		pygame.draw.rect(self.surface, (200,200,200), pygame.Rect(0,300,500,80),5)
		
		return self.surface

#BALL SPORTS
class Pool:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.nfnt = pygame.font.SysFont("Arial", 18)
		self.score = 0
		self.time = 1
		self.pang = 0
		self.pbll = [pygame.Rect(300,500,40,40),0,0]
		
		self.balls = []
		for b in range(12):
			self.balls.append([b,pygame.Rect(b*50,b*50,40,40),0,0])
		self.holes = [pygame.Rect(10,10,50,50),pygame.Rect(265,10,50,50),pygame.Rect(580,10,50,50),pygame.Rect(10,645,50,50),pygame.Rect(580,645,50,50),pygame.Rect(10,1270,50,50),pygame.Rect(265,1270,50,50),pygame.Rect(580,1270,50,50)]
		self.colors = [(200,200,10),(10,10,200),(200,10,10),(200,10,200),(200,10,10),(10,200,10),(100,50,10),(10,10,10),(200,200,10),(10,10,200),(200,10,10),(200,10,200),(200,100,10),(10,200,10),(100,50,10)]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			if pygame.Rect.colliderect(mouse,self.pbll[0]):
				self.pbll[1] = 20
				self.pbll[2] = self.pang
			self.pang += 0.5
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((10,200,100))
		if self.time < 0:
			self.time += 1
		for i in self.holes:
			pygame.draw.ellipse(self.surface,(50,50,50),i)
		for i in self.balls:
			if i[2] > 0:
				i[2] -= 0.1
				i[1].x += int(np.cos(i[3]) * i[2])
				i[1].y += int(np.sin(i[3]) * i[2])
			if pygame.Rect.colliderect(i[1],self.pbll[0]) and i[1].width == 40:
					i[2] += self.pbll[1]
					i[3] = self.pbll[2]
					self.pbll[1] = int(self.pbll[1]/2)
					self.pbll[2] += 2
			for b in self.balls:
				if pygame.Rect.colliderect(i[1],b[1]) and i != b and b[1].width == 40:
					b[2] += i[2]
					b[3] = i[3]
					i[2] = int(i[2]/2)
					i[3] += 2
			for h in self.holes:
				if pygame.Rect.colliderect(i[1],h) and i[1].width == 40:
					i[1] = pygame.Rect(h.x + 10,h.y + 10,30,30)
					i[2] = 0
					
			if i[1].x <= 0: i[1].x += 2; i[3] += 2
			if i[1].x >= self.surface.get_width(): i[1].x -= 2; i[3] += 2
			if i[1].y <= 0: i[1].y += 2; i[3] += 2
			if i[1].y >= self.surface.get_height(): i[1].y -= 2; i[3] += 2
			
			if i[0] < 9: c = ((240,240,240),(10,10,10))
			else: c = ((10,10,10),(240,240,240))
			pygame.draw.ellipse(self.surface,self.colors[i[0]],i[1])
			pygame.draw.ellipse(self.surface,c[0],pygame.Rect(i[1].x + 10,i[1].y + 10,20,20))
			self.surface.blit(self.nfnt.render(str(i[0]),True,c[1]),(i[1].x + 20 - (len(str(i[0])) * 5),i[1].y + 10))
		if self.pbll[1] > 0:
			self.pbll[1] -= 0.1
			self.pbll[0].x += int(np.cos(self.pbll[2]) * self.pbll[1])
		self.pbll[0].y += int(np.sin(self.pbll[2]) * self.pbll[1])
		
		if self.pbll[0].x <= 0: self.pbll[0].x += 2; self.pbll[2] += 2
		if self.pbll[0].x >= self.surface.get_width(): self.pbll[0].x -= 2; self.pbll[2] += 2
		if self.pbll[0].y <= 0: self.pbll[0].y += 2; self.pbll[2] += 2
		if self.pbll[0].y >= self.surface.get_height(): self.pbll[0].y -= 2; self.pbll[2] += 2
		
		pygame.draw.ellipse(self.surface,(240,240,240),self.pbll[0])
		pygame.draw.line(self.surface,(240,240,240),(self.pbll[0].x + 20 - int(np.cos(self.pang) * 30),self.pbll[0].y + 20 - int(np.sin(self.pang) * 30)),(self.pbll[0].x + 20 - int(np.cos(self.pang) * 250),self.pbll[0].y + 20 - int(np.sin(self.pang) * 250)),3)

		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

class MiniGolf: pass

class Bowling: pass

class CannonBattle:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.balls = []
		self.strg = 0
		
	def inside_events(self,pressed,mouse):
		mp = pygame.mouse.get_pos()
		xx = mp[0]
		if xx < 100: xx = 100
		if xx > 200: xx = 200
		yy = mp[1]
		if yy < 300: yy = 300
		if yy > 400: yy = 400
		if pressed[4][0]: self.balls.append({'X': xx,'Y': yy, 'XSPEED': (xx - 100)/25, 'YSPEED': (yy - 400)/25})
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		mp = pygame.mouse.get_pos()
		pygame.draw.rect(self.surface,(200,100,100),pygame.Rect(50,300,10,self.strg))
		pygame.draw.rect(self.surface,(100,100,100),pygame.Rect(100,300,100,100),2)
		xx = mp[0]
		if xx < 100: xx = 100
		if xx > 200: xx = 200
		yy = mp[1]
		if yy < 300: yy = 300
		if yy > 400: yy = 400
		pygame.draw.line(self.surface,(100,200,100),(100,400),(xx,yy),10)
		for i in self.balls:
			i['X'] += i['XSPEED']
			i['Y'] += i['YSPEED']
			i['YSPEED'] += 0.2
			pygame.draw.ellipse(self.surface, (200,200,200), (int(i['X']),int(i['Y']),10,10))
		self.balls = [i for i in self.balls if i['Y'] < 500]
		pygame.draw.ellipse(self.surface, (200,100,100), (mp[0] - 5,mp[1] - 5,10,10),5)
		
		return self.surface

#MEMORY GAMING
class Twothousandforthyeight:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 15)
		self.blocks = [[[0,2],[0,0],0,0]]
		self.direction = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if mr.y < 100: self.direction = 1
			elif mr.x > 260: self.direction = 2
			elif mr.y > 260: self.direction = 3
			elif mr.x < 100: self.direction = 4
			cor = []
			for y in range(4):
				for x in range(4):
					cor.append([x * 41,y * 41])
			for i in self.blocks:
				j = 0
				while j < len(cor):
					if i[1][0] == cor[j][0] and i[1][1] == cor[j][1]:
						del cor[j]; j -= 1
					j += 1
			self.blocks.append([[len(self.blocks),2],cor[np.random.randint(0,len(cor))],0,-10])
			for i in self.blocks: i[2] = 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		for y in range(5):
			for x in range(5):
				pygame.draw.rect(self.surface,(100,100,100),pygame.Rect(100 + (x * 41),100 + (y * 41),40,40))
		for i in self.blocks:
			pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(100 + i[1][0] - i[4],100 + i[1][1] - i[4],40 + (i[4] * 2),40 + (i[4] * 2)))
			self.surface.blit(self.font.render(str(i[0][1]),1,(10,10,10)), (100 + i[1][0],100 + i[1][1]))
			if i[2] == 1:
				if self.direction == 1: i[1][1] -= 2
				if self.direction == 2: i[1][0] += 2
				if self.direction == 3: i[1][1] += 2
				if self.direction == 4: i[1][0] -= 2
				for j in self.blocks:
					if i[0][0] != j[0][0] and pygame.Rect.colliderect(pygame.Rect(i[1][0],i[1][1],40,40),pygame.Rect(j[1][0],j[1][1],40,40)):
						if i[0][1] == j[0][1]:
							i[0][1] += j[0][1]; j[0][0] = -1
							i[4] = 10; j[4] = 10
						else: i[2] = 0; j[2] = 0
				if i[1][0] < 0: i[1][0] = 0; i[2] = 0
				if i[1][0] > 164: i[1][0] = 164; i[2] = 0
				if i[1][1] < 0: i[1][1] = 0; i[2] = 0
				if i[1][1] > 164: i[1][1] = 164; i[2] = 0
			else:
				i[1][0] = np.floor(i[1][0]/41) * 41
				i[1][1] = np.floor(i[1][1]/41) * 41
			if i[4] < 0: i[4] += 1
			elif i[4] > 0: i[4] -= 1
		self.blocks = [i for i in self.blocks if i[0][0] != -1]

		return self.surface

class Memory:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.score = 0
		self.time = 100
		self.match = [0,0]
		self.shuffle()
	
	def shuffle(self):
		self.buttons = []
		self.values = []
		for i in range(6):
			for j in range(2):
				self.values.append(i + 1)
		for x in range(4):
			for y in range(3):
				v = np.random.randint(0,len(self.values))
				self.buttons.append([pygame.Rect(100 + (x * 60),200 + (y * 60),50,50),self.values[v],2])
				del self.values[v]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.time == 0:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if i[2] == 0:
					if pygame.Rect.colliderect(mouse,i[0]):
						if self.match[0] == 0:
							self.match[0] = i[1]
						else: self.match[1] = i[1]
						i[2] = 1
						break
			if self.match[0] != 0 and self.match[1] != 0:
				for i in self.buttons:
					if i[1] in self.match:
						if self.match[0] != self.match[1] and i[2] == 1:
							self.time = 30
							i[2] = 2
				self.match = [0,0]
			q = 0
			for i in self.buttons:
				if i[2] == 1: q += 1
			if q == len(self.buttons):
				self.score += 1
				self.time = 100
				self.shuffle()
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.time > 0: self.time -= 1
		for i in self.buttons:
			if self.time == 0 and i[2] == 2: i[2] = 0
			if i[2] == 0: c = (100,100,100)
			elif i[1] == 1: c = (200,10,10)
			elif i[1] == 2: c = (200,100,10)
			elif i[1] == 3: c = (200,200,10)
			elif i[1] == 4: c = (100,200,10)
			elif i[1] == 5: c = (10,200,200)
			elif i[1] == 6: c = (10,10,200)
			pygame.draw.rect(self.surface,c,i[0])
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

class Simon:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.score = 0
		self.time = 1
		self.sequence = [np.random.randint(0,4)]
		self.mimic = []
		self.turn = 0
		
		self.buttons = []
		for y in range(2):
			for x in range(2):
				self.buttons.append([pygame.Rect(100 + (x * 60),400 + (y * 60),50,50),0])
		self.buttons[self.sequence[0]][1] = 20
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.time == len(self.sequence):
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			v = 0
			for i in self.buttons:
				if pygame.Rect.colliderect(mouse,i[0]):
						self.mimic.append(v)
						i[1] = 20
				v += 1
			if self.mimic[self.turn] == self.sequence[self.turn]:
				self.turn += 1
				if self.turn == len(self.sequence):
					self.sequence.append(np.random.randint(0,4))
					self.mimic = []
					self.turn = 0
					self.time = -60
					self.score += 1
			else:
				self.sequence = [np.random.randint(0,4)]
				self.mimic = []
				self.turn = 0
				self.time = -60
				self.score = 0
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.time < 0:
			self.time += 1
			if self.time == -1:
				self.buttons[self.sequence[0]][1] = 20
		elif self.time < len(self.sequence):
			if self.buttons[self.sequence[self.time]][1] == 0:
				self.time += 1
				if self.time < len(self.sequence):
					self.buttons[self.sequence[self.time]][1] = 20
		v = 0
		for i in self.buttons:
			if i[1] > 0: i[1] -= 1
			if i[1] < 6: c = (100,100,100)
			elif v == 0: c = (200,10,10)
			elif v == 1: c = (200,200,10)
			elif v == 2: c = (100,200,10)
			elif v == 3: c = (10,10,200)
			pygame.draw.rect(self.surface,c,i[0])
			v += 1
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

class FindtheCup:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.img = pygame.Surface((20,30),pygame.SRCALPHA)
		pygame.draw.polygon(self.img,(100,100,100),((5,0),(25,0),(20,25),(0,25)))
		pygame.draw.ellipse(self.img,(100,100,100),pygame.Rect(0,20,20,10))
		self.inside = 1
		self.cups = [0,1,2]
		self.mov = []
		self.buttons = [pygame.Rect(200,200,40,40),pygame.Rect(250,200,40,40),pygame.Rect(300,200,40,40)]
		self.moves = 20
		self.wait = 50
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.moves == 0 and self.wait == 0:
			for i in self.buttons:
				if pygame.Rect.colliderect(mouse,i):
					self.moves = 20
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(str(self.cups[0]),1,(200,200,200)), (10,10))
		self.surface.blit(self.font.render(str(self.cups[1]),1,(200,200,200)), (10,50))
		self.surface.blit(self.font.render(str(self.cups[2]),1,(200,200,200)), (10,100))
		if self.wait > 0:
			if self.mov != []:
				self.cups[self.mov[0]] += 0.02
				self.cups[self.mov[1]] -= 0.02
			self.wait -= 1
		elif self.moves > 0:
			for i in range(len(self.cups)): self.cups[i] = int(self.cups[i])
			self.mov = []
			while len(self.mov) < 1:
				j = np.random.randint(0,len(self.cups))
				if j not in self.mov and int(self.cups[j] != 2): self.mov.append(j)
			while len(self.mov) < 2:
				j = np.random.randint(0,len(self.cups))
				if j not in self.mov and int(self.cups[j] != 0): self.mov.append(j)
			self.moves -= 1
			self.wait = 50
		for i in range(len(self.cups)):
			self.surface.blit(self.img,(200 + (self.cups[i] * 50),200))
			if int(self.cups[i]) == int(self.inside): pygame.draw.ellipse(self.surface,(200,100,100),self.buttons[i])
		
		return self.surface

class ImageMatch:
	def __init__(self):
		self.surface = pygame.Surface((640,1280))
		self.font = pygame.font.SysFont("Arial", 64)
		self.rows = [0,0,0]
		self.lock = 0
		self.images = []
		for i in ['madladcat','flamencoflamingo','eggrapper1','peacockpigeon','bigeye']:
			self.images.append(pygame.image.load(res.FREAKS_PATH + i + '_stand.png'))
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.KEYDOWN:
			self.lock += 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for y in range(len(self.rows)):
			ln = 0
			for i in self.images: ln += i.get_width() + 10
			xx = 0
			for i in self.images:
				self.surface.blit(i,(xx + self.rows[y], 20 + (int(i.get_height()/len(self.rows)) * y)),pygame.Rect(0,0,i.get_width(),int(i.get_height()/len(self.rows)) * y))
				self.surface.blit(i,(xx + ln + self.rows[y], 20 + (int(i.get_height()/len(self.rows)) * y)),pygame.Rect(0,0,i.get_width(),int(i.get_height()/len(self.rows)) * y))
				xx += i.get_width() + 10
			if ln >= self.lock:
				if y%2 == 0:
					self.rows[y] += 2
					if self.rows[y] > ln: self.rows[y] = 0
				else:
					self.rows[y] -= 2
					if self.rows[y] < -ln: self.rows[y] = 0
		return self.surface

class Cassino:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.slots = []
		self.sltsz = 90
		for i in range(3): self.slots.append(np.random.randint(0,10) * self.sltsz)
		self.stop = 0
		self.acc = 10.0
		self.img = pygame.Surface((self.sltsz,self.sltsz * 11))
		self.img.fill((200,200,200))
		for y in range(10):
			self.img.blit(self.font.render(str(y),True,(10,10,10)),(10,10 + (y * self.sltsz)))
		self.img.blit(self.font.render("0",True,(10,10,10)),(10,10 + (11 * self.sltsz)))
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.acc == 0.0: self.acc = 10.0
			elif self.stop == 0: self.stop = 50
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		if self.stop > 0:
			if self.acc > 0: self.acc -= 0.5
			self.stop -= 1
		for i in range(len(self.slots)):
			if self.acc == 0.0:
				self.slots[i] = int(self.slots[i]/self.sltsz) * self.sltsz
		for x in range(3):
			self.surface.blit(self.img,(50 + (x * 100),200),(0,self.slots[x],self.sltsz,self.sltsz))
			self.slots[x] += int(self.acc)
			if self.slots[x] > self.sltsz * 10: self.slots[x] = 0
		
		return self.surface

class Roulette:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.spin = 0.0
		self.speed = 0.0
		self.load = 0
		self.prizes = [10,20,30,40,50,60,70,80]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.load == 0:
			self.speed = 0.5
			self.load = 100
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		#self.surface.blit(self.font.render(self.txt,1,(200,200,200)), (10,10))
		if self.speed > 0:
			self.spin += self.speed
			self.speed -= 0.003
		if self.load > 0: self.load -= 1
		cc = [(200,100,100),(200,200,100),(100,200,100),(100,100,200),(200,100,100),(200,200,100),(100,200,100),(100,100,200)]
		for i in range(len(self.prizes)):
			pygame.draw.arc(self.surface,cc[i],(100,100,200,200),((i/(len(self.prizes)/2)) + self.spin) * 3.14,(((i+1)/(len(self.prizes)/2)) + self.spin) * 3.14,100)
		pygame.draw.polygon(self.surface,(100,100,100),((190,90),(210,90),(200,110)))
		
		return self.surface

class NumberPuzzle:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 13)
		self.grid = []
		lst = [1,2,3,4,5,6,7,8]
		for y in range(3):
			for x in range(3):
				if len(self.grid) < 8:
					rr = np.random.randint(0,len(lst))
					self.grid.append([x,y,lst[rr]])
					del lst[rr]
		self.hole = [2,2]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.grid:
				if pygame.Rect.colliderect(mouse,pygame.Rect(100 + (i[0] * 41), 150 + (i[1] * 41), 40, 40)):
					if [i[0],i[1]] in [[self.hole[0] + x,self.hole[1] + y] for x in [-1,0,1] for y in [-1,0,1] if abs(x) != abs(y)]:
						pst = i.copy()
						i[0] = self.hole[0]
						i[1] = self.hole[1]
						self.hole = [pst[0],pst[1]]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for i in self.grid:
			pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(100 + (i[0] * 41), 150 + (i[1] * 41), 40, 40))
			self.surface.blit(self.font.render(str(i[2]),1,(10,10,10)), (110 + (i[0] * 41),160 + (i[1] * 41)))
		
		return self.surface

#BOARD GAMING
class Chess:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.smll = pygame.font.SysFont("Arial", 15)
		self.grid = []
		for y in range(8):
			self.grid.append([])
			for x in range(8):
				self.grid[y].append([pygame.Rect(50 + (x * 41), 50 + (y * 41), 40, 40), 0, 0])
		pp = [1,2,3,4,5,3,2,1]
		for i in range(len(pp)): self.grid[0][i][2] = pp[i]; self.grid[0][i][1] = 1
		for i in range(len(pp)): self.grid[7][i][2] = pp[i]; self.grid[7][i][1] = 2
		for i in range(8): self.grid[1][i][2] = 0; self.grid[1][i][1] = 1
		for i in range(8): self.grid[6][i][2] = 0; self.grid[6][i][1] = 2
		self.piece = [None,None]
		self.places = []
		self.turn = 0
		self.score = [0,0]

	def search(self,x,y,nxt=False):
		att = False
		tt = int(not self.turn)
		if self.grid[y][x][2] in [1,2,4]: rr = 10
		else: rr = 2
		fxrng = [0]
		fyrng = [0]
		for r in range(1,rr + 1):
			if x - r >= 0: fxrng.append(-r)
			if x + r <= 7: fxrng.append(r)
			if y - r >= 0: fyrng.append(-r)
			if y + r <= 7: fyrng.append(r)
		for fy in fyrng:
			for fx in fxrng:
				do = False
				if self.grid[y][x][2] == 0 and fy == tt: do = True
				if self.grid[y][x][2] in [3,4,5] and abs(fx) == abs(fy): do = True
				if self.grid[y][x][2] in [1,4,5] and abs(fx) != abs(fy): do = True
				if do and x + fx >= 0 and x + fx <= 7 and y + fy >= 0 and y + fy <= 7:
					rd = []
					if fx < 0: rd.append(x + fx + 1)
					else: rd.append(x + fx - 1)
					if fy < 0: rd.append(y + fy + 1)
					else: rd.append(y + fy - 1)
					if self.grid[y + fy][x + fx][1] == 0 and self.grid[rd[1]][rd[0]][1] == tt + 1:
						if att == False: self.places = []
						self.places.append([x + fx,y + fy])
						self.places.append([rd[0],rd[1]])
						att = True
					elif self.grid[y + fy][x + fx][1] == 0 and att == False and nxt == False:
						do = False
						if self.grid[y][x][2] == 1: do = True
						elif self.turn + fy == tt and abs(fx) == 1: do = True
						if do: self.places.append([x + fx,y + fy])
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.score[0] == 20: self.__init__()
			if self.score[1] == 20: self.__init__()
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						if self.piece == [None,None]:
							if self.grid[y][x][1] == self.turn + 1:
								self.piece = [x,y]
								self.search(x,y)
						else:
							tt = int(not self.turn)
							if x == self.piece[0] and y == self.piece[1]: self.piece = [None,None]; self.places = []
							elif [x,y] in self.places and self.grid[y][x][1] == 0:
								self.grid[self.piece[1]][self.piece[0]][1] = 0
								self.grid[y][x][1] = self.turn + 1
								att = False
								for i in self.places:
									if abs(self.piece[0] - i[0]) == abs(self.piece[0] - x) - 1 and abs(self.piece[1] - i[1]) == abs(self.piece[1] - y) - 1:
										self.grid[(i[1] - self.piece[1]) + self.piece[1]][(i[0] - self.piece[0]) + self.piece[0]][1] = 0
										self.grid[(i[1] - self.piece[1]) + self.piece[1]][(i[0] - self.piece[0]) + self.piece[0]][2] = 0
										self.score[self.turn] += 1
										att = True
								#MASTER
								if self.turn == 0 and y == 9: self.grid[y][x][2] = 1
								if self.turn == 1 and y == 0: self.grid[y][x][2] = 1
								if self.grid[self.piece[1]][self.piece[0]][2] == 1:
									self.grid[self.piece[1]][self.piece[0]][2] = 0
									self.grid[y][x][2] = 1
								self.piece = [None,None]
								self.places = []
								if att: self.search(x,y,True)
								if self.places == []: self.turn = int(not self.turn)
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		bw = False
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.piece == [x,y]: cc = (100,200,100)
				elif bw: cc = (10,10,10)
				else: cc = (200,200,200)
				pygame.draw.rect(self.surface,cc,self.grid[y][x][0])
				if self.grid[y][x][1] == 1:
					pygame.draw.ellipse(self.surface,(200,100,100),self.grid[y][x][0])
					self.surface.blit(self.smll.render(str(self.grid[y][x][2]),1,(20,20,20)), (self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10))
				if self.grid[y][x][1] == 2:
					pygame.draw.ellipse(self.surface,(10,10,200),self.grid[y][x][0])
					self.surface.blit(self.smll.render(str(self.grid[y][x][2]),1,(200,200,200)), (self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10))
				if [x,y] in self.places: pygame.draw.ellipse(self.surface,(100,100,100),pygame.Rect(self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10,self.grid[y][x][0].width - 20,self.grid[y][x][0].height - 20))
				bw = not bw
			bw = not bw
		
		return self.surface

class Checkers:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(10):
			self.grid.append([])
			for x in range(10):
				self.grid[y].append([pygame.Rect(50 + (x * 41), 50 + (y * 41), 40, 40), 0, 0])
		for i in range(5): self.grid[0][1 + (i * 2)][1] = 1
		for i in range(5): self.grid[1][(i * 2)][1] = 1
		for i in range(5): self.grid[2][1 + (i * 2)][1] = 1
		for i in range(5): self.grid[3][(i * 2)][1] = 1
		for i in range(5): self.grid[6][1 + (i * 2)][1] = 2
		for i in range(5): self.grid[7][(i * 2)][1] = 2
		for i in range(5): self.grid[8][1 + (i * 2)][1] = 2
		for i in range(5): self.grid[9][(i * 2)][1] = 2
		self.piece = [None,None]
		self.places = []
		self.turn = 0
		self.score = [0,0]

	def search(self,x,y,nxt=False):
		att = False
		if self.grid[y][x][2] == 1: rr = 10
		else: rr = 2
		fxrng = []
		fyrng = []
		for r in range(1,rr + 1):
			if x - r >= 0: fxrng.append(-r)
			if x + r <= 9: fxrng.append(r)
			if y - r >= 0: fyrng.append(-r)
			if y + r <= 9: fyrng.append(r)
		for fy in fyrng:
			for fx in fxrng:
				if abs(fx) == abs(fy) and x + fx >= 0 and x + fx <= 9 and y + fy >= 0 and y + fy <= 9:
					tt = int(not self.turn)
					rd = []
					if fx < 0: rd.append(x + fx + 1)
					else: rd.append(x + fx - 1)
					if fy < 0: rd.append(y + fy + 1)
					else: rd.append(y + fy - 1)
					if abs(fx) > 1 and self.grid[y + fy][x + fx][1] == 0 and self.grid[rd[1]][rd[0]][1] == tt + 1:
						if att == False: self.places = []
						self.places.append([x + fx,y + fy])
						self.places.append([rd[0],rd[1]])
						att = True
					elif self.grid[y + fy][x + fx][1] == 0 and att == False and nxt == False:
						do = False
						if self.grid[y][x][2] == 1: do = True
						elif self.turn + fy == tt and abs(fx) == 1: do = True
						if do: self.places.append([x + fx,y + fy])
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.score[0] == 20: self.__init__()
			if self.score[1] == 20: self.__init__()
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						if self.piece == [None,None]:
							if self.grid[y][x][1] == self.turn + 1:
								self.piece = [x,y]
								self.search(x,y)
						else:
							tt = int(not self.turn)
							if x == self.piece[0] and y == self.piece[1]: self.piece = [None,None]; self.places = []
							elif [x,y] in self.places and self.grid[y][x][1] == 0:
								self.grid[self.piece[1]][self.piece[0]][1] = 0
								self.grid[y][x][1] = self.turn + 1
								att = False
								for i in self.places:
									if abs(self.piece[0] - i[0]) == abs(self.piece[0] - x) - 1 and abs(self.piece[1] - i[1]) == abs(self.piece[1] - y) - 1:
										self.grid[(i[1] - self.piece[1]) + self.piece[1]][(i[0] - self.piece[0]) + self.piece[0]][1] = 0
										self.grid[(i[1] - self.piece[1]) + self.piece[1]][(i[0] - self.piece[0]) + self.piece[0]][2] = 0
										self.score[self.turn] += 1
										att = True
								#MASTER
								if self.turn == 0 and y == 9: self.grid[y][x][2] = 1
								if self.turn == 1 and y == 0: self.grid[y][x][2] = 1
								if self.grid[self.piece[1]][self.piece[0]][2] == 1:
									self.grid[self.piece[1]][self.piece[0]][2] = 0
									self.grid[y][x][2] = 1
								self.piece = [None,None]
								self.places = []
								if att: self.search(x,y,True)
								if self.places == []: self.turn = int(not self.turn)
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		bw = False
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.piece == [x,y]: cc = (100,200,100)
				elif bw: cc = (10,10,10)
				else: cc = (200,200,200)
				pygame.draw.rect(self.surface,cc,self.grid[y][x][0])
				if self.grid[y][x][1] == 1: pygame.draw.ellipse(self.surface,(200,100,100),self.grid[y][x][0])
				if self.grid[y][x][1] == 2: pygame.draw.ellipse(self.surface,(10,10,200),self.grid[y][x][0])
				if self.grid[y][x][2] == 1: pygame.draw.ellipse(self.surface,(200,200,200),pygame.Rect(self.grid[y][x][0].x + 2,self.grid[y][x][0].y + 2,self.grid[y][x][0].width - 4,self.grid[y][x][0].height - 4))
				if [x,y] in self.places: pygame.draw.ellipse(self.surface,(100,100,100),pygame.Rect(self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10,self.grid[y][x][0].width - 20,self.grid[y][x][0].height - 20))
				bw = not bw
			bw = not bw
		
		return self.surface

class Trilha:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(7):
			self.grid.append([])
			for x in range(7):
				vl = -1
				if y in [0,6] and x in [0,3,6]: vl = 0
				if y in [1,5] and x in [1,3,5]: vl = 0
				if y in [2,4] and x in [2,3,4]: vl = 0
				if y == 3 and x in [0,1,2,4,5,6]: vl = 0
				self.grid[y].append([pygame.Rect(50 + (x * 40), 50 + (y * 40), 40, 40), vl])
		self.piece = [None,None]
		self.places = []
		self.turn = 0
		self.score = [9,9]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.score[0] == -6: self.__init__()
			if self.score[1] == -6: self.__init__()
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						tt = int(not self.turn - 2)
						if self.turn > 1 and self.grid[y][x][1] == tt:
							self.grid[y][x][1] = 0
							self.score[tt] -= 1
						elif self.score[self.turn] > 0 and self.grid[y][x][1] == 0:
							self.score[self.turn] -= 1
							self.grid[y][x][1] = self.turn + 1
							self.turn = int(not self.turn)
						elif self.piece == [None,None]:
							if self.grid[y][x][1] == self.turn + 1:
								self.piece = [x,y]
								fxrng = [0]
								fyrng = [0]
								if x > 0: fxrng.append(-1)
								if x < 6: fxrng.append(1)
								if y > 0: fyrng.append(-1)
								if y < 6: fyrng.append(1)
								for py in fyrng:
									for px in fxrng:
										sz = 1
										while True:
											if self.grid[y + (py * sz)][x + (px * sz)][1] == 0 and abs(px) != abs(py):
												self.places.append([x + px,y + py]); break
											elif self.grid[y + (py * sz)][x + (px * sz)][1] == -1:
												if px * (sz + 1) > 0 and px * (sz + 1) < 6: sz += 1
												elif py * (sz + 1) > 0 and py * (sz + 1) < 6: sz += 1
												else: break
											else: break
						else:
							if x == self.piece[0] and y == self.piece[1]: self.piece = [None,None]; self.places = []
							elif [x,y] in self.places and self.grid[y][x][1] == 0:
								self.grid[self.piece[1]][self.piece[0]][1] = 0
								self.grid[y][x][1] = self.turn + 1
								self.piece = [None,None]
								self.places = []
								ya = [0,0,0,0,0,0,0]
								for cy in range(7):
									xa = 0
									for cx in range(7):
										if self.grid[cy][cx][1] == self.turn + 1:
											xa += 1
											ya[cx] += 1
										elif self.grid[cy][cx][1] != -1:
											xa = 0
								print(xa)
								if xa == 3 or 3 in ya: self.turn += 2
								else: self.turn = int(not self.turn)
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		bw = False
		pygame.draw.rect(self.surface,(100,50,10),pygame.Rect(50, 50, 280, 280))
		pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(70, 70, 240, 240),3)
		pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(110, 110, 160, 160),3)
		pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(150, 150, 80, 80),3)
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.piece == [x,y]: pygame.draw.rect(self.surface,(100,200,100),self.grid[y][x][0])
				if self.grid[y][x][1] == 0: pygame.draw.ellipse(self.surface,(10,10,10),pygame.Rect(self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10,self.grid[y][x][0].width - 20,self.grid[y][x][0].height - 20))
				if self.grid[y][x][1] == 1: pygame.draw.ellipse(self.surface,(200,200,200),self.grid[y][x][0])
				if self.grid[y][x][1] == 2: pygame.draw.ellipse(self.surface,(10,10,10),self.grid[y][x][0])
				if [x,y] in self.places: pygame.draw.ellipse(self.surface,(10,10,10),self.grid[y][x][0],3)
				bw = not bw
			bw = not bw
		
		return self.surface

class Blackgammon:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 8)
		self.grid = []
		for y in (1,0):
			if y == 1: rr = range(13)[::-1]
			if y == 0: rr = range(13)
			for x in rr:
				if x != 6:
					self.grid.append([pygame.Rect(50 + (x * 40), 50 + (y * 460), 40, 40), 0, 0])
		self.grid[12][1] = 1; self.grid[12][2] = 5
		self.grid[16][1] = 2; self.grid[16][2] = 3
		self.grid[18][1] = 2; self.grid[18][2] = 5
		self.grid[23][1] = 1; self.grid[23][2] = 2
		self.grid[11][1] = 2; self.grid[11][2] = 5
		self.grid[7][1] = 1; self.grid[7][2] = 3
		self.grid[5][1] = 1; self.grid[5][2] = 5
		self.grid[0][1] = 2; self.grid[0][2] = 2
		self.places = []
		self.turn = -2
		self.dice = [0,0]
		self.score = [0,0]
		self.walk = []
		self.time = 0
		self.opt = -1
		self.values = [
			[(25,25)],
			[(10,10),(40,40)],
			[(10,10),(25,25),(40,40)],
			[(10,10),(40,10),(10,40),(40,40)],
			[(10,10),(40,10),(25,25),(10,40),(40,40)],
			[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]
		]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.score[0] == 15: self.__init__()
			if self.score[1] == 15: self.__init__()
			if self.time == 0 and self.walk == []: self.time += 1
			if self.turn >= 0:
				for i in range(len(self.grid)):
					if pygame.Rect.colliderect(mouse,self.grid[i][0]) and self.grid[i][1] == self.turn + 1:
						do = 0
						if self.turn == 0: ww = i - self.walk[0]
						if self.turn == 1: ww = i + self.walk[0]
						if ww < 24 and ww >= 0:
							if self.grid[ww][1] in [0,self.turn + 1]: do = 1
							elif self.grid[ww][2] == 1: do = 1; self.grid[ww][2] = 0
						elif self.turn == 0 and ww < 0: do = 2
						elif self.turn == 1 and ww >= 24: do = 3
						if do > 0:
							self.grid[i][2] -= 1
							if self.grid[i][2] == 0: self.grid[i][1] = 0
							if do == 1: self.grid[ww][1] = self.turn + 1; self.grid[ww][2] += 1
							if do == 2: self.score[0] += 1
							if do == 3: self.score[1] += 1
							del self.walk[0]
							if self.walk == []: self.turn = int(not self.turn)
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		pygame.draw.rect(self.surface,(100,50,10),pygame.Rect(50,50,560,500))
		for i in range(13): pygame.draw.polygon(self.surface,(150,150,150),((50 + (i * 40),50),(90 + (i * 40),50),(70 + (i * 40),250)))
		for i in range(13): pygame.draw.polygon(self.surface,(150,150,150),((50 + (i * 40),550),(90 + (i * 40),550),(70 + (i * 40),350)))
		pygame.draw.line(self.surface,(0,0,0),(310,50),(310,550),40)

		for i in range(len(self.grid)):
			self.surface.blit(self.font.render(str(i),1,(200,200,200)), (self.grid[i][0].x,self.grid[i][0].y))
			if self.grid[i][1] > 0:
				if self.grid[i][1] == 1: cc = (200,200,200)
				if self.grid[i][1] == 2: cc = (10,10,10)
				for t in range(self.grid[i][2]):
					if i < 12: yy = -40
					else: yy = 40
					pygame.draw.ellipse(self.surface,cc,pygame.Rect(self.grid[i][0].x + 5,self.grid[i][0].y + 5 + (t * yy),self.grid[i][0].width - 10,self.grid[i][0].height - 10))
		for i in range(2):
			for j in range(self.score[i]):
				if i == 0: pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(560,520 - (j * 12),30,10))
				if i == 1: pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(560,50 + (j * 12),30,10))
		
		if self.time >= 1:
			self.time += 1
			if self.time%5 == 0:
				if self.turn < 0: self.dice[self.turn + 2] = np.random.randint(1,7)
				else:
					for i in range(2): self.dice[i] = np.random.randint(1,7)
		if self.time > 120:
			self.time = 0
			if self.turn < 0:
				if self.turn == -2:
					self.turn += 1
				else:
					if self.dice[0] >= self.dice[1]: self.turn = 0
					if self.dice[0] < self.dice[1]: self.turn = 1
			elif self.dice[0] == self.dice[1]:
				for i in range(4): self.walk.append(self.dice[0])
			else: self.walk = self.dice.copy()
		for i in range(2):
			srf = pygame.Surface((50,50))
			srf.fill((210,220,200))
			for d in self.values[self.dice[i] - 1]:
				pygame.draw.circle(srf,(10,10,10),d,5)
			self.surface.blit(srf,(300 + (i * 60),700))
		
		return self.surface

class Ludo:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 8)
		self.grid = []
		for y in range(15):
			self.grid.append([])
			for x in range(15):
				do = False
				if y in [6,7,8]: do = True
				elif x in [6,7,8]: do = True
				if do: self.grid[y].append([pygame.Rect(50 + (x * 41), 50 + (y * 41), 40, 40), 0, 0])
		self.places = []
		self.turn = 0
		self.dice = 0
		self.walk = 0
		self.time = 0
		self.opt = -1
		self.players = [[37,None,None,None],[24,None,None,None],[11,None,None,None],[50,None,None,None]]
		self.starts = [37,24,11,50]
		self.finish = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
		self.values = [
			[(25,25)],
			[(10,10),(40,40)],
			[(10,10),(25,25),(40,40)],
			[(10,10),(40,10),(10,40),(40,40)],
			[(10,10),(40,10),(25,25),(10,40),(40,40)],
			[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]
		]
		self.path = [[1,14],[2,14],[2,13],[2,12],[2,11],[2,10],[2,9],[9,8],[10,8],[11,8],[12,8],[13,8],[14,8],
			[14,7],[14,6],[13,6],[12,6],[11,6],[10,6],[9,6],[2,5],[2,4],[2,3],[2,2],[2,1],[2,0],
			[1,0],[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[5,6],[4,6],[3,6],[2,6],[1,6],[0,6],
			[0,7],[0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14]]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.time == 0 and self.opt == -1: self.time += 1
			if self.opt == 4:
				self.players[self.turn][len([i for i in self.players[self.turn] if i != None])] = self.starts[self.turn]
				self.opt = -1
				self.turn += 1
				if self.turn > 3: self.turn = 0
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						for p in range(4):
							if self.players[self.turn][p] != None and [x,y] == self.path[self.players[self.turn][p]]:
								if self.opt == 5: self.walk = 20
								else: self.walk = (self.dice) * 10
								self.opt = p
	
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		plst = [0,1,3,2]
		clst = [(100,200,100),(200,100,100),(100,200,200),(200,200,100),(200,200,200)]
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if y == 7 and x in [1,2,3,4,5]: cc = 0
				elif y == 6 and x == 1: cc =0
				elif y == 7 and x in [9,10,11,12,13]: cc = 3
				elif y == 8 and x == 13: cc = 3
				elif x == 1 and y in [1,2,3,4,5]: cc = 1
				elif y == 1 and x == 2: cc = 1
				elif x == 1 and y in [9,10,11,12,13]: cc = 2
				elif y == 13 and x == 0: cc = 2
				else: cc = 4
				pygame.draw.rect(self.surface,clst[cc],self.grid[y][x][0])
				for i in range(len(plst)):
					for p in range(len(plst)):
						if self.finish[plst[i]][plst[p]] != None: pass
						elif self.players[plst[i]][plst[p]] != None and [x,y] == self.path[self.players[plst[i]][plst[p]]]:
							if self.opt not in [-1,4] and self.turn == plst[i]: pygame.draw.rect(self.surface,(0,200,0),self.grid[y][x][0])
							pygame.draw.ellipse(self.surface,(10,10,10),pygame.Rect(self.grid[y][x][0].x + 5,self.grid[y][x][0].y + 5,self.grid[y][x][0].width - 10,self.grid[y][x][0].height - 10))
							pygame.draw.ellipse(self.surface,clst[i],pygame.Rect(self.grid[y][x][0].x + 10,self.grid[y][x][0].y + 10,self.grid[y][x][0].width - 20,self.grid[y][x][0].height - 20))
		plg = [[(295,295),(295,418)],[(295,295),(418,295)],[(418,295),(418,418)],[(295,418),(418,418)]]
		for i in range(len(plst)):
			pygame.draw.rect(self.surface,clst[i],pygame.Rect(50 + (368 * (i - (2 * np.floor(i/2)))), 50 + (368 * np.floor(i/2)), 246, 246))
			pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(100 + (368 * (i - (2 * np.floor(i/2)))), 100 + (368 * np.floor(i/2)), 146, 146))
			pygame.draw.polygon(self.surface,clst[i],(plg[plst[i]][0],plg[plst[i]][1],(355,355)))
			for j in range(len(self.players[plst[i]])):
				if self.players[plst[i]][j] == None:
					pygame.draw.ellipse(self.surface,(10,10,10),pygame.Rect(120 + (368 * (i - (2 * np.floor(i/2)))) + (80 * (j - (2 * np.floor(j/2)))),120 + (368 * np.floor(i/2)) + (80 * np.floor(j/2)),30,30))
					pygame.draw.ellipse(self.surface,clst[i],pygame.Rect(125 + (368 * (i - (2 * np.floor(i/2)))) + (80 * (j - (2 * np.floor(j/2)))),125 + (368 * np.floor(i/2)) + (80 * np.floor(j/2)),20,20))
		if self.time >= 1:
			self.time += 1
			if self.time%5 == 0: self.dice = np.random.randint(1,7)
		if self.time > 120:
			self.time = 0
			if self.dice == 5 and self.players[self.turn][-1] == None: self.opt = 4
			elif self.dice == 6: self.opt = 6
			else: self.opt = 0
		if self.walk > 0:
			if self.walk%10 == 0:
				if self.finish[self.turn][self.opt] == None:
					self.players[self.turn][self.opt] += 1
					if self.players[self.turn][self.opt] >= len(self.path): self.players[self.turn][self.opt] = 0
					if self.players[self.turn][self.opt] == self.starts[self.turn]: self.finish[self.turn][self.opt] = 0
				else:
					self.finish[self.turn][self.opt] += 1
					if self.finish[self.turn][self.opt] > 6: self.finish[self.turn][self.opt] = 6
			self.walk -= 1
			if self.walk <= 0:
				for p in range(len(self.players)):
					if p != self.turn:
						for pp in range(len(self.players[p])):
							if self.players[p][pp] == self.players[self.turn][self.opt]:
								self.players[p][pp] = None
								self.opt = 5
				if self.opt not in [5,6]:
					self.opt = -1
					self.turn += 1
					if self.turn > 3: self.turn = 0
		srf = pygame.Surface((50,50))
		srf.fill((210,220,200))
		for d in self.values[self.dice - 1]:
			pygame.draw.circle(srf,(10,10,10),d,5)
		self.surface.blit(srf,(400,700))
		
		return self.surface

class Reversi:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(8):
			self.grid.append([])
			for x in range(8):
				self.grid[y].append([pygame.Rect(50 + (x * 41), 50 + (y * 41), 40, 40), 0])
		self.grid[3][3][1] = 1
		self.grid[3][4][1] = 2
		self.grid[4][3][1] = 2
		self.grid[4][4][1] = 1
		self.piece = [None,None]
		self.turn = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						if self.piece == [None,None]:
							if self.grid[y][x][1] == self.turn + 1:
								self.piece = [x,y]
						else:
							if x == self.piece[0] and y == self.piece[1]: self.piece = [None,None]
							for fy in [-1,0,1]:
								for fx in [-1,0,1]:
									for ss in range(2,6):
										try:
											if x == self.piece[0] + (fx * ss) and y == self.piece[1] + (fy * ss):
												if self.grid[y][x][1] == 0:
													if self.turn == 0: tt = 1
													if self.turn == 1: tt = 0
													if self.grid[self.piece[1] + (fy * (ss - 1))][self.piece[0] + (fx * (ss - 1))][1] not in [0,tt]:
														for n in range(ss + 1):
															self.grid[self.piece[1] + (fy * n)][self.piece[0] + (fx * n)][1] = self.turn + 1
														self.piece = [None,None]
														self.turn += 1
														if self.turn > 1: self.turn = 0
										except: pass
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.piece == [x,y]: pygame.draw.rect(self.surface,(100,200,100),self.grid[y][x][0])
				else: pygame.draw.rect(self.surface,(100,100,100),self.grid[y][x][0])
				if self.grid[y][x][1] == 1: pygame.draw.ellipse(self.surface,(200,200,200),self.grid[y][x][0])
				if self.grid[y][x][1] == 2: pygame.draw.ellipse(self.surface,(10,10,10),self.grid[y][x][0])
		
		return self.surface

class SnakesNLadders:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 15)
		self.grid = []
		for y in range(30):
			self.grid.append([])
			for x in range(10):
				self.grid[y].append([pygame.Rect(10 + (x * 22), 50 + (y * 22), 20, 20), None, 0])
		self.turn = 0
		self.time = 0
		self.dice = 0
		self.values = [
			[(25,25)],
			[(10,10),(40,40)],
			[(10,10),(25,25),(40,40)],
			[(10,10),(40,10),(10,40),(40,40)],
			[(10,10),(40,10),(25,25),(10,40),(40,40)],
			[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]
		]
		self.pawns = [1,1]
		self.walk = 0
		self.snakes = {12:8,99:57,55:45,73:69,52:33}
		self.ladders = {3:38,36:48,74:88,60:62,31:66}
		self.pos = {}
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.pawns:
				if i >= 99: self.__init__()
			if self.time == 0: self.time += 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		bw = False
		way = 1
		for y in range(10):
			for x in range(10):
				if bw: cc = (100,100,200)
				else: cc = (200,200,100)
				if way == 1: vl = (x + (y * 10)) + 1
				else: vl = ((y * 10) + 9 - x) + 1
				pygame.draw.rect(self.surface,cc,pygame.Rect(20 + (x * 30),320 - (y * 30),30,30))
				self.surface.blit(self.font.render(str(vl),1,(10,10,10)), (22 + (x * 30),322 - (y * 30)))
				for i in range(len(self.pawns)):
					if i == 0: cc = (200,100,100)
					else: cc = (100,200,100)
					if self.pawns[np.floor(i).astype(int)] == vl: pygame.draw.ellipse(self.surface,cc,pygame.Rect(25 + (x * 30),325 - (y * 30),20,20))
				self.pos[vl] = [30 + (x * 30),330 - (y * 30)]
				bw = not bw
			bw = not bw
			way = -way
		way = 1
		for y in range(10):
			for x in range(10):
				if way == 1: vl = (x + (y * 10)) + 1
				else: vl = ((y * 10) + 9 - x) + 1
				if vl in self.snakes: pygame.draw.line(self.surface,(10,200,10),(30 + (x * 30),330 - (y * 30)),self.pos[self.snakes[vl]],10)
				if vl in self.ladders: pygame.draw.line(self.surface,(200,10,10),(30 + (x * 30),330 - (y * 30)),self.pos[self.ladders[vl]],10)
			way = -way
		if self.time >= 1:
			self.time += 1
			if self.time%5 == 0: self.dice = np.random.randint(1,7)
		if self.time > 120:
			self.time = 0
			self.walk = (self.dice) * 10
		if self.walk > 0:
			if self.walk%10 == 0: self.pawns[self.turn] += 1
			self.walk -= 1
			if self.walk <= 0:
				if self.pawns[self.turn] in self.snakes: self.pawns[self.turn] = self.snakes[self.pawns[self.turn]]
				if self.pawns[self.turn] in self.ladders: self.pawns[self.turn] = self.ladders[self.pawns[self.turn]]
				self.turn = int(not self.turn)
		srf = pygame.Surface((50,50))
		srf.fill((210,220,200))
		for d in self.values[self.dice - 1]:
			pygame.draw.circle(srf,(10,10,10),d,5)
		self.surface.blit(srf,(200,350))
		
		return self.surface

#SOLITAIRE GAMING
class SpiderSolitaire:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.sft = pygame.font.SysFont("Arial", 22)
		self.cards = []
		self.table = [[],[],[],[],[],[],[],[],[],[]]
		self.mount = []
		self.drgdrp = [None,None]
		nb = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
		for n in nb:
			srf = pygame.Surface((70,100))
			srf.fill((240,240,240))
			srf.blit(self.sft.render(n,True,(10,10,10)),(5,5))
			srf.blit(self.sft.render(n,True,(10,10,10)),(45,75))
			self.cards.append(srf)
		for i in range(8):
			for n in range(len(nb)): self.mount.append(n)
		for i in range(5):
			for n in self.table:
				rr = np.random.randint(0,len(self.mount))
				n.append(self.mount[rr])
				del self.mount[rr]
		self.mrct = pygame.Rect(20,50,70,100)
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.drgdrp != [None,None]:
				if self.table[np.floor((mr.x - 100)/80).astype(int)] == [] or self.table[self.drgdrp[0]][self.drgdrp[1]] == self.table[np.floor((mr.x - 100)/80).astype(int)][-1] - 1:
					for i in self.table[self.drgdrp[0]][self.drgdrp[1]:]:
						self.table[np.floor((mr.x - 100)/80).astype(int)].append(i)
					del self.table[self.drgdrp[0]][self.drgdrp[1]:]
				self.drgdrp = [None,None]
				chk = 12
				stt = -1
				for i in range(len(self.table[np.floor((mr.x - 100)/80).astype(int)])):
					if self.table[np.floor((mr.x - 100)/80).astype(int)][i] == chk:
						if stt == -1: stt = i
						chk -= 1
					else: chk = 12; stt = -1
				if chk < 0: del self.table[np.floor((mr.x - 100)/80).astype(int)][stt:]
		if pressed[4][0]:
			if len(self.mount) > 0 and pygame.Rect.colliderect(mouse,self.mrct):
				for n in self.table:
					rr = np.random.randint(0,len(self.mount))
					n.append(self.mount[rr])
					del self.mount[rr]
			for i in range(len(self.table)):
				for j in range(len(self.table[i])):
					if pygame.Rect.colliderect(mouse,pygame.Rect(100 + (i * 80),50 + (j * 30),70,100)):
						self.drgdrp = [i,j]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((10,200,100))
		if len(self.mount) > 0: pygame.draw.rect(self.surface,(200,10,10),self.mrct)
		for i in range(len(self.table)):
			for j in range(len(self.table[i])):
				if i != self.drgdrp[0] or j < self.drgdrp[1]: self.surface.blit(self.cards[self.table[i][j]],(100 + (i * 80),50 + (j * 30)))
		if self.drgdrp != [None,None]:
			mp = pygame.mouse.get_pos()
			for i in range(len(self.table[self.drgdrp[0]][self.drgdrp[1]:])):
				self.surface.blit(self.cards[self.table[self.drgdrp[0]][self.drgdrp[1]:][i]],(mp[0] - 20,mp[1] - 20 + (i * 30)))

		return self.surface

class Mahjong:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.blocks = []
		self.select = []
		bbs = []
		for i in range(4): bbs += [0,1,2,3]
		for z in range(2):
			self.blocks.append([])
			for y in range(2):
				self.blocks[z].append([])
				for x in range(4):
					rr = np.random.randint(0,len(bbs))
					self.blocks[z][y].append([pygame.Rect(150 + (x * 45) + (z * 20), 150 + (y * 65) + (z * 30), 40, 60), bbs[rr], 0])
					del bbs[rr]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for z in range(len(self.blocks)):
				for y in range(len(self.blocks[z])):
					for x in range(len(self.blocks[z][y])):
						el = self.blocks[z][y][x]
						if el != None and pygame.Rect.colliderect(mouse,el[0]):
							if self.select != []:
								cp = self.blocks[self.select[0]][self.select[1]][self.select[2]]
								if el != cp and el[1] == cp[1]:
									self.blocks[z][y][x] = None
									self.blocks[self.select[0]][self.select[1]][self.select[2]] = None
									self.select = []
								else: self.select = [z,y,x]
							else: self.select = [z,y,x]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		#self.surface.blit(self.font.render(self.txt,1,(200,200,200)), (10,10))

		cc = [(200,100,100),(200,200,100),(100,200,100),(100,100,200)]
		for z in range(len(self.blocks)):
			for y in range(len(self.blocks[z])):
				for x in range(len(self.blocks[z][y])):
					el = self.blocks[z][y][x]
					if el != None:
						if self.select == [z,y,x]: pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(el[0].x - 2,el[0].y - 2,el[0].width + 4,el[0].height + 4))
						pygame.draw.rect(self.surface,cc[el[1]],el[0])
		
		return self.surface

class PegSolitaire:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(7):
			self.grid.append([])
			for x in range(7):
				self.grid[y].append([pygame.Rect(50 + (x * 41), 50 + (y * 41), 40, 40), 1])
		self.grid[3][3][1] = 0
		self.piece = [None,None]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for y in range(len(self.grid)):
				for x in range(len(self.grid[y])):
					if pygame.Rect.colliderect(mouse,self.grid[y][x][0]):
						if self.piece == [None,None]:
							if self.grid[y][x][1] == 1:
								self.piece = [x,y]
						else:
							if x == self.piece[0] and y == self.piece[1]: self.piece = [None,None]
							for fy in [-1,0,1]:
								for fx in [-1,0,1]:
									go = False
									if y in [2,3,4]: go = True
									elif x not in [0,1,5,6]: go = True
									if go and self.grid[y][x][1] == 0 and abs(fx) != abs(fy):
										if x == self.piece[0] + (fx * 2) and y == self.piece[1] + (fy * 2):
											if self.grid[self.piece[1] + fy][self.piece[0] + fx][1] == 1:
												self.grid[self.piece[1]][self.piece[0]][1] = 0
												self.grid[self.piece[1] + fy][self.piece[0] + fx][1] = 0
												self.grid[y][x][1] = 1
												self.piece = [None,None]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				go = False
				if y in [2,3,4]: go = True
				elif x not in [0,1,5,6]: go = True
				if go:
					if self.piece == [x,y]: pygame.draw.rect(self.surface,(200,100,100),self.grid[y][x][0])
					if self.grid[y][x][1] == 0: pygame.draw.ellipse(self.surface,(200,200,200),self.grid[y][x][0])
					if self.grid[y][x][1] == 1: pygame.draw.ellipse(self.surface,(100,200,100),self.grid[y][x][0])
		
		return self.surface

#CARD GAMING
class Dominoes:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.dominoes = []
		self.values = [
			[()],
			[(25,25)],
			[(10,10),(40,40)],
			[(10,10),(25,25),(40,40)],
			[(10,10),(40,10),(10,40),(40,40)],
			[(10,10),(40,10),(25,25),(10,40),(40,40)],
			[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]
		]
		for i in range (7):
			for j in range(7):
				srf = pygame.Surface((50,100))
				srf.fill((210,220,200))
				pygame.draw.line(srf,(10,10,10),(5,50),(45,50),3)
				for d in self.values[i]:
					if d != ():
						pygame.draw.circle(srf,(10,10,10),d,5)
				for d in self.values[j]:
					if d != ():
						pygame.draw.circle(srf,(10,10,10),(d[0],d[1] + 50),5)
				self.dominoes.append([srf,(i,j)])
		np.random.shuffle(self.dominoes)
		self.hands = [self.dominoes[0:12],self.dominoes[12:24],self.dominoes[24:36],self.dominoes[36:48]]
		self.dominoes[48][0] = pygame.transform.rotate(self.dominoes[48][0],90)
		self.tree = [self.dominoes[48]]
				
		self.font = pygame.font.SysFont("Arial", 64)
		self.score = [0,0,0,0]
		self.mode = 1
		self.turn = 0
		self.mn = 0
			
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.turn == 0:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			x = 0
			for i in self.hands[self.turn]:
				print(self.hands[0])
				print('-------')
				print(self.tree)
				if pygame.Rect.colliderect(mouse,pygame.Rect(10 + (x * 55),1000,50,100)):
					if i[1][0] == self.tree[0][1][0]:
						if i[1][0] != i[1][1]:
							i[0] = pygame.transform.rotate(i[0],270)
						self.tree.insert(0,i)
						del self.hands[self.turn][x]
					elif i[1][1] == self.tree[0][1][0]:
						if i[1][0] != i[1][1]:
							i[0] = pygame.transform.rotate(i[0],90)
						self.tree.insert(0,i)
						del self.hands[self.turn][x]
					elif i[1][0] == self.tree[len(self.tree) - 1][1][1]:
						if i[1][0] != i[1][1]:
							i[0] = pygame.transform.rotate(i[0],90)
						self.tree.append(i)
						del self.hands[self.turn][x]
					elif i[1][1] == self.tree[len(self.tree) - 1][1][1]:
						if i[1][0] != i[1][1]:
							i[0] = pygame.transform.rotate(i[0],270)
						self.tree.append(i)
						del self.hands[self.turn][x]
				x += 1
			
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((10,200,100))
		
		for i in range(len(self.hands)):
			for j in range(len(self.hands[i])):
				if i == 0: pos = (10 + (j * 55),1000)
				if i == 1: pos = (600,300 + (j * 55))
				if i == 2: pos = (10 + (j * 55),10)
				if i == 3: pos = (10,300 + (j * 55))
				self.surface.blit(pygame.transform.rotate(self.hands[i][j][0],i * 90),pos)
		
		x = 0
		for i in self.tree:
			if i[1][0] == i[1][1]:
				self.surface.blit(i[0],(100 + x,475))
				x += 55
			else:
				self.surface.blit(i[0],(100 + x,500))
				x += 105
			
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]) + ' - ' + str(self.score[2]) + ' - ' + str(self.score[3]),1,(200,200,200)), (10,10))
			
		return self.surface

class Sueca:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.sft = pygame.font.SysFont("Arial", 22)
		self.score = [0,0]
		self.time = 0
		self.turn = 0
		self.cards = []
		self.table = []
		self.deck = []
		self.ww = None
		lp = ('C','O','E','P')
		lb = ('2','3','4','5','6','Q','J','K','7','A')
		for p in range(4):
			self.cards.append([])
			for n in range(len(lb)):
				if p < 2: cl = (240,10,10)
				else: cl = (10,10,10)
				srf = pygame.Surface((70,100),pygame.SRCALPHA)
				srf.fill((240,240,240))
				srf.blit(self.sft.render(lb[n],True,cl),(5,5))
				#srf.blit(pygame.image.load('minigames/cardfront.png'),(0,0))
				#srf.blit(pygame.image.load('minigames/suit' + str(p - 1) + '.png'),(5,40))
				srf.blit(self.sft.render(lb[n],True,cl),(5,5))
				srf.blit(self.sft.render(lb[n],True,cl),(45,75))
				self.cards[p].append(srf)
				self.deck.append([n,p])
		for i in range(7): np.random.shuffle(self.deck)
		self.trunfo = self.deck[-1][1]
		self.deck = [self.deck[0:10],self.deck[10:20],self.deck[20:30],self.deck[30:40]]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.time == 0:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			if self.turn == 0:
				for i in range(len(self.deck[0])):
					if pygame.Rect.colliderect(mouse,pygame.Rect(20 + (i * 72),360,70,100)):
						do = False
						if len(self.table) == 0: do = True
						elif [i for i in self.deck[self.turn] if i[1] == self.table[0][1]] == []: do = True
						elif self.deck[self.turn][i][1] == self.table[0][1]: do = True
						if do:
							self.table.append([self.deck[self.turn][i],self.turn])
							del self.deck[self.turn][i]
							self.turn += 1
							self.time = 60
		
	def outside_events(self,pressed): pass

	def draw(self):
		if self.time > 0: self.time -= 1
		if len(self.table) == 4:
			if self.time == 120:
				pp = [i for i in self.table if i[0][1] == self.table[0][0][1] or i[0][1] == self.trunfo]
				ss = sorted(((v[0], v[1]) for v in pp), reverse=True)
				print('-----------------------')
				print(pp)
				print(ss)
				print(ss[0][1])
				if ss[0][0] == 9: vv = 11
				elif ss[0][0] == 8: vv = 10
				elif ss[0][0] == 7: vv = 4
				elif ss[0][0] == 6: vv = 3
				elif ss[0][0] == 5: vv = 2
				else: vv = 0
				self.ww = ss[0][1]
				self.score[(self.ww + 2)%2] += vv
				self.turn = self.ww
			if self.time == 0:
				self.table = []
				if self.turn != 1: self.time = 60
		elif self.turn != 0 and self.time == 0:
			do = False
			if self.table != []: print('NAIPE: '+str(self.table))
			rr = np.random.randint(0,len(self.deck[self.turn]))
			if len(self.table) == 0: do = True
			elif [i for i in self.deck[self.turn] if i[1] == self.table[0][1]] == []: do = True
			else:
				rr = 0
				while rr < len(self.deck[self.turn]) and do == False:
					if self.deck[self.turn][rr][1] == self.table[0][1]: do = True
					else: do += 1
			if do:
				self.table.append([self.deck[self.turn][rr],self.turn])
				del self.deck[self.turn][rr]
				self.turn += 1
				if self.turn > 3: self.turn = 0
				if len(self.table) != 4: self.time = 60
				else: self.time = 121
		self.surface.fill((10,200,100))
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(10,10,10)), (10,10))
		self.surface.blit(self.font.render('TRUNFO: ' + str(self.trunfo),1,(10,10,10)), (10,10))
		for i in range(len(self.table)):
			if len(self.table) == 4 and i == self.ww: pygame.draw.rect(self.surface,(200,200,100),pygame.Rect(15 + (i * 80),45,80,110))
			self.surface.blit(self.cards[self.table[i][0][1]][self.table[i][0][0]],(20 + (i * 80),50))
		for i in range(len(self.deck[0])):
			self.surface.blit(self.cards[self.deck[0][i][1]][self.deck[0][i][0]],(20 + (i * 72),360))

		return self.surface

class Copas:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.sft = pygame.font.SysFont("Arial", 22)
		self.score = 0
		self.time = 100
		self.match = [0,0]
		self.cards = []
		
		nb = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
		for p in range(4):
			for n in nb:
				if p < 2: cl = (240,10,10)
				else: cl = (10,10,10)
				srf = pygame.Surface((70,100))
				srf.fill((240,240,240))
				srf.blit(self.sft.render(n,True,cl),(5,5))
				srf.blit(pygame.image.load('Sprites/np_' + str(p) + '.png'),(25,40))
				srf.blit(self.sft.render(n,True,cl),(45,75))
				self.cards.append(srf)
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0] and self.time == 0:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if i[2] == 0:
					if pygame.Rect.colliderect(mouse,i[0]):
						if self.match[0] == 0:
							self.match[0] = i[1]
						else: self.match[1] = i[1]
						i[2] = 1
						break
			if self.match[0] != 0 and self.match[1] != 0:
				for i in self.buttons:
					if i[1] in self.match:
						if self.match[0] != self.match[1] and i[2] == 1:
							self.time = 30
							i[2] = 2
				self.match = [0,0]
			q = 0
			for i in self.buttons:
				if i[2] == 1: q += 1
			if q == len(self.buttons):
				self.score += 1
				self.time = 100
				self.shuffle()
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.time > 0: self.time -= 1
		c = 0
		for x in range(4):
			for y in range(13):
				self.surface.blit(self.cards[c],(x * 72,y * 102))
				c += 1
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

#WORD GAMING
class Matchingwords:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 40)
		
		letters = []
		for i in 'abcdefghijklmnopqrstuvwxyz':
			letters.append(i)
		x = 0
		self.buttons = []
		for i in range(3):
			for j in range(10):
				if x >= len(letters): break
				self.buttons.append([pygame.Rect(20 + (j * 60), 800 + (i * 60),50,50),letters[x]])
				x += 1
		self.level = [
			[0,'B','A','B','O','S','E','I','R','A'],
			['C','A','S','A',15,10,'N',4,2,'U'],
			[1,'U',7,'P','A','S','C','O','A','L'],
			[3,'D',8,'C','E','G','O','N','H','A'],
			[' ','U','A','U','R','S','S','Ç','N',11],
			[' ','C','A','B','E','S','T','A','A','G'],
			[' ','O','A','L','O','S','O',12,'R','A'],
			[' ',13,'A','I',14,'E','D','R','A','T'],
			[5,'B','A','C','O','N',' ','E',9,'O'],
			['S','O','L',6,'C','A','R','T','A','S'],
		]
		self.words = [
			['BABOSEIRA','Tolice, coisa pouca.',[1,0],[9,0]],
			['CASA','Onde os peões estão no tabuleiro.',[0,1],[3,1]],
			['AULA','O que o professor faz.',[9,0],[9,3]],
			['BAUDUCO','Marca brasileira de biscoitos.',[1,0],[1,9]],
			['ENCONSTO','Segundo a espiritualidade, uma entidade maligna.',[6,0],[6,7]],
			['SOL','Quinta nota da escala de dó.',[0,9],[2,9]],
			['CARTAS','Comunicação por escrito (pl.)',[4,9],[9,9]],
			['PASCOAL','Hernesto (?), músico brasileiro.',[3,2],[9,2]],
			['CEGONHA','Segundo a lenda, ela traz os bebês em uma bolsa.',[3,3],[9,3]],
			['ARANHA','Ela é teimosa e desobediente (folc.)',[8,7],[8,2]],
			['ONÇA','Amigo da (?), pessoa desleal.',[7,2],[7,5]],
			['GATOS','Animais domésticos e populares.',[9,5],[9,9]],
			['TER','Verbo possessivo no infinitivo.',[7,9],[7,7]],
			['BACON','Carne de porco usada em lanches.',[1,8],[5,8]],
			['TARDE','O período entre o meio-dia e as 6h PM.',[9,7],[5,7]],
			['AEREO','Relativo ao ar.',[4,2],[4,6]],
		]
		self.grid = []
		for y in range(len(self.level)):
			self.grid.append([])
			for x in range(len(self.level[y])):
				if isinstance(self.level[y][x],int): pp = self.level[y][x]
				else: pp = ''
				self.grid[y].append([pygame.Rect(50 + (x * 41),50 + (y * 41),40,40),pp])
		self.ltt = 'A'
		self.hint = None
		self.time = 0
			
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if pygame.Rect.colliderect(mouse,i[0]):
					self.ltt = i[1].upper()
			for y in self.grid:
				for x in y:
					if pygame.Rect.colliderect(mouse,x[0]):
						if isinstance(x[1],int): self.hint = x[1]
						else: x[1] = self.ltt
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		
		if self.time > 0: self.time -= 1
		if self.time == 1: pass

		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if isinstance(self.grid[y][x][1],int): pygame.draw.rect(self.surface,(10,10,10),self.grid[y][x][0])
				elif self.level[y][x] != ' ':
					if self.grid[y][x][1] != '' and self.grid[y][x][1] != self.level[y][x]: cc = (200,100,100)
					else: cc = (200,200,200)
					pygame.draw.rect(self.surface,cc,self.grid[y][x][0])
					self.surface.blit(self.font.render(self.grid[y][x][1],1,(10,10,10)),(self.grid[y][x][0].x + 5,self.grid[y][x][0].y + 1))
		if self.hint != None: self.surface.blit(self.font.render(self.words[self.hint][1],1,(200,200,200)),(50,600))
		for i in self.buttons:
			if self.ltt == i[1].upper(): cc = (100,200,100)
			else: cc = (200,200,200)
			self.surface.blit(self.font.render(i[1],1,cc),(i[0].x + 5,i[0].y))
		
		return self.surface

class TicTacToe:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.buttons = []
		for x in range (3):
			for y in range(3):
				self.buttons.append([pygame.Rect(100 + (x * 100), 200 + (y * 100),90,90),0])
		self.font = pygame.font.SysFont("Arial", 64)
		self.score = [0,0]
		self.mode = 1
		self.turn = 1
			
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			grd = []
			pl = []
			if self.turn == 3:
				for i in self.buttons: i[1] = 0
			for i in self.buttons:
				if i[1] == 0 and self.turn < 3:
					if pygame.Rect.colliderect(mouse,i[0]):
						i[1] = self.turn
						break
			if self.mode == 0:
				x = 0
				for i in self.buttons:
					if i[1] == 0:
						pl.append(x)
					x += 1
				if len(pl) > 0:
					ch = np.random.randint(0,len(pl))
					self.buttons[pl[ch]][1] = 2
			if self.mode == 1:
				if self.turn == 1: self.turn = 2
				else: self.turn = 1
			
			wn = 0
			for i in self.buttons: grd.append(i[1])
			for p in (1,2):
				if [p,p,p] == [grd[0],grd[1],grd[2]]: wn = p
				if [p,p,p] == [grd[3],grd[4],grd[5]]: wn = p
				if [p,p,p] == [grd[6],grd[7],grd[8]]: wn = p
				if [p,p,p] == [grd[0],grd[3],grd[6]]: wn = p
				if [p,p,p] == [grd[1],grd[4],grd[7]]: wn = p
				if [p,p,p] == [grd[2],grd[5],grd[8]]: wn = p
				if [p,p,p] == [grd[0],grd[4],grd[8]]: wn = p
				if [p,p,p] == [grd[2],grd[4],grd[6]]: wn = p
			
			b = 0
			for i in self.buttons:
				if i[1] != 0: b += 1
			if b == len(self.buttons): wn = 3
			if wn == 1: self.score[0] += 1
			if wn == 2: self.score[1] += 1
			if wn != 0: self.turn = 3
			
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for x in range(2): pygame.draw.line(self.surface,(200,200,200),(195 + (x * 100),195),(195 + (x * 100),495),3)
		for y in range(2): pygame.draw.line(self.surface,(200,200,200),(95,295 + (y * 100)),(395,295 + (y * 100)),3)
		for i in self.buttons:
			pdd = 3
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			if pygame.Rect.colliderect(mouse,i[0]): pygame.draw.rect(self.surface,(50,50,50),i[0])
			if i[1] == 1:
				pygame.draw.line(self.surface,(200,200,200),(i[0].x + pdd,i[0].y + pdd),(i[0].x + i[0].width - (pdd * 2),i[0].y + i[0].height - (pdd * 2)),3)
				pygame.draw.line(self.surface,(200,200,200),(i[0].x + i[0].width - pdd,i[0].y + pdd),(i[0].x + pdd,i[0].y + i[0].height - (pdd * 2)),3)
			if i[1] == 2: pygame.draw.circle(self.surface,(200,200,200),(i[0].x + int(i[0].width/2),i[0].y + int(i[0].height/2)),int(i[0].width/2) - pdd,3)
		self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
			
		return self.surface

class LinesNBoxes:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 64)
		self.grid = []
		for y in range(20):
			for x in range(20):
				self.grid.append([x,y])
		self.piece = [None,None]
		self.places = []
		self.turn = 0
		self.lines = [[],[]]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			for i in self.grid:
				if pygame.Rect.colliderect(mouse,pygame.Rect(100 + (20 * i[0]),100 + (20 * i[1]),19,19)):
					if self.piece == [None,None]:
						self.piece = i.copy()
					elif i in [[self.piece[0] + x,self.piece[1] + y] for x in [-1,0,1] for y in [-1,0,1] if abs(x) != abs(y)]:
						self.lines[self.turn].append([self.piece,i.copy()])
						self.turn = int(not self.turn)
						self.piece = [None,None]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(80,80,420,420))
		for i in range(len(self.lines)):
			for j in self.lines[i]:
				if i == 0: cc = (200,100,100)
				elif i == 1: cc = (100,100,200)
				pygame.draw.line(self.surface,cc,(100 + (20 * j[0][0]),100 + (20 * j[0][1])),(100 + (20 * j[1][0]),100 + (20 * j[1][1])),5)
		for i in self.grid:
			if i == self.piece: pygame.draw.circle(self.surface,(10,10,10),(100 + (20 * i[0]),100 + (20 * i[1])),10)
			else: pygame.draw.circle(self.surface,(10,10,10),(100 + (20 * i[0]),100 + (20 * i[1])),5)
		
		return self.surface

class Nonogram:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 15)
		self.level = [
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
			[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		]
		self.grid = []
		for y in range(15):
			self.grid.append([])
			for x in range(15):
				self.grid[y].append([pygame.Rect(100 + (x * 41), 100 + (y * 41), 40, 40), self.level[y][x], 0])
		self.info = [[],[]]
		add = 0
		for y in range(len(self.level)):
			self.info[0].append([])
			for x in range(len(self.level[y])):
				if add > 0 and self.level[y][x] == 1: self.info[0][y].append(add); add = 0
				if self.level[y][x] == 2: add += 1
			if add > 0: self.info[0][y].append(add); add = 0
		add = 0
		for x in range(len(self.level)):
			self.info[1].append([])
			for y in range(len(self.level[x])):
				if add > 0 and self.level[y][x] == 1: self.info[1][x].append(add); add = 0
				if self.level[y][x] == 2: add += 1
			if add > 0: self.info[1][x].append(add); add = 0
		self.paint = False
		self.edit = False
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.MOUSEBUTTONUP: self.paint = False
		if pressed[4][0]: self.paint = True
		if event.type == pygame.KEYDOWN:
			if self.paint == False:
				self.level = [[1 for i in range(15)] for j in range(15)]
			self.paint = not self.paint
		if self.paint:
			for y in self.grid:
				for x in y:
					if pygame.Rect.colliderect(mouse,x[0]):
						if pygame.mouse.get_pressed()[0]: x[2] = 2
						if pygame.mouse.get_pressed()[2]: x[2] = 1
						if x[1] != x[2]: x[2] = 0
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		for i in range(len(self.info[0])):
			for j in range(len(self.info[0][i])):
				self.surface.blit(self.font.render(str(self.info[0][i][j]),1,(200,200,200)), (20 + (j * 20),120 + (i * 41)))
		for i in range(len(self.info[1])):
			for j in range(len(self.info[1][i])):
				self.surface.blit(self.font.render(str(self.info[1][i][j]),1,(200,200,200)), (120 + (i * 41),20 + (j * 20)))
		for y in self.grid:
			for x in y:
				if x[2] == 0: pygame.draw.rect(self.surface,(100,100,100),x[0])
				elif x[2] == 1: pygame.draw.rect(self.surface,(200,100,100),x[0])
				elif x[2] == 2: pygame.draw.rect(self.surface,(100,200,100),x[0])
		
		return self.surface

class HuntingWords:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 33)
		self.score = 0
		self.time = 1
		self.words = ['galinha','foca','gato','bola','fogão','geladeira','porta',
		'mesa','blusa','casa','óculos','cadeira','janela','lençol','luz','sol',
		'cachorro','mochila','travesseiro','carregador','telefone','televisão',
		'cesta','chapéu','igreja','padre','avião','vovó','chocolate','gelo',
		'barco','pessoa','olhos','interruptor','parede','vidro','garrafa',
		'banheiro','cozinha','quarto','caixa','mala','cobertor','short','dente',
		'nariz','coração','sobrancelhas']
		self.buttons = []
		self.grid = []
		self.match = ''
		self.index = []
		self.hold = 0
		for y in range(20):
			for x in range(20):
				self.buttons.append([pygame.Rect(10 + (x * 50),200 + (y * 50),50,50),0])
				self.grid.append('_')
		for i in range(10):
			t = np.random.randint(0,4)
			t = 1
			w = np.random.randint(0,len(self.words))
			while len(self.words[w]) >= 10:
				w = np.random.randint(0,len(self.words))
			s = np.random.randint(0,11 - len(self.words[w]))
			for l in range(len(self.words[w])):
				if t == 0:
					self.grid[i + s + (l * 10)] = self.words[w][l]
				if t == 1:
					self.grid[(i * 10) + s + l] = self.words[w][l]
				if t == 2:
					self.grid[(i * 10) + s + (l * 10)] = self.words[w][l]
		letters = 'abcdefghijklmnopqrstuvwxyz'
		for i in range(len(self.grid)):
			if self.grid[i] == '_':
				c = np.random.randint(0,len(letters))
				self.grid[i] = letters[c]
		
	def inside_events(self,pressed,mouse):
		if event.type == pygame.MOUSEBUTTONUP: self.hold = 0
		if pressed[4][0]: self.hold = 1
		if self.hold:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			v = 0
			for i in self.buttons:
				if pygame.Rect.colliderect(mouse,i[0]) and v not in self.index:
					self.match += self.grid[v]
					self.index.append(v)
				v += 1
		else:
			if self.match in self.words:
				for i in self.index: self.buttons[i][1] = 1
			self.match = ''
			self.index = []
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((200,200,200))
		
		l = 0
		for i in self.buttons:
			if i[1] == 0: c = (200,200,200)
			if i[1] == 1: c = (100,200,10)
			if l in self.index: c = (200,10,10)
			pygame.draw.rect(self.surface,c,i[0])
			self.surface.blit(self.font.render(self.grid[l],1,(10,10,10)), (i[0].x + 10,i[0].y + 5))
			l += 1
		
		self.surface.blit(self.font.render(str(self.score),1,(10,10,10)), (10,10))
		
		return self.surface

class Sudoku:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 20)
		self.smll = pygame.font.SysFont("Arial", 8)
		self.grid = []
		rows  = [g*3 + r for gr in np.random.sample([range(3),len(range(3))]) for g in gr for rr in np.random.sample([range(3),len(range(3))]) for r in rr] 
		cols  = [g*3 + c for gr in np.random.sample([range(3),len(range(3))]) for g in gr for cr in np.random.sample([range(3),len(range(3))]) for c in cr]
		nums  = random.sample(range(1,10),len(range(1,10)))
		brd = [[nums[(3*(r%3)+r//3+c)%9] for c in cols] for r in rows]
		spc = []
		for i in brd: spc.append(i.copy())
		for p in random.sample(range(81),81 * 3//4):
			spc[p//9][p%9] = None
		for ly in range(3):
			for y in range(3):
				self.grid.append([])
				for lx in range(3):
					for x in range(3):
						self.grid[y + (ly * 3)].append([pygame.Rect(50 + ((x + (lx * 3)) * 42) + (lx * 3), 50 + ((y + (ly * 3)) * 42) + (ly * 3), 40, 40), spc[(y + (ly * 3))][(x + (lx * 3))], brd[(y + (ly * 3))][(x + (lx * 3))]])
		self.bts = []
		for i in range(10):
			self.bts.append(pygame.Rect(50 + (i * 42), 450, 40, 40))
		self.select = 1
		self.notes = False
		self.block = [-1,-1]
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if [i for i in self.bts if i != None] == []: self.__init__()
			yy = 0
			for y in self.grid:
				xx = 0
				for x in y:
					if pygame.Rect.colliderect(mouse,x[0]):
						if self.notes:
							if isinstance(x[1],list) == False:
								x[1] = [0,0,0,0,0,0,0,0,0]
								x[1][self.select - 1] = self.select
							elif x[1][self.select - 1] == self.select: x[1][self.select - 1] = 0
							else: x[1][self.select - 1] = self.select
						elif x[1] != x[2]:
							if isinstance(x[1],list): x[1] = self.select
							elif x[1] == self.select: x[1] = None
							else: x[1] = self.select
						if len([i[1] for j in self.grid for i in j if i[1] == x[1] and i[1] == i[2]]) == 9:
							self.bts[x[1] - 1] = None
						self.block = [xx,yy]
					xx += 1
				yy += 1
			for i in range(10):
				if self.bts[i] != None and pygame.Rect.colliderect(mouse,self.bts[i]):
					if i == 9: self.notes = not self.notes
					else: self.select = i + 1
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		bw = False
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.grid[y][x][1] != self.grid[y][x][2] and isinstance(self.grid[y][x][1],int):
					cc = (200,100,100)
				elif self.block == [x,y] or x == self.block[0] or y == self.block[1] or [x,y] in [[(np.floor(self.block[0]/3)*3) + i,(np.floor(self.block[1]/3)*3) + j] for i in range(3) for j in range(3)]:
					cc = (100,200,100)
				elif bw: cc = (150,150,150)
				else: cc = (200,200,200)
				pygame.draw.rect(self.surface,cc,self.grid[y][x][0])
				if isinstance(self.grid[y][x][1],list):
					for yy in range(3):
						for xx in range(3):
							if self.grid[y][x][1][xx + (yy * 3)] == (xx + (yy * 3)) + 1:
								self.surface.blit(self.smll.render(str(self.grid[y][x][1][xx + (yy * 3)]),1,(10,10,10)), (self.grid[y][x][0].x + 5 + (xx * 10),self.grid[y][x][0].y + 5 + (yy * 10)))
				elif self.grid[y][x][1] != None: self.surface.blit(self.font.render(str(self.grid[y][x][1]),1,(10,10,10)), (self.grid[y][x][0].x + 5,self.grid[y][x][0].y + 5))
				bw = not bw
		for i in range(10):
			if self.bts[i] != None and i < 9:
				if self.select == i + 1: cc = (100,200,100)
				else: cc = (100,100,100)
				pygame.draw.rect(self.surface,cc,self.bts[i])
				self.surface.blit(self.font.render(str(i + 1),1,(10,10,10)), (52 + (i * 42),452))
			elif i == 9:
				if self.notes: cc = (100,200,100)
				else: cc = (100,100,100)
				pygame.draw.rect(self.surface,cc,self.bts[i])
				self.surface.blit(self.font.render(str('notes'),1,(10,10,10)), (52 + (i * 42),452))
		
		return self.surface

class Hangman:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 44)
		
		letters = []
		for i in 'abcdefghijklmnopqrstuvwxyz':
			letters.append(i)
		x = 0
		self.buttons = []
		for i in range(3):
			for j in range(10):
				if x >= len(letters): break
				self.buttons.append([pygame.Rect(20 + (j * 60), 200 + (i * 60),50,50),letters[x]])
				x += 1
		self.words = ['galinha','foca','gato','bola','fogão','geladeira','porta','mesa','blusa','casa','óculos','cadeira','janela','lençol','luz','sol','cachorro','mochila','guarda-roupa','travesseiro','carregador','telefone','televisão','cesta','chapéu','igreja','padre','avião','vovó','chocolate','gelo','ar condicionado','barco','pessoa','olhos','interruptor','parede','vidro','garrafa','banheiro','cozinha','quarto','caixa','mala','cobertor','short','dente','nariz','coração','sobrancelhas']
		self.word = ''
		self.guess = ''
		self.mistakes = ''
		self.doll = 0
		self.time = 0
		
		p = np.random.randint(0,len(self.words))
		self.word = self.words[p]
		for i in self.word:
			if i != ' ': self.guess += '_'
			else: self.guess = ' '
			
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if pygame.Rect.colliderect(mouse,i[0]):
					if i[1] in self.word:
						x = 0
						for w in self.word:
							if w == i[1]:
								self.guess = self.guess[0:x] + i[1] + self.guess[x + 1:]
							x += 1
					elif self.doll < 6:
						self.mistakes += i[1]
						self.doll += 1
						if self.doll == 6:
							self.time = 60
					if self.word == self.guess:
							self.time = 60
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((10,200,100))
		
		if self.time > 0: self.time -= 1
		if self.time == 1:
			self.word = ''
			self.guess = ''
			self.mistakes = ''
			self.doll = 0
			self.time = 0
		
			p = np.random.randint(0,len(self.words))
			self.word = self.words[p]
			for i in self.word:
				if i != ' ': self.guess += '_'
				else: self.guess = ' '
		
		self.surface.blit(self.font.render(self.mistakes,1,(200,200,200)),(20,20))
		self.surface.blit(self.font.render(self.guess,1,(200,200,200)),(200,100))
		
		if self.doll > 0: pygame.draw.circle(self.surface,(200,200,200),(300,300),50,3)
		if self.doll > 1: pygame.draw.line(self.surface,(200,200,200),(300,350),(300,500),3)
		if self.doll > 2: pygame.draw.line(self.surface,(200,200,200),(300,350),(250,450),3)
		if self.doll > 3: pygame.draw.line(self.surface,(200,200,200),(300,350),(350,450),3)
		if self.doll > 4: pygame.draw.line(self.surface,(200,200,200),(300,500),(250,600),3)
		if self.doll > 5: pygame.draw.line(self.surface,(200,200,200),(300,500),(350,600),3)
		
		for i in self.buttons:
			#pygame.draw.rect(self.surface,(200,200,200),i[0])
			self.surface.blit(self.font.render(i[1],1,(200,200,200)),(i[0].x + 5,i[0].y))
		
		return self.surface

class Yatzy:
	def __init__(self):
		sz = pygame.display.Info()
		self.surface = pygame.Surface((sz.current_w,sz.current_h))
		self.font = pygame.font.SysFont("Arial", 15)
		self.dice = [1,1,1,1,1]
		self.lock = [0,0,0,0,0]
		self.launch = 3
		self.time = 0
		self.score = 0
		self.values = [
			[(25,25)],
			[(10,10),(40,40)],
			[(10,10),(25,25),(40,40)],
			[(10,10),(40,10),(10,40),(40,40)],
			[(10,10),(40,10),(25,25),(10,40),(40,40)],
			[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]
		]
		self.rcts = []
		for i in range(6):
			self.rcts.append(pygame.Rect(20 + (i * 55),450,50,50))
		self.vls = [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.vlb = [1,2,3,4,5,6,'3x','4x','H','S','L','Y','?']
		self.vlk = [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.vrct = []
		for x in range(2):
			for y in range(7):
				if x == 0 and y == 6: break
				self.vrct.append(pygame.Rect(100 + (x * 100),100 + (y * 50),40,40))
		
	def inside_events(self,pressed,mouse):
		if pressed[4][0]:
			if self.vlk == [1,1,1,1,1,1,1,1,1,1,1,1,1]: self.__init__()
			for i in range(len(self.rcts)):
				if pygame.Rect.colliderect(mouse,self.rcts[i]):
					if i < 5 and self.launch < 3: self.lock[i] = int(not self.lock[i])
					elif i == 5 and self.launch > 0 and self.time == 0:
						self.time += 1
						self.launch -= 1
						for v in range(13):
							if self.vlk[v] == 0: self.vls[v] = 0
			for i in range(len(self.vrct)):
				if pygame.Rect.colliderect(mouse,self.vrct[i]) and self.vlk[i] == 0:
					self.vlk[i] = 1
					self.score += self.vls[i]
					self.launch = 3
					self.lock = [0,0,0,0,0]
		
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,50))
		for i in range(13):
			if self.vlk[i] == 0: pygame.draw.rect(self.surface,(200,200,200),self.vrct[i])
			if self.vlk[i] == 1: pygame.draw.rect(self.surface,(100,100,100),self.vrct[i])
			self.surface.blit(self.font.render(str(self.vlb[i]),1,(200,200,200)), (self.vrct[i].x - 40,self.vrct[i].y + 10))
			self.surface.blit(self.font.render(str(self.vls[i]),1,(10,10,10)), (self.vrct[i].x + 10,self.vrct[i].y + 10))
		if self.time >= 1:
			self.time += 1
			if self.time%5 == 0:
				for i in range(5):
					if self.lock[i] == 0: self.dice[i] = np.random.randint(1,7)
		if self.time > 120:
			self.time = 0
			for i in range(13):
				if self.vlk[i] == 0:
					tt = 0
					srt = self.dice.copy()
					srt.sort()
					for d in srt:
						if i == d - 1: self.vls[i] += d
						tt += d
					for d in srt:
						if i == 6 and srt.count(d) >= 3: self.vls[i] = tt
						if i == 7 and srt.count(d) >= 4: self.vls[i] = tt
					if i == 8 and srt in [[d,d,dd,dd,dd] for d in range(1,7) for dd in range(1,7) if d != dd]+[[d,d,d,dd,dd] for d in range(1,7) for dd in range(1,7) if d != dd]: self.vls[i] = 20
					if i == 9 and srt[:-1] in [[n for n in range(1 + j,5 + j)] for j in range(3)]: self.vls[i] = 30
					if i == 10 and srt in [[n for n in range(1 + j,6 + j)] for j in range(2)]: self.vls[i] = 40
					if i == 11 and self.dice.count(d) >= 5: self.vls[i] = 50
					if i == 12: self.vls[i] = tt
		for i in range(6):
			srf = pygame.Surface((50,50))
			if i < 5 and self.launch < 3:
				if self.lock[i] == 0: srf.fill((210,220,200))
				if self.lock[i] == 1: srf.fill((210,220,10))
				for d in self.values[self.dice[i] - 1]:
					pygame.draw.circle(srf,(10,10,10),d,5)
				self.surface.blit(srf,(self.rcts[i].x,self.rcts[i].y))
			elif i == 5:
				srf.fill((200,10,10))
				self.surface.blit(srf,(self.rcts[i].x,self.rcts[i].y))
				self.surface.blit(self.font.render(str(self.launch),1,(200,200,200)), (self.rcts[i].x + 10,self.rcts[i].y + 10))
		
		return self.surface

class Stop: pass

if os.path.basename(sys.argv[0]) == os.path.basename(__file__):
	g = Game()
	while True: g.run()