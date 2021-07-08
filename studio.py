import pygame
import pytmx
import math
import random
import sys
import os
import resources as res
import GUI

pygame.init()

class App:
	def __init__(self):
		sz = pygame.display.Info()
		self.window = (sz.current_w, sz.current_h)
		self.screen = pygame.display.set_mode(self.window)
		self.fnt = {'REGULAR': pygame.font.SysFont("Arial", 64),'CODE': pygame.font.SysFont("Arial", 32)}
		self.uicolors = [(50,50,100),(100,100,150),(150,150,200),(10,100,50),(10,10,50),(200,200,250)]
		for j in os.listdir(res.SFX_PATH[:-1]): 
			res.sfx(j)
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.vkb = GUI.Vkeyboard(self.window)
		self.buttons = []
		self.dirbts = []
		self.opt = [0,0]
		self.mnu = 0
		self.scroll = 0
		self.lang = 'PT'
		self.labels = {
		'PT': [['Primateria','Novo Projeto'],
		['Nome:','Diretório:','Autor:','Descrição:','Ano:','Idioma principal:','Template:','Criar'],
		['Mapa','Arquivos','Dados','Imagens','SFX','Menu','Código']]
		}
		self.keys = ['GNAME','DIRECTORY','AUTHOR','DESCRIPTION','YEAR','LANG']
		self.values = {'GNAME': '','DIRECTORY': '','AUTHOR': '','DESCRIPTION': '','YEAR': '','LANG': 'PT'}
		file = open('database_PT.py','r')
		self.file = file.read()
		file.close()
		self.path = './'
		self.curdir = 0
		self.mphld = [0,0]
		self.img = None
		self.map = None
		self.tiles = []
		self.objects = []
		self.zoom = [0,0]
		
	def loadmap(self,file):
		self.map = pytmx.load_pygame(file)
		self.tiles = []
		self.objects = []
		for i in range(2):
			for y in range(0, self.map.height):
				for x in range(0, self.map.width):
					gid = self.map.get_tile_gid(x, y, i)
					t = self.map.get_tile_properties_by_gid(gid)
					try: img = self.map.get_tile_image_by_gid(t['frames'][0].gid)
					except: img = self.map.get_tile_image_by_gid(gid)
					self.tiles.append([img,[x,y,i],t])
		for i in self.map.layers:
			if i.name.startswith('Camada'): continue
			for obj in i:
				self.objects.append(self.map.get_object_by_name(obj.name))
	
	def events(self):
		mp = pygame.mouse.get_pos()
		mr = pygame.Rect(mp[0],mp[1],2,2)
		if self.mphld != None:
			self.scroll = self.mphld[1]
			if pygame.mouse.get_pressed()[0]:
				self.mphld[1] = mp[1]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.VIDEORESIZE:
				self.window = (event.w,event.h)
			if self.vkb.active:
				self.values[self.keys[self.opt[1]]] = self.vkb.output
				self.vkb.events(event)
				self.buttons = []
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.mphld[1] += mp[1]
			#BUTTONS
			for i in range(len(self.buttons)):
				if len(self.buttons) > 0 and pygame.Rect.colliderect(mr,self.buttons[i][1]):
					if event.type == pygame.MOUSEBUTTONUP:
						if self.mnu == 0:
							self.buttons = []
							self.mnu = 1
						elif self.mnu == 1:
							if i in [0,1,2,3,4]:
								self.vkb.active = True
								self.opt[1] = i
							elif i == 7:
								self.buttons = []
								self.mnu = 2
								self.opt = [0,0]
						else:
							self.mnu = i + 2
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.buttons[i][2] = 1
			#DIRECTORY OPTIONS
			for i in range(len(self.dirbts)):
				if len(self.dirbts) > 0 and pygame.Rect.colliderect(mr,self.dirbts[i][1]):
					if event.type == pygame.MOUSEBUTTONUP:
						if self.mnu == 3:
							#OPEN FOLDER
							if os.path.isdir(self.path + self.dirbts[i][0]):
								if self.dirbts[i][0] == '../':
									self.path = self.path[0:-self.curdir]
								else:
									self.curdir = len(self.dirbts[i][0]) + 1
									self.path += self.dirbts[i][0] + '/'
								self.dirbts = []
								print(self.path)
							#OPEN FILES
							else:
								if self.dirbts[i][0].endswith('.tmx'):
									self.loadmap(self.path + self.dirbts[i][0])
									self.mnu = 4
								elif self.dirbts[i][0].endswith('.png'):
									self.img = pygame.image.load(self.path + self.dirbts[i][0])
									self.mnu = 5
								else:
									file = open(self.dirbts[i][0],'r')
									self.file = file.read()
									file.close()
									self.mnu = 8
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.dirbts[i][2] = 1
						self.opt[1] = i + 1
						#if self.mnu == 2:
						#	self.vkb.active = True
		
	def filemenu(self):
		if self.buttons == []:
			for i in range(2):
				rct = pygame.Rect(20,120 + (i * 120),self.window[0] - 40,100)
				self.buttons.append([self.labels[self.lang][0][1],rct,0])
		pygame.draw.rect(self.screen,self.uicolors[2],pygame.Rect(0,0,self.window[0],100))
		self.screen.blit(self.fnt['REGULAR'].render(self.labels[self.lang][0][0],True,self.uicolors[5]),(10,10))
		for i in self.buttons:
			srf = pygame.Surface((i[1].width,i[1].height))
			if i[2] == 0: srf.fill(self.uicolors[2])
			else: srf.fill(self.uicolors[3])
			srf.blit(self.fnt['REGULAR'].render(i[0],True,self.uicolors[4]),(10,10))
			self.screen.blit(srf,(i[1].x,i[1].y))
			if pygame.mouse.get_pressed()[0] == False: i[2] = 0
	
	def new(self):
		if self.buttons == []:
			lst = self.labels[self.lang][1]
			for i in range(len(lst)):
				rct = pygame.Rect(20,120 + (i * 120),self.window[0] - 40,100)
				self.buttons.append([lst[i],rct,0])
		pygame.draw.rect(self.screen,self.uicolors[2],pygame.Rect(0,0,self.window[0],100))
		self.screen.blit(self.fnt['REGULAR'].render('New Project',True,self.uicolors[5]),(10,10))
		y = 0
		for i in self.buttons:
			srf = pygame.Surface((i[1].width,i[1].height))
			if i[2] == 0: srf.fill(self.uicolors[2])
			else: srf.fill(self.uicolors[3])
			if y in [0,1,2,3,4]: txt = i[0] + ' ' + self.values[self.keys[y]]
			else: txt = i[0]
			srf.blit(self.fnt['REGULAR'].render(txt,True,self.uicolors[4]),(10,10))
			self.screen.blit(srf,(i[1].x,i[1].y))
			if pygame.mouse.get_pressed()[0] == False: i[2] = 0
			y += 1
			
	def studio(self):
		ln = 40
		#CREATE BUTTONS
		if self.buttons == []:
			lst = self.labels[self.lang][2]
			for i in range(len(lst)):
				rct = pygame.Rect(20 + (i * 120),20,100,100)
				srf = pygame.Surface((rct.width,rct.height))
				srf.fill(self.uicolors[2])
				srf.blit(self.fnt['REGULAR'].render(lst[i],True,self.uicolors[4]),(10,10))
				self.buttons.append([srf,rct,0])
		#CREATE DIRBUTTONS
		if self.dirbts == []:
			lst = os.listdir(self.path)
			lst.sort()
			y = 1
			for i in ['../'] + lst:
				self.dirbts.append([i,pygame.Rect(0,150 + (y * ln),self.window[0],ln),0])
				y += 1
		for i in self.buttons:
			self.screen.blit(i[0],(i[1].x,i[1].y))
		srfedit = pygame.Surface((self.window[0],self.window[1] - 140))
		srfedit.fill(self.uicolors[0])
		#MAP MENU
		if self.mnu == 2:
			for i in self.tiles:
				if i[0] != None:
					srfedit.blit(i[0],(i[1][0] * self.map.tilewidth,i[1][1] * self.map.tileheight))
		#FILES MENU
		if self.mnu == 3:
			srfedit.blit(self.fnt['CODE'].render(self.path,True,self.uicolors[5]),(10,10))
			y = 1
			for i in self.dirbts:
				if y > self.window[1]: break
				if self.opt[1] == y + 1:
					pygame.draw.rect(srfedit,self.uicolors[2],i[1])
				srfedit.blit(self.fnt['CODE'].render(i[0],True,self.uicolors[5]),(10,10 + (y * ln)))
				y += 1
		#DATABASE MENU
		if self.mnu == 4:
			pass
		#IMAGES MENU
		if self.mnu == 5:
			if self.img != None: srfedit.blit(self.img,(0,0))
		#SFX MENU
		if self.mnu == 6:
			pass
		#GUI MENU
		if self.mnu == 7:
			pass
		#CODE MENU
		if self.mnu == 8:
			y = self.scroll
			for i in self.file.splitlines():
				if y > self.window[1]: break
				srfedit.blit(self.fnt['CODE'].render(i,True,self.uicolors[5]),(10,10 + y))
				y += ln
		self.screen.blit(srfedit,(0,140))
	
	def run(self):
		self.screen.fill(self.uicolors[1])
		if self.mnu == 0: self.filemenu()
		if self.mnu == 1: self.new()
		if self.mnu >= 2: self.studio()
		#VKEYBOARD
		if self.vkb.active:
			self.display[1].blit(self.vkb.draw(),(0,self.vkb.size[1] - self.vkb.pos))
			self.hpctrl = []
		self.vkb.scroll()
		try: pygame.display.flip()
		except: self.screen = pygame.display.set_mode(self.window)
		self.clock.tick(self.FPS)
		
app = App()
while True: app.run()