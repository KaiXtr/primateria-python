import sys
import pygame
import math
import random
from pygame.locals import *

pygame.init()
play = False

class Game:
	def __init__(self):
		self.display = pygame.display.set_mode((640, 1280))
		self.font = pygame.font.SysFont("Arial", 64)
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.minigame = Simon()
		
	def run(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			self.minigame.events(event)
		self.display.fill((0,0,100))
		
		self.display.blit(self.minigame.draw(),(0,0))
		
		pygame.display.flip()
		self.clock.tick(self.FPS)
		
class Pong:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
			self.goals = [pygame.Rect(200,200,100,20),pygame.Rect(200,1000,100,20)]
			self.ball = {'X': 100,'Y': 200, 'DIRECTION': 0, 'SPEED': 5}
			self.font = pygame.font.SysFont("Arial", 64)
			self.score = [0,0]
		
		def events(self, event):
			mp = pygame.mouse.get_pos()
			if mp[1] < int(self.surface.get_height()/2):
				self.goals[0].x = mp[0]
			if mp[1] > int(self.surface.get_height()/2):
				self.goals[1].x = mp[0]
		
		def draw(self):
			self.surface.fill((0,0,0))
			
			self.ball['X'] += int(math.cos(self.ball['DIRECTION']) * self.ball['SPEED'])
			self.ball['Y'] += int(math.sin(self.ball['DIRECTION']) * self.ball['SPEED'])
			
			for r in self.goals:
				if pygame.Rect.colliderect(pygame.Rect(self.ball['X'],self.ball['Y'],30,30),r):
					self.ball['DIRECTION'] += 2
			
			if self.ball['X'] <= 0:
				self.ball['DIRECTION'] += 2
				self.ball['X'] += 1
				self.ball['SPEED'] += 1
			if self.ball['X'] >= self.surface.get_width():
				self.ball['DIRECTION'] += 2
				self.ball['X'] -= 1
				self.ball['SPEED'] += 1
			if self.ball['Y'] <= 0:
				self.score[1] += 1
				self.ball['X'] = 200
				self.ball['Y'] = 500
				self.ball['SPEED'] = 5
				'''self.ball['DIRECTION'] += 2
				self.ball['Y'] += 1
				self.ball['SPEED'] += 1'''
			if self.ball['Y'] >= self.surface.get_height():
				self.score[0] += 1
				self.ball['X'] = 200
				self.ball['Y'] = 500
				self.ball['SPEED'] = 5
				'''self.ball['DIRECTION'] += 2
				self.ball['Y'] -= 1
				self.ball['SPEED'] += 1'''
			
			if self.ball['DIRECTION'] > 360: self.ball['DIRECTION'] -= 360
			
			pygame.draw.line(self.surface,(200,200,200),(0,int(self.surface.get_height()/2)),(self.surface.get_width(),int(self.surface.get_height()/2)),5)
			
			self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
			
			pygame.draw.circle(self.surface, (200,0,0), (self.ball['X'], self.ball['Y']), 15)
			for r in self.goals:
				pygame.draw.rect(self.surface,(0,200,0), r)
			
			return self.surface
			
class TicTacToe:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
			self.buttons = []
			for x in range (3):
				for y in range(3):
					self.buttons.append([pygame.Rect(100 + (x * 60), 200 + (y * 60),50,50),0])
			self.font = pygame.font.SysFont("Arial", 64)
			self.score = [0,0]
			self.mode = 1
			self.turn = 1
				
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				grd = []
				pl = []
				for i in self.buttons:
					if i[1] == 0:
						if pygame.Rect.colliderect(mr,i[0]):
							i[1] = self.turn
							break
				if self.mode == 0:
					x = 0
					for i in self.buttons:
						if i[1] == 0:
							pl.append(x)
						x += 1
					if len(pl) > 0:
						ch = random.randint(0,len(pl) - 1)
						self.buttons[pl[ch]][1] = 2
				if self.mode == 1:
					if self.turn == 1: self.turn = 2
					else: self.turn = 1
				
				wn = 0
				for i in self.buttons: grd.append(i[1])
				if grd[0] == 1 and grd[1] == 1 and grd[2] == 1: wn = 1
				if grd[3] == 1 and grd[4] == 1 and grd[5] == 1: wn = 1
				if grd[6] == 1 and grd[7] == 1 and grd[8] == 1: wn = 1
				if grd[0] == 1 and grd[3] == 1 and grd[6] == 1: wn = 1
				if grd[1] == 1 and grd[4] == 1 and grd[7] == 1: wn = 1
				if grd[2] == 1 and grd[5] == 1 and grd[8] == 1: wn = 1
				if grd[0] == 1 and grd[4] == 1 and grd[8] == 1: wn = 1
				if grd[2] == 1 and grd[4] == 1 and grd[6] == 1: wn = 1
				
				if grd[0] == 2 and grd[1] == 2 and grd[2] == 2: wn = 2
				if grd[3] == 2 and grd[4] == 2 and grd[5] == 2: wn = 2
				if grd[6] == 2 and grd[7] == 2 and grd[8] == 2: wn = 2
				if grd[0] == 2 and grd[3] == 2 and grd[6] == 2: wn = 2
				if grd[1] == 2 and grd[4] == 2 and grd[7] == 2: wn = 2
				if grd[2] == 2 and grd[5] == 2 and grd[8] == 2: wn = 2
				if grd[0] == 2 and grd[4] == 2 and grd[8] == 2: wn = 2
				if grd[2] == 2 and grd[4] == 2 and grd[6] == 2: wn = 2
				
				b = 0
				for i in self.buttons:
					if i[1] != 0: b += 1
				if b == len(self.buttons): wn = 3
				
				if wn == 1: self.score[0] += 1
				if wn == 2: self.score[1] += 1
				if wn != 0:
					for i in self.buttons:
						i[1] = 0
				
		def draw(self):
			self.surface.fill((0,0,0))
			for i in self.buttons:
				if i[1] == 0: c = (200,200,200)
				if i[1] == 1: c = (10,10,200)
				if i[1] == 2: c = (200,10,10)
				pygame.draw.rect(self.surface,c,i[0])
			self.surface.blit(self.font.render(str(self.score[0]) + ' - ' + str(self.score[1]),1,(200,200,200)), (10,10))
				
			return self.surface
			
class Memory:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
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
					v = random.randint(0,len(self.values) - 1)
					self.buttons.append([pygame.Rect(100 + (x * 60),200 + (y * 60),50,50),self.values[v],2])
					del self.values[v]
			
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN and self.time == 0:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				for i in self.buttons:
					if i[2] == 0:
						if pygame.Rect.colliderect(mr,i[0]):
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

class Hangman:
	def __init__(self):
		self.surface = pygame.Surface((640,1280))
		self.font = pygame.font.SysFont("Arial", 44)
		
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
		self.words = ['galinha','foca','gato','bola','fogão','geladeira','porta','mesa','blusa','casa','óculos','cadeira','janela','lençol','luz','sol','cachorro','mochila','guarda-roupa','travesseiro','carregador','telefone','televisão','cesta','chapéu','igreja','padre','avião','vovó','chocolate','gelo','ar condicionado','barco','pessoa','olhos','interruptor','parede','vidro','garrafa','banheiro','cozinha','quarto','caixa','mala','cobertor','short','dente','nariz','coração','sobrancelhas']
		self.word = ''
		self.guess = ''
		self.mistakes = ''
		self.doll = 0
		self.time = 0
		
		p = random.randint(0,len(self.words) - 1)
		self.word = self.words[p]
		for i in self.word:
			if i != ' ': self.guess += '_'
			else: self.guess = ' '
			
	def events(self,event):
		if event.type == MOUSEBUTTONDOWN:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if pygame.Rect.colliderect(mr,i[0]):
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
		
	def draw(self):
		self.surface.fill((0,0,0))
		
		if self.time > 0: self.time -= 1
		if self.time == 1:
			self.word = ''
			self.guess = ''
			self.mistakes = ''
			self.doll = 0
			self.time = 0
		
			p = random.randint(0,len(self.words) - 1)
			self.word = self.words[p]
			for i in self.word:
				if i != ' ': self.guess += '_'
				else: self.guess = ' '
		
		self.surface.blit(self.font.render(self.mistakes,1,(200,200,200)),(20,20))
		self.surface.blit(self.font.render(self.guess,1,(200,200,200)),(200,700))
		
		if self.doll > 0:
			pygame.draw.circle(self.surface,(200,200,200),(300,300),50,3)
		if self.doll > 1:
			pygame.draw.line(self.surface,(200,200,200),(300,350),(300,500),3)
		if self.doll > 2:
			pygame.draw.line(self.surface,(200,200,200),(300,350),(250,450),3)
		if self.doll > 3:
			pygame.draw.line(self.surface,(200,200,200),(300,350),(350,450),3)
		if self.doll > 4:
			pygame.draw.line(self.surface,(200,200,200),(300,500),(250,600),3)
		if self.doll > 5:
			pygame.draw.line(self.surface,(200,200,200),(300,500),(350,600),3)
		
		for i in self.buttons:
			pygame.draw.rect(self.surface,(200,200,200),i[0])
			self.surface.blit(self.font.render(i[1],1,(10,10,10)),(i[0].x + 5,i[0].y))
		
		return self.surface
		
class HuntingWords:
	def __init__(self):
		self.surface = pygame.Surface((640,1280))
		self.font = pygame.font.SysFont("Arial", 44)
		self.score = 0
		self.time = 1
		self.words = ['galinha','foca','gato','bola','fogão','geladeira','porta','mesa','blusa','casa','óculos','cadeira','janela','lençol','luz','sol','cachorro','mochila','travesseiro','carregador','telefone','televisão','cesta','chapéu','igreja','padre','avião','vovó','chocolate','gelo','barco','pessoa','olhos','interruptor','parede','vidro','garrafa','banheiro','cozinha','quarto','caixa','mala','cobertor','short','dente','nariz','coração','sobrancelhas']
		self.buttons = []
		self.grid = []
		for y in range(10):
			for x in range(10):
				self.buttons.append([pygame.Rect(10 + (x * 60),300 + (y * 60),60,60),0])
				self.grid.append('_')
		for i in range(7):
			t = random.randint(0,3)
			t = 1
			w = random.randint(0,len(self.words) - 1)
			while len(self.words[w]) >= 10:
				w = random.randint(0,len(self.words) - 1)
			s = random.randint(0,10 - len(self.words[w]))
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
				c = random.randint(0,len(letters) - 1)
				self.grid[i] = letters[c]
		
	def events(self,event):
		if event.type == MOUSEBUTTONDOWN:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			v = 0
			for i in self.buttons:
				if pygame.Rect.colliderect(mr,i[0]):
					i[1] = 1
		if event.type == MOUSEBUTTONUP:
			for i in self.buttons: i[1] = 0
		
	def draw(self):
		self.surface.fill((0,0,0))
		
		l = 0
		for i in self.buttons:
			if i[1] == 0: c = (200,200,200)
			if i[1] == 1: c = (100,200,10)
			pygame.draw.rect(self.surface,c,i[0])
			self.surface.blit(self.font.render(self.grid[l],1,(10,10,10)), (i[0].x + 10,i[0].y + 5))
			l += 1
		
		self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
		
		return self.surface

class Simon:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
			self.font = pygame.font.SysFont("Arial", 64)
			self.score = 0
			self.time = 1
			self.sequence = [random.randint(0,3)]
			self.mimic = []
			self.turn = 0
			
			self.buttons = []
			for y in range(2):
				for x in range(2):
					self.buttons.append([pygame.Rect(100 + (x * 60),400 + (y * 60),50,50),0])
			self.buttons[self.sequence[0]][1] = 20
			
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN and self.time == len(self.sequence):
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				v = 0
				for i in self.buttons:
					if pygame.Rect.colliderect(mr,i[0]):
							self.mimic.append(v)
							i[1] = 20
					v += 1
				if self.mimic[self.turn] == self.sequence[self.turn]:
					self.turn += 1
					if self.turn == len(self.sequence):
						self.sequence.append(random.randint(0,3))
						self.mimic = []
						self.turn = 0
						self.time = -60
						self.score += 1
				else:
					self.sequence = [random.randint(0,3)]
					self.mimic = []
					self.turn = 0
					self.time = -60
					self.score = 0
			
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

class Dominoes:
		def __init__(self):
			self.surface = pygame.Surface((700,1280))
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
			random.shuffle(self.dominoes)
			self.hands = [self.dominoes[0:12],self.dominoes[12:24],self.dominoes[24:36],self.dominoes[36:48]]
			self.dominoes[48][0] = pygame.transform.rotate(self.dominoes[48][0],90)
			self.tree = [self.dominoes[48]]
					
			self.font = pygame.font.SysFont("Arial", 64)
			self.score = [0,0,0,0]
			self.mode = 1
			self.turn = 0
			self.mn = 0
				
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN and self.turn == 0:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				x = 0
				for i in self.hands[self.turn]:
					print(self.hands[0])
					print('-------')
					print(self.tree)
					if pygame.Rect.colliderect(mr,pygame.Rect(10 + (x * 55),1000,50,100)):
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
			
class Chess:
		def __init__(self):
			self.surface = pygame.Surface((750,1280))
			self.font = pygame.font.SysFont("Arial", 64)
			self.time = [0,0,0]
			self.buttons = []
			for y in range(8):
				for x in range(8):
					self.buttons.append([x,y,0])
					
			self.pieces = [
				[[1,0,0],[2,1,0],[3,2,0],[4,3,0],[5,4,0],[3,5,0],[2,6,0],[1,7,0]],
				[[1,0,7],[2,1,7],[3,2,7],[4,3,7],[5,4,7],[3,5,7],[2,6,7],[1,7,7]]
			]
			for i in range(8): self.pieces[0].append([0,i,1])
			for i in range(8): self.pieces[1].append([0,i,6])
			self.turn = 0
			self.ply = 0
			self.mnu = 0
			
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN and self.turn == 0:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				pl = []
				for i in self.buttons:
					for j in self.pieces[self.turn]:
						rct = pygame.Rect(20 + (i[0] * 80),200 + (i[1] * 80),80,80)
						if pygame.Rect.colliderect(mr,rct):
							if self.mnu == 0:
								if j[1] == i[0] and j[2] == i[1]:
									self.mnu = 1
									self.ply = j
									i[1] = 1
									if j[0] == 0:
										pl = [(j[1],j[2] + 1)]
									if j[0] == 1:
										pl = [(j[1],j[2] + 1)]
									if j[0] == 2:
										pl = [(j[1],j[2] + 1)]
									if j[0] == 3:
										pl = [(j[1],j[2] + 1)]
									if j[0] == 4:
										pl = [(j[1],j[2] + 1)]
									if j[0] == 5:
										pl = [(j[1],j[2] + 1)]
							elif self.mnu == 1:
								if i[2] == 1 and j == self.ply:
									j[1] = i[0]
									j[2] = i[1]
									self.turn = 0
									self.mnu = 0
									self.ply = 0
									pl = []
								i[2] = 0
				for j in pl:
					for i in self.buttons:
						if i[0] == j[0] and i[1] == j[1]:
							i[2] = 1
			
		def draw(self):
			self.surface.fill((0,0,0))
			self.time[2] += 1
			if self.time[2] == 60:
				self.time[1] += 1
				self.time[2] = 0
			if self.time[1] == 60:
				self.time[0] += 1
				self.time[1] = 0
			bw = False
			xd = 0
			for i in self.buttons:
				if bw == False:
					if i[2] == 0: c = (10,10,10)
					if i[2] == 1: c = (100,100,200)
				if bw == True:
					if i[2] == 0: c = (200,200,200)
					if i[2] == 1: c = (100,200,10)
				
				pygame.draw.rect(self.surface,c,pygame.Rect(20 + (i[0] * 80),200 + (i[1] * 80),80,80))
				xd += 1
				if xd < 8: bw = not bw
				else: xd = 0
			for i in range(2):
				for p in self.pieces[i]:
					if i == 0: c = (200,200,200)
					if i == 1: c = (10,10,10)
					self.surface.blit(pygame.image.load('Sprites/chpi_' + str(0) + str(0) +'.png'),(20 + (p[1] * 80),200 + (p[2] * 80)))
					
			self.surface.blit(self.font.render(str(self.time[0]) + ':' + str(self.time[1]),1,(200,200,200)), (10,10))
			
			return self.surface
			
class Copas:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
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
			
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN and self.time == 0:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				for i in self.buttons:
					if i[2] == 0:
						if pygame.Rect.colliderect(mr,i[0]):
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

class Sinuca:
		def __init__(self):
			self.surface = pygame.Surface((640,1280))
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
			
		def events(self,event):
			if event.type == MOUSEBUTTONDOWN:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				if pygame.Rect.colliderect(mr,self.pbll[0]):
					self.pbll[1] = 20
					self.pbll[2] = self.pang
				self.pang += 0.5
			
		def draw(self):
			self.surface.fill((0,0,0))
			if self.time < 0:
				self.time += 1
			for i in self.holes:
				pygame.draw.ellipse(self.surface,(50,50,50),i)
			for i in self.balls:
				if i[2] > 0:
					i[2] -= 0.1
					i[1].x += int(math.cos(i[3]) * i[2])
					i[1].y += int(math.sin(i[3]) * i[2])
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
				
				if i[0] == 0: c = (200,10,10)
				elif i[0] == 1: c = (200,200,10)
				elif i[0] == 2: c = (100,200,10)
				elif i[0] == 3: c = (10,10,200)
				c = (200,10,10)
				pygame.draw.ellipse(self.surface,c,i[1])
				pygame.draw.ellipse(self.surface,(240,240,240),pygame.Rect(i[1].x + 10,i[1].y + 10,20,20))
				self.surface.blit(self.nfnt.render(str(i[0]),True,(10,10,10)),(i[1].x + 10,i[1].y + 10))
			if self.pbll[1] > 0:
				self.pbll[1] -= 0.1
				self.pbll[0].x += int(math.cos(self.pbll[2]) * self.pbll[1])
			self.pbll[0].y += int(math.sin(self.pbll[2]) * self.pbll[1])
			
			if self.pbll[0].x <= 0: self.pbll[0].x += 2; self.pbll[2] += 2
			if self.pbll[0].x >= self.surface.get_width(): self.pbll[0].x -= 2; self.pbll[2] += 2
			if self.pbll[0].y <= 0: self.pbll[0].y += 2; self.pbll[2] += 2
			if self.pbll[0].y >= self.surface.get_height(): self.pbll[0].y -= 2; self.pbll[2] += 2
			
			pygame.draw.ellipse(self.surface,(240,240,240),self.pbll[0])
			pygame.draw.line(self.surface,(240,240,240),(self.pbll[0].x + 20 - int(math.cos(self.pang) * 30),self.pbll[0].y + 20 - int(math.sin(self.pang) * 30)),(self.pbll[0].x + 20 - int(math.cos(self.pang) * 250),self.pbll[0].y + 20 - int(math.sin(self.pang) * 250)),3)

			self.surface.blit(self.font.render(str(self.score),1,(200,200,200)), (10,10))
			
			return self.surface

g = Game()
while play == True:
	g.run()