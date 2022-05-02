# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3
import resources as res
import urllib.request
import pygame
import plyer
import numpy as np
import sys
import os

import PIL.Image
import PIL.ImageOps

import tools
import minigames
import resources as res
sys.path.insert(0,'databases')
if res.FILES != []: dtb = __import__('database_' + res.FILES[0][4])
else: dtb = __import__('database_' + res.MAINLANG)

class Test:
	def __init__(self):
		pygame.init()
		res.sfx()
		res.fonts()
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		pygame.mixer.music = pygame.mixer.Channel(1)
		pygame.mixer.music.set_volume(res.MSC)
		for i in range(4):
			res.MIXER.append(pygame.mixer.Channel(i))
			res.MIXER[i].set_volume(res.SFX)
		self.display = pygame.display.set_mode((800, 600),pygame.RESIZABLE | pygame.SRCALPHA)
		self.font = pygame.font.SysFont("Arial", 30)
		self.clock = pygame.time.Clock()
		self.menu = [Pseudo3d(),Popup('Calendar',(100,100),miniature=True),Popup('docs/LICENSE.FLAC.txt',(50,50))]
		self.counters = []#[Counter(8),Counter(5)]
		self.img = pygame.image.load('SS1.jpg').convert()

	def run(self):
		res.HOVERTEXT = None
		for event in pygame.event.get():
			pressed, mouse = tools.event.get_pressed(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.VIDEORESIZE:
				self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.SRCALPHA)
			rcts = []
			for i in range(len(self.menu))[::-1]:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(int(mp[0]),int(mp[1]),20,20)
				do = True
				for r in rcts:
					if pygame.Rect.colliderect(mr,r): do = False
				if do: self.menu[i].inside_events(pressed,mouse)
				if type(self.menu[i]).__name__ == 'Popup': rcts.append(self.menu[i].rect)
				nw = []
				for x in self.menu:
					if type(x).__name__ == 'Popup':
						if x.gui != None: nw.append(x)
					else: nw.append(x)
				self.menu = nw
		pressed, click = tools.event.get_pressed(None)
		for i in self.menu: i.outside_events(pressed)

		self.display.fill((100,100,100))
		for i in self.menu:
			if type(i).__name__ == 'Popup': self.display.blit(i.draw(),(i.rect.x,i.rect.y))
			else: self.display.blit(i.draw(),(0,0))
		if len(self.menu) > 4:
			img = self.menu[4].gui.wheel()
			self.display.blit(img,(100 - int(img.get_width()/2),100 - int(img.get_height()/2)))
		for i in range(len(self.counters)):
			self.counters[i].update(int(self.time))
			self.display.blit(self.counters[i].draw(),(0,i * 40))
		if res.HOVERTEXT:
			sz = self.font.size(res.HOVERTEXT)
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(int(mp[0]),int(mp[1]),sz[0] + 10,sz[1] + 10)
			pygame.draw.rect(self.display,(10,10,10),mr)
			self.display.blit(self.font.render(res.HOVERTEXT,True,res.COLOR),(mr.x + 5,mr.y + 5))

		for i in res.MIXER:
			if pygame.display.get_active(): i.set_volume(res.SFX)
			elif res.MUTE: i.set_volume(0)
		pygame.display.flip()
		self.clock.tick(60)

class Popup:
	def __init__(self,gui,rect=(100,100),msg=None,miniature=None,deletable=True,border=True):
		res.FONTS = {**res.FONTS,'MESSAGE': tools.text.font_size(res.FONTS['DEFAULT'],6)}
		self.bdsz = 10
		self.top = 50
		self.apps = []
		self.btrects = []
		self.show = True
		self.min = False
		self.infobar = 0
		self.battery = 3600
		self.deletable = deletable
		self.imgs = {}
		self.goback = None
		self.drag = False

		#POPUP DIALOGBOXES
		if gui in ['conf','info']:
			self.gui = gui
			self.ratio = [350 + (self.bdsz * 2),100 + (self.bdsz * 2) + self.top]
			if gui == 'conf': rg = 2
			else: rg = 1
			for i in range(rg): self.btrects.append(pygame.Rect(self.bdsz + 40 + (100 * i),self.bdsz + self.top + 50,80,40))
		#APP MENUS
		elif gui in ['Phone','PC','PDA']:
			self.gui = gui
			self.infobar = 28
			self.apps = ['Contacts','Email','Radio','Bestiary','Tasks','Status','Tactics','Settings','About']
			if gui == 'PC':
				self.imgs['BKG'] = pygame.image.load(res.BACKG_PATH + 'pcbkg_1.png').convert_alpha()
				self.ratio = [600,400]
				yy = 0
			else:
				self.imgs['BKG'] = pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png').convert_alpha()
				self.ratio = [400,300]
				yy = self.infobar
			for y in range(3):
				for x in range(3):
					self.btrects.append(pygame.Rect(self.bdsz + 20 + (60 * x),self.bdsz + self.top + yy + 20 + (60 * y),50,50))
			for i in self.apps: self.imgs[i] = pygame.image.load(res.SPRITES_PATH + 'ph_' + i.lower() + '.png').convert_alpha()
			for i in range(2): self.imgs['desktop_' + str(i)] = pygame.image.load(res.SPRITES_PATH + 'desktop_' + str(i) + '.png').convert_alpha()
		#MEDIA PLAYER
		elif os.path.splitext(gui)[1][1:] in ('png','jpg','wav','ogg','mp3','gif'):
			self.gui = eval('MediaPlayer')(gui)
			self.ratio = [self.gui.surface.get_width() + (self.bdsz * 2),self.gui.surface.get_height() + (self.bdsz * 2) + self.top]
			if self.gui.ext in ['png','jpg']: gui = 'Image'
			if self.gui.ext in ['wav','ogg','mp3']: gui = 'AudioPlayer'
			if self.gui.ext == 'gif': gui = 'GifPlayer'
		#TEXT READER
		elif os.path.splitext(gui)[1][1:] in ('txt','md'):
			self.gui = eval('TextReader')(gui)
			self.ratio = [self.gui.surface.get_width() + (self.bdsz * 2),self.gui.surface.get_height() + (self.bdsz * 2) + self.top]
			gui = 'TextReader'
		#DISPLAY GUIS
		else:
			sz = (400,300)
			lst = ['Inventory','Trash','Storage','Products','Basket']
			for i in range(len(lst)):
				if gui == lst[i]: self.gui = eval('Inventory')(sz,i)
			else: self.gui = eval(gui)()
			self.ratio = [self.gui.surface.get_width() + (self.bdsz * 2),self.gui.surface.get_height() + (self.bdsz * 2) + self.top]

		self.title = gui
		self.surface = pygame.Surface(tuple(self.ratio),pygame.SRCALPHA)

		#POPUP BORDER
		self.brd = pygame.Surface(tuple(self.ratio),pygame.SRCALPHA)
		if border:
			self.brd.fill(res.COLOR)
			for r in range(3):
				col = [res.COLOR[0] - int(120/(r + 1)),res.COLOR[1] - int(120/(r + 1)),res.COLOR[2] - int(120/(r + 1))]
				for i in range(len(col)):
					if col[i] < 0: col[i] = 0
				pygame.draw.rect(self.brd,tuple(col),pygame.Rect(r,r,self.ratio[0] - (r * 2),self.ratio[1] - (r * 2)),1)
			for x in range(int(self.ratio[0]/10)):
				for y in range(int(self.ratio[1]/10)):
					self.brd.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10,y * 10))
			if gui.startswith('minigames.'): tt = dtb.MINIGAMES[self.title[10:]].lower()
			else: tt = dtb.MENU[self.title]
			self.brd.blit(res.FONTS['TITLE'].render(tt, True, (0, 0, 0)), (10, 10))

		self.msg = msg
		self.rect = pygame.Rect(rect[0],rect[1],self.surface.get_width(),self.surface.get_height())
		self.optrects = [pygame.Rect(self.bdsz,self.bdsz,30,30),pygame.Rect(self.surface.get_width() - self.bdsz - 30,self.bdsz,30,30)]
		if miniature != None: self.optrects.append(pygame.Rect(self.surface.get_width() - self.bdsz - 70,self.bdsz,30,30))
		
	def inside_events(self,pressed,mouse):
		mr1 = pygame.Rect(int((mouse.x - self.rect.x)/res.GSCALE),int((mouse.y - self.rect.y)/res.GSCALE),mouse.width,mouse.height)
		mr2 = pygame.Rect(int(mouse.x - self.rect.x),int(mouse.y - self.rect.y),mouse.width,mouse.height)
		if pygame.Rect.colliderect(self.rect,mouse):
			#POPUP MESSAGE OPTIONS
			if self.gui in ['conf','info'] and self.battery > 0:
				if pygame.Rect.colliderect(self.btrects[0],mr2): self.gui = None; return True
				elif pygame.Rect.colliderect(self.btrects[1],mr2): self.gui = None; return False
			#APP MENUS
			elif self.gui in ['Phone','PC','PDA']:
				for i in range(len(self.btrects)):
					if pygame.Rect.colliderect(mr2,self.btrects[i]):
						if pressed[4][0]:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
							self.title = self.apps[i]
							self.goback = self.gui
							self.gui = eval(self.apps[i])()
							self.ratio = [self.gui.surface.get_width() + (self.bdsz * 2),self.gui.surface.get_height() + (self.bdsz * 2) + self.top]
			#GUI OPTIONS
			else: self.gui.inside_events(pressed,mr2)
			#EXIT AND MINIMIZE BUTTONS
			if pressed[4][0]:
				if self.min == False:
					if pygame.Rect.colliderect(self.optrects[1],mr2):
						res.MIXER[0].play(res.SOUND['MENU_BACK'])
						if self.goback:
							self.title = self.goback
							self.gui = self.goback
						elif self.deletable: self.gui = None
						else: self.show = False
					if len(self.optrects) > 2 and pygame.Rect.colliderect(self.optrects[2],mr2):
						res.MIXER[0].play(res.SOUND['MENU_GO'])
						self.min = not self.min
	
	def outside_events(self,pressed):
		mp = pygame.mouse.get_pos()
		mr1 = pygame.Rect(int((mp[0] - self.rect.x)/res.GSCALE),int((mp[1] - self.rect.y)/res.GSCALE),20,20)
		mr2 = pygame.Rect(int(mp[0] - self.rect.x),int(mp[1] - self.rect.y),20,20)
		if pygame.Rect.colliderect(self.rect,pygame.Rect(mp[0],mp[1],2,2)):
			#HOVER TEXT
			if self.gui in ['Phone','PC','PDA']:
				for i in range(len(self.btrects)):
					if pygame.Rect.colliderect(mr2,self.btrects[i]):
						res.HOVERTEXT = dtb.MENU[self.apps[i]]
			#GUI OPTIONS
			elif self.battery > 0: res.HINTEXT = self.title.upper(); self.gui.outside_events(pressed)
			#DRAG POPUP
			if pressed[4][0] and pygame.Rect.colliderect(self.optrects[0],mr2): self.drag = True
			else: self.drag = False
		if self.drag: self.rect.x = mp[0] - 10; self.rect.y = mp[1] - 10
	
	def draw(self):
		if self.min == False:
			self.surface.blit(self.brd,(0,0))
			for i in self.optrects[1:]: pygame.draw.rect(self.surface,(200,100,100),i)
		else: self.surface.fill((0,0,0,0))
		if self.gui == 'PC': yy = self.bdsz + self.top
		else: yy = self.bdsz + self.top + self.infobar

		pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(self.bdsz,yy,self.ratio[0] - (self.bdsz * 2),self.ratio[1] - self.top - (self.bdsz * 2)))
		#INFO BAR
		if self.infobar and not self.min and self.battery > 0:
			self.battery -= 1
			dt = tools.text.digitstring(res.TIME[0],2) + ':' + tools.text.digitstring(res.TIME[1],2)
			dtsz = self.ratio[0] - (self.bdsz * 2) - res.FONTS['DATETIME'].size(dt)[0] - 10
			infbr = pygame.Surface((self.ratio[0] - (self.bdsz * 2),self.infobar))

			#BATTERY ICON
			if self.gui == 'PC': add = 3; infbr.fill((50,50,200))
			else:
				add = 50
				infbr.fill((0,0,0))
				pygame.draw.rect(infbr,(255,255,255),pygame.Rect(dtsz - 40,5,40,20),2)
				pygame.draw.rect(infbr,(255,255,255),pygame.Rect(dtsz - 42,10,2,10))
				if self.battery > 1000: col = (255,255,255)
				else: col = (200,10,10)
				if self.battery > 0: pygame.draw.rect(infbr,col,pygame.Rect(dtsz - 4 - int(32/(3600/self.battery)),9,int(32/(3600/self.battery)),12))
			
			#SIGNAL ICON
			if res.SIGNAL: rng = res.SIGNAL
			else: rng = 4
			for i in range(rng):
				if res.SIGNAL == 0:
					for v in [((0,4),(5,9)),((5,4),(0,9))]: pygame.draw.line(infbr,(255,255,255),(dtsz - (add + 15) + v[0][0],v[0][1]),(dtsz - (add + 15) + v[1][0],v[1][1]),2)
				pygame.draw.rect(infbr,(255,255,255),pygame.Rect(dtsz - add - ((3 - i) * 4),8 + ((3 - i) * 4),2,16 - ((3 - i) * 4)))
			
			#DATE AND HOUR
			if self.gui != 'PC': infbr.blit(res.FONTS['DATETIME'].render(tools.text.digitstring(res.DATE[0],2) + '/' + tools.text.digitstring(res.DATE[1],2) + '/' + tools.text.digitstring(res.DATE[2],4), True, (255, 255, 255)), (3, 3))
			infbr.blit(res.FONTS['DATETIME'].render(dt, True, (255, 255, 255)), (dtsz, 3))

			#TASKBAR ICONS
			for i in range(2): infbr.blit(self.imgs['desktop_' + str(i)],(3 + (30 * i),3))

			if self.gui == 'PC': self.surface.blit(infbr,(self.bdsz,self.ratio[1] - self.bdsz - self.infobar))
			else: self.surface.blit(infbr,(self.bdsz,self.bdsz + self.top))

		#POPUP MESSAGE
		if self.gui in ['conf','info']:
			for i in self.optrects[1:]: pygame.draw.rect(self.surface,(200,100,100),i)
			pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(self.bdsz,yy,350,100))
			for i in self.btrects: pygame.draw.rect(self.surface,(100,100,100),i)
			xx = int((350 - (self.bdsz * 2))/2) - int(res.FONTS['MESSAGE'].size(self.msg)[0]/2)
			self.surface.blit(res.FONTS['MESSAGE'].render(self.msg, True, (200, 200, 200)), (xx,yy + 5))
		#APP MENUS
		elif self.gui in ['Phone','PC','PDA']:
			self.surface.blit(self.imgs['BKG'],(self.bdsz,yy),pygame.Rect(0,0,600 - (self.bdsz * 2),400 - (self.bdsz * 2) - self.top - self.infobar))
			for i in range(len(self.btrects)):
				self.surface.blit(self.imgs[self.apps[i]],(self.btrects[i].x,self.btrects[i].y))
		#DISPLAY UI
		else:
			sz = (self.gui.surface.get_width() + (self.bdsz * 2),self.gui.surface.get_height() + (self.bdsz * 2) + self.top)
			#MINIMIZED WINDOW
			if self.min:
				if (round(self.ratio[0]),round(self.ratio[1])) != self.gui.ratio[1]:
					for i in range(2): self.ratio[i] -= (sz[i] - self.gui.ratio[1][i])/10
					self.surface = pygame.Surface((round(self.ratio[0]),round(self.ratio[1])))
				else:
					if self.title in ['Inventory','Storage','Products','Basket','Trash']: self.surface.blit(self.gui.bar(0,4,(0,4),'horizontal'),(0,0))
					else: self.surface.blit(self.gui.miniature(),(0,0))
			#MAXIMIZED WINDOW
			else:
				if (round(self.ratio[0]),round(self.ratio[1])) != sz:
					for i in range(2): self.ratio[i] += (self.gui.ratio[0][i] - self.gui.ratio[1][i])/10
					self.surface = pygame.Surface((round(self.ratio[0]),round(self.ratio[1])))
				elif self.battery > 0:
					#GUI SURFACE
					self.gui.draw()
					self.surface.blit(self.gui.surface,(self.bdsz,yy))
				#NO BATTERY
				else:
					self.surface.blit(self.brd,(0,0))
					pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(self.bdsz,yy,self.gui.surface.get_width(),self.gui.surface.get_height()))
					pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(self.bdsz + int(self.gui.surface.get_width()/2) - 25,yy + int(self.gui.surface.get_height()/2) - 110,50,10),5)
					pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(self.bdsz + int(self.gui.surface.get_width()/2) - 50,yy + int(self.gui.surface.get_height()/2) - 100,100,200),5)
					pygame.draw.line(self.surface,(200,200,200),(self.bdsz + int(self.gui.surface.get_width()/2) - 20,yy + int(self.gui.surface.get_height()/2) - 20),(self.bdsz + int(self.gui.surface.get_width()/2) + 20,self.bdsz + self.top + int(self.gui.surface.get_height()/2) + 20),5)
					pygame.draw.line(self.surface,(200,200,200),(self.bdsz + int(self.gui.surface.get_width()/2) + 20,yy + int(self.gui.surface.get_height()/2) - 20),(self.bdsz + int(self.gui.surface.get_width()/2) - 20,self.bdsz + self.top + int(self.gui.surface.get_height()/2) + 20),5)

		return self.surface

class Counter:
	def __init__(self,length):
		self.sz = 10 * res.GSCALE
		lst = [0,1,2,3,4,5,6,7,8,9,0]
		self.img = pygame.Surface((self.sz,self.sz * len(lst)),pygame.SRCALPHA)
		for i in range(len(lst)): self.img.blit(res.FONTS['DEFAULT'].render(str(lst[i]),True,(200,200,200)),(0,i * self.sz))
		self.slots = [0 for i in range(length)]

	def update(self,value):
		lst = [i for i in tools.text.digitstring(value,len(self.slots))]
		for i in range(len(self.slots)):
			if self.slots[i] < int(lst[i]) * self.sz: self.slots[i] += 2
			if int(lst[i]) == 0 and self.slots[i] > int(lst[i]): self.slots[i] += 2
			if self.slots[i] >= (self.sz * 10): self.slots[i] = 0

	def draw(self,space=6 * res.GSCALE):
		srf = pygame.Surface((self.sz * len(self.slots),self.sz),pygame.SRCALPHA)
		for i in range(len(self.slots)): srf.blit(self.img,(space * i,0),(0,self.slots[i],self.sz,self.sz))
		return srf

class Vkeyboard:
	def __init__(self,rect,type='QWERTY',display=False):
		type = type.upper()
		if type == 'NUMPAD': cl = 3
		elif type == 'CALC': cl = 4
		else: cl = 10
		sz = int((rect.width - (cl * 12))/cl)
		sp = 10 + sz
		self.display = display
		self.surface = pygame.Surface((rect.width,sp * 5.5))
		self.font = pygame.font.SysFont("Arial", 44)
		self.type = type
		self.rect = rect
		self.active = False
		self.caps = 1
		self.page = 0
		self.hold = 0
		self.opt = 0
		self.output = ''
		
		if type == 'QWERTY': lst = '1234567890qwertyuiopasdfghjklzxcvbnm, .'
		elif type == 'DVORAK': lst = "1234567890',.pyfgcrlaoeuidhtnsjkxbmwvq z"
		elif type == 'NUMPAD': lst = '123456789#0*'
		elif type == 'CALC': lst = '123+456-789÷0=.×'
			
		acclst = [('a','äåæªáãàâ'),('c','ćçč'),('e','ëėēèéêę'),('o','ºōœøöòôóõ'),
		('u','ūùúüû')]
		
		letters = [[],[]]
		for i in lst: letters[0].append(str(i))
		for i in '~`|•√π÷×¶∆@#$_&-+()/*"'+"':;!?,.<>={}[]%©®": letters[1].append(i)
		for i in letters:
			i.insert(29,1)
			i.insert(37,0)
			i.insert(38,2)
			i.append(3)
		for i in range(len(letters[0])):
			for a in acclst:
				if letters[0][i] == a[0]: letters[0][i] = a[0] + a[1]
		self.buttons = [[],[]]
		for p in range(2):
			x = 0
			rws = 5
			dsy = 0
			if type in ['NUMPAD','CALC']: rws = 4
			if display: dsy = 1
			for i in range(rws):
				rr = 10
				add = 0
				if type == 'QWERTY' and i in [2,3]: rr = 9
				if type == 'NUMPAD': rr = 3
				if type == 'CALC': rr = 4
				for j in range(rr):
					if x >= len(letters[p]): break
					pp = 1
					if letters[p][x] == ' ': pp = 6
					if letters[p][x] in [0,1,2,3]: pp = 1.5
					self.buttons[p].append([pygame.Rect(add + 20 + (j * sp), 20 + ((i + dsy) * sp),sz * pp,sz),letters[p][x],3])
					if letters[p][x] == ' ': add += sz * 5
					if letters[p][x] in [1,2]: add += sz * 0.5
					x += 1
	
	def events(self,event):
		#if self.pos == 0: self.output = ''
		mp = pygame.mouse.get_pos()
		mr = pygame.Rect(mp[0],mp[1] - self.rect.y,2,2)
		for i in self.buttons[self.page]:
			do = False
			if pygame.Rect.colliderect(mr,i[0]) and event.type == pygame.MOUSEBUTTONDOWN: do = True
			elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[0]: pass #do = True digit from keyboard
			if do:
				#BACKSPACE
				if i[1] == 0:
					if res.TTS: plyer.tts.speak(dtb.TTSTEXT['DELETE'])
					else: res.MIXER[0].play(res.SOUND['MENU_BACK'])
					self.output = self.output[0:-1]
				#CAPS
				elif i[1] == 1:
					self.caps += 1
					if self.caps > 2: self.caps = 0
					if res.TTS: plyer.tts.speak(dtb.TTSTEXT['CAPS' + str(self.caps + 1)])
					else: res.MIXER[0].play(res.SOUND['MENU_GO'])
					res.MIXER[0].play(res.SOUND['MENU_GO'])
				#NEXT PAGE
				elif i[1] == 2:
					self.page += 1
					if self.page > 1: self.page = 0
					if res.TTS: plyer.tts.speak(dtb.TTSTEXT['PAGE'] + ' ' + str(self.page + 1))
					else: res.MIXER[0].play(res.SOUND['MENU_GO'])
				#ENTER
				elif i[1] == 3:
					if res.TTS: plyer.tts.speak(dtb.TTSTEXT['CONFIRM'])
					else: res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.active = False
				else:
					if res.TTS:
						if i[1][self.opt] in dtb.TTSTEXT: vv = dtb.TTSTEXT[i[1][self.opt]]
						else: vv = i[1][self.opt]
						plyer.tts.speak(vv)
					else: res.MIXER[0].play(res.SOUND['TEXT_INPUT'])
					#OPERATIONS
					if self.type == 'CALC' and i[1][self.opt] in '+-÷×=':
						if i[1][self.opt] == '=': self.output = str(eval(self.output.replace('÷','/').replace('×','*')))
						else: self.output += i[1][self.opt]
					#TEXT INPUT
					else:
						if len(i[1]) > 1: self.hold += 1
						if self.caps == 0: self.output += i[1][self.opt]
						else:
							self.output += i[1][self.opt].upper()
							if self.caps == 1: self.caps = 0
				i[2] = 0
	
	def scroll(self):
		if self.active and self.rect.y < self.rect.height: self.rect.y += 10
		if self.active == False and self.rect.y > 0: self.rect.y -= 10

	def draw(self):
		self.surface.fill((0,0,0))
		
		if self.display: self.surface.blit(self.font.render(self.output,1,res.COLOR),(10,10))
		r = 0
		for i in self.buttons[self.page]:
			add = 0
			if self.type == 'QWERTY' and r > 19 and r < 29: add = 20
			pygame.draw.rect(self.surface,res.COLOR,pygame.Rect(add + i[0].x,i[0].y,i[0].width,i[0].height),i[2])
			if i[1] == 0: self.surface.blit(self.font.render('<X>',1,res.COLOR),(add + i[0].x + 8,i[0].y))
			elif i[1] == 1: self.surface.blit(self.font.render(str(self.caps) + '^',1,res.COLOR),(add + i[0].x + 8,i[0].y))
			elif i[1] == 2: self.surface.blit(self.font.render(str(self.page + 1) + '/2',1,res.COLOR),(add + i[0].x + 8,i[0].y))
			elif i[1] == 3: self.surface.blit(self.font.render('&',1,res.COLOR),(add + i[0].x + 8,i[0].y))
			else:
				if self.caps == 0: txt = i[1][0]
				else: txt = i[1][0].upper()
				self.surface.blit(self.font.render(txt,1,res.COLOR),(add + i[0].x + 8,i[0].y))
			i[2] = 3
			r += 1
		
		return self.surface

class Backgrounds:
	def __init__(self,size,type):
		self.surface = pygame.Surface(size)
		self.rect = pygame.Rect(0,0,600,600)
		self.font = pygame.font.SysFont("Arial", 64)
		self.type = type
		self.show = False

		self.btime = 100
		self.banimation = {'INDEX': None, 'GIF': 0}
		self.bbg = {'IMAGE': None, 'X': 0, 'ACC': 0, 'DIRECTION': False}

		self.lst = []
		self.img = 0
		self.transform = 4
		self.blink = 0.0
		self.x = 0
		self.palette = [[(196,206,228),(250,0,0)],[(18,46,85),(0,250,0)]]
		if self.type == 'stars':
			self.lst = [[np.random.randint(0,self.surface.get_width()),np.random.randint(0,self.surface.get_height()),np.random.uniform(0.1,1)] for i in range(50)]
		elif self.type in ['mirrors','kaleidoscope']:
			for t in range(14):
				self.lst.append([])
				for r in range(2):
					if r: img = tools.image.reverse(res.BACKG_PATH + 'chp_' + str(t) + '.png')
					else: img = pygame.image.load(res.BACKG_PATH + 'chp_' + str(t) + '.png')
					sz = img.get_width()
					srf = pygame.Surface((sz * 2,sz * 2))
					srf.blit(img, (0,0))
					srf.blit(pygame.transform.flip(img,True,False), (sz,0))
					srf.blit(pygame.transform.flip(img,False,True), (0,sz))
					srf.blit(pygame.transform.flip(img,True,True), (sz,sz))
					self.lst[t].append(srf)
		elif self.type == 'channels':
			for i in range(48): self.lst.append(pygame.transform.scale(tools.image.rgb_channel(res.BACKG_PATH + 'chp_1.png',i),(120,120)))
		elif self.type == 'tunnel':
			img = tools.image.glitch(res.BACKG_PATH + 'chp_5.png').convert()
			rpt = 16
			for i in range(rpt): self.lst.append(pygame.transform.scale(img,(int(img.get_width()/rpt) * i,int(img.get_height()/rpt) * i)))
		
	def random(self,i=None):
		from mutagen.mp3 import MP3
		self.msc.pause()
		pygame.mixer.music.pause()
		res.MIXER[1].play(tools.mixer.noise(),-1)
		kp = str(self.tv)
		self.tv = 0
		self.rectrot = 0
		self.img = self.bbgs[0]
		chg = round(np.random.randint(0,100))
		if kp == '0': chg = 100
		elif i != None: chg = 100
		if self.mnu < 6 and self.lopt != -1:
			self.wait = round(np.random.randint(10,100))
			for i in range(round(np.random.randint(1,30)/res.FPS)): self.run()
			self.ton.stop()
			#CHANGE IMAGE
			if chg > 25:
				if self.lopt == -1: self.tv = 0
				elif self.mnu == 3:
					if self.lopt < len(res.FILES[1]) - 1:
						self.tv = round(np.random.randint(0,res.FILES[1][self.lopt])) + 1
					else: self.tv = len(self.bbgs)
				elif self.mnu == 4:
					self.tv = self.lopt + 1
			else: self.tv = int(kp)
			if self.tv >= len(self.bbgs): self.bbgs[0]
			else: self.img = self.bbgs[self.tv]
			#CHANGE SONG
			if chg > 50:
				self.msc.stop()
				pygame.mixer.music.stop()
				rd = round(np.random.randint(0,res.RANGE_RADIO - 1))
				if len(res.RADIO[rd]) > 0:
					sng = round(np.random.randint(0,len(res.RADIO[rd]) - 1))
					msc = res.MUSIC_PATH + res.RADIO[rd][sng] + '.mp3'
					if msc.endswith('.mp3'):
						audio = MP3(msc)
						pygame.mixer.music.load(msc)
						pygame.mixer.music.play(1,round(np.random.randint(20,int(audio.info.length) - 20)))
						try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
						except: self.mscinfo = {'TITLE': res.RADIO[rd][sng],'ARTIST': 'unknown','ALBUM': 'unknown'}
					elif msc.endswith('.wav'):
						audio = pygame.mixer.Sound(msc)
						res.MIXER[2].play(audio)
					elif msc.endswith('.ogg'):
						audio = pygame.mixer.Sound(msc)
						res.MIXER[2].play(audio)
			else: self.msc.unpause(); pygame.mixer.music.unpause()
			#CHANGE TRANSFORMATION
			if chg > 75:
				self.transform['VALUE'] = 0
				self.transform['TYPE'] = round(np.random.randint(2,3))
				spd = round(np.random.randint(0,100))
				if self.transform['TYPE'] == 5: self.transform['SPEED'] = 2
				elif spd > 75: self.transform['SPEED'] = -2
				elif spd > 50: self.transform['SPEED'] = 2
				elif spd > 25: self.transform['SPEED'] = -1
				else: self.transform['SPEED'] = 1
				if self.transform['TYPE'] in [0,4] and self.transform['SPEED'] < 0: self.transform['VALUE'] = round(np.random.randint(200,300))
				if self.transform['TYPE'] == 5: self.transform['VALUE'] = round(np.random.randint(1,2))
				if self.transform['TYPE'] in [1,4]:
					self.rectrot = self.img.get_rect(center=pygame.Rect(0,0,600,400).center)
	
	def inside_events(self,pressed,mouse): pass

	def outside_events(self,pressed): pass

	def menu(self):
		self.screen.fill((0,0,0))
		for i in self.display: i.fill((0,0,0,0))
		rztxt = np.floor((self.windoww/300)/2)
		#RANDOM SCREEN
		if self.mnu not in [6,5,9,10] and self.classrun and self.sltt == 140 and self.img != None:
			#RANDOM FONT
			if self.rndtxt < (100 + round(np.random.randint(5,20))): self.rndtxt += 1
			else: self.rndtxt = 0
			if self.rndtxt >= 100:
				dt = res.FONTS.keys()
				lst = []
				for i in dt: lst.append(i)
				self.curfnt = lst[round(np.random.randint(0,len(res.FONTS) - 1))]
			else: self.curfnt = 'DEFAULT'
			area = (0,-self.winbar,self.windoww,self.windowh - self.winbar)
			#NOISE
			if self.tv in [0,len(self.bbgs)]:
				self.noise += 1
				if self.noise == 3: self.noise = 0
				self.surface.blit(self.img[self.noise], (0, 0))
			else:
				self.transform['VALUE'] += self.transform['SPEED'] * res.FPS
				if self.blink < (100 + round(np.random.randint(1,10))): self.blink += 1
				else: self.blink = 0
				img = self.img[np.floor(self.blink/100)]
				#SCALE
				if self.transform['TYPE'] == 0:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform['VALUE'] * 2),img.get_rect().height + round(self.transform['VALUE'] * 2)))
					self.surface.blit(img, (600 - img.get_rect().width, 600 - img.get_rect().height),area)
				#ROTATE
				elif self.transform['TYPE'] == 1:
					img = pygame.transform.scale(img,(800,800))
					trs = pygame.transform.rotate(img,self.transform['VALUE'])
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.surface.blit(trs, self.rectrot,area)
				#MOVE HORIZONTAL
				elif self.transform['TYPE'] == 2:
					self.surface.blit(img, (self.transform['VALUE'], int(self.windowh/2) - int(img.get_rect().height/2)))
					if self.transform['VALUE'] < 0: self.surface.blit(img, (img.get_rect().width + self.transform['VALUE'], 0),area)
					if self.transform['VALUE'] > 0: self.surface.blit(img, (-img.get_rect().width + self.transform['VALUE'], 0),area)
				#MOVE VERTICAL
				elif self.transform['TYPE'] == 3:
					self.surface.blit(img, (0, self.transform['VALUE']))
					if self.transform['VALUE'] < 0: self.surface.blit(img, (0, img.get_rect().height + self.transform['VALUE']),area)
					if self.transform['VALUE'] > 0: self.surface.blit(img, (0, -img.get_rect().height + self.transform['VALUE']),area)
				#SCALE AND ROTATE
				if self.transform['TYPE'] == 4:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform['VALUE']/6),img.get_rect().height + round(self.transform['VALUE']/4)))
					trs = pygame.transform.rotate(img,self.transform['VALUE'])
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.surface.blit(trs, self.rectrot,area)
				#RANDOM
				if self.transform['TYPE'] == 5:
					if self.transform['VALUE'] > 13: self.transform['VALUE'] = 1
					img = pygame.image.load(res.BACKG_PATH + 'chp_' + str(self.transform['VALUE']) + str(self.blink) + '.png')
					self.surface.blit(img, (0,0),area)
		
		#INFO
		if self.mnu > 1 and self.mnu < 6:
			'''self.surface.blit(res.FONTS['DEFAULT'].render(dtb.ABOUT[0] + ' ' + res.VERSION + ':' + str(self.glock.get_fps()), True, (240,240,240)), ((-35 + int(self.displayzw/(self.displayzh/self.winbar))), (-35 + self.winbar)))
			if self.stime > 0:
				self.surface.blit(res.FONTS['DEFAULT'].render(dtb.ABOUT[1], True, (240,240,240)), ((self.windoww - 140 - int(self.displayzw/(self.displayzh/self.winbar))), (self.windowh + 35) - self.winbar))'''
			self.surface.blit(res.FONTS[self.curfnt].render(dtb.ABOUT[0][:9], True, (240,240,240)), (50,25))
			self.surface.blit(res.FONTS['MINI'].render(dtb.ABOUT[0][11:] + ' ' + res.VERSION, True, (240,240,240)), (50,55))
			if self.stime > 0:
				self.surface.blit(res.FONTS[self.curfnt].render(dtb.ABOUT[1], True, (240,240,240)), (self.windoww - 200,self.windowh - 35))
			#HOLIDAYS
			for i in dtb.HOLIDAYS:
				if self.holiday.month == i[0] and self.holiday.day == i[1]:
					sz = res.FONTS[self.curfnt].size(i[2])[0] + 50
					self.surface.blit(res.FONTS[self.curfnt].render(i[2], True, (240,240,240)), (self.windoww - sz, 65))
			#SECRETS
			if self.stime > 0: self.stime -= 1 * res.FPS
			if self.stime <= 0:
				if self.sscroll > -20 - res.FONTS[self.curfnt].size(self.stext)[0]:
					self.sscroll -= 3 * res.FPS
					self.surface.blit(res.FONTS[self.curfnt].render(self.stext, True, (240,240,240)),(self.sscroll,self.windowh - 50))
				else:
					self.sscroll = self.windoww + 20
					self.stext = dtb.TSECRETS[np.random.randint(0,len(dtb.TSECRETS) - 1)]
					self.stime = np.random.randint(600,1000)
		#WAIT
		if self.mnu > 0 and self.mnu < 6:
			if self.wait > 0 and self.tv > 0: self.wait -= 1 * res.FPS
			prb = round(np.random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv > 0 and self.sltt == 140: self.random()

		#LOAD GAME RECAP
		if self.mnu == 8:
			if self.wait > 0: self.wait -= 1 * res.FPS
			if self.wait == 0 and self.tv == 0:
				res.MIXER[2].play(pygame.mixer.Sound(res.MUSIC_PATH + 'fate_occurrences.mp3'),-1)
				self.ton.stop()
				self.mnu = 6
		return self.display
	
	def bdraw(self):
		pass
		'''moved background display to Background class
			yy = -(int(res.GSCALE/3) * 10)
			if self.turn == -4:
				self.surfaces[0].blit(self.bbg['IMAGE'], (self.bbg['X'], yy))
				self.surfaces[0].blit(self.bbg['IMAGE'], (self.bbg['X'] - 600, yy))
				if self.display.width > 600:
					self.surfaces[0].blit(self.bbg['IMAGE'], (self.bbg['X'] + 600, yy))
				self.bbg['X'] += 5
				if self.bbg['X'] > 600: self.bbg['X'] = 0
			elif self.bbg['IMAGE'] != None:
				self.surfaces[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5), yy))
				if self.display.width > 595:
					self.surfaces[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5) + 600, yy))
				if self.obstacles:
					self.surfaces[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5) - 600, yy))
					self.bbg['X'] += 5
					if self.bbg['X'] > 600: self.bbg['X'] = 0
					self.bbg['ACC'] = 0
				else:
					if self.bbg['DIRECTION']:
						self.bbg['ACC'] += 0.05
						if self.bbg['ACC'] > 1:
							self.bbg['DIRECTION'] = False
					elif self.bbg['DIRECTION'] == False:
						self.bbg['ACC'] -= 0.05
						if self.bbg['ACC'] < -1:
							self.bbg['DIRECTION'] = True
					self.bbg['X'] += self.bbg['ACC']'''

	def draw(self):
		self.surface.fill((0,0,0))
		sz = 400
		if self.type == 'stars':
			xx = 0; yy = 0
			if self.transform in [1,2,8]: xx = self.x
			if self.transform in [4,5,6]: xx = -self.x
			if self.transform in [2,3,4]: yy = self.x
			if self.transform in [6,7,8]: yy = -self.x
			for i in self.lst:
				pygame.draw.rect(self.surface,(200,200,200),pygame.Rect(i[0] + int(xx * i[2]),i[1] + int(yy * i[2]),2,2))
			self.x += 2
			'''if self.x%120 == 0:
				add = [[np.random.randint(0,self.surface.get_width()),np.random.randint(0,self.surface.get_height()),np.random.uniform(0.1,1)] for i in range(50)]
				for i in add: self.lst.append(i)'''
		elif self.type == 'mirrors':
			bimg = self.lst[self.img][np.floor(self.blink).astype(int)]
			ww = bimg.get_width() - sz
			hh = bimg.get_height() - sz
			if self.transform == 0:
				self.surface.blit(bimg, (0,0),(ww - self.x,0,sz,sz))
				self.surface.blit(pygame.transform.flip(bimg,True,False), (sz,0),(self.x,0,sz,sz))
			if self.transform > 0:
				if self.transform in [1,2]: xx = self.x
				if self.transform in [3,4]: xx = -self.x
				if self.transform in [1,3]: yy = self.x
				if self.transform in [2,4]: yy = -self.x
				self.surface.blit(bimg, (0,0),(ww - xx,hh - yy,sz,sz))
				self.surface.blit(pygame.transform.flip(bimg,True,False), (sz,0),(xx,hh - yy,sz,sz))
				self.surface.blit(pygame.transform.flip(bimg,False,True), (0,sz),(ww - xx,yy,sz,sz))
				self.surface.blit(pygame.transform.flip(bimg,True,True), (sz,sz),(xx,yy,sz,sz))
			self.x += 2
			if self.x > 0:
				self.x = -ww
				self.img += 1
			if self.img > len(self.lst) - 1: self.img = 0
			self.blink += 0.02
			if self.blink >= np.random.randint(1.0,3.0): self.blink = 0.0
		elif self.type == 'channels':
			cc = 0
			for y in range(6):
				for x in range(8):
					self.surface.blit(self.lst[cc], (self.lst[cc].get_width() * x,self.lst[cc].get_height() * y))
					cc += 1
		elif self.type == 'tunnel':
			for i in self.lst[::-1]: self.surface.blit(i,(int(self.surface.get_width()/2) - int(i.get_width()/2),int(self.surface.get_height()/2) - int(i.get_height()/2)))
		
		return self.surface

class MediaPlayer:
	def __init__(self,file):
		self.ext = os.path.splitext(file)[1][1:]
		self.img = None
		self.snd = None
		self.play = 0
		self.stime = 0
		self.offset = [0,0]
		self.zoom = 100
		self.gif = 0.0
		self.optrects = []

		if self.ext in ['png','jpg']:
			self.img = [pygame.image.load(res.SPRITES_PATH + file)]
			self.surface = pygame.Surface((self.img[0].get_width() * 2,self.img[0].get_height() * 2), pygame.SRCALPHA)
		elif self.ext in ['wav','ogg','mp3']:
			self.zoom = 0.5
			self.surface = pygame.Surface((300,400),pygame.SRCALPHA)
			self.snd = pygame.mixer.Sound(file)
			self.img = [tools.mixer.audio_display(self.snd,zoomt=self.zoom)]
		elif self.ext == 'gif':
			import PIL.ImageSequence
			img = PIL.Image.open(res.SPRITES_PATH + file)
			self.surface = pygame.Surface((img.size[0] * 2,img.size[1] * 2), pygame.SRCALPHA)
			self.img = []
			if img.is_animated:
				for i in PIL.ImageSequence.Iterator(img):
					self.img.append(pygame.transform.scale(pygame.image.fromstring(i.tobytes(), img.size, img.mode),(i.size[0] * 2,i.size[1] * 2)))
				self.img = self.img[1:]
			else: self.img = [img]
		
	def inside_events(self,pressed,mouse):
		if self.ext in ['wav','ogg','mp3']:
			if pressed[4][0]:
				if res.MIXER[1].get_busy():
					if self.play: res.MIXER[1].pause(); self.play = 0
					else: res.MIXER[1].unpause(); self.play = 1
				else: res.MIXER[1].play(self.snd); self.play = 1
			if pressed[5][0]: res.MIXER[1].stop(); self.play = 0
							
	def outside_events(self,pressed):
		if self.ext in ['png','jpg']:
			if pressed[0][0] and self.offset[1] > -0.5 * self.zoom: self.offset[1] -= 1
			if pressed[1][0] and self.offset[1] < 0.5 * self.zoom: self.offset[1] += 1
			if pressed[2][0] and self.offset[0] > -0.5 * self.zoom: self.offset[0] -= 1
			if pressed[3][0] and self.offset[0] < 0.5 * self.zoom: self.offset[0] += 1
			if pressed[4][0] and self.zoom < 200: self.zoom += 1
			if pressed[5][0] and self.zoom > 50: self.zoom -= 1

	def draw(self):
		self.surface.fill((0,0,0))
		if self.snd:
			self.surface.blit(self.img[0],(-(int(self.img[0].get_width()/100) * self.stime),0))
			if self.play: self.stime += 1
			if res.MIXER[1].get_busy() == False: self.stime = 0
			pygame.draw.rect(self.surface,res.COLOR,pygame.Rect(0,self.img[0].get_height() + 10,self.surface.get_width(),10))
			pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(int(((self.surface.get_width() - 10)/100) * self.stime),self.img[0].get_height() + 10,10,10))
		elif self.img:
			img = self.img[np.floor(self.gif).astype(int)]
			if self.ext not in ['gif']: img = pygame.transform.scale(img,(int((img.get_width() * 2)/100) * self.zoom,int((img.get_height() * 2)/100) * self.zoom))
			self.surface.blit(img, (int(self.surface.get_width()/2) - int(img.get_width()/2) + self.offset[0], int(self.surface.get_height()/2) - int(img.get_height()/2) + self.offset[1]))
			if len(self.img) > 1:
				self.gif += 0.2
				if self.gif >= len(self.img): self.gif = 0.0
		return self.surface

class VectorialDraw:
	def __init__(self,rect=pygame.Rect(0,0,300,300)):
		self.surface = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
		self.rect = rect
		self.font = pygame.font.SysFont("Arial", 64)
		self.type = 'spiral'
		self.index = 0
		self.show = False
		self.wait = 0
		self.gif = 1 
		self.crc = 0
	
	def inside_events(self,pressed,mouse): pass

	def outside_events(self,pressed): pass
		
	def draw(self):
		self.surface.fill((0,0,0,0))
		sz = 50
		cc = 300
		col = (200,200,200)
		st = 5

		if self.type == 'spiral':
			rng = 1
			for i in range(self.gif * 2):
				pos = ((np.cos(((np.pi * 2)/100) * (i + self.crc)) * i) + cc,(np.sin(((np.pi * 2)/100) * (i + self.crc)) * i) + cc)
				if i > 0: pygame.draw.aaline(self.surface,col,prv,pos,st)
				prv = pos
		if self.type in ['arrow','round']:
			rng = 3
			if self.index == 0: vrtx = [(0,10),(5,0),(10,10)]
			if self.index == 1: vrtx = [(5,0),(10,5),(5,10)]
			if self.index == 2: vrtx = [(0,0),(5,10),(10,0)]
			if self.index == 3: vrtx = [(5,0),(0,5),(5,10)]
			for x in range(4):
				for i in range(len(vrtx)):
					ani = (self.gif/8) * (x + 1)
					pos = ((vrtx[i][0] * ani) + cc - (5 * ani),(vrtx[i][1] * ani) + cc - (5 * ani))
					if i > 0: pygame.draw.aaline(self.surface,col,prv,pos,st)
					prv = pos
		if self.type == 'lines':
			rng = 0
			if self.index == 0: vrtx = [(0,0),(2,5)]
			for i in range(len(vrtx)):
				pos = ((vrtx[i][0] * sz) + cc,(int(vrtx[i][1]/self.gif) * sz) + cc)
				if i > 0: pygame.draw.aaline(self.surface,col,prv,pos,st)
				prv = pos
		if self.type == 'wave':
			rng = 0
			aa = 50
			ff = 4
			w = self.surface.get_width() * 2
			for i in range(w):
				if self.index < 8: y = (aa * np.cos(((i/w) * 4 * np.pi) * ff)) + 300
				elif self.index == 8: y = (aa * np.tan(((i/w) * 2 * np.pi) * ff)) + 300
				else: y = (aa * int((i/w) * 2 * np.pi * ff) * 2) + 300
				if i > 0: pygame.draw.aaline(self.surface,col,prv,(i - self.gif, y),st)
				prv = (i - self.gif, y)
		if self.type == 'symbol':
			rng = 31
			#FOUR ELEMENTS
			if self.index == 0: vrtx = [(3,1),(1,5),(5,5),(3,1)]
			if self.index == 1: vrtx = [(1,1),(5,1),(3,5),(1,1)]
			if self.index == 2: vrtx = [(3,1),(1,5),(5,5),(3,1),None,(1,3),(5,3),None]
			if self.index == 3: vrtx = [(1,1),(5,1),(3,5),(1,1),None,(1,3),(5,3),None]
			#PENTAGRAM AND HEXAGRAMS
			if self.index == 4: vrtx = [(3,1),(2,5),(5,3),(1,3),(4,5),(3,1)]
			if self.index == 5: vrtx = [(3,1),(1,4),(5,4),(3,1),None,(3,5),(1,2),(5,2),(3,5)]
			if self.index == 6: vrtx = [(3,1),(1,4),(5,2),(3,5),(1,2),(5,4),(3,1)]
			if self.index == 7: vrtx = [(3,1),(1,4),(5,4),(3,1),None,(4,2),(1,3),(2,5),(2,2),(5,3),(4,5),(4,2)]
			if self.index == 8: vrtx = [(3,1),(5,5),(4,2),(1,4),(5,4),(2,2),(4,5),(3,1)]
			if self.index == 9: vrtx = [(2,1),(2,5),(5,2),(1,2),(4,5),(4,1),(1,4),(5,4),(2,1)]
			#TRISKLE
			if self.index == 10: vrtx = [(3,3,5,100),(1,1,5,400,25),(5,1,5,400,50),(3,5,5,400,75),(0,0,0,0)]
			#CROSSES
			if self.index == 11: vrtx = [(3,1),(3,5),None,(1,2),(5,2),None]
			if self.index == 12: vrtx = [(3,1),(3,5),None,(1,4),(5,4),None]
			if self.index == 13: vrtx = [(3,1,1,100),(3,2),(3,4),None,(2,2),(4,2),None]
			#GENDERS
			if self.index == 14: vrtx = [(3,6,2,100),(3,1),(3,4),None,(2,1),(4,3),None,(2,3),(4,1),None]
			if self.index == 15: vrtx = [(3,3,1,100),(4,2),(5,1),None,(4,1),(5,1),(5,2),None]
			if self.index == 16: vrtx = [(3,2,1,100),(3,3),(3,5),None,(2,4),(4,4),None]
			if self.index == 17: vrtx = [(3,3,1,100),(4,2),(5,1),None,(4,1),(5,1),(5,2),None,(3,4),(3,6),None,(2,5),(4,5),None]
			if self.index == 18: vrtx = [(3,3,2,100),(1,3),(1,1),None,(5,3),(5,5),None]
			#TRIA PRIMA
			if self.index == 19: vrtx = [(3,3,2,100),(1,3),(5,3),None]
			if self.index == 20: vrtx = [(3,1,1,200),(3,3,1,100),(3,4),(3,6),None,(2,5),(4,5),None]
			if self.index == 21: vrtx = [(3,3,2,100),(3,4),(3,1),None,(2,2),(4,2),None]
			#SACRED GEOMETRY
			if self.index == 22: vrtx = [(3,1,1,100),(2,2,1,100),(4,2,1,100),(2,3,1,100),(4,3,1,100),(3,4,1,100),(2,0,1,100)]
			#AIM
			if self.index == 23: vrtx = [(3,3,1,100),(0,0,0,0)]
			if self.index == 24: vrtx = [(3,1),(3,5),None,(1,3),(5,3),None]
			if self.index == 25: vrtx = [(3,1),(3,2),None,(1,3),(2,3),None,(5,3),(4,3),None,(3,4),(3,5),None]
			if self.index == 26: vrtx = [(3,3,1,100),(3,1),(3,2),None,(1,3),(2,3),None,(5,3),(4,3),None,(3,4),(3,5),None]
			if self.index == 27: vrtx = [(3,2,1,100),(1,3),(3,4),(5,3),None]
			if self.index == 28: vrtx = [(2,1),(4,1),(3,2),(2,1),None,(2,5),(4,5),(3,4),(2,5)]
			if self.index == 29: vrtx = [(1,2),(1,4),(2,3),(1,2),None,(5,2),(5,4),(4,3),(5,2)]
			if self.index == 30: vrtx = [(1,3,3,200),(5,3,3,200),(0,0,0,0)]
			if self.index == 31: vrtx = [(3,1,3,200),(3,5,3,200),(0,0,0,0)]
			for i in range(len(vrtx)):
				if vrtx[i] != None:
					if len(vrtx[i]) == 4: vrtx[i] = (vrtx[i][0] * sz,vrtx[i][1] * sz,vrtx[i][2] * sz,vrtx[i][3])
					else: vrtx[i] = (vrtx[i][0] * sz,vrtx[i][1] * sz)
			for i in range(len(vrtx) - 1):
				if vrtx[i] and vrtx[i + 1] != None:
					rd = ((2 * 3.14)/360) * self.crc
					if len(vrtx[i]) >= 4:
						if len(vrtx[i]) > 4: ang = vrtx[i][4]
						else: ang = 1
						org = (((vrtx[i][0] - (sz * 3)) * np.cos(rd) + (vrtx[i][1] - (sz * 3)) * np.sin(rd)) + cc,
							(-(vrtx[i][0] - (sz * 3)) * np.sin(rd) + (vrtx[i][1] - (sz * 3)) * np.cos(rd)) + cc)
						pygame.draw.ellipse(self.surface,col,(org[0],org[1],10,10))
						for c in range(self.gif):
							pos = ((np.cos(((np.pi * 2)/(vrtx[i][3] * sz)) * (ang + c + self.crc) * sz) * vrtx[i][2]) + org[0],
								(np.sin(((np.pi * 2)/(vrtx[i][3] * sz)) * (ang + c + self.crc) * sz) * vrtx[i][2]) + org[1])
							if c > 0: pygame.draw.aaline(self.surface,col,prv,pos,st)
							prv = pos
					else:
						nxt = (vrtx[i][0] + int(((vrtx[i + 1][0] - vrtx[i][0])/100) * self.gif),
								vrtx[i][1] + int(((vrtx[i + 1][1] - vrtx[i][1])/100) * self.gif))
						cor1 = (((vrtx[i][0] - (sz * 3)) * np.cos(rd) + (vrtx[i][1] - (sz * 3)) * np.sin(rd)) + cc,
							(-(vrtx[i][0] - (sz * 3)) * np.sin(rd) + (vrtx[i][1] - (sz * 3)) * np.cos(rd)) + cc)
						cor2 = (((nxt[0] - (sz * 3)) * np.cos(rd) + (nxt[1] - (sz * 3)) * np.sin(rd)) + cc,
							(-(nxt[0] - (sz * 3)) * np.sin(rd) + (nxt[1] - (sz * 3)) * np.cos(rd)) + cc)

						pygame.draw.line(self.surface,col,cor1,cor2,st)
						pygame.draw.circle(self.surface,col,cor1,10)
						pygame.draw.circle(self.surface,col,cor2,10)
		self.crc += 0
		if self.crc >= 360: self.crc = 0
		if self.gif < 100: self.gif += 2
		elif self.wait < 50: self.wait += 1
		elif self.index < rng: self.index += 1; self.gif = 0; self.wait = 0
		else: self.index = 0; self.gif = 0; self.wait = 0
		
		return self.surface

class Pseudo3d:
	def __init__(self,rect=pygame.Rect(0,0,300,300),dots=True):
		self.surface = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
		self.rect = rect
		self.clock = pygame.time.Clock()
		self.show = False
		self.axis = [0,0,0]
		self.index = 3
		self.center = [(2,2,2),(2,2,2),(2,2,2),(3,3,3),(2,2,2),(2,2,2)]
		self.dots = dots
		self.faces = []
		self.textures = []
		self.donetextures = {}

		#TETRAEDRO
		if self.index == 0:
			self.vrtx = [[1,4,1],[4,4,1],[2,4,4],[2,1,2]]
			self.edges = [[0,1],[1,2],[2,0],[0,3],[1,3],[2,3]]
			self.faces = [[0,1,2],[0,1,3],[1,2,3],[2,0,3]]
			self.textures = ['SS1.jpg','SS1.jpg','SS1.jpg','SS1.jpg']
		#PIRÂMIDE
		if self.index == 1:
			self.vrtx = [[1,4,1],[4,4,1],[4,4,4],[1,4,4],[2,1,2]]
			self.edges = [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]]
		#OCTAEDRO
		if self.index == 2:
			self.vrtx = [[1,2,1],[3,2,1],[3,2,3],[1,2,3],[2,1,2],[2,3,2]]
			self.edges = [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4],[0,5],[1,5],[2,5],[3,5]]
		#HEXAEDRO REGULAR
		if self.index == 3:
			self.vrtx = [[1,1,1],[4,1,1],[4,4,1],[1,4,1],[1,1,4],[4,1,4],[4,4,4],[1,4,4]]
			self.edges = [[0,1],[1,2],[2,3],[3,0],[0,4],[1,5],[2,6],[3,7],[4,5],[5,6],[6,7],[7,4]]
			self.faces = [[0,1,2,3],[4,5,6,7],[4,5,1,0],[6,7,3,2],[1,5,6,2],[4,0,3,7]]
			#self.textures = ['SS1.jpg','SS1.jpg','SS1.jpg','SS1.jpg','SS1.jpg','SS1.jpg']
		#DODECAEDRO
		if self.index == 4:
			self.vrtx = [[3,2,1],[5,3,1],[4,4,1],[1,4,1],[3,2,1]]
			self.edges = []
		#ICOSAEDRO
		if self.index == 5:
			self.vrtx = [[3,0,2],[5,1,2],[5,3,2],[3,4,2],[1,3,2],[1,1,2],
				[2,1,1],[4,1,1],[3,3,1],[3,1,4],[2,3,4],[4,3,4]]
			self.edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],
				[6,7],[7,8],[8,6],[9,11],[11,10],[10,9],
				[0,6],[0,7],[1,7],[2,7],[2,8],[3,8],[4,8],[4,6],[5,6],
				[0,9],[1,9],[1,11],[2,11],[3,11],[3,10],[4,10],[5,10],[5,9]]

	def inside_events(self,pressed,mouse): pass

	def outside_events(self,pressed):
		if pressed[0][0]: self.axis[0] += 0.1
		if pressed[1][0]: self.axis[0] -= 0.1
		if pressed[2][0]: self.axis[1] += 0.1
		if pressed[3][0]: self.axis[1] -= 0.1
		if pressed[4][0]: self.axis[2] += 0.1
		if pressed[5][0]: self.axis[2] -= 0.1
				
	def rotate(self,vrtx,theta,axis):
		sinTheta = np.sin(theta);
		cosTheta = np.cos(theta);
		
		for n in range(len(vrtx)):
			x = vrtx[n][0] - self.center[self.index][0]
			y = vrtx[n][1] - self.center[self.index][1]
			z = vrtx[n][2] - self.center[self.index][2]
			if axis == 'x':
				vrtx[n][1] = y * cosTheta - z * sinTheta
				vrtx[n][2] = z * cosTheta + y * sinTheta
			if axis == 'y':
				vrtx[n][0] = x * cosTheta + z * sinTheta
				vrtx[n][2] = z * cosTheta - x * sinTheta
			if axis == 'z':
				vrtx[n][0] = x * cosTheta - y * sinTheta
				vrtx[n][1] = y * cosTheta + x * sinTheta
			
		return vrtx

	def textureGet(self,file,vrtx):
		vv = ''
		for i in vrtx: vv += '.' + str(i[0]) + ':' + str(i[1])
		txtstr = file + vv
		if txtstr in self.donetextures: return self.donetextures[txtstr]
		else:
			print(txtstr)
			img = PIL.Image.open(file)
			pa = [(0,0),(img.size[0],0),img.size,(0,img.size[1])]
			#vrtx = [(0,0),(img.size[0],-200),(img.size[0],img.size[1] + 200),(0,img.size[1])]
			m = []
			for p1, p2 in zip(pa,vrtx):
				m.append([p1[0],p1[1],1,0,0,0,-p2[0] * p1[0],-p2[0] * p1[1]])
				m.append([0,0,0,p1[0],p1[1],1,-p2[1] * p1[0],-p2[1] * p1[1]])
			A = np.matrix(m, dtype=float)
			B = np.array(vrtx).reshape(8)
			coffs = np.array(np.dot(np.linalg.inv(A.T * A) * A.T, B)).reshape(8)
			img = img.transform(img.size,PIL.Image.PERSPECTIVE,coffs,PIL.Image.BICUBIC)
			srf = pygame.image.fromstring(img.tobytes(),img.size,img.mode).convert()
			self.donetextures[txtstr] = srf
			return srf

	def draw(self):
		self.surface.fill((0,0,0))
		sz = 30
		cc = 200
		lst = self.rotate([i.copy() for i in self.vrtx],self.axis[0],'x')
		lst = self.rotate(lst,self.axis[1],'y')
		lst = self.rotate(lst,self.axis[2],'z')
		col = ((200,10,10),(10,200,10),(10,10,200),(200,200,10),(10,200,200))
		c = 0
		for e in range(len(self.faces)):
			if len(self.faces[e]) < 4: self.faces[e].append(0)
			args = []
			txt = []
			for v in self.faces[e]:
				node = lst[v]
				args.append(((node[0] * sz) + cc, (node[1] * sz) + cc))
				txt.append((int(node[0] * sz),int(node[1] * sz)))
			#txt[-1] = (10,10)
			if self.textures and e < 4: self.surface.blit(self.textureGet(self.textures[e],txt),args[0])
			else: pygame.draw.polygon(self.surface,col[c],args)
			if self.dots: pygame.draw.circle(self.surface,(200,200,200),args[0],5)
			c += 1
			if c > len(col) - 1: c = 0
		for e in range(len(self.edges)):
			n0 = self.edges[e][0]
			n1 = self.edges[e][1]
			node0 = lst[n0]
			node1 = lst[n1]
			cor1 = ((node0[0] * sz) + cc, (node0[1] * sz) + cc)
			cor2 = ((node1[0] * sz) + cc, (node1[1] * sz) + cc)
			pygame.draw.line(self.surface,(200,200,200),cor1,cor2)
		return self.surface

class Files:
	def __init__(self,rect):
		self.surface = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
		self.rect = rect
		self.show = False
		self.wdw = None
		self.curfnt = 'DEFAULT'
		self.opt = 0
		self.mnu = 0
		self.scroll = 0
		self.txt = []
		self.classrun = True
		self.gmtim = []

		#self.grd = [self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0)),
		#self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0))]
		
		res.recent_data(0)
		self.optrects = []
		for i in range(len(res.FILES)):
			ss = np.floor(res.FILES[i][2]/1000).astype(int)
			mm = 0
			hh = 0
			while ss > 60: ss -= 60; mm += 1
			while mm > 60: mm -= 60; hh += 1
			self.gmtim.append(tools.text.digitstring(hh,2) + ' : ' + tools.text.digitstring(mm,2) + ' : ' + tools.text.digitstring(ss,2))
		for i in range(15): self.optrects.append(pygame.Rect(0,0 + (i * 101),rect.width,100))
		self.grd = [tools.draw.gradient((rect.width,200),(0,0,0,200),(0,0,0,0)),
		tools.draw.gradient((rect.width,200),(0,0,0,200),(0,0,0,0))]
	
	def inside_events(self,pressed,mouse):
		mouse.x -= self.rect.x
		mouse.y -= self.rect.y
		rng = [4,6,len(res.FILES),res.FILES[res.ID][2] + 2,len(res.FILES),0,0]
		if self.wdw:
			self.wdw.inside_events(pressed,mouse)
			if self.wdw.gui == None: self.wdw = None
		#MOUSE
		if res.MOUSE > 0:
			#SELECT FILES
			if not self.wdw:
				self.opt = -1
				for i in range(rng[self.mnu]):
					if pygame.Rect.colliderect(mouse,pygame.Rect(self.optrects[i].x,self.optrects[i].y - self.scroll,self.optrects[i].width,self.optrects[i].height)):
						self.opt = i
						if pressed[4][0]: #and self.optrects[i].width == 250:
							#TITLE AND PAUSE MENU
							if self.mnu in [0,1]:
								if self.mnu == 1: lst = [0,1,2,3,4,5]
								else: lst = [1,3,4,5]
								if lst[i] == 0: self.show = False; res.PAUSE = 0 #CONTINUE
								if lst[i] == 1: self.mnu = 2 #LOAD GAME
								if lst[i] == 2: self.mnu = 4 #SAVE GAME
								if lst[i] == 3: self.wdw = Popup('Settings') #SETTINGS
								if lst[i] == 4: self.wdw = Popup('About') #ABOUT
								if lst[i] == 5: pygame.quit(); exit() #EXIT GAME
							#FILE SELECT
							elif self.mnu in [2,4]:
								#SELECT GAME
								if i < len(res.FILES):
									res.ID = self.opt
									self.opt = -1
									self.mnu = 3
								#NEW GAME
								else:
									res.ID = self.opt
									res.MIXER[0].play(res.SOUND['FILE_NEW'])
									res.new_data()
									#res.recent_data(2,self.opt)
									pygame.mixer.music.fadeout(3000)
									self.msc.fadeout(3000)
									self.ton.fadeout(3000)
									self.mnu = 7
							#CHAPTER SELECT
							elif self.mnu == 3:
								#LOAD GAME
								if i < res.FILES[res.ID][2] + 1:
									res.MIXER[0].play(res.SOUND['FILE_LOAD'])
									res.load_data()
									res.CHAPTER = self.opt
									self.msc.stop()
									self.scroll = int(50/res.GSCALE)
									self.wait = 50
									self.mnu = 8
									self.txt = tools.text.wrap(dtb.CHAPTERS[res.CHAPTER][2],res.FONTS['RECAP'],self.surface.get_width() - 200)
								#DELETE GAME
								else:
									res.MIXER[0].play(res.SOUND['FILE_DELETE'])
									res.delete_data()
									self.mnu -= 1
									self.scroll = 0
			#KEYBOARD
			if res.MOUSE < 2:
				if pressed[4][0]:
					if self.mnu == 4: self.mnu = 3
				#SELECT
				if pressed[0][0] and self.mnu == 3: self.opt -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[1][0] and self.mnu == 3: self.opt += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])

			#RANGE LIMIT
			if res.MOUSE == 0:
				if self.opt < 0: self.opt = rng[self.mnu]
				if self.opt > rng[self.mnu]: self.opt = 0
	
	def outside_events(self,pressed):
		if self.wdw: self.wdw.outside_events(pressed)
	
	def draw(self):
		self.surface.fill((0,0,0,0))
		rng = [4,6,len(res.FILES),res.FILES[res.ID][2] + 2,len(res.FILES),0,0]
		#FILES/CHAPTERS MENU
		scrl = 0
		for i in range(rng[self.mnu]):
			if self.opt == i:
				if self.optrects[i].width < self.rect.width:
					self.optrects[i].width += 4
					self.optrects[i].x -= 4
				if self.optrects[i].y > int(self.surface.get_height()/2): scrl = -(self.optrects[i].height * i)
				else: scrl = int(self.surface.get_height()/2) - int(self.optrects[i].height/2) - self.optrects[i].y
				col = (255,255,0)
			else:
				if self.optrects[i].width > self.rect.width - 20:
					self.optrects[i].width -= 4
					self.optrects[i].x += 4
				col = (255,255,255)
			shd = pygame.Surface((self.optrects[i].width,self.optrects[i].height))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.surface.blit(shd,(self.optrects[i].x + 5,self.optrects[i].y + 5 + self.scroll))
			pygame.draw.rect(self.surface, col, pygame.Rect(self.optrects[i].x,self.optrects[i].y + self.scroll,self.optrects[i].width,self.optrects[i].height))
			#TITLE AND PAUSE
			if self.mnu in [0,1]:
				if self.mnu == 1: lst = ['resume','load_file','save_file','Settings','About','exit']
				else: lst = ['load_file','Settings','About','exit']
				self.surface.blit(res.FONTS[self.curfnt].render(dtb.MENU[lst[i]], True, (0,0,0)), (self.optrects[i].x + 10, self.optrects[i].y + 10 + self.scroll))
			#FILES MENU
			if self.mnu in [2,4]:
				if i != len(res.FILES):
					self.surface.blit(res.FONTS[self.curfnt].render(dtb.CHAPTERS[res.FILES[i][2]][0], True, (0,0,0)), (self.optrects[i].x + 10, self.optrects[i].y + 10 + self.scroll))
					self.surface.blit(res.FONTS[self.curfnt].render(self.gmtim[i], True, (0, 0, 0)), (self.optrects[i].x + 10, self.optrects[i].y + 30 + self.scroll))
				else: self.surface.blit(res.FONTS[self.curfnt].render(dtb.MENU['new_file'], True, (0,0,0)), (self.optrects[i].x + 50, self.optrects[i].y + 20 + self.scroll))
			#CHAPTERS MENU
			if self.mnu == 3:
				if i != res.FILES[res.ID][2] + 1:
					self.surface.blit(res.FONTS[self.curfnt].render(dtb.CHAPTERS[i][0], True, (0,0,0)), (self.optrects[i].x + 10, self.optrects[i].y + 10 + self.scroll))
					self.surface.blit(res.FONTS[self.curfnt].render(dtb.CHAPTERS[i][1], True, (0,0,0)), (self.optrects[i].x + 10, self.optrects[i].y + 30 + self.scroll))
				else: self.surface.blit(res.FONTS[self.curfnt].render(dtb.MENU['delete_file'], True, (0,0,0)), (self.optrects[i].x + 70, self.optrects[i].y + 20 + self.scroll))
		#SETTINGS/ABOUT MENU
		if self.wdw: srf = self.surface.blit(self.wdw.draw(),(100,100))
		if self.mnu in [3,4]:
			if self.scroll > scrl and self.scroll - 1 != scrl: self.scroll -= 2
			if self.scroll < scrl and self.scroll + 1 != scrl: self.scroll += 2
		#RECAP
		if self.mnu == 7:
			self.surface.blit(self.bbgs[res.CHAPTER + 1][0], (0,np.floor(-self.scroll)))
			lt = 0
			for y in self.txt:
				self.surface.blit(res.FONTS['RECAP'].render(y, True, (0,0,0)), (101, (self.displayzh - np.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				self.surface.blit(res.FONTS['RECAP'].render(y, True, (0,0,0)), (102, (self.displayzh - np.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				self.surface.blit(res.FONTS['RECAP'].render(y, True, (255,255,255)), (100, (self.displayzh - np.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				lt += 25
			self.scroll += 1 * res.FPS
			if self.scroll > (self.displayzh + int(lt/res.GSCALE)) - int(100/res.GSCALE) or self.skip:
				self.msc.fadeout(5000)
				self.classrun = False
		#LOAD GAME RECAP
		if self.mnu == 8:
			if self.wait > 0: self.wait -= 1 * res.FPS
			if self.wait == 0:
				pygame.mixer.music.play(pygame.mixer.Sound(res.MUSIC_PATH + 'fate_occurrences.mp3'),-1)
				self.mnu = 7
		
		return self.surface

class Inventory:
	def __init__(self,srf=None,typ=0):
		res.FONTS = {**res.FONTS,'DESCRIPTION': pygame.font.Font(res.FONTS_PATH + 'BohemianTypewriter.ttf', 9 * res.GSCALE)}
		self.allowlimit = False
		self.allowtrash = False
		self.allowbag = False
		srf = (400,300)
		if srf:
			self.ratio = [srf,(100,40)]
			self.itbor = pygame.Surface((130, 40))
			self.itbor.fill(res.COLOR)
			for x in range(13):
				for y in range(4):
					self.itbor.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10,y * 10))
			self.surface = pygame.Surface((srf[0] * res.GSCALE,srf[1] * res.GSCALE), pygame.SRCALPHA)
			self.fade = srf[0] + 400
		else: self.surface = pygame.Surface((0,0))
		self.srf = None
		self.hld = 0
		self.spn = 0
		self.itmov = ''
		self.type = typ
		self.opt = [0,0,0,0]
		self.scroll = [0,0]
		self.shake = 0
		self.arrow = 0
		self.arrdir = False
		self.doneimages = {}
		self.exzoom = 0
		self.battle = False
		self.click = pygame.Rect(0,0,0,0)
		xx = 0
		yy = 0
		w = 30 * res.GSCALE
		h = 30 * res.GSCALE
		b = 2
		ptinv = [res.INVENTORY[x] for x in range(len(res.INVENTORY)) if x in res.PARTY[res.FORMATION]]
		lst = [[ptinv],[ptinv],[ptinv,res.STORAGE],[ptinv,res.PRODUCTS],[ptinv,res.BASKET],[res.BASKET,res.PRODUCTS]]
		self.optrects = []
		for l in range(len(lst[self.type])):
			x = 10
			y = 45
			self.optrects.append([])
			for u in range(3):
				if self.type < 2: xx = (200 * u * res.GSCALE)
				else: yy = (200 * u)
				self.optrects[l].append([])
				for j in range(5):
					self.optrects[l][u].append([])
					if j == 4: y += 5
					for i in range(5):
						if i == 1: x += 5
						exx = []
						for ex in range(4): exx.append(pygame.Rect(x + xx + (ex * w) + (l * 200),y + yy,w,h))
						self.optrects[l][u][j].append(exx)
						x += w + b
					x = 10
					y += h + b
				x = 10
				y = 45
		img = pygame.image.load(res.ITEMS_PATH + 'shade.png').convert_alpha()
		self.imgs = {'shade': pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE))}
		for i in res.PARTY[res.FORMATION]:
			img = pygame.image.load(res.SPRITES_PATH + 'who_' + str(i) + '.png').convert_alpha()
			self.imgs[i] = pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE))
			
	def dev(self,d=None):
		if d == None:
			it = res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][0]
		else: it = d
		if it == 'phone': dv = Apps(0)
		elif it == 'PDA': dv = Apps(1)
		elif it == 'mp3': dv = 'radio'
		else:
			try: dv = eval(it)
			except: dv = None
		if dv != None: bt = int(res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1])
		else: bt = 0
		
		return [dv,bt]

	def find(self, where, item, act='item'):
		if isinstance(item,list): fnd = []
		else: fnd = None
		for i in range(len(res.INVENTORY)):
			if isinstance(item,str) and fnd != None: break
			able = True
			if where != None:
				if i == where: able = True
				else: able = False
			else: able = True
			if able == True:
				yy = 0
				for y in res.INVENTORY[i]:
					if isinstance(item,str) and fnd != None: break
					xx = 0
					for x in y:
						if isinstance(item,str) and fnd != None: break
						for it in range(len(x[::2])):
							if isinstance(item,str) and fnd != None: break
							if isinstance(item,str) and fnd == None:
								if act == 'item' and x[it] == item: fnd = [x[it],x[it + 1]]
								if act == 'position' and x[it] == item: fnd = (i,yy,xx,it)
								if act == 'value' and x[it].startswith(item): fnd = [(i,yy,xx,it),int(x[it + 1])]
							elif isinstance(item,list):
								if act == 'item' and x[it].startswith(item[0]): fnd.append([x[it],x[it + 1]])
								if act == 'position' and x[it].startswith(item[0]): fnd.append((i,yy,xx,it))
								if act == 'value' and x[it].startswith(item[0]): fnd.append([(i,yy,xx,it),int(x[it + 1])])
						xx += 1
					yy += 1
							
		return fnd

	def add(self, where, item, prp='0000'):
		trigg = False
		for j in range(len(res.INVENTORY[where])):
			if j != 4:
				for i in range(len(res.INVENTORY[where][j])):
					if i != 0 and res.INVENTORY[where][j][i][0] == '_' and trigg == False:
						vi = prp
						if item.startswith('food'):
							dd = res.DATE[0] + int(dtb.ITEMS[item][7][0:2])
							mm = res.DATE[1] + int(dtb.ITEMS[item][7][2:4])
							if dd > 30: dd -= 30; mm += 1
							if mm > 12: dd += 1; mm -= 12
							if dd < 10: dd = '0' + str(dd)
							if mm < 10: mm = '0' + str(mm)
							vi = str(dd) + str(mm)
						res.INVENTORY[where][j][i] = [item,vi]
						trigg = True

	def space(self, where, ex=0, opt=None, lopt=None, inv=0):
		if self.allowlimit:
			if opt != None:
				if self.itmov[0] != 0:
					vlm = dtb.ITEMS[self.itmov[0]][3]
					wei = dtb.ITEMS[self.itmov[0]][4]
				else:
					vlm = dtb.ITEMS[self.itmov[ex]][3]
					wei = dtb.ITEMS[self.itmov[ex]][4]
			else:
				vlm = 0
				wei = 0
			trigg = True
			for y in res.INVENTORY[where][:-1]:
				for x in y[1:]:
					if x[0] != '_':
						vlm += dtb.ITEMS[x[0]][3]
						wei += dtb.ITEMS[x[0]][4]
			if res.INVENTORY[where][4][0][0] != '_':
				if vlm > dtb.ITEMS[res.INVENTORY[where][4][0][0]][3]: trigg = False
				if wei > dtb.ITEMS[res.INVENTORY[where][4][0][0]][4]: trigg = False
			if res.INVENTORY[where][4][0][0] == '_': trigg = False
			if lopt == 4: trigg = True
			elif opt == 0: trigg = True
			
			if inv in [2,3,4,6] and opt > 4: trigg = True
			return trigg
		else: return True
		
	def duration(self,i,u):
		if i[0].startswith('food') and i[0].endswith('wasted') == False:
			if int(i[1][2:4]) <= res.DATE[1]:
				if int(i[1][0:2]) <= res.DATE[0]: i[0] += '_wasted'
		elif i[0].startswith('drink') and i[0].endswith('wasted') == False:
			if int(i[1][2:4]) <= res.DATE[1]:
				if int(i[1][0:2]) <= res.DATE[0]: i[0] += '_wasted'
		elif i[0].startswith('clth'):
			if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
			if int(i[1]) == 0: res.CHARACTERS[u]['HEALTH'] = 3
		elif i[0].startswith('grenade') and int(i[1]) > 0:
			if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
			if int(i[1]) == 0:
				res.MIXER[0].play(res.SOUND['HIT'])
				res.CHARACTERS[u]['VITALITY'] -= dtb.ITEMS[i[0]][5]['DAMAGE']
		elif i[0] == 'cigar' and float(i[1]) > 0: i[1] = str(float(i[1]) - 0.2)
			
	def inside_events(self,pressed,mouse):
		self.click = mouse
		#ACCESORIES SELECT
		if self.itmov != '' and self.itmov[0] == 0:
			for i in range(len(self.optrects[0][self.opt[2]][self.opt[1]][self.opt[0]][self.opt[3]])):
				if pygame.Rect.colliderect(mouse,pygame.Rect(optrct.x - self.scroll[0],optrct.y,optrct.width,optrct.height)):
					self.opt[3] = i
			if pressed[2][0] and self.opt[3] > 1: self.opt[3] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if pressed[3][0] and self.opt[3] < len(self.itmov): self.opt[3] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		#SELECT ITEM
		else:					
			if pressed[2][0]: self.opt[0] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if pressed[3][0]: self.opt[0] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])	
		if self.type < 2:
			if self.opt[0] < 0: self.opt[0] = 4; self.opt[2] -= 1
			if self.opt[0] > 4: self.opt[0] = 0; self.opt[2] += 1
			if self.opt[1] < 0: self.opt[1] = 4
			if self.opt[1] > 4: self.opt[1] = 0
		else:
			if self.opt[0] < 0: self.opt[0] = 9
			if self.opt[0] > 9: self.opt[0] = 0
			if self.opt[0] < 5:
				if self.opt[1] < 0: self.opt[1] = 4; self.opt[2] -= 1
				if self.opt[1] > 4: self.opt[1] = 0; self.opt[2] += 1
			else:
				if self.opt[1] < 0: self.opt[1] = np.ceil(len(res.STORAGE)/5) - 1
				if self.opt[1] > np.ceil(len(res.STORAGE)/5) - 1: self.opt[1] = 0
		if self.opt[2] < 0: self.opt[2] = len(res.PARTY[res.FORMATION]) - 1
		if self.opt[2] > len(res.PARTY[res.FORMATION]) - 1: self.opt[2] = 0

		ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.opt[2]]]
		lst = [res.STORAGE,res.BASKET,res.BASKET,None,res.BASKET,res.PRODUCTS]
		if self.type == 6 and self.opt[0] < 5: it = res.PRODUCTS[self.opt[0] + (self.opt[1] * 5) - 5]
		elif self.opt[0] > 4 and self.type > 1: it = lst[self.type - 2][self.opt[0] + (self.opt[1] * 5) - 5]
		else: it = res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]]

		if pressed[4][0] and self.opt[0] < 4:
			#USING ITEMS
			if self.itmov == '' or self.itmov[0] == 0:
				prb = np.random.randint(0,100)
				#RANDOM BATTLE
				if it[0] in dtb.ITEMENEMIES and prb > 100 - dtb.ITEMENEMIES[it[0]][1]:
					self.dialog([(13,[dtb.ITEMENEMIES[it[0]][0]])])
				#FOOD
				elif it[0].startswith('food_'):
					#if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] not in [4,10]:
					self.actqueue.append({'RECT': self.player[0]['RECT'],'SPEED': 5,'ACT': 0,'BAR': 0,
					'CHARACTER': res.PARTY[res.FORMATION][self.opt[2]],'ITEM': (self.opt[1],self.opt[0])})
					self.soundplay('MENU_GO')
				#DRINK
				elif it[0].startswith('drink') or it[0].startswith('bottle'):
					if it[0].startswith('drink'): drk = it[0]; amt = int(it[1])
					elif it[0].startswith('bottle') and len(it) > 2: drk = it[2]; amt = int(it[3])
					else: drk == None
					if drk != None:
						if ch['FLAW'] == 'lactose intolerant':
							if drk in dtb.LACTOSE_FOOD: good = False
							else: good = True
						else: good = True
						if good:
							res.MIXER[0].play(res.SOUND['HEAL'])
							hl = dtb.ITEMS[drk][5]
							if it in res.CHARACTERS[self.opt[2]]['FAVFOOD']: hl += int(hl/2)
							ch['VITALITY'] += hl
							ch['THIRST'] += dtb.ITEMS[drk][6]
							if it[0].startswith('drink') and res.DISITEMS[it[0]] == 0:
								res.DISITEMS[it[0]] = 1
							if ch['VITALITY'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
								ch['VITALITY'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
						else:
							res.MIXER[0].play(res.SOUND['INCONSCIOUS'])
							ch['HEALTH'] = 10
						if amt > 0: amt -= 1
						if amt == 0:
							if it[0].startswith('bottle'):
								it = it[0:2]
							else:
								if dtb.ITEMS[it[0]][8] != None: it = ['trash_' + dtb.ITEMS[drk][8],'0000']
								else: it = ['_','0000']
							res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]] = it
						self.notification.append({'TEXT': 'hp_' + str(hl), 'COLOR': (255, 0, 0), 'HALIGN': 'left','X': 0})
					else: res.MIXER[0].play(res.SOUND['ERROR'])
				#TOOLS
				elif it[0].startswith('tool_'):
					try: t = self.tilrect[0][(np.floor((self.player[self.opt[2]]['RECT'].y + 15)/self.map.tilewidth) * self.map.width) + np.floor((self.player[p]['RECT'].x + 15)/self.map.tilewidth)]
					except: t = None
					if t != None and len(dtb.ITEMS[it[0]]) > 5:
						if t[0] == dtb.ITEMS[it[0]][5]['UNLOCK']:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
				#GRENADES
				elif it[0].startswith('grenade') and it in res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][1:]:
					res.MIXER[0].play(res.SOUND['MELEE'])
					it = ['_','0000']
					self.opt[2] = 1
					self.type = 0
				#REPELLENTS
				elif it[0].startswith('repellent'):
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					ch['HEALTH'] = 2
					self.waitlst.append(['repellent' + str(res.PARTY[res.FORMATION][self.opt[2]]),self.waitime + dtb.ITEMS[it[0]][5]])
					it = ['_','0000']
				#PILLS
				elif it[0].startswith('pill_'):
					for i in range(len(dtb.PROFNAMES.keys())):
						if it[0].endswith(dtb.PROFNAMES.keys()[i]):
							res.MIXER[0].play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][i] += 1
							it = ['_','0000']
				#ACCESORIES ACCESS
				elif it[0].startswith('phone' or 'wallet' or 'bag' or 'locksmith'):
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.opt[3] = 1
				#TENTS
				elif it[0].startswith('tent_'):
					res.MIXER[0].play(res.SOUND['INVENTORY_CLOSE'])
					self.build = it[0]
					self.type = 0
					if it[1] != 'infinite':
						if int(it[1]) > 0: it = [it[0],str(int(i[1]) - 1)]
						else: it = ['_','0000']
				#EXAMINE
				elif it[0].startswith('newspaper' or 'id_'):
					res.MIXER[0].play(res.SOUND['PAGE_FLIP'])
					if it[0].startswith('id_'): self.read = GUI.ID(res.PARTY[res.FORMATION][self.opt[2]])
					else: self.read = GUI.Newspaper()
				#PAINT TILES
				elif it[0].startswith('til_'):
					res.MIXER[0].play(res.SOUND['INVENTORY_CLOSE'])
					self.paint = dtb.ITEMS[it[0]][5]
					self.player[0]['PAUSE'] = 0
					self.type = 0
					if it[1] != 'infinite':
						if int(it[1]) > 0: it = [it[0],str(int(i[1]) - 1)]
						else: it = ['_','0000']
				#GUI TOOLS
				elif it[0].startswith('guit_'):
					if it[0] == 'guit_save': res.MIXER[0].play(res.SOUND['FILE_SAVE']); self.savemap()
					elif it[0] == 'guit_load': res.MIXER[0].play(res.SOUND['FILE_LOAD']); self.loadmap()
					elif it[0] == 'guit_undo' and self.ihist > 0: res.MIXER[0].play(res.SOUND['MENU_BACK']); self.ihist -= 1
					elif it[0] == 'guit_redo' and self.ihist < len(self.shist): res.MIXER[0].play(res.SOUND['MENU_GO']); self.ihist += 1
					elif it[0] in ['guit_scissors','guit_glue','guit_copy']:
						if it[0] == 'guit_scissors': self.sstore = []
						pos = [0,0]
						for t in self.mapdata['TILES'][self.slayer]:
							if it[0] == 'guit_glue':
								self.mapdata['TILES'][self.slayer][pos[0] * pos[1]] = self.sstore[pos[0] * pos[1]]
							if pos[0] >= self.slctbox[0] and pos[0] < self.slctbox[2]:
								if pos[1] >= self.slctbox[1] and pos[1] < self.slctbox[3]:
									if it[0] in ['guit_scissors','guit_copy']: self.sstore.append(t)
									if it[0] == 'guit_scissors':
										self.mapdata['TILES'][self.slayer][pos[0] * pos[1]] = 0
									pos[0] += 1
							if pos[0] >= self.mapdata['WIDTH']:
								pos[0] = 0; pos[1] += 1
					else:
						res.MIXER[0].play(res.SOUND['INVENTORY_CLOSE'])
						self.guit = dtb.ITEMS[it[0]][5]
						self.player[0]['PAUSE'] = 0
						self.type = 0
				#ERROR
				else: res.MIXER[0].play(res.SOUND['ERROR'])
				if self.battle:
					self.turn += 1
					self.opt[2] = 1
					self.type = 0
			#ACCESORIES EXIT
			elif self.itmov[0] == 0:
				if self.opt[3] == len(self.itmov):
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.itmov = ''
					self.opt[3] = 0
				else: res.MIXER[0].play(res.SOUND['ERROR'])
			#CRAFTING
			elif it[0] != '_':
				craft = False
				if it[0].startswith('bag') and dtb.ITEMS[self.itmov[0]][3] == 1: craft = True
				if it[0].startswith('undr') and dtb.ITEMS[self.itmov[0]][3] == 1: craft = True
				for i in [('clth','clth'),('key','locksmith'),('id_card','wallet'),('credit_card','wallet'),
					('condiment','food'),('drink','bottle'),('acc','gun'),('tool_syringe','drug')]:
					if self.itmov[0].startswith(i[0]) and it[0].startswith(i[1]): craft = True
				#LIGHTER
				if self.itmov[0].startswith('tool_lighter') and int(self.itmov[1]) != 0:
					if it[0] == 'grenade_molotov_cocktail':
						self.itmov[1] = str(int(self.itmov[1]) - 1)
						it[1] = '300'
					if it[0] == 'cigar':
						self.itmov[1] = str(int(self.itmov[1]) - 1)
						it[1] = '500'
				#RECHARGE WEAPONS
				if self.itmov[0].startswith('ammo') and it[0].startswith('gun'):
					if dtb.ITEMS[self.itmov[0]][5] == dtb.ITEMS[it[0]][5]['GAUGE']:
						craft = True
						res.MIXER[0].play(res.SOUND['GUN_RECHARGE'])
						it[3] = dtb.ITEMS[it[0]][5]['CAPACITY']
						if self.opt[1] == 4 and self.opt[0]> 0:
							if int(it[3]) > 0:
								plus = int(98/(dtb.ITEMS[it[0]][5]['CAPACITY']/int(it[3])))
							else: plus = 0
							self.barpp[self.opt[2]][self.opt[0] - 1] = plus
					else: craft = False
				#ADDING ACCESORIES
				if craft:
					for a in range(len(it[::2])):
						if it[a] == '_':
							res.MIXER[0].play(res.SOUND['CRAFT'])
							it[(a + 1) * 2] = self.itmov[0]
							it[((a + 1) * 2) + 1] = self.itmov[1]
							self.itmov = ''
							break
						else: res.MIXER[0].play(res.SOUND['ERROR']); self.shake = 5
				#MERGE ITEMS
				merge = False
				for a in dtb.CRAFTING:
					if it[0] in a[0:2] and self.itmov[0] in a[0:2]:
						res.MIXER[0].play(res.SOUND['CRAFT'])
						it = [a[2],'9999']
						self.itmov = ''
						merge = True
				if merge == False and craft == False: res.MIXER[0].play(res.SOUND['ERROR']); self.shake = 5
				if self.battle:
					self.turn += 1
					self.opt[2] = 1
					self.type = 0
			else: res.MIXER[0].play(res.SOUND['ERROR'])
		#MOVE ITEMS
		if pressed[5][0]:
			#TRASH
			if self.type == 1 and it[0] != '_': it = ['_','0000']; res.MIXER[0].play(res.SOUND['FILE_DELETE'])
			elif self.itmov != '':
				#TAKE SUB-ITEM
				if self.itmov[0] == 0:
					if self.opt[3] < len(self.itmov) and self.itmov[self.opt[3]][0] != '_':
						res.MIXER[0].play(res.SOUND['MENU_GO'])
						self.itmov = [self.itmov[self.opt[3]][0],self.itmov[self.opt[3]][1]]
						for i in range(2): del it[2 * self.opt[3]]
					else: res.MIXER[0].play(res.SOUND['ERROR']); self.shake = 5
				#PLACE ITEM
				elif it[0] == '_' and self.space(res.PARTY[res.FORMATION][self.opt[2]],self.opt[3],self.opt[0],self.opt[1],self.type):
					#CLOTHING
					if self.itmov[0].startswith('clth'):
						self.player[self.opt[2]]['COSTUME'] = self.find(res.PARTY[res.FORMATION][self.opt[2]],['clth'],'position')
					if self.itmov[0].startswith('head'):
						self.player[self.opt[2]]['ACCESORIES'] = self.find(res.PARTY[res.FORMATION][self.opt[2]],['head'],'position')
						if self.itmov[0] == 'head_hairclip':
							if self.opt[0] == 0: hr = 2
							else: hr = 8
							res.CHARACTERS[res.PARTY[res.FORMATION][self.opt[2]]]['HAIR'][1] = hr
							self.player[self.opt[2]]['HAIR'][1] = hr
					#STORAGE
					if self.type == 2:
						chk = True
						for j in res.STORAGE:
							if j[0] == '_': chk = False
						if chk:
							for i in range(5): res.STORAGE.append(['_','0000'])
					res.MIXER[0].play(res.SOUND['EQUIP'])
					if self.type == 4: self.itmov[1] = 'WASHING: ' + str(tools.text.digitstring(hh,2)) + str(tools.text.digitstring(mm,2))
					else: it = self.itmov.copy()
					self.itmov = ''
					if self.battle:
						self.turn += 1
						self.opt[2] = 1
						self.type = 0
				#SWITCH ITEMS
				elif self.space(res.PARTY[res.FORMATION][self.opt[2]],self.opt[3],self.opt[0],self.opt[1],self.type):
					res.MIXER[0].play(res.SOUND['EQUIP'])
					trd = it.copy()
					it = self.itmov
					if self.itmov[0].startswith('clth'):
						self.player[self.opt[2]]['COSTUME'] = dtb.ITEMS[self.itmov[0]][5]
					self.itmov = trd
				#ERROR
				else: res.MIXER[0].play(res.SOUND['ERROR']); self.shake = 5
			#TAKE ITEM
			elif it[0] != '_':
				if self.opt[0] > 4:
					#BUY AND SELL
					if self.type in [6,7]:
						mny = self.find(None,'wallet','value')
						if mny != None and mny[1] >= dtb.ITEMS[it[0]][2]:
							if self.space(res.PARTY[res.FORMATION][0]) == False:
								self.dialog(dtb.DIALOGS['MERCATOR'][2])
							elif self.confirmation() == 1:
								self.add(res.PARTY[res.FORMATION][0],it[0])
								res.MIXER[0].play(res.SOUND['BUY'])
								mny[1] -= int(dtb.ITEMS[it[0]][2] * it[0])
						else:
							res.MIXER[0].play(res.SOUND['ERROR'])
							self.dialog(dtb.DIALOGS['MERCATOR'][1])
					#WASH
					elif self.type == 4:
						if res.TIME[0] >= int(it[2][0:2]):
							if res.TIME[1] >= int(it[2][2:4]): prp = '0100'
							else: prp = '0000'
						else: prp = '0000'
						self.itmov = [it[0],prp]
						del it
				else:
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.itmov = it.copy()
					it = ['_','0000']
			else: res.MIXER[0].play(res.SOUND['ERROR'])
		#DEVICES SHORTCUT
		if pressed[7][0]: res.SHORTCUT = [res.PARTY[res.FORMATION][self.opt[2]],self.opt[1],self.opt[0]]; res.MIXER[0].play(res.SOUND['MENU_GO'])

		if self.type == 6 and self.opt[0] < 5: res.PRODUCTS[self.opt[0] + (self.opt[1] * 5) - 5] = it
		elif self.opt[0] > 4 and self.type > 1: lst[self.type - 2][self.opt[0] + (self.opt[1] * 5) - 5] = it
		else: res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]] = it
		if self.itmov != '' and self.itmov[0] == '_': self.itmov = ''
		
	def outside_events(self,pressed):
		#HINTEXT
		if self.itmov == '': res.HINTEXT = 'INVENTORY_ITEMS'
		elif self.itmov[0] == 0: res.HINTEXT = 'INVENTORY_ACCESORIES'
		else: res.HINTEXT = 'INVENTORY_HOLD'
		#SELECT ITEM
		if self.itmov == '':
			for l in range(len(self.optrects)):
				for u in range(len(self.optrects[l])):
					for j in range(len(self.optrects[l][u])):
						for i in range(len(self.optrects[l][u][j])):
							rct = self.optrects[l][u][j][i][0]
							optrct = pygame.Rect(rct.x + int(rct.width/2) - self.scroll[0],rct.y + int(rct.height*2) - self.scroll[1],rct.width,rct.height)
							if pygame.Rect.colliderect(self.click,optrct):
								self.opt[0] = i
								self.opt[1] = j
								self.opt[2] = u
								if res.INVENTORY[self.opt[2]][self.opt[1]][self.opt[0]][0] != '_':
									res.HOVERTEXT = dtb.ITEMS[res.INVENTORY[self.opt[2]][self.opt[1]][self.opt[0]][0]][0]
		#INVENTORY WHEEL 
		if pressed[4][0]:
			if self.hld < 80: self.hld += 1
		elif self.hld > 0: self.hld -= 1
		
	def itimg(self,it):
		img = None
		if it in self.doneimages: img = self.doneimages[it]
		else:
			for pth in ['./'] + ['./plugins/' + i + '/' for i in os.listdir('plugins')]:
				if it.startswith('letter'): img = pygame.image.load(pth + res.ITEMS_PATH + it + '_H.png')
				elif it.startswith('til_'): img = self.tilset[dtb.ITEMS[it][5]]
				elif it.startswith('clth_') or it.startswith('tool_lighter') or it.startswith('bottle'):
					img = pygame.image.load(pth + res.ITEMS_PATH + it[:-1] + '.png')
					img.fill(res.PALETTES[2][int(it[-1]) - 1],None,pygame.BLEND_RGBA_MULT)
				elif it.endswith('_wasted'):
					img = pygame.image.load(pth + res.ITEMS_PATH + it.replace('_wasted','') + '.png')
					img.fill((50,50,50),None,pygame.BLEND_RGBA_MULT)
				elif it != '_':
					if it.startswith('bed_'):
						img = pygame.image.load(pth + res.ITEMS_PATH + 'bed.png')
						if it.endswith('single'): ad = pygame.image.load(pth + res.ITEMS_PATH + 'wS.png')
						if it.endswith('couple'): ad = pygame.image.load(pth + res.ITEMS_PATH + 'wC.png')
						img.blit(ad,(img.get_width() - ad.get_width() - 1, 1))
					else:
						nrml = False
						for i in ['cage_','tent_']:
							if it.startswith(i):
								img = pygame.image.load(pth + res.ITEMS_PATH + i + '.png')
								if it.endswith('big'): ad = pygame.image.load(pth + res.ITEMS_PATH + 'wB.png')
								if it.endswith('medium'): ad = pygame.image.load(pth + res.ITEMS_PATH + 'wM.png')
								if it.endswith('small'): ad = pygame.image.load(pth + res.ITEMS_PATH + 'wP.png')
								img.blit(ad,(img.get_width() - ad.get_width() - 1, 1))
								nrml = True
						if nrml == False:
							try: img = pygame.image.load(pth + res.ITEMS_PATH + it + '.png')
							except: img = None
				if img != None: break
		self.doneimages[it] = img
		return pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE))
		
	def wheel(self):
		if self.hld > 40:
			sz = (self.hld - 40) * 2
			srf = pygame.Surface((sz * 2,sz * 2),pygame.SRCALPHA)
			pygame.draw.circle(srf,(0,0,0),(sz,sz),sz)
			self.spn += int((self.spn - (self.opt[0] * 2))/5)
			r = int(sz/2)
			crc = int(2 * np.pi * sz)
			for i in range(4):
				img = None
				offset = [sz,sz]
				if res.INVENTORY[res.PARTY[res.FORMATION][0]][4][i + 1][0] != '_':
					img = self.itimg(res.INVENTORY[res.PARTY[res.FORMATION][0]][4][i + 1][0])
					offset[0] -= int(img.get_width()/2)
					offset[1] -= int(img.get_height()/2)
				xx = int(np.cos(crc * (i + 1)) * r) + offset[0]
				yy = int(np.sin(crc * (i + 1)) * r) + offset[1]
				if self.opt[0] == i + 1: pygame.draw.arc(srf,res.COLOR,pygame.Rect(0,0,sz * 2,sz * 2),crc * i,crc * (i + 1) + 1,5)
				if img: srf.blit(img,(xx,yy))
			return srf
		else: return pygame.Surface((0,0))
		
	def bar(self,where,row,column,orientation):
		lst = []
		if isinstance(row,tuple):
			for x in res.INVENTORY[where][row[0]:row[1]]: lst.append(x[column])
		if isinstance(column,tuple): lst = res.INVENTORY[where][row][column[0]:column[1]]
		if orientation == 'horizontal': srf = pygame.Surface((20 + (len(lst) * 40),50))
		if orientation == 'vertical': srf = pygame.Surface((50,20 + (len(lst) * 40)))
		srf.fill((0,0,0))
		x = 0
		for i in lst:
			if i[0] != '_':
				if orientation == 'horizontal': srf.blit(self.itimg(i[0]),(10 + (x * 40),10))
				if orientation == 'vertical': srf.blit(self.itimg(i[0]),(10,10 + (x * 40)))
			x += 1
		return srf
		
	def examine(self,it):
		if self.exzoom < 100: self.exzoom += 1
		if it in dtb.EXAMINE: img = pygame.image.load(res.SPRITES_PATH + it + '.png')
		else: img = self.itimg(it)
		srf = pygame.transform.scale(img,(int(img.get_width()/100) * self.exzoom,int(img.get_height()/100) * self.exzoom))
		return srf
	
	def draw(self):
		self.surface.fill((0,0,0,0))
		mnc = 0
		dscr = '_'
		#SCROLL
		'''if self.type == 0:
			if self.scroll[0] < (self.opt[2] * 200):
				self.scroll[0] += 40
			if self.scroll[0] > (self.opt[2] * 200):
				self.scroll[0] -= 40
		if self.scroll[0] < 0: self.scroll[0] = 0'''

		#if self.type in [1,5]: rct.x = self.optrects[mnc][j][i].x - self.scroll[0]
		#else: rct.y = self.optrects[mnc][j][i].y - self.scroll[0]
		#DRAW ITEMS
		ptinv = [res.INVENTORY[x] for x in range(len(res.INVENTORY)) if x in res.PARTY[res.FORMATION]]
		lst = [[ptinv],[ptinv],[ptinv,res.STORAGE],[ptinv,res.PRODUCTS],[ptinv,res.BASKET],[res.BASKET,res.PRODUCTS]]
		ll = 0
		for l in lst[self.type]:
			for n in range(len(l)):
				vlm = 0
				wei = 0
				for j in range(len(l[n])):
					for i in range(len(l[n][j])):
						if ll == 1: it = l[0]
						else: it = l[n][j][i]
						#CHECK BAG
						trigg = False
						if i == 0 or j == 4: trigg = True
						elif self.allowbag:
							if l[n][4][0][0] != '_': trigg = True
						else: trigg = True

						#DRAW RECTS
						if self.opt[0] == i and self.opt[1] == j and self.opt[2] == mnc:
							cl = res.COLOR; trigg = True
							dscr = l[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]]
						elif res.SHORTCUT[0] == n and res.SHORTCUT[1] == j and res.SHORTCUT[2] == i: cl = (255,255,167)
						elif it[0].endswith('_wasted'): cl = (176,255,182)
						elif it[0].startswith('clth_') and int(it[1]) == 0: cl = (176,255,182)
						else: cl = (200,200,200)
						if ll == 1: rct = self.optrects[ll][0][n][j][0]
						else: rct = self.optrects[ll][n][j][i][0]
						if trigg == True:
							pygame.draw.rect(self.surface,cl,rct)
							#ITEM DURATION
							for dr in [['tube',(10,200,10),5],['bottle',(100,100,200),5],['vest',(153,153,153),6],['cigar',(153,153,153),500],
								['gun',(255,183,183),'CAPACITY'],['phone',(255,226,173),3600]]:
								if it[0].startswith(dr[0]) and float(it[1]) > 1.0:
									if self.opt[0] != i or self.opt[1] != j or self.opt[2] != mnc:
										if isinstance(dr[2],str): dv = dtb.ITEMS[it[0]][5][dr[2]]
										elif dr[2] >= 500: dv = int(dr[2])
										else: dv = dtb.ITEMS[it[0]][dr[2]]
										drct = rct.copy()
										drct.height = int(rct.height/(dv/float(it[1])))
										drct.y += rct.height - drct.height
										pygame.draw.rect(self.surface,dr[1],drct)
							#DRAW SPRITES
							if it[0] != '_':
								self.surface.blit(self.itimg(it[0]),(rct.x,rct.y))
								if i > 0 and j < 4:
									vlm += dtb.ITEMS[it[0]][3]
									wei += dtb.ITEMS[it[0]][4]
				#VOLUME AND WEIGHT
				lst = [['volume',vlm],['weight',wei]]
				sz = res.FONTS['DEFAULT'].size(res.CHARACTERS[n]['NAME'])[0]
				if self.type in [0,1]:
					pos = [((55 + (210 * mnc) - self.scroll[0]) * res.GSCALE, 15 * res.GSCALE),((55 + (210 * mnc) - self.scroll[0]) * res.GSCALE, 30 * res.GSCALE),(((40 + (210 * mnc) - self.scroll[0]) * res.GSCALE) - sz, 15 * res.GSCALE)]
				else:
					pos = [(55 * res.GSCALE, (15 + (210 * mnc) - self.scroll[0]) * res.GSCALE),(55 * res.GSCALE, (30 + (210 * mnc) - self.scroll[0]) * res.GSCALE),((40 * res.GSCALE) - sz, (15 + (210 * mnc) - self.scroll[0]) * res.GSCALE)]
				if self.allowlimit:
					for i in range(2):
						self.surface.blit(res.FONTS['DEFAULT'].render(dtb.MENU[lst[i][0]], True, (255, 255, 255)), pos[i])
						pygame.draw.rect(self.surface, (100, 100, 100), pygame.Rect(pos[i][0],pos[i][1],80,10))
						if vlm > 0 and res.INVENTORY[n][4][0][0] != '_':
							pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(pos[i][0],pos[i][1],int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/lst[i][1])),10))
							if self.itmov != '' and self.itmov[0] != 0:
								pygame.draw.rect(self.surface, (200, 10, 10), pygame.Rect(pos[i][0] + int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/lst[i][1])),pos[i][1],int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/dtb.ITEMS[self.itmov[0]][3])),10))
				self.surface.blit(res.FONTS['DEFAULT'].render(res.CHARACTERS[n]['NAME'], True, (255, 255, 255)),pos[2])
				self.surface.blit(self.imgs[n],(pos[2]))
				mnc += 1
			ll += 1
		#HOLDING ITEM
		if self.itmov != '' and self.itmov[0] != '_':
			ox = (self.opt[0] * 32) 
			lox = (self.opt[1] * 32)
			if self.opt[0] > 0: ox += 5
			if self.opt[1] == 4: lox += 5
			if self.opt[0] > 4: ox += 34
			#ITEM MOVE
			if self.itmov[0] != 0:
				img = self.itimg(self.itmov[0])
				if self.type < 2:
					self.surface.blit(self.imgs['shade'], (14 + (self.opt[2] * 200) + ox - self.scroll[0],62 + lox))
					self.surface.blit(img, (10 + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,35 + lox))
				else:
					self.surface.blit(pygame.image.load(res.ITEMS_PATH + 'shade.png'), (14 + ox,62 + (self.opt[2] * 200) + lox - self.scroll[0]))
					self.surface.blit(img, (10 + ox + self.shake,35 + (self.opt[2] * 200) + lox - self.scroll[0]))
			#SUB-ITEMS
			else:
				srf = pygame.Surface((70,40))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.surface.blit(srf, (25 + (self.opt[2] * 200) + ox - self.scroll[0],40 + lox),pygame.Rect(0,0,10 + (len(self.itmov) * 30),40))
				self.surface.blit(self.itbor, (20 + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,35 + lox),pygame.Rect(0,0,10 + (len(self.itmov) * 30),40))
				for it in range(len(res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]][2::2]) + 1):
					if self.opt[3] == it + 1:
						pygame.draw.rect(self.surface, res.COLOR, pygame.Rect(25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,40 + lox,30,30))
						if self.opt[3] != len(self.itmov): dscr = [self.itmov[self.opt[3]][0],res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]][it * 2]]
					else: pygame.draw.rect(self.surface, (255,255,255), pygame.Rect(25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,40 + lox,30,30))
					if it + 1 == len(self.itmov):
						self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'e_run.png'), (25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,40 + lox))
					elif self.itmov[it + 1][0] != '_':
						img = self.itimg(self.itmov[it + 1][0])
						self.surface.blit(img, (25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll[0] + self.shake,40 + lox))
		#ARROWS
		if self.arrdir == False:
			self.arrow += 1
			if self.arrow == 8: self.arrdir = True
		elif self.arrdir == True:
			self.arrow -= 1
			if self.arrow == 0: self.arrdir = False
		if self.type < 2:
			if self.opt[2] > 0: self.surface.blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),270), (0 + self.arrow,110))
			if self.opt[2] < len(res.PARTY[res.FORMATION]) - 1: self.surface.blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),90), ((self.surface.get_width() - 12) - self.arrow,110))
		else:
			if self.opt[2] > 0: self.surface.blit(pygame.transform.flip(pygame.image.load(res.SPRITES_PATH + 'arw.png'),False,True), (80,0 + self.arrow))
			if self.opt[2] < len(res.PARTY[res.FORMATION]) - 1: self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (80,208 - self.arrow))
		
		#TRASH
		if self.type == 1: self.surface.blit(res.FONTS['DESCRIPTION'].render(dtb.MENU['drop'], True, (255, 255, 255)), (20, self.surface.get_height() - 50))
		else:
			#ITEM DESCRIPTION
			if self.itmov != '' and self.opt[3] < len(self.itmov):
				dtp = 1
				if self.itmov[0] != 0:
					for i in ('bag','vest','amulet','melee','gun','grenade'):
						if self.itmov[0].startswith(i):
							dtp = 3
							if dscr[0].startswith(i): dtp = 4
				if self.opt[3] != len(self.itmov) and self.itmov[self.opt[3]][0] in res.DISITEMS:
					if res.DISITEMS[self.itmov[0][0]] == 0: dtp = 2
				if dtp == 1 and dscr[0] == '_': dtp = 0
			elif dscr[0] != '_': dtp = 1
			else: dtp = 0
			if dtp > 0:
				#ITEM DESCRIPTION
				if dtp == 1:
					txt = dtb.ITEMS[dscr[0]][1].copy()
					if self.type == 3 and self.opt[0] > 4: txt[1] += '$' + str(dtb.ITEMS[dscr[0]][2] * dscr[1])
					elif dscr[0].startswith('gun'): txt[1] += ' - ammo: ' + str(dscr[1]) + '/' + str(dtb.ITEMS[dscr[0]][5]['CAPACITY'])
					if dscr[0].startswith('wallet'): txt[1] += ' - $' + str(dscr[1][0:6])
					if dscr[0].startswith('credit_card'): txt[1] += ' - $' + str(dscr[1])
					if dscr[0].startswith('bottle') and len(dscr) > 2: txt[1] += ' - ' + str(dscr[1]) + 'm: ' + str(dtb.ITEMS[dscr[2]][0])
					y = 0
					for t in tools.text.wrap(txt,res.FONTS['DESCRIPTION'],self.surface.get_width() - 40):
						self.surface.blit(res.FONTS['DESCRIPTION'].render(tools.text.dislexic(t), True, (255, 255, 255)), (20, self.surface.get_height() - 80 + y))
						y += 30
				#NOT DISCOVERED
				elif dtp == 2: self.surface.blit(res.FONTS['DESCRIPTION'].render(dtb.MENU['discover'], True, (255, 255, 255)), (20, self.surface.get_height() - 50))
				#ITEM STATS
				elif dtp > 2 and self.itmov[0] != 0:
					xbr = 0
					ybr = 0
					for p in [[['vest','amulet'],'armor',5],[['vest','amulet'],'duration',6],[['tool','melee','gun','grenade'],'damage',5,'DAMAGE'],
					[['gun'],'capacity',5,'CAPACITY'],[['tool','melee','gun'],'recharge',5,'RECHARGE'],[['tool','melee','gun'],'cadency',5,'CADENCY'],
					[['gun'],'gauge',5,'GAUGE'],[['food','drink'],'vitality',5],[['food'],'hunger',6],[['drink'],'thirst',6]]:
						shw = False
						for n in p[0]:
							if self.itmov[0].startswith(n): shw = True
						if shw:
							if len(p) > 3: it = dtb.ITEMS[self.itmov[0]][p[2]][p[3]]
							else: it = dtb.ITEMS[self.itmov[0]][p[2]]
							self.surface.blit(res.FONTS['DESCRIPTION'].render(dtb.MENU[p[1]], True, (255, 255, 255)), (80 + (xbr * 200), self.surface.get_height() - 80 + (ybr * 30)))
							pygame.draw.rect(self.surface,(100,100,100),pygame.Rect(80 + (xbr * 160),self.surface.get_height() - (ybr * 20),50,10))
							pygame.draw.rect(self.surface,(255,255,255),pygame.Rect(80 + (xbr * 160),self.surface.get_height() - (ybr * 20),np.floor(50/it),10))
							if dtp == 4:
								df = np.floor(50/dtb.ITEMS[self.itmov[0]][5]) - np.floor(50/dtb.ITEMS[dscr[0]][5])
								if df != 0:
									if df < 0: pygame.draw.rect(self.surface,(200,10,10),pygame.Rect(80 + (xbr * 160) + np.floor(50/it),self.surface.get_height() - (ybr * 20),abs(df),10))
									if df > 0: pygame.draw.rect(self.surface,(10,200,10),pygame.Rect(80 + (xbr * 160) + np.floor(50/it) - abs(df),self.surface.get_height() - (ybr * 20),abs(df),10))
							ybr += 1
							if ybr == 2:
								xbr += 1
								ybr = 0
		#ITEM SHAKE
		if self.shake > 0: self.shake = -self.shake
		elif self.shake < 0: self.shake = -self.shake - 1
		
		return self.surface

class LevelMenu:
	def __init__(self,sz):
		self.surface = pygame.Surface(sz)
		self.rect = pygame.Rect(0,0,300,300)
		self.show = False
		self.scroll = self.surface.get_width() + 50
		self.inv = Inventory(None)
		self.optrects = []
		dvd3 = np.floor((160 * res.GSCALE)/3)
		for i in range(3): self.optrects.append(pygame.Rect(dvd3 * i,0,dvd3,40))
		self.opt = [0,0]
		self.mnu = 3
		self.hpl = 0

		if self.mnu == 2:
			pygame.mixer.music.fadeout(500)
			res.MIXER[0].play(res.SOUND['BATTLE_LOST'])
		
	def inside_events(self,pressed,mouse):
		for i in range(len(self.optrects)):
			if pygame.Rect.colliderect(mouse,self.optrects[i]): self.opt[0] = i
		if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[2][0]: self.opt[0] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt[0] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])

		if pressed[4][0]:
			if self.mnu == 2:
				res.MIXER[0].play(res.SOUND['MENU_GO'])
				self.inv.find('money')
				#restart level
				res.MAP = 'hospital_0'
				res.PX = 315
				res.PY = 200

		if self.opt[0] < 0: self.opt[0] = 2
		if self.opt[0] > 2: self.opt[0] = 0
					
	def outside_events(self,pressed):
		pass

	def draw(self):
		self.surface.fill((0,0,0))
		if self.scroll > 0: self.scroll -= 10

		#CHAPTER START
		if self.mnu == 0:
			self.surface.blit(res.FONTS['DEFAULT'].render(dtb.CITIES[0][0],True,(200,200,200)),(0,0))
		#LEVEL START
		if self.mnu == 1:
			self.surface.blit(res.FONTS['DEFAULT'].render(dtb.CITIES[0][0],True,(200,200,200)),(0,0))
		#WIN SCREEN
		if self.mnu == 2:
			pd = 200 - (50 * res.GSCALE) + self.scroll
			#LABEL
			if self.hpl < 0: self.surface.blit(res.FONTS['TITLE'].render(dtb.MENU['victory'], True, (255,255,255)), (pd + 30, 100))
			else: self.surface.blit(res.FONTS['TITLE'].render(dtb.MENU['perfect'], True, (255,255,255)), (pd, 100))
			
			#GREENBLOOD
			for it in ['tube100','tube250']:
				btls = self.inv.find(None,it,'value')
				if btls != None:
					break
					if btls[1] >= dtb.ITEMS[res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]][5]: btls = None
			if btls != None:
				it = res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]
				if btls[1] > 0 and int(200/(dtb.ITEMS[it][5]/btls[1])) >= 1:
					pygame.draw.rect(self.surface, (0, 255, 100), pygame.Rect(self.surface.get_width() - pd + 150,300 - int(200/(dtb.ITEMS[it][5]/btls[1])),30,int(200/(dtb.ITEMS[it][5]/btls[1]))))
					if int(btls[1]) < 90:
						pygame.draw.ellipse(self.surface, (32, 219, 166), pygame.Rect(self.surface.get_width() - pd + 40,250 - int(200/(dtb.ITEMS[it][5]/btls[1])),30,13))
					pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(self.surface.get_width() - pd,280 - int(200/(dtb.ITEMS[it][5]/btls[1])),50,20))
					self.surface.blit(res.FONTS['DEFAULT'].render(str(btls[1]) + 'ml', True, (0,0,0)), ((self.surface.get_width() - 5 + pd) * res.GSCALE, (285 - int(200/(dtb.ITEMS[it][5]/int(btls[1])))) * res.GSCALE))
			self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'gbbar.png'), (self.surface.get_width() - pd, 150))
			pygame.draw.ellipse(self.surface,(200,200,200),pygame.Rect(pd + 400, 150,30,15),1)
			pygame.draw.arc(self.surface,(200,200,200),pygame.Rect(pd + 400, 160,30,15),np.pi,np.pi * 2,1)

			ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.opt[0]]]
			#PARTY XP
			for i in range(len(res.PARTY[res.FORMATION])):
				img = pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][i]) + '.png')
				self.surface.blit(pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE)), (pd - 10, 160 + (i * 50)))
				pygame.draw.rect(self.surface, (50, 50, 50), pygame.Rect(pd + 30,160 + (i * 50),200,40))
				if ch['EXPERIENCE'] > 0: pygame.draw.rect(self.surface, (0, 255, 100), pygame.Rect(pd + 30,160 + (i * 50),int(200/(dtb.NEXTLEVEL[ch['LEVEL']]/ch['EXPERIENCE'])),40))
			
			#LEVEL UP
			bw = (self.surface.get_width() * 2) - pd
			if self.opt[1] > 0:
				for i in range(len(dtb.PROFNAMES)):
					#self.surface.blit(res.FONTS['DEFAULT'].render(dtb.BATTLE[39] + ' +' + str(ch['STRENGHT'][ch['LEVEL']] - ch['STRENGHT'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.scroll) * 2, 260))
					pygame.draw.rect(self.surface, (50, 50, 50), pygame.Rect(bw + self.scroll,120,100,15))
					pygame.draw.rect(self.surface, (255, 255, 0), pygame.Rect(bw + self.scroll,120,np.floor(100/(100/(dtb.CLASSES[ch['CLASS']][dtb.PROFNAMES.keys()[i]][ch['LEVEL']] + ch['BONUS'][i]))),15))
					if dtb.CLASSES[ch['CLASS']][dtb.PROFNAMES.keys()[i]][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display, (0, 255, 100), pygame.Rect(bw + self.scroll,120,np.floor(100/(100/(dtb.CLASSES[ch['CLASS']][dtb.PROFNAMES.keys()[i]][ch['LEVEL'] - 1] + ch['BONUS'][i]))),15))
				
				if self.opt[0] == 0: n = np.random.randint(0,6)
				elif self.opt[0] == 1: n = ' '
				else: n = self.opt[0]
				pygame.draw.rect(self.surface, (50, 50, 50), pygame.Rect(bw + 110 + self.scroll,145,15,15))
				self.surface.blit(res.FONTS['DEFAULT'].render(str(n), True, (240,240,240)), ((bw + 115 + self.scroll) * res.GSCALE, 295))
				
				if self.mnu <= 0:
					pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
					pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
				
				self.surface.blit(res.FONTS['TITLE'].render(ch['NAME'].lower(), True, (255,255,255)), (800 + self.scroll, 30))
				self.surface.blit(res.FONTS['DEFAULT'].render(dtb.MENU['level_up'] + str(dtb.CNAMES[ch['CLASS']][ch['LEVEL'] - 1]) + ' !', True, (255,255,255)), ((800 + self.scroll) * res.GSCALE, 70 * res.GSCALE))
		#LOST SCREEN
		elif self.mnu == 3:
			sz = int(self.surface.get_width()/2) - int(res.FONTS['TITLE'].size(dtb.MENU['lost'])[0]/2)
			self.surface.blit(res.FONTS['TITLE'].render(dtb.MENU['lost'], True, (255,255,255)), (sz + self.scroll, 100))
			self.surface.blit(res.FONTS['DEFAULT'].render('-$100', True, (255,255,255)), (sz + self.scroll, 240))
		#LEVEL END
		elif self.mnu == 4:
			pass
		
		return self.surface

class Calendar:
	def __init__(self, size=(160 * res.GSCALE,160 * res.GSCALE)):
		self.surface = pygame.Surface(size, pygame.SRCALPHA)
		self.ratio = [size,(400,400)]
		self.scroll = 0
		self.optrects = []
		dvd3 = np.floor((160 * res.GSCALE)/3)
		for i in range(10):
			self.optrects.append([])
			for y in range(7):
				for x in range(7):
					self.optrects[i].append(pygame.Rect(20 + (x * 41),60 + (y * 31),40,30))
		self.opt = [0,0,0]
		self.mnu = 0
		
	def inside_events(self,pressed,mouse):
		'''for i in range(len(self.optrects[self.mnu])):
			if pygame.Rect.colliderect(mouse,self.optrects[self.mnu][i]): self.opt[0] = i'''
		if pressed[0][0]: self.opt[0] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[0] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[2][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])

		if self.opt[0] < 0: self.opt[0] = len(res.CALENDAR) - 1; self.opt[1] = 0
		if self.opt[0] > len(res.CALENDAR) - 1: self.opt[0] = 0; self.opt[1] = 0
		if self.opt[1] < 0: self.opt[0] -= 1; self.opt[1] = len(res.CALENDAR[self.opt[0]]) - 1
		if self.opt[1] > len(res.CALENDAR[self.opt[0]]) - 1: self.opt[0] += 1; self.opt[1] = 0
		if self.opt[2] < 0: self.opt[1] -= 1; self.opt[2] = len(res.CALENDAR[self.opt[0]][self.opt[1]]) - 1
		if self.opt[2] > len(res.CALENDAR[self.opt[0]][self.opt[1]]) - 1: self.opt[1] += 1; self.opt[2] = 0
					
	def outside_events(self,pressed):
		pass

	def miniature(self):
		ww = self.ratio[1]
		srf = pygame.Surface(ww)
		srf.fill((0,0,0))

		dt = tools.text.digitstring(res.DATE[0],2) + '/' + tools.text.digitstring(res.DATE[1],2) + '/' + tools.text.digitstring(res.DATE[2],2)
		tm = tools.text.digitstring(res.TIME[0],2) + ':' + tools.text.digitstring(res.TIME[1],2) + ':' + tools.text.digitstring(res.TIME[2],2)

		sz = res.FONTS['DEFAULT'].size(dtb.CITIES[0][0])
		srf.blit(res.FONTS['DEFAULT'].render(dtb.CITIES[0][0],True,(200,200,200)),(int(ww[0]/2) - int(sz[0]/2),int(ww[1]/2) - int(sz[1] * 2)))
		sz = res.FONTS['DEFAULT'].size(dt)
		srf.blit(res.FONTS['DEFAULT'].render(dt,True,(200,200,200)),(int(ww[0]/2) - int(sz[0]/2),int(ww[1]/2) - int(sz[1] * 0.5)))
		sz = res.FONTS['DEFAULT'].size(tm)
		srf.blit(res.FONTS['DEFAULT'].render(tm,True,(200,200,200)),(int(ww[0]/2) - int(sz[0]/2),int(ww[1]/2) + int(sz[1] * 1.0)))

		return srf

	def draw(self):
		self.surface.fill((10,10,10,0))
		if self.mnu == 0:
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MONTHS[self.opt[1]].capitalize() + ' ' + str(2005 + self.opt[0]), True, (200,200,200)), (20, 10))
			lst = ['D','S','T','Q','Q','S','S']
			for i in range(7):
				rct = pygame.Rect(self.optrects[self.opt[0]][i].x,self.optrects[self.opt[0]][i].y - 20,self.optrects[self.opt[0]][i].width,20)
				pygame.draw.rect(self.surface,(100,100,100),rct)
				self.surface.blit(res.FONTS['CALIBRI'].render(lst[i], True, (10,10,10)), (rct.x + 10, rct.y))
			col = (200,200,200)
			dd = res.CALENDAR[self.opt[0]][self.opt[1]][self.opt[2]]
			for d in range(7):
				for i in range(7):
					pygame.draw.rect(self.surface,col,self.optrects[self.opt[0]][i + (d * 7)])
					if i + (d * 7) - dd >= 0 and i + (d * 7) - dd < len(res.CALENDAR[self.opt[0]][self.opt[1]]):
						self.surface.blit(res.FONTS['CALIBRI'].render(str(i + (d * 7) - dd + 1), True, (10,10,10)), (self.optrects[self.opt[0]][i + (d * 7)].x + 5, self.optrects[self.opt[0]][i + (d * 7)].y + 5))

		return self.surface

class GPS:
	def __init__(self, mn, rm, tl, pl, en, sig, size=(360,400)):
		self.img = pygame.image.load(res.BACKG_PATH + 'GPS.png')
		self.surface = pygame.Surface(size, pygame.SRCALPHA)
		res.FONTS = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scrpos = (60,49)
		self.rqst = True
		self.ingame = 0
		self.scroll = 0
		self.mp = None
		self.optrects = []
		self.xy = [80,80]
		self.zoom = 200
		
		if res.SIGNAL > 0:
			if self.mp == None:
				ww = 0
				hh = 0
				for t in tl[0]:
					if ww < t[1].x: ww = t[1].x
					if hh < t[1].y: hh = t[1].y
				ww += 30
				hh += 30
				self.mp = pygame.Surface((ww,hh))
				for t in tl[0]:
					if t[0] == 'STONE': pygame.draw.rect(self.mp,(135,135,135),t[1])
					else: pygame.draw.rect(self.mp,(64,64,64),t[1])
				for t in tl[3]:
					pygame.draw.rect(self.mp,(64,64,64),t[1])
				self.mp = pygame.transform.scale(self.mp, (200,200))
		
		self.mn = mn
		self.rm = rm
		self.pl = pl
		self.en = en
		self.sig = sig
		
	def inside_events(self,pressed,mouse):
		pass
		
	def outside_events(self,pressed):
		if pressed[0][0]: self.xy[1] += 3
		if pressed[1][0]: self.xy[1] -= 3
		if pressed[2][0]: self.xy[0] += 3
		if pressed[3][0]: self.xy[0] -= 3
		if pressed[4][0]: self.zoom += 5
		if pressed[5][0]: self.zoom -= 5

		if self.xy[0] < 50: self.xy[0] = 50
		if self.xy[0] > 200: self.xy[0] = 200
		if self.xy[1] < 50: self.xy[1] = 50
		if self.xy[1] > 200: self.xy[1] = 200
		if self.zoom < 50: self.zoom = 50
		if self.zoom > 200: self.zoom = 200
	
	def map(self, pl):
		srf = pygame.Surface((106,106))
		xx = 100 + ((200/self.mp.get_height()) * pl['RECT'].x * self.mp.get_width()/(self.map.width * self.map.tilewidth))
		yy = 100 + ((200/self.mp.get_height()) * pl['RECT'].y * self.mp.get_height()/(self.map.height * self.map.tileheight))
		srf.blit(self.mp,(xx,yy))
		
		return srf
	
	def compass(self):
		if len(res.MARKER) > 0 and res.MARKER[0][0] == res.MAP:
			xx = (self.player[0]['RECT'].x - self.cam.x) - (res.MARKER[0][1] - self.cam.x)
			yy = (self.player[0]['RECT'].y - self.cam.y) - (res.MARKER[0][2] - self.cam.y)
			dir = (xx,yy)
			lth = np.hypot(*dir)
			if lth == 0.0: dir = (0, -1)
			else: dir = (dir[0]/lth,dir[1]/lth)
			img = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'mp_compass.png'),(np.degrees((np.arctan2(-dir[1],dir[0]))) + 90))
			try: self.mpcrct = img.get_rect(center = self.mpcrct.center)
			except: self.mpcrct = img.get_rect(center=pygame.Rect(self.displayzw - 70,20,50,50).center)
			self.surface.blit(img,self.mpcrct)
			if self.colide(self.player[0]['RECT'],pygame.Rect(res.MARKER[0][1] - 40,res.MARKER[0][2] - 40,80,80)):
				del res.MARKER[0]

	def draw(self):
		self.rqst = False
		if self.mn == False: scr = [pygame.Surface((sz,232)),pygame.Surface((sz * 2,464),pygame.SRCALPHA)]
		if self.mn == True: scr = [pygame.Surface((100,100)),pygame.Surface((200,200),pygame.SRCALPHA)]
		for i in scr: i.fill((0,0,0,0))
		if res.SIGNAL > 0:
			mpx = self.xy[0] - int(self.zoom/2)
			mpy = self.xy[1] - int(self.zoom/2)
			scr[0].blit(pygame.transform.scale(self.mp, (self.zoom,self.zoom)), (mpx,mpy))

			xx = (self.pl['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
			yy = (self.pl['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
			scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in res.MARKER:
				xx = (i[1] - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
				yy = (i[2] - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				#if i[0] == rm:
				scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_pin' + str(i[3]) + '.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in self.sig:
				if i[0] == 5:
					xx = (i[1]['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
					yy = (i[1]['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_' + i[1]['ICON'] + '.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in self.en:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				if i['VITALITY'] > 0 and i['RECT'].x > 0 and i['RECT'].y > 0:
					scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_anomaly.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
		else: scr[1].blit(res.FONTS['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (25, 200))

		if self.mn == False:
			pygame.draw.rect(scr[1], (140, 255, 253), pygame.Rect(0,0,sz * 2,80))
			scr[1].blit(res.FONTS['TITLE'].render(dtb.MENU[0], True, (0, 0, 0)), (5, 4))

		return scr

class TextReader:
	def __init__(self,txt):
		self.surface = pygame.Surface((200 * res.GSCALE,200 * res.GSCALE), pygame.SRCALPHA)
		file = []
		with open(txt,'r') as f:
			file += f.readlines()
		txt = tools.text.wrap(file,res.FONTS['DEFAULT'],self.surface.get_width() - 40)
		self.text = []
		for i in range(len(txt)): self.text.append(res.FONTS['DEFAULT'].render(txt[i],True,(10,10,10)))
		self.txtsz = res.FONTS['DEFAULT'].size(txt[0])[1] + 10
		self.scroll = 0
		
	def inside_events(self,pressed,mouse): pass
							
	def outside_events(self,pressed):
		if pressed[0][0] and self.scroll > 0: self.scroll -= 2
		if pressed[1][0] and self.scroll < self.txtsz * len(self.text): self.scroll += 2

	def draw(self):
		self.surface.fill((200,200,200))
		for i in range(len(self.text)):
			self.surface.blit(self.text[i], (10, (10 + (i * self.txtsz)) - self.scroll))
		pygame.draw.rect(self.surface,(10,10,10),pygame.Rect(self.surface.get_width() - 10,0,10,self.surface.get_height()))
		pygame.draw.rect(self.surface,res.COLOR,pygame.Rect(self.surface.get_width() - 10,int((self.surface.get_height()/(self.txtsz * len(self.text))) * (self.scroll + 1)),10,10))
		return self.surface

class Contacts:
	def __init__(self):
		self.img = pygame.image.load(res.BACKG_PATH + 'phone.png')
		self.surface = pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.vkb = Vkeyboard((160 * res.GSCALE,200 * res.GSCALE),type='CALC',display=True)
		self.scrpos = (39,46)
		self.rqst = True
		self.ingame = 0
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.nb = None
		self.credit = 0
		self = Inventory(False)
		self.battery = self.find(res.PARTY[res.FORMATION][0],'phone')
		self.credit = self.find(res.PARTY[res.FORMATION][0],'sim_card','value')
		if self.battery != None: self.battery = int(self.battery[1])
		else: self.battery = 0
		if self.credit != None: self.credit = self.credit[1]
		else: self.credit = 0
		self.mnu = 0
		self.exvar = 0
		
	def inside_events(self,pressed,mouse):
		#SELECT OPTIONS
		if pressed[5][0]: self.vkb.events()
		if self.nb != None:
			if pressed[2][0] and self.opt == 1: self.opt = 0; res.MIXER[0].play(res.SOUND['MENU_VER'])
			if pressed[3][0] and self.opt == 0: self.opt = 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
			if pressed[4][0]:
				self.sfx.stop()
				self.ch_rng.stop()
				if self.opt == 0:
					self.ingame = 4
				elif self.opt == 1:
					res.MIXER[0].play(res.SOUND['MENU_BACK'])
					self.phone = 1
				if self.radonoff == True: pygame.mixer.music.unpause()
				if res.CHAPTER == 0 and res.SCENE == 0:
					self.ingame = 5
		else:
			if pressed[2][0]:
				res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if self.mnu == 0: self.opt[0] -= 1; self.opt[1] = 0
				elif self.mnu < 3: self.mnu = 1
				else:
					self.mnu -= 1
					if self.mnu < 3: self.mnu = 5
	
			if pressed[3][0]:
				res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if self.mnu == 0: self.opt[0] += 1; self.opt[1] = 0
				elif self.mnu < 3: self.mnu = 2
				else:
					self.mnu += 1
					if self.mnu > 5: self.mnu = 3
	
			if pressed[0][0]:
				res.MIXER[0].play(res.SOUND['MENU_VER'])
				if self.mnu < 3: self.opt[1] -= 1
				else:
					self.exvar -= 1
					if self.exvar < 0: self.exvar = 5
					res.PARTY[self.opt[1]][self.mnu - 3] = self.exvar
	
			if pressed[1][0]:
				res.MIXER[0].play(res.SOUND['MENU_VER'])
				if self.mnu < 3: self.opt[1] += 1
				else:
					self.exvar += 1
					if self.exvar > 5: self.exvar = 0
					res.PARTY[self.opt[1]][self.mnu - 3] = self.exvar
			#PARTY SELECT
			if self.opt[0] == 0:
				if self.opt[1] < 0: self.opt[1] = len(res.PARTY)
				if self.opt[1] > len(res.PARTY): self.opt[1] = 0
	
				if pressed[4][0]:
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					if self.opt[1] < len(res.PARTY):
						if self.mnu == 0:
							self.mnu = 1
						elif self.mnu == 1:
							res.FORMATION = self.opt[1]
							for i in res.PARTY[res.FORMATION]:
								res.CHARACTERS[i]['VITALITY'] = dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
							res.MIXER[1].play(res.SOUND['PARTY_CHANGE'])
							self.mnu = 0
							self.opt = [0,0]
						elif self.mnu > 2:
							res.party_make(self.opt[1])
							self.mnu = 0
						elif len(res.PARTY) > 1:
							del res.PARTY[self.opt[1]]
							self.mnu = 0 
					else:
						res.PARTY.append([0,0,0])
						self.exvar = 0
						self.mnu = 3
			#PHONE SELECT
			if self.opt[0] == 1:
				if self.opt[1] < 0: self.opt[1] = len(res.CONTACTS) - 1
				if self.opt[1] > len(res.CONTACTS) - 1: self.opt[1] = 0
	
				if pressed[4][0]:
					if self.mnu == 0:
						pygame.time.wait(round(np.random.randint(10,200)))
						if self.credit > 0:
							credit = self.find(res.PARTY[res.FORMATION][0],'phone')
							if credit != None:
								if credit[2] == 'sim_card': credit[3] = str(int(credit[3]) - 1); self.credit = int(credit[3])
								elif credit[4] == 'sim_card': credit[5] = str(int(credit[5]) - 1); self.credit = int(credit[5])
							res.CALLHIST.insert(0,[res.CONTACTS[self.opt[1]][1],False])
							self.nb = res.CONTACTS[self.opt[1]]
							if self.nb[1] in ['23778988','69696969','53478809']:
								self.ingame = 1
							else: self.ingame = 2
						else: self.ingame = 3
	
			if self.opt[0] < 0: self.opt[0] = 2
			if self.opt[0] > 2: self.opt[0] = 0
		
	def outside_events(self,event):
		pass
	
	def call(self):
		self.surface.fill((10,10,10,0))
		sz = self.surface.get_width() #button width
		num = 0
		for i in dtb.NUMBERS:
			if i[1] == self.nb: break
			num += 1
		self.surface.blit(pygame.image.load(res.BACKG_PATH + 'call_' + self.nb + '.png'), (0, 90))
		pygame.draw.rect(self.surface, (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(0,0,sz,90))
		self.surface.blit(res.FONTS['CALIBRI'].render(dtb.NUMBERS[num][0], True, (255, 255, 255)), (100, 20))
		self.surface.blit(res.FONTS['CALIBRI'].render(self.nb, True, (255, 255, 255)), (100, 40))
		self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[32] + str(self.credit), True, (255, 255, 255)), (100, 80))
		self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[33], True, (255, 255, 255)), (100, 120))

		if self.opt == 0: self.surface.blit(pygame.transform.scale(pygame.image.load(res.SPRITES_PATH + 'cl_ys.png'), (40, 40)), (25, 185))
		else: self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'cl_ys.png'), (30, 190))
		if self.opt == 1: self.surface.blit(pygame.transform.scale(pygame.image.load(res.SPRITES_PATH + 'cl_no.png'), (40, 40)), (sz - 55, 185))
		else: self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'cl_no.png'), (sz - 50, 190))

		return self.surface
		
	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.blit(self.vkb.draw(),(20,20))
		return self.surface
	
	def dd(self):
		if self.nb != None: self.call()
		else:
			sz = self.surface.get_width() #button width
			self.surface.fill((0,0,0))
			self.surface.blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))
			
			if self.opt[0] == 0: em = res.PARTY
			if self.opt[0] == 1: em = res.CONTACTS
			if self.opt[0] == 2: em = res.CALLHIST
			if self.opt[1] > 2:
				if self.scroll < (self.opt[1] - 2) * 51:
					self.scroll += 5.1
			elif self.opt[1] > 0 and self.opt[1] < len(em) - 1:
				if self.scroll > (self.opt[1] - 1) * 51:
					self.scroll -= 5.1
			elif self.opt[1] == 0:
				if self.scroll > 0:
					self.scroll -= 5.1
			
			y = 0
			for i in em:
				if self.opt[1] != y/51: col = (255, 255, 255)
				else: col = (15, 255, 0)
				pygame.draw.rect(self.surface, col, pygame.Rect(0,66 + y - self.scroll,sz,50))
	
				if self.opt[0] > 0: self.surface.blit(res.FONTS['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, (76 + y - self.scroll) * 2))
				else:
					if self.opt[1] == y/51:
						if self.mnu == 1: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(sz - 52,74 + y - self.scroll,24,24))
						self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'tc_9.png'), (sz - 50, 76 + y - self.scroll))
						if self.mnu == 2: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(sz - 30,74 + y - self.scroll,24,24))
						self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'tc_8.png'), (sz - 28, 76 + y - self.scroll))
						if self.mnu == 3: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(8,74 + y - self.scroll,24,24))
						if self.mnu == 4: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(30,74 + y - self.scroll,24,24))
						if self.mnu == 5: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(52,74 + y - self.scroll,24,24))
					x = 0
					for p in i:
						self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (10 + x, 76 + y - self.scroll))
						x += 22
				if self.opt[0] == 0: self.surface.blit(res.FONTS['CALIBRI'].render('grupo ' + str(int((y + 51)/51)), True, (0, 0, 0)), (20, (96 + y - self.scroll) * 2))
				if self.opt[0] == 1: self.surface.blit(res.FONTS['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, (92 + y - self.scroll) * 2))
				if self.opt[0] == 2: self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(i[1]).lower() + '.png'), (160, 43 + y - self.scroll))
				y += 51
			if self.opt[0] == 0:
				if self.opt[1] != y/51: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
				else: pygame.draw.rect(self.surface, (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,sz,50))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[31], True, (0, 0, 0)), (170, (83 + y - self.scroll) * 2))
			if y == 0 and self.opt[0] == 1:
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[16], True, (255, 255, 255)), (100, 280))
			dvd3 = np.floor(sz/3)
			if self.opt[0] == 0:
				pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0,45,dvd3,20))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[23], True, (0, 0, 0)), (16, 94))
			else:
				pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0,40,dvd3,25))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[23], True, (255, 255, 255)), (16, 94))
			if self.opt[0] == 1:
				pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[24], True, (0, 0, 0)), ((dvd3 * 2) + 20, 94))
			else:
				pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(dvd3,40,dvd3,25))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[24], True, (255, 255, 255)), ((dvd3 * 2) + 20, 94))
			if self.opt[0] == 2:
				pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[25], True, (0, 0, 0)), ((dvd3 * 4) + 20, 94))
			else:
				pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(dvd3 * 2,40,dvd3,25))
				self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[25], True, (255, 255, 255)), ((dvd3 * 4) + 20, 94))
			pygame.draw.rect(self.surface, (15, 255, 0), pygame.Rect(0,0,sz * 2,80))
			self.surface.blit(res.FONTS['TITLE'].render(dtb.MENU[1], True, (0, 0, 0)), (10, 10))
	
			return self.surface
		
class Email:
	def __init__(self):
		self.surface = pygame.Surface((180 * res.GSCALE,200 * res.GSCALE), pygame.SRCALPHA)
		self.scroll = 0
		self.optrects = []
		dvd3 = np.floor((180 * res.GSCALE)/3)
		for i in range(3): self.optrects.append(pygame.Rect(dvd3 * i,0,dvd3,40))
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed,mouse):
		if res.SIGNAL > 0:
			if self.mnu == 0:
				if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
				if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
				if pressed[2][0]: self.opt[0] -= 1; self.opt[1] = 0; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: self.opt[0] += 1; self.opt[1] = 0; res.MIXER[0].play(res.SOUND['MENU_HOR'])

			if pressed[4][0] and res.SIGNAL > 0:
				if self.mnu == 0: self.mnu = 1; res.MIXER[0].play(res.SOUND['MENU_GO'])
				elif self.mnu > 0:
					res.MIXER[0].play(res.SOUND['MENU_BACK'])
					if self.opt[0] == 0: self.phn.e_unread[self.opt[1]][3] = 1
					if self.opt[0] == 2: res.INBOX[self.opt[1]][3] = 1
					self.mnu = 0
			read = 0
			unrd = 0
			for i in res.INBOX:
				if i[3] == 0: unrd += 1
				if i[3] == 1: read += 1

			if self.opt[0] < 0: self.opt[0] = 2
			if self.opt[0] > 2: self.opt[0] = 0
			if self.opt[0] == 0:
				if self.opt[1] < 0: self.opt[1] = unrd
				if self.opt[1] > unrd: self.opt[1] = 0
			if self.opt[0] == 1:
				if self.opt[1] < 0: self.opt[1] = read
				if self.opt[1] > read: self.opt[1] = 0
			if self.opt[0] == 2:
				if self.opt[1] < 0: self.opt[1] = len(res.INBOX) - 1
				if self.opt[1] > len(res.INBOX) - 1: self.opt[1] = 0
		
	def outside_events(self,pressed):
		if self.mnu > 0:
			if pressed[0][0]: self.mnu -= 2
			if pressed[1][0]: self.mnu += 2

			if self.mnu < 1: self.mnu = 1
			if self.mnu > 1000: self.mnu = 1000
	
	def draw(self):
		sz = self.surface.get_width() #button width
		self.surface.fill((10,10,10,0))
		if res.SIGNAL > 0:
			if self.mnu == 0:
				lst = ['unread','read','all']
				for i in range(3):
					if self.opt[0] == i: col = (10,10,10); pygame.draw.rect(self.surface, (200, 200, 200), self.optrects[i])
					else: col = (200,200,200)
					self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[lst[i]], True, col), (self.optrects[i].x + 10, self.optrects[i].y + 10))
				lst = [[x for x in res.INBOX if x[1] < 100],[x for x in res.INBOX if x[1] == 100],res.INBOX]
				for i in range(len(lst[self.opt[0]])):
					if self.opt[1] != i: col = (200, 200, 200)
					else: col = (255, 123, 0)
					pygame.draw.rect(self.surface, col, pygame.Rect(0,40 + (i * 81) - self.scroll,sz * res.GSCALE,80))
					self.surface.blit(res.FONTS['CALIBRI'].render(dtb.TASKINDEX[lst[self.opt[0]][i][0]][0][0], True, (10, 10, 10)), (20, 50 + (i * 81) - self.scroll))
				if len(lst[self.opt[0]]) == 0: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU['empty'], True, (200, 200, 200)), (80, 280))
		else: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU['no_signal'], True, (200, 200, 200)), (100, 200))

		return self.surface

class Newspaper:
	def __init__(self):
		self.surface = pygame.Surface((600,600), pygame.SRCALPHA)
		self.page = 0
		self.rdnws = []
		for i in range(5):
			nw = ''
			prb = np.random.randint(0,len(dtb.RANDNEWS[0]) - 1)
			nw += dtb.RANDNEWS[0][prb][0]
			fnd = dtb.RANDNEWS[0][prb][1]
			while True:
				add = np.random.randint(0,len(fnd) - 1)
				if isinstance(fnd[add],str):
					nw += ' ' + fnd[add]
					break
				else:
					nw += ' ' + fnd[add][0]
					fnd = fnd[add][1]
			if prb in [0,1]:
				pprb = np.random.randint(0,100)
				if pprb > 50:
					pl = np.random.randint(0,len(dtb.RANDNEWS[1]) - 1)
					nw += ' ' + dtb.RANDNEWS[1][pl]
			nw += '.'
			self.rdnws.append(nw)
		
	def inside_events(self,pressed,mouse):
		if pressed[2][0]: self.page -= 1; res.MIXER[0].play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page += 1; res.MIXER[0].play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		self.surface.fill((200,200,200,0))
		
		pygame.draw.rect(self.surface,(50,50,200),pygame.Rect(5,5,sz - 10,40))
		fsz = res.FONTS['TITLE'].size('O LOBO')[0]
		self.surface.blit(res.FONTS['TITLE'].render('O LOBO', True, (200,200,200)), (int(((sz * 2)/2) - (fsz/2)), 15))
		self.surface.blit(res.FONTS['SMALL'].render(str(res.DATE[0]) + '/' + str(res.DATE[1]) + ' - 1ª edição', True, (10,10,10)), (30, 70))
		for y in range(5):
			if y == 0: self.surface.blit(res.FONTS['MEDIUM'].render(self.rdnws[y], True, (10,10,10)), (25, 100))
			else: self.surface.blit(res.FONTS['SMALL'].render(self.rdnws[y], True, (10,10,10)), (25, 150 + (y * 20)))

		return self.surface
		
class ID:
	def __init__(self,n):
		self.surface = pygame.Surface((500,300), pygame.SRCALPHA)
		self.page = 0
		self.who = n
		
	def inside_events(self,pressed):
		if pygame.event == pygame.MOUSEBUTTONDOWN: self.page = int(not bool(self.page))
		if pressed[2][0]: self.page = 0; res.MIXER[0].play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page = 1; res.MIXER[0].play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		self.surface.fill((0,0,0))
		self.surface.fill((100,200,100))
		pygame.draw.rect(self.surface,(10,40,10),pygame.Rect(0,0,250,150),10)
		
		if self.page == 0:
			img = pygame.image.load(res.SPRITES_PATH + 'pht_' + str(self.who) + '.png')
			pygame.draw.rect(self.surface,(250,250,250),pygame.Rect(30,30,img.get_rect().width,img.get_rect().height))
			self.surface.blit(img, (30, 30))
		if self.page == 1:
			lsttxt = [('rg','XX.XXX.XXX-X'),('name',res.CHARACTERS[self.who]['NAME'] + ' ' + res.CHARACTERS[self.who]['LASTNAME']),
			('hometown',res.CHARACTERS[self.who]['HOMETOWN']),('birth',str(res.CHARACTERS[self.who]['BIRTH'][0]) + '/' + str(res.CHARACTERS[self.who]['BIRTH'][1]) + '/' + str(res.CHARACTERS[self.who]['BIRTH'][2])),
			('cpf','XXX.XXX.XXX-XX')]
			lstpos = [((30, 30),(120, 30)),((30, 60),(30, 75)),((30, 200),(30, 215)),((300, 200),(300, 215)),((30, 240),(30, 255))]
			for i in range(len(lsttxt)):
				self.surface.blit(res.FONTS['SMALL'].render(lsttxt[i][0], True, (10,40,10)), lstpos[i][0])
				self.surface.blit(res.FONTS['MEDIUM'].render(lsttxt[i][1], True, (10,10,10)), lstpos[i][1])
			
		return self.surface

class Radio:
	def __init__(self):
		self.surface = pygame.Surface((160 * res.GSCALE,110 * res.GSCALE), pygame.SRCALPHA)
		self.rdsrf = pygame.Surface((90 * res.GSCALE,25 * res.GSCALE))
		self.ratio = [(160 * res.GSCALE,110 * res.GSCALE),(90 * res.GSCALE,25 * res.GSCALE)]
		self.onoff = False
		self.load = ''
		self.msc = 0
		self.fm = 0
		self.vm = 0
		self.song = res.MUSIC_PATH + res.RADIO[np.floor(self.fm/20)][self.msc]
		self.mscinfo = {'TITLE': 'no song','ARTIST': 'unknown','ALBUM': 'unknown'}
		self.button = pygame.Rect(0,120,160 * res.GSCALE,100)
		self.scroll = 0
		self.nwsw = 0
		self.nwss = 0
		
	def inside_events(self,pressed,mouse):
		if mouse.x <= 0: self.fm = 0
		elif mouse.x > 160 * res.GSCALE: self.fm = (res.RANGE_RADIO - 1) * 20
		else: self.fm = int(((res.RANGE_RADIO - 1) * 20)/((160 * res.GSCALE)/mouse.x))
		if res.SIGNAL > 0:
			do = False
			if pressed[4][0]: do = True
			elif pygame.Rect.colliderect(self.button,mouse): do = True
			if do:
				self.onoff = not self.onoff
				if self.onoff == False:
					res.MIXER[0].play(res.SOUND['MENU_BACK'])
					res.MIXER[1].stop()
					pygame.mixer.music.stop()
				else:
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					res.MIXER[1].play(res.SOUND['NOISE'],-1)
					self.song = res.MUSIC_PATH + res.RADIO[np.floor(self.fm/20)][self.msc] + '.mp3'
					audio = MP3(self.song)
					try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
					except: self.mscinfo = {'TITLE': res.RADIO[np.floor(self.fm/20)][self.msc] + '.mp3','ARTIST': 'unknown','ALBUM': 'unknown'}
					pygame.mixer.music.load(self.song)
					pygame.mixer.music.play()
			if pressed[7][0]:
				res.MIXER[1].stop()
						
	def outside_events(self,pressed):
		if pressed[2][0]: self.fm -= 1; self.vm -= 0.05
		if pressed[3][0]: self.fm += 1; self.vm += 0.05

		if self.fm < 0: self.fm = (res.RANGE_RADIO - 1) * 20
		if self.fm > (res.RANGE_RADIO - 1) * 20: self.fm = 0
		if self.vm < 0.0: self.vm = 1.0
		if self.vm > 1.0: self.vm = 0.0

		pygame.mixer.music.set_volume(self.vm)
		res.MIXER[1].set_volume(1 - self.vm)
		ind = np.floor(self.fm/(res.RANGE_RADIO * 2))
		if ind > 6: ind = 6
		if self.vm == 0.0 and self.onoff == True:
			if res.RADIO[ind] != []:
				self.song = res.MUSIC_PATH + res.RADIO[ind][self.msc] + '.mp3'
				audio = MP3(self.song)
				try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
				except: self.mscinfo = {'TITLE': res.RADIO[ind][self.msc] + '.mp3','ARTIST': 'unknown','ALBUM': 'unknown'}
				pygame.mixer.music.load(self.song)
				pygame.mixer.music.play()
				
	def miniature(self):
		ind = np.floor(self.fm/(res.RANGE_RADIO * 2))
		self.rdsrf = pygame.Surface((360 + self.nwsw,50))
		self.rdsrf.fill((255, 0, 135))
		if self.msc < 0:
			ttsz = np.floor(res.FONTS['CALIBRI'].size('?????')[0]/2)
			self.rdsrf.blit(res.FONTS['CALIBRI'].render('?????', True, (10, 10, 10)), (-self.scroll * 2, 5 * 2))
		else:
			if self.nwsw > 0: txt = dtb.RADIONEWS[self.nwind][2]
			else:
				txt = self.mscinfo['TITLE']
				if self.mscinfo['ARTIST'] != 'unknown': txt += ' – ' + self.mscinfo['ARTIST']
			out = tools.text.dislexic(txt)
			ttsz = np.floor(res.FONTS['CALIBRI'].size(out)[0]/2)
			self.rdsrf.blit(res.FONTS['CALIBRI'].render(out, True, (10, 10, 10)), (-self.scroll * 2, 5 * 2))
		self.scroll += 1
		if self.scroll > ttsz: self.scroll = -180
		if self.nwsw > 0 and self.nwsw < ttsz: self.nwsw += 3
				
		if pygame.mixer.music.get_busy() == False and self.msc > -2:
			self.msc += 1
			if self.msc >= len(res.RADIO[round(self.fm/20)]): self.msc = 0
			if res.RADIO[round(self.fm/20)] != []:
				self.song = res.MUSIC_PATH + res.RADIO[ind][self.msc] + '.mp3'
				audio = MP3(self.song)
				try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
				except: self.mscinfo = {'TITLE': res.RADIO[ind][self.msc] + '.mp3','ARTIST': 'unknown','ALBUM': 'unknown'}
				pygame.mixer.music.load(self.song)
				pygame.mixer.music.play()
		
		return self.rdsrf

	def draw(self):
		sz = self.surface.get_width()
		self.surface.fill((0,0,0,0))
		f = 0
		sp = np.floor(sz/res.RANGE_RADIO)
		for i in range((res.RANGE_RADIO * 2) - 1):
			pygame.draw.line(self.surface, (200, 200, 200), (0 + f,80),(0 + f,119),1)
			pygame.draw.line(self.surface, (200, 200, 200), (round(sp/2) + f,100),(round(sp/2) + f,119),1)
			f += sp
		pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(int((160 * res.GSCALE)/(((res.RANGE_RADIO - 1) * 20)/(self.fm + 1))) - 4,80,4,40))
		pygame.draw.rect(self.surface, (255, 0, 135), self.button)
		ind = np.floor(self.fm/(res.RANGE_RADIO * 2))
		if ind > 6: ind = 6
		if res.RADIO[ind] != []:
			txt = self.mscinfo['TITLE']
			if self.mscinfo['ARTIST'] != 'unknown': txt += ' – ' + self.mscinfo['ARTIST']
			self.surface.blit(res.FONTS['CALIBRI'].render(txt, True, (10, 10, 10)), (self.button.x + 10, self.button.y + 20))
		else: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[20], True, (255, 255, 255)), (self.button.x + 10, self.button.y + 20))
		self.surface.blit(res.FONTS['CALIBRI'].render(str(self.fm/10) + 'MHz', True, (10, 10, 10)), (self.button.x + 10, self.button.y + 60))
		
		return self.surface

class Camera:
	def __init__(self):
		self.img = pygame.image.load(res.BACKG_PATH + 'camera.png')
		self.surface = pygame.Surface((360,464), pygame.SRCALPHA)
		self.scrpos = (57,89)
		self.rqst = True
		self.battle = False
		self.scroll = 0
		self.optrects = []
		self.opt = 0
		res.recent_data(0)
		self.optrects = []
		for i in range(len(res.FILES[0]) + 1):
			self.optrects.append(pygame.Rect(0,41 + (i * 51),self.surface.get_width(),50))
	
	def inside_events(self,pressed,mouse):
		if res.SIGNAL > 0:
			if pressed[0][0]: self.opt -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])

			if self.opt < 0: self.opt = 2
			if self.opt > 2: self.opt = 0
			
			do = False
			if pressed[4][0]: do = True
			for i in range(len(self.optrects)):
				if pygame.Rect.colliderect(self.optrects[i],mouse):
					self.opt = i
					#do = True
			if do:
				if self.battle == False and res.SIGNAL > 0:
					res.MIXER[0].play(res.SOUND['FILE_SAVE'])
					res.ID = self.opt
					res.CHAPTER = 13
					self.ingame = 6
					#SAVE FILE
					if self.opt < len(res.FILES[0]):
						res.recent_data(1,self.opt)
					#NEW FILE
					else:
						res.recent_data(2,self.opt)
					res.save_data(0)
					res.recent_data(0)
				elif self.battle == True:
					rsg = False
					for j in range(len(res.BESTIARY)):
						if len(self.foe) > 0 and res.BESTIARY[j]['N'] == self.foe[0]['FILE'] and res.BESTIARY[j]['SEEN'] == 1:
							fid = str(j)
							if int(fid) < 10: fid = '00' + fid
							elif int(fid) < 40: fid = '0' + fid
							res.BESTIARY[j]['ID'] = fid
							res.BESTIARY[j]['DATE'] = str(res.DATE[0]) + '/' + str(res.DATE[1])
							res.BESTIARY[j]['SEEN'] = 2
							rsg = True
					if rsg == True:
						res.MIXER[0].play(res.SOUND['CAMERA'])
						self.ingame = 7
	
	def outside_events(self,pressed):
		pass
		
	def photo(self,bg,foes,xpos):
		self.rqst = False
		self.surface.fill((0,0,0))
		self.surface.blit(bg, (-xpos, -88))
		for i in foes:
			self.surface.blit(i['SPRITE'], (-xpos + i['MASK'].x, -88 + i['MASK'].y))

		return self.surface
		
	def draw(self):
		self.rqst = False
		sz = self.surface.get_width() #button width
		self.surface.fill((0,0,0))
		self.surface.blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))

		if res.SIGNAL > 0:
			y = 0
			for i in self.optrects:
				if self.opt != y: col = (255, 255, 255)
				else: col = (255, 255, 10)
				rct = pygame.Surface((i.width,i.height))
				rct.fill(col)
				rct.set_alpha(100)
				self.surface.blit(rct,(i.x,i.y))
				if y < len(res.FILES[0]):
					self.surface.blit(res.FONTS['MONOTYPE'].render(dtb.CHAPTERS[res.FILES[1][y]][0], True, (0, 0, 0)), (20, (51 + (y * 51)) * 2))
					ss = np.floor(res.FILES[2][y]/1000)
					mm = 0
					hh = 0
					while ss > 60: ss -= 60; mm += 1
					while mm > 60: mm -= 60; hh += 1
					if ss < 10: ss = '0' + str(ss)
					else: ss = str(ss)
					if mm < 10: mm = '0' + str(mm)
					else: mm = str(mm)
					if hh < 10: hh = '0' + str(hh)
					else: hh = str(hh)
					self.surface.blit(res.FONTS['MONOTYPE'].render(hh + ' : ' + mm + ' : ' + ss, True, (0, 0, 0)), (20, (65 + (y * 51)) * 2))
					x = 0
					for p in res.FILES[4][y][::-1]:
						self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (sz - 30 - x, 65 + (y * 51)))
						x += 22
				else: self.surface.blit(res.FONTS['MONOTYPE'].render(dtb.MENU[61], True, (0, 0, 0)), (20, (61 + (y * 51)) * 2))
				y += 1
		else: self.surface.blit(res.FONTS['MONOTYPE'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0,0,sz * 2,80))
		self.surface.blit(res.FONTS['TITLE'].render(dtb.MENU[5], True, (0, 0, 0)), (10, 10))
		
		return self.surface

class Bestiary:
	def __init__(self):
		self.surface = pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.scroll = 0
		self.optrects = [[]]
		self.opt = [0,0]
		self.mnu = 0
		for i in range(len(res.BESTIARY)):
			if res.BESTIARY[i]['SEEN'] > 1: self.optrects[0].append(pygame.Rect(0,41 + (i * 51),self.surface.get_width(),50))
		
	def inside_events(self,pressed,mouse):
		if res.SIGNAL > 0:
			if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])

			if pressed[4][0]:
				if self.mnu == 0: self.mnu = 1; res.MIXER[0].play(res.SOUND['MENU_GO'])
				elif self.mnu > 0: self.mnu = 0; res.MIXER[0].play(res.SOUND['MENU_BACK'])

			lst = [x for x in res.BESTIARY if x['SEEN'] > 1]
			if self.mnu == 0:
				for i in range(len(self.optrects[0])):
					if pygame.Rect.colliderect(self.optrects[0][i],mouse): self.opt[1] = i; self.mnu = 1; res.MIXER[0].play(res.SOUND['MENU_GO'])
				if self.opt[1] < 0: self.opt[1] = len(lst)
				if self.opt[1] > len(lst): self.opt[1] = 0

			if self.mnu > 0:
				if pygame.event == pygame.MOUSEBUTTONDOWN: self.mnu = 0; res.MIXER[0].play(res.SOUND['MENU_BACK'])
				if pressed[2][0]: self.mnu = 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: self.mnu = 2; res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if self.opt[1] < 0: self.opt[1] = 3
				if self.opt[1] > 3: self.opt[1] = 0
	
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.surface.get_width()
		self.scroll = 0
		if self.opt[0] > 2: self.scroll += (self.opt[0] - 2) * 51

		self.surface.fill((220,220,200,0))
		pygame.draw.line(self.surface,(100,50,50),(20,10),(20,630),1)
		for i in range(20): pygame.draw.line(self.surface,(10,10,20),(30,45 + (i * 30)),((sz * res.GSCALE) - 30,45 + (i * 30)),1)
		if res.SIGNAL > 0:
			lst = [x for x in res.BESTIARY if x['SEEN'] > 1]
			frk = lst[self.opt[1]]
			fc = (30, 30, 50)
			if len(lst) > 0:
				#FREAKS LIST
				if self.mnu == 0:
					for i in range(len(self.optrects[0])):
						if self.opt[1] != i: cl = (255, 255, 255)
						else: cl = (134, 0, 211)
						pygame.draw.rect(self.surface, cl, pygame.Rect(self.optrects[0][i].x,self.optrects[0][i].y - self.scroll,self.optrects[0][i].width,self.optrects[0][i].height))
						self.surface.blit(res.FONTS['CALIBRI'].render(dtb.FREAKS[lst[i]['N']]['NAME'], True, (0, 0, 0)), ((self.optrects[0][i].x + 10) * res.GSCALE, (self.optrects[0][i].y + 10 - self.scroll) * res.GSCALE))
						self.surface.blit(res.FONTS['CALIBRI'].render(lst[i]['ID'], True, (0, 0, 0)), ((self.optrects[0][i].x + 10) * res.GSCALE, (self.optrects[0][i].y + 25 - self.scroll) * res.GSCALE))
				#FREAK INFORMATION
				if self.mnu == 1:
					self.surface.blit(res.FONTS['DESCRIPTION'].render('TAM.' + frk['N'], True, fc), ((sz * res.GSCALE) - 40, 30))
					#self.surface.blit(pygame.image.load(res.FREAKS_PATH + frk['N'] + '_stand.png'), (40, 70))
					self.surface.blit(res.FONTS['DESCRIPTION'].render(dtb.FREAKS[frk['N']]['NAME'], True, fc), (300, 70))
					self.surface.blit(res.FONTS['DESCRIPTION'].render('OA: ' + str(dtb.FREAKS[frk['N']]['OA']), True, fc), (300, 80))
					self.surface.blit(res.FONTS['DESCRIPTION'].render('RG: ' + str(frk['DATE'][0]) + '/' + str(frk['DATE'][1]) + '/' + str(frk['DATE'][2]), True, fc), (300, 90))
					self.surface.blit(res.FONTS['DESCRIPTION'].render('HG: ' + dtb.FREAKS[frk['N']]['HEIGHT'], True, fc), (300, 100))
					self.surface.blit(res.FONTS['DESCRIPTION'].render('HT: ' + dtb.FHABITATS[dtb.FREAKS[frk['N']]['HABITAT']], True, fc), (300, 120))
					#DESCRIPTION
					j = 0
					for l in tools.text.wrap([dtb.FREAKS[frk['N']]['INFO']],res.FONTS['DESCRIPTION'],(sz - 30) * res.GSCALE):
						self.surface.blit(res.FONTS['DESCRIPTION'].render(l, True, (0, 0, 0)), (20 * res.GSCALE, (100 + j) * res.GSCALE))
						j += 10
				#FREAK HABILITIES INFORMATION
				if self.mnu == 2:
					'''pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
					pygame.draw.rect(self.surface, (134, 0, 211), pygame.Rect(92,243,83,3))
					pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(10,50,160,77))'''

					y = 0
					for i in dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES']:
						if lopt != y/19: pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(11,51 + y,158,18))
						else: pygame.draw.rect(self.surface, (134, 0, 211), pygame.Rect(11,51 + y,158,18))
						self.surface.blit(res.FONTS['CALIBRI'].render(i[0], True, (0, 0, 0)), (40, (53 + y) * 2))
						y += 19

					j = 0
					for l in dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][1]:
						self.surface.blit(res.FONTS['DESCRIPTION'].render(l, True, (0, 0, 0)), (40, 360 + j))
						j += 30

					if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 1: dmg = dtb.MENU[37] + str(dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 2: dmg = dtb.MENU[38] + str(dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 3: dmg = dtb.MENU[39] + str(dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 4: dmg = dtb.MENU[40] + str(dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 5: dmg = dtb.MENU[41] + str(dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 6:
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 4: dmg = dtb.MENU[42]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 5: dmg = dtb.MENU[43]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 6: dmg = dtb.MENU[44]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 7: dmg = dtb.MENU[45]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 8: dmg = dtb.MENU[46]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 9: dmg = dtb.MENU[47]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 10: dmg = dtb.MENU[48]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 11: dmg = dtb.MENU[49]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] in (12,13,14): dmg = dtb.MENU[50]
						if dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 15: dmg = dtb.MENU[51]
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 7: dmg = dtb.MENU[52]
					elif dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 8: dmg = dtb.MENU[53]
					else: dmg = ''

					self.surface.blit(res.FONTS['CALIBRI'].render(dmg, True, (0, 0, 0)), (20, 210))
			else: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU['no_freaks'], True, (255, 255, 255)), (40, 140))
		else: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU['no_signal'], True, (255, 255, 255)), (50, 280))

		return self.surface
		
class Tasks:
	def __init__(self):
		self.surface = pygame.Surface((160 * res.GSCALE,160 * res.GSCALE), pygame.SRCALPHA)
		self.scroll = 0
		self.optrects = []
		dvd3 = np.floor((160 * res.GSCALE)/3)
		for i in range(3): self.optrects.append(pygame.Rect(dvd3 * i,0,dvd3,40))
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed,mouse):
		for i in range(len(self.optrects)):
			if pygame.Rect.colliderect(mouse,self.optrects[i]): self.opt[0] = i
		if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[2][0]: self.opt[0] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt[0] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])

		if self.opt[0] < 0: self.opt[0] = 2
		if self.opt[0] > 2: self.opt[0] = 0
		if self.opt[1] < 0: self.opt[1] = len(res.TASKS) - 1
		if self.opt[1] > len(res.TASKS) - 1: self.opt[1] = 0
					
	def outside_events(self,pressed):
		pass

	def draw(self):
		sz = self.surface.get_width()
		if self.opt[1] > 2:
			if self.scroll < (self.opt[1] - 2) * 31:
				self.scroll += 6.2
		elif self.opt[1] > 0 and self.opt[1] < len(em) - 1:
			if self.scroll > (self.opt[1] - 1) * 31:
				self.scroll -= 6.2
		elif self.opt[1] == 0 and self.scroll > 0:
			self.scroll -= 6.2
			
		self.surface.fill((10,10,10,0))
		lst = ['to_do','done','all']
		for i in range(3):
			if self.opt[0] == i: col = (10,10,10); pygame.draw.rect(self.surface, (200, 200, 200), self.optrects[i])
			else: col = (200,200,200)
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[lst[i]], True, col), (self.optrects[i].x + 10, self.optrects[i].y + 10))
		lst = [[x for x in res.TASKS if x[1] < 100],[x for x in res.TASKS if x[1] == 100],res.TASKS]
		for i in range(len(lst[self.opt[0]])):
			if self.opt[1] != i: col = (200, 200, 200)
			else: col = (255, 123, 0)
			pygame.draw.rect(self.surface, col, pygame.Rect(0,40 + (i * 81) - self.scroll,sz * res.GSCALE,80))
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.TASKINDEX[lst[self.opt[0]][i][0]][0][0], True, (10, 10, 10)), (20, 50 + (i * 81) - self.scroll))
		if len(lst[self.opt[0]]) == 0: self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU['no_tasks'], True, (200, 200, 200)), (80, 280))
		
		return self.surface
		
class Status:
	def __init__(self):
		self.surface = pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.mnsrf = pygame.Surface((90 * res.GSCALE,90 * res.GSCALE))
		self.ratio = [(180 * res.GSCALE,232 * res.GSCALE),(90 * res.GSCALE,90 * res.GSCALE)]
		self.scroll = 0
		self.optrects = []
		dvd3 = np.floor((180 * res.GSCALE)/3)
		for i in range(len(res.PARTY[res.FORMATION])): self.optrects.append(pygame.Rect(i * dvd3,0,dvd3,40))
		self.opt = 0
		self.bars = []
		for i in range(3): self.bars.append([100,100])
		self.imgs = {}
		for i in res.PARTY[res.FORMATION]:
			img = pygame.image.load(res.SPRITES_PATH + 'who_' + str(i) + '.png').convert_alpha()
			self.imgs[i] = pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE))
	
	def inside_events(self,pressed,mouse):
		for i in range(len(self.optrects)):
			if pressed[4][0] and pygame.Rect.colliderect(mouse,self.optrects[i]): self.opt = i
		if pressed[2][0]: self.opt -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])

		if self.opt < 0: self.opt = len(res.PARTY[res.FORMATION]) - 1
		if self.opt > len(res.PARTY[res.FORMATION]) - 1: self.opt = 0
					
	def outside_events(self,pressed): pass

	def miniature(self):
		self.mnsrf.fill((10,10,10))
		
		sz = self.mnsrf.get_width()
		ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.opt]]
		eq = res.INVENTORY[res.PARTY[res.FORMATION][self.opt]][4][res.EQUIP[self.opt]]
		nn = ch['NICK']
		if nn == None: nn = ch['NAME']
		self.mnsrf.blit(res.FONTS['TITLE'].render(nn.lower(), True, (255, 255, 255)), (20, 20))
		
		low = 0
		lst = [(ch['VITALITY'],dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']])] #VITALITY BAR
		if eq[0].startswith('gun'): lst.append((dtb.ITEMS[eq[0]][5]['CAPACITY'],eq[1])) #AMMO BAR
		elif eq[0].startswith('magic'): lst.append((ch['ENERGY'],100)) #ENERGY BAR
		else: lst.append((ch['SANITY'],100)) #SANITY BAR

		for i in range(len(lst)):
			pygame.draw.rect(self.mnsrf, (50, 50, 50), pygame.Rect(20,120 + (i * 60),sz - 40,40))
			if self.bars[self.opt][i] > 0: pygame.draw.rect(self.mnsrf, (200,200,10), pygame.Rect(20,120 + (i * 60),int((sz - 40)/self.bars[self.opt][i]),40))
			if lst[i][0] > int(lst[i][1]/5): col = (10, 200, 10)
			else: col = (250, 10, 10); low = 1
			if lst[i][0] > 0:
				if self.bars[self.opt][i] > int(100/(lst[i][1]/lst[i][0])):
					res.MIXER[0].play(res.SOUND['HP_LOSS'])
					self.bars[self.opt][i] -= 1
				pygame.draw.rect(self.mnsrf, col, pygame.Rect(20,120 + (i * 60),int((sz - 40)/(lst[i][1]/lst[i][0])),40))
		if len(ch['HEALTH']) > 0: self.mnsrf.blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(ch['HEALTH'][0]) + '.png'), (22, 122))
				
		#if self.equip[p] == 6: hpcol = (100, 100, 100)
		if low == 1 and res.MIXER[1].get_busy() == False: res.MIXER[1].play(res.SOUND['HP_LOW'])
		if low == 2 and res.MIXER[1].get_busy() == False: res.MIXER[1].play(res.SOUND['DYING'])
		
		return self.mnsrf

	def draw(self):
		sz = self.surface.get_width()
		self.scroll = 0
		if self.opt > 2: self.scroll += (self.opt - 2) * 60
		self.surface.fill((10,10,10,0))

		for i in range(len(res.PARTY[res.FORMATION])):
			tsz = res.FONTS['CALIBRI'].size(res.CHARACTERS[res.PARTY[res.FORMATION][i]]['NAME'])[0]
			if self.opt == i: pygame.draw.rect(self.surface, (200, 200, 200), self.optrects[i]); cl = (10, 10, 10)
			else: pygame.draw.rect(self.surface, (100, 200, 200), self.optrects[i]); cl = (10, 10, 10)
			#else: cl = (200, 200, 200)
			self.surface.blit(res.FONTS['CALIBRI'].render(res.CHARACTERS[res.PARTY[res.FORMATION][i]]['NAME'], True, cl), (self.optrects[i].x + int(self.optrects[i].width/2) - int(tsz/2), 5))
		#TEXT
		ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.opt]]
		self.surface.blit(self.imgs[self.opt], (10, 40))
		lst = [ch['NAME'] + ' ' + res.CHARACTERS[res.PARTY[res.FORMATION][self.opt]]['LASTNAME'] + ' nv.' + str(ch['LEVEL']),dtb.CNAMES[ch['CLASS']][0].capitalize() + ' ' + dtb.CNAMES[ch['SUBCLASS']],
			dtb.PRONOUNS[ch['PRONOUN']] + ' | ' + ch['BLOOD'] + ' | ' + dtb.ZODIAC[tools.data.sign(ch['BIRTH'])]]
		for i in range(len(lst)):
			txsz = res.FONTS['CALIBRI'].size(lst[i])
			self.surface.blit(res.FONTS['CALIBRI'].render(lst[i], True, (255, 255, 255)), ((sz * res.GSCALE) - 40 - txsz[0], 100 + (i * 30)))
		#BARS
		lst = [(ch['VITALITY'],dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]),(ch['SANITY'],100),(ch['HUNGER'],1000),(ch['THIRST'],1000),(ch['SLEEP'],1000)]
		for i in range(len(lst)):
			#self.surface.blit(res.FONTS['CALIBRI'].render('hp:', True, (255, 255, 255)), (20, 260))
			pygame.draw.rect(self.surface, (50, 50, 50), pygame.Rect(40,200 + (i * 30),200,20))
			if lst[i][0] > 0: pygame.draw.rect(self.surface, (200, 200, 200), pygame.Rect(40,200 + (i * 30),int(200/(lst[i][1]/lst[i][0])),20))
		#PENTACLE
		xx = 40
		yy = 400
		rr = 40 * res.GSCALE
		pnt = []
		lst = [x for x in dtb.PROFNAMES.keys()]
		for i in range(len(lst)):
			p = -((2 * 3.14)/len(lst)) * i
			vl = (rr/(5/dtb.CLASSES[ch['CLASS']][lst[i]][ch['LEVEL']]))
			pnt.append((int(np.cos(p) * vl) + xx + rr,int(np.sin(p) * vl) + yy + rr))
			pygame.draw.line(self.surface,(200,50,50),(xx + rr,yy + rr),(int(np.cos(p) * rr) + xx + rr,int(np.sin(p) * rr) + yy + rr),1)
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.PROFNAMES[lst[i]], True, (255, 255, 255)), (int(np.cos(p) * rr) + xx + rr + 10,int(np.sin(p) * rr) + yy + rr + 10))
			ord = [0,2,4,1,3,0]
		for i in range(len(ord) - 1): pygame.draw.line(self.surface,(200,200,200),pnt[ord[i]],pnt[ord[i + 1]],2)
		pygame.draw.ellipse(self.surface,(200,200,200),pygame.Rect(xx,yy,rr * 2,rr * 2),3)
		
		return self.surface

class Tactics:
	def __init__(self):
		self.surface = pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.ratio = [(180 * res.GSCALE,232 * res.GSCALE),(210,50)]
		self.scroll = 0
		self.optrects = []
		for i in range(20): self.optrects.append(pygame.Rect(0,i * 41 * res.GSCALE,180 * res.GSCALE,40 * res.GSCALE))
		self.btrects = []
		for i in range(4): self.btrects.append(pygame.Rect(10 + (i * 40),10,30,30))
		self.opt = [0,0,0]
		self.mnu = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[2][0]: self.opt[0] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt[0] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])

		if self.opt[0] < 0: self.opt[0] = len(res.PARTY[res.FORMATION])
		if self.opt[0] > len(res.PARTY[res.FORMATION]): self.opt[0] = 0
		if self.opt[1] < 0: self.opt[1] = len(res.TACTICAL[res.PARTY[res.FORMATION][self.opt[0]]])
		if self.opt[1] > len(res.TACTICAL[res.PARTY[res.FORMATION][self.opt[0]]]): self.opt[1] = 0
								
	def outside_events(self,pressed):
		pass
	
	def miniature(self):
		srf = pygame.Surface((210,50))
		srf.fill((0,0,0))

		lst = ['tactical','talk','guard','run']
		for i in range(len(self.btrects)):
			if self.opt[2] == i: col = res.COLOR
			else: col = (200,200,200)
			pygame.draw.rect(srf,col,self.btrects[i])
			srf.blit(pygame.image.load(res.SPRITES_PATH + 'e_' + lst[i] + '.png'), (self.btrects[i].x,self.btrects[i].y))
		srf.blit(pygame.image.load(res.SPRITES_PATH + 'e_invphn.png'), (srf.get_width() - 40, 10))

		return srf

	def draw(self):
		self.surface.fill((10,10,10,0))
		if self.opt[1] > 2: self.scroll += (self.opt[1] - 2) * 51

		for i in range(len(res.TACTICAL[res.PARTY[res.FORMATION][self.opt[0]]])):
			if self.opt[1] == i: col = (33, 75, 127)
			else: col = (200,200,200)
			pygame.draw.rect(self.surface, col, self.optrects[i])
			j = dtb.TRICKS[res.TACTICAL[res.PARTY[res.FORMATION][self.opt[0]]][i]]
			self.surface.blit(res.FONTS['CALIBRI'].render(j['NAME'], True, (10, 10, 10)), (self.optrects[i].x + 10, self.optrects[i].y + 10))
			self.surface.blit(res.FONTS['DESCRIPTION'].render(j['DESCRIPTION'], True, (10, 10, 10)), (self.optrects[i].x + 10, self.optrects[i].y + 40))
	
		return self.surface
		
class Achievements:
	def __init__(self):
		self.surface = pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.scroll = 0
		self.optrects = []
		for i in range(len(dtb.ACHIEVEMENTS)): self.optrects.append(pygame.Rect(0,102 * i,180 * res.GSCALE,100))
		self.opt = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[0][0]: self.opt -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if self.opt < 0: self.opt = len(dtb.ACHIEVEMENTS) - 1
		if self.opt > len(dtb.ACHIEVEMENTS) - 1: self.opt = 0
					
	def outside_events(self,pressed): pass

	def draw(self):
		self.surface.fill((10,10,10,0))
		for i in range(len(self.optrects)):
			if self.opt != i: col = (200, 200, 200)
			else: col = (255, 191, 0)
			pygame.draw.rect(self.surface, col, self.optrects[i])
			if dtb.ACHIEVEMENTS[i][2] == True: tcol = (0,0,0)
			else: tcol = (80,80,80)
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.ACHIEVEMENTS[i][0], True, tcol), (10, 20 + (102 * i)))
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.ACHIEVEMENTS[i][1], True, tcol), (10, 50 + (102 * i)))
		
		return self.surface

class Ranking:
	def __init__(self):
		self.surface = pygame.Surface((360,464), pygame.SRCALPHA)
		self.scroll = 0
		
	def inside_events(self,pressed):
		pass
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		self.surface.fill((10,10,10,0))
		if res.SIGNAL > 0: pass
		else: self.surface.blit(res.FONTS.render(dtb.MENU[15], True, (255, 255, 255)), (25, 140))

		return self.surface
		
class Settings:
	def __init__(self):
		self.surface = pygame.Surface((180,232)), pygame.Surface((180 * res.GSCALE,232 * res.GSCALE), pygame.SRCALPHA)
		self.scroll = 0
		self.optrects = []
		for i in range(15): self.optrects.append(pygame.Rect(0,i * 82,180 * res.GSCALE,80))
		self.opt = [0,0]
		self.mnu = 0
		self.trg = 0
		self.buttons = []
		btlst = [3,8,2,3,10,2,10]
		for i in range(len(btlst)):
			self.buttons.append([])
			for b in range(btlst[i]):
				self.buttons[i].append(pygame.Rect(0,b * 35,self.surface.get_width(),30))
		self.imgs = {}
		for i in range(res.RANGE_BORDER):
			img = pygame.image.load(res.SPRITES_PATH + 'border_' + str(i) + '.png').convert_alpha()
			self.imgs[i] = pygame.transform.scale(img,(img.get_width() * res.GSCALE,img.get_height() * res.GSCALE))
		
	def inside_events(self,pressed,mouse):
		if pressed[0][0]: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if self.opt[1] < 0: self.opt[1] = len(self.buttons[self.mnu])
		if self.opt[1] > len(self.buttons[self.mnu]): self.opt[1] = 0
		#MAIN SETTINGS
		if self.mnu == 0:
			if pressed[4][0]:
				if self.opt[1] == 3:
					res.save_data(1)
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.opt[0] = 1
					self.opt[1] = 4
					self.phone = 1
					if res.CHAPTER == 0 and res.SCENE == 0:
						res.MIXER[0].play(res.SOUND['CALLING'],-1)
						self.ch_rng.play(res.SOUND['RINGTONE_' + str(self.phn.pbg)],-1)
						self.phone = 17
						self.nb = '977904623'
				else:
					self.mnu = self.opt[1] + 1
					self.opt[0] = 0
					self.opt[1] = 0
		#GAMEPLAY SETTINGS
		elif self.mnu == 1:
			if self.opt[1] == 0:
				if pressed[2][0]:
					res.LANG = 'EN'; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]:
					res.LANG = 'PT'; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 1:
				if pressed[2][0]: res.SPEED += 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SPEED -= 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.SPEED < 1: res.SPEED = 5
				if res.SPEED > 5: res.SPEED = 1
			if self.opt[1] == 5:
				if pressed[2][0]: res.BORDER -= 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.BORDER += 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.BORDER < 0: res.BORDER = res.RANGE_BORDER
				if res.BORDER > res.RANGE_BORDER: res.BORDER = 0
			if self.opt[1] == 6:
				if pressed[2][0]: res.CENSORSHIP = False; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CENSORSHIP = True; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 7:
				if pressed[2][0]: res.HINT = False; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HINT = True; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 8:
				if pressed[2][0]: res.HELP = False; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HELP = True; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
		#CONTROLS MENU
		elif self.mnu == 3:
			if pressed[4][0]:
				self.mnu = self.opt[1] + 4
				self.opt[0] = 0
				self.opt[1] = 0
		#MOUSE SETTINGS
		elif self.mnu == 4:
			if self.opt[1] == 1:
				if pressed[2][0]: res.CURSOR -= 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CURSOR += 1; self.sfx.set_volume(res.SFX); res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.CURSOR < 0: res.CURSOR = res.RANGE_CURSOR
				if res.CURSOR > res.RANGE_CURSOR: res.CURSOR = 0
			if pressed[4][0]:
				self.mnu = self.opt[1] + 4
				self.opt[0] = 0
				self.opt[1] = 0
		#1P SETTINGS
		elif self.mnu == 5:
			#UP KEY
			for i in range(len(res.CONTROLS)):
				if self.opt[1] == i:
					if pressed[4][0] and self.trg == 0: self.trg = 1
					elif self.trg:
						if event.key not in res.CONTROLS:
							res.CONTROLS = event.key; self.trg = 0
		#GO BACK
		if pressed[5][0]:
			if self.mnu > 0:
				res.MIXER[0].play(res.SOUND['MENU_BACK'])
				self.mnu = 0
							
	def outside_events(self,pressed):
		#COLORS SETTINGS
		if self.mnu == 1:
			if self.opt[1] == 2:
				if pressed[2][0]: res.COLOR[0] -= 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[0] += 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.COLOR[0] < 30: res.COLOR[0] = 242
				if res.COLOR[0] > 242: res.COLOR[0] = 30
			if self.lopt == 3:
				if pressed[2][0]: res.COLOR[1] -= 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[1] += 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.COLOR[1] < 30: res.COLOR[1] = 242
				if res.COLOR[1] > 242: res.COLOR[1] = 30
			if self.lopt == 4:
				if pressed[2][0]: res.COLOR[2] -= 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[2] += 5; res.MIXER[0].play(res.SOUND['MENU_HOR'])

				if res.COLOR[2] < 30: res.COLOR[2] = 242
				if res.COLOR[2] > 242: res.COLOR[2] = 30
		#AUDIO SETTINGS
		if self.mnu == 2:
			if self.opt[1] == 0:
				if pressed[2][0]: res.SFX -= 0.1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SFX += 0.1;	res.MIXER[0].play(res.SOUND['MENU_HOR'])
				self.sfx.set_volume(res.SFX)
				if res.SFX < 0.0: res.SFX = 0.0
				if res.SFX > 1.0: res.SFX = 1.0
			if self.opt[1] == 1:
				if pressed[2][0]: res.MSC -= 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.MSC += 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])

				if res.MSC < 0.0: res.MSC = 0.0
				if res.MSC > 1.0: res.MSC = 1.0

	def draw(self):
		self.surface.fill((10,10,10,0))
		sz = self.surface.get_width() #button width

		rng = [4,10,10,10]
		inpts = [
		['gameplay','sound','controls','exit'],
		['lang','border'],
		['sfx','music','tts','cc'],
		]
		for i in range(rng[self.mnu]):
			if self.opt[1] == i: col = (91, 91, 91)
			else: col = (200,200,200)
			rct = self.optrects[i].copy()
			rct.y += self.scroll
			pygame.draw.rect(self.surface, col, rct)
			
			txt = ''
			if inpts[self.mnu][i] == 'lang': txt = ': ' + res.LANG
			if self.mnu == 3:
				if self.opt[0] == i and not self.trg: txt = dtb.MENU['bt_choose']
				else: txt = ': ' + pygame.key.name(res.CONTROLS[0][i])
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.MENU[inpts[self.mnu][i]] + txt, True, (10,10,10)), (rct.x + 10, rct.y + 10))
			
			if inpts[self.mnu][i] in ['censorship','hints','tutorials']:
				swrct = pygame.Rect(rct.x + rct.height - 60,rct.y + 10,50,rct.height - 20)
				if inpts[self.mnu][i] == 'censorship': vl = res.CENSORSHIP
				if inpts[self.mnu][i] == 'hints': vl = res.HINTS
				if inpts[self.mnu][i] == 'tutorials': vl = res.TUTORIALS
				if vl: (140,255,124)
				else: (255,61,61)
				pygame.draw.rect(self.surface,col,swrct)
			if inpts[self.mnu][i] in ['sfx','audio','speed']:
				if inpts[self.mnu][i] == 'sfx': vl = (res.SFX,1.0)
				if inpts[self.mnu][i] == 'audio': vl = (res.MSC,1.0)
				if inpts[self.mnu][i] == 'speed': vl = (res.SPEED,5)
				barct = pygame.Rect(rct.x + rct.height - 60,rct.y + 10,50,rct.height - 20)
				pygame.draw.rect(self.surface,(100,100,100),barct)
				pygame.draw.rect(self.surface,(200,100,100),pygame.Rect(barct.x + int(barct.width/(vl[1]/vl[0])),barct.y,10,10))
			if inpts[self.mnu][i] == 'cursor':
				self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'), (rct.x + 10, rct.y + 10))
			if inpts[self.mnu][i] == 'border':
				for b in range(np.floor(sz/10) - 4):
						for c in range(3): self.surface.blit(self.imgs[res.BORDER], (rct.x + 10 + (b * 10), rct.y + 10 + (c * 10)))

		return self.surface
		
class About:
	def __init__(self):
		self.surface = pygame.Surface((160 * res.GSCALE,200 * res.GSCALE), pygame.SRCALPHA)
		self.optrects = []
		for i in range(2): self.optrects.append(pygame.Rect(0,150 + (i * 40),160 * res.GSCALE,40))
		self.opt = 0
		
	def inside_events(self,pressed,mouse):
		if pressed[0][0] and self.opt == 1: self.opt = 0; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0] and self.opt == 0: self.opt = 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		for i in range(len(self.optrects)):
			if pygame.Rect.colliderect(self.optrects[i],mouse): self.opt = i
		if pressed[4][0]:
			res.MIXER[0].play(res.SOUND['MENU_GO'])
			lst = ['twitter.com/kaixtr','github.com/kaixtr']
			for i in range(len(lst)):
				if self.opt == i: urllib.request.urlopen('https://' + lst[i])
							
	def outside_events(self,pressed):
		pass

	def draw(self):
		self.surface.fill((200,200,200))
		lst = [res.GNAME,res.AUTHOR + ' ' + res.YEAR,dtb.ABOUT[0],dtb.ABOUT[1]]
		for i in range(4): self.surface.blit(res.FONTS['CALIBRI'].render(lst[i], True, (10, 10, 10)), (20, 20 + (30 * i)))
		for i in range(len(self.optrects)):
			if self.opt == i: col = (150,150,150)
			else: col = (200,200,200)
			pygame.draw.rect(self.surface, col, self.optrects[i])
			self.surface.blit(res.FONTS['CALIBRI'].render(dtb.ABOUT[2 + i], True, (10, 10, 10)), (self.optrects[i].x + 20, self.optrects[i].y + 10))
		self.surface.blit(res.FONTS['CALIBRI'].render(dtb.ABOUT[4], True, (0, 0, 0)), (40, 300))
		
		return self.surface

if os.path.basename(sys.argv[0]) == os.path.basename(__file__):
	t = Test()
	while True: t.run()