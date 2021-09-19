# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3
import pygame
import pytmx
import plyer
import random
import datetime
import traceback
import numpy
import math
import sys
import os

from plugins import *
import resources as res
import minigames as mng
import GUI

from PIL import Image
import PIL.ImageOps

if res.FILES[3] != []:
	#if res.FILES[3][0] == 'PT': import database_PT as dtb
	#if res.FILES[3][0] == 'EN': import database_EN as dtb
	dtb = __import__('database_' + res.FILES[3][0])
else: dtb = __import__('database_' + res.MAINLANG)#import database_PT as dtb

class Title:
	def __init__(self):
		if os.uname().sysname == 'Windows':
			self.windoww = 1200
			self.windowh = 800
			res.MOUSE = 1
			res.GSCALE = 2
		else:
			sz = pygame.display.Info()
			self.windoww = sz.current_w
			self.windowh = sz.current_h
			res.MOUSE = 2
			res.GSCALE = 2
		self.displayzw = int(self.windoww/2)
		self.displayzh = int(self.windowh/2)
		pygame.init()
		pygame.display.set_caption(res.GNAME)
		pygame.display.set_icon(pygame.image.load('icon.ico'))
		pygame.mouse.set_visible(False)
		if res.TTS: plyer.tts.speak('')
		if res.VIBRATE: plyer.vibrator.vibrate(0.01)

		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((self.displayzw, self.displayzh),pygame.SRCALPHA),pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
		self.fnt = {'DEFAULT': pygame.font.Font(res.FONTS_PATH + res.FONT, 22),'RECAP': pygame.font.Font(res.FONTS_PATH + 'BohemianTypewriter.ttf', 26),
		'CALIBRI': pygame.font.SysFont('Calibri', 30),'MINI': pygame.font.SysFont('Calibri', 20), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 22)}
		self.guitools = GUI.Guitools()
		self.settings = GUI.Settings()
		self.about = GUI.About()
		pygame.mixer.music.set_volume(res.MSC)
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.ton = pygame.mixer.Channel(1)
		self.ton.set_volume(res.SFX)
		self.msc = pygame.mixer.Channel(2)
		self.msc.set_volume(res.MSC)
		self.glock = pygame.time.Clock()
		self.FPS = 1
		self.winbar = int(self.windowh/2) - 30
		self.wait = 0
		self.noise = 0
		self.tv = 1
		self.blink = 0
		self.img = None
		self.transform = {'TYPE': 0, 'VALUE': 0, 'SPEED': 0}
		self.rectrot = 0
		self.rndtxt = 0
		self.curfnt = 'DEFAULT'
		self.opt = 0
		self.lopt = -1
		self.mnu = -1
		self.scroll = 0
		self.txt = []
		self.skip = False
		self.classrun = True
		self.loadingif = None
		self.holiday = datetime.datetime.now()
		self.logoalpha = 0
		self.sscroll = self.windoww + 20
		self.stext = dtb.TSECRETS[random.randint(0,len(dtb.TSECRETS) - 1)]
		self.stime = random.randint(600,1000)
		self.gmtim = []
		
		self.load = 0
		self.msg = 0
		self.tim = 1.0
		self.gif = 0
		self.stars = []
		sfxpath = os.listdir(res.SFX_PATH[:-1])
		self.fload = res.RANGE_RADIO + len(sfxpath) + 3 + (13 * 2)
		self.bump = pygame.image.load(res.BACKG_PATH + 'bump_' + str(random.randint(0,res.RANGE_BUMP)) + '.png')
		for i in res.FILES[0]:
			if res.FILES[1][i] == 0:
				del res.FILES[0][i]
				del res.FILES[1][i]
				del res.FILES[2][i]
				del res.FILES[3][i]
		self.flrects = []
		self.oprects = []
		self.chrects = []
		self.pserects = []
		#halign = 0 #left
		#halign = int(self.displayzw/2) - int((460/res.GSCALE)/2) #center
		halign = self.displayzw - int(460/res.GSCALE) #right
		for i in range(len(res.FILES[2])):
			ss = math.floor(res.FILES[2][i]/1000)
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
			self.gmtim.append(hh + ' : ' + mm + ' : ' + ss)
				
			self.flrects.append(pygame.Rect(abs(halign - int(40/res.GSCALE)),int(200/res.GSCALE) + (i * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
			self.oprects.append([])
			self.oprects[i].append(pygame.Rect(abs(halign - 72),118 + (i * 51),24,24))
			self.oprects[i].append(pygame.Rect(abs(halign - 50),118 + (i * 51),24,24))
		self.flrects.append(pygame.Rect(abs(halign - int(40/res.GSCALE)),int(200/res.GSCALE) + (len(res.FILES[0]) * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
		for i in range(len(dtb.CHAPTERS) + 1):
			self.chrects.append(pygame.Rect(abs(halign - int(40/res.GSCALE)),int(200/res.GSCALE) + (i * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
		#self.chrects.append(pygame.Rect(abs(halign - int(40/res.GSCALE)),int(200/res.GSCALE) + (len(dtb.CHAPTERS) * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
		for i in range(len(dtb.PAUSE)):
			self.pserects.append(pygame.Rect(abs(halign - int(40/res.GSCALE)),int(200/res.GSCALE) + (i * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
		self.grd = [self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0)),
		self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0))]
		if res.GAMETIME == 0:
			res.new_data()
			res.recent_data(2)
		self.run()
		self.mnu = 0
		if res.GAMETIME > 0: self.msc.play(pygame.mixer.Sound(res.MUSIC_PATH + 'alchimera.mp3'))
		#LOADING SPRITES
		res.spr()
		res.battlesprites()
		res.animals()
		#LOADING SFX
		pygame.mixer.init()
		for j in sfxpath: 
			res.sfx(j)
			self.run()
		#LOADING BACKGROUNDS
		if True:
			if self.windoww > self.windowh: sz = self.windoww
			else: sz = self.windowh
			self.sltc = pygame.Surface((sz,sz),pygame.SRCALPHA)
			pygame.draw.ellipse(self.sltc,(250,250,250),pygame.Rect(0,0,sz,sz),30)
			pygame.draw.line(self.sltc,(250,250,250),(0,int(sz/2)),(sz,int(sz/2)),30)
			self.sltt = 0
			self.bbgs = [[]]
			for i in range(3):
				self.bbgs[0].append(pygame.transform.scale(pygame.image.load(res.BACKG_PATH + 'noise_' + str(i) + '.png'),(sz,sz)))
				self.run()
			for t in range(14):
				n = 13#need to save bckgs in other apps
				rvs = Image.open(res.BACKG_PATH + 'chp_' + str(n) + '.png')
				rvs = PIL.ImageOps.invert(rvs)
				self.bbgs.append([pygame.transform.scale(pygame.image.load(res.BACKG_PATH + 'chp_' + str(n) + '.png'),(sz,sz)),
				pygame.transform.scale(pygame.image.fromstring(rvs.tobytes(), rvs.size, rvs.mode),(sz,sz))])
				self.run()
		self.mnu = 3
		self.mscinfo = ''
		if res.GAMETIME == 0:
			#self.msc.play(pygame.mixer.Sound(res.MUSIC_PATH + 'alchimera.mp3'))
			self.wait = 200
			self.msg = -1
	
	def get_pressed(self,event):
		pressed = []
		for i in range(len(res.CONTROLS[0])):
			pressed.append([])
			for p in range(4):
				pressed[i].append(0)
		#KEYBOARD/MOUSE
		if res.MOUSE < 2:
			ky = pygame.key.get_pressed()
			for p in range(4):
				for i in range(len(res.CONTROLS[p])):
					pressed[i][p] = ky[res.CONTROLS[p][i]]
		#JOYSTICK
		pygame.joystick.init()
		connect = pygame.joystick.get_count()
		if connect > 1:
			res.MOUSE = 3
			joystick = pygame.joystick.Joystick(0)
			joystick.init()
			#for i in range(6 + joystick.get_numbuttons()): pressed.append([0])
			for b in range(4):
				if pressed[res.JOYSTICK[b]][0] == 0:
					pressed[res.JOYSTICK[b]][0] = int(joystick.get_axis(b))
			for b in range(joystick.get_numbuttons()):
				if res.JOYSTICK[b + 4] == None and pressed[b + 4][0] == 0: pressed[b + 4][0] = 0
				elif pressed[res.JOYSTICK[b + 4]][0] == 0: pressed[res.JOYSTICK[b + 4]][0] = joystick.get_button(b)
			for b in range(2):
				if res.JOYSTICK[b + 4 + joystick.get_numbuttons()] == None: pressed[b + 4 + joystick.get_numbuttons()][0] = 0
				elif pressed[res.JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] == 0:
					pressed[res.JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] = int(joystick.get_axis(b + 4))
			for i in pressed:
				while len(i) < 3: i.append(0)
		#TOUCH
		mp = pygame.mouse.get_pos()
		self.click = pygame.Rect(mp[0],mp[1],2,2)
		return pressed
	
	def events(self):
		for event in pygame.event.get():
			self.pressed = self.get_pressed(event)
			#EXIT
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.displayzw = int(self.windoww/res.GSCALE)
				self.displayzh = int(self.windowh/res.GSCALE)
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
				self.display = [pygame.Surface((self.displayzw, self.displayzh)),pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
				self.flrects = []
				self.oprects = []
				self.chrects = []
				for i in range(len(res.FILES[2])):
					ss = math.floor(res.FILES[2][i]/1000)
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
					self.gmtim.append(hh + ' : ' + mm + ' : ' + ss)
					
					self.flrects.append(pygame.Rect(self.displayzw - int(500/res.GSCALE),int(200/res.GSCALE) + (i * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
					self.oprects.append([])
					self.oprects[i].append(pygame.Rect(self.displayzw - 72,118 + (i * 51),24,24))
					self.oprects[i].append(pygame.Rect(self.displayzw - 50,118 + (i * 51),24,24))
				self.flrects.append(pygame.Rect(self.displayzw - int(500/res.GSCALE),int(200/res.GSCALE) + (len(res.FILES[0]) * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
				for i in range(len(dtb.CHAPTERS)):
					self.chrects.append(pygame.Rect(self.displayzw - int(500/res.GSCALE),int(200/res.GSCALE) + (i * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
				self.chrects.append(pygame.Rect(self.displayzw - int(500/res.GSCALE),int(200/res.GSCALE) + (len(dtb.CHAPTERS) * 51),int(460/res.GSCALE),int(100/res.GSCALE)))
				self.grd = []
				for g in range(200):
					srf = pygame.Surface((self.windoww,1),pygame.SRCALPHA)
					srf.fill((0,0,0,200 - g))
					self.grd.append(srf)
			lst = [0,0,0,self.flrects,self.chrects,0,0,0,0,0,self.pserects]
			if self.mnu == 11: self.settings.inside_events(self.pressed)
			if self.mnu == 12: self.about.inside_events(self.pressed)
			#MOUSE
			if res.MOUSE > 0:
				#SKIP
				if self.pressed[4][0]:
					if self.mnu < 2 and res.GAMETIME > 0: self.mnu += 1
					elif self.mnu == 6: self.skip = True
				#SELECT FILES
				if self.mnu in [3,4,10]:
					self.lopt = -1
					for i in range(len(lst[self.mnu])):
						mp = pygame.Rect(int(self.click.x/res.GSCALE),int(self.click.y/res.GSCALE),2,2)
						if pygame.Rect.colliderect(mp,pygame.Rect(lst[self.mnu][i].x,lst[self.mnu][i].y + self.scroll,lst[self.mnu][i].width,lst[self.mnu][i].height)):
							self.lopt = i
							if event.type == pygame.MOUSEBUTTONDOWN and lst[self.mnu][i].width == 250:
								if self.mnu == 3:
									#SELECT GAME
									if i < len(res.FILES[0]):
										res.ID = self.lopt
										self.lopt = -1
										self.mnu = 4
									#NEW GAME
									else:
										res.ID = self.lopt
										self.sfx.play(res.SOUND['FILE_NEW'])
										res.new_data()
										#res.recent_data(2,self.lopt)
										pygame.mixer.music.fadeout(3000)
										self.msc.fadeout(3000)
										self.ton.fadeout(3000)
										self.mnu = 7
								elif self.mnu == 4:
									#LOAD GAME
									if i < res.FILES[1][res.ID] + 1:
										self.sfx.play(res.SOUND['FILE_LOAD'])
										res.load_data()
										res.CHAPTER = self.lopt
										pygame.mixer.music.stop()
										self.ton.play(res.SOUND['NOISE'],-1)
										self.img = self.bbgs[0]
										self.msc.stop()
										self.scroll = int(50/res.GSCALE)
										self.wait = 50
										self.mnu = 8
										self.tv = 0
										self.txt = self.guitools.wrap(dtb.CHAPTERS[res.CHAPTER][2],self.fnt['RECAP'],self.windoww - 200)
									#DELETE GAME
									else:
										self.sfx.play(res.SOUND['FILE_DELETE'])
										res.delete_data()
										self.mnu -= 1
										self.scroll = 0
								elif self.mnu == 10:
									#CONTINUE
									if i == 0:
										self.mnu = 9
									#LOAD GAME
									if i == 1:
										self.mnu = 3
									#SAVE GAME
									if i == 2:
										self.mnu = 3
									#SETTINGS
									if i == 3:
										self.mnu = 11
									#ABOUT
									if i == 4:
										self.mnu = 12
									#EXIT GAME
									if i == 5:
										pygame.exit()
				#SELECT CHAPTER
				"""elif self.mnu == 4:
					self.lopt = -1
					for i in range(len(self.chrects)):
						if pygame.Rect.colliderect(self.click,pygame.Rect(self.chrects[i].x,self.chrects[i].y + self.scroll,self.chrects[i].width,self.chrects[i].height)):
							self.lopt = i
							if self.pressed[0] and self.chrects[i].width == 250:
								#LOAD GAME
								if i < res.FILES[1][res.ID] + 1:
									self.sfx.play(res.SOUND['FILE_LOAD'])
									res.load_data()
									res.CHAPTER = self.lopt
									pygame.mixer.music.stop()
									self.ton.play(res.SOUND['NOISE'],-1)
									self.img = self.bbgs[0]
									self.msc.stop()
									self.scroll = int(50/res.GSCALE)
									self.wait = 50
									self.mnu = 8
									self.tv = 0
									self.txt = self.guitools.wrap(dtb.CHAPTERS[res.CHAPTER][2],self.fnt['RECAP'],self.windoww - 200)
								#DELETE GAME
								else:
									self.sfx.play(res.SOUND['FILE_DELETE'])
									res.delete_data()
									self.mnu -= 1
									self.scroll = 0"""
			#KEYBOARD
			if res.MOUSE < 2:
				if self.pressed[5][0]:
					if self.mnu == 4: self.mnu = 3
				#SELECT
				if self.pressed[0][0] and self.mnu == 3: self.lopt -= 1; self.sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[1][0] and self.mnu == 3: self.lopt += 1; self.sfx.play(res.SOUND['MENU_VER'])

				if self.pressed[2][0] and self.mnu == 4: self.opt = 0; self.sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[3][0] and self.mnu == 4: self.opt = 1; self.sfx.play(res.SOUND['MENU_VER'])
			#RANGE LIMIT
			if res.MOUSE == 0:
				if self.lopt < 0: self.lopt = len(lst[self.mnu])
				if self.lopt > len(lst[self.mnu]): self.lopt = 0
		self.pressed = self.get_pressed(None)
		if self.mnu == 11: self.settings.outside_events(self.pressed)
		if self.mnu == 12: self.about.outside_events(self.pressed)

	def random(self,i=None):
		self.msc.pause()
		pygame.mixer.music.pause()
		self.ton.play(res.SOUND['NOISE'],-1)
		kp = str(self.tv)
		self.tv = 0
		self.rectrot = 0
		self.img = self.bbgs[0]
		chg = round(random.randint(0,100))
		if kp == '0': chg = 100
		elif i != None: chg = 100
		if self.mnu < 6 and self.lopt != -1:
			self.wait = round(random.randint(10,100))
			for i in range(round(random.randint(1,30)/self.FPS)): self.run()
			self.ton.stop()
			#CHANGE IMAGE
			if chg > 25:
				if self.lopt == -1: self.tv = 0
				elif self.mnu == 3:
					if self.lopt < len(res.FILES[1]) - 1:
						self.tv = round(random.randint(0,res.FILES[1][self.lopt])) + 1
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
				rd = round(random.randint(0,res.RANGE_RADIO - 1))
				if len(res.RADIO[rd]) > 0:
					sng = round(random.randint(0,len(res.RADIO[rd]) - 1))
					msc = res.MUSIC_PATH + res.RADIO[rd][sng] + '.mp3'
					if msc.endswith('.mp3'):
						audio = MP3(msc)
						pygame.mixer.music.load(msc)
						pygame.mixer.music.play(1,round(random.randint(20,int(audio.info.length) - 20)))
						try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
						except: self.mscinfo = {'TITLE': res.RADIO[rd][sng],'ARTIST': 'unknown','ALBUM': 'unknown'}
					elif msc.endswith('.wav'):
						audio = pygame.mixer.Sound(msc)
						self.msc.play(audio)
					elif msc.endswith('.ogg'):
						audio = pygame.mixer.Sound(msc)
						self.msc.play(audio)
			else: self.msc.unpause(); pygame.mixer.music.unpause()
			#CHANGE TRANSFORMATION
			if chg > 75:
				self.transform['VALUE'] = 0
				self.transform['TYPE'] = round(random.randint(2,3))
				spd = round(random.randint(0,100))
				if self.transform['TYPE'] == 5: self.transform['SPEED'] = 2
				elif spd > 75: self.transform['SPEED'] = -2
				elif spd > 50: self.transform['SPEED'] = 2
				elif spd > 25: self.transform['SPEED'] = -1
				else: self.transform['SPEED'] = 1
				if self.transform['TYPE'] in [0,4] and self.transform['SPEED'] < 0: self.transform['VALUE'] = round(random.randint(200,300))
				if self.transform['TYPE'] == 5: self.transform['VALUE'] = round(random.randint(1,2))
				if self.transform['TYPE'] in [1,4]:
					self.rectrot = self.img.get_rect(center=pygame.Rect(0,0,600,400).center)
	
	def intro(self):
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', math.floor(self.windoww/200) * 2)}
				self.display[1] = pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)
		self.screen.fill((0,0,10))
		#STARS
		if len(self.stars) < 10000:
			'''self.stars.append([(random.randint((self.windoww/2) - 5,(self.windoww/2) + 5),
			random.randint((self.windowh/2) - 5,(self.windowh/2) + 5)),random.randint(1,9)])'''
			prb = random.randint(0,100)
			if prb > 50: self.stars.append([[self.windoww,random.randint(0,self.windowh)],random.randint(3,12)])
		for i in self.stars:
			'''if i[1] == 1:
				i[0][0] += 2'''
			i[0][0] -= i[1]
			pygame.draw.rect(self.screen,(200,200,200),pygame.Rect(i[0][0],i[0][1],3,3))
		if len(self.stars) > 0:
			if self.stars[0][0][0] < 0: del self.stars[0]
		#BLACK BARS
		if self.mnu < 4 and self.winbar > 100:
			self.winbar -= 2 * self.FPS
		elif self.mnu == 4 and self.winbar < int(self.windowh/2):
			self.winbar += 10 * self.FPS
		elif self.mnu == 4:
			self.msc.fadeout(3000)
			self.classrun = False
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0,0,self.windoww,self.winbar))
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0,self.windowh - self.winbar,self.windoww,self.winbar))
		#MESSAGE
		if self.msg > -1 and self.msg < len(dtb.CHAPTERS[0][2]):
			sz = self.fnt['DEFAULT'].size(dtb.CHAPTERS[0][2][self.msg])[0]
			self.screen.blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[0][2][self.msg], True, (200,200,200)), (int(self.windoww/2) - int(sz/2),self.windowh - 50))
		#TIME
		self.wait -= 1
		if self.wait == 0:
			self.msg += 1
			if self.msg >= len(dtb.GINTRO):
				self.mnu = 4
			self.wait = 50
		
	def loading(self):
		flp = False
		#EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		#MESSAGES
		self.tim += 0.01
		if self.tim >= 1.0: self.tim = 0.0; self.msg = round(random.randint(0,len(dtb.MESSAGES) - 1)); flp = True
		#FILL DISPLAY
		if flp: self.screen.fill((0,0,0))
		else:
			self.screen.fill((0,0,0),pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
			self.screen.fill((0,0,0),pygame.Rect(42,self.windowh - 68,self.windoww - 154,6))
		#DRAW MESSAGES
		if res.GAMETIME > 0:
			for i in range(len(dtb.MESSAGES[self.msg])):
				self.screen.blit(self.fnt['DEFAULT'].render(dtb.MESSAGES[self.msg][i], True, (200,200,200)), (int(self.windoww/2) - 100, (int(self.windowh/2) - (len(dtb.MESSAGES[self.msg]) * 40)) + (i * 40)))
		#LOADING BAR
		pygame.draw.rect(self.screen,(200,200,200),pygame.Rect(40,self.windowh - 70,self.windoww - 150,10))
		pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(42,self.windowh - 68,math.floor((self.windoww - 154)/(self.fload/self.load)),6))
		#LOADING ICON
		self.gif += 1
		if self.gif >= 8: self.gif = 0
		self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'loading_' + str(self.gif) + '.png'), (self.windoww - 80, self.windowh - 80))
		#FLIP SCREEN
		if flp: pygame.display.flip()
		else:
			pygame.display.update(pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
			pygame.display.update(pygame.Rect(42,self.windowh - 68,self.windoww - 154,6))

	def menu(self):
		self.screen.fill((0,0,0))
		for i in self.display: i.fill((0,0,0,0))
		rztxt = math.floor((self.windoww/300)/2)
		#RANDOM SCREEN
		if self.mnu not in [6,5,9,10] and self.classrun and self.sltt == 140 and self.img != None:
			#RANDOM FONT
			if self.rndtxt < (100 + round(random.randint(5,20))): self.rndtxt += 1
			else: self.rndtxt = 0
			if self.rndtxt >= 100:
				dt = self.fnt.keys()
				lst = []
				for i in dt: lst.append(i)
				self.curfnt = lst[round(random.randint(0,len(self.fnt) - 1))]
			else: self.curfnt = 'DEFAULT'
			area = (0,-self.winbar,self.windoww,self.windowh - self.winbar)
			#NOISE
			if self.tv in [0,len(self.bbgs)]:
				self.noise += 1
				if self.noise == 3: self.noise = 0
				self.display[0].blit(self.img[self.noise], (0, 0))
			else:
				self.transform['VALUE'] += self.transform['SPEED'] * self.FPS
				if self.blink < (100 + round(random.randint(1,10))): self.blink += 1
				else: self.blink = 0
				img = self.img[math.floor(self.blink/100)]
				#SCALE
				if self.transform['TYPE'] == 0:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform['VALUE'] * 2),img.get_rect().height + round(self.transform['VALUE'] * 2)))
					self.display[0].blit(img, (600 - img.get_rect().width, 600 - img.get_rect().height),area)
				#ROTATE
				elif self.transform['TYPE'] == 1:
					img = pygame.transform.scale(img,(800,800))
					trs = pygame.transform.rotate(img,self.transform['VALUE'])
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot,area)
				#MOVE HORIZONTAL
				elif self.transform['TYPE'] == 2:
					self.display[0].blit(img, (self.transform['VALUE'], int(self.windowh/2) - int(img.get_rect().height/2)))
					if self.transform['VALUE'] < 0: self.display[0].blit(img, (img.get_rect().width + self.transform['VALUE'], 0),area)
					if self.transform['VALUE'] > 0: self.display[0].blit(img, (-img.get_rect().width + self.transform['VALUE'], 0),area)
				#MOVE VERTICAL
				elif self.transform['TYPE'] == 3:
					self.display[0].blit(img, (0, self.transform['VALUE']))
					if self.transform['VALUE'] < 0: self.display[0].blit(img, (0, img.get_rect().height + self.transform['VALUE']),area)
					if self.transform['VALUE'] > 0: self.display[0].blit(img, (0, -img.get_rect().height + self.transform['VALUE']),area)
				#SCALE AND ROTATE
				if self.transform['TYPE'] == 4:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform['VALUE']/6),img.get_rect().height + round(self.transform['VALUE']/4)))
					trs = pygame.transform.rotate(img,self.transform['VALUE'])
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot,area)
				#RANDOM
				if self.transform['TYPE'] == 5:
					if self.transform['VALUE'] > 13: self.transform['VALUE'] = 1
					img = pygame.image.load(res.BACKG_PATH + 'chp_' + str(self.transform['VALUE']) + str(self.blink) + '.png')
					self.display[0].blit(img, (0,0),area)
		#SETTINGS/ABOUT MENU
		lst = [0,0,0,self.flrects,self.chrects,0,0,0,0,0,self.pserects]
		if self.mnu in [11,12]:
			if self.mnu == 11: srf = self.settings.draw()
			if self.mnu == 12: srf = self.about.draw()
			for i in range(len(srf)): self.display[i].blit(srf[i],(100,100))
		#FILES/CHAPTERS MENU
		if self.mnu in [3,4,10]:
			scrl = 0
			for i in range(len(lst[self.mnu])):
				it = lst[self.mnu]
				if self.lopt == i:
					if it[i].width < 250:
						it[i].width += 4
						it[i].x -= 4
					if it[i].y > int(self.displayzh/2): scrl = -(it[i].height * i)
					else: scrl = int(self.displayzh/2) - int(it[i].height/2) - it[i].y
					if self.tv != i + 1 and self.wait == 0: self.random(i + 1)
					col = (255,255,0)
				else:
					if it[i].width > 230:
						it[i].width -= 4
						it[i].x += 4
					col = (255,255,255)
				shd = pygame.Surface((it[i].width,it[i].height))
				shd.set_alpha(100)
				shd.fill((10,10,10))
				self.display[0].blit(shd,(it[i].x + 5,it[i].y + 5 + self.scroll))
				pygame.draw.rect(self.display[0], col, pygame.Rect(it[i].x,it[i].y + self.scroll,it[i].width,it[i].height))
				if self.mnu == 3:
					if i != len(res.FILES[1]):
						self.display[1].blit(self.fnt[self.curfnt].render(dtb.CHAPTERS[res.FILES[1][i]][0], True, (0,0,0)), ((it[i].x + 10) * res.GSCALE, (110 + (i * 51) + self.scroll) * res.GSCALE))
						self.display[1].blit(self.fnt[self.curfnt].render(self.gmtim[i], True, (0, 0, 0)), ((it[i].x + 10) * res.GSCALE, (130 + (i * 51) + self.scroll) * res.GSCALE))
					else: self.display[1].blit(self.fnt[self.curfnt].render(dtb.MENU[61], True, (0,0,0)), ((it[i].x + 50) * res.GSCALE, (120 + (i * 51) + self.scroll) * res.GSCALE))
				if self.mnu == 4:
					if i != res.FILES[1][res.ID] + 1:
						self.display[1].blit(self.fnt[self.curfnt].render(dtb.CHAPTERS[i][0], True, (0,0,0)), ((it[i].x + 10) * res.GSCALE, (110 + (i * 51) + self.scroll) * res.GSCALE))
						self.display[1].blit(self.fnt[self.curfnt].render(dtb.CHAPTERS[i][1], True, (0,0,0)), ((it[i].x + 10) * res.GSCALE, (130 + (i * 51) + self.scroll) * res.GSCALE))
					else: self.display[1].blit(self.fnt[self.curfnt].render('excluir', True, (0,0,0)), ((it[i].x + 70) * res.GSCALE, (120 + (i * 51) + self.scroll) * res.GSCALE))
				if self.mnu == 10:
					self.display[1].blit(self.fnt[self.curfnt].render(dtb.PAUSE[i], True, (0,0,0)), ((it[i].x + 10) * res.GSCALE, (110 + (i * 51) + self.scroll) * res.GSCALE))
			#NEW FILE
			"""if self.lopt == len(res.FILES[0]):
				if self.flrects[len(res.FILES[1])].width < 250:
					self.flrects[len(res.FILES[1])].width += 4
					self.flrects[len(res.FILES[1])].x -= 4
				if self.flrects[len(res.FILES[1])].y > int(self.displayzh/2):
					scrl = -(self.flrects[len(res.FILES[1])].height * len(res.FILES[1]))
				else:
					scrl = int(self.displayzh/2) - int(self.flrects[len(res.FILES[1])].height/2) - self.flrects[len(res.FILES[1])].y
				col = (255,255,0)
			else:
				if self.flrects[len(res.FILES[1])].width > 230:
					self.flrects[len(res.FILES[1])].width -= 4
					self.flrects[len(res.FILES[1])].x += 4
				col = (255,255,255)
			shd = pygame.Surface((self.flrects[len(res.FILES[1])].width,self.flrects[len(res.FILES[1])].height))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.display[0].blit(shd,(self.flrects[len(res.FILES[1])].x + 5,self.flrects[len(res.FILES[1])].y + 5 + self.scroll))
			pygame.draw.rect(self.display[0], col, pygame.Rect(self.flrects[len(res.FILES[1])].x,self.flrects[len(res.FILES[1])].y + self.scroll,self.flrects[len(res.FILES[1])].width,self.flrects[len(res.FILES[1])].height))
			self.display[1].blit(self.fnt[self.curfnt].render(dtb.MENU[61], True, (0,0,0)), ((self.flrects[len(res.FILES[1])].x + 50) * res.GSCALE, (120 + (len(res.FILES[1]) * 51) + self.scroll) * res.GSCALE))
		#CHAPTERS MENU
		if self.mnu == 4:
			scrl = 0
			for i in range(res.FILES[1][res.ID] + 1):
				if self.lopt == i:
					if self.chrects[i].width < 250:
						self.chrects[i].width += 4
						self.chrects[i].x -= 4
					if self.chrects[i].y + self.scroll > int(self.displayzh/2):
						scrl = -(self.chrects[i].height * i)
					else:
						scrl = int(self.displayzh/2) - int(self.chrects[i].height/2) - self.chrects[i].y
					if self.tv != i + 1 and self.wait == 0: self.random(i + 1)
					col = (255,255,0)
				else:
					if self.chrects[i].width > 230:
						self.chrects[i].width -= 4
						self.chrects[i].x += 4
					col = (255,255,255)
				shd = pygame.Surface((self.chrects[i].width,self.chrects[i].height))
				shd.set_alpha(100)
				shd.fill((10,10,10))
				self.display[0].blit(shd,(self.chrects[i].x + 5,self.chrects[i].y + 5 + self.scroll))
				pygame.draw.rect(self.display[0], col, pygame.Rect(self.chrects[i].x,self.chrects[i].y + self.scroll,self.chrects[i].width,self.chrects[i].height))
				self.display[1].blit(self.fnt[self.curfnt].render(dtb.CHAPTERS[i][0], True, (0,0,0)), ((self.chrects[i].x + 10) * res.GSCALE, (110 + (i * 51) + self.scroll) * res.GSCALE))
				self.display[1].blit(self.fnt[self.curfnt].render(dtb.CHAPTERS[i][1], True, (0,0,0)), ((self.chrects[i].x + 10) * res.GSCALE, (130 + (i * 51) + self.scroll) * res.GSCALE))
			#DELETE FILE
			if self.lopt == res.FILES[1][res.ID] + 1:
				if self.chrects[res.FILES[1][res.ID] + 1].width < 250:
					self.chrects[res.FILES[1][res.ID] + 1].width += 4
					self.chrects[res.FILES[1][res.ID] + 1].x -= 4
				if self.chrects[res.FILES[1][res.ID] + 1].y + self.scroll > int(self.displayzh/2):
					scrl = -(self.chrects[res.FILES[1][res.ID] + 1].height * (res.FILES[1][res.ID] + 1))
				else:
					scrl = int(self.displayzh/2) - int(self.chrects[res.FILES[1][res.ID] + 1].height/2) - self.chrects[res.FILES[1][res.ID] + 1].y
				col = (255,255,0)
			else:
				if self.chrects[res.FILES[1][res.ID] + 1].width > 230:
					self.chrects[res.FILES[1][res.ID] + 1].width -= 4
					self.chrects[res.FILES[1][res.ID] + 1].x += 4
				col = (255,255,255)
			shd = pygame.Surface((self.chrects[res.FILES[1][res.ID] + 1].width,self.chrects[res.FILES[1][res.ID] + 1].height))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.display[0].blit(shd,(self.chrects[res.FILES[1][res.ID] + 1].x + 5,self.chrects[res.FILES[1][res.ID] + 1].y + 5 + self.scroll))
			pygame.draw.rect(self.display[0], col, pygame.Rect(self.chrects[res.FILES[1][res.ID] + 1].x,self.chrects[res.FILES[1][res.ID] + 1].y + self.scroll,self.chrects[res.FILES[1][res.ID] + 1].width,self.chrects[res.FILES[1][res.ID] + 1].height))
			self.display[1].blit(self.fnt[self.curfnt].render('excluir', True, (0,0,0)), ((self.chrects[res.FILES[1][res.ID] + 1].x + 70) * res.GSCALE, (120 + ((res.FILES[1][res.ID] + 1) * 51) + self.scroll) * res.GSCALE))
		"""
		if self.mnu in [3,4]:
			if self.scroll > scrl and self.scroll - 1 != scrl: self.scroll -= 2
			if self.scroll < scrl and self.scroll + 1 != scrl: self.scroll += 2
		#RECAP
		if self.mnu == 6:
			self.display[0].blit(self.bbgs[res.CHAPTER + 1][0], (0,math.floor(-self.scroll)))
			lt = 0
			for y in self.txt:
				self.display[1].blit(self.fnt['RECAP'].render(y, True, (0,0,0)), (101, (self.displayzh - math.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				self.display[1].blit(self.fnt['RECAP'].render(y, True, (0,0,0)), (102, (self.displayzh - math.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				self.display[1].blit(self.fnt['RECAP'].render(y, True, (255,255,255)), (100, (self.displayzh - math.floor(self.scroll * 1.5) + lt) * res.GSCALE))
				lt += 25
			self.scroll += 1 * self.FPS
			if self.scroll > (self.displayzh + int(lt/res.GSCALE)) - int(100/res.GSCALE) or self.skip:
				self.msc.fadeout(5000)
				self.mnu = 7
		#GRADIENT
		self.display[1].blit(self.grd[0],(0,0))
		self.display[1].blit(self.grd[1],(0,self.windowh - 200))
		#BLACK BARS
		if self.mnu in [3,4] and self.winbar > 100 and self.sltt == 140:
			self.winbar -= 10 * self.FPS
		if self.mnu == 7:
			if self.winbar < int(self.windowh/2):
				self.winbar += 10 * self.FPS
			if self.winbar == int(self.windowh/2):
				self.classrun = False
		if self.mnu == 9 and self.winbar > 0:
			self.winbar -= 10 * self.FPS
		if self.mnu == 10 and self.winbar < 100:
			self.winbar += 10 * self.FPS
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,0,self.windoww,self.winbar))
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,self.windowh - self.winbar,self.windoww,self.winbar))
		#INFO
		if self.mnu > 1 and self.mnu < 6:
			'''self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[0] + ' ' + res.VERSION + ':' + str(self.glock.get_fps()), True, (240,240,240)), ((-35 + int(self.displayzw/(self.displayzh/self.winbar))), (-35 + self.winbar)))
			if self.stime > 0:
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[1], True, (240,240,240)), ((self.windoww - 140 - int(self.displayzw/(self.displayzh/self.winbar))), (self.windowh + 35) - self.winbar))'''
			self.display[1].blit(self.fnt[self.curfnt].render(dtb.ABOUT[0][:9], True, (240,240,240)), (50,25))
			self.display[1].blit(self.fnt['MINI'].render(dtb.ABOUT[0][11:] + ' ' + res.VERSION, True, (240,240,240)), (50,55))
			if self.stime > 0:
				self.display[1].blit(self.fnt[self.curfnt].render(dtb.ABOUT[1], True, (240,240,240)), (self.windoww - 200,self.windowh - 35))
			#HOLIDAYS
			for i in dtb.HOLIDAYS:
				if self.holiday.month == i[0] and self.holiday.day == i[1]:
					sz = self.fnt[self.curfnt].size(i[2])[0] + 50
					self.display[1].blit(self.fnt[self.curfnt].render(i[2], True, (240,240,240)), (self.windoww - sz, 65))
			#SECRETS
			if self.stime > 0: self.stime -= 1 * self.FPS
			if self.stime <= 0:
				if self.sscroll > -20 - self.fnt[self.curfnt].size(self.stext)[0]:
					self.sscroll -= 3 * self.FPS
					self.display[1].blit(self.fnt[self.curfnt].render(self.stext, True, (240,240,240)),(self.sscroll,self.windowh - 50))
				else:
					self.sscroll = self.windoww + 20
					self.stext = dtb.TSECRETS[random.randint(0,len(dtb.TSECRETS) - 1)]
					self.stime = random.randint(600,1000)
		#WAIT
		if self.mnu > 0 and self.mnu < 6:
			if self.wait > 0 and self.tv > 0: self.wait -= 1 * self.FPS
			prb = round(random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv > 0 and self.sltt == 140: self.random()
		#LOAD GAME RECAP
		if self.mnu == 8:
			if self.wait > 0: self.wait -= 1 * self.FPS
			if self.wait == 0 and self.tv == 0:
				self.msc.play(pygame.mixer.Sound(res.MUSIC_PATH + 'fate_occurrences.mp3'),-1)
				self.ton.stop()
				self.mnu = 6
		#DRAW CIRCLE
		if self.sltt < 140:
			self.sltt += 5
			sz = self.sltc.get_rect()
			img = pygame.transform.scale(self.sltc,(int(sz.width/100) * self.sltt,int(sz.width/100) * self.sltt))
			sz = img.get_rect()
			self.screen.blit(img,((self.windoww/2) - (sz.width/2),(self.windowh/2) - (sz.height/2)))
		#DRAW SURFACES
		else:
			self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)),(0, 0))
			self.screen.blit(self.display[1],(0, 0))
		#MOUSE
		if res.MOUSE == 1:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'), pygame.mouse.get_pos())
		return self.display
		
	def run(self):
		if self.mnu < 3 and self.mnu != -1: self.load += 1
		#SPLASH
		'''if self.mnu == -1:
			self.events()
			self.screen.fill((0,0,0))
			srf = pygame.image.load('splash.png')
			sz = srf.get_rect()
			self.screen.blit(srf, (int(self.windoww/2) - int(sz.width/2),int(self.windowh/2) - int(sz.height/2)))
			pygame.display.flip()'''
		#LOGO
		if self.mnu < 2:
			self.events()
			self.screen.fill((0,0,0))
			#AUTHOR LOGO
			if self.mnu == 0:
				if self.logoalpha < 255 and self.wait == 0:
					self.logoalpha += 5 * self.FPS
				elif self.wait != (30 * self.FPS):
					self.wait += 1
				elif self.logoalpha > 0 and self.wait == (30 * self.FPS):
					self.logoalpha -= 10 * self.FPS
				else:
					self.wait = 0
					self.mnu = 1
			#SOURCE LOGO
			elif self.mnu == 1:
				if self.logoalpha < 255 and self.wait == 0:
					self.logoalpha += 10 * self.FPS
				elif self.wait != (30 * self.FPS):
					self.wait += 1
				elif self.logoalpha > 0 and self.wait == (30 * self.FPS):
					self.logoalpha -= 10 * self.FPS
				else:
					self.wait = 0
					self.mnu = 2
			#DRAW
			srf = pygame.Surface((600,400))
			if self.mnu == 0: srf.blit(self.bump, (0, 0))
			if self.mnu == 1: srf.blit(pygame.image.load(res.BACKG_PATH + 'source.png'), (0, 0))
			srf.set_alpha(self.logoalpha)
			self.screen.blit(srf, (int(self.windoww/2) - 300,int(self.windowh/2) - 200))
		elif self.mnu == 2:
			self.loading()
		else:
			if res.GAMETIME > 0 and res.TMNU:
				self.events()
				self.menu()
			else: self.classrun = False #self.intro()
		#UPDATE
		if self.mnu != 2:
			try: pygame.display.flip()
			except: self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
			self.glock.tick(int(60/self.FPS))

class Game:
	def __init__(self):
		#START GAME
		self.title = Title()
		while self.title.classrun: self.title.run()
		self.title.winbar = 0
		self.title.sltt = 140
		self.title.mnu = 9
		#GAME SETTINGS
		sz = pygame.display.Info()
		self.windoww = sz.current_w
		self.windowh = sz.current_h
		res.GSCALE = 3
		self.displayzw = int(self.windoww/res.GSCALE)
		self.displayzh = int(self.windowh/res.GSCALE)
		self.displayx = 0
		self.displayy = 0
		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((self.displayzw, self.displayzh)), pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
		self.glock = pygame.time.Clock()
		self.FPS = 0
		self.fnt = {'DEFAULT': pygame.font.Font(res.FONTS_PATH + res.FONT, 10 * res.GSCALE), 'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 30),
			'MININFO': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 25), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 15),
			'CONTROLKEYS': pygame.font.Font(res.FONTS_PATH + 'controlkeys.ttf', 15),'ANGER': pygame.font.Font(res.FONTS_PATH + res.FONT, 15 * res.GSCALE),
			'DISDBG': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', int(7.5 * res.GSCALE))}
		self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)
		self.camgrid = 1
		self.campos = [0,0]
		self.tilemation = 0
		self.rectdebug = True
		self.disdbg = True
		self.classrun = 1
		self.hpctrl = []
		self.waitime = 0
		self.waitlst = [['advice',432000],['rain',3600]]
		self.blankimg = pygame.Surface((self.windoww,self.windowh))
		self.blankimg.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
		self.blankimg.set_alpha(100)
		for x in range(math.ceil(self.blankimg.get_width()/10)):
			for y in range(math.ceil(self.blankimg.get_height()/10)):
				self.blankimg.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		#MIXER CHANNELS
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		pygame.mixer.music.set_volume(res.MSC)
		self.channels = []
		for i in range(4):
			self.channels.append([pygame.mixer.Channel(i + 4),None])
			self.channels[i][0].set_volume(res.SFX)
		self.ch_sfx = pygame.mixer.Channel(0) #for quick sounds
		self.ch_sfx.set_volume(res.SFX)
		self.ch_msc = pygame.mixer.Channel(1) #for background ambience loops
		self.ch_msc.set_volume(res.MSC)
		self.ch_ton = pygame.mixer.Channel(2) #for long sounds or jingles
		self.ch_ton.set_volume(res.SFX)
		self.ch_rng = pygame.mixer.Channel(3) #for phone ringtone
		self.ch_rng.set_volume(res.MSC)
		#MENU VARIABLES
		self.guitools = GUI.Guitools()
		self.tilset = self.guitools.get_tiles()
		self.rad = GUI.Radio()
		self.cal = GUI.Contacts()
		self.inv = GUI.Inventory((self.displayzw,self.displayzh))
		dv = self.inv.dev()
		self.dev = dv[0]
		if self.dev == 'radio': self.dev = self.rad
		if self.dev != None: self.dev.battery = dv[1]
		self.dvmp = pygame.Rect(0,0,2,2)
		self.vkb = GUI.Vkeyboard((self.windoww,self.windowh))
		self.minigame = None
		self.read = None
		#score counter, time counter
		self.counter = [[0,0,0]]
		self.opt = 1
		self.lopt = 0
		self.mnu = 1
		self.exvar = 0
		self.phone = 0
		self.phofa = 0
		self.winbar = int(self.displayzh/2)
		self.winbar = 0
		self.transtype = 'bars'
		self.grd = []
		for g in range(200):
			srf = pygame.Surface((self.windoww,1),pygame.SRCALPHA)
			srf.fill((0,0,0,200 - g))
			self.grd.append(srf)
		self.dmg = []
		self.actqueue = []
		self.notification = []
		self.dlg = {'TEXT': [], 'FADE': 500, 'Y': 0, 'CAMERA': 0, 'SPEED': res.SPEED, 'VOICE': 1, 'FONT': 'DEFAULT', 'TYPE': 0}
		self.tutorial = {'TEXT': [], 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 0, 'NEXT': '','GO': 0}
		self.chat = ['@kaixtr: Eu gosto disso!','@kanbz: Bem bacana!']
		self.cityname = ''
		#BATTLE VARIABLES
		self.equip = []
		self.battle = False
		self.btime = 100
		self.banimation = {'INDEX': None, 'GIF': 0}
		self.bbg = {'IMAGE': None, 'X': 0, 'ACC': 0, 'DIRECTION': False}
		self.obstacles = False
		self.hits = 0
		self.tdmg = 0
		self.hpl = 0
		self.tbt = 0
		self.turn = -1
		self.aim = pygame.Rect(300,int(self.displayzh/2),30,30)
		self.player = []
		self.barhp = []
		self.barpp = []
		self.barst = []
		self.barxp = []
		self.dices = []
		self.sttsy = 0
		#BARS
		x = 0
		for i in res.PARTY[res.FORMATION]:
			#HP BAR
			res.CHARACTERS[i]['HP'] = dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
			self.barhp.append(int(100/(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]/abs(res.CHARACTERS[i]['HP']))))
			#XP BAR
			if res.CHARACTERS[i]['XP'] > 0: self.barxp.append(int(100/(dtb.NEXTLEVEL[res.CHARACTERS[i]['LEVEL']]/res.CHARACTERS[i]['XP'])))
			else: self.barxp.append(0)
			#AMMO BAR
			self.equip.append(0)
			self.barpp.append([])
			for j in res.INVENTORY[i][4][1:]:
				if j[0] != '_':
					if j[0].startswith('gun') and int(j[1]) > 0: b = int(100/(dtb.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
					else: b = 0
					self.barpp[x].append(b)
				else:
					self.barpp[x].append(0)
			#PLAYER
			self.player.append({'RECT': pygame.Rect(res.PX,res.PY,20,20),'SPEED': 0,'ACC': 0,'SPEEDLOCK': False,'JUMP': 0,'GRAVITY': -5,'STEP': 10,
			'SWIM': None,'HEAT': res.TEMPERATURE,'HEAD': 'D','SPRITE': 'STANDD','SCORE': 0,'DRIVING': None,'SLEEP': False,'POSTURE': 1,
			'HAIR': res.CHARACTERS[i]['HAIR'],'SKIN': res.CHARACTERS[i]['SKIN'],
			'ACCESORIES': self.inv.find(i,['head'],'position'),'COSTUME': self.inv.find(i,['clth'],'position'),
			'GIF': 0.0,'BLINK': 100,'INVFRM': 0,'DMGTIM': 100,'SHK': 0,'DIRECTION': 3,'PAUSE': 0,
			'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','PLAYING': False,'NODES': [],'HOLD': None})
			x += 1
		self.player[0]['PLAYING'] = True
		self.donesprites = {}
		self.objects = []
		self.tilrect = []
		self.tilhide = False
		self.tilalpha = 0
		#MAP VARIABLES
		self.mapdata = {}
		self.enemies = []
		self.foe = []
		self.fig = []
		self.mrc = []
		self.npcs = []
		self.vehicles = []
		self.particles = []
		self.portalgo = {}
		#BUTTONS
		if res.MOUSE == 2:
			self.buttons = [pygame.Rect(20,self.windowh - 264,240,80),pygame.Rect(20,self.windowh - 100,240,80),pygame.Rect(20,self.windowh - 264,80,240),
			pygame.Rect(184,self.windowh - 264,80,240),pygame.Rect(self.windoww - 190,self.windowh - 100,80,80),pygame.Rect(self.windoww - 100,self.windowh - 100,80,80),
			pygame.Rect(self.windoww - 190,40,80,80),pygame.Rect(self.windoww - 100,40,80,80),pygame.Rect(20,40,80,80)]
		else: self.buttons = []
		#STUDIO
		self.editing = False
		self.paint = ''
		self.guit = 1
		self.build = ''
		self.slayer = 0
		self.shist = []
		self.ihist = 0
		self.sselect = [0,0,0,0]
		self.sstore = []
		#STARTING GAME
		if res.CHAPTER == 0 and res.SCENE == -3:
			self.tutorial = {'TEXT': dtb.TUTORIALS['BEGIN'], 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
			for j in self.tutorial['TEXT']:
				if isinstance(j,list):
					if j[0] == 'phone':
						self.tutorial['GO'] = j[1]
					if j[0] == 'wait':
						self.tutorial['WAIT'] = j[1]
						if len(j) > 2: self.tutorial['NEXT'] = j[2]
				else: self.tutorial['OUTPUT'].append(j)
			self.player[0]['PAUSE'] = 1
			self.loadmap('hauntedhouse_0')
			self.dev = self.cal
			self.phone = 1
			self.mnu = 1
		else:
			self.tilrect = [[437,437,437,437,437,0,437,437,437,0,0,437,437,437,0,0,437,437,437,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
			self.loadmap(res.MAP)
			"""for i in range(30): self.run()
			self.transiction(300,100,type='hole')
			for i in range(30): self.run()
			self.transiction(100,300,type='hole')
			for i in range(30): self.run()
			self.transiction(True,self.displayzw,type='side')
			for i in range(30): self.run()
			self.transiction(True,self.displayzw * 2,type='side')
			for i in range(30): self.run()
			self.transiction(True,1,type='zoom')
			for i in range(30): self.run()
			self.transiction(False,100,type='zoom')"""
			#self.transiction(False,0)

	def people(self,i,t):
		doll = None
		#ANIMATION
		if i['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(res.SPRITES[i['SPRITE']]): i['GIF'] = 0
		if i['PAUSE'] < 2: i['BLINK'] -= 1
		if i['BLINK'] < 0: i['BLINK'] = round(random.randint(30,90))
		#JUMP
		if i['GRAVITY'] > -5:
			i['JUMP'] += i['GRAVITY']
			i['GRAVITY'] -= 0.5
		if i['SPRITE'].startswith('SLEEP') == False:
			visible = True
			if t:
				if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 23: visible = False
				if i['INVFRM'] > 0:
					visible = not bool(i['INVFRM']%2)
					i['INVFRM'] -= 1
					if i['INVFRM'] == 0: self.sttsy = 0
			#MAP ICON
			if res.MAP == 'rodoviary':
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
			else:
				#DONE SPRITE
				sprstr = str(i['HAIR'][0]) + str(i['HAIR'][1]) + str(i['HAIR'][2]) + i['HEAD'] + str(math.floor(i['BLINK'])) + \
				'_' + i['SPRITE'] + str(i['SKIN']) + str(math.floor(i['GIF']))
				if sprstr in self.donesprites: doll = self.donesprites[sprstr]
				else:
					#EXTRA SPACEMENT
					if i['SPRITE'].startswith('STAND'): lst = [0,1,1,0]
					elif i['SPRITE'].startswith('TIREDSTAND'): lst = [0,1]
					elif i['SPRITE'].startswith('JUMP'): lst = [0,1]
					elif i['SPRITE'].startswith('WALK'): lst = [0,1,1,1,0,1,1,1]
					elif i['SPRITE'].startswith('RUN'): lst = [0,1,2,1,0,1,2,1]
					else: lst = [0]
					try: xsp = lst[math.floor(i['GIF'])]
					except: xsp = 0
					if i['SPRITE'].endswith('L') or i['SPRITE'].endswith('R'): xsp += 1
					if i['JUMP'] > 0: xsp = 1
					if i['HEAD'].startswith('DD'): xsp += 1
					#HEAD
					if i['HAIR'][1] >= 10: nb = str(i['HAIR'][1] - 1)
					else: nb = '0' + str(i['HAIR'][1] - 1)
					if nb == '0-1': nb = '00'
					dd = False
					if i['HEAD'] == 'L':
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_H.png')
						head_img = pygame.image.load(res.TEMP_PATH + 'headH.png')
					elif i['HEAD'] == 'LU':
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_U.png')
						head_img = pygame.image.load(res.TEMP_PATH + 'headU.png')
					elif i['HEAD'] == 'LD':
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_LD.png')
						head_img = pygame.image.load(res.TEMP_PATH + 'headHD.png')
					elif i['HEAD'] == 'R':
						hair_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_H.png'),True,False)
						head_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'headH.png'),True,False)
					elif i['HEAD'] == 'RU':
						hair_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_U.png'),True,False)
						head_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'headU.png'),True,False)
					elif i['HEAD'] == 'RD':
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_RD.png')
						head_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'headHD.png'),True,False)
					elif i['HEAD'] == 'DD':
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_D.png')
						head_img = pygame.image.load(res.TEMP_PATH + 'headD.png')
						dd = True
					else:
						hair_img = pygame.image.load(res.TEMP_PATH + 'hair_' + nb + '_' + i['HEAD'] + '.png')
						head_img = pygame.image.load(res.TEMP_PATH + 'head' + i['HEAD'] + '.png')
					if i['HAIR'][1] > 0:
						hair_img.fill((res.PALETTES[1][int(i['HAIR'][0])]),None,pygame.BLEND_RGBA_MULT)
						hair_rect = hair_img.get_rect()
					else:
						hair_rect = head_img.get_rect()
						hair_img = pygame.Surface((hair_rect.width,hair_rect.height),pygame.SRCALPHA)
					head_img.fill((res.PALETTES[0][int(i['SKIN'])]),None,pygame.BLEND_RGBA_MULT)
					head_rect = head_img.get_rect()
					eye_img = None
					mouth_img = None
					fh_img = None
					acc_img = []
					if int(i['DIRECTION']) < 6:
						#EYES
						if i['BLINK'] < 2 and i['GRAVITY'] == -5 and i['JUMP'] == 0: eye_img = 'eye_1'
						else: eye_img = 'eye_0'
						eye_img = pygame.image.load(res.TEMP_PATH + eye_img + '.png')
						#MOUTH
						if self.dlg['CAMERA'] == i['RECT']:
							mouth_img = pygame.image.load(res.TEMP_PATH + 'mouth_' + str(math.floor(i['GIF'])) + '.png')
							mouth_rect = mouth_img.get_rect()
						#FACIAL HAIR
						if i['HAIR'][2] > 0:
							if i['HAIR'][2] >= 10: nb = str(i['HAIR'][2] - 1)
							else: nb = '0' + str(i['HAIR'][2] - 1)
							if i['HEAD'] == 'L':
								fh_img = pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_H.png')
							elif i['HEAD'] == 'LD':
								fh_img = pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_HD.png')
							elif i['HEAD'] == 'R':
								fh_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_H.png'),True,False)
							elif i['HEAD'] == 'RD':
								fh_img = pygame.transform.flip(pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_HD.png'),True,False)
							elif i['HEAD'] == 'DD':
								fh_img = pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_D.png')
								dd = True
							else:
								fh_img = pygame.image.load(res.TEMP_PATH + 'fhair_' + nb + '_D.png')
							fh_img.fill((res.PALETTES[1][int(i['HAIR'][0])]),None,pygame.BLEND_RGBA_MULT)
						#ACCESORIES
						if t and i['ACCESORIES'] != []:
							for acc in i['ACCESORIES']:
								it = res.INVENTORY[acc[0]][acc[1]][acc[2]][acc[3]]
								if it != 'head_hairclip':
									acc_img.append(pygame.image.load(res.TEMP_PATH + it + '.png'))
					#FACE
					if i['DIRECTION'] == 1: xx = 4
					elif i['DIRECTION'] == 2: xx = 1
					elif i['DIRECTION'] == 4: xx = -1
					elif i['DIRECTION'] == 5: xx = -4
					else: xx = 0
					if dd: yy = 1
					else: yy = 0
					if eye_img != None:
						head_img.blit(eye_img,(1 + xx,4 + yy))
					if mouth_img != None:
						head_img.blit(mouth_img,(2 + xx,7 + yy))
					if acc_img != []:
						for acc in acc_img:
							head_img.blit(acc,(xx,5 + yy))
					face_srf = pygame.Surface((hair_rect.width,hair_rect.height),pygame.SRCALPHA)
					face_srf.blit(head_img,((hair_rect.width/2) - (head_rect.width/2),1 + (hair_rect.height/2) - (head_rect.height/2)))
					face_srf.blit(hair_img,(0,0))
					if fh_img != None:
						face_srf.blit(fh_img,((hair_rect.width/2) - (head_rect.width/2),7 + (hair_rect.height/2) - (head_rect.height/2)))
					#HOLDING ITEM
					if i['HOLD'] != None:
						xx = -5; yy = -20
						if i['DIRECTION'] in [1,2,8]: xx = 10
						if i['DIRECTION'] in [4,5,6]: xx = -20
						if i['DIRECTION'] in [2,3,4]: yy = 5
						if i['DIRECTION'] in [6,7,8]: yy = -30
						self.tilrect[2][i['HOLD']][1].x = i['RECT'].x + xx
						self.tilrect[2][i['HOLD']][1].y = i['RECT'].y + yy
					#BODY
					if i['SWIM'] == None:
						if t and i['SLEEP']: body_img = res.SPRITES['REST'][0].copy()
						else: body_img = res.SPRITES[i['SPRITE']][math.floor(i['GIF'])].copy()
						body_img.fill((res.PALETTES[0][int(i['SKIN'])]),None,pygame.BLEND_RGBA_MULT)
						#CLOTHES
						'''clth_img = []
						if t and i['COSTUME'] != [] and int(i['DIRECTION']) < 6:
							for clth in i['COSTUME']:
								it = res.INVENTORY[clth[0]][clth[1]][clth[2]][clth[3]]
								cc = pygame.image.load(res.TEMP_PATH + it[0:-2] + '_' + i['SPRITE'] + '.png')
								cc.fill((res.PALETTES[1][dtb.ITEMS[it][5]]),None,pygame.BLEND_RGBA_MULT)
								clth_img.append(cc)
						if clth_img != []:
							for clth in clth.img:
								body_img.blit(clth,(0,0))'''
					#SWIMMING
					else:
						xsp += 21
						i['SWIM'] += 0.1
						if i['SWIM'] > 1.5: i['SWIM'] = 0.0
						body_img = pygame.image.load(res.SPRITES_PATH + 'water_' + str(math.floor(i['SWIM'])) + '.png')
					#DRAW
					fsz = face_srf.get_rect()
					bsz = body_img.get_rect()
					if bsz.width > fsz.width: wd = bsz.width
					else: wd = fsz.width
					doll = pygame.Surface((wd,fsz.height + bsz.height),pygame.SRCALPHA)
					doll.blit(body_img,((wd/2) - (bsz.width/2),fsz.height))
					doll.blit(face_srf,((wd/2) - (fsz.width/2),xsp))
					#doll = pygame.transform.scale(doll,(wd * 2,(fsz.height + bsz.height) * 2))
					self.donesprites[sprstr] = doll
				#SHADE
				if i['SPRITE'].startswith('SEAT') == False or i['SPRITE'].startswith('DRIVE') == False:
					if res.TIME[0] < 12:
						tms = (12 - res.TIME[0]) * 2
						sxx = i['RECT'].x - self.cam.x - tms + 5
					else:
						tms = (res.TIME[0] - 12) * 2
						sxx = i['RECT'].x - self.cam.x
					if tms < 5: tms = 5
					shd = pygame.transform.scale(pygame.transform.rotate(doll,90),(tms,7))
					shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					shd.set_alpha(100)
					self.display[0].blit(shd, (sxx,i['RECT'].y - self.cam.y + 5))
				if visible:
					img = doll.copy()
					if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					self.display[0].blit(img,(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y - i['RECT'].height - i['JUMP']))
		return doll
					
	def pet(self, i):
		#ANIMATION
		if self.player[0]['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(i['SPRITE']): i['GIF'] = 0
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
		if res.TIME[0] < 12:
			tms = (12 - res.TIME[0]) * 2
			sxx = i['RECT'].x - self.cam.x - tms + 5
		else:
			tms = (res.TIME[0] - 12) * 2
			sxx = i['RECT'].x - self.cam.x
		if tms < 5: tms = 5
		img = i['SPRITE'][math.floor(i['GIF'])]
		shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,4))
		shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
		shd.set_alpha(100)
		self.display[0].blit(shd, (sxx, i['RECT'].y - self.cam.y))
		self.display[0].blit(img, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
		#MOVEMENT
		if self.winbar == 0:
			#FOLLOW MOVEMENT
			if i['MOVE'] == 'follow':
				if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y:
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 8
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 6
					else: i['DIRECTION'] = 7

				elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: 
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 2
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 3

				elif i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 8
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 2
					else: i['DIRECTION'] = 1

				elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 6
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 5
			#HORIZONTAL MOVEMENT
			elif i['MOVE'] == 'walk':
				if i['DIRECTION'] == 0:
					i['DIRECTION'] = 1
			#MOVING
			if self.player[0]['PAUSE'] < 3 and i['SPEED'] != 0:
				if i['DIRECTION'] == 1: i['RECT'].x += i['SPEED'] - 1
				if i['DIRECTION'] == 2: i['RECT'].x += i['SPEED'] - 1; i['RECT'].y += i['SPEED'] - 1
				if i['DIRECTION'] == 3: i['RECT'].y += i['SPEED'] - 1
				if i['DIRECTION'] == 4: i['RECT'].x -= i['SPEED'] - 1; i['RECT'].y += i['SPEED'] - 1
				if i['DIRECTION'] == 5: i['RECT'].x -= i['SPEED'] - 1
				if i['DIRECTION'] == 6: i['RECT'].x -= i['SPEED'] - 1; i['RECT'].y -= i['SPEED'] - 1
				if i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED'] - 1
				if i['DIRECTION'] == 8: i['RECT'].x += i['SPEED'] - 1; i['RECT'].y -= i['SPEED'] - 1
				i['TIME'] -= 1
			#TIMING
			if i['TIME'] <= 0:
				if i['FILE'].startswith('PIGEON'):
					do = random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit': i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand': i['MOVE'] = 'sit'
					elif do == 1:
						dl = [1,5]
						i['DIRECTION'] = dl[random.randint(0,1)]
						i['MOVE'] = 'walk'
				elif i['FILE'].startswith('DOG'):
					do = random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit': i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand': i['MOVE'] = 'sit'
					elif do == 1:
						dl = [1,5]
						i['DIRECTION'] = dl[random.randint(0,1)]
						i['MOVE'] = 'walk'
				if i['DIRECTION'] == 1: dr = 'L'
				if i['DIRECTION'] == 5: dr = 'R'
				i['SPRITE'] = res.SPRITES[i['FILE'] + '_' + i['MOVE'].upper() + dr]
				i['TIME'] = 20

	def enemy(self, i):
		if self.battle == False:
			#DRAW
			if self.rectdebug: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			img = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_mini.png')
			if res.TIME[0] < 12:
				tms = (12 - res.TIME[0]) * 2
				sxx = i['RECT'].x + int(i['RECT'].width/2) - self.cam.x - tms + 5
			else:
				tms = (res.TIME[0] - 12) * 2
				sxx = i['RECT'].x + int(i['RECT'].width/2) - self.cam.x
			if tms < 5: tms = 5
			shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,7))
			shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
			shd.set_alpha(100)
			self.display[0].blit(shd, (sxx, i['RECT'].y - self.cam.y))
			for b in res.BESTIARY:
				if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
					img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
			self.display[0].blit(img, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - (img.get_height() - 10)))
			if i['PATH'] == 'notice': self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'notice.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - 30))
			#REPELLENT
			rplt = False
			for c in res.PARTY[res.FORMATION]:
				if res.CHARACTERS[c]['HEALTH'] == 2: rplt = True
		if self.winbar == 0 and self.battle == False and i['FIGHTING'] == False:
			#NOTICING
			if i['PATH'] == 'notice':
				if i['TIME'] == 0:
					i['PATH'] = 'follow'
			#STEALTH MOVEMENT
			elif i['PATH'] == 'stealth':
				if self.facing(i,self.player[0]) == 2 and rplt == False:
					self.ch_sfx.play(res.SOUND['NOTICED'])
					i['PATH'] = 'notice'
					i['TIME'] = 10
				else:
					if i['DIRECTION'] == 0:
						i['DIRECTION'] = 1

					if i['TIME'] == 0:
						if i['DIRECTION'] == 1: i['DIRECTION'] = 5
						elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
						i['TIME'] = 20
			#FOLLOW MOVEMENT
			elif i['PATH'] == 'follow':
				if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y:
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 8
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 6
					else: i['DIRECTION'] = 7

				elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: 
					if i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 2
					elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 3

				elif i['RECT'].x - self.cam.x < self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 8
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 2
					else: i['DIRECTION'] = 1

				elif i['RECT'].x - self.cam.x > self.player[0]['RECT'].x + 10 - self.cam.x:
					if i['RECT'].y - self.cam.y > self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 6
					elif i['RECT'].y - self.cam.y < self.player[0]['RECT'].y - 5 - self.cam.y: i['DIRECTION'] = 4
					else: i['DIRECTION'] = 5
				if rplt:
					i['PATH'] = 'horizontal'
					i['DIRECTION'] = 0
					i['TIME'] = 20
			#HORIZONTAL MOVEMENT
			elif i['PATH'] == 'horizontal':
				if i['DIRECTION'] == 0:
					i['DIRECTION'] = 1
				if i['TIME'] == 0:
					if i['DIRECTION'] == 1: i['DIRECTION'] = 5
					elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
					i['TIME'] = 20
			#MOVING
			if self.player[0]['PAUSE'] < 3 and i['PATH'] != 'stay':
				if i['DIRECTION'] == 1: i['RECT'].x += i['AGILITY'] - 1
				if i['DIRECTION'] == 2: i['RECT'].x += i['AGILITY'] - 1; i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 3: i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 4: i['RECT'].x -= i['AGILITY'] - 1; i['RECT'].y += i['AGILITY'] - 1
				if i['DIRECTION'] == 5: i['RECT'].x -= i['AGILITY'] - 1
				if i['DIRECTION'] == 6: i['RECT'].x -= i['AGILITY'] - 1; i['RECT'].y -= i['AGILITY'] - 1
				if i['DIRECTION'] == 7: i['RECT'].y -= i['AGILITY'] - 1
				if i['DIRECTION'] == 8: i['RECT'].x += i['AGILITY'] - 1; i['RECT'].y -= i['AGILITY'] - 1
				i['TIME'] -= 1
		#PLAYER COLISION
		if self.battle == False and self.colide(i['RECT'], self.player[0]['RECT']) and i['DIRECTION'] > 0 and self.dlg['FADE'] == 500:
			if i['FIGHTING'] == False and rplt == False:
				#BATTLE ENTER
				if res.BTYPE < 3:
					if i['TYPE'] != 'mercenary': self.foe.append(i)
					else: self.mrc.append(i)
					i['FIGHTING'] = True
					if (len(self.foe) + len(self.mrc)) == 1:
						for b in res.BESTIARY:
							if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
								self.turn = -6
								break
						if self.phone > 0: self.turn = -2
						if self.inv.type > 0: self.turn = -2
						if self.turn != -6: self.turn = -self.facing(i,self.player[0])
						self.fight()
				#DAMAGE
				elif self.player[0]['INVFRM'] == 0:
					if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HP'] > 0:
						res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HP'] -= i['STRENGHT']
						self.ch_ton.play(res.SOUND['BATTLE_LOST'])
						self.player[0]['INVFRM'] = 60
						while self.sttsy < 120:
							self.sttsy += 10
							self.run()
					else:
						self.ch_ton.play(res.SOUND['GAME_OVER'])
		#BATTLE IMAGE
		if self.battle and i['FADE'] > 0 and i['HEALTH'] != 9:
			i['FIGHTING'] = True
			if i['MASK'].x < self.displayzw:
				#MOVE
				if self.mnu == 2 and self.equip[self.turn] < 4 and i['HEALTH'] != 1:
					if i['DODGE'] == 'walk':
						if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
						if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']
						if i['MASK'].x < int(self.displayzw/6): i['DIRECTION'] = 1
						if i['MASK'].x > (self.displayzw - int(self.displayzw/6)): i['DIRECTION'] = 5
					if i['DODGE'] == 'jump':
						if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
						if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']
						if i['MASK'].x < int(self.displayzw/6): i['DIRECTION'] = 1
						if i['MASK'].x > (self.displayzw - int(self.displayzw/6)): i['DIRECTION'] = 5
						i['MASK'].y += i['SPEED']
						i['SPEED'] -= 0.5
						if i['SPEED'] == -3.0:
							i['DIRECTION'] = 5
							i['SPEED'] = 3
					if i['DODGE'] == 'fly':
						if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
						if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']
						if i['MASK'].x < int(self.displayzw/6): i['DIRECTION'] = 1
						if i['MASK'].x > (self.displayzw - int(self.displayzw/6)): i['DIRECTION'] = 5
						i['MASK'].y += i['SPEED']
						if i['DIRECTION'] == 1:
							i['SPEED'] -= 0.5
							if i['SPEED'] == -3.0: i['DIRECTION'] = 5
						if i['DIRECTION'] == 5:
							i['SPEED'] += 0.5
							if i['SPEED'] == 3.0: i['DIRECTION'] = 1
					if i['DODGE'] == 'spin':
						i['MASK'].x += i['SPEED']
						if i['DIRECTION'] == 1:
							i['SPEED'] -= 0.5
							if i['SPEED'] == -3.0: i['DIRECTION'] = 5
						if i['DIRECTION'] == 5:
							i['SPEED'] += 0.5
							if i['SPEED'] == 3.0: i['DIRECTION'] = 1
					if i['DODGE'] == 'circle':
						i['MASK'].x = int(math.cos(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzw/2) - 50
						i['MASK'].y = int(math.sin(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzh/2) - 50
						i['SPEED'] += 0.5
				elif self.mnu == 1:
					if i['DODGE'] == 'jump': i['SPEED'] = 3.0
					if i['DODGE'] in ['fly','spin','circle']: i['SPEED'] = 0.0
				if i['FADE'] < 10:
					#i['SPRITE'].blit(pygame.image.load(res.SPRITES_PATH + 'eff_death_' + str(i['FADE']) + '.png'), (0,0), special_flags=pygame.BLEND_SUB)
					if i['FADE'] > 5: i['SPRITE'].fill((int((i['FADE'] - 5) * 50),10,10),None,pygame.BLEND_RGBA_MULT)
					elif i['FADE'] > 0: i['SPRITE'].fill((200,10,10,int(i['FADE'] * 50)),None,pygame.BLEND_RGBA_MULT)
				#DRAW
				if i['AWAY'] == 0:
					self.display[0].blit(i['SPRITE'], (int(i['MASK'].x) + int(self.bbg['X'] * 1.5), int(i['MASK'].y)))
				else:
					i['AWAY'] += 1
					szw = i['SPRITE'].get_width() - (int(i['SPRITE'].get_width()/20) * i['AWAY'])
					szh = i['SPRITE'].get_height() - (int(i['SPRITE'].get_height()/20) * i['AWAY'])
					if szw < 0: szw = 0
					if szh < 0: szh = 0
					if szw == 0 and szh == 0:
						i['FIGHTING'] = False
						i['FADE'] = 0
					self.display[0].blit(pygame.transform.scale(i['SPRITE'],(szw,szh)), (i['MASK'].x, i['MASK'].y - i['AWAY']))
				#EFFECTS ANIMATION
				if i['HEALTH'] > 2:
					self.display[0].blit(res.SPRITES['EFFECT_' + str(i['HEALTH'])][math.floor(i['EFFECT'])], (i['MASK'].x + 5 + math.floor(self.bbg['X']/3), i['MASK'].y - 10))
					i['EFFECT'] += 0.5
					if i['EFFECT'] >= len(res.SPRITES['EFFECT_' + str(i['HEALTH'])]): i['EFFECT'] = 0.0
			else: i['MASK'].x -= i['AGILITY']
		#SHOOT
		if res.BTYPE == 3:
			ind = 0
			for p in self.particles:
				if p['TYPE'] == 'gunshot' and self.colide(i['RECT'],pygame.Rect(p['X'],p['Y'],p['RADIUS'],p['RADIUS'])):
					self.ch_sfx.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
					self.hitisplay(10, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y,1,1), '50', (200, 200, 200))
					self.player[p['PLAYER']]['SCORE'] += 10
					i['FIGHTING'] = False
					i['HP'] = 0
					del self.particles[ind]
					break
				ind += 1
	
	def npc(self, i):
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
		if i['TYPE'] in [0,2,3,4]: imgrct = self.people(i,False)
		elif i['TYPE'] >= 5:
			shk = 0
			if i['TYPE'] == 11:
				for w in res.WASH:
					if w[1] == i['WHO']:
						shk = int(random.randint(-2,2))
						break
			imgrct = pygame.image.load(res.SPRITES_PATH + 'obj_' + str(i['INDEX']) + '.png')
			self.display[0].blit(imgrct, (i['RECT'].x - self.cam.x + shk, i['RECT'].y - self.cam.y - 10))
			if self.player[0]['SLEEP'] and i['TYPE'] == 6: self.people(self.player[0],False)
		else: imgrct = pygame.Surface((i['RECT'].width,i['RECT'].height))
		#FOLLOW
		if i['FOLLOW'] != None and i['FOLLOW'] != (None,None):
			i['SPEED'] = 3
			if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y:
				if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 8
				elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 6
				else: i['DIRECTION'] = 7
			elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: 
				if i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 2
				elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x: i['DIRECTION'] = 4
				else: i['DIRECTION'] = 3
			elif i['RECT'].x - self.cam.x < i['FOLLOW'].x - self.cam.x:
				if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 8
				elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 2
				else: i['DIRECTION'] = 1
			elif i['RECT'].x - self.cam.x > i['FOLLOW'].x - self.cam.x:
				if i['RECT'].y - self.cam.y > i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 6
				elif i['RECT'].y - self.cam.y < i['FOLLOW'].y - self.cam.y: i['DIRECTION'] = 4
				else: i['DIRECTION'] = 5
		#HORIZONTAL
		if self.battle == False and i['TYPE'] == 0 and i['FOLLOW'] == None:
			if i['MOVE'] == 'horizontal':
				i['SPEED'] = 1
				if i['DIRECTION'] not in [1,5]:
					i['DIRECTION'] = 1
				if i['TIME'] == 0:
					if i['DIRECTION'] == 1: i['DIRECTION'] = 5
					elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
					i['TIME'] = 30
				i['TIME'] -= 1
			#SIDEWALK
			elif i['MOVE'] == 'sidewalk':
				i['SPEED'] = 1
				try: t = self.tilrect[1][(math.floor((i['RECT'].y + 15)/self.map.tilewidth) * self.map.width) + math.floor((i['RECT'].x + 15)/self.map.tilewidth)]
				except: t = None
				if self.rectdebug and t != None:
					pygame.draw.rect(self.display[0], (255,200,0), pygame.Rect(t[1].x - self.cam.x, t[1].y - self.cam.y, t[1].width, t[1].height),3)
				if t != None and t[0]['TYPE'].startswith('SIDEWALK'): #and self.colide(i['RECT'],t[1]):
					if t[0].endswith('1'):
						if i['DIRECTION'] in [1,2]: i['DIRECTION'] = 7
						if i['DIRECTION'] in [3,4]: i['DIRECTION'] = 5
						if i['DIRECTION'] in [5,6]: i['DIRECTION'] = 3
						if i['DIRECTION'] in [7,8]: i['DIRECTION'] = 1
					elif t[0].endswith('2'):
						if i['DIRECTION'] in [1,2]: i['DIRECTION'] = 3
						if i['DIRECTION'] in [3,4]: i['DIRECTION'] = 1
						if i['DIRECTION'] in [5,6]: i['DIRECTION'] = 7
						if i['DIRECTION'] in [7,8]: i['DIRECTION'] = 5
			elif i['MOVE'] == 'nodeon':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(i['RECT'],n['RECT']):
						if n['GOING'] == 1: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'nodeoff':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(i['RECT'],n['RECT']):
						if n['GOING'] == 0: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'fixed': i['SPEED'] = 0
		#MOVEMENT
		dirs = ['R','RD','D','LD','L','LU','U','RU']
		if self.player[0]['PAUSE'] < 3:
			if i['SPEED'] > 0:
				i['HEAD'] = dirs[i['DIRECTION'] - 1]
				i['SPRITE'] = 'WALK' + dirs[i['DIRECTION'] - 1]
				if i['DIRECTION'] == 1: i['RECT'].x += i['SPEED']
				if i['DIRECTION'] == 2: i['RECT'].x += i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 3: i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 4: i['RECT'].x -= i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 5: i['RECT'].x -= i['SPEED']
				if i['DIRECTION'] == 6: i['RECT'].x -= i['SPEED']; i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 8: i['RECT'].x += i['SPEED']; i['RECT'].y -= i['SPEED']
			elif i['MOVE'] == 'stand':
				i['HEAD'] = dirs[i['DIRECTION'] - 1]
				i['SPRITE'] = 'STAND' + dirs[i['DIRECTION'] - 1]
				i['MOVE'] = 'fixed'
			elif i['MOVE'] == 'seat':
				i['HEAD'] = dirs[i['DIRECTION'] - 1]
				i['SPRITE'] = 'SEAT' + dirs[i['DIRECTION'] - 1]
			else: i['SPRITE'] = 'STAND' + dirs[i['DIRECTION'] - 1]
			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
					if self.colide(i['RECT'],i['FOLLOW']):
						if i['FOLLMOV'] != '': i['MOVE'] = i['FOLLMOV']
						i['DIRECTION'] = i['FOLLEND']
						i['FOLLOW'] = None
						i['FOLLEND'] = 0
						i['FOLLMOV'] = ''
						i['SPEED'] = 0
				else:
					if i['FOLLMOV'] != '': i['MOVE'] = i['FOLLMOV']
					i['DIRECTION'] = i['FOLLEND']
					i['FOLLOW'] = None
					i['FOLLEND'] = 0
					i['FOLLMOV'] = ''
					i['SPEED'] = 0
		#ACTIONS
		for p in self.player:
			cld = 0
			if self.colide(p['RECT'],i['RECT']) and p['PLAYING']: cld = 1
			else:
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(int(mp[0]/res.GSCALE),int(mp[1]/res.GSCALE),2,2)
				if imgrct != None and self.colide(mr,pygame.Rect(i['RECT'].x - self.cam.x,i['RECT'].y - imgrct.get_height() - self.cam.y,imgrct.get_width(),imgrct.get_height())): cld = 2
			if cld > 0 and self.portalgo == {} and i['WHO'] != None:
				if i['TALKING'] == False:
					#ARROW
					if self.battle == False and self.dlg['CAMERA'] != i['RECT'] and self.dlg['FADE'] > 0 and isinstance(i['TYPE'],str) == False:
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (i['RECT'].x - self.cam.x + int(i['RECT'].width/2) - 5, i['RECT'].y - self.cam.y - i['RECT'].height * 2))
						self.hpctrl = dtb.HINTS['NPC_DIALOG']
					#SCENE CHANGE
					if isinstance(i['TYPE'],str) and i['TYPE'].startswith('scene'):
						if res.SCENE == int(i['TYPE'][5]) - 1:
							res.SCENE = int(i['TYPE'][5])
							act = True
						else: act = False
					#DO ACTION
					else:
						if cld == 1: act = False
						else: act = True
						if self.pressed[4][0]: act = True
					if act:
						p['PAUSE'] = 1
						i['FOLLOW'] = None
						i['TALKING'] = True
						#NPC DIALOG
						if i['TYPE'] in [0,None] or isinstance(i['TYPE'],str):
							if self.dlg['FADE'] > 0:
								#DIALOG
								if i['WHO'] == None:
									self.dialog(dtb.DIALOGS['STNPC'][round(random.randint(0,len(dtb.DIALOGS['STNPC']) - 1))].copy(),i['RECT'])
								else:#elif i['WHO'] != 'REWARD':
									if isinstance(i['WHO'], int): self.dialog(dtb.DIALOGS['NPC_' + str(i['WHO'])][res.DLGSAV[i['WHO']]].copy(),i['RECT'])
									elif len(dtb.DIALOGS[i['WHO']]) > res.DLGSAV[i['WHO']]:
										self.dialog(dtb.DIALOGS[i['WHO']][res.DLGSAV[i['WHO']]].copy(),i['RECT'])
									else: self.dialog(dtb.DIALOGS['EMPTY CHEST'])
						#MARKET CASHIER
						elif i['TYPE'] == 2:
							#DRIVE THRU
							if i['WHO'].startswith('DRITHR'):
								if p['DRIVING'] != None:
									if self.dlg['FADE'] > 0: self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),i['RECT'])
								else:
									self.inv.type = 3
									self.inv.fade = 0
									self.lopt = 1
									self.opt = 0
									self.mnu = 0
							#NOTHING IN BASKET
							elif res.BASKET == []:
								if self.dlg['FADE'] > 0:
									self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),i['RECT'])
							#BUY ITEMS
							else:
								self.inv.type = 3
								self.inv.fade = 0
								self.lopt = 1
								self.opt = 0
								self.mnu = 0
						#BED
						elif i['TYPE'] == 6:
							p['RECT'].x = i['RECT'].x + 5
							p['RECT'].y = i['RECT'].y + 5
							p['SLEEP'] = not p['SLEEP']
							if p['SLEEP'] == False: p['PAUSE'] = 1
							else: p['PAUSE'] = 0
						#PHONE
						elif i['TYPE'] == 8:
							for m in ['credit_card','wallet']:
								mny = self.inv.find(None,m,'value')
							if mny != None and mny[1] > 0:
								res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1] - 1)
								self.dev = self.inv.dev('phone')
								self.wait()
								dtb.CALLHIST.insert(0,[dtb.CONTACTS[self.lopt][1],False])
								self.dialog(dtb.DIALOGS[dtb.CONTACTS[self.lopt][1]][0],i['RECT'])
							else:
								self.dialog([dtb.MENU[18]],i['RECT'])
						#BATTERY PLUG
						elif i['TYPE'] == 9:
							if self.inv.find(res.PARTY[res.FORMATION][0],'charger') != None:
								self.ch_sfx.play(res.SOUND['MENU_GO'])
								bt = self.inv.find(None,'phone')
								bt[1] = '3600'
								self.dialog(dtb.DIALOGS['PLUG'][1])
							else:
								self.dialog(dtb.DIALOGS['PLUG'][0])
						#REFUEL
						elif i['TYPE'] == 10 and p['DRIVING'] != None:
							while res.GAS < self.vehicles[p['DRIVING']]['CAPACITY']:
								res.GAS += 1
								self.run()
		else: i['TALKING'] = False

	def vehicle(self, i):
		rect = pygame.Rect(i['RECT'].x - 5,i['RECT'].y - 5,60,30)
		for p in self.player:
			if p['DRIVING'] == i['N']:
				i['RECT'].x = p['RECT'].x
				i['RECT'].y = p['RECT'].y
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'moto_' + str(i['INDEX']) + '_walkL.png'), (rect.x - self.cam.x + 10, rect.y + rect.height - self.cam.y - 30))
		#MOVEMENT
		if i['MOVE'] == 'street':
			try: t = self.tilrect[0][(math.floor(i['RECT'].y/self.map.tilewidth) * self.map.width) + math.floor(i['RECT'].x/self.map.tilewidth)]
			except: t = None
			if t != None and t[0]['TYPE'].startswith('STREET') and self.colide(i['RECT'],t[1]):
				if t[0]['TYPE'].endswith('1'):
					if i['DIRECTION'] == 1: i['DIRECTION'] = 7
					if i['DIRECTION'] == 3: i['DIRECTION'] = 5
					if i['DIRECTION'] == 5: i['DIRECTION'] = 3
					if i['DIRECTION'] == 7: i['DIRECTION'] = 1
				if t[0]['TYPE'].endswith('2'):
					if i['DIRECTION'] == 1: i['DIRECTION'] = 3
					if i['DIRECTION'] == 3: i['DIRECTION'] = 1
					if i['DIRECTION'] == 5: i['DIRECTION'] = 7
					if i['DIRECTION'] == 7: i['DIRECTION'] = 5
		if i['MOVE'] == 'nodeon':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] == 2: i['DIRECTION'] = n['TYPE']
		elif i['MOVE'] == 'nodeoff':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] == 3: i['DIRECTION'] = n['TYPE']
		elif i['MOVE'] == 'police':
			for n in self.nodes:
				if self.colide(rect,n['RECT']):
					if n['GOING'] in [2,3]:
						if n['TYPE'] in [1,5]:
							if self.player[0]['RECT'].x > i['RECT'].x: i['DIRECTION'] = 1
							if self.player[0]['RECT'].x < i['RECT'].x: i['DIRECTION'] = 5
						if n['TYPE'] in [3,7]:
							if self.player[0]['RECT'].y > i['RECT'].y: i['DIRECTION'] = 3
							if self.player[0]['RECT'].y < i['RECT'].y: i['DIRECTION'] = 7
		if i['MOVE'] != 'fixed':
			if i['DIRECTION'] == 1: i['RECT'].x += 4
			if i['DIRECTION'] == 2: i['RECT'].x += 4; i['RECT'].y += 4
			if i['DIRECTION'] == 3: i['RECT'].y += 4
			if i['DIRECTION'] == 4: i['RECT'].x -= 4; i['RECT'].y += 4
			if i['DIRECTION'] == 5: i['RECT'].x -= 4
			if i['DIRECTION'] == 6: i['RECT'].x -= 4; i['RECT'].y -= 4
			if i['DIRECTION'] == 7: i['RECT'].y -= 4
			if i['DIRECTION'] == 8: i['RECT'].x += 4; i['RECT'].y -= 4
		#SOUND
		snd = pygame.mixer.Sound(res.SFX_PATH + 'step_motor.wav')
		xx = (self.player[0]['RECT'].x - self.cam.x) - (i['RECT'].x - self.cam.x)
		yy = (self.player[0]['RECT'].y - self.cam.y) - (i['RECT'].y - self.cam.y)
		dir = (xx,yy)
		dst = math.hypot(*dir)
		if dst == 0.0: dir = (0, -1)
		else: dir = (dir[0]/dst,dir[1]/dst)
		'''if dst < 0: dst = -dst
		if dst == 0: dst = 1'''
		snd.set_volume(2/dst)
		snd.play()
		pygame.draw.line(self.display[0],(200,10,10),(self.player[0]['RECT'].x - self.cam.x,self.player[0]['RECT'].y - self.cam.y),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		self.display[0].blit(self.fnt['DEFAULT'].render(str(dst),True,(200,200,200)),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		#ACTION
		for p in self.player:
			if self.colide(p['RECT'], rect) and p['DRIVING'] == None:
				if self.battle == False:
					self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - int(rect.height/2)))
					self.hpctrl = dtb.HINTS['VEHICLE_USE']
				if self.pressed[4][0] and self.inv.type == 0 and self.phone == 0:
					trigger = True
					p['DRIVING'] = i['N']
					p['RECT'].x = rect.x
					p['RECT'].y = rect.y
					i['MOVE'] = 'fixed'
					'''self.displayzw = 1200
					self.displayzh = 800
					self.display = pygame.Surface((1200, 800))
					self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)'''

	def portal(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,30,30)
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height),3)
		if self.colide(self.player[0]['RECT'], rect) and self.winbar > 0: spr = '1'
		else: spr = '0'
		if res.MAP != 'rodoviary':
			if i['RECT'].width == 24: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_0' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
			if i['RECT'].width == 48: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_1' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		else: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		goto = False
		#ENTERING DOOR
		if self.colide(self.player[0]['RECT'], rect) and self.winbar == 0 and self.portalgo == {}:
			if i['OPENING'] == 'key':
				fnd = self.inv.find(res.PARTY[res.FORMATION][0],'key_bedroom')
				if fnd != None and fnd[1] == i['CLOSURE']: goto = True
				else: goto = False
			elif i['OPENING'] != None:
				if res.TIME[0] > i['OPENING'][0] and res.TIME[0] < i['CLOSURE'][0]: goto = True
				elif res.TIME[0] == i['OPENING'][0]:
					if res.TIME[1] > i['OPENING'][1]: goto = True
				elif res.TIME[0] == i['CLOSURE'][0]:
					if res.TIME[1] < i['CLOSURE'][1]: goto = True
			elif i['MAP'] == None:
				if self.player[0]['SPEED'] == 0: goto = True
				else: goto = False
			else: goto = True

			#if i['RECT'].width == 24 and self.driving > 0: goto = False
			#elif i['RECT'].width == 48: goto = False
		#TELEPORT
		if goto:
			for p in self.player:
				p['PAUSE'] = 1
				p['SPEED'] = 0
			if i['TYPE'] > 0:
				self.ch_ton.play(res.SOUND['DOOR_OPEN'])
			if i['MUSIC'] not in ['inside','outside',None]:
				self.ch_msc.fadeout(1000)
				spd = 5
			else: spd = 10
			#BATHROOM
			if i['MAP'] == 'bathroom':
				self.transiction(True, int(self.displayzh/2))
				for i in range(30): self.run()
				self.ch_ton.play(res.SOUND['TREASURE_GET'])
				for i in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[i]['HEALTH'] in [3,5]:
						res.CHARACTERS[i]['HEALTH'] = 0
				for i in range(60): self.run()
				self.ch_ton.play(res.SOUND['DOOR_CLOSE'])
				for p in self.player[0]:
					p['RECT'].x = i['RECT'].x
					p['RECT'].y = i['RECT'].y + 20
					p['PAUSE'] = 0
				self.transiction(False, 0)
			#UPDATE POSITION
			else:
				#IN
				self.portalgo = [{'MATCH': None, 'RECT' : pygame.Rect(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y,i['RECT'].width,i['RECT'].height)},{}]
				self.portalgo[1] = self.player[0].copy()
				self.portalgo[1]['RECT'].x -= self.cam.x
				self.portalgo[1]['RECT'].y -= self.cam.y
				if i['MAP'] != None:
					self.transiction(True, int(self.displayzh/2), spd, "side")
					self.loadmap(i['MAP'])
				#OUT
				self.portalgo[0]['MATCH'] = i['MATCH']
				while self.portalgo[0]['MATCH'] != None: self.run()
				if i['TYPE'] > 0: self.ch_ton.play(res.SOUND['DOOR_CLOSE'])
				if i['MUSIC'] == 'outside': self.ch_msc.set_volume(1.0)
				elif i['MUSIC'] == 'inside': self.ch_msc.set_volume(0.2)
				elif i['MUSIC'] != None: self.ch_msc.play(res.SOUND[i['MUSIC'].upper()],-1)
				#CITYNAME
				if i['MAP'] != None:
					if self.cityname == '':
						self.transiction(False, 0, spd, "side")
					else:
						self.transiction(False, 50, 5)
						for r in range(100): self.run()
						self.transiction(False, 0, 5)
						self.cityname = ''
				self.portalgo = {}
				for p in self.player:
					#TO ANOTHER ROOM
					if i['MAP'] != None:
						p['RECT'].x = i['PX']
						p['RECT'].y = i['PY']
					#TO SAME ROOM
					else:
						lst = []
						for pr in self.objects:
							if pr[0] == 4 and pr[1]['N'] != i['N'] and pr[1]['MAP'] == None and pr[1]['PX'] == i['PX']:
								lst.append([pr[1]['RECT'].x,pr[1]['RECT'].y])
						if lst != []:
							prb = random.randint(0,len(lst) - 1)
							p['RECT'].x = lst[prb][0]
							p['RECT'].y = lst[prb][1]
					p['PAUSE'] = 0
					
	def pathfinding(self, rct, tgt, map):
		pass
		
	def soundplay(self, sound, value=1):
		for i in self.channels:
			if value == 0 and i[1] == sound:
				i[0].stop()
				i[1] = None
				break
			if i[0].get_busy() == False:
				i[0].play(res.SOUND[sound],value)
				i[1] = sound
				break
		return res.SOUND[sound]
	
	def colide(self, i1, i2):
		cld = False
		if isinstance(i2, list):
			ind = 0
			for i in i2[2]:
				if self.facing(i1,i[1]) == 2:
					cld = pygame.Rect.colliderect(i1['RECT'],i[1])
					if cld and i1['JUMP'] == 0:
						#HOLD OBJECT
						if i[0] == 'HOLD':
							self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (i[1].x - self.cam.x + int(i[1].width/2) - 5, i[1].y - self.cam.y - i[1].height))
							if self.pressed[4][0] and self.player[0]['HOLD'] == None:
								self.player[0]['HOLD'] = ind
							cld = False
				ind += 1
			#JUMP
			if cld == False:
				for i in i2[3]:
					if self.facing(i1,i[1]) == 2:
						cld = pygame.Rect.colliderect(i1['RECT'],i[1])
						if cld and i1['JUMP'] == 0: break
			#TURN ON OFF AREAS
			if cld == False and i1['PLAYING']:
				for i in i2[4]:
					if self.facing(i1,i[1]) == 2:
						if pygame.Rect.colliderect(i1['RECT'],i[1]) and i1['JUMP'] == 0:
							if i[0].endswith('ON') and self.tilhide == False: self.tilhide = True
							if i[0].endswith('OFF') and self.tilhide: self.tilhide = False
							break
		else:
			cld = pygame.Rect.colliderect(i1,i2)

		return cld

	def facing(self, i1, i2):
		if isinstance(i2, dict) == False: i2 = {'RECT': i2, 'DIRECTION': self.player[0]['DIRECTION']}
		if i1['DIRECTION'] == i2['DIRECTION'] or i1['DIRECTION'] == i2['DIRECTION'] + 1 or i1['DIRECTION'] == i2['DIRECTION'] - 1:
			if i1['DIRECTION'] == 1:
				if i1['RECT'].x < i2['RECT'].x: return 2
				elif i1['RECT'].x > i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 2:
				if i1['RECT'].x < i2['RECT'].y: return 2
				elif i1['RECT'].x > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 3:
				if i1['RECT'].y < i2['RECT'].y: return 2
				elif i1['RECT'].y > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 4:
				if i1['RECT'].y < i2['RECT'].y: return 2
				elif i1['RECT'].y > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 5:
				if i1['RECT'].x > i2['RECT'].x: return 2
				elif i1['RECT'].x < i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 6:
				if i1['RECT'].x > i2['RECT'].y: return 2
				elif i1['RECT'].x < i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 7:
				if i1['RECT'].y > i2['RECT'].y: return 2
				elif i1['RECT'].y < i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 8:
				if i1['RECT'].y > i2['RECT'].y: return 2
				elif i1['RECT'].y < i2['RECT'].y: return 3
				else: return 1
		else: return 1
		
	def get_pressed(self,event):
		pressed = []
		for i in range(len(res.CONTROLS[0])):
			pressed.append([])
			for p in range(4):
				pressed[i].append(0)
		#KEYBOARD/MOUSE
		if res.MOUSE < 2:
			ky = pygame.key.get_pressed()
			for p in range(4):
				for i in range(len(res.CONTROLS[p])):
					pressed[i][p] = ky[res.CONTROLS[p][i]]
		#JOYSTICK
		pygame.joystick.init()
		connect = pygame.joystick.get_count()
		if connect > 1:
			res.MOUSE = 3
			joystick = pygame.joystick.Joystick(0)
			joystick.init()
			#for i in range(6 + joystick.get_numbuttons()): pressed.append([0])
			for b in range(4):
				if pressed[res.JOYSTICK[b]][0] == 0:
					pressed[res.JOYSTICK[b]][0] = int(joystick.get_axis(b))
			for b in range(joystick.get_numbuttons()):
				if res.JOYSTICK[b + 4] == None and pressed[b + 4][0] == 0: pressed[b + 4][0] = 0
				elif pressed[res.JOYSTICK[b + 4]][0] == 0: pressed[res.JOYSTICK[b + 4]][0] = joystick.get_button(b)
			for b in range(2):
				if res.JOYSTICK[b + 4 + joystick.get_numbuttons()] == None: pressed[b + 4 + joystick.get_numbuttons()][0] = 0
				elif pressed[res.JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] == 0:
					pressed[res.JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] = int(joystick.get_axis(b + 4))
			for i in pressed:
				while len(i) < 3: i.append(0)
		#TOUCH
		mp = pygame.mouse.get_pos()
		self.click = pygame.Rect(mp[0],mp[1],2,2)
		if len(self.buttons) > 0:
			res.MOUSE = 2
			if event != None:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if res.VIBRATE: plyer.vibrator.vibrate(0.1)
					chk = 1
				else: chk = 0
			else: chk = pygame.mouse.get_pressed()[0]
			for i in range(len(self.buttons)):
				if self.colide(self.click,self.buttons[i]):
					if chk: pressed[i] = [1,0,0,0]
					elif pressed[i][0] == 0: pressed[i] = [0,0,0,0]
				elif pressed[i][0] == 0: pressed[i] = [0,0,0,0]
		return pressed

	def events(self):
		for event in pygame.event.get():
			self.pressed = self.get_pressed(event)
			#EXIT
			if event.type == pygame.QUIT:
				if self.confirmation() == 1:
					pygame.quit()
					sys.exit()
					exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.displayzw = int(self.windoww/res.GSCALE)
				self.displayzh = int(self.windowh/res.GSCALE)
				self.inv = GUI.Inventory((self.displayzw,self.displayzh))
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
				self.display = [pygame.Surface((self.displayzw, self.displayzh)),pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
				self.buttons = [pygame.Rect(20,self.windowh - 264,240,80),pygame.Rect(20,self.windowh - 100,240,80),pygame.Rect(20,self.windowh - 264,80,240),
				pygame.Rect(184,self.windowh - 264,80,240),pygame.Rect(self.windoww - 190,self.windowh - 100,80,80),pygame.Rect(self.windoww - 100,self.windowh - 100,80,80),
				pygame.Rect(self.windoww - 190,40,80,80),pygame.Rect(self.windoww - 100,40,80,80),pygame.Rect(20,40,80,80)]
			#DEBUG
			if self.pressed[8][0] and res.DEBUG: self.dialog(['',(22,'debug')])
			#CLICK
			if res.MOUSE == 1:
				for i in range(2):
					if res.CLICK[i] == 'move' and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[i]:
						rct = pygame.Rect(int((math.floor(self.click.x/self.map.tilewidth) * self.map.tilewidth)/res.GSCALE),
						int((math.floor(self.click.y/self.map.tileheight) * self.map.tileheight)/res.GSCALE),10,10)
						img = []
						for a in range(2): img.append(pygame.image.load(res.SPRITES_PATH + 'click_' + str(a) + '.png'))
						self.objects.append(['click',{'RECT': rct,'IMAGE': img,'GIF': 0.0,'DESTROY': False},rct.y])
						self.player[0]['FOLLOW'] = rct
						self.player[0]['FOLLEND'] = 3
			#BATTLE OPTIONS
			if self.battle and self.phone == 0 and self.dlg['FADE'] > 0 and self.turn >= 0:
				if self.turn == len(res.PARTY[res.FORMATION]):
					self.fight()
					tp = 0
				else:
					if self.turn == 0: tp = 0
					elif self.turn >= len(self.player): tp = 0
					elif self.player[self.fig[self.turn]['N']]['PLAYING']: tp = self.turn
					else: tp = 0
				#CHOOSING WEAPON
				if self.mnu == 1:
					if self.pressed[2][tp]: self.equip[self.fig[self.turn]['N']] -=1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[3][tp]: self.equip[self.fig[self.turn]['N']] +=1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
				
					if self.equip[self.turn] < 0: self.equip[self.fig[self.turn]['N']] = 7
					if self.equip[self.turn] > 7: self.equip[self.fig[self.turn]['N']] = 0

					if self.pressed[4][tp]:
						#WEAPONS
						if self.equip[self.turn] < 4:
							if res.BTYPE == 1: sht = True
							elif self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] == 100: sht = True
							else: sht = False
							if sht:
								if res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('melee'):
									self.ch_sfx.play(res.SOUND['MELEE'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('tool'):
									self.ch_sfx.play(res.SOUND['MELEE'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('gun') and self.barpp[self.turn][self.equip[self.fig[self.turn]['N']]] > 0:
									self.ch_sfx.play(res.SOUND['GUN_TRIGGER'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('grenade'):
									self.ch_sfx.play(res.SOUND['MELEE'])
									res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][1] = '300'
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0] == '_':
									self.mnu = 2
								else: self.ch_sfx.play(res.SOUND['ERROR'])
							else: self.ch_sfx.play(res.SOUND['ERROR'])
						#TACTICAL
						elif self.equip[self.fig[self.turn]['N']] == 4:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.mnu = 2
						#DIALOG
						elif self.equip[self.fig[self.turn]['N']] == 5:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							if self.dlg['TEXT'] == []: self.dialog(dtb.DIALOGS['BATTLEDIALOG'])
							self.mnu = 1
							self.turn += 1
						#GUARD
						elif self.equip[self.fig[self.turn]['N']] == 6:
							self.ch_ton.play(res.SOUND['GUARD'])
							self.fig[self.turn]['RESISTANCE'] += 3
							self.turn += 1
							if self.turn == len(self.fig): self.fight()
						#RUN AWAY
						elif self.equip[self.fig[self.turn]['N']] == 7:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.fight()
							if self.battle:
								self.turn = len(res.PARTY[res.FORMATION])
								self.fight()
				#USING WEAPON
				elif self.mnu == 2:
					if self.equip[self.fig[self.turn]['N']] == 4:
						if self.pressed[2][tp]: self.opt -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][tp]: self.opt += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					sht = False
					if self.pressed[4][tp]: sht = True
					elif res.MOUSE > 0:
						self.aim.x = int(pygame.mouse.get_pos()[0]/res.GSCALE)
						self.aim.y = int(pygame.mouse.get_pos()[1]/res.GSCALE)
						if event.type == pygame.MOUSEBUTTONUP:
							if self.colide(self.aim,pygame.Rect(0,self.winbar,self.displayzw,self.displayzh - (self.winbar * 2))):
								sht = True
					if sht:
						#SHOT OR HIT
						if self.equip[self.fig[self.turn]['N']] < 4:
							self.fight()
							if res.BTYPE == 1: trn = True
							elif self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] == 0: trn = True
							else: trn = False
							if trn:
								self.turn += 1
								self.mnu = 1
								if self.turn == len(res.PARTY[res.FORMATION]):
									if res.BTYPE == 1: self.fight()
									else: self.turn = 0
							else: self.mnu = 2
						#TACTICAL ATTACK
						elif self.equip[self.fig[self.turn]['N']] == 4:
							ttl = self.opt
							for i in self.fig:
								self.equip[self.fig[self.turn]['N']] = res.TACTICAL[ttl][self.fig[self.turn]['N']]
								if self.equip[self.fig[self.turn]['N']] != 0:
									if self.equip[self.fig[self.turn]['N']] + 1 < 5:
										self.equip[self.fig[self.turn]['N']] -= 1
										self.ch_sfx.play(res.SOUND['GUN_TRIGGER'])
										self.mnu = 2
										self.wait()
									if self.equip[self.fig[self.turn]['N']] != 6: self.fight()
									else:
										self.fig[self.fig[self.turn]['N']]['RESISTANCE'] += 3
										self.ch_sfx.play(res.SOUND['GUARD'])
								self.turn += 1
							for i in self.equip: i = 4
					#CANCEL MOVE
					if self.pressed[5][tp]:
						self.ch_sfx.play(res.SOUND['MISS'])
						self.mnu = 1
					if self.opt < 0: self.opt = len(res.TACTICAL) - 1
					if self.opt > len(res.TACTICAL) - 1: self.opt = 0
			#PAUSE MENU
			mnuchk = [None,None,None,None]
			p = 0
			for i in res.ACTION:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if i == 'pause': mnuchk[0] = p
					if i == 'chat': mnuchk[1] = p
					if i == 'inventory': mnuchk[2] = p
					if i == 'shortcut': mnuchk[3] = p
				p += 1
			if mnuchk[0] and self.pressed[mnuchk[0]][0]:
				if self.title.mnu == 10:
					for p in self.player: p['PAUSE'] = 0
					self.title.mnu = 9
				elif self.title.mnu == 9:
					for p in self.player: p['PAUSE'] = 2
					self.title.mnu = 10
					self.winbar = 1
			if self.title.mnu == 10: self.title.events()
			#CHAT MENU
			if mnuchk[1] and self.pressed[mnuchk[1]][0]:
				self.dialog([(3,'chat'),(22,'chat')])
				if self.dlg['FADE'] > 0: pass
			#INVENTORY OPTIONS
			if mnuchk[2] and self.pressed[mnuchk[2]][0] and self.phone == 0 and self.inv.itmov == '':
				#OPEN AND CLOSE
				if self.inv.type > 0:
					self.inv.type = 0
					self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
					if self.inv.type == 2 and self.dlg['FADE'] > 0:
						self.dialog(dtb.DIALOGS['DEPOSIT'][1])
					for p in self.player: p['PAUSE'] = 0
					if self.battle: self.mnu = 1
				elif self.inv.type == 0 and self.inv.hld < 20:
					self.inv.type = 1
					self.ch_sfx.play(res.SOUND['INVENTORY_OPEN'])
					for p in self.player: p['PAUSE'] = 1
					self.inv.fade = 0
					self.inv.opt = [0,0,0,0]
			do = 0
			if self.inv.hld > 20: do = 1
			if self.inv.type > 0: do = 2
			if do:
				if event.type == pygame.KEYDOWN: self.inv.rqst = True
				if event.type == pygame.MOUSEBUTTONDOWN: self.inv.rqst = True
				#HOLDING ITEM
				if self.inv.itmov != '':
					#ACCESORIES SELECT
					if self.inv.itmov[0] == 0:
						if self.pressed[2][0]:
							if self.inv.opt[3] > 1: self.inv.opt[3] -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][0]:
							if self.inv.opt[3] < len(self.inv.itmov): self.inv.opt[3] += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					#MOVING ITEM
					else:
						if self.pressed[2][0]: self.inv.opt[0] -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][0]: self.inv.opt[0] += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if do > 1:
							if self.pressed[0][0]: self.inv.opt[1] -= 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
							if self.pressed[1][0]: self.inv.opt[1] += 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
				#SELECT ITEM
				else:
					if self.pressed[2][0]: self.inv.opt[0] -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[3][0]: self.inv.opt[0] += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if do > 1:
						if self.pressed[0][0]: self.inv.opt[1] -= 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
						if self.pressed[1][0]: self.inv.opt[1] += 1; self.ch_sfx.play(res.SOUND['MENU_VER'])	
				if self.inv.type == 1:
					if self.inv.opt[0] < 0: self.inv.opt[0] = 4; self.inv.opt[2] -= 1
					if self.inv.opt[0] > 4: self.inv.opt[0] = 0; self.inv.opt[2] += 1
					if self.inv.opt[1] < 0: self.inv.opt[1] = 4
					if self.inv.opt[1] > 4: self.inv.opt[1] = 0
				else:
					if self.inv.opt[0] < 0: self.inv.opt[0] = 9
					if self.inv.opt[0] > 9: self.inv.opt[0] = 0
					if self.inv.opt[0] < 5:
						if self.inv.opt[1] < 0: self.inv.opt[1] = 4; self.inv.opt[2] -= 1
						if self.inv.opt[1] > 4: self.inv.opt[1] = 0; self.inv.opt[2] += 1
					else:
						if self.inv.opt[1] < 0: self.inv.opt[1] = math.ceil(len(res.STORAGE)/5) - 1
						if self.inv.opt[1] > math.ceil(len(res.STORAGE)/5) - 1: self.inv.opt[1] = 0
				if self.inv.opt[2] < 0: self.inv.opt[2] = len(res.PARTY[res.FORMATION]) - 1
				if self.inv.opt[2] > len(res.PARTY[res.FORMATION]) - 1: self.inv.opt[2] = 0
				#MOUSE CLICK
				abl = False
				mr = pygame.Rect(self.click.x - self.inv.pos[0],self.click.y - self.inv.pos[1],2,2)
				if event.type == pygame.MOUSEBUTTONDOWN:
					for u in range(len(self.inv.optrects)):
						for j in range(len(self.inv.optrects[u])):
							for i in range(len(self.inv.optrects[u][j])):
								optrct = self.inv.optrects[u][j][i][self.inv.type]
								if self.colide(mr,pygame.Rect(optrct.x - self.inv.scroll,optrct.y,optrct.width,optrct.height)):
									self.inv.opt[0] = i
									self.inv.opt[1] = j
									self.inv.opt[2] = u
									abl = True
				ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.inv.opt[2]]]
				if self.inv.type == 2 and self.inv.opt[0] > 4: it = res.STORAGE[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
				elif self.inv.type == 3 and self.inv.opt[0] > 4: it = res.BASKET[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
				elif self.inv.type == 4 and self.inv.opt[0] > 4: it = res.WASH[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
				elif self.inv.type == 6:
					if self.inv.opt[0] > 4: it = res.BASKET[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
					else: it = res.PRODUCTS[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
				elif self.inv.type == 7 and self.inv.opt[0] > 4: it = res.PRODUCTS[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5]
				else: it = res.INVENTORY[res.PARTY[res.FORMATION][self.inv.opt[2]]][self.inv.opt[1]][self.inv.opt[0]]
				if self.pressed[4][0]: abl = True
				if abl and self.inv.opt[0] < 4:
					#USING ITEMS
					if self.inv.itmov == '' or self.inv.itmov[0] == 0:
						prb = random.randint(0,100)
						#RANDOM BATTLE
						if it[0] in dtb.ITEMENEMIES and prb > 100 - dtb.ITEMENEMIES[it[0]][1]:
							self.dialog([(13,[dtb.ITEMENEMIES[it[0]][0]])])
						#FOOD
						elif it[0].startswith('food_'):
							#if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] not in [4,10]:
							self.actqueue.append({'RECT': self.player[0]['RECT'],'SPEED': 5,'ACT': 0,'BAR': 0,
							'CHARACTER': res.PARTY[res.FORMATION][self.inv.opt[2]],'ITEM': (self.inv.opt[1],self.inv.opt[0])})
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
									self.ch_ton.play(res.SOUND['HEAL'])
									hl = dtb.ITEMS[drk][5]
									if it in res.CHARACTERS[self.inv.opt[2]]['FAVFOOD']: hl += int(hl/2)
									ch['HP'] += hl
									ch['THIRST'] += dtb.ITEMS[drk][6]
									if it[0].startswith('drink') and res.DISITEMS[it[0]] == 0:
										res.DISITEMS[it[0]] = 1
									if ch['HP'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
										ch['HP'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
								else:
									self.ch_ton.play(res.SOUND['INCONSCIOUS'])
									ch['HEALTH'] = 10
								if amt > 0: amt -= 1
								if amt == 0:
									if it[0].startswith('bottle'):
										it = it[0:2]
									else:
										if dtb.ITEMS[it[0]][8] != None: it = ['trash_' + dtb.ITEMS[drk][8],'0000']
										else: it = ['_','0000']
									res.INVENTORY[res.PARTY[res.FORMATION][self.inv.opt[2]]][self.inv.opt[1]][self.inv.opt[0]] = it
								self.notification.append({'TEXT': 'hp_' + str(hl), 'COLOR': (255, 0, 0), 'HALIGN': 'left','X': 0})
							else: self.ch_ton.play(res.SOUND['ERROR'])
						#TOOLS
						elif it[0].startswith('tool_') and self.battle == False:
							try: t = self.tilrect[0][(math.floor((self.player[self.inv.opt[2]]['RECT'].y + 15)/self.map.tilewidth) * self.map.width) + math.floor((self.player[p]['RECT'].x + 15)/self.map.tilewidth)]
							except: t = None
							if t != None and len(dtb.ITEMS[it[0]]) > 5:
								if t[0] == dtb.ITEMS[it[0]][5]['UNLOCK']:
									self.ch_sfx.play(res.SOUND['MENU_GO'])
						#GRENADES
						elif it[0].startswith('grenade') and self.battle and it in res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][1:]:
							self.ch_sfx.play(res.SOUND['MELEE'])
							it = ['_','0000']
							self.inv.opt[2] = 1
							self.inv.type = 0
						#REPELLENTS
						elif it[0].startswith('repellent'):
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							ch['HEALTH'] = 2
							self.waitlst.append(['repellent' + str(res.PARTY[res.FORMATION][self.inv.opt[2]]),self.waitime + dtb.ITEMS[it[0]][5]])
							it = ['_','0000']
						#PILLS
						elif it[0].startswith('pill_'):
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							if it[0].endswith('strenght'): ch['BONUS'][0] += 1
							if it[0].endswith('resistance'): ch['BONUS'][1] += 1
							if it[0].endswith('agility'): ch['BONUS'][2] += 1
							if it[0].endswith('knowledge'): ch['BONUS'][3] += 1
							if it[0].endswith('charisma'): ch['BONUS'][4] += 1
							it = ['_','0000']
						#ACCESORIES ACCESS
						elif it[0].startswith('phone') or it[0] == 'wallet' or it[0].startswith('bag') or it[0].startswith('locksmith'):
							self.ch_ton.play(res.SOUND['MENU_GO'])
							self.inv.itmov = [0]
							for a in range(len(it[2::2])):
								self.inv.itmov.append([it[(a + 1) * 2],it[((a + 1) * 2) + 1]])
							self.inv.opt[3] = 1
						#TENTS
						elif it[0].startswith('tent_'):
							self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
							self.build = it[0]
							self.player[0]['PAUSE'] = 0
							self.inv.type = 0
							if it[1] != 'infinite':
								if int(it[1]) > 0: it = [it[0],str(int(i[1]) - 1)]
								else: it = ['_','0000']
						#NEWSPAPERS
						elif it[0].startswith('newspaper'):
							self.ch_sfx.play(res.SOUND['PAGE_FLIP'])
							self.player[0]['PAUSE'] = 0
							self.read = GUI.Newspaper()
						#IDENTIFICATION
						elif it[0].startswith('id'):
							self.ch_sfx.play(res.SOUND['PAGE_FLIP'])
							self.player[0]['PAUSE'] = 0
							self.read = GUI.ID(dtb.ITEMS[it[0]][5])
						#PAINT TILES
						elif it[0].startswith('til_'):
							self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
							self.paint = dtb.ITEMS[it[0]][5]
							self.player[0]['PAUSE'] = 0
							self.inv.type = 0
							if it[1] != 'infinite':
								if int(it[1]) > 0: it = [it[0],str(int(i[1]) - 1)]
								else: it = ['_','0000']
						#GUI TOOLS
						elif it[0].startswith('guit_'):
							if it[0] == 'guit_save': self.ch_ton.play(res.SOUND['FILE_SAVE']); self.savemap()
							elif it[0] == 'guit_load': self.ch_ton.play(res.SOUND['FILE_LOAD']); self.loadmap()
							elif it[0] == 'guit_undo' and self.ihist > 0: self.ch_ton.play(res.SOUND['MENU_BACK']); self.ihist -= 1
							elif it[0] == 'guit_redo' and self.ihist < len(self.shist): self.ch_ton.play(res.SOUND['MENU_GO']); self.ihist += 1
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
								self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
								self.guit = dtb.ITEMS[it[0]][5]
								self.player[0]['PAUSE'] = 0
								self.inv.type = 0
						#ERROR
						else: self.ch_ton.play(res.SOUND['ERROR'])
						if self.battle:
							self.turn += 1
							self.inv.opt[2] = 1
							self.inv.type = 0
					#ACCESORIES EXIT
					elif self.inv.itmov[0] == 0:
						if self.inv.opt[3] == len(self.inv.itmov):
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.inv.itmov = ''
							self.inv.opt[3] = 0
						else: self.ch_ton.play(res.SOUND['ERROR'])
					#CRAFTING
					elif it[0] != '_':
						craft = False
						if it[0].startswith('bag') and dtb.ITEMS[self.inv.itmov[0]][3] == 1: craft = True
						if it[0].startswith('undr') and dtb.ITEMS[self.inv.itmov[0]][3] == 1: craft = True
						if self.inv.itmov[0].startswith('clth') and it[0].startswith('clth'): craft = True
						if self.inv.itmov[0].startswith('key') and it[0].startswith('locksmith'): craft = True
						if self.inv.itmov[0].startswith('id_card') and it[0].startswith('wallet'): craft = True
						if self.inv.itmov[0].startswith('credit_card') and it[0].startswith('wallet'): craft = True
						if self.inv.itmov[0].startswith('condiment') and it[0].startswith('food'): craft = True
						if self.inv.itmov[0].startswith('drink') and it[0].startswith('bottle'): craft = True
						if self.inv.itmov[0].startswith('acc') and it[0].startswith('gun'): craft = True
						if self.inv.itmov[0] == 'tool_syringe' and it[0].startswith('drug'): craft = True
						#LIGHTER
						if self.inv.itmov[0].startswith('tool_lighter') and int(self.inv.itmov[1]) != 0:
							if it[0] == 'grenade_molotov_cocktail':
								self.inv.itmov[1] = str(int(self.inv.itmov[1]) - 1)
								it[1] = '300'
							if it[0] == 'cigar':
								self.inv.itmov[1] = str(int(self.inv.itmov[1]) - 1)
								it[1] = '500'
						#RECHARGE WEAPONS
						if self.inv.itmov[0].startswith('ammo') and it.startswith('gun'):
							if dtb.ITEMS[self.inv.itmov[0]][5] == dtb.ITEMS[it[0]][5]['GAUGE']:
								craft = True
								self.ch_ton.play(res.SOUND['GUN_RECHARGE'])
								it[3] = dtb.ITEMS[it[0]][5]['CAPACITY']
								if self.inv.opt[1] == 4 and self.inv.opt[0]> 0:
									if int(it[3]) > 0:
										plus = int(98/(dtb.ITEMS[it[0]][5]['CAPACITY']/int(it[3])))
									else: plus = 0
									self.barpp[self.inv.opt[2]][self.inv.opt[0] - 1] = plus
							else: craft = False
						#ADDING ACCESORIES
						if craft:
							for a in range(len(it[::2])):
								if it[a] == '_':
									self.ch_ton.play(res.SOUND['CRAFT'])
									it[(a + 1) * 2] = self.inv.itmov[0]
									it[((a + 1) * 2) + 1] = self.inv.itmov[1]
									self.inv.itmov = ''
									break
								else: self.ch_ton.play(res.SOUND['ERROR']); self.shake = 5
						#MERGE ITEMS
						merge = False
						for a in dtb.CRAFTING:
							if it[0] in a[0:2] and self.inv.itmov[0] in a[0:2]:
								self.ch_ton.play(res.SOUND['CRAFT'])
								it = [a[2],'9999']
								self.inv.itmov = ''
								merge = True
						if merge == False and craft == False: self.ch_ton.play(res.SOUND['ERROR']); self.shake = 5
						if self.battle:
							self.turn += 1
							self.inv.opt[2] = 1
							self.inv.type = 0
					else: self.ch_ton.play(res.SOUND['ERROR'])
				#MOVE ITEMS
				if self.pressed[5][0] and do > 1:
					#TRASH
					if self.inv.type == 5:
						if it[0] != '_': #and self.confirmation() == 1:
							it = ['_','0000']
					elif self.inv.itmov != '':
						#TAKE SUB-ITEM
						if self.inv.itmov[0] == 0:
							if self.inv.opt[3] < len(self.inv.itmov) and self.inv.itmov[self.inv.opt[3]][0] != '_':
								self.ch_sfx.play(res.SOUND['MENU_GO'])
								self.inv.itmov = [self.inv.itmov[self.inv.opt[3]][0],self.inv.itmov[self.inv.opt[3]][1]]
								for i in range(2): del it[2 * self.inv.opt[3]]
							else: self.ch_sfx.play(res.SOUND['ERROR']); self.inv.shake = 5
						#PLACE ITEM
						elif it[0] == '_' and self.inv.space(res.PARTY[res.FORMATION][self.inv.opt[2]],self.inv.opt[3],self.inv.opt[0],self.inv.opt[1],self.inv.type):
							#CLOTHING
							if self.inv.itmov[0].startswith('clth'):
								self.player[self.inv.opt[2]]['COSTUME'] = self.inv.find(res.PARTY[res.FORMATION][self.inv.opt[2]],['clth'],'position')
							if self.inv.itmov[0].startswith('head'):
								self.player[self.inv.opt[2]]['ACCESORIES'] = self.inv.find(res.PARTY[res.FORMATION][self.inv.opt[2]],['head'],'position')
								if self.inv.itmov[0] == 'head_hairclip':
									if self.inv.opt[0] == 0: hr = 2
									else: hr = 8
									res.CHARACTERS[res.PARTY[res.FORMATION][self.inv.opt[2]]]['HAIR'][1] = hr
									self.player[self.inv.opt[2]]['HAIR'][1] = hr
							#AMMO BAR
							if self.inv.itmov[0].startswith('gun'):
								self.barpp = []
								x = 0
								for i in res.PARTY[res.FORMATION]:
									self.barpp.append([])
									for j in res.INVENTORY[i][4][1:]:
										if j[0] != '_' and j[0].startswith('melee') == False:
											if int(j[1]) > 0: b = int(100/(dtb.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
											else: b = 0
											self.barpp[x].append(b)
										else:
											self.barpp[x].append(0)
									x += 1
							if self.inv.type == 2:
								chk = True
								for j in res.STORAGE:
									if j[0] == '_': chk = False
								if chk:
									for i in range(5):
										res.STORAGE.append(['_','0000'])
							self.ch_sfx.play(res.SOUND['EQUIP'])
							if self.inv.type == 4:
								if res.TIME[0] >= 10: hh = str(res.TIME[0])
								else: hh = '0' + str(res.TIME[0])
								if res.TIME[1] >= 10: mm = str(res.TIME[1])
								else: mm = '0' + str(res.TIME[1])
								if (self.inv.opt[0] + (self.inv.opt[1] * 5) - 5) > len(res.WASH):
									res.WASH.append([self.inv.itmov[0],'0000',hh + mm])
								else: it = [self.inv.itmov[0],'0000',hh + mm]
							else: it = self.inv.itmov.copy()
							self.inv.itmov = ''
							if self.battle:
								self.turn += 1
								self.inv.opt[2] = 1
								self.inv.type = 0
						#SWITCH ITEMS
						elif self.inv.space(res.PARTY[res.FORMATION][self.inv.opt[2]],self.inv.opt[3],self.inv.opt[0],self.inv.opt[1],self.inv.type):
							self.ch_sfx.play(res.SOUND['EQUIP'])
							trd = it.copy()
							it = self.inv.itmov
							if self.inv.itmov[0].startswith('clth'):
								self.player[self.inv.opt[2]]['COSTUME'] = dtb.ITEMS[self.inv.itmov[0]][5]
							self.inv.itmov = trd
						#ERROR
						else: self.ch_sfx.play(res.SOUND['ERROR']); self.inv.shake = 5
					#TAKE ITEM
					elif it[0] != '_':
						if self.inv.opt[0] > 4:
							#BUY AND SELL
							if self.inv.type in [6,7]:
								mny = self.inv.find(None,'wallet','value')
								if mny != None and mny[1] >= dtb.ITEMS[it[0]][2]:
									if self.inv.space(res.PARTY[res.FORMATION][0]) == False:
										self.dialog(dtb.DIALOGS['MERCATOR'][2])
									elif self.confirmation() == 1:
										self.inv.add(res.PARTY[res.FORMATION][0],it[0])
										self.ch_sfx.play(res.SOUND['BUY'])
										mny[1] -= int(dtb.ITEMS[it[0]][2] * it[0])
								else:
									self.ch_sfx.play(res.SOUND['ERROR'])
									self.dialog(dtb.DIALOGS['MERCATOR'][1])
							#WASH
							elif self.inv.type == 4:
								if res.TIME[0] >= int(it[2][0:2]):
									if res.TIME[1] >= int(it[2][2:4]): prp = '0100'
									else: prp = '0000'
								else: prp = '0000'
								self.inv.itmov = [it[0],prp]
								del it
						else:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.inv.itmov = it.copy()
							it = ['_','0000']
					else: self.ch_ton.play(res.SOUND['ERROR'])
				#DEVICES SHORTCUT
				if self.pressed[7][0]:
					self.ch_sfx.play(res.SOUND['MENU_GO'])
					res.SHORTCUT = [res.PARTY[res.FORMATION][self.inv.opt[2]],self.inv.opt[1],self.inv.opt[0]]
					dv = self.inv.dev()
					self.dev = dv[0]
					if self.dev == 'radio': self.dev = self.rad
					if self.dev != None: self.dev.battery = dv[1]
				if self.inv.type == 2 and self.inv.opt[0] > 4: res.STORAGE[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5] = it
				elif self.inv.type == 3 and self.inv.opt[0] > 4: res.BASKET[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5] = it
				elif self.inv.type == 4 and self.inv.opt[0] > 4: res.WASH[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5] = it
				elif self.inv.type == 6:
					if self.inv.opt[0] > 4: res.BASKET[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5] = it
					else: res.PRODUCTS[self.inv.opt[0] + (self.inv.opt[1] * 5) - 5] = it
				elif self.inv.type == 7 and self.inv.opt[0] > 4: res.PRODUCTS[self.opt + (self.lopt * 5) - 5] = it
				else: res.INVENTORY[res.PARTY[res.FORMATION][self.inv.opt[2]]][self.inv.opt[1]][self.inv.opt[0]] = it
				if self.inv.itmov != '' and self.inv.itmov[0] == '_':
					self.inv.itmov = ''
			#DEVICE OPTIONS
			if mnuchk[3] and self.pressed[mnuchk[3]][0] and self.dev != None and self.inv.find(res.PARTY[res.FORMATION][0],'phone') != None and self.inv.type == 0:
				#OPEN AND CLOSE
				if self.phone == 0:
					self.player[0]['HEAD'] = 'DD'
					self.player[0]['SPRITE'] = 'PHONE'
					self.player[0]['PAUSE'] = 1
					self.phone = 1
				else:
					self.phone = 0
					if self.battle == False:
						self.dev.opt = [0,0]
						self.player[0]['PAUSE'] = 0
					else:
						self.mnu = 1
			#DEVICE EVENTS
			if self.phone > 0 and self.dev != None and self.dev.battery > 0:
				if event.type == pygame.KEYDOWN: self.dev.rqst = True
				if event.type == pygame.MOUSEBUTTONDOWN: self.dev.rqst = True
				self.dev.inside_events(self.pressed,self.dvmp)
				#CALL DIALOG
				if self.dev.ingame < 3:
					self.player[0]['SPRITE'] = 'CALL'
					self.phone = 0
					if self.dev.ingame == 1:
						gt = 0
						for i in self.waitlst:
							if i[0] == 'delivery': gt = 1
						self.dialog(dtb.DIALOGS[self.cal.nb][1][gt])
					if self.dev.ingame == 2:
						self.dialog(dtb.DIALOGS[self.cal.nb][1][0])
					self.player[0]['PAUSE'] = 1
					self.player[0]['SPRITE'] = 'PHONE'
					self.phone = 1
				#CAN'T CALL
				elif self.dev.ingame == 3:
					self.dialog([dtb.MENU[17]])
				#GET CALL
				elif self.dev.ingame < 6:
					self.phone = 0
					self.sfx.play(res.SOUND['MENU_GO'])
					self.player[0]['DIRECTION'] = 0
					self.player[0]['SPEED'] = 0
					self.player[0]['SPRITE'] = 'CALL'
					if self.dlg['FADE'] > 0:
						self.dialog(dtb.DIALOGS[self.cal.nb][0])
						res.CALLHIST.append([self.cal.nb,True])
						self.player[0]['SPRITE'] = 'STANDD'
					self.cal.nb = ''
					if self.dev.ingame == 5:
						self.phone = 0
						self.ch_msc.play(res.SOUND['AMBIENCE_SIREN'],-1)
						self.transiction(False, 50)
						#self.dialog(dtb.DIALOGS['HHBIANCA'][0])
						self.player[0]['PAUSE'] = 0
						self.transiction(False,0)
				#SAVE
				elif self.dev.ingame == 6:
					res.PX = self.player[0]['RECT'].x
					res.PY = self.player[0]['RECT'].y
				#PHOTO NOTIFICATION
				elif self.dev.ingame == 7:
					self.notification.append({'TEXT': self.foe[0]['NAME'] + ' registrada', 'COLOR': (134, 0, 211), 'HALIGN': 'left','X': 0})
			#MINIGAMES EVENTS
			if self.minigame != None:
				self.minigame.events(event)
			#READING OPTIONS
			if self.read != None:
				self.read.inside_events(self.pressed)
				if self.pressed[7][0]:
					self.ch_sfx.play(res.SOUND['PAGE_FLIP'])
					self.read = None
			#PLAYER OPTIONS
			if self.battle == False and self.inv.type == 0 and self.phone == 0:
				p = 0
				for i in self.player:
					i['POSTURE'] = 1
					if i['PAUSE'] == 0 and i['PLAYING'] and self.inv.type == 0:
						for a in range(6):
							if self.pressed[a][p]:
								#BOMB
								if res.ACTION[a] == 'bomb':
									sht = None
									for f in ['regular','slime','bolt','grenade','tactical']:
										if sht == None: sht = self.inv.find(res.PARTY[res.FORMATION][p],'bomb_' + f,'value')
									if sht != None:
										if sht[1] > 0:
											pp = 0
											nn = res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]]
											if nn == 'bomb_slime': pp = 1
											if nn == 'bomb_bolt': pp = 2
											img = []
											for f in range(13):
												img.append(pygame.image.load(res.SPRITES_PATH + 'bomb_' + str(f) + '.png'))
											self.particles.append({'TYPE': 'bomb',
											'X': math.floor(i['RECT'].x/self.map.tilewidth) * self.map.tilewidth,
											'Y': math.floor(i['RECT'].y/self.map.tileheight) * self.map.tileheight,
											'IMAGE': img,'GIF': 0.0,'POWER': pp})
											self.ch_sfx.play(res.SOUND['EQUIP'])
											sht[1] -= 1
											if sht[1] == 0: nn = 'bomb_regular'
											res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]] = nn
											res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3] + 1] = str(sht[1])
										else: self.ch_sfx.play(res.SOUND['ERROR'])
								#SHOOTING
								if res.ACTION[a] == 'shoot':
									sht = None
									for f in ['bubble','doublebubble','triplebubble','bounce','plasma','phantom','follow']:
										if sht == None: sht = self.inv.find(res.PARTY[res.FORMATION][p],'pow_' + f,'value')
									if sht != None:
										if sht[1] > 0:
											nn = res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]]
											qq = 1; ww = 0; ff = None; pp = 0
											if nn == 'pow_doublebubble': qq = 2
											if nn == 'pow_triplebubble': qq = 3
											if nn == 'pow_plasma': pp = 1
											if nn == 'pow_bounce': ww = 1
											if nn == 'pow_phantom': ww = 2
											if nn == 'pow_follow': ff = None
											for q in range(qq):
												self.particles.append({'TYPE': 'gunshot', 'X': i['RECT'].x, 'Y': i['RECT'].y,
												'COLOR': (100,150,200),'RADIUS': 3, 'DIRECTION': (i['DIRECTION'] - 1) * (45/qq), 'SPEED': 15,
												'WALL' : ww,'FOLLOW': ff,'POWER': pp,'PLAYER': p,'DESTROY': False})
											self.ch_sfx.play(res.SOUND['GUNSHOT_1'])
											sht[1] -= 1
											if sht[1] == 0: nn = 'pow_bubble'
											res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]] = nn
											res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3] + 1] = str(sht[1])
										else: self.ch_sfx.play(res.SOUND['ERROR'])
								#JUMP
								if res.ACTION[a] == 'jump':
									i['GRAVITY'] = 4.5 + float(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ACROBATICS']/2)
									i['STEP'] = 0
									self.ch_sfx.play(res.SOUND['FALL'])
								#RUN
								if res.ACTION[a] == 'run' and res.MOUSE == 2:
									spd1 = 3 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/4)
									spd2 = 6 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/2)
									if i['SWIM'] != None: spd1 -= 3; spd2 -= 1
									#elif self.inv.space(p) == False: spd1 -= 2; spd2 -= 1
									i['SPEEDLOCK'] = not i['SPEEDLOCK']
									if i['SPEEDLOCK'] == False: i['SPEED'] = spd1
									elif i['SPEEDLOCK']: i['SPEED'] = spd2
						if i['DRIVING'] == None:
							if i['JUMP'] == 0 and res.MAP != 'rodoviary':
								#PLACE OBJECTS
								if self.pressed[4][p]:
									if i['HOLD'] != None:
										i['HOLD'] = None
						#DRIVING DIRECTIONS
						else:
							if res.GAS > 0:
								if self.pressed[2][p]:
									i['DIRECTION'] -= 1
									if i['DIRECTION'] == 0: i['DIRECTION'] = 8
								elif self.pressed[3][p]:
									i['DIRECTION'] += 1
									if i['DIRECTION'] == 9: i['DIRECTION'] = 1
					p += 1
			#BUILD ITEMS
			if self.pressed[4][0] and self.build != '' and self.battle == False and self.phone == 0 and self.player[0]['SLEEP'] == False:
				if self.inv.type == 0:
					if self.build.startswith('tent'):
						self.objects.append(['tent',{'RECT': pygame.Rect(math.floor((self.player[0]['RECT'].x + 15)/30) * 30,math.floor((self.player[0]['RECT'].y + 15)/30) * 30,30,30),'SPRITE': pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')},self.player[0]['RECT'].y])
						self.build = ''
			#VKEYBOARD
			if self.vkb.active == True: self.vkb.events(event)
		self.pressed = self.get_pressed(None)
		#BATTLE AIM MOVE
		if self.battle and self.mnu == 2 and res.MOUSE < 2:
			for tp in range(len(self.player)):
				if self.pressed[0][tp] and self.aim.x > 10: self.aim.x -= 1
				if self.pressed[1][tp] and self.aim.x < self.displayzw - 10: self.aim.x += 1
				if self.pressed[2][tp] and self.aim.y > self.winbar: self.aim.y -= 1
				if self.pressed[3][tp] and self.aim.y < self.displayzh - self.winbar: self.aim.y += 1
		#INVENTORY WHEEL
		if self.pressed[6][0]:
			if self.inv.hld < 40: self.inv.hld += 1
		elif self.inv.hld > 0: self.inv.hld -= 1
		#PHONE HOLDING OPTIONS
		if self.phone > 0 and self.dev != None: self.dev.outside_events(self.pressed)
		#READING SCROLL
		if self.read != None: self.read.outside_events(self.pressed)
		#MOVE CAMERA
		if True:
			dir = 0
			spd = 2
			bt = [3,1,2,0,3,0]
			for d in range(4):
				if self.pressed[bt[d]][0] and res.ACTION[bt[d]] == 'camera':
					if self.pressed[bt[d - 1]][0]: dir = (d * 2)
					elif self.pressed[bt[d + 1]][0]: dir = (d * 2) + 2
					else: dir = (d * 2) + 1
			if dir == 1: self.cam.x += spd
			elif dir == 2: self.cam.x += spd; self.cam.y += spd
			elif dir == 3: self.cam.y += spd
			elif dir == 4: self.cam.x -= spd; self.cam.y += spd
			elif dir == 5: self.cam.x -= spd
			elif dir == 6: self.cam.x -= spd; self.cam.y -= spd
			elif dir == 7: self.cam.y -= spd
			elif dir == 8: self.cam.x += spd; self.cam.y -= spd
		#PAINT TILES
		do = False
		if self.pressed[4][0]: do = True
		if pygame.mouse.get_pressed()[0]: do = True
		if self.editing and do and self.paint != '' and self.battle == False and self.phone == 0 and self.player[0]['PAUSE'] == 0:
			if self.inv.type == 0 and self.map.properties['EDIT']:
				self.ch_sfx.play(res.SOUND['PAINT'])
				mse = [math.floor((self.cam.x + int(self.click.x/res.GSCALE))/self.mapdata['TILEWIDTH']),
				math.floor((self.cam.y + int(self.click.y/res.GSCALE))/self.mapdata['TILEHEIGHT'])]
				pos = (mse[0] * self.mapdata['TILEWIDTH'],mse[1] * self.mapdata['TILEHEIGHT'])
				ind = (mse[0] * self.mapdata['WIDTH']) + mse[1]
				if self.guit == 0 and ind < len(self.mapdata['TILES'][self.slayer]):
					self.tilmap[self.slayer][0].blit(self.tilset[0],pos)
					self.mapdata['TILES'][self.slayer][ind] = self.tilset[0]
				elif self.guit == 1 and ind < len(self.mapdata['TILES'][self.slayer]):
					self.tilmap[self.slayer][0].blit(self.tilset[self.paint],pos)
					self.mapdata['TILES'][self.slayer][ind] = self.tilset[self.slayer]
				elif self.guit == 2 and ind < len(self.mapdata['TILES'][self.slayer]):
					self.paint = self.mapdata['TILES'][self.slayer][ind]; self.guit = 1
				elif self.guit == 3: self.tilmap[0][l].blit(self.tilset[0],0)
				elif self.guit == 4:
					mp = pygame.mouse.get_pos()
					self.sselect[2] = self.click[0]
					self.sselect[3] = self.click[1]
				self.shist.insert(self.ihist,self.tilmap.copy())
				self.ihist += 1
		#PLAYER MOVEMENT
		p = 0
		for i in self.player:
			sprupd = True
			if i['PAUSE'] == 0 and i['PLAYING'] and self.battle == False:
				if i['DRIVING'] == None:
					if i['JUMP'] == 0:
						#POSTURE
						for a in range(6):
							if self.pressed[a][p]:
								if res.ACTION[a] == 'look': i['POSTURE'] = 2
								if res.ACTION[a] == 'squat': i['POSTURE'] = 0
						#SPEED SET
						spd1 = 3 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/4)
						spd2 = 6 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/2)
						if i['SWIM'] != None: spd1 -= 3; spd2 -= 1
						#elif self.inv.space(p) == False: spd1 -= 2; spd2 -= 1
						if res.MAP != 'rodoviary' and res.MOUSE < 2:
							if self.pressed[5][p]: i['SPEED'] = spd2
							else: i['SPEED'] = spd1
						elif res.MOUSE < 2: i['SPEED'] = 1
						else:
							if i['SPEEDLOCK'] == False: i['SPEED'] = spd1
							elif i['SPEEDLOCK']: i['SPEED'] = spd2
						#MOVE DIRECTIONS
						prs = 0
						bt = [3,1,2,0,3,0]
						for d in range(4):
							if self.pressed[bt[d]][p] and res.ACTION[bt[d]] in ['move','walk']:
								if res.ACTION[bt[d]] == 'move': sprupd = False
								if i['DIRECTION'] in [(d * 2),(d * 2) + 1,(d * 2) + 2]: prs = 2
								if self.pressed[bt[d - 1]][p]: i['DIRECTION'] = (d * 2)
								elif self.pressed[bt[d + 1]][p]: i['DIRECTION'] = (d * 2) + 2
								else: i['DIRECTION'] = (d * 2) + 1
								if prs == 0: prs = 1
						if i['DIRECTION'] == 0: i['DIRECTION'] = 8
						if prs == 0 and i['ACC'] > 0.0 and i['SPEED'] > 0.0: i['SPEED'] -= i['ACC']
						#elif prs == 2 and i['SPEED'] > 0.0: i['SPEED'] -= 0.5
						elif prs == 0: i['SPEED'] = 0
				#DRIVING OPTIONS
				else:
					if self.pressed[0][p]:
						i['DRIVING'] = None
						'''self.displayzw = 600
						self.displayzh = 400
						self.display[0] = pygame.Surface((600, 400))
						self.cam.width = self.displayzw
						self.cam.height = self.displayzh'''
						i['DIRECTION'] = 3
					if res.GAS > 0:
						if self.pressed[1][0]:
							if i['SPEED'] > 0.0: i['SPEED'] -= self.vehicles[i['DRIVING']]['ACCELERATION']
						elif self.pressed[5][p]:
							if i['SPEED'] < self.vehicles[i['DRIVING']]['SPEED'] and res.GAS > 0.0:
								i['SPEED'] += self.vehicles[i['DRIVING']]['ACCELERATION']
							res.GAS -= self.vehicles[i['DRIVING']]['GAS']
						else: i['SPEED'] -= self.vehicles[i['DRIVING']]['ACCELERATION']
			#FOLLOW
			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
					i['SPEED'] = 3
					if i['RECT'].y > i['FOLLOW'].y:
						if i['RECT'].x < i['FOLLOW'].x: i['DIRECTION'] = 8
						elif i['RECT'].x > i['FOLLOW'].x: i['DIRECTION'] = 6
						else: i['DIRECTION'] = 7

					elif i['RECT'].y < i['FOLLOW'].y: 
						if i['RECT'].x < i['FOLLOW'].x: i['DIRECTION'] = 2
						elif i['RECT'].x > i['FOLLOW'].x: i['DIRECTION'] = 4
						else: i['DIRECTION'] = 3

					elif i['RECT'].x < i['FOLLOW'].x:
						if i['RECT'].y > i['FOLLOW'].y: i['DIRECTION'] = 8
						elif i['RECT'].y < i['FOLLOW'].y: i['DIRECTION'] = 2
						else: i['DIRECTION'] = 1

					elif i['RECT'].x > i['FOLLOW'].x:
						if i['RECT'].y > i['FOLLOW'].y: i['DIRECTION'] = 6
						elif i['RECT'].y < i['FOLLOW'].y: i['DIRECTION'] = 4
						else: i['DIRECTION'] = 5

					if self.colide(i['RECT'],i['FOLLOW']):
						i['DIRECTION'] = i['FOLLEND']
						i['FOLLOW'] = None
						i['FOLLEND'] = 'head'
						i['SPEED'] = 0
				else:
					i['DIRECTION'] = i['FOLLEND']
					i['FOLLOW'] = None
					i['FOLLEND'] = 'head'
					i['SPEED'] = 0
			#MOVING CHARACTER
			dx = 0; dy = 0
			if i['DIRECTION'] in [8,1,2]: dx = self.map.tilewidth
			if i['DIRECTION'] in [2,3,4]: dy = self.map.tileheight
			if i['DIRECTION'] in [4,5,6]: dx = -self.map.tilewidth
			if i['DIRECTION'] in [6,7,8]: dy = -self.map.tileheight
			ind = (math.floor((i['RECT'].y + dy)/self.map.tileheight) * self.map.width) + math.floor((i['RECT'].x + dx)/self.map.tilewidth)
			rct = self.tilrect[3][ind]
			if rct == None: cld = False
			else:
				cld = self.colide(i['RECT'],rct[1])
				#if cld == False:
				#	for obj in self.objects:
				#		if obj[0] == 'move': cld = self.colide(i['RECT'],obj[1]['RECT'])
			if cld: i['SPEED'] = 0
			else:
				#POSITION UPDATE
				if i['SPEED'] > 0 and i['JUMP'] == 0 and i['PLAYING']:
					if i['DIRECTION'] == 1: i['RECT'].x += int(i['SPEED'])
					elif i['DIRECTION'] == 2: i['RECT'].x += int(i['SPEED']); i['RECT'].y += int(i['SPEED'])
					elif i['DIRECTION'] == 3: i['RECT'].y += int(i['SPEED'])
					elif i['DIRECTION'] == 4: i['RECT'].x -= int(i['SPEED']); i['RECT'].y += int(i['SPEED'])
					elif i['DIRECTION'] == 5: i['RECT'].x -= int(i['SPEED'])
					elif i['DIRECTION'] == 6: i['RECT'].x -= int(i['SPEED']); i['RECT'].y -= int(i['SPEED'])
					elif i['DIRECTION'] == 7: i['RECT'].y -= int(i['SPEED'])
					elif i['DIRECTION'] == 8: i['RECT'].x += int(i['SPEED']); i['RECT'].y -= int(i['SPEED'])
					#ALIGN
					algn = 30
					if i['DIRECTION'] in [3,7]: i['RECT'].x = (round(i['RECT'].x/algn) * algn) + int(algn/2) - int(i['RECT'].width/2)
					if i['DIRECTION'] in [1,5]: i['RECT'].y = (round(i['RECT'].y/algn) * algn) + int(algn/2) - int(i['RECT'].height/2)
					#i['RECT'].x += int(math.cos(i['DIRECTION']) * i['SPEED'])
					#i['RECT'].y += int(math.sin(i['DIRECTION']) * i['SPEED'])
				elif i['JUMP'] > 0 and i['PLAYING']:
					if i['DIRECTION'] == 3: i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED']
				#PARTY FOLLOW
				if i['PLAYING'] == False:
					if len(self.player[p - 1]['NODES']) > 5:
						if self.player[p - 1]['SPEED'] > 0:
							i['SPEED'] = self.player[p - 1]['NODES'][0]['SPEED']
							i['RECT'] = self.player[p - 1]['NODES'][0]['RECT']
							i['DIRECTION'] = self.player[p - 1]['NODES'][0]['DIRECTION']
							del self.player[p - 1]['NODES'][0]
							if len(self.player[p - 1]['NODES']) == 0: i['SPEED'] = 0
						else: i['SPEED'] = 0
					else: i['SPEED'] = 0
				if len(self.player) > p + 1 and i['SPEED'] > 0:
					i['NODES'].append({'RECT': self.player[p]['RECT'].copy(),'DIRECTION': self.player[p]['DIRECTION'],'SPEED': self.player[p]['SPEED']})
				#SPRITE UPDATE
				if sprupd:
					if i['JUMP'] > 0: spr = 'JUMP'
					elif i['DRIVING'] != None: spr = 'DRIVE'
					elif i['SPEED'] > 3: spr = 'RUN'
					elif i['SPEED'] > 0: spr = 'WALK'
					elif i['POSTURE'] == 0: spr = 'SEAT'
					elif i['POSTURE'] == 2: spr = 'DRIVE'
					elif res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] > dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][p]]['CLASS']]['RESISTANCE'][res.CHARACTERS[res.PARTY[res.FORMATION][p]]['LEVEL']]/5: spr = 'STAND'
					else: spr = 'TIREDSTAND'
					if i['SPEED'] > 0 or i['FOLLEND'] == 'head':
						if i['DIRECTION'] == 1: i['HEAD'] = 'R'
						elif i['DIRECTION'] == 2: i['HEAD'] = 'RD'
						elif i['DIRECTION'] == 3: i['HEAD'] = 'D'
						elif i['DIRECTION'] == 4: i['HEAD'] = 'LD'
						elif i['DIRECTION'] == 5: i['HEAD'] = 'L'
						elif i['DIRECTION'] == 6: i['HEAD'] = 'LU'
						elif i['DIRECTION'] == 7: i['HEAD'] = 'U'
						elif i['DIRECTION'] == 8: i['HEAD'] = 'RU'
					if self.phone == 0:
						if i['DIRECTION'] == 1: i['SPRITE'] = spr + 'R'
						elif i['DIRECTION'] == 2: i['SPRITE'] = spr + 'RD'
						elif i['DIRECTION'] == 3: i['SPRITE'] = spr + 'D'
						elif i['DIRECTION'] == 4: i['SPRITE'] = spr + 'LD'
						elif i['DIRECTION'] == 5: i['SPRITE'] = spr + 'L'
						elif i['DIRECTION'] == 6: i['SPRITE'] = spr + 'LU'
						elif i['DIRECTION'] == 7: i['SPRITE'] = spr + 'U'
						elif i['DIRECTION'] == 8: i['SPRITE'] = spr + 'RU'
			if res.GAS < 1.0: i['DIRECTION'] = 0
			if i['SPEED'] < 0: i['SPEED'] = 0
			p += 1
		#DIALOG SPEED
		if self.dlg['FADE'] == 0:
			self.dlg['SPEED'] = res.SPEED
			if self.pressed[4][0]: self.dlg['SPEED'] = 1

	def dialog(self, txt, wh=0):
		self.dlg = {'TEXT': [], 'FADE': 500, 'Y': 0, 'CAMERA': 0,
		'SPEED': res.SPEED, 'VOICE': 1, 'FONT': 'DEFAULT', 'TYPE': res.DTYPE}
		self.dlgrct = []
		self.lopt = 0
		self.player[0]['PAUSE'] = 1
		self.player[0]['SPEED'] = 0
		tid = 0
		did = 0
		spd = 10
		while tid < len(txt):
			#TEXT
			if isinstance(txt[tid], str):
				while self.dlg['FADE'] > 0:
					if self.winbar < 50 and self.battle == False:
						self.winbar += 5
					self.dlg['FADE'] -= 50
					self.run(False)
				else:
					self.dlg['TEXT'].append('')
					if res.TTS: plyer.tts.speak(txt[tid])
					if self.dlg['TYPE'] == 0: self.dlg['Y'] += 30
					else: self.dlg['Y'] += 40
					for i in txt[tid]:
						while True:
							if spd > 0: spd -= 10/self.dlg['SPEED']
							else:
								if res.TTS == False:
									if self.dlg['TYPE'] == 3: vv = 'TEXT_INPUT'
									else: vv = 'TTS' + str(self.dlg['VOICE'])
									self.soundplay(vv)
								self.dlg['TEXT'][did] += i
								if res.DISLEXIC:
									self.dlg['TEXT'][did] += ' '
								spd = 10
								break
							self.run(False)
					did += 1
			#DIALOG PROTOCOLS
			else:
				#SIDE MESSAGE
				if txt[tid] == 0:
					self.dlg['TEXT'].append(0)
					did += 1
				#WAIT FOR PRESS
				elif txt[tid] == 1:
					self.dlg['TEXT'].append(1)
					self.ch_sfx.stop()
					self.wait()
					self.ch_ton.play(res.SOUND['MENU_GO'])
					did += 1
				#DIALOG NAME
				elif txt[tid] == 2:
					pass
				#CHAPTER INTRO
				elif txt[tid] == 3:
					res.SCENE = -1
					self.ch_msc.pause()
					self.ch_ton.play(res.SOUND['BAUM'])
					self.player[0]['PAUSE'] = 3
					for i in range(100): self.run()
					res.SCENE = 0
					self.player[0]['PAUSE'] = 1
					self.ch_msc.unpause()
				#CHAPTER END
				elif txt[tid] in [4,5]:
					pygame.mixer.stop()
					self.player[0]['PAUSE'] = 3
					self.ch_ton.play(res.SOUND['CHAPTER_END'])
					spdacc = 0
					for i in range(120):
						spdacc += 2
						self.displayy += spdacc
						if self.displayy > self.windowh: self.displayy = 0
						self.run()
					if txt[tid] == 5:
						res.CHAPTER += 1
						res.DATE = dtb.CHAPTERS[res.CHAPTER][3]
						res.TIME = dtb.CHAPTERS[res.CHAPTER][4]
						res.MAP = dtb.CHAPTERS[res.CHAPTER][5][0]
						res.PX = dtb.CHAPTERS[res.CHAPTER][5][1]
						res.PY = dtb.CHAPTERS[res.CHAPTER][5][2]
					pygame.mixer.stop()
					self.title.ton.play(res.SOUND['NOISE'],-1)
					self.title.classrun = True
					self.title.winbar = 50
					self.title.wait = 100
					self.title.mnu = 7
					self.title.tv = 0
					self.classrun = 2
				#DIALOG SETTINGS
				elif txt[tid][0] == 0:
					if txt[tid][1] == 0: self.dlg['VOICE'] = txt[tid][2]
					if txt[tid][1] == 1: self.dlg['TYPE'] = txt[tid][2]
					if txt[tid][1] == 2: self.dlg['FONT'] = txt[tid][2]
				#ITEM GET
				elif txt[tid][0] == 1:
					if isinstance(txt[tid][1],int):
						mny = None
						for it in ['credit_card','wallet']:
							if mny == None: mny = self.inv.find(None,it,'value')
						if mny != None:
							mny[1] += txt[tid][1]
							res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1])
							self.ch_sfx.play(res.SOUND['CASH_GET'])
							self.notification.append({'TEXT': 'Adquiriu $' + str(txt[tid][1]), 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
					elif txt[tid][1] == 'greenblood':
						gb = self.inv.find(None,'tube','value')
						if gb != None:
							if gb[1] > 150: self.dialog(dtb.DIALOGS['REWARD'][3].copy(),i['RECT'])
							elif gb[1] > 90: self.dialog(dtb.DIALOGS['REWARD'][2].copy(),i['RECT'])
							elif gb[1] > 0: self.dialog(dtb.DIALOGS['REWARD'][1].copy(),i['RECT'])
							else: self.dialog(dtb.DIALOGS['REWARD'][0].copy(),i['RECT'])
							if gb[1] > 0 and self.notification['X'] == 0:
								mny = None
								for m in ['credit_card','wallet']:
									if mny == None: mny = self.inv.find(None,m,'value')
								if mny!= None:
									res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1] + gb[1])
									self.ch_sfx.play(res.SOUND['CASH_GET'])
									self.notification.append({'TEXT': 'Adquiriu $' + str(gb[1]), 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
									self.dlg['TEXT'] = []
									res.INVENTORY[gb[0][0]][gb[0][1]][gb[0][2]][gb[0][3]] = '000'
								else: self.dialog(dtb.DIALOGS['REWARD'][4].copy(),i['RECT'])
						else: self.dialog(dtb.DIALOGS['REWARD'][0].copy(),i['RECT'])
					else:
						if txt[tid][1] not in dtb.ITEMS: print('CAUTION: No item ' + txt[tid][1] + ' in database!')
						else:
							gt = True
							if len(txt[tid]) > 2 and txt[tid][2] != 0:
								mny = self.inv.find(None,'credit_card','value')
								if mny[1] < txt[tid][2]: gt = False
							if len(txt[tid]) > 3:
								if res.DLGSAV[txt[tid][3]] == 0:
									res.DLGSAV[txt[tid][3]] = 1
								else: gt = False
							if len(txt[tid]) > 4: prp = txt[tid][4]
							else: prp = '0000'
							if gt:
								if len(txt[tid]) > 2 and txt[tid][2] != 0:
									mny[1] -= txt[tid][2]
									res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1])
								self.inv.add(res.PARTY[res.FORMATION][0],txt[tid][1],prp)
								self.ch_sfx.play(res.SOUND['ITEM_GET'])
								self.notification.append({'TEXT': dtb.ITEMS[txt[tid][1]][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': -180,'IMAGE': pygame.image.load(res.ITEMS_PATH + txt[tid][1] + '.png')})
				#MORALITY
				elif txt[tid][0] == 2:
					if txt[tid][3] == 0:
						res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += txt[tid][2]
					else:
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] >= txt[tid][2]:
							for i in txt[tid][3]:
								txt.insert(tid + 1, i)
						else:
							for i in txt[tid][4]:
								txt.insert(tid + 1, i)
				#INSERT TEXT
				elif txt[tid][0] == 3:
					if isinstance(txt[tid][1],int):
						adtxt = res.CHARACTERS[txt[tid][1]]['NAME']
					elif txt[tid][1] == 'self':
						adtxt = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['NAME']
					elif txt[tid][1] == 'chat':
						adtxt = self.chat.copy()
					elif txt[tid][1] == 'CC':
						if res.CC: adtxt = txt[tid][2]
						else: adtxt = ''
					elif txt[tid][1].startswith('pronoun'):
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['PRONOUN'] == 'he':
							adtxt = dtb.DTALKS['he' + txt[tid][1][-1]]
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['PRONOUN'] == 'she':
							adtxt = dtb.TALKS['she' + txt[tid][1][-1]]
					elif txt[tid][1] == 'time':
						if res.TIME[0] < 6:
							adtxt = dtb.DTALKS['good night']
						elif res.TIME[0] < 12:
							adtxt = dtb.DTALKS['good morning']
						elif res.TIME[0] < 18:
							adtxt = dtb.DTALKS['good afternoon']
						elif res.TIME[0] < 24:
							adtxt = dtb.DTALKS['good evening']
					elif txt[tid][1] == 'deaths':
						adtxt = str(res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'])
					elif isinstance(txt[tid][1],tuple):
						adtxt = pygame.key.name(self.pressed[txt[tid][1][0]][txt[tid][1][1]]).lower()
					else:
						adtxt = dtb.DTALKS[txt[tid][1]]
					if isinstance(adtxt,str):
						if len(txt[tid]) > 2:
							adtxt += txt[tid][2]
						txt.insert(tid + 1, adtxt)
					else:
						for i in adtxt:
							txt.insert(tid + 1, '')
							self.dlg['TEXT'].append(i)
							did += 1
				#CALLING
				elif txt[tid][0] == 4:
					if txt[tid][1] != 'stop':
						self.ch_ton.play(res.SOUND['CALLING'],-1)
						self.ch_rng.play(res.SOUND['RINGTONE_' + str(res.PARTY[res.FORMATION][0])])
						if self.rad.onoff: pygame.mixer.music.pause()
						tw = 0
						cl = False
						while tw < 2000 and cl == False:
							pygame.time.wait(10)
							for event in pygame.event.get():
								if event.type == pygame.KEYUP:
									cl = True
							tw += 1
						self.ch_ton.stop()
						self.ch_rng.stop()
						self.ch_sfx.play(res.SOUND['EQUIP'])
						if cl:
							self.phone = 1
							self.mnu = 1
							txt.insert(tid + 1, [2,'stop'])
							txt.insert(tid + 1, 0)
							for i in self.dev.call(str(dtb.CONTACTS[txt[tid][1]][1]),0,False,False)[-1:0:-1]:
								txt.insert(tid + 1, i)
					else:
						self.phone = 0
						self.mnu = 0
				#NEW EMAIL
				elif txt[tid][0] == 5:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					mail = dtb.EMAILS[txt[tid][1]].copy()
					mail.append(0)
					res.INBOX.append(mail)
					res.inbx_save(len(res.INBOX)-1,0)
					self.notification.append({'TEXT': dtb.NOTINFO['EMAIL'], 'COLOR': (255, 221, 0), 'HALIGN': 'left','X': 0})
				#TASKS
				elif txt[tid][0] == 6:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					if txt[tid][1] in dtb.TASKINDEX:
						res.TASKS.append([txt[tid][1], 0])
						if 'TIME' in dtb.TASKINDEX[txt[tid][1]][0]:
							res.TIME = dtb.TASKINDEX[txt[tid][1]][0]['TIME']
						if 'MARKER' in dtb.TASKINDEX[txt[tid][1]][0]:
							res.MARKER.append(dtb.TASKINDEX[txt[tid][1]][0]['MARKER'])
						#res.task_save(txt[tid][1],0)
						self.notification.append({'TEXT': dtb.TASKINDEX[txt[tid][1]][0]['NAME'], 'COLOR': (255, 123, 0), 'HALIGN': 'left','X': 0})
					elif self.inv.find(res.PARTY[res.FORMATION][0],txt[tid][1]):
						self.ch_ton.play(res.SOUND['ITEM_GET'])
						for j in txt[tid][3][::-1]:
							txt.insert(tid + 1, j)
					else:
						for j in txt[tid][2][::-1]:
							txt.insert(tid + 1, j)
				#NEW CONTACT
				elif txt[tid][0] == 7:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					dtb.CONTACTS.append(dtb.NUMBERS[txt[tid][1]].copy())
					dtb.call_save(len(dtb.CONTACTS)-1)
					self.notification.append({'TEXT': dtb.NOTINFO['CONTACT'], 'COLOR': (165, 255, 0), 'HALIGN': 'left','X': 0})
				#ACHIEVEMENT
				elif txt[tid][0] == 8:
					self.ch_sfx.play(res.SOUND['ACHIEVEMENT'])
					dtb.ACHIEVEMENTS[txt[tid][1]][2] = True
					self.notification.append({'TEXT': dtb.ACHIEVEMENTS[txt[tid][1]][0], 'COLOR': (255, 191, 0), 'HALIGN': 'right','X': 0})
				#RELATIONS
				elif txt[tid][0] == 9:
					if txt[tid][3] == 0: res.RELATIONS[txt[tid][1][0]][txt[tid][1][1]] += txt[tid][2]
					elif txt[tid][3] == 1: res.RELATIONS[txt[tid][1][0]][txt[tid][1][1]] -= txt[tid][2]
					else:
						if res.RELATIONS[txt[tid][1][0]][txt[tid][1][1]] >= txt[tid][2]:
							for i in txt[tid][3]:
								txt.insert(tid + 1, i)
						else:
							for i in txt[tid][4]:
								txt.insert(tid + 1, i)
				#DIALOG CHOICES
				elif txt[tid][0] == 10:
					while self.dlg['FADE'] > 0:
						if self.winbar < 50 and self.battle == False: self.winbar += 5
						self.dlg['FADE'] -= 50
						self.run()
					else:
						self.dlg['CAMERA'] = 0
						self.dlg['TEXT'].append(0)
						yy = 0
						for j in txt[tid][-1:0:-1]:
							if res.DISLEXIC:
								out = ''
								for t in j[0]:
									out += t + ' '
							else: out = j[0]
							self.dlg['TEXT'].append(out)
							txtsz = math.floor(self.fnt['DEFAULT'].size(out)[0]/res.GSCALE) + 10
							yyax = self.displayzh - 100
							self.dlgrct.append(pygame.Rect((self.displayzw - 22) - txtsz,yyax + self.dlg['Y'] - yy,5 + txtsz,25))
							self.dlg['Y'] += 40
							yy += 40
						self.dlg['TEXT'].append(0)
						self.lopt = 1
						ln = len(txt[tid][1:])
						trigger = True
						yy = 0
						while trigger:
							if self.pressed[0][0]:
								if self.lopt < ln: self.ch_sfx.play(res.SOUND['MENU_HOR']); self.lopt += 1
							if self.pressed[1][0]:
								if self.lopt > 1: self.ch_sfx.play(res.SOUND['MENU_VER']); self.lopt -= 1
							do = False
							if self.pressed[4][0]: do = True
							for i in range(len(self.dlgrct)):
								mp = pygame.mouse.get_pos()
								if self.colide(self.dlgrct[i],pygame.Rect(int(mp[0]/res.GSCALE),int(mp[1]/res.GSCALE),2,2)):
									self.lopt = i
									do = True
							if do:
								self.ch_ton.play(res.SOUND['MENU_GO'])
								trigger = False
								crg = -1
								rctsv = self.dlgrct[self.lopt - 1].copy()
								self.dlgrct = [rctsv]
								i = 1
								while i <= ln + 1:
									if i != self.lopt:
										del self.dlg['TEXT'][crg - i]
										crg += 1
										ln -= 1
									i += 1
							self.run(False)
						self.dlg['CAMERA'] = wh
						for j in txt[tid][self.lopt][-1:0:-1]:
							txt.insert(tid + 1, j)
						self.lopt = 0
						did = len(self.dlg['TEXT'])
				#SKIP DIALOGS
				elif txt[tid][0] == 11:
					tid += txt[tid][1]
				#GUI CLASS
				elif txt[tid][0] == 12:
					if txt[tid][1] in ['storage','wash','trash','cashier','products','mercator']:
						if txt[tid][1] in ['products','mercator']:
							res.PRODUCTS = []
							for p in txt[tid][2]:
								add = [p[0],1]
								if len(p) > 1:
									if res.DATE[3] == p[1]:
										add[1] = int(add[1] * p[2])
								res.PRODUCTS.append(add)
							while len(res.PRODUCTS) < 25: res.PRODUCTS.append(['_',1])
						self.ch_sfx.play(res.SOUND['INVENTORY_OPEN'])
						if txt[tid][1] == 'storage': self.inv.type = 2
						if txt[tid][1] == 'cashier': self.inv.type = 3
						if txt[tid][1] == 'wash': self.inv.type = 4
						if txt[tid][1] == 'trash': self.inv.type = 5
						if txt[tid][1] == 'products': self.inv.type = 6
						if txt[tid][1] == 'mercator': self.inv.type = 7
						self.player[0]['PAUSE'] = 1
						self.inv.fade = 0
						self.opt = 0
						self.lopt = 0
						self.mnu = 0
					elif txt[tid][1].startswith('minigames.'):
						self.transiction(True,100)
						self.minigame = eval(txt[tid][1])
						self.transiction(False,0)
					else:
						dv = self.inv.dev(txt[tid][1])
						self.dev = dv[0]
						if self.dev == 'radio': self.dev = self.rad
						self.dev.battery = 9999
						self.phone = 1
				#BATTLE
				elif txt[tid][0] == 13:
					self.dlg['TEXT'] = []
					pygame.mixer.music.stop()
					if len(txt[tid]) > 2: rpt = txt[tid][2]
					else: rpt = 1
					x = 0
					for k in range(rpt):
						for f in txt[tid][1]:
							i = dtb.FREAKS[f].copy()
							i['FILE'] = f
							i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_stand.png')
							i['DIRECTION'] = 1
							i['FIGHTING'] = False
							i['HP'] = i['VITALITY']
							i['HEALTH'] = 0
							i['TIME'] = 20
							i['EFFECT'] = 0.0
							i['JUMP'] = 0
							if self.battle:
								sz = i['SPRITE'].get_rect()
								i['MASK'] = pygame.Rect(230,self.displayzh - (50 + sz.height),sz.width,sz.height)
								i['FIGHTING'] = True
								dprb = [1,5]
								i['DIRECTION'] = dprb[round(random.randint(0,1))]
								i['SPEED'] = 0
								i['BTIMES'] = [0,0,0,0]
								i['FADE'] = 10
								i['AWAY'] = 0
								i['N'] = x
							if i['TYPE'] != 'mercenary' and self.map.properties['HABITAT'] == i['HABITAT']:
								i['STRENGHT'] = int(i['STRENGHT'] * 1.25)
								i['AGILITY'] = int(i['AGILITY'] * 1.25)
								i['RESISTANCE'] = int(i['RESISTANCE'] * 1.25)
								i['HP'] = int(i['HP'] * 1.25)
							if i['TYPE'] == 'mercenary': self.mrc.append(i)
							else: self.foe.append(i)
							x += 1
					txt = []
					tid = 0
					if self.battle == False:
						self.mnu = 0
						self.turn = -4
						self.fight()
				#PROBABILITY
				elif txt[tid][0] == 14:
					prb = random.randint(0,100)
					for i in txt[tid][1:]:
						if prb > i[0] - 100:
							txt.insert(tid + 1, i[1:])
				#PLAY SFX/MUSIC
				elif txt[tid][0] == 15:
					if txt[tid][2] == 0:
						if len(txt[tid]) > 2: lp = txt[tid][2]
						else: lp = 0
						self.ch_sfx.play(res.SOUND[txt[tid][1]],lp)
					if txt[tid][2] == 1:
						pygame.mixer.music.load(res.MUSIC_PATH + txt[tid][1] + '.mp3')
						pygame.mixer.music.play(-1)
				#CHECK CHARACTER/DEATHS
				elif txt[tid][0] == 16:
					if txt[tid][1] == 'DEATHS':
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'] < 10: lst = txt[tid][2][0]
						elif res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'] < 20: lst = txt[tid][2][1]
						elif res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'] < 30: lst = txt[tid][2][2]
						elif res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'] < 40: lst = txt[tid][2][3]
						elif res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'] < 50: lst = txt[tid][2][4]
						else: lst = txt[tid][2][5]
						for j in lst[::-1]:
							txt.insert(tid + 1, j)
					else:
						if res.PARTY[res.FORMATION][0] == txt[tid][1]:
							for j in txt[tid][2][::-1]:
								txt.insert(tid + 1, j)
				#DELIVERY
				elif txt[tid][0] == 17:
					self.waitlst.append(['delivery',self.waitime + txt[tid][2],txt[tid][3]])
				#CHANGE PARTY
				elif txt[tid][0] == 18:
					ap = []
					p = 0
					for i in txt[tid][1:]:
						if i[1] != None:
							for n in range(len(self.npcs)):
								if i[1] == self.npcs[n]['N']:
									player = self.player[p].copy()
									xx = player['RECT'].x
									yy = player['RECT'].y
									dd = player['DIRECTION']
									cc = res.CHARACTERS[res.PARTY[res.FORMATION][p]].copy()
									ii = player['HAIR'] + player['COSTUME'] + cc['SKIN']
									npc = self.npcs[n].copy()
									self.player[p]['RECT'].x = npc['RECT'].x
									self.player[p]['RECT'].y = npc['RECT'].y
									self.player[p]['DIRECTION'] = npc['DIRECTION']
									self.player[p]['FOLLEND'] = 'head'
									self.player[p]['SPEED'] = 0
									self.npcs[n]['RECT'].x = xx
									self.npcs[n]['RECT'].y = yy
									self.npcs[n]['INDEX'] = ii
									self.npcs[n]['DIRECTION'] = dd
									self.npcs[n]['MOVE'] = 'stand'
									if len(i) > 2: self.npcs[n]['WHO'] = i[2]
						ap.append(i[0])
						p += 1
					res.PARTY[res.FORMATION] = ap
				#DATETIME
				elif txt[tid][0] == 19:
					ds = self.dlg['TEXT'].copy()
					self.dlg['TEXT'] = [] 
					self.dlg['TYPE'] = 3
					self.transiction(True,250,10,'fade')
					if txt[tid][1] != None: res.TIME = txt[tid][1]
					if txt[tid][2] != None: res.DATE = txt[tid][2]
					for i in range(10): self.run()
					tt = str(res.TIME[0]) + ':' + str(res.TIME[1]) + ':' + str(res.TIME[2])
					dd = str(res.DATE[0]) + '/' + str(res.DATE[1]) + '/' + str(res.DATE[2])
					self.dialog([(0,1,3),tt,dd,1])
					self.transiction(False,0,10,'fade')
					self.dlg['TEXT'] = ds
					self.dlg['TYPE'] = res.DTYPE
				#INCREASE/DECREASE STATUS
				elif txt[tid][0] == 20:
					if txt[tid][2] < 2:
						for i in self.foe + self.mrc:
							prb = round(random.randint(0,20))
							if prb > 10:
								self.ch_sfx.play(res.SOUND['ATTRIBUTE_LOSS'])
								if i['TYPE'] == 'spirit': tst = self.fig[self.turn]['SPIRITS']
								else: tst = self.fig[self.turn]['INTIMIDATION']
								if txt[tid][1] == 0:
									i['STRENGHT'] -= txt[tid][2] + tst
									self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['STRENGHT'].lower(), (200, 20, 20))
								if txt[tid][1] == 1:
									i['AGILITY'] -= txt[tid][2] + tst
									self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['AGILITY'].lower(), (20, 200, 20))
								if txt[tid][1] == 2:
									i['RESISTANCE'] -= txt[tid][2] + tst
									self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['RESISTANCE'].lower(), (20, 20, 200))
					if txt[tid][2] > 2:
						prb = round(random.randint(0,20))
						if prb > 10:
							self.ch_sfx.play(res.SOUND['ATTRIBUTE_GAIN'])
							if txt[tid][1] == 0:
								self.fig[self.turn]['STRENGHT'] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
								self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['STRENGHT'].lower(), (200, 20, 20))
							if txt[tid][1] == 1:
								self.fig[self.turn]['AGILITY'] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
								self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['AGILITY'].lower(), (20, 200, 20))
							if txt[tid][1] == 2:
								self.fig[self.turn]['RESISTANCE'] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
								self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES['RESISTANCE'].lower(), (20, 20, 200))
				#NEXT SCENE
				elif txt[tid][0] == 21:
					if isinstance(txt[tid][1],str): res.DLGSAV[txt[tid][1]] = txt[tid][2]
					else: res.SCENE = txt[tid][1]
				#KEYBOARD INPUT
				elif txt[tid][0] == 22:
					snd = self.ch_msc.get_sound()
					self.ch_msc.stop()
					yy = 0
					self.dlg['TEXT'].append(0)
					self.dlg['TEXT'].append('')
					txtsz = math.floor(self.fnt['DEFAULT'].size(self.dlg['TEXT'][-1])[0]/res.GSCALE) + 10
					self.dlgrct.append(pygame.Rect((self.displayzw - 22) - txtsz,self.displayzh - 100 + self.dlg['Y'] - yy,5 + txtsz,25))
					self.dlg['Y'] += 40
					self.vkb.active = True
					while self.vkb.active:
						self.dlg['TEXT'][-1] = self.vkb.output
						txtsz = math.floor(self.fnt['DEFAULT'].size(self.dlg['TEXT'][-1])[0]/res.GSCALE) + 10
						self.dlgrct[-1].x = self.displayzw - 22 - txtsz
						self.dlgrct[-1].width = 5 + txtsz
						self.run(False)
						if self.vkb.active == False:
							#CHAT MESSAGING
							if txt[tid][1] == 'chat':
								self.chat.append(0)
								self.chat.append(self.vkb.output)
								self.chat.append(0)
								if self.pressed[6][0] == False:
									self.vkb.output = False
									self.vkb.active = True
							#COMMAND LINE
							elif txt[tid][1] == 'debug':
								cmd = self.vkb.output.split(' ')
								if cmd[0].lower() == 'help':
									txt.insert(tid + 1,'mute pacify rectdebug disdbg player character \
									loadmap chapter time date dialog item battle inventory')
								if cmd[0].lower() == 'mute':
									pygame.mixer.stop()
									pygame.mixer.music.stop()
								if cmd[0].lower() == 'pacify':
									self.enemies = []
								if cmd[0].lower() == 'rectdebug':
									self.rectdebug = not self.rectdebug
								if cmd[0].lower() == 'disdbg':
									self.disdbg = not self.disdbg
								if cmd[0].lower() == 'editing':
									self.editing = not self.editing
								if cmd[0].lower() == 'python':
									try: txt.insert(tid + 1,str(eval(self.vkb.output.replace('python ',''))))
									except Exception as e: txt.insert(tid + 1,str(e))
								if cmd[0].lower() == 'player':
									if len(cmd) > 3:
										if cmd[3] in ['True','False']: vl = bool(cmd[3])
										elif abs(cmd[3]).isdigit(): vl = int(cmd[3])
										else: vl = str(cmd[3])
										self.player[int(cmd[1])][cmd[2].upper()] = vl
									else: txt.insert(tid + 1,'missing arguments in "player": (index, key, value)')
								if cmd[0].lower() == 'character':
									if len(cmd) > 3:
										if cmd[3] in ['True','False']: vl = bool(cmd[3])
										elif abs(cmd[3]).isdigit(): vl = int(cmd[3])
										else: vl = str(cmd[3])
										res.CHARACTER[int(cmd[1])][cmd[2].upper()] = vl
									else: txt.insert(tid + 1,'missing arguments in "character": (index, key, value)')
								if cmd[0].lower() == 'loadmap':
									if len(cmd) > 1: self.loadmap(cmd[1])
									else: txt.insert(tid + 1,'missing arguments in "loadmap": (file)')
								if cmd[0].lower() == 'chapter':
									if len(cmd) > 1: res.CHAPTER = int(cmd[1])
									else: txt.insert(tid + 1,'missing arguments in "chapter": (value)')
								if cmd[0].lower() == 'time':
									if len(cmd) > 2: res.TIME = [int(cmd[1]),int(cmd[2]),0]
									else: txt.insert(tid + 1,'missing arguments in "time": (hour,minute)')
								if cmd[0].lower() == 'date':
									if len(cmd) > 2: res.DATE = [int(cmd[1]),int(cmd[2]),2007,1,1]
									else: txt.insert(tid + 1,'missing arguments in "date": (day,month)')
								if cmd[0].lower() == 'dialog':
									if len(cmd) > 2: txt.insert(tid + 1,(23,cmd[1].upper(),int(cmd[2])))
									else: txt.insert(tid + 1,'missing arguments in "dialog": (key, index)')
								if cmd[0].lower() == 'item':
									if len(cmd) > 1: txt.insert(tid + 1,(1,cmd[1]))
									else: txt.insert(tid + 1,'missing arguments in "item": (key)')
								if cmd[0].lower() == 'battle':
									if len(cmd) > 1: txt.insert(tid + 1,(13,[cmd[1].lower()]))
									else: txt.insert(tid + 1,'missing arguments in "battle": (key)')
								if cmd[0].lower() == 'inventory':
									if len(cmd) > 1: self.inv.type = int(cmd[1])
									else: txt.insert(tid + 1,'missing arguments in "inventory": (value)')
								if cmd[0].lower() == 'gui':
									if len(cmd) > 1: txt.insert(tid + 1,(12,cmd[1]))
									else: txt.insert(tid + 1,'missing arguments in "gui": (class)')
					if txt[tid][1] in [0,1,2,3,4,5]:
						res.CHARACTERS[txt[tid][1]]['NAME'] = self.vkb.output
					if snd != None: self.ch_msc.play(snd,-1)
					self.dlg['TEXT'].append(0)
					did = len(self.dlg['TEXT'])
				#GET OTHER DIALOG
				elif txt[tid][0] == 23:
					dlg = txt[tid][1]
					if dlg not in dtb.DIALOGS: print('CAUTION: No dialog ' + dlg + ' in database!')
					else:
						idx = None
						if len(txt[tid]) > 2: idx = txt[tid][2]
						if self.battle:
							if dlg == None: dlg = self.foe[self.opt]['FILE']
							if dlg.upper() not in dtb.DIALOGS:
								dlg = 'IRRATIONAL'
							else: dlg = self.foe[self.opt]['FILE'].upper()
						if idx == None:
							for j in dtb.DIALOGS[dlg].copy()[::-1]:
								txt.insert(tid + 1, j)
						else:
							for j in dtb.DIALOGS[dlg][idx].copy()[::-1]:
								txt.insert(tid + 1, j)
						did = len(self.dlg['TEXT'])
				#MOVE CHARACTER
				elif txt[tid][0] == 24:
					px = txt[tid][2][0]
					py = txt[tid][2][1]
					if isinstance(px,str): px = self.player[0]['RECT'].x + int(px[2:])
					if isinstance(py,str): py = self.player[0]['RECT'].y + int(py[2:])
					if txt[tid][1] == None:
						if txt[tid][2] != (None,None):
							self.player[0]['FOLLOW'] = pygame.Rect(px,py,10,10)
						else: self.player[0]['FOLLOW'] = (None,None)
						self.player[0]['FOLLEND'] = txt[tid][3]
						if len(txt[tid]) > 4: self.player[0]['FOLLMOV'] = txt[tid][4]
					else:
						if txt[tid][1] == 'n':
							n = 0
							for i in self.npcs:
								if i['N'] > n: n = i['N']
						else: n = txt[tid][1]
						for i in self.npcs:
							if i['N'] == n:
								if txt[tid][2] != (None,None):
									i['FOLLOW'] = pygame.Rect(px,py,10,10)
								else: i['FOLLOW'] = (None,None)
								i['FOLLEND'] = txt[tid][3]
								if len(txt[tid]) > 4: i['FOLLMOV'] = txt[tid][4]
				#CHARACTER EMOTION
				elif txt[tid][0] == 25:
					if txt[tid][1] == None:
						self.player[0]['HEAD'] = txt[tid][2]
					else:
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								i['HEAD'] = txt[tid][2]
				#CAMERA
				elif txt[tid][0] == 26:
					if isinstance(txt[tid][1],int):
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								self.dlg['CAMERA'] = i['RECT']
					else: self.dlg['CAMERA'] = pygame.Rect(txt[tid][1][0],txt[tid][1][1],1,1)
				#WAIT
				elif txt[tid][0] == 27:
					ds = self.dlg['TEXT'].copy()
					self.dlg['TEXT'] = []
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = 'TWNN'
					for i in range(txt[tid][1]): self.run()
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = ''
					self.dlg['TEXT'] = ds
				#TUTORIAL
				elif txt[tid][0] == 28:
					if res.HELP:
						self.ch_ton.play(res.SOUND['NOTIFICATION'])
						self.tutorial = {'TEXT': dtb.TUTORIALS[txt[tid][1]].copy(), 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
						for j in self.tutorial['TEXT']:
							if isinstance(j,list):
								if j[0] == 'phone':
									self.tutorial['GO'] = j[1]
									if len(j) > 2: self.tutorial['NEXT'] = j[2]
								if j[0] == 'wait':
									self.tutorial['WAIT'] = j[1]
									if len(j) > 2: self.tutorial['NEXT'] = j[2]
								if j[0] == 'image':
									self.tutorial['OUTPUT'].append(j)
							else: self.tutorial['OUTPUT'].append(j)
				#ANOTHER PLACE
				elif txt[tid][0] == 29:
					ds = self.dlg['TEXT'].copy()
					self.dlg['TEXT'] = []
					self.transiction(True, 210, 10)
					self.loadmap(txt[tid][1])
					self.player[0]['RECT'].x = txt[tid][2]
					self.player[0]['RECT'].y = txt[tid][3]
					self.transiction(False, 50, 10)
					self.dlg['TEXT'] = ds
				#PUT CHARACTER
				elif txt[tid][0] == 30:
					ind = 0
					for n in self.npcs:
						if n['N'] > ind: ind = n['N']
					ind += 1
					self.npcs.append({'N': ind, 'RECT': pygame.Rect(txt[tid][1][0], txt[tid][1][1], 0, 0), 'TYPE': txt[tid][4], 'INDEX': txt[tid][2], 'WHO': txt[tid][3],
					'GIF': 0.0,'BLINK': 100,'HEAD': 'D','SPRITE': 'STANDD','MOVE': 'fixed','DIRECTION': 3,'SPEED': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None,'PAUSE': 0})
					self.objects.append(['npc',ind,txt[tid][1][1]])
				#CENSORSHIP
				elif txt[tid][0] == 31:
					if res.CENSORSHIP == False: txt.insert(tid + 1, txt[tid][2])
					elif res.CENSORSHIP: txt.insert(tid + 1, txt[tid][1])
			tid += 1
		#FINISH DIALOG
		self.dlg = {'TEXT': [], 'FADE': 0, 'Y': 0, 'CAMERA': 0,
		'SPEED': res.SPEED, 'VOICE': 1, 'FONT': 'DEFAULT', 'TYPE': res.DTYPE}
		self.player[0]['PAUSE'] = 0
		while self.dlg['FADE'] < 500:
			self.dlg['FADE'] += 50
			if self.winbar > 0 and self.battle == False:
				self.winbar -= 5
				self.run()

	def wait(self):
		waiting = True
		while waiting:
			self.pressed = self.get_pressed(None)
			for i in self.pressed:
				for j in i:
					if j: waiting = False
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN: waiting = False
				if event.type == pygame.KEYDOWN: waiting = False
			self.run(False)
	
	def confirmation(self):
		yesno = 0
		opt = 1
		srf = pygame.Surface((360,160))
		srf.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
		for x in range(36):
			for y in range(16):
				srf.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		while yesno == 0:
			for event in pygame.event.get():
				self.pressed = self.get_pressed(None)
				if self.pressed[2][0]: self.ch_sfx.play(res.SOUND['MENU_HOR']); opt = 1
				if self.pressed[3][0]: self.ch_sfx.play(res.SOUND['MENU_VER']); opt = 2
				if self.pressed[4][0]:
					yesno = opt
					if yesno == 1: self.ch_sfx.play(res.SOUND['MENU_GO'])
					if yesno == 2: self.ch_sfx.play(res.SOUND['MENU_BACK'])
					opt = 0
				if event.type == pygame.FINGERDOWN: yesno = 1
			srf.fill((0,0,0),pygame.Rect(10,10,340,140))
			srf.blit(self.fnt['DEFAULT'].render(dtb.MENU[85], True, (255, 255, 255)), (90, 20))
			if opt == 1: srf.blit(self.fnt['DEFAULT'].render(dtb.MENU[83], True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (80, 100))
			else: srf.blit(self.fnt['DEFAULT'].render(dtb.MENU[83], True, (255, 255, 255)), (80, 100))
			if opt == 2: srf.blit(self.fnt['DEFAULT'].render(dtb.MENU[84], True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (220, 100))
			else: srf.blit(self.fnt['DEFAULT'].render(dtb.MENU[84], True, (255, 255, 255)), (220, 100))

			self.screen.blit(srf, (int(self.windoww/2) - 180, int(self.windowh/2) - 80))
			self.run(False)

		return yesno

	def transiction(self, fade, limit, spd=5, type='bars'):
		dw = int((self.windoww/res.GSCALE)/100)
		dh = int((self.windowh/res.GSCALE)/100)
		self.transtype = type
		if type in ['bars','hole','side','fade','image','squares']:
			if type in ['hole','image']:
				chk = fade < limit
				self.winbar = 200
			else: chk = fade
			if type in ['bars','hole']: mm = dh
			else: mm = 1
			if chk:
				while self.winbar < limit:
					self.winbar += mm * spd
					self.run()
				if self.winbar > limit: self.winbar = limit
			else:
				while self.winbar > limit:
					self.winbar -= mm * spd
					self.run(False)
				if self.winbar < limit: self.winbar = limit
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
					acc += 1
		self.transtype = 'bars'
				
	def audioedit(self,snd,function,value):
		snd = pygame.sndarray.array(snd)
		if value > 0:
			window_size=2**13
			h=2**11
			if function == 'velocity':
				indices = numpy.round(numpy.arange(0, len(snd), value))
				indices = indices[indices < len(snd)].astype(int)
				snd = snd[indices.astype(int)]	     
			if function in ['stretch','pitch']:
				if function == 'pitch': factor = 1.0/(2**(1.0 * value/12.0))
				else: factor = value
				phase = numpy.zeros(window_size)
				hanning_window = numpy.hanning(window_size)
				result = numpy.zeros(int(len(snd)/value + window_size))
				for i in numpy.arange(0,len(snd)-(window_size+h), h*factor):
					ind = int(i)
					a1 = snd[ind: ind + window_size]
					a2 = snd[ind + h: ind + window_size + h]
					s1 = numpy.fft.fft(hanning_window * a1)
					s2 = numpy.fft.fft(hanning_window * a2)
					phase = (phase + numpy.angle(s2/s1)) % 2*numpy.pi
					a2_rephased = numpy.fft.ifft(numpy.abs(s2)*numpy.exp(1j*phase))
					i2 = int(i/f)
					result[i2 : i2 + window_size] += hanning_window*a2_rephased
				result = ((2**(16-4)) * result/result.max()).astype('int16')
				if function == 'pitch':
					indices = numpy.round(numpy.arange(0, len(snd[window_size:]), 2**(1.0 * value/12.0)))
					indices = indices[indices < len(snd[window_size:])].astype(int)
					snd = snd[indices.astype(int)]	     
		return pygame.sndarray.make_sound(snd)

	def fight(self):
		#BATTLE START
		if self.turn < 0:
			#PLAY SOUND
			self.inv.type = 0
			self.phone = 0
			self.player[0]['PAUSE'] = 2
			self.player[0]['SPEED'] = 0
			if self.rad.onoff: pygame.mixer.music.pause()
			if self.turn == -1: self.ch_ton.play(res.SOUND['BATTLE_FOE'])
			elif self.turn == -2:
				res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += 1
				self.ch_ton.play(res.SOUND['BATTLE_ENEMY'])
			elif self.turn == -3:
				res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] -= 1
				self.ch_ton.play(res.SOUND['BATTLE_AMBUSH'])
			elif self.turn == -6: self.ch_ton.play(res.SOUND['BAUM'])
			elif self.foe[0]['TYPE'] == 'boss': self.ch_ton.play(res.SOUND['BATTLE_BOSS'])
			if self.player[0]['DRIVING'] != None: self.obstacles = True
			#BACKGROUND
			self.bbg['IMAGE'] = pygame.image.load(res.BACKG_PATH + 'bt_' + self.map.properties['HABITAT'] + '.png')
			self.bbg['X'] = 0
			self.bbg['ACC'] = 0
			self.bbg['DIRECTION'] = False
			#SET UP PARTY
			self.fig = []
			tr = 0
			for i in res.PARTY[res.FORMATION]:
				dt = res.CHARACTERS[i]
				dt['N'] = tr
				dt['STRENGHT'] = dtb.CLASSES[dt['CLASS']]['STRENGHT'][dt['LEVEL']]
				dt['AGILITY'] = dtb.CLASSES[dt['CLASS']]['AGILITY'][dt['LEVEL']]
				dt['RESISTANCE'] = dtb.CLASSES[dt['CLASS']]['RESISTANCE'][dt['LEVEL']]
				dt['STAMINA'] = [100,100,100,100]
				self.fig.append(dt)
				tr += 1
			self.player[0]['SPEED'] = 0
			#SET UP ENEMIES
			x = 0
			for i in self.foe + self.mrc:
				sz = i['SPRITE'].get_rect()
				i['MASK'] = pygame.Rect(230 - ((len(self.foe + self.mrc) - 1) * 80) + (x * 80),self.displayzh - (50 + sz.height),sz.width,sz.height)
				dprb = [1,5]
				i['DIRECTION'] = dprb[round(random.randint(0,1))]
				i['SPEED'] = 0
				i['HP'] = i['VITALITY']
				i['BTIMES'] = [0,0,0,0]
				i['FADE'] = 10
				i['AWAY'] = 0
				i['N'] = x
				x += 1
			#CONDITIONS
			if len(self.foe) > 0:
				if self.turn == -3:
					self.foe[0]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[0]['FILE']) + '_backwards.png')
					self.foe[0]['HEALTH'] = 1
			else:
				if self.turn == -3:
					self.mrc[0]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[0]['FILE']) + '_backwards.png')
					self.mrc[0]['HEALTH'] = 1
			#ZOOM TRANSITION
			dw = int(self.windoww/100)
			dh = int(self.windowh/100)
			if self.turn != -6:
				self.transiction(True,int(self.windoww/100),type='zoom')
				"""acc = 0
				while True:
					self.displayzw -= acc * dw
					self.displayzh -= acc * dh
					self.cam.x += int(acc * (dw/2))
					self.cam.y += int(acc * (dh/2))
					self.cam.width = self.displayzw
					self.cam.height = self.displayzh
					if self.displayzw > dw: self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					else:
						self.displayzw = dw; self.displayzh = dh;
						self.cam.width = dw; self.cam.height = dh;
						self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
						break
					self.run()
					acc += 1"""
			#MYSTERIOUS FREAK
			else:
				freakname = self.foe[0]['NAME'].lower()
				showname = ''
				self.dlg['CAMERA'] = self.foe[0]['RECT']
				abc = 'abcdefghijklmnopqrstuvwxyz'
				for r in range(20):
					showname = ''
					for i in range(len(freakname)):
						self.ch_sfx.play(res.SOUND['TEXT_INPUT'])
						showname += abc[random.randint(0,len(abc) - 1)]
					self.cityname = showname
					self.run()
				for i in range(len(freakname)):
					self.ch_sfx.play(res.SOUND['MENU_GO'])
					showname = showname[:i] + freakname[i] + showname[i + 1:]
					self.cityname = showname
					self.run()
				self.ch_ton.play(res.SOUND['FREAK_DISCOVER'])
				self.transiction(300,100,type="image")
				for i in range(60): self.run()
				self.cityname = ''
				self.transtype = 'bars'
				self.dlg['CAMERA'] = 0
			#PLAY SONG
			if len(self.foe) > 0: sng = res.MUSIC_PATH + self.foe[0]['SONG'].lower() + '.mp3'
			elif len(self.mrc) > 0: sng = res.MUSIC_PATH + self.mrc[0]['SONG'].lower() + '.mp3'
			pygame.mixer.music.load(sng)
			pygame.mixer.music.play()
			self.player[0]['GIF'] = 0.0
			self.tilemation = 0.0
			self.battle = True
			self.sttsy = 120
			#ZOOM TRANSITION
			if self.turn != -6:
				self.transiction(False,int(self.windoww/res.GSCALE),type="zoom")
				"""acc = 0
				while True:
					self.displayzw += acc * dw
					self.displayzh += acc * dh
					self.cam.x -= int(acc * (dw/2))
					self.cam.y -= int(acc * (dh/2))
					self.cam.width = self.displayzw
					self.cam.height = self.displayzh
					if self.displayzw < int(self.windoww/res.GSCALE): self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					else:
						self.displayzw = int(self.windoww/res.GSCALE)
						self.displayzh = int(self.windowh/res.GSCALE)
						self.cam.x = 0
						self.cam.y = 0
						self.cam.width = int(self.windoww/res.GSCALE)
						self.cam.height = int(self.windowh/res.GSCALE)
						self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
						break
					self.run()
					acc += 1"""
			#TRANSICTION
			if res.GSCALE < 3: nb = 100
			else: nb = 60
			if self.turn != -6: self.transiction(True, nb)
			else: self.turn = 0; self.transiction(100,500,type="image")
			#SEEN ANOMALY
			chk = None
			for i in res.BESTIARY:
				if len(self.foe) > 0:
					if self.foe[0]['FILE'] == i['N'] and i['SEEN'] == 0:
						chk = self.foe[0]['NAME']
						i['SEEN'] = 1
			if chk == None and len(self.mrc) > 0: chk = self.mrc[0]['NAME']
			#AMBUSH
			if self.turn == -2: self.turn = len(self.fig)
			else: self.turn = 0
			#INITIATIVE DICES
			l = 0
			for i in self.player:
				if i['PLAYING']: l += 1
			if l > 1:
				for i in range(30):
					self.dices = []
					for d in range(len(self.player)):
						if self.player[d]['PLAYING']:
							di = dtb.CLASSES[self.fig[d]['CLASS']]['AGILITY'][self.fig[d]['LEVEL']] + self.fig[d]['BONUS'][2]
							self.dices.append([random.randint(0,di),d])
						else: self.dices.append([-1,d])
					self.run()
				for i in range(30):
					self.run()
				self.dices.sort(reverse=True)
				ord = []
				for i in self.dices:
					ord.append(self.fig[i[1]])
				self.dices = []
				self.fig = ord
			self.mnu = 1
		#PLAYERS TURN
		elif self.turn < len(res.PARTY[res.FORMATION]):
			again = False
			self.mnu = 3
			#EQUIPMEMT
			if self.equip[self.fig[self.turn]['N']] < 4:
				it = res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.turn] + 1][0]
				#SET STAMINA
				if res.BTYPE == 2:
					if it == '_':
						self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] -= (100 - (self.fig[self.turn]['ATLETISM'] * 2))
					else:
						self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] -= dtb.ITEMS[it][5]['CADENCY']
					if self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] < 0:
						self.fig[self.turn]['STAMINA'][self.equip[self.fig[self.turn]['N']]] = 0
				#SET AMMO
				if it != '_':
					pp = int(res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1])
					pp -= 1
					res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1] = str(pp)
				gottem = False
				#GRENADES
				if it.startswith('grenade'):
					cld = pygame.Rect(self.aim.x - 30,self.aim.y - 30,self.aim.width + 30,self.aim.height + 30)
					self.attackimation(9)
					res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.turn] + 1] = ['_','0000']
				#GUNS N MELEE
				else:
					cld = self.aim
				for i in self.foe + self.mrc:
					if self.colide(cld, i['MASK']) and i['FIGHTING']:
						gottem = True
						if it == '_': wpdmg = 0
						else: wpdmg = dtb.ITEMS[res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0]][5]['DAMAGE']
						dmg = int(random.randint(wpdmg - 2,wpdmg + 2)) - i['RESISTANCE'] + self.fig[self.turn]['STRENGHT']
						if res.CHARACTERS[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]]['HEALTH'] == 11: dmg = int(dmg/2)
						if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_damage.png')
						#HIT
						if dmg <= 0:
							dmg = 1
						for p in range(dmg * 2):
							if i['TYPE'] == 'mercenary': cl = (150, 25, 29)
							else: cl = (10, 255, 50)
							self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(random.randint(3,5)), 'DIRECTION': round(random.randint(0,360)),
								'SPEED': round(random.randint(2,6)), 'COLOR': cl})
						i['HP'] -= dmg
						self.hits += 1
						self.tdmg += dmg
						if dmg >= wpdmg + 2 - i['RESISTANCE'] + dtb.CLASSES[self.fig[self.fig[self.turn]['N']]['CLASS']]['STRENGHT'][self.fig[self.fig[self.turn]['N']]['LEVEL']]:
							if i['HP'] <= 0:
								self.ch_ton.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								i['AWAY'] = 1
							self.ch_sfx.play(res.SOUND['CRITICAL'])
							self.hitisplay(10, i['MASK'], dtb.BATTLE[3], (200, 0, 0))
						else:
							if it.startswith('melee'): self.ch_sfx.play(res.SOUND['HIT'])
							if it.startswith('gun'): self.ch_sfx.play(res.SOUND['GUNSHOT_1'])
							if it.startswith('grenade'): self.ch_sfx.play(res.SOUND['HIT'])
							else: self.ch_sfx.play(res.SOUND['HIT'])
							self.hitisplay(10, i['MASK'], str(dmg), (200, 0, 0))
						if i['HEALTH'] != 1 and i['HP'] > 0: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_stand.png')
						#CHECK WIN
						if i['HP'] <= 0:
							if dmg >= i['RESISTANCE']: again = True
							if i['ITEM'] != None:
								prb = round(random.randint(0,100))
								if prb > i['ITEM'][1]:
									self.inv.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
									self.ch_sfx.play(res.SOUND['ITEM_GET'])
									self.notification.append({'TEXT': 'it_' + i['ITEM'][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
							if i['AWAY'] == 0:
								self.ch_ton.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								while i['FADE'] > 0:
									i['FADE'] -= 0.5
									self.run()
							i['FIGHTING'] = False
				#MISS
				if gottem == False:
					self.ch_sfx.play(res.SOUND['MISS'])
					self.hitisplay(5, self.aim, dtb.BATTLE[4], (200, 200, 200))
				self.mnu = 0
			#RUN AWAY
			elif self.equip[self.turn] == 7:
				self.dialog([self.fig[self.turn]['NAME'] + dtb.BATTLE[15]])
				run = round(random.randint(0,30)) + self.fig[self.turn]['ATLETISM']
				if run > 20:
					self.ch_msc.fadeout(500)
					pygame.mixer.music.fadeout(500)
					self.dialog([dtb.BATTLE[17]])
					res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += 1
					self.transiction(True, int(self.displayzh/2))
					for i in self.enemies: i['FIGHTING'] = False
					self.turn = 0
					self.mnu = 0
					self.hits = 0
					self.tdmg = 0
					self.hpl = 0
					self.tbt = 0
					self.foe = []
					self.mrc = []
					self.battle = False
					self.sttsy = 0
					self.opt = 1
					self.player[0]['RECT'].x += 150
					if self.rad.onoff: pygame.mixer.music.unpause()
					self.transiction(False, 0)
				else:
					self.dialog([dtb.BATTLE[16]])
			#EXTRA ATTACK
			dth = 0
			for d in self.foe + self.mrc:
				if d['HP'] <= 0: dth += 1
			if dth < len(self.foe) + len(self.mrc) and self.battle and again:
				self.ch_ton.play(res.SOUND['ONE_MORE'])
				self.hitisplay(0, self.aim, dtb.BATTLE[5], (10, 50, 255))
				self.turn -= 1
			if self.turn < len(self.fig):
				self.aim.x = 100 + dtb.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]
		#ENEMIES TURN
		else:
			self.inv.type = 0
			self.phone = 0
			self.tbt += round(self.btime/10)
			self.btime = 100
			self.mnu = 3
			count = 0
			for i in self.foe + self.mrc:
				if i['HP'] > 0 and i['FIGHTING'] and i['HEALTH'] != 1 and len(self.fig) > 0:
					count += 1
					if count == 6: break
					#CONDITION DAMAGE
					if i['HEALTH'] > 15:
						i['HP'] -= 5
						self.hitisplay(5, i['MASK'], str(5), (200, 0, 0))
					#HABILITY
					prb = []
					for h in i['HABILITIES']:
						prb.append(h[4])
					opt = int(random.randint(0,100))
					rng = 100
					for p in range(len(prb)):
						rng -= prb[p]
						if opt >= rng:
							act = i['HABILITIES'][p].copy()
							break
					dd = i['NAME'] + dtb.BATTLE[18] + act[0]
					i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + i['FILE'] + '_attack.png')
					#TARGET RANGE
					otk = 0
					if i['TYPE'] != 'mercenary': lst = self.mrc
					else: lst = self.foe
					for d in lst:
						if d['HP'] > 0: otk += 1
					if i['HEALTH'] == 9: pl = int(random.randint(-20,len(self.fig) - 1 + otk))
					else: pl = int(random.randint(-1,len(self.fig) - 1 + otk))
					#DECREASE STATUS LIMIT
					if act[3] == 2 and i['BTIMES'][0] == 2: act = i['HABILITIES'][0]
					if act[3] == 3 and i['BTIMES'][1] == 2: act = i['HABILITIES'][0]
					if act[3] == 4 and i['BTIMES'][2] == 2: act = i['HABILITIES'][0]
					#ATTACK
					if pl >= 0:
						if pl >= len(self.fig): act = ['','',-10,1]
						if act[3] == 1:
							#SIMPLE ATTACK
							if act[2] < 0:
								#ATTACK PARTY
								if pl < len(self.fig):
									#ARMOR
									vst = self.inv.find(pl,'vest','value')
									if vst != None:
										act[2] += int(dtb.ITEMS[res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3]]][5])
										vst[1] -= 1
										if vst[1] <= 0: self.ch_ton.play(res.SOUND['MENU_BACK'])
										res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3] + 1] = str(vst[1])
									#FEAR
									if self.fig[pl]['FEAR'] == i['TYPE']: act[2] *= 1.5
									act[2] += i['RESISTANCE'] - self.fig[pl]['RESISTANCE']
									self.turn = self.fig[pl]['N']
									self.ch_ton.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
									self.ch_sfx.play(res.SOUND['DAMAGE_1'])
									#DODGE
									if self.attackimation(act[5]):
										act[2] -= math.floor(act[2]/5)
										self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
									#CRITICAL
									if -act[2] > int(self.fig[self.turn]['RESISTANCE']/4):
										if self.fig[pl]['HP'] <= 0: self.fig[pl]['HP'] -= 1
										else: self.fig[pl]['HP'] += act[2] + self.fig[pl]['RESISTANCE']
										self.hitisplay(-act[2] * 2, True, '', (0,0,0))
										self.fig[pl]['HEALTH'] = 15
										self.ch_ton.play(res.SOUND['INCONSCIOUS'])
									#HIT
									elif -act[2] > 0:
										if self.fig[pl]['HP'] <= 0: self.fig[pl]['HP'] -= 1
										else: self.fig[pl]['HP'] += act[2] + self.fig[pl]['RESISTANCE']
										self.hitisplay(-act[2] * 2, False, '', (0,0,0))
									#NO DAMAGE
									else:
										if self.fig[pl]['HP'] > 0: self.fig[pl]['HP'] += -1
										self.hitisplay(2, None, '', (0,0,0))
									self.hpl += act[2]
								else:
									#ATTACK MERCENARY
									if i['TYPE'] != 'mercenary':
										self.ch_sfx.play(res.SOUND['HIT'])
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.mrc[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.mrc[pl - len(self.fig)]['HP'] += act[2]
									#ATTACK FREAK
									else:
										self.ch_sfx.play(res.SOUND['HIT'])
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.foe[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.foe[pl - len(self.fig)]['HP'] += act[2]
							#SELF HEALING
							elif act[2] > 0:
								self.ch_ton.play(res.SOUND['HEAL'])
								i['HP'] += act[2]
						elif act[3] in [2,3,4,5]:
							lst = ('STRENGHT','AGILITY','RESISTANCE','CHARISMA')
							#REDUCE ATTRIBUTE
							if act[2] < 0 and ['BTIMES'][act[3] - 2] < 2:
								self.turn = self.fig[pl]['N']
								self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
								self.fig[pl]['STRENGHT'] += act[2]
								self.hitisplay(5, i['MASK'], '-' + str(act[2]) + ' ' + dtb.PROFNAMES[lst[act[3] - 2]], (200, 10, 10))
								i['BTIMES'][act[3] - 2] += 1
							#GROW ATTRIBUTE
							elif act[2] > 0:
								i[lst[act[3] - 2]] += act[2]
								self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
								self.hitisplay(5, i['MASK'], '+' + str(act[2]) + ' ' + dtb.PROFNAMES[lst[act[3] - 2]], (200, 10, 10))
						#INPUT CONDITION
						elif act[3] == 6:
							self.fig[pl]['HEALTH'] = act[2]
							if self.fig[pl]['HEALTH'] == 5: self.fig[pl]['AGILITY'] -= 20
							self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
							self.hitisplay(5, i['MASK'], dtb.FCONDITIONS[act[2]], (10, 10, 10))
						#ADD ANOMALY
						elif act[3] == 7:
							prb = round(random.randint(0,100))
							if prb > 49:
								wh = round(random.randint(0,len(act[2]) - 1))
								self.dialog([(13,[act[2][wh]])])
								if self.dlg['FADE'] > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,nw['NAME'] + dtb.BATTLE[37],1])
							else:
								if self.dlg['FADE'] > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,dtb.BATTLE[38],1])
						#RUN AWAY
						elif act[3] == 9:
							if self.dlg['FADE'] > 0: self.dialog([i['NAME'] + ' arregou!',1])
							while i['FADE'] > 0:
								i['FADE'] -= 0.5
								self.run()
							i['FIGHTING'] = False
							i['HP'] = 0
						#CHARGE ATTACK
						elif act[3] == 10:
							self.ch_ton.play(res.SOUND['CHARGE'])
							self.attackimation(act[5])
							self.turn = self.fig[pl]['N']
							self.ch_ton.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
							self.ch_sfx.play(res.SOUND['DAMAGE_1'])
							if self.attackimation(act[5]) == False:
								act[2] -= int(act[2]/5)
								self.fig[pl]['HP'] += act[2] + self.fig[pl]['RESISTANCE']
								self.hitisplay(-act[2] * 2, None, '', (0,0,0))
								self.hpl += act[2]
							else:
								self.ch_sfx.play(res.SOUND['HIT'])
								for p in range(dmg * 3):
									self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(random.randint(3,5)), 'DIRECTION': round(random.randint(0,360)), 'SPEED': round(random.randint(2,6))})
								self.hitisplay(10, i['MASK'], str(act[2]), (200, 0, 0))
								if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE'])+ '_stand.png')
								i['HP'] -= act[2]
								self.hits += 1
								self.tdmg += act[2]
							#COUNTER DAMAGE
							if i['HP'] <= 0:
								self.ch_ton.play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								while i['FADE'] > 0:
									i['FADE'] -= 0.5
									self.run()
								if i['ITEM'] != None:
									prb = round(random.randint(0,100))
									if prb > i['ITEM'][1]:
										self.inv.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
										self.ch_sfx.play(res.SOUND['ITEM_GET'])
										self.notification.append({'TEXT': 'it_' + i['ITEM'][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
								i['FIGHTING'] = False
						#CHECK DEATH
						if pl < len(self.fig) and self.fig[pl]['HP'] <= 0:
							self.mnu = 1
							#PERMADEATH
							if self.fig[pl]['HEALTH'] == 15 and self.fig[pl]['HP'] < 0:
								if self.fig[pl]['HP'] > -5: self.fig[pl]['HP'] -= 1
								else: self.ch_ton.play(res.SOUND['DEATH'])
							else:
								#FAINT
								if self.fig[pl]['BLESS'] == 0:
									self.fig[pl]['HP'] = 0
									self.fig[pl]['HEALTH'] = 15
									self.ch_ton.play(res.SOUND['INCONSCIOUS'])
								#REVIVE
								else:
									self.fig[pl]['BLESS'] -= 1
									self.fig[pl]['HP'] = dtb.CLASSES[self.fig[pl]['CLASS']]['RESISTANCE'][self.fig[pl]['LEVEL']]
									self.ch_ton.play(res.SOUND['REVIVE'])
						i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']).lower() + '_stand.png')
					#MISS
					else:
						i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']).lower() + '_stand.png')
						self.ch_sfx.play(res.SOUND['MISS'])
				#TURN AROUND
				elif i['HEALTH'] == 1 and self.dlg['FADE'] > 0:
					i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_stand.png')
					i['HEALTH'] = 9
			if self.turn > -1:
				self.turn =  0
				self.mnu = 1
		#OBSTACLES
		if self.obstacles:
			dmg = []
			self.mnu = 3
			for p in range(len(self.fig)):
				dmg.append(5)
				#ARMOR
				vst = self.inv.find(pl,'vest','value')
				if vst != None:
					dmg[p] += int(dtb.ITEMS[res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3]]][5])
					vst[1] -= 1
					if vst[1] <= 0: self.ch_ton.play(res.SOUND['MENU_BACK'])
					res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3] + 1] = str(vst[1])
			if self.attackimation(1):
				for p in range(len(self.fig)): dmg -= int(dmg/5)
				self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
			else:
				for p in range(len(self.fig)): self.fig[p]['HP'] += dmg[p] + self.fig[p]['RESISTANCE']
				self.hitisplay(-dmg[p] * 2, None, '', (0,0,0))
				self.ch_sfx.play(res.SOUND['DAMAGE_1'])
				self.hpl += dmg[p]
			self.mnu = 1
		#VICTORY
		dth = 0
		for d in self.foe + self.mrc:
			if d['HP'] <= 0: dth += 1
		if dth == len(self.foe) + len(self.mrc) and self.battle:
			self.ch_msc.fadeout(500)
			pygame.mixer.music.fadeout(500)
			if len(self.foe) >= 10: self.ch_ton.play(res.SOUND['BATTLE_BOSS_WON'])
			elif len(self.foe) > 0 and self.foe[0]['TYPE'] == 'boss': self.ch_ton.play(res.SOUND['BATTLE_BOSS_WON'])
			elif self.hpl == 0: self.ch_ton.play(res.SOUND['BATTLE_PERFECT'])
			else: self.ch_ton.play(res.SOUND['BATTLE_WON'])
			self.tbt += round(self.btime/10)
			xp = int(((self.hits*self.tdmg)-self.hpl+self.tbt)/len(self.fig))
			self.mnu = self.displayzw
			while self.sttsy > 120:
				self.sttsy -= 10
				self.run()
			self.transiction(True, int(self.displayzh/2) + 10)
			self.turn = -4
			self.obstacles = False
			self.bbg['X'] = 0
			while self.mnu > 0:
				self.mnu -= 60
				self.run()
			self.wait()
			#GREENBLOOD
			btls = None
			for i in res.PARTY[res.FORMATION]:
				for it in ['tube100','tube250']:
					btls = self.inv.find(i,it,'value')
					if btls != None and int(btls[1]) < dtb.ITEMS[res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]][5]: break
				if btls != None and int(btls[1]) < dtb.ITEMS[res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]][5]: break
			if btls != None:
				gb = btls[1]
				for i in self.foe:
					gb += i['BLOOD']
				while btls[1] < gb:
					if (gb - btls[1]) > 100: btls[1] += 5
					else: btls[1] += 1
					if btls[1] >= dtb.ITEMS[res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]][5]: break
					self.run()
				res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3] + 1] = str(btls[1])
			#PARTY XP
			for i in range(len(res.PARTY[res.FORMATION])):
				res.CHARACTERS[i]['XP'] += xp
				plux = int(100/(dtb.NEXTLEVEL[res.CHARACTERS[i]['LEVEL']]/res.CHARACTERS[i]['XP']))
			lvlup = False
			self.exvar = -1
			for i in range(len(self.fig)):
				self.lopt = -2
				while self.barxp[i] < plux and self.barxp[i] < 100:
					self.barxp[i] += 1
					self.run()
				#LEVEL UP
				if self.barxp[i] >= 100:
					self.lopt = -1
					if lvlup == False:
						self.bbg['IMAGE'] = pygame.image.load(res.BACKG_PATH + 'level_up.png')
						self.ch_ton.play(res.SOUND['LEVEL_UP'],-1)
						self.transiction(False, int(200/res.GSCALE), 10)
						lvlup = True
					if self.mnu < -self.displayzw:
						self.mnu = -self.displayzw
					while self.mnu > -(self.displayzw + 100):
						self.mnu -= 50
						self.run()
					self.exvar += 1
					self.barxp[i] = 0
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL'] += 1
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['HP'] += dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][i]]['CLASS']]['RESISTANCE'][res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL']] - dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][i]]['CLASS']]['RESISTANCE'][res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL'] - 1]
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['XP'] = 0
					self.wait()
					self.lopt = random.randint(0,6)
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['BONUS'][1] += self.lopt
					self.wait()
					while self.mnu > -((self.displayzw * 2) + 200):
						self.mnu -= 50
						self.run()
			if lvlup:
				self.transiction(True, 210, 10)
				self.ch_ton.fadeout(2500)
			else: self.wait()
			self.hits = 0
			self.tdmg = 0
			self.hpl = 0
			self.tbt = 0
			self.foe = []
			self.mrc = []
			self.btime = 100
			self.turn = -1
			self.battle = False
			if self.rad.onoff:pygame.mixer.music.play(self.song)
			self.player[0]['PAUSE'] = 0
			self.transiction(False, 0)

	def hitisplay(self, ex, tar, dmg, col):
		#SHAKE SCREEN
		if tar in [True,False]:
			if tar == False: dv = int(ex/30)
			else: dv = 0
			while ex != 0:
				self.screen.fill((255, 0, 0))
				if tar:
					self.displayx = dv * res.GSCALE
					self.displayy = 0
					dv += ex * 10
					if dv > self.displayzw * 1.25:
						dv = 1
						ex -= 3
						if ex < 0: ex = 0
				else:
					self.displayx = ex
					self.displayy = ex
					if ex > 0:
						ex = -ex
					elif ex < 0:
						ex = -ex
						ex -= dv
				self.run()
			self.displayx = 0
			self.displayy = 0
			self.dmg['INFO'] = None
	
	def attackimation(self, wh):
		self.banimation['INDEX'] = wh
		self.banimation['GIF'] = 0
		ddg = False
		counter = False
		if wh != 10:
			while self.banimation['GIF'] < len(res.SPRITES['ATTACKIMATION_' + str(wh)]):
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[res.ACT[0]] and self.banimation['GIF'] == len(res.SPRITES['ATTACKIMATION_' + str(wh)]):
						ddg = True
				self.run()
				self.banimation['GIF'] += 0.5
		else:
			while True:
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[res.ACT[0]] and self.banimation['GIF'] > 4.0:
						counter = True
				if counter == False: self.banimation['GIF'] += 0.25
				if counter: self.banimation['GIF'] -= 0.25

				if self.banimation['GIF'] == len(res.SPRITES['ATTACKIMATION_' + str(wh)]): ddg = False; break
				elif self.banimation['GIF'] == 0.0: ddg = True; break
				self.run()
		self.banimation['INDEX'] = None
		self.banimation['GIF'] = 0

		return ddg
		
	def particle(self, p):
		#POP
		if p['TYPE'] == 'pop':
			img = pygame.image.load(res.SPRITES_PATH + 'pop_' + str(int(p['GIF'])) + '.png')
			self.display[0].blit(img,(p['X'] - self.cam.x,p['Y'] - self.cam.y))
			if p['GIF'] < 8: p['GIF'] += 1
		#BOMB
		elif p['TYPE'] == 'bomb':
			if math.floor(p['GIF']) < len(p['IMAGE']):
				self.display[0].blit(p['IMAGE'][math.floor(p['GIF'])],(p['X'] - self.cam.x,p['Y'] - self.cam.y))
			p['GIF'] += 0.5
		#EXPLODE
		elif p['TYPE'] == 'explode':
			img = pygame.image.load(res.SPRITES_PATH + 'explode_' + str(math.floor(p['GIF'])) + '.png')
			self.display[0].blit(img,(p['X'] - self.cam.x,p['Y'] - self.cam.y))
			p['GIF'] += 1
			if p['GIF'] >= p['LIMIT']: p['GIF'] = 0
			p['TIME'] += 1
		#RAINDROP
		elif p['TYPE'] == 'raindrop' and self.turn != -6:
			rd = False
			if p['TIME'] <= 0:
				rd = True
				for i in self.areas:
					if self.colide(i['RECT'],pygame.Rect(p['X'],p['Y'],p['RADIUS'],p['RADIUS'])):
						rd = False
						break
			if rd == False:
				p['TIME'] -= 1
				p['X'] += int(math.cos(p['DIRECTION']) * p['SPEED'])
				p['Y'] += int(math.sin(p['DIRECTION']) * p['SPEED'])
				self.display[0].blit(p['IMAGE'], (p['X'],p['Y']))
				if p['TIME'] == 0:
					p['X'] = p['X'] + self.cam.x
					p['Y'] = p['Y'] + self.cam.y
			elif p['GIF'] <= 8:
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'raindrop_' + str(p['GIF']) + '.png'), (p['X'] - self.cam.x + 4,p['Y'] -self.cam.y + 6))
				p['GIF'] += 1
		#GREENBLOOD & GUNSHOT
		elif p['TYPE'] in ['blood','gunshot']:
			p['X'] += int(math.cos(p['DIRECTION']) * p['SPEED'])
			p['Y'] += int(math.sin(p['DIRECTION']) * p['SPEED'])
			if p['TYPE'] == 'blood':
				p['RADIUS'] -= 0.25
				if p['RADIUS'] < 0.0: p['RADIUS'] = 0.0
				cor = (p['X'],p['Y'])
			else: cor = (p['X'] - self.cam.x,p['Y'] - self.cam.y)
			pygame.draw.circle(self.display[0], p['COLOR'], cor, math.ceil(p['RADIUS']))
			if p['TYPE'] == 'gunshot':
				if self.colide(pygame.Rect(p['X'],p['Y'],2,2),self.cam) == False: p['DESTROY']
		#SPIN
		elif p['TYPE'] == 'spin':
			p['X'] += int(math.cos(p['DIRECTION']) * 5)
			p['Y'] += int(math.sin(p['DIRECTION']) * 5)
			cor = (p['X'] - self.cam.x,p['Y'] - self.cam.y)
			self.display[0].blit(pygame.transform.rotate(p['IMAGE'],p['SPIN']),cor)
			p['SPIN'] += 10
			p['TIME'] += 1
	
	def savemap(self, mp=None):
		tilset = os.listdir(res.TILES_PATH + 'files')
		tilset.remove('interior2.tsx')
		tilset.sort()
		contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
		'<map version="1.2" tiledversion="1.3.0" orientation="orthogonal" ' + \
		'renderorder="left-up" compressionlevel="0" width="{}" height="{}" '.format(self.mapdata['WIDTH'],self.mapdata['HEIGHT'])
		contents += 'tilewidth="{}" tileheight="{}" infinite="0" nextlayerid="14" nextobjectid="77">\n'.format(self.mapdata['TILEWIDTH'],self.mapdata['TILEHEIGHT'])
		if len(self.mapdata['PROPERTIES']) > 0:
			contents += '	<properties>\n'
			for p in self.mapdata['PROPERTIES'].items():
				contents += '		<property name="{}" type="{}" value="{}"/>\n'.format(p[0],type(p[1]).__name__,p[1])
			contents += '	</properties>\n'
		gid = 1
		for i in tilset:
			tst = pytmx.load_pygame(res.TILESETS_PATH + i)
			gid += tst.tilecount
			contents += '	<tileset firstgid="{}" source="../{}"/>\n'.format(gid,res.TILESETS_PATH + i)
		id = 1
		tid = 0
		oid = 1
		for i in self.mapdata['TILES']:
			contents += '	<layer id="{}" name="TILE LAYER {}" width="{}" height="{}">\n'.format(id,tid + 1,self.mapdata['WIDTH'],self.mapdata['HEIGHT'])
			contents += '<data encoding="csv">\n'
			dd = ''
			for d in i: dd += self.guitools.digitstring(d,3) + ','
			for d in range(self.mapdata['WIDTH']):
				contents += str(dd[d * (self.mapdata['WIDTH']) * 4:(d + 1) * (self.mapdata['HEIGHT']) * 4]) + '\n'
			contents = contents[0:-2] + '\n</data>\n	</layer>\n'
			tid += 1
		for i in self.mapdata['LAYERS']:
			nol = False
			if i.name.startswith('Camada'): nol = True
			elif i.name.startswith('TILE LAYER'): nol = True
			if nol: continue
			else:
				contents += '	<objectgroup id="{}" name="{}">'.format(id,i.name)
				for j in i:
					contents += '		<object id="{}" name="{}" type="{}" x="{}" y="{}">'.format(oid,j.name,j.type,j.x,j.y)
					if len(j.properties) > 0:
						contents += '			<properties>'
						for p in j.properties.items():
							contents += '				<property name="{}" type="{}" value="{}"/>'.format(p[0],type(p[1]).__name__,p[1])
						contents += '			</properties>'
					contents += '		</object>'
					oid += 1
				contents += '	</objectgroup>'
			id += 1
		contents += '</map>'
		if mp == None: nn = res.MAP
		else: nn = mp
		file = open(res.MAPS_PATH + nn + '.tmx','w')
		file.write(contents)
		file.close()
			
	def loadmap(self, mp=None):
		if mp == None: self.map = pytmx.load_pygame(res.MAPS_PATH + res.MAP + '.tmx')
		else:
			if mp[1:8] == 'highway':
				self.map = pytmx.load_pygame(res.MAPS_PATH + mp[1:11] + '.tmx')
				self.cityname = dtb.CITIES[self.map.properties['CITY']][0]
			else: self.map = pytmx.load_pygame(res.MAPS_PATH + mp + '.tmx')
			res.MAP = mp
		tilimg = {}
		self.tilmap = [[],[],[],[],[],[],[]]
		self.objects = []
		for i in range(len(self.player)):
			self.objects.append(['player',i,self.player[i]['RECT'].y])
		self.donesprites = {}
		pcam = [0,0]
		for i in range(len(self.player)):
			pcam[0] += self.player[i]['RECT'].x; pcam[1] += self.player[i]['RECT'].y
			if self.player[i]['PLAYING']: self.counter.append([0,0,0,0,0,0,0,0,0,0])
		if len(self.player) > 0: pcam = [int(pcam[0]/len(self.player)),int(pcam[1]/len(self.player))]
		else: pcam = [int(self.displayzw/2),int(self.displayzh/2)]
		self.cam.x = int(self.cam.x - pcam[0] - (self.displayzw/2))
		self.cam.y = int(self.cam.y - pcam[1] - (self.displayzh/2))
		#rects 1,rects 2,carry/hold,walls,hide,water
		self.tilrect = [[],[],[],[],[],[],[]]
		self.enemies = []
		self.foe = []
		self.npcs = []
		self.vehicles = []
		self.nodes = []
		self.areas = []
		self.particles = []
		self.loadingif = 0
		self.bbg['X'] = 0
		for i in self.player: i['NODES'] = []
		if 'ENEMIES' not in self.map.properties: self.map.properties['ENEMIES'] = ''
		if 'HABITAT' not in self.map.properties: self.map.properties['HABITAT'] = 'jungle'
		if 'EDIT' not in self.map.properties: self.map.properties['EDIT'] = False
		if 'INTERIOR' not in self.map.properties: self.map.properties['INTERIOR'] = 0
		if 'CITY' not in self.map.properties: self.map.properties['CITY'] = 0
		if 'HSCROLL' not in self.map.properties: self.map.properties['HSCROLL'] = 0
		if 'VSCROLL' not in self.map.properties: self.map.properties['VSCROLL'] = 0
		self.camgrid = 1
		portalind = 0
		#DRAW MAP BOUNDARIES
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, (self.map.height * self.map.tileheight) + self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		self.tilrect[3].append(['WALL',pygame.Rect((self.map.width * self.map.tilewidth) + self.map.tilewidth,-self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		#DRAW MAP
		i = -1
		tlyrs = 0
		for l in self.map.layers:
			nol = True
			if l.name.startswith('Camada'): nol = False
			if l.name.startswith('TILE LAYER'): nol = False
			if nol: continue
			else: i += 1; tlyrs += 1
			for a in range(2):
				self.tilmap[i].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
				for y in range(0, self.map.height):
					for x in range(0, self.map.width):
						gid = self.map.get_tile_gid(x, y, i)
						#NO TILE
						if gid == None and i == 0:
							self.tilrect[0].append(['WALL',pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
							if self.tilrect[3][len(self.tilrect[3]) - 1][0] == 'WALL': self.tilrect[3][len(self.tilrect[3]) - 1][1].width += self.map.tilewidth
							else: self.tilrect[3].append(['WALL',pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
						#FOUND TILE
						else:
							t = self.map.get_tile_properties_by_gid(gid)
							if t != None:
								#GET TILE TYPE
								if 'TYPE' not in t: t['TYPE'] = None
								elif t['TYPE'] == None: t['TYPE'] = 'NONE'
								else: t['TYPE'] = t['TYPE'].upper()
								#LOAD TIME IMAGE
								if gid in tilimg.keys() and t['TYPE'] != 'TREADMILL':
									if t['frames'] != []:
										if len(tilimg[gid]) <= a:
											if a >= len(tilimg[gid]): frm = t['frames'][len(tilimg[gid]) - 1]
											else: frm = t['frames'][a]
											tilimg[gid].append(self.map.get_tile_image_by_gid(frm.gid))
										image = tilimg[gid][a]
									else:
										image = tilimg[gid]
								else:
									if t['frames'] != []:
										image = self.map.get_tile_image_by_gid(t['frames'][a].gid)
										tilimg[gid] = []
										tilimg[gid].append(image)
									else:
										image = self.map.get_tile_image_by_gid(gid)
										tilimg[gid] = image
								#SKY
								if t['TYPE'] == 'SKY':
									if len(self.tilmap[3]) == 0:
										img = pygame.image.load(res.BACKG_PATH + 'sky.png')
										srf = pygame.Surface((self.map.width * self.map.tilewidth,img.get_height()), pygame.SRCALPHA)
										srf.fill((100,0,0))
										for rx in range(int((self.map.width * self.map.tilewidth)/img.get_width())):
											srf.blit(img, (rx * img.get_width(), 0))
										self.tilmap[3].append(srf)
								#PARALLAX SCROLLING
								elif t['TYPE'] == 'BACKGROUND':
									if len(self.tilmap[int(t['LAYER'])]) < a + 1:
										self.tilmap[int(t['LAYER'])].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
									if res.TIME[0] >= 18: fr = 1
									elif res.TIME[0] >= 6: fr = 0
									else: fr = 1
									if t['frames'] != []: image = self.map.get_tile_image_by_gid(t['frames'][fr].gid)
									else: image = self.map.get_tile_image_by_gid(gid)
									self.tilmap[int(t['LAYER'])][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#OBJECT TILE
								elif t['TYPE'] == 'OBJECT':
									tlrct = pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)
									self.objects.append(['tile',{'RECT': tlrct,'IMAGE': image},tlrct.y])
								#COLOR TILE
								elif t['TYPE'] == 'COLOR':
									t['SCALE'] = 30
									if int(t['COLOR']) == 0:
										t['COLOR'] = res.CHAPTER
									img = []
									for fi in range(t['COLOR'] + 1):
										img.append(self.map.get_tile_image_by_gid(t['frames'][fi].gid))
									t['IMAGE'] = img
								#ANIMATED TILES
								elif t['TYPE'] in ['SUNMOON','TREADMILL','PORTAL','SPIKE','JUMP']:
									if t['TYPE'] == 'SPIKE':
										t['HIDE'] = False
										t['TIME'] = 0 
									t['GIF'] =  0
									t['SFX'] = 100
									img = []
									for fi in range(len(t['frames'])):
										if t['TYPE'] != 'TREADMILL': frm = self.map.get_tile_image_by_gid(t['frames'][fi].gid)
										else: frm = pygame.transform.rotate(self.map.get_tile_image_by_gid(t['frames'][fi].gid),45 * (int(t['DIRECTION']) - 1))
										img.append(frm)
									t['IMAGE'] = img
								#MOVING
								elif t['TYPE'] == 'MOVING':
									t['IMAGE'] = image
									t['INOUT'] = True
									t['TIME'] = 0
								#NORMAL TILE
								elif t['TYPE'] not in ['INVISIBLE','CARRY','HOLD','HIDEON','HIDEOFF','WATER']:
									self.tilmap[i][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#TILRECT
								try: 
									p = self.map.get_tile_properties(x, y, i)
									trct = pygame.Rect((x + int(p['X'])) * self.map.tilewidth, (y + int(p['Y'])) * self.map.tileheight,int(p['WIDTH']),int(p['HEIGHT']))
								except: trct = pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)
								if i < 2 and a == 0:
									#STEP TILES
									if i == 0: self.tilrect[i].append([t,trct])
									#MOVABLE OBJECTS
									if t['TYPE'] in ['CARRY','HOLD','DESTROY']:
										if t['frames'] != []:
											trct = pygame.Rect(x * self.map.tilewidth, (y * self.map.tileheight) + self.map.tileheight,self.map.tilewidth,self.map.tileheight)
											srf = pygame.Surface((self.map.tilewidth,self.map.tileheight * 2), pygame.SRCALPHA)
											srf.blit(self.map.get_tile_image_by_gid(t['frames'][1].gid),(0,0))
											srf.blit(self.map.get_tile_image_by_gid(t['frames'][0].gid),(0,self.map.tileheight))
										else: srf = image
										self.objects.append(['move',{'IMAGE': srf,'RECT': trct,'TYPE': t['TYPE'],'DIRECTION': 0,'SPEED': 0,'DESTROY': False},trct.y])
									#PORTAL
									elif t['TYPE'] == 'PORTAL':
										dt = {'N': portalind, 'RECT': trct,
										'TYPE': 0, 'PX': t['GO'], 'PY': t['GO'], 'MAP': None,
										'OPENING': None,'CLOSURE': None,'MUSIC': None,'MATCH': None}
										self.objects.append(['portal',dt,trct.y])
										portalind += 1
									#SUNMOON
									elif t['TYPE'] == 'SUNMOON':
										self.tilrect[6].append([t,trct])
									#PROPS
									elif t['TYPE'] in ['SPIKE','JUMP','DESTROY']:
										self.tilrect[i].append([t,trct])
									#MIRROR SURFACES
									elif t['TYPE'] == 'WATER':
										self.tilrect[5].append([image,trct])
									#WALLS
									if t['TYPE'] in ['WALL','OBJECT','INVISIBLE']:
										#GLUE WALLS
										'''bft = self.tilrect[3][len(self.tilrect[3]) - 1]
										#if bft[1].y == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										#elif bft[1].height == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										if bft[1].x == (x - 1) * self.map.tileheight: bft[1].width += self.map.tileheight
										elif bft[1].width == (x - 1) * self.map.tilewidth bft[1].width += self.map.tilewidth'''
										
										#APPEND WALLS
										#else:
										if t['TYPE'] == 'OBJECT': hh = int(self.map.tileheight/2)
										else: hh = self.map.tileheight
										ww = pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,hh)
										if i == 0: self.tilrect[3].append([t,ww])
										else: self.tilrect[3][(x * self.map.width) + x] = [{'TYPE': 'WALL'},ww]
									elif i == 0 and a == 0: self.tilrect[3].append(None)
								#HIDE TILES
								else:
									if t['TYPE'].startswith('HIDE'): self.tilrect[4].append([t['TYPE'],pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,int(self.map.tilewidth),int(self.map.tileheight))])
							#FOR GRID
							elif i in [0,1]:
								self.tilrect[i].append(None)
								if i == 0: self.tilrect[3].append(None)
		#OBJECTS
		vhn = 0
		for lyr in self.map.layers:
			if lyr.name.startswith('Camada'): continue
			if lyr.name.startswith('TILE LAYER'): continue
			for i in lyr:
				#NPCS
				if i.name.startswith('npc'):
					obj = self.map.get_object_by_name(i.name)
					npc = {'N': int(i.name[4:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)),
					'TYPE': 0, 'INDEX': '000000', 'WHO': None,'HAIR': [0,0,0],'SKIN': 0,
					'GIF': 0.0,'BLINK': 100,'HEAD': 'D','SPRITE': 'STANDD','MOVE': 'fixed','DIRECTION': 3,'SPEED': 0, 'PAUSE': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None}
					
					if npc['RECT'].width == 0: npc['RECT'].width = 20
					if npc['RECT'].height == 0: npc['RECT'].height = 20
					add = True
					if obj.type == 'None': npc['TYPE'] = None
					#elif obj.type.startswith('scene'): npc['TYPE'] = int(obj.type)
					elif obj.type.startswith('if'):
						if res.SCENE == int(obj.type[2:]): npc['TYPE'] = 0
						else: add = False
					else: npc['TYPE'] = int(obj.type)

					for pr in obj.properties.items():
						if pr[0] == 'INDEX':
							npc['INDEX'] = pr[1]
							npc['HEAD'] = 'D'
							npc['SPRITE'] = 'STANDD'
						if pr[0] == 'HAIR':
							npc['HAIR'] = [int(pr[1][0:2]),int(pr[1][2:4]),int(pr[1][4:6])]
						if pr[0] == 'SKIN': npc['SKIN'] = pr[1]
						if pr[0] == 'WHO': npc['WHO'] = pr[1]
						if pr[0] == 'DIRECTION': npc['DIRECTION'] = int(pr[1])
						if pr[0] == 'MOVE': npc['MOVE'] = pr[1]

					if add:
						self.npcs.append(npc)
						self.objects.append(['npc',int(i.name[4:]),int(obj.y)])
				#VEICHLES
				if i.name.startswith('vehicle'):
					obj = self.map.get_object_by_name(i.name)
					vh = dtb.VEHICLES['moto_' + str(obj.type)].copy()
					vhn = int(i.name[8:])
					vh['N'] = vhn
					vh['RECT'] = pygame.Rect(int(obj.x), int(obj.y), 60, 10)
					vh['INDEX'] = int(obj.type)
					vh['DIRECTION'] = 1
					for pr in obj.properties.items():
						if pr[0] == 'MOVE': vh['MOVE'] = pr[1]
						if pr[0] == 'DIRECTION': vh['DIRECTION'] = int(pr[1])
					self.vehicles.append(vh)
					self.objects.append(['vehicle',int(i.name[8:]),int(obj.y)])
				#PORTALS
				if i.name.startswith('portal'):
					obj = self.map.get_object_by_name(i.name)
					dt = {'N': int(i.name[7:]) + portalind, 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)),
					'TYPE': int(obj.type), 'PX': obj.properties['PX'], 'PY': obj.properties['PY'], 'MAP': None,
					'OPENING': None,'CLOSURE': None,'MUSIC': None,'MATCH': None}
					for pr in obj.properties.items():
						if pr[0] == 'TIME':
							if obj.properties['TIME'].startswith('key'):
								dt['OPENING'] = obj.properties['TIME'][0:3]
								dt['CLOSURE'] = obj.properties['TIME'][3:7]
							else:
								dt['OPENING'] = [int(obj.properties['TIME'][0:2]),int(obj.properties['TIME'][2:4])]
								dt['CLOSURE'] = [int(obj.properties['TIME'][4:6]),int(obj.properties['TIME'][6:8])]
						if pr[0] == 'MUSIC': dt['MUSIC'] = obj.properties['MUSIC']
						if pr[0] == 'MATCH': dt['MATCH'] = obj.properties['MATCH']
						if pr[0] == 'MAP': dt['MAP'] = obj.properties['MAP']
						if pr[0].startswith('IF'):
							if pr[0][3:6] == 'NOT':
								pass
							elif res.CHAPTER == int(pr[0][3:5]):
								dt['MAP'] = pr[1]
							else: dt['MAP'] = obj.properties['IF NOT']
					self.objects.append(['portal',dt,int(obj.y)])
				#SIGNS
				if i.name.startswith('sign'):
					obj = self.map.get_object_by_name(i.name)
					sg = {'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), len(obj.type) * 10, int(obj.height)), 'TEXT': obj.type}
					for pr in obj.properties.items():
						if pr[0] == 'ICON': sg['ICON'] = pr[1]
					self.objects.append(['sign',sg,int(obj.y)])
				#LIGHTS
				if i.name.startswith('light'):
					obj = self.map.get_object_by_name(i.name)
					img = pygame.Surface((int(obj.width),int(obj.height)),pygame.SRCALPHA)
					if obj.type == '0':
						pygame.draw.ellipse(img, (255, 255, 255), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					elif obj.type == '1':
						for r in range(math.floor(obj.height/2)):
							srf = pygame.Surface((obj.width,obj.height),pygame.SRCALPHA)
							pygame.draw.circle(srf, (255, 255, 255, r), (math.floor(obj.width/2),math.floor(obj.height/2)), r)
							img.blit(srf,(0,0))
					elif obj.type == '2':
						pygame.draw.ellipse(img, (255, 208, 0, 100), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					self.objects.append(['light',{'TYPE': obj.type, 'IMAGE': img, 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))},int(obj.y)])
				#TOLLS
				if i.name.startswith('toll'):
					obj = self.map.get_object_by_name(i.name)
					tl = {'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'CENTER': pygame.Rect(0,0,44,16).center, 'ANGLE': int(obj.rotation), 'TIME': 0}
					self.objects.append(['toll',tl,int(obj.y)])
				#RADARS
				if i.name.startswith('radar'):
					obj = self.map.get_object_by_name(i.name)
					self.objects.append(['radar',{'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'LIMIT': 80},int(obj.y)])
				#NODES
				if i.name.startswith('node'):
					obj = self.map.get_object_by_name(i.name)
					self.nodes.append({'N': int(i.name[5:]), 'TYPE': int(obj.type), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'GOING': int(obj.properties['GOING'])})
					self.objects.append(['node',int(i.name[5:]),int(obj.y)])
				#AREAS
				if i.name.startswith('area'):
					obj = self.map.get_object_by_name(i.name)
					self.areas.append({'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))})
		#VEHICLE
		for p in self.player:
			if p['DRIVING'] != None:
				vh = dtb.VEHICLES['moto_0'].copy()
				vh['N'] = vhn + 1
				vh['RECT'] = pygame.Rect(int(p['RECT'].x), int(p['RECT'].y), 60, 10)
				vh['INDEX'] = 0
				vh['DIRECTION'] = 1
				vh['MOVE'] = 'fixed'
				self.vehicles.append(vh)
				self.objects.append(['vehicle',vhn + 1,int(p['RECT'].y)])
				p['DRIVING'] = vhn + 1
		#ENEMIES
		for prp in self.map.properties.items():
			if prp[0] == 'ENEMIES' and len(prp[1]) > 0:
				st = 0
				en = 0
				lst = []
				for i in self.map.properties['ENEMIES']:
					if i == '-':
						lst.append(self.map.properties['ENEMIES'][st:en])
						st = en + 1
					en += 1
				for i in range(round(random.randint(5,10))):
					wh = lst[round(random.randint(0,len(lst) - 1))]
					self.enemies.append(dtb.FREAKS[wh].copy())
					self.enemies[i]['N'] = i
					self.enemies[i]['FILE'] = wh
					self.enemies[i]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.enemies[i]['FILE']) + '_stand.png')
					sz = pygame.image.load(res.FREAKS_PATH + self.enemies[i]['FILE'] + '_mini.png').get_rect()
					rct = None
					while rct == None: rct = self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))]
					self.enemies[i]['RECT'] = pygame.Rect(rct[1].x,rct[1].y,sz.width,10)
					self.enemies[i]['DIRECTION'] = 1
					self.enemies[i]['FIGHTING'] = False
					self.enemies[i]['HP'] = self.enemies[i]['VITALITY']
					self.enemies[i]['HEALTH'] = 0
					self.enemies[i]['TIME'] = 20
					self.enemies[i]['FADE'] = 10
					self.enemies[i]['EFFECT'] = 0.0
					self.enemies[i]['JUMP'] = 0
					if self.map.properties['HABITAT'] == self.enemies[i]['HABITAT']:
						self.enemies[i]['STRENGHT'] = int(self.enemies[i]['STRENGHT'] * 1.25)
						self.enemies[i]['AGILITY'] = int(self.enemies[i]['AGILITY'] * 1.25)
						self.enemies[i]['RESISTANCE'] = int(self.enemies[i]['RESISTANCE'] * 1.25)
						self.enemies[i]['HP'] = int(self.enemies[i]['HP'] * 1.25)
					self.objects.append(['enemy',i,self.enemies[i]['RECT'].y])
			#SIGNAL
			elif prp[0] == 'SIGNAL': res.SIGNAL = self.map.properties['SIGNAL']
			#TEMPERATURE
			elif prp[0] == 'CITY': res.TEMPERATURE = dtb.CITIES[self.map.properties['CITY']][1][res.DATE[1] - 1]
			#CAMGRID
			elif prp[0] == 'CAMGRID': self.camgrid = self.map.properties['CAMGRID']
			#EDIT
			elif prp[0] == 'EDIT':
				tt = []
				tilset = os.listdir(res.TILESETS_PATH)
				tilset.remove('interior2.tsx')
				tilset.sort()
				for i in range(tlyrs):
					tt.append([])
					for y in range(self.map.height):
						for x in range(self.map.width):
							gg = self.map.get_tile_gid(x,y,i)
							if gg > 0:
								stp = self.map.get_tileset_from_gid(gg).name
								gg += 1
								for t in tilset:
									tlset = pytmx.load_pygame(res.TILESETS_PATH + t)
									gg += tlset.tilecount
									if tlset.name == stp: break
							tt[i].append(gg)
				self.mapdata = {
				'WIDTH': self.map.width,'HEIGHT': self.map.height,
				'TILEWIDTH': self.map.tilewidth,'TILEHEIGHT': self.map.tileheight,
				'PROPERTIES': self.map.properties,'TILES': tt,'LAYERS': self.map.layers,
				}
				self.shist.append(self.tilmap.copy())
				self.ihist = 0
				print(self.shist[self.ihist])
			#ANIMALS
			elif prp[0] == 'ANIMALS':
				st = 0
				en = 0
				lst = []
				for i in self.map.properties['ANIMALS']:
					if i == '-':
						lst.append(self.map.properties['ANIMALS'][st:en])
						st = en + 1
					en += 1
				for i in range(random.randint(0,5)):
					prb = random.randint(0,len(lst) - 1)
					img = res.SPRITES[lst[prb] + '_WALKL'][0]
					sz = img.get_rect()
					rct = None
					while rct == None: rct = self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))]
					rct = pygame.Rect(rct[1].x,rct[1].y,sz.width,sz.height)
					self.objects.append(['pet',{'N': i,'FILE': lst[prb],'RECT': rct,'SPRITE': res.SPRITES[lst[prb] + '_WALKL'],
					'GIF': 0.0,'DIRECTION': 1,'SPEED': 2,'MOVE': 'walk','TIME': 20},rct.y])
		#GLUE TILES
		if len(self.tilrect[5]) > 0:
			nw = []
			rct = [pygame.Surface((self.tilrect[5][0][1].width,self.tilrect[5][0][1].height)),self.tilrect[5][0][1]]
			for i in range(len(self.tilrect[5]) - 1):
				if self.tilrect[5][i][1].x == self.tilrect[5][i + 1][1].x + self.map.tilewidth:
					rct[1].width += self.map.tilewidth
				else: nw.append(rct.copy()); rct = [pygame.Surface((self.tilrect[5][i][1].width,self.tilrect[5][i][1].height)),self.tilrect[5][i][1]]
			self.tilrect[5] = nw
			self.loadingif = None
		for i in self.objects:
			if i[0] == 4: print(i[1])
	
	def draw(self):
		for i in self.display: i.fill((0,0,0,0))
		if self.battle and self.turn < 0: self.hpctrl = []
		elif self.dlg['FADE'] > 0: self.hpctrl = []
		else: self.hpctrl = dtb.HINTS['MENUS']
		#TILEMATION
		if self.player[0]['PAUSE'] < 2: self.tilemation += 0.1
		if self.tilemation >= 2.0: self.tilemation = 0.0
		#BLINDNESS
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 12:
			self.display[0].fill((0,0,0))
		#STUDIO
		elif self.editing:
			self.display[0].fill((200,0,200))
			"""for l in self.shist[self.ihist]:
				pos = [0,0]
				for t in l:
					self.display[0].blit(self.tilset[t],((pos[0] * self.mapdata['TILEWIDTH']),(pos[1] * self.mapdata['TILEHEIGHT'])))
					pos[0] += 1
					if pos[0] >= self.mapdata['WIDTH']:
						pos[0] = 0; pos[1] += 1"""
			for i in self.shist[self.ihist]:
				for l in i:
					self.display[0].blit(i[0],(0,0))#,(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
			for y in self.objects:
				if y[0] == 'npc':
					for i in self.npcs:
						if i['N'] == y[1]:
							pygame.draw.rect(self.display[0],(200,200,0),pygame.Rect(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y,i['RECT'].width,i['RECT'].height))
				if y[0] == 'portal': pygame.draw.rect(self.display[0],(200,200,0),pygame.Rect(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y,y[1]['RECT'].width,y[1]['RECT'].height))
			self.display[0].blit(self.inv.bar(1,4,(1,5),'vertical'),(0,0))
		#TILED MAP
		elif self.turn != -6:
			#SKY
			if len(self.tilmap[3]) > 0:
				tt = (res.TIME[0] * 60) + res.TIME[1]
				img = self.tilmap[3][0]
				self.display[0].blit(img, (0, -(tt * ((img.get_height() - (img.get_height()/self.displayzh))/1440))))
				if len(self.tilrect[6]) > 0:
					for i in range(2):
						aa = ((tt)/240) + 2 + (i * 3)
						xx = int(math.cos(aa) * 100) + int(self.displayzw/2)
						yy = int(math.sin(aa) * 100) + int(self.displayzh/2)
						if i == 0: frm = 0
						else: frm = res.DATE[4]
						self.display[0].blit(self.tilrect[6][0][0]['IMAGE'][frm],(xx,yy))	
			#PARALLAX SCROLLING
			px = 2
			for t in self.tilmap[4:]:
				if len(t) > 0: self.display[0].blit(t[math.floor(self.tilemation)], (-math.floor(self.cam.x/px), -math.floor(self.cam.y/px)))
				px += 3
			self.display[0].blit(self.tilmap[0][math.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
			if len(self.tilmap[1]) > 0: self.display[0].blit(self.tilmap[1][math.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
			#PROPS
			ind = 0
			for i in list(filter(lambda item: item != None, self.tilrect[0] + self.tilrect[1])):
				if i != None:
					if i[0]['TYPE'] == 'COLOR':
						if i[0]['SCALE'] == self.map.tilewidth: img = i[0]['IMAGE'][i[0]['COLOR']]
						else:
							img = pygame.transform.scale(i[0]['IMAGE'][i[0]['COLOR']],(i[0]['SCALE'],self.map.tileheight))
							i[0]['SCALE'] += 1
						self.display[0].blit(img, (i[1].x - self.cam.x, i[1].y - self.cam.y))
					if i[0]['TYPE'] in ['TREADMILL','PORTAL']:
						self.display[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
						i[0]['GIF'] += 0.5
						if i[0]['GIF'] == len(i[0]['IMAGE']):
							i[0]['GIF'] = 0
						sdist = 60
						sarea = pygame.Rect(i[1].x - sdist,i[1].y - sdist,sdist * 2,sdist * 2)
						"""sx = (self.player[0]['RECT'].x - sarea.x/sdist)
						if sx > 1.0: sx -= 1.0
						sy = (self.player[0]['RECT'].y - sarea.y/sdist)
						if sy > 1.0: sy -= 1.0
						i[0]['SFX'] = (sx + sy/2)
						self.ch_ton.set_volume(i[0]['SFX'] * res.SFX)
						self.ch_ton.play(res.SOUND['STEP_MOTOR'])"""
					if i[0]['TYPE'] == 'MOVING':
						self.display[0].blit(i[0]['IMAGE'], (i[1].x - self.cam.x, i[1].y - self.cam.y))
						if i[0]['INOUT'] == False:
							if i[0]['DIRECTION'] == 1: i[1].x -= 1
							if i[0]['DIRECTION'] == 3: i[1].y -= 1
						if i[0]['INOUT']:
							if i[0]['DIRECTION'] == 1: i[1].x += 1
							if i[0]['DIRECTION'] == 3: i[1].y += 1
						i[0]['TIME'] += 1
						if i[0]['TIME'] == 30:
							i[0]['TIME'] = 0
							i[0]['INOUT'] = not i[0]['INOUT']
					if i[0]['TYPE'] == 'SPIKE':
						self.display[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
						if i[0]['TIME'] < 30: i[0]['TIME'] += 1
						if i[0]['TIME'] == 30:
							if i[0]['HIDE'] == False:
								i[0]['GIF'] += 0.5
								if int(i[0]['GIF']) == len(i[0]['IMAGE']) - 1:
									i[0]['HIDE'] = True
									i[0]['TIME'] = 0
							elif i[0]['HIDE']:
								i[0]['GIF'] -= 0.5
								if int(i[0]['GIF']) == 0:
									i[0]['HIDE'] = False
									i[0]['TIME'] = 0
					if i[0]['TYPE'] == 'JUMP' and i[0]['DIRECTION'] == 0:
						self.display[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
						if i[0]['GIF'] > 0: i[0]['GIF'] += 0.5
						if int(i[0]['GIF']) == len(i[0]['IMAGE']) - 1: i[0]['GIF'] = 0
					if i[0]['TYPE'] == 'SLIME':
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'slime.png'), (i[1].x - self.cam.x, i[1].y - self.cam.y))
				ind += 1
			#MIRROR SURFACES
			for i in self.tilrect[5]:
				self.display[0].blit(i[0],(i[1].x - self.cam.x, i[1].y - self.cam.y))
				if self.rectdebug: pygame.draw.rect(self.display[0],(0,0,255),pygame.Rect(i[1].x - self.cam.x,i[1].y - self.cam.y,i[1].width,i[1].height),3)
		else: self.display[0].fill((250,10,10))
		#for t in self.tilrect[3]:
		#	if self.rectdebug and t!= None: pygame.draw.rect(self.display[0],(255,0,0),pygame.Rect(t[1].x - self.cam.x,t[1].y - self.cam.y,t[1].width,t[1].height),3)
		#DEPTH
		dpth = 0
		for i in range(len(self.objects)):
			if i!= len(self.objects) - 1:
				if self.objects[i][2] > self.objects[i + 1][2]:
					self.objects.insert(i, self.objects[i + 1])
					del self.objects[i + 2]
		#DELETE OBJECTS
		for i in range(len(self.enemies)):
			if self.enemies[i]['HP'] <= 0: del self.enemies[i]; break
		for i in range(len(self.npcs)):
			if self.npcs[i]['DIRECTION'] == 0: del self.npcs[i]; break
		for i in range(len(self.objects)):
			if self.objects[i][0] in ['item','move','click'] and self.objects[i][1]['DESTROY']:
				del self.objects[i]; break
		#OVERWORLD
		if self.battle == False and self.editing == False:
			#OBJECTS
			cm = pygame.Rect(self.cam.x - 100,self.cam.y - 100,self.cam.width + 200,self.cam.height + 200)
			for y in self.objects:
				if y[0] == 'player':
					#PLAYER
					p = 0
					for i in self.player:
						if y[1] == p:
							if self.rectdebug: pygame.draw.rect(self.display[0], (0,0,255), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
							doll = self.people(i,True)
							#CONDITIONS
							if res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HEALTH'] > 1:
								if i['SHK'] == 0:
									pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								else: pygame.draw.rect(self.display[0], (255,10,10), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HEALTH']) + '.png'), (i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40))
							if self.map.properties['HSCROLL'] != 0 and i['RECT'].x < self.cam.x - self.map.tilewidth: res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] = 0
							if self.map.properties['VSCROLL'] != 0 and i['RECT'].y < self.cam.y - self.map.tileheight: res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] = 0
							#MIRROR SURFACES
							for t in self.tilrect[5]:
								doll = pygame.transform.flip(doll,False,True)
								self.display[0].blit(doll,(t[1].x + i['RECT'].x - (self.cam.x * 2),t[1].y + i['RECT'].y - (self.cam.y * 2)))
							#TILE COLISION
							for tl in range(2):
								if i['STEP'] > 0: i['STEP'] -= 1
								ind = (math.floor((i['RECT'].y + 15)/self.map.tileheight) * self.map.width) + math.floor((i['RECT'].x + 15)/self.map.tilewidth)
								t = self.tilrect[tl][ind]
								if t != None:
									if self.rectdebug:
										if tl == 0: pygame.draw.rect(self.display[0],(255,255,0),pygame.Rect(t[1].x + 2 - self.cam.x,t[1].y + 2 - self.cam.y,t[1].width - 4,t[1].height - 4),3)
									if i['PAUSE'] == 0:
										#PROPS COLISION
										if i['DRIVING'] == None:
											#TREADMILL
											if t[0]['TYPE'] == 'TREADMILL' and self.colide(i['RECT'],t[1]):
												if t[0]['DIRECTION'] == 1: i['RECT'].x += 2
												if t[0]['DIRECTION'] == 3: i['RECT'].y += 2
												if t[0]['DIRECTION'] == 5: i['RECT'].x -= 2
												if t[0]['DIRECTION'] == 7: i['RECT'].y -= 2
											#MOVING
											elif t[0]['TYPE'] == 'MOVING' and self.colide(i['RECT'],t[1]):
												i['RECT'].x += abs(i['RECT'].x - t[1].x)
												i['RECT'].y += abs(i['RECT'].y - t[1].y)
												self.soundplay('STEP_METAL')
											#SPIKE
											elif t[0]['TYPE'] == 'SPIKE' and self.colide(i['RECT'],t[1]):
												do = False
												if t[0]['WAIT'] == 0: do = True
												elif int(t[0]['GIF']) > 0: do = True
												if do:
													if res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] > 0:
														res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] -= 5
														self.ch_ton.play(res.SOUND['BATTLE_LOST'])
														self.player[p]['INVFRM'] = 60
														while self.sttsy < 120:
															self.sttsy += 10
															self.run()
													else:
														self.ch_ton.play(res.SOUND['GAME_OVER'])
											#JUMP
											elif t[0]['TYPE'] == 'JUMP' and i['GRAVITY'] == -5:
												if t[0]['DIRECTION'] == 0: i['GIF'] = 1; do = True
												elif i['DIRECTION'] == int(t[0]['DIRECTION']): do = True
												else: do = False
												if do:
													i['GRAVITY'] = 4.5 + float(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ACROBATICS']/2)
													i['STEP'] = 0
													self.ch_sfx.play(res.SOUND['FALL'])
											#HOLE
											elif t[0]['TYPE'] == 'HOLE' and self.colide(i['RECT'],t[1]):
												res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] = 0
											#SLIME
											elif t[0]['TYPE'] == 'SLIME' and self.colide(i['RECT'],t[1]): i['ACC'] = 0.5
											else: i['ACC'] = 0
										if i['DRIVING'] == None and i['SPEED'] > 0:
											#STEP SOUNDS
											if t[0]['TYPE'] not in ['NONE','BACKGROUND','SKY','CLOTH','JUMP','SPIKE','HOLE','SLIME','TUNNEL'] and i['JUMP'] == 0:
												if i['STEP'] == 0 and res.MAP != 'rodoviary':
													#STREET AND SIDEWALK
													if t[0]['TYPE'].startswith('STREET'): self.soundplay('STEP_STONE',0)
													elif t[0]['TYPE'].startswith('SIDEWALK'): self.soundplay('STEP_BRICK',0)
													#COLOR TILES
													elif t[0]['TYPE'] == 'COLOR':
														if t[0]['SCALE'] == 30 and t[0]['COLOR'] > 0:
															self.dmg.append({'INFO': pygame.Surface((43,40), pygame.SRCALPHA, 32), 'TYPE': 0,
															'TEXT': '10','RECT': pygame.Rect(i['RECT'].x, i['RECT'].y,1,1),
															'GRAVITY': -8, 'SHADE': 1, 'SHAKE': 0, 'COLOR': (200,200,200), 'ALPHA': 250, 'TIME': 10})
															i['SCORE'] += 10
															t[0]['COLOR'] -= 1
															t[0]['SCALE'] = 0
															#self.audioedit(res.SOUND['STEP_COLOR'],'pitch',t[0]['COLOR'])
															self.soundplay('STEP_COLOR',0)
														else: self.soundplay('STEP_BRICK',0)
													#PROPS SOUND
													elif t[0]['TYPE'] in ['TREADMILL','MOVING']:
														self.soundplay('STEP_METAL',0)
													#REGULAR SOUND
													elif t[0]['TYPE'] != 'WALL':
														self.soundplay('STEP_' + t[0]['TYPE'],0)
													if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
												#SWIMMING
												if t[0]['TYPE'] == 'WATER':
													if i['SWIM'] == None: i['SWIM'] = 0.0
												else: i['SWIM'] = None
										#DRIVING
										elif i['DRIVING'] != None and t[0]['TYPE'] != 'WALL' and t[0]['TYPE'].startswith('JUMP') == False and i['JUMP'] == 0:
											if i['STEP'] == 0 and res.MAP != 'rodoviary':
												self.soundplay('STEP_MOTOR',0)
												if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
							y[2] = i['RECT'].y
						p += 1
				#ENEMIES
				if y[0] == 'enemy':
					for i in self.enemies:
						if i['N'] == y[1]: self.enemy(i); y[2] = i['RECT'].y
				#NPCS
				elif y[0] == 'npc':
					for i in self.npcs:
						if i['N'] == y[1]: self.npc(i); y[2] = i['RECT'].y
				#VEHICLES
				elif y[0] == 'vehicle':
					for i in self.vehicles:
						if i['N'] == y[1]: self.vehicle(i); y[2] = i['RECT'].y
				#PORTALS
				elif y[0] == 'portal': self.portal(y[1]); y[2] = y[1]['RECT'].y
				#SIGNS
				elif y[0] == 'sign':
					if self.colide(y[1]['RECT'],cm) and self.turn != -6:
						if res.MAP != 'rodoviary':
							sz = self.fnt['DEFAULT'].size(dtb.SIGNS[y[1]['TEXT']])
							pygame.draw.rect(self.display[0], (250, 250, 250), pygame.Rect(y[1]['RECT'].x - self.cam.x, y[1]['RECT'].y - self.cam.y, math.floor(sz[0]/2) + 10, math.floor(sz[1]/2) + 10))
							self.display[1].blit(self.fnt['DEFAULT'].render(dtb.SIGNS[y[1]['TEXT']], True, (0,0,0)), ((5 + y[1]['RECT'].x - self.cam.x) * res.GSCALE,(5 + y[1]['RECT'].y - self.cam.y) * res.GSCALE))
						else: self.display[1].blit(self.fnt['DEFAULT'].render(y[1]['TEXT'], True, (250,250,250)), ((y[1]['RECT'].x - self.cam.x - math.floor(self.cam.x/5)) * res.GSCALE,(y[1]['RECT'].y - self.cam.y - math.floor(self.cam.y/5)) * res.GSCALE))
					y[2] = y[1]['RECT'].y
				#ITEMS
				elif y[0] == 'item':
					if self.colide(y[1]['RECT'],cm):
						if y[1]['DIRECTION'] == False:
							y[1]['ACC'] -= 1
							if y[1]['ACC'] < -3: y[1]['DIRECTION'] = True
						if y[1]['DIRECTION']:
							y[1]['ACC'] += 1
							if y[1]['ACC'] > 3: y[1]['DIRECTION'] = False
						y[1]['FLOAT'] += int(y[1]['ACC'])
						self.display[0].blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y + y[1]['FLOAT']))
						for p in range(len(self.player)):
							if self.colide(self.player[p]['RECT'],y[1]['RECT']):
								if y[1]['ITEM'].startswith('bomb'):
									res.INVENTORY[res.PARTY[res.FORMATION][p]][4][1][0] = y[1]['ITEM']
									res.INVENTORY[res.PARTY[res.FORMATION][p]][4][1][1] = '3'
								elif y[1]['ITEM'].startswith('pow_bubble'):
									res.INVENTORY[res.PARTY[res.FORMATION][p]][4][2][0] = y[1]['ITEM']
									res.INVENTORY[res.PARTY[res.FORMATION][p]][4][2][1] = '3'
								else: self.inv.add(res.PARTY[res.FORMATION][0],y[1]['ITEM'])
								self.ch_sfx.play(res.SOUND['ITEM_GET'])
								self.particles.append({'TYPE': 'pop','GIF': 0.0,'X': y[1]['RECT'].x,'Y': y[1]['RECT'].y})
								y[1]['DESTROY'] = True
					y[2] = y[1]['RECT'].y
				#MOVE
				elif y[0] == 'move':
					if self.colide(y[1]['RECT'],cm):
						self.display[0].blit(y[1]['IMAGE'],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - self.map.tileheight))
						if self.rectdebug: pygame.draw.rect(self.display[0], (0,0,255), pygame.Rect(y[1]['RECT'].x - self.cam.x, y[1]['RECT'].y - self.cam.y, y[1]['RECT'].width, y[1]['RECT'].height),3)
						if y[1]['DIRECTION'] in [8,1,2]: y[1]['RECT'].x += y[1]['SPEED']
						if y[1]['DIRECTION'] in [2,3,4]: y[1]['RECT'].y += y[1]['SPEED']
						if y[1]['DIRECTION'] in [4,5,6]: y[1]['RECT'].x -= y[1]['SPEED']
						if y[1]['DIRECTION'] in [6,7,8]: y[1]['RECT'].y -= y[1]['SPEED']
						y[1]['DIRECTION'] = 0
						y[1]['SPEED'] = 0
						for p in self.player:
							if self.colide(p['RECT'],y[1]['RECT']) and p['PLAYING']:
								if y[1]['TYPE'] == 'CARRY':
									y[1]['DIRECTION'] = p['DIRECTION']
									y[1]['SPEED'] = p['SPEED']
					y[2] = y[1]['RECT'].y
				#TOLLS
				elif y[0] == 'toll':
					if self.colide(y[1]['RECT'],cm):
						srf = pygame.Surface((44,44), pygame.SRCALPHA)
						trs = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'toll.png'),y[1]['ANGLE'] + 90)
						#i['CENTER'] = trs.get_rect(center = i['CENTER'].center)
						srf.blit(trs,(0,0))
						self.display[0].blit(srf,(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y))
						if y[1]['TIME'] > 0: y[1]['TIME'] -= 1
						if self.colide(self.player[0]['RECT'],y[1]['RECT']):
							if y[1]['TIME'] == 0:
								mny = self.inv.find(None,'credit_card','value')
								if mny != None and mny[1] >= 10:
									self.ch_sfx.play(res.SOUND['BUY'])
									mny[1] -= 10
									y[1]['TIME'] = 180
									self.notification.append({'TEXT': 'Pedágio -$ 10', 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
								elif self.facing(self.player[0],y[1]['RECT']) == 2:
									self.player[0]['SPEED'] = 0
					y[2] = y[1]['RECT'].y
				#RADARS
				elif y[0] == 'radar':
					if self.colide(y[1]['RECT'],cm):
						if self.colide(self.player[0]['RECT'],y[1]['RECT']):
							for j in self.objects:
								if j[0] == 5 and j[1]['TEXT'] == 'radar' + str(0):
									j[1]['TEXT'] = self.player[0]['SPEED']
							if self.player[0]['SPEED'] > y[1]['LIMIT']:
								self.ch_sfx.play(res.SOUND['BUY'])
								mny = self.inv.find(None,'credit_card','value')
								if mny != None: mny[1] -= 10
					y[2] = y[1]['RECT'].y
				#TENTS
				elif y[0] == 'tent':
					if self.colide(y[1]['RECT'],cm):
						self.display[0].blit(y[1]['SPRITE'],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - 20))
						for p in self.player:
							if self.colide(p['RECT'],y[1]['RECT']):
								 self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (y[1]['RECT'].x - self.cam.x + int(y[1]['RECT'].width/2) - 5,y[1]['RECT'].y - self.cam.y - y[1]['RECT'].height * 2))
								 if self.pressed[4][0]: p['SLEEP'] = not p['SLEEP']
					y[2] = y[1]['RECT'].y
				#PETS
				elif y[0] == 'pet':
					if self.colide(y[1]['RECT'],cm): self.pet(y[1]); y[2] = y[1]['RECT'].y
				#TILES
				elif y[0] == 11:
					self.display[0].blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y)); y[2] = y[1]['RECT'].y
				#CLICK
				elif y[0] == 'click':
					y[1]['GIF'] += 0.1
					if math.floor(y[1]['GIF']) >= len(y[1]['IMAGE']):
						y[1]['GIF'] = 0
					self.display[0].blit(y[1]['IMAGE'][math.floor(y[1]['GIF'])],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - 20))
					if self.colide(self.player[0]['RECT'],y[1]['RECT']): y[1]['DESTROY'] = True
					y[2] = y[1]['RECT'].y
			#BUILD ITEMS
			if self.build != '':
				srf = pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')
				srf.set_alpha(100)
				self.display[0].blit(srf,((math.floor((self.player[0]['RECT'].x + 15)/30) * 30) - self.cam.x,(math.floor((self.player[0]['RECT'].y + 15)/30) * 30) - self.cam.y - 20))
			#NODES DEBUG
			if self.rectdebug:
				for i in self.nodes: pygame.draw.rect(self.display[0], (250,250,10),pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			#OVER TILES & CLOUDS
			if res.MAP != 'rodoviary':
				if self.turn != -6 and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] != 12:
					if len(self.tilmap[2]) > 0: self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
			else:
				self.bbg['X'] += 0.2
				if math.floor(self.bbg['X']) > (self.map.width * self.map.tilewidth): self.bbg['X'] = 0.0
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbg['X']) - self.cam.x, -self.cam.y))
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbg['X']) - (self.map.width * self.map.tilewidth) - self.cam.x, -self.cam.y))
			'''for t in self.tilrect[4 + math.floor(self.tilemation)]:
				if self.colide(t[1],self.cam): self.display[0].blit(t[2], (t[1].x - self.cam.x, t[1].y - self.cam.y))'''
			#DAYTIME & WEATHER
			if res.TIME[0] >= 18: tim = 100
			elif res.TIME[0] >= 6: tim = 0
			else: tim = 100
			srf = pygame.Surface((self.displayzw,self.displayzh))
			srf.set_alpha(tim)
			srf.fill((0, 58, 160))
			#LIGHTS
			for y in self.objects:
				if y[0] == 'light':
					if self.colide(y[1]['RECT'], self.cam):
						srf.blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y),None,pygame.BLEND_RGBA_SUB)
			if self.map.properties['INTERIOR'] == 0: self.display[0].blit(srf, (0,0))
			#RAIN
			if self.map.properties['INTERIOR'] == 0 and res.WEATHER == 1 and res.MAP != 'rodoviary':
				if len(self.particles) < 100:
					for i in range(5):
						img = pygame.Surface((2,2),pygame.SRCALPHA)
						pygame.draw.circle(img,(0, 148, 255),(1,1),2)
						img.set_alpha(120)
						self.particles.append({'IMAGE': img,'TYPE': 'raindrop', 'X': round(random.randint(0,self.cam.width + int(self.cam.width/4))), 'Y': -int(self.cam.height/2),
							'RADIUS': 2, 'DIRECTION': 90, 'SPEED': 15, 'TIME': round(random.randint(10,60)), 'GIF': 0})
			#PARTICLES
			p = 0
			while p < len(self.particles):
				ptc = self.particles[p]
				if ptc['TYPE'] == 'pop' and ptc['GIF'] >= 8: del self.particles[p]; p -= 1
				if ptc['TYPE'] == 'bomb' and int(ptc['GIF']) >= len(ptc['IMAGE']):
					#DESTROY BRICKS
					if ptc['POWER'] == 0:
						for obj in self.objects:
							if obj[0] == 'move' and obj[1]['TYPE'] == 'DESTROY':
								if self.colide(obj[1]['RECT'], pygame.Rect(ptc['X'] - int((self.map.tilewidth * 3)/2),ptc['Y'] - int((self.map.tileheight * 3)/2),self.map.tilewidth * 3,self.map.tileheight * 3)):
									prb = random.randint(0,30)
									if prb > 20:
										pit = random.randint(0,100)
										if pit > 90: it = 'pow_speed'
										elif pit > 80: it = 'pow_speed'
										elif pit > 40: it = 'pow_bubble'
										else: it = 'bomb_regular'
										img = pygame.image.load(res.ITEMS_PATH + it + '.png')
										self.objects.append(['item',{'IMAGE': img,'ITEM': it,'RECT': pygame.Rect(ptc['X'],ptc['Y'],img.get_width(),img.get_height()),
										'FLOAT': 0,'ACC': 3,'DIRECTION': False,'DESTROY': False},100])
									for i in range(10):
										self.particles.append({'TYPE': 'spin','IMAGE': pygame.image.load(res.SPRITES_PATH + 'brick.png'),'DIRECTION': random.randint(1,6),'SPIN': 0,'TIME': 0,'X': obj[1]['RECT'].x,'Y': obj[1]['RECT'].y})
									obj[1]['DESTROY'] = True
						self.particles.append({'TYPE': 'explode','GIF': 0.0,'TIME': 0,'X': ptc['X'],'Y': ptc['Y'],'LIMIT': 3})
						self.ch_ton.play(res.SOUND['EXPLOSION_' + str(random.randint(1,4))])
					if ptc['POWER'] == 1:
						rct = [{'TYPE': 'SLIME'},pygame.Rect(math.floor(ptc['X']/self.map.tilewidth) * self.map.tilewidth,math.floor(ptc['Y']/self.map.tileheight) * self.map.tileheight,self.map.tilewidth,self.map.tileheight)]
						self.tilrect[1][(math.floor((ptc['Y'] + 15)/self.map.tilewidth) * self.map.width) + math.floor((ptc['X'] + 15)/self.map.tilewidth)] = rct
					del self.particles[p]
				if ptc['TYPE'] == 'explode' and ptc['TIME'] >= 30: del self.particles[p]; p -= 1
				if ptc['TYPE'] == 'raindrop' and ptc['GIF'] > 8: del self.particles[p]; p -= 1
				if ptc['TYPE'] == 'blood' and ptc['RADIUS'] <= 0.0: del self.particles[p]; p -= 1
				if ptc['TYPE'] == 'gunshot' and ptc['DESTROY']: del self.particles[p]; p -= 1
				if ptc['TYPE'] == 'spin' and ptc['TIME'] >= 30: del self.particles[p]; p -= 1
				p += 1
			if len(self.particles) > 0:
				for p in self.particles: self.particle(p)
			#HIDE PLACES
			if self.tilhide == False and self.tilalpha > 0: self.tilalpha -= 20
			if self.tilhide and self.tilalpha < 255: self.tilalpha += 20
			if self.tilalpha < 0: self.tilalpha = 0
			if self.tilalpha > 255: self.tilalpha = 255
			al = 255 - self.tilalpha
			for i in self.tilrect[4]:
				srf = pygame.Surface((i[1].width,i[1].height))
				if i[0].endswith('ON') and al > 0: srf.set_alpha(al); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
				if i[0].endswith('OFF') and self.tilalpha > 0: srf.set_alpha(self.tilalpha); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
			#MINI MAP
			if self.dev != None and self.dev.img == 'GPS':
				try: self.display[0].blit(self.dev.map(True, self.player[0]), (0,self.displayzh - 106))
				except: pass
			#MAP COMPASS
			if len(res.MARKER) > 0 and res.MARKER[0][0] == res.MAP:
				xx = (self.player[0]['RECT'].x - self.cam.x) - (res.MARKER[0][1] - self.cam.x)
				yy = (self.player[0]['RECT'].y - self.cam.y) - (res.MARKER[0][2] - self.cam.y)
				dir = (xx,yy)
				lth = math.hypot(*dir)
				if lth == 0.0: dir = (0, -1)
				else: dir = (dir[0]/lth,dir[1]/lth)
				img = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'mp_compass.png'),(math.degrees((math.atan2(-dir[1],dir[0]))) + 90))
				try: self.mpcrct = img.get_rect(center = self.mpcrct.center)
				except: self.mpcrct = img.get_rect(center=pygame.Rect(self.displayzw - 70,20,50,50).center)
				self.display[0].blit(img,self.mpcrct)
				if self.colide(self.player[0]['RECT'],pygame.Rect(res.MARKER[0][1] - 40,res.MARKER[0][2] - 40,80,80)):
					del res.MARKER[0]
			#DRIVING BARS
			for p in self.player:
				if p['DRIVING'] != None:
					pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,20,100,20))
					if res.GAS >= 1: pygame.draw.rect(self.display[0], (255,155,66), pygame.Rect(20,20,int(100/(self.vehicles[p['DRIVING']]['CAPACITY']/round(res.GAS))),20))
					pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,42,100,20))
					if p['SPEED'] > 0: pygame.draw.rect(self.display[0], (0,255,0), pygame.Rect(20,42,int(100/(20/p['SPEED'])),20))
					self.hpctrl = dtb.HINTS['VEHICLE_CONTROLS']
			#BLACK BARS
			if self.winbar > 0:
				#MYSTERIOUS FREAK
				"""if self.turn == -6:
					srf = pygame.Surface((self.displayzw,self.displayzh),pygame.SRCALPHA)
					srf.fill((0,0,0))
					srf.blit(pygame.image.load(res.SPRITES_PATH + 'aim_mysterious.png'), (self.dlg['CAMERA'].x - self.cam.x - 30, self.dlg['CAMERA'].y - self.cam.y - 30),None,pygame.BLEND_RGBA_SUB)
					self.display[0].blit(srf,(0,0))"""
				#REGULAR BARS
				if self.transtype == 'bars':
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
				if self.transtype == 'hole':
					srf = pygame.Surface((self.displayzw,self.displayzh),pygame.SRCALPHA)
					srf.fill((0,0,0))
					img = pygame.image.load(res.SPRITES_PATH + 'aim_mysterious.png')
					sz = (int(img.get_width()/100) * self.winbar,int(img.get_height()/100) * self.winbar)
					img = pygame.transform.scale(img,(sz[0],sz[1]))
					srf.blit(img, (self.player[0]['RECT'].x - self.cam.x - int(img.get_width()/2), self.player[0]['RECT'].y - self.cam.y - int(img.get_height()/2)),None,pygame.BLEND_RGBA_SUB)
					self.display[0].blit(srf,(0,0))
				if self.transtype == 'side':
					if self.winbar < self.displayzw: pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.winbar,self.displayzh))
					else: pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(self.displayzw - self.winbar,0,self.winbar,self.displayzh))
				if self.transtype == 'image':
					srf = pygame.Surface((self.displayzw,self.displayzh),pygame.SRCALPHA)
					srf.fill((0,0,0))
					img = pygame.image.load(res.SPRITES_PATH + 'aim_mysterious.png')
					sz = (int(img.get_width()/100) * self.winbar,int(img.get_height()/100) * self.winbar)
					img = pygame.transform.scale(img,(sz[0],sz[1]))
					srf.blit(img, (self.dlg['CAMERA'].x - self.cam.x - int(img.get_width()/2), self.dlg['CAMERA'].y - self.cam.y - int(img.get_height()/2)),None,pygame.BLEND_RGBA_SUB)
					self.display[0].blit(srf,(0,0))
				if self.transtype == 'fade':
					srf = pygame.Surface((self.displayzw,self.displayzh),pygame.SRCALPHA)
					srf.fill((0,0,0))
					srf.set_alpha(self.winbar)
					self.display[0].blit(srf,(0,0))
			#RADIOPLAY
			if self.rad.onoff and self.turn != -6: self.display[1].blit(self.rad.display(),(0,0))
			#CITY NAME
			if self.cityname != '' and self.winbar >= 50: abl = True
			elif self.cityname != '' and self.turn == -6: abl = True
			else: abl = False
			if abl:
				sz = self.fnt['MININFO'].size(self.cityname)
				self.display[0].blit(self.fnt['MININFO'].render(self.cityname, True, (250,250,250)), (self.displayzw - sz[0] - 20, int(self.displayzh/2)))
			#PORTALGO
			if self.portalgo != {}:
				if self.rectdebug: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y, self.portalgo[0]['RECT'].width, self.portalgo[0]['RECT'].height))
				if self.portalgo[0]['RECT'].width == 24: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_01.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				if self.portalgo[0]['RECT'].width == 48: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_11.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				self.portalgo[1]['RECT'].x = self.portalgo[0]['RECT'].x + self.cam.x
				self.portalgo[1]['RECT'].y = self.portalgo[0]['RECT'].y + self.cam.y + 20
				self.people(self.portalgo[1],True)
				for i in self.objects:
					if i[0] == 4 and self.portalgo[0]['MATCH'] != None and i[1]['MATCH'] == self.portalgo[0]['MATCH']:
						self.cam.x += int((i[1]['RECT'].x  - self.cam.x - self.displayzw/2)/15)
						self.cam.y += int((i[1]['RECT'].y  - self.cam.y - self.displayzh/2)/15)
						chk = 0
						if i[1]['RECT'].x - self.cam.x < self.portalgo[0]['RECT'].x:
							self.portalgo[0]['RECT'].x -= 10
							if i[1]['RECT'].x - self.cam.x >= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif i[1]['RECT'].x - self.cam.x > self.portalgo[0]['RECT'].x and chk == 0:
							self.portalgo[0]['RECT'].x += 10
							if i[1]['RECT'].x - self.cam.x <= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif chk == 0: chk += 1
						if i[1]['RECT'].y - self.cam.y < self.portalgo[0]['RECT'].y:
							self.portalgo[0]['RECT'].y -= 10
							if i[1]['RECT'].y - self.cam.y >= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif i[1]['RECT'].y - self.cam.y > self.portalgo[0]['RECT'].y and chk != 2:
							self.portalgo[0]['RECT'].y += 10
							if i[1]['RECT'].y - self.cam.y <= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif chk == 1: chk += 1

						if chk == 2: self.portalgo[0]['MATCH'] = None
						#if self.colide(self.portalgo['RECT'],i['RECT']):
						#	self.portalgo['MATCH'] = None
		#HEALTH DAMAGE
		u = 0
		dth = 0
		for i in res.PARTY[res.FORMATION]:
			if res.CHARACTERS[i]['HEALTH'] in [4,5,6,7,16,17,18,19,20,21]:
				self.player[u]['DMGTIM'] -= 1
				if self.player[u]['DMGTIM'] == 0:
					self.player[u]['DMGTIM'] = 100
					self.player[u]['SHK'] = 3
					res.CHARACTERS[i]['HP'] -= 1
					if res.CHARACTERS[i]['HEALTH'] == 17:
						chc = round(random.randint(0,100))
						if chc > 70: res.CHARACTERS[i]['HEALTH'] = 0
				if self.player[u]['SHK'] > 0: self.player[u]['SHK'] = -self.player[u]['SHK']
				elif self.player[u]['SHK'] < 0: self.player[u]['SHK'] = -self.player[u]['SHK'] - 1
			if res.CHARACTERS[i]['HP'] <= 0: dth += 1
			elif res.CHARACTERS[i]['HEALTH'] in [8,13,14,15]: dth += 1
			u += 1
		#GAME OVER
		if dth == len(res.PARTY[res.FORMATION]) and self.turn != -5:
			if self.rad.onoff: pygame.mixer.music.stop(); self.rad.onoff = False
			self.ch_msc.fadeout(500)
			pygame.mixer.music.fadeout(500)
			self.ch_ton.play(res.SOUND['BATTLE_LOST'])
			while self.sttsy > 120:
				self.sttsy -= 10
				self.run(False)
			self.transiction(True, 100)
			self.battle = True
			self.obstacles = False
			self.turn = -5
			self.bbg['X'] = 0
			self.mnu = self.displayzw
			acc = 60
			while self.mnu > 0:
				self.mnu -= acc
				acc -= 2
				self.run(False)
			self.turn = -5
			self.wait()
			res.MAP = 'hospital_0'
			res.PX = 315
			res.PY = 200
			mny = self.inv.find(None,'credit_card','value')
			if mny != None:
				for i in res.PARTY[res.FORMATION]:
					mny[1] -= 100
				for i in res.PARTY[res.FORMATION]:
					res.CHARACTERS[i]['HP'] = dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
					res.CHARACTERS[i]['HEALTH'] = 0
			self.__init__()
			if res.CHAPTER > 0: self.loadmap(res.MAP)
			self.transiction(False, 0)
		#BATTLE
		if self.battle:
			#BACKGROUND
			yy = -(int(res.GSCALE/3) * 10)
			if self.turn == -4:
				self.display[0].blit(self.bbg['IMAGE'], (self.bbg['X'], yy))
				self.display[0].blit(self.bbg['IMAGE'], (self.bbg['X'] - 600, yy))
				if self.displayzw > 600:
					self.display[0].blit(self.bbg['IMAGE'], (self.bbg['X'] + 600, yy))
				self.bbg['X'] += 5
				if self.bbg['X'] > 600: self.bbg['X'] = 0
			elif self.bbg['IMAGE'] != None:
				self.display[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5), yy))
				if self.displayzw > 595:
					self.display[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5) + 600, yy))
				if self.obstacles:
					self.display[0].blit(self.bbg['IMAGE'], (int(self.bbg['X'] * 0.5) - 600, yy))
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
					self.bbg['X'] += self.bbg['ACC']
			#FOES
			foelst = []
			maxhgt = 0
			count = 0
			oldlst = self.foe + self.mrc
			oldsiz = len(oldlst)
			while len(foelst) < oldsiz:
				count = 0
				maxhgt = 0
				for i in oldlst:
					if float(i['HEIGHT'].replace(',','.')) > maxhgt:
						maxhgt = count
					count += 1
				foelst.append(oldlst[maxhgt])
				del oldlst[maxhgt]
			count = 0
			for i in foelst[::-1]:
				if count == 5: break
				self.enemy(i)
				count += 1
			#SKIP PLAYER & BLINDNESS
			if self.mnu < 3 and self.turn >= 0 and self.turn < len(self.fig):
				if self.fig[self.turn]['HEALTH'] == 12: self.display[0].fill((0,0,0))
				if self.fig[self.turn]['HP'] <= 0: self.turn += 1
				elif self.fig[self.turn]['HEALTH'] in [8,13,14,15]: self.turn += 1
				if self.turn >= len(self.fig):
					if res.BTYPE == 1: self.fight()
					else: self.turn = 0
			#BLACK BARS
			if self.windoww > self.windowh: wbrh = self.winbar - 10
			else: wbrh = self.winbar * 2
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - wbrh,self.displayzw,wbrh))
		#STATUS
		if self.sttsy > 0:
			upsts = pygame.Surface((self.displayzw,100))
			if res.GSCALE < 3: dwyy = 38
			else: dwyy = 18
			#ENEMIES COUNT
			if self.battle and self.winbar <= 100 and self.turn != -4:
				ce = 0
				if len(self.mrc) == 0:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (self.displayzw - 100, int(self.winbar/2) - 15))
				else:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (self.displayzw - 100, 15))
					ce = 0
					for i in self.mrc:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.mrc)), True, (255,255,255)), (self.displayzw - 100, 50))
			#PLAYERS BARS
			p = 0
			low = 0
			while p < len(res.PARTY[res.FORMATION]):
				#NAME
				if self.battle == False: ctr = res.PARTY[res.FORMATION][p]
				else: ctr = res.PARTY[res.FORMATION][self.fig[p]['N']]
				if p == self.turn:
					pygame.draw.rect(upsts, (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(p * 120,0,120,100))
					upsts.blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, (0,0,0)), (10 + p * 120, 10))
				else: 
					upsts.blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (10 + p * 120, 10))
				#VITALITY GRAY
				pygame.draw.rect(upsts, (10, 10, 10), pygame.Rect(10 + p * 120,40,100,20))
				col = (255,255,0)
				if res.CHARACTERS[ctr]['HP'] > 0:
					minush = int(98/(dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]/res.CHARACTERS[ctr]['HP']))
				if res.CHARACTERS[ctr]['HP'] < 0:
					minush = int(98/(10/abs(res.CHARACTERS[ctr]['HP'])))
					col = (random.randint(100,255), 10, 10)
					low = 2
				else: minush = 0
				if self.barhp[p] > minush:
					self.ch_sfx.play(res.SOUND['HP_LOSS'])
					self.barhp[p] -= 1
				pygame.draw.rect(upsts, (50, 50, 50), pygame.Rect(11 + p * 120, 41,98,18))
				if self.barhp[p] > 0: pygame.draw.rect(upsts, col, pygame.Rect(11 + p * 120, 41,self.barhp[p],18))
				#LIFE BAR
				limit = dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]
				if self.equip[p] == 6 and self.turn > p: hpcol = (100, 100, 100)
				elif res.CHARACTERS[ctr]['HP'] > dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]/5: hpcol = (10, 250, 10)
				elif res.CHARACTERS[ctr]['HP'] > 0:
					hpcol = (250, 10, 10)
					low = 1
				else: hpcol = (250, 10, 10)
				if res.CHARACTERS[ctr]['HP'] > 0:
					pygame.draw.rect(upsts, hpcol, pygame.Rect(11 + p * 120, 41,int(98/(limit/abs(res.CHARACTERS[ctr]['HP']))),18))
				if low == 1:
					if self.ch_ton.get_busy() == False: self.ch_ton.play(res.SOUND['HP_LOW'])
				if low == 2:
					if self.ch_ton.get_busy() == False: self.ch_ton.play(res.SOUND['DYING'])
				#CONDITION ICON
				if res.CHARACTERS[ctr]['HEALTH'] > 1:
					upsts.blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[ctr]['HEALTH']) + '.png'), (14 + (p * 120), 44))
				#AMMO BAR
				if self.equip[p] < 4:
					pygame.draw.rect(upsts, (10, 10, 10), pygame.Rect(10 + p * 120, 70,100,20))
					barehands = False
					if res.INVENTORY[ctr][4][self.equip[p] + 1][0] != '_':
						if int(res.INVENTORY[ctr][4][self.equip[p] + 1][1]) > 0:
							try: minush = int(98/(dtb.ITEMS[res.INVENTORY[ctr][4][self.equip[p] + 1][0]][5]['CAPACITY']/int(res.INVENTORY[ctr][4][self.equip[p] + 1][1])))
							except: minush = 0
						else: minush = 0
					
						if self.barpp[p][self.equip[p]] > minush:
							self.barpp[p][self.equip[p]] -= 1
						if self.barpp[p][self.equip[p]] > 0:
							pygame.draw.rect(upsts, (0, 100, 250), pygame.Rect(11 + p * 120, 71,self.barpp[p][self.equip[p]],18))
					else: barehands = True
					#STAMINA
					if res.BTYPE == 2:
						if self.fig[p]['STAMINA'][self.equip[p]] < 100:
							stcol = (100,100,250)
							if self.turn != p:
								if barehands: stadd = 1
								else: stadd = dtb.ITEMS[res.INVENTORY[ctr][4][self.equip[p] + 1][0]][5]['RECHARGE']
								self.fig[p]['STAMINA'][self.equip[p]] += stadd
								if self.fig[p]['STAMINA'][self.equip[p]] == 100: self.ch_sfx.play(res.SOUND['READY'])
						if self.fig[p]['STAMINA'][self.equip[p]] >= 100:
							self.fig[p]['STAMINA'][self.equip[p]] = 100
							stcol = (10,250,250)
						if barehands: dv = 100
						else: dv = self.barpp[p][self.equip[p]]
						if dv > 0 and self.fig[p]['STAMINA'][self.equip[p]]:
							pygame.draw.rect(upsts,stcol, pygame.Rect(11 + p * 120, 71,int(dv/(100/self.fig[p]['STAMINA'][self.equip[p]])),18))
				p += 1
			if res.GSCALE < 3: self.display[0].blit(upsts,(0,self.sttsy - 120))
			else: self.display[0].blit(pygame.transform.scale(upsts,(upsts.get_rect().width - (int(upsts.get_rect().width/10) * 4),60)),(0,int((self.sttsy - 120)/2)))
			#ACTIONS
			if self.battle:
				if self.turn < len(res.PARTY[res.FORMATION]) and self.turn >= 0:
					itind = res.PARTY[res.FORMATION][self.fig[self.turn]['N']]
					#TIME BAR:
					if self.btime > 0:
						pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,self.displayzh - wbrh,int(self.displayzw/(100/self.btime)),5))
					if self.mnu < 3 and self.turn < len(self.fig): self.btime -= 0.5
					if self.btime == 0:
						self.turn = len(self.fig)
						self.mnu = 1
						self.fight()
					#OPTIONS
					if self.mnu == 1:
						x = 0
						if self.displayzw < self.displayzh: brdx = (35 * 4) + 46
						else: brdx = (35 * 9) + 46
						brdx = int(self.displayzw/2) - int(brdx/2)
						for i in res.INVENTORY[itind][4][1:]:
							if self.equip[self.fig[self.turn]['N']] == x: pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + (x * 35),(self.displayzh + dwyy) - wbrh,30,30))
							else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(brdx + (x * 35),(self.displayzh + dwyy) - wbrh,30,30))
							if res.INVENTORY[itind][4][x + 1][0] != '_':
								self.display[0].blit(self.inv.itimg(res.INVENTORY[itind][4][x + 1][0]), (brdx + 2 + (x * 35), (self.displayzh + dwyy) - wbrh))
							x += 1
						if wbrh == self.winbar * 2: wbrh -= 35
						if self.displayzw < self.displayzh: brdx -= (35 * 4) + 46
						if self.equip[self.fig[self.turn]['N']] == 4:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 186,(self.displayzh + dwyy) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_TACTICS']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 186,(self.displayzh + dwyy) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_tactical.png'), (brdx + 186, (self.displayzh + dwyy) - wbrh))
						if self.equip[self.fig[self.turn]['N']] == 5:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 221,(self.displayzh + dwyy) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_DIALOG']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 221,(self.displayzh + dwyy) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_talk.png'), (brdx + 221, (self.displayzh + dwyy) - wbrh))
						if self.equip[self.fig[self.turn]['N']] == 6:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 256,(self.displayzh + dwyy) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_GUARD']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 256,(self.displayzh + dwyy) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_guard.png'), (brdx + 256, (self.displayzh + dwyy) - wbrh))
						if self.equip[self.fig[self.turn]['N']] == 7:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 291,(self.displayzh + dwyy) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_RUN']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 291,(self.displayzh + dwyy) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_run.png'), (brdx + 291, (self.displayzh + dwyy) - wbrh))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_invphn.png'), (brdx + 324, (self.displayzh + dwyy) - wbrh))
					#AIM BAR
					elif self.mnu == 2:
						if self.equip[self.fig[self.turn]['N']] < 4:
							if res.CHARACTERS[itind]['HEALTH'] == 9:
								prb = random.randint(0,10)
								if prb > 5: self.aim.x += round(random.randint(30,60))
								if prb < 5: self.aim.x -= round(random.randint(30,60))
							#else: self.aim.x += 20 - self.fig[self.turn]['AGILITY']
							if self.aim.x > (self.displayzw - int(self.displayzw/6)):
								self.aim.x = int(self.displayzw/6)
							chk = False
							for i in res.INVENTORY[itind][4][self.equip[self.fig[self.turn]['N']] + 1][1:]:
								if isinstance(i,str) and i.startswith('aim'): chk = True; break
							if chk: str(dtb.ITEMS[i][5])
							else: img = '0'
							self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'aim_' + img + '.png'), (self.aim.x - 15, self.aim.y))
							#self.display[0].blit(pygame.image.load(res.SPRITES_PATH + '' + res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0] + '.png'), (150 + int(self.aim.x/2), 255))
							self.hpctrl = dtb.HINTS['BATTLE_SHOT']
						#TACTICS
						elif self.equip[self.fig[self.turn]['N']] == 4:
							x = 0
							for i in res.TACTICAL:
								if self.opt == x: pygame.draw.rect(self.display[0], (255, 0, 0), pygame.Rect(118 + x * 35,338,30,30))
								else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(118 + x * 35,338,30,30))
								x += 1
			#ATTACKIMATION
			if self.banimation['INDEX'] != None:
				srf = pygame.Surface((self.displayzw,self.displayzh))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.display[0].blit(srf, (0,0))
				img = res.SPRITES['ATTACKIMATION_' + str(self.banimation['INDEX'])][math.floor(self.banimation['GIF'])]
				sz = img.get_rect()
				self.display[0].blit(img, (int(self.displayzw/2) - int(sz.width/2),int(self.displayzh/2) - int(sz.height/2)))
			#DICES
			if self.dices != []:
				y = 0
				for i in self.dices:
					if i[0] != -1:
						pygame.draw.rect(self.display[0],(res.COLOR[0],res.COLOR[1],res.COLOR[2]),pygame.Rect(int(self.displayzw/2) - (30 * len(self.dices)) + (y * 80),int(self.displayzh/2) - 30,60,60))
						self.display[0].blit(self.fnt['MININFO'].render(str(i[0]),True,(10,10,10)),(int(self.displayzw/2) - (30 * len(self.dices)) + (y * 80) + 15,int(self.displayzh/2) - 15))
					y += 1
			#GRADIENT
			'''for i in range(len(self.grd)):
				self.display[1].blit(self.grd[i],(0,i))
				self.display[1].blit(self.grd[i],(0,self.windowh - i))'''
			#WIN SCREEN
			if self.winbar >= 100:
				if self.turn == -4:
					pd = 200 - (50 * res.GSCALE)
					#LABEL
					if self.hpl < 0: self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[6], True, (255,255,255)), (pd + 30 + self.mnu, pd - 30))
					else: self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[7], True, (255,255,255)), (pd + 30 + self.mnu, pd - 30))
					#GREENBLOOD
					for it in ['tube100','tube250']:
						btls = self.inv.find(None,it,'value')
						if btls != None and btls[1] >= dtb.ITEMS[res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]][5]: btls = None
					if btls != None:
						it = res.INVENTORY[btls[0][0]][btls[0][1]][btls[0][2]][btls[0][3]]
						if btls[1] > 0 and int(200/(dtb.ITEMS[it][5]/btls[1])) >= 1:
							pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(pd + 40 - self.mnu,300 - int(200/(dtb.ITEMS[it][5]/btls[1])),30,int(200/(dtb.ITEMS[it][5]/btls[1]))))
							if int(btls[1]) < 90:
								pygame.draw.ellipse(self.display[0], (32, 219, 166), pygame.Rect(pd + 40 - self.mnu,291 - int(200/(dtb.ITEMS[it][5]/btls[1])),30,13))
							pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(self.displayzw - pd + self.mnu,280 - int(200/(dtb.ITEMS[it][5]/btls[1])),50,20))
							self.display[1].blit(self.fnt['DEFAULT'].render(str(btls[1]) + 'ml', True, (0,0,0)), ((self.displayzw - (5 + pd) + self.mnu) * res.GSCALE, (285 - int(200/(dtb.ITEMS[it][5]/int(btls[1])))) * res.GSCALE))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'gbbar.png'), (pd + 40, pd + 20))
					#PARTY XP
					for i in range(len(res.PARTY[res.FORMATION])):
						if self.mnu > 0: mvx = self.mnu
						else: mvx = 0
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][i]) + '.png'), (pd + mvx, pd + 20 + (i * 30)))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(pd + 30 + mvx,pd + 20 + (i * 30),100,20))
						if self.barxp[i] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(pd + 30 + mvx,pd + 20 + (i * 30),self.barxp[i],20))
					#LEVEL UP
					bw = (self.displayzw * 2) - pd
					ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.exvar]]
					if ch['LEVEL'] > 0:
						#self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[39] + ' +' + str(ch['STRENGHT'][ch['LEVEL']] - ch['STRENGHT'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 260))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + self.mnu,120,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(bw + self.mnu,120,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL']] + ch['BONUS'][0]))),15))
						if dtb.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(bw + self.mnu,120,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL'] - 1] + ch['BONUS'][0]))),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[40] + ' +' + str(ch['ATTACK'][ch['LEVEL']] - ch['ATTACK'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 290))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + self.mnu,145,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(bw + self.mnu,145,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']] + ch['BONUS'][1]))),15))
						if dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(bw + self.mnu,145,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL'] - 1] + ch['BONUS'][1]))),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[41] + ' +' + str(ch['AGILITY'][ch['LEVEL']] - ch['AGILITY'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 320))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + self.mnu,170,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(bw + self.mnu,170,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL']] + ch['BONUS'][2]))),15))
						if dtb.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(bw + self.mnu,170,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL'] - 1] + ch['BONUS'][2]))),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[42] + ' +' + str(ch['RESISTANCE'][ch['LEVEL']] - ch['RESISTANCE'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 350))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + self.mnu,195,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(bw + self.mnu,195,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['KNOWLEDGE'][ch['LEVEL']] + ch['BONUS'][3]))),15))
						if dtb.CLASSES[ch['CLASS']]['KNOWLEDGE'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(bw + self.mnu,195,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['KNOWLEDGE'][ch['LEVEL'] - 1] + ch['BONUS'][3]))),15))
						#self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[43] + ' +' + str(ch['RESISTANCE'][ch['LEVEL']] - ch['RESISTANCE'][ch['LEVEL'] - 1]), True, (255,255,255)), ((1000 + self.mnu) * 2, 380))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + self.mnu,220,100,15))
						pygame.draw.rect(self.display[0], (255, 255, 0), pygame.Rect(bw + self.mnu,220,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['CHARISMA'][ch['LEVEL']] + ch['BONUS'][4]))),15))
						if dtb.CLASSES[ch['CLASS']]['CHARISMA'][ch['LEVEL'] - 1] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(bw + self.mnu,220,math.floor(100/(100/(dtb.CLASSES[ch['CLASS']]['CHARISMA'][ch['LEVEL'] - 1] + ch['BONUS'][4]))),15))
						if self.lopt == -1: n = random.randint(0,6)
						elif self.lopt == -2: n = ' '
						else: n = self.lopt
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(bw + 110 + self.mnu,145,15,15))
						self.display[1].blit(self.fnt['DEFAULT'].render(str(n), True, (240,240,240)), ((bw + 115 + self.mnu) * res.GSCALE, 295))
						
						if self.mnu <= 0:
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
						
						self.display[0].blit(self.fnt['MININFO'].render(ch['NAME'].lower(), True, (255,255,255)), (800 + self.mnu, 30))
						self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[14] + str(dtb.CNAMES[ch['CLASS']][ch['LEVEL'] - 1]) + ' !', True, (255,255,255)), ((800 + self.mnu) * res.GSCALE, 70 * res.GSCALE))
				#LOST SCREEN
				elif self.turn == -5:
					self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[8], True, (255,255,255)), (200 + self.mnu, 70))
					self.display[1].blit(self.fnt['DEFAULT'].render('-$100', True, (255,255,255)), ((200 + self.mnu) * res.GSCALE, 240))
		#HITISPLAY
		if len(self.dmg) > 0:
			for i in range(len(self.dmg)):
				if self.dmg[i]['INFO'] == None:
					del self.dmg[i]; break
			for i in self.dmg:
				if i['INFO'] != None:
					i['INFO'].set_alpha(i['ALPHA'])
					if i['TYPE'] == 0: cor = (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y)
					else: cor = (i['RECT'].x, i['RECT'].y)
					self.display[0].blit(i['INFO'], cor)
					if i['TIME'] > 0:
						if i['SHAKE'] != 0:
							i['RECT'].x += i['SHAKE']
							i['RECT'].y += i['SHAKE']
							i['SHAKE'] = -i['SHAKE']
							if i['SHAKE'] > 0: i['SHAKE'] -= 1
						if i['TYPE'] == 0: lm = 0
						else: lm = 8
						if i['GRAVITY']  < lm:
							i['RECT'].y += i['GRAVITY']
							i['GRAVITY'] += 1
							if i['GRAVITY'] < 0 and i['TYPE'] == 1: i['SHADE'] += 1
						elif i['SHAKE'] == 0: i['TIME'] -= 1
						if i['INFO'] != None:
							if i['TYPE'] == 0: fnt = 'DEFAULT'
							else: fnt = 'MININFO'
							i['INFO'].blit(self.fnt[fnt].render(i['TEXT'], True, (0,0,0)), (11 - i['SHADE'], 11 - i['SHADE']))
							i['INFO'].blit(self.fnt[fnt].render(i['TEXT'], True, i['COLOR'] ), (10 - i['SHADE'], 10 - i['SHADE']))
					elif i['ALPHA'] > 0: i['ALPHA'] -= 40
					else: i['INFO'] = None
		#ACTQUEUE
		for i in self.actqueue:
			if i['RECT'] == self.player[0]['RECT']: pos = (self.player[0]['RECT'].x - int(self.player[0]['RECT'].width/2) - self.cam.x,self.player[0]['RECT'].y - 40 - self.cam.y)
			else: pos = (i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y)
			pygame.draw.rect(self.display[0],(10,10,10),pygame.Rect(pos[0],pos[1],50,10))
			if i['BAR'] > 0: pygame.draw.rect(self.display[0],(10,200,10),pygame.Rect(pos[0],pos[1],math.floor(50/(100/i['BAR'])),10))
		#INVENTORY
		if self.inv.fade < self.windoww + 400:
			if self.inv.shake != 0: self.inv.rqst = True
			if self.inv.scroll != (self.mnu * 200): self.inv.rqst = True
			if self.inv.rqst: self.inv.draw()
			hh = int(self.windowh/2) - int(self.inv.srf[0].get_height()/2)
			shd = pygame.Surface((self.inv.srf[0].get_width(),self.inv.srf[0].get_height()),pygame.SRCALPHA)
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.inv.pos = ((self.windoww + 10) - self.inv.fade,hh)
			self.display[1].blit(shd,((self.windoww + 20) - self.inv.fade,hh + 10))
			self.display[1].blit(self.inv.srf[0], ((self.windoww + 10) - self.inv.fade,hh))
			self.display[1].blit(self.inv.srf[1], ((self.windoww + 10) - self.inv.fade,hh))
		if self.inv.type > 0:
			if self.inv.itmov == '': self.hpctrl = dtb.HINTS['INVENTORY_ITEMS']
			elif self.inv.itmov[0] != 0: self.hpctrl = dtb.HINTS['INVENTORY_HOLD']
			else: self.hpctrl = dtb.HINTS['INVENTORY_ACCESORIES']
			if self.inv.fade < int(self.windoww/2) + int(self.inv.srf[0].get_rect().width/2): self.inv.fade += 50
		elif self.inv.fade < self.windoww + 400: self.inv.fade += 50
		#INVENTORY WHEEL
		if self.inv.hld > 20:
			if self.inv.hld == 30: srf = self.inv.wheel()
			else: srf = pygame.transform.scale(self.inv.wheel(),((self.inv.hld - 20) * 3,(self.inv.hld - 20) * 3))
			self.display[0].blit(srf,(self.player[0]['RECT'].x - self.cam.x - int(srf.get_width()/2),self.player[0]['RECT'].y - self.cam.y - int(srf.get_width()/2)))
		#DEVICE
		if self.dev != None:
			if self.dev.rqst and self.phone > 0:
				if self.dev.img == 'camera':
					self.dev.battle = self.battle
					pht = self.battle
				else: pht = False
				if pht:
					self.dev.photo(self.bbg['IMAGE'], self.foe, pps)
				else: self.dev.draw()
			scl1 = res.GSCALE
			scl2 = int(res.GSCALE/2)
			if res.GSCALE == 3: pass
			scr = [pygame.transform.scale(self.dev.scr[0],(int(self.dev.scr[0].get_rect().width * scl1),int(self.dev.scr[0].get_rect().height * scl1))),
			pygame.transform.scale(self.dev.scr[1],(int(self.dev.scr[1].get_rect().width * scl2),int(self.dev.scr[1].get_rect().height * scl2)))]
			scl2 = scr[0].get_rect().width/self.dev.img.get_rect().width
			img = pygame.transform.scale(self.dev.img,(int((self.dev.img.get_rect().width + (self.dev.scrpos[0] * 2)) * scl2),int((self.dev.img.get_rect().height + (self.dev.scrpos[1] * 2)) * scl2)))
			self.hpctrl = dtb.HINTS[self.dev.hpctrl]
			imgh = math.floor(self.windoww/2) - math.floor(scr[0].get_width()/2)
			vv = int(self.windowh/2) - int(scr[0].get_rect().height/2)
			mp = pygame.mouse.get_pos()
			self.dvmp = pygame.Rect(int(mp[0]/res.GSCALE) - imgh,int(mp[1]/res.GSCALE) - self.phofa,2,2)
			if self.phone > 0:
				pygame.draw.rect(self.display[1],(10,10,10),pygame.Rect(imgh,self.phofa,scr[0].get_width(),scr[0].get_height()))
				if self.phofa < vv:
					self.phofa += 40
					if self.phofa >= 40:
						self.ch_sfx.play(res.SOUND['PHONE_UNLOCK'])
						self.phofa = vv
			else:
				if self.phofa == vv: self.ch_sfx.play(res.SOUND['PHONE_LOCK'])
				if self.phofa > 0: self.phofa -= 40
			if self.phofa == vv:
				if self.dev.battery:
					self.display[1].blit(scr[0], (imgh,self.phofa))
					self.display[1].blit(scr[1], (imgh,self.phofa))
				else:
					self.display[1].blit(pygame.image.load(res.BACKG_PATH + 'battery_low.png'), (imgh,self.phofa))
			if self.phofa > 0:
				pass
				#self.display[1].blit(img, (imgh - (self.dev.scrpos[0] * scl2),self.phofa - (self.dev.scrpos[1] * scl2)))
		#MINIGAME
		if self.minigame != None:
			self.display[1].blit(self.minigame.draw(), (0,0))
		#READING
		if self.read != None:
			srf = self.read.draw()
			self.display[0].blit(srf[0], (int(self.displayzw/2) - int(srf[0].get_rect().width/2), int(self.displayzh/2) - int(srf[0].get_rect().height/2)))
			self.display[1].blit(srf[1], (int(self.windoww/2) - int(srf[1].get_rect().width/2), int(self.windowh/2) - int(srf[1].get_rect().height/2)))
		#DIALOG
		if self.dlg['FADE'] < 500 and res.SCENE != -1:
			if self.dlg['TEXT'] != []:
				opt = 1
				ln = 1
				#DIALOG BOX
				if self.dlg['TYPE'] == 0:
					srf = pygame.Surface((self.windoww,self.winbar * res.GSCALE))
					srf.fill((0,0,0))
					yyax = 20 + self.windowh - (self.winbar * res.GSCALE)
				elif self.dlg['TYPE'] == 3:
					srf = pygame.Surface((self.windoww,40 * res.GSCALE))
					srf.fill((200,0,0))
					yyax = int(self.windowh/2)
				else: yyax = self.displayzh - 100
				if self.vkb.active: yyax = int((self.vkb.size[1] - self.vkb.pos - 100)/res.GSCALE)
				#DIALOG SCROLL
				if self.dlg['Y'] > (self.lopt * 40):
					self.dlg['Y'] -= int((40 * ln)/10)
					if self.dlg['Y'] < (self.lopt * 40): self.dlg['Y'] = (self.lopt * 40)
				if self.dlg['Y'] < (self.lopt * 40):
					self.dlg['Y'] += int((40 * ln)/10)
					if self.dlg['Y'] > (self.lopt * 40): self.dlg['Y'] = (self.lopt * 40)
				sd = False
				yy = 0
				ind = 0
				for i in self.dlg['TEXT']:
					if i == 0: sd = not sd
					if isinstance(i,str):
						if sd:
							self.dlgrct[ind].y = yyax + self.dlg['Y'] - yy
							ind += 1
						yy += 40
				yy = 0
				for i in self.dlg['TEXT'][::-1]:
					if isinstance(i,str):
						txt = self.fnt[self.dlg['FONT']].render(i, True, (255, 255, 255))
						txtsz = math.floor(self.fnt[self.dlg['FONT']].size(i)[0]/res.GSCALE) + 10
						if txtsz < 30: txtsz = 30
					if self.dlg['TYPE'] in [1,2] and i != 1 and i != 0 and len(i) != 0:
						#DIALOG BALOONS
						if sd == False:
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(20,yyax + self.dlg['Y'] - yy,5 + txtsz,25))
							pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(20,(yyax + 25) + self.dlg['Y'] - yy,5 + txtsz,5))
							pygame.draw.polygon(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), ((25,(yyax + 25) + self.dlg['Y'] - yy),(45,(yyax + 25) + self.dlg['Y'] - yy),(25,(yyax + 35) + self.dlg['Y'] - yy)))
							pygame.draw.polygon(self.display[0], (0, 0, 0), ((25,(yyax + 21) + self.dlg['Y'] - yy),(45,(yyax + 21) + self.dlg['Y'] - yy),(25,(yyax + 31) + self.dlg['Y'] - yy)))
						else:
							if self.lopt == opt:
								col1 = (res.COLOR[0],res.COLOR[1],res.COLOR[2])
								col2 = (10,10,10)
							else:
								col1 = (10,10,10)
								col2 = (res.COLOR[0],res.COLOR[1],res.COLOR[2])
							pygame.draw.rect(self.display[0], col1, self.dlgrct[opt - 1])
							pygame.draw.rect(self.display[0], col2, pygame.Rect(self.dlgrct[opt - 1].x,self.dlgrct[opt - 1].y + 25,self.dlgrct[opt - 1].width,self.dlgrct[opt - 1].height - 25))
							pygame.draw.polygon(self.display[0], col2, (((self.displayzw - 42),(yyax + 25) + self.dlg['Y'] - yy),((self.displayzw - 22),(yyax + 25) + self.dlg['Y'] - yy),((self.displayzw - 22),(yyax + 35) + self.dlg['Y'] - yy)))
							pygame.draw.polygon(self.display[0], col1, (((self.displayzw - 42),(yyax + 21) + self.dlg['Y'] - yy),((self.displayzw - 22),(yyax + 21) + self.dlg['Y'] - yy),((self.displayzw - 22),(yyax + 31) + self.dlg['Y'] - yy)))
							opt += 1
					if i == 0:
						if sd == False: sd = True
						elif sd: sd = False
					elif isinstance(i, str):
						if self.dlg['FONT'] == 'ANGER':
							shkx = int(random.randint(-5,5))
							shky = int(random.randint(-5,5))
						else: shkx = 0; shky = 0
						if self.dlg['TYPE'] in [0,3]:
							if sd == False: srf.blit(txt, (shkx + (30 * res.GSCALE), shky + (((self.winbar - 30 + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							else: srf.blit(txt, (shkx + (((self.displayzw - 12) - txtsz) * res.GSCALE), shky + (((self.winbar - 30 + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							yy += 20
						elif self.dlg['TYPE'] == 1:
							if sd == False: self.display[1].blit(txt, (shkx + (30 * res.GSCALE), shky + (((yyax + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							else: self.display[1].blit(txt, (shkx + (((self.displayzw - 12) - txtsz) * res.GSCALE), shky + (((yyax + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							yy += 40
						else:
							if sd == False: self.display[1].blit(txt, (shkx + (30 * res.GSCALE), shky + (((yyax + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							else: self.display[1].blit(txt, (shkx + (((self.displayzw - 12) - txtsz) * res.GSCALE), shky + (((yyax + 7) + self.dlg['Y'] - yy) * res.GSCALE)))
							yy += 40
				if self.dlg['TYPE'] in [0,3]:
					self.display[1].blit(srf,(0,yyax))
		#EASTER EGG
		if self.cityname == 'TWNN': self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'TWNN.png'), (35,0))
		#PAUSE MENU
		if self.title.mnu in [9,10] and self.title.winbar > 0:
			tt = self.title.menu()
			self.display[0].blit(tt[0],(0,0))
			self.display[1].blit(tt[1],(0,0))
		#NOTIFICATIONS
		i = 0
		while i < len(self.notification):
			if self.notification[i]['TEXT'] == None:
				del self.notification[i]
				i -= 1
			i += 1
		y = [0,0]
		for i in self.notification:
			ch = res.CHARACTERS[res.PARTY[res.FORMATION][0]]
			#SIZES
			if res.DISLEXIC:
				txt = ''
				for t in i['TEXT']:
					txt += t + ' '
			else: txt = i['TEXT']
			isz = 0
			if 'IMAGE' in i: isz += i['IMAGE'].get_width()
			if 'BAR' in i: isz += 105
			szw = math.floor(self.fnt['DEFAULT'].size(txt)[0]/2) + 30 + isz
			szh = math.floor(self.fnt['DEFAULT'].size(txt)[1]/2) + 30
			#MOVING
			if i['HALIGN'] == 'left':
				yy = 0
				i['X'] += 20
				if i['X'] < 0: xx = i['X']
				else: xx = 0
			if i['HALIGN'] == 'right':
				yy = 1
				i['X'] -= 20
				if i['X'] > self.displayzw - szw: xx = i['X']
				else: xx = self.displayzw - szw
			#BLINKING
			if 'BLIMIT' in i:
				i['BLINK'] += 1
				if i['BLINK'] < int(i['BLIMIT']/2):
					visible = True
				else: visible = False
				if i['BLINK'] >= i['BLIMIT']:
					i['BLINK'] = 0
			else: visible = True
			#MESSAGE
			if visible:
				addx = 0
				if i['COLOR'] != (0,0,0): pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(xx - 3,y[yy] + 27,szw,szh))
				else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(xx - 3,y[yy] + 27,szw,szh))
				pygame.draw.rect(self.display[0], i['COLOR'], pygame.Rect(xx,y[yy] + 30,szw - 6,szh - 6))
				if 'IMAGE' in i: self.display[0].blit(i['IMAGE'], (10 + xx, y[yy] + 40)); addx += i['IMAGE'].get_width() + 10
				if 'BAR' in i:
					pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(10 + xx + addx,y[yy] + 40,100,20))
					pygame.draw.rect(self.display[0], (200,200,10), pygame.Rect(10 + xx + addx,y[yy] + 40,int(100/(i['BAR'][0]/i['BAR'][1])),20))
					pygame.draw.rect(self.display[0], (10,200,10), pygame.Rect(10 + xx + addx,y[yy] + 40,int(100/(i['BAR'][0]/i['BAR'][2])),20))
				self.display[1].blit(self.fnt['DEFAULT'].render(txt, True, (0, 0, 0)), ((10 + xx + addx) * res.GSCALE, (y[yy] + 45) * res.GSCALE))
				y[yy] += szh + 10
			if i['X'] in [1000,-1000]:
				i['TEXT'] = None
		#TUTORIALS
		if self.tutorial['OUTPUT'] != []:
			nxt = False
			if self.tutorial['GO'] > 0 and self.phone == self.tutorial['GO']: self.tutorial['TIME'] = self.tutorial['WAIT']; nxt = True

			if self.tutorial['TIME'] < self.tutorial['WAIT']:
				if self.tutorial['FADE'] < 200: self.tutorial['FADE'] += 20
			elif self.tutorial['TIME'] >= self.tutorial['WAIT']: nxt = True
			if nxt:
				if self.tutorial['NEXT'] != '':
					self.tutorial = {'TEXT': dtb.TUTORIALS[self.tutorial['NEXT']].copy(), 'OUTPUT': [], 'FADE': 200, 'TIME': 0, 'WAIT': 300, 'NEXT': '','GO': 0}
					for j in self.tutorial['TEXT']:
						if isinstance(j,list):
							if j[0] == 'phone':
								self.tutorial['GO'] = j[1]
								if len(j) > 2: self.tutorial['NEXT'] = j[2]
							if j[0] == 'wait':
								self.tutorial['WAIT'] = j[1]
								if len(j) > 2: self.tutorial['NEXT'] = j[2]
							if j[0] == 'image':
								self.tutorial['OUTPUT'].append(j)
						else: self.tutorial['OUTPUT'].append(j)
				else:
					self.tutorial['GO'] = 0
					if self.tutorial['FADE'] > 0: self.tutorial['FADE'] -= 10
					else: self.tutorial['OUTPUT'] = []

			if self.tutorial['GO'] == 0: self.tutorial['TIME'] += 1
			pygame.draw.rect(self.display[0], (250,250,250), pygame.Rect(578 - self.tutorial['FADE'],18,self.tutorial['FADE'] + 4,int(self.tutorial['FADE']/2) + 4))
			pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(580 - self.tutorial['FADE'],20,self.tutorial['FADE'],int(self.tutorial['FADE']/2)))
			if self.tutorial['FADE'] == 200:
				x = 0
				y = 0
				sid = 0
				end = 0
				ky = [res.UP[0],res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.RUN[0],res.BAG[0],res.PHONE[0]]
				for j in self.tutorial['OUTPUT']:
					if isinstance(j,str): self.display[1].blit(self.fnt['DEFAULT'].render(j, True, (250, 250, 250)), (770 + x,50 + y))
					elif isinstance(j,list) and j[0] == 'image': self.display[0].blit(pygame.image.load(res.SPRITES_PATH + '' + j[1] + '.png'), (520 + x,25 + y))
					elif j == 0:
						for i in range(end): sid += 1
						x = 0
						y += 20
					else:
						if ky[j - 1] == pygame.K_LSHIFT: out = 'À'
						elif ky[j - 1] == pygame.K_RSHIFT: out = 'À'
						elif ky[j - 1] == pygame.K_LCTRL: out = 'Á'
						elif ky[j - 1] == pygame.K_RCTRL: out = 'Á'
						elif ky[j - 1] == pygame.K_LALT: out = 'Â'
						elif ky[j - 1] == pygame.K_RALT: out = 'Â'
						elif ky[j - 1] == pygame.K_BACKSPACE: out = 'Ã'
						elif ky[j - 1] == pygame.K_RETURN: out = 'Ä'
						elif ky[j - 1] == pygame.K_UP: out = 'È'
						elif ky[j - 1] == pygame.K_LEFT: out = 'É'
						elif ky[j - 1] == pygame.K_DOWN: out = 'Ê'
						elif ky[j - 1] == pygame.K_RIGHT: out = 'Ë'
						else: out = pygame.key.name(ky[j - 1]).upper()
						self.display[0].blit(self.fnt['CONTROLKEYS'].render(out, True, (250, 250, 250)), (385 + x,30 + y))
						for l in self.tutorial['OUTPUT'][sid:end]:
							if l in ['m','w','M','Q','T','U','V','W','Y','?']: x += 8
							elif l in ['f','r']: x += 6
							elif l in ['J']: x += 5
							elif l in ['l']: x += 4
							elif l in ['i','I','!','.',',']: x += 2
							else: x += 7
					end += 1
		#CHAPTER NAME
		if res.SCENE == -1:
			srf = pygame.Surface((self.displayzw,self.displayzh),pygame.SRCALPHA)
			srf.fill((0,0,0))
			rct = pygame.Surface((self.displayzw,80))
			rct.fill((255,255,255))
			srf.blit(rct,(0,int(self.displayzh/2) - 40),None,pygame.BLEND_RGBA_MULT)
			srf.blit(self.fnt['MININFO'].render(dtb.CHAPTERS[res.CHAPTER][0].lower(), True, (10, 10, 10)), (10, int(self.displayzh/2)))
			self.display[1].blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[res.CHAPTER][1], True, (250, 250, 250)), (10 * res.GSCALE, (int(self.displayzh/2) + 80) * res.GSCALE))
			self.display[0].blit(srf, (0,0))
		#SCORE COUNTERS
		sz = 10 * res.GSCALE
		srf = pygame.Surface((sz,sz * 10),pygame.SRCALPHA)
		srf.fill((0,0,0))
		for i in [0,1,2,3,4,5,6,7,8,9,0]: srf.blit(self.fnt['DEFAULT'].render(str(i),True,(200,200,200)),(0,i * sz))		
		x = 0
		for p in self.player:
			if p['PLAYING']:
				for i in range(len(str(p['SCORE']))):
					self.counter[x + 1][i + 10 - (len(str(p['SCORE'])))] += int(((int(str(p['SCORE'])[i]) * sz) - self.counter[x + 1][i + 10 - (len(str(p['SCORE'])))])/2)
				for i in range(len(self.counter[x + 1])):
					self.display[1].blit(srf, (20 + (i * sz), 20 + (x * sz)), (0,self.counter[x + 1][i],sz,sz))
				x += 1
		#TIME COUNTER
		if 'TIME' in dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]]:
			for i in range(3):
				if i != 2:
					nn = str(res.TIME[1])
					if len(nn) < 2: nn = '0' + nn
					nn = int(nn[i - 2])
				else:
					if res.TIME[2] == 0: nn = 0
					else: nn = int(str(res.TIME[2])[0])
				self.counter[0][i] += int(((nn * sz) - self.counter[0][i])/2)
			for i in range(len(self.counter[0])):
				self.display[1].blit(srf, (200 + (i * sz), 60), (0,self.counter[0][i],sz,sz))
		#VKEYBOARD
		if self.vkb.active:
			self.display[1].blit(self.vkb.draw(),(0,self.vkb.size[1] - self.vkb.pos))
			self.hpctrl = []
		self.vkb.scroll()
		#HELP CONTROLS
		if self.hpctrl != [] and res.HINT:
			hpsz = 0
			for i in self.hpctrl[::-1]:
				if isinstance(i,str):
					hptxt = self.fnt['DEFAULT'].render(' ' + i + ' ', True, (250, 250, 250))
					hpsz += self.fnt['DEFAULT'].size(' ' + i + ' ')[0]
					self.display[1].blit(hptxt, (self.windoww - 40 - hpsz, self.windowh - 40))
				elif isinstance(i,int):
					ky = res.CONTROLS[0]
					if ky[i] == pygame.K_LSHIFT: out = 'À'
					elif ky[i] == pygame.K_RSHIFT: out = 'À'
					elif ky[i] == pygame.K_LCTRL: out = 'Á'
					elif ky[i] == pygame.K_RCTRL: out = 'Á'
					elif ky[i] == pygame.K_LALT: out = 'Â'
					elif ky[i] == pygame.K_RALT: out = 'Â'
					elif ky[i] == pygame.K_BACKSPACE: out = 'Ã'
					elif ky[i] == pygame.K_RETURN: out = 'Ä'
					elif ky[i] == pygame.K_UP: out = 'È'
					elif ky[i] == pygame.K_LEFT: out = 'É'
					elif ky[i] == pygame.K_DOWN: out = 'Ê'
					elif ky[i] == pygame.K_RIGHT: out = 'Ë'
					else: out = pygame.key.name(ky[i]).upper()
					hpsz += self.fnt['CONTROLKEYS'].size(out)[0] + 20
					self.display[0].blit(self.fnt['CONTROLKEYS'].render(out, True, (250, 250, 250)), (self.displayzw - 20 - math.floor(hpsz/res.GSCALE), self.displayzh - 20))
		#TOUCH BUTTONS
		if len(self.buttons) > 0 and self.battle == False and self.dlg['TEXT'] == []:
			if self.player[0]['SPEED'] > 0: prs = str(self.player[0]['DIRECTION'])
			else: prs = '0'
			tchpad = pygame.image.load(res.SPRITES_PATH + 'tchpad_' + prs + '.png')
			tchpad.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]),None,pygame.BLEND_RGBA_MULT)
			self.display[1].blit(tchpad,(20,self.windowh - 264))
			for bt in [(4,(self.windoww - 190,self.windowh - 100)),(5,(self.windoww - 100,self.windowh - 100)),
			(6,(self.windoww - 190,40)),(7,(self.windoww - 100,40))]:
				abl = False
				if self.inv.type == 0: abl = True
				elif bt[0] in [6,7]: abl = True
				if abl:
					if bt[0] == 5:
						if self.player[0]['SPEEDLOCK']: fr = '1'
						else: fr = str(int(self.pressed[bt[0]][0]))
					else: fr = str(int(self.pressed[bt[0]][0]))
					img = pygame.image.load(res.SPRITES_PATH + 'tch_' + fr + '.png')
					img.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]),None,pygame.BLEND_RGBA_MULT)
					self.display[1].blit(img,bt[1])
		#DISDEBUG
		if self.disdbg:
			prs = ''
			mix = 0
			osinfo = os.uname()
			for i in range(len(self.pressed)): prs += str(self.pressed[i][0]) + ','
			for i in range(len(self.channels)):
				if self.channels[i][1]: mix += 1
			dinfo = ['DEVICE WIDTH: ' + str(self.windoww) + ' | DEVICE HEIGHT: ' + str(self.windowh) + ' | ',
			'GAME WIDTH: ' + str(self.displayzw) + ' | GAME HEIGHT: ' + str(self.displayzh) + ' | FPS: ' + str(int(self.glock.get_time())) + ' | ',
			'CAMERA X: ' + str(self.cam.x) + ' | CAMERA Y: ' + str(self.cam.y) + ' | ',
			'SYSTEM: ' + osinfo.sysname + ' | NODE: ' + osinfo.nodename + ' | RELEASE: ' + osinfo.release + ' | VERSION: ' + osinfo.version + ' | ',
			'MACHINE: ' + osinfo.machine,
			'PRESSED: [' + prs[0:-1] + '] + | MIXER: ' + str(mix) + ' | ',
			'TIME: ' + str(res.TIME[0]) + ':' + str(res.TIME[1]) + ':' + str(res.TIME[2]) + ' | DATE: ' + str(res.DATE[0]) + '/' + str(res.DATE[1]) + '/' + str(res.DATE[2]) + ' | ',
			'INVENTORY: ' + str(self.inv.type) + ' | PAUSE: ' + str(self.title.mnu)]
			y = 0
			for txt in self.guitools.wrap(dinfo,self.fnt['DISDBG'],int(self.windoww * 0.75)):
				self.display[1].blit(self.fnt['DISDBG'].render(txt, True, (200,200,200)), (10, 10 + (y * 30)))
				y += 1
		#CAMERA
		camfollow = True
		camspd = int(res.CAMACC * res.GSCALE)
		recam = [self.cam.x,self.cam.y]
		if len(self.player) == 0:
			pcam = [int(self.displayzw/2),int(self.displayzh/2)]
		elif self.dlg['CAMERA'] == 0:
			pcam = [0,0]
			for i in self.player:
				if i['POSTURE'] == 2: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y - 200
				else: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y
			pcam = [int(pcam[0]/len(self.player)),int(pcam[1]/len(self.player))]
		else: pcam = [self.dlg['CAMERA'].x,self.dlg['CAMERA'].y]
		cmgrd = [[0,(self.map.width * self.map.tilewidth) - self.displayzw],
		[0,(self.map.height * self.map.tileheight) - self.displayzh]]
		lst = [[self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight],
		[self.displayzw,self.displayzh]]
		camscroll = [self.map.properties['HSCROLL'],self.map.properties['VSCROLL']]
		for i in range(2):
			if lst[0][i] > lst[1][i]:
				if camfollow:
					if self.portalgo == {}:
						self.campos[i] = pcam[i]
					#SCROLL CAMERA
					if camscroll[i] != 0:
						recam[i] += camscroll[i]
					#REGULAR CAMERA
					elif self.camgrid == 1:
						recam[i] += int((self.campos[i] - recam[i] - (lst[1][i]/2))/camspd)
					#STATIC CAMERA
					else:
						if self.camgrid == 'screen': gg = lst[1][i]
						else: gg = self.camgrid * self.map.tilewidth
						recam[i] = math.floor(self.campos[i]/gg) * gg
				if recam[i] < cmgrd[i][0]: recam[i] = cmgrd[i][0]
				if recam[i] > cmgrd[i][1]: recam[i] = cmgrd[i][1]
			else: recam[i] = -int((lst[1][i] - lst[0][i])/2)
		self.cam.x = recam[0]
		self.cam.y = recam[1]
		#UPDATE SCREEN
		#self.screen.blit(self.blankimg,(0,0))
		chk = False
		for i in res.INVENTORY[res.PARTY[res.FORMATION][0]]:
			if i[0][0].startswith('head_glasses'): chk = True; break
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['FLAW'] != 'myopia': chk = not chk
		if chk == False:
			srf = pygame.transform.scale(self.display[0], (self.displayzw * res.GSCALE, self.displayzh * res.GSCALE))
			srf.set_alpha(100)
			self.screen.blit(srf, (self.displayx - 20, self.displayy))
			self.screen.blit(srf, (self.displayx + 10, self.displayy))
			srf = self.display[1]
			srf.set_alpha(100)
			self.screen.blit(srf, (self.displayx - 20, self.displayy))
			self.screen.blit(srf, (self.displayx + 10, self.displayy))
		else:
			if self.displayx > self.displayzw * 0.25:
				self.screen.blit(pygame.transform.scale(self.display[0], (self.displayzw * res.GSCALE, self.displayzh * res.GSCALE)), (self.displayx - int(self.displayzw * res.GSCALE * 1.25), self.displayy))
				self.screen.blit(self.display[1], (self.displayx - int(self.displayzw * res.GSCALE * 1.25), self.displayy))
			if self.displayy > self.displayzh * 0.25:
				self.screen.blit(pygame.transform.scale(self.display[0], (self.displayzw * res.GSCALE, self.displayzh * res.GSCALE)), (self.displayx, self.displayy - int(self.displayzh * res.GSCALE * 1.25)))
				self.screen.blit(self.display[1], (self.displayx, self.displayy - int(self.displayzh * res.GSCALE * 1.25)))
			self.screen.blit(pygame.transform.scale(self.display[0], (self.displayzw * res.GSCALE, self.displayzh * res.GSCALE)), (self.displayx, self.displayy))
			self.screen.blit(self.display[1], (self.displayx, self.displayy))
		#MOUSE
		if res.MOUSE == 1:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'),(self.click.x,self.click.y))

	def loading(self):
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				self.classrun = 0
				res.recent_data(1,res.ID)
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windowh = event.h
				sh = int(event.h/4)
				self.windoww = 6 * sh
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
		self.screen.fill((0,0,0),pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
		if self.loadingif != None:
			self.loadingif += 0.01
			if str(self.loadingif)[2] == '0': upd = True
			else: upd = False
			if self.loadingif >= 8.0: self.loadingif = 0.0
		if upd:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'loading_' + str(math.floor(self.loadingif)) + '.png'), (self.windoww - 80, self.windowh - 80))
			pygame.display.update(pygame.Rect(self.windoww - 80,self.windowh - 80,30,30))

	def crash(self):
		self.screen.fill((0,0,0))
		et, ev, eb = sys.exc_info()
		tlist = []
		for t in traceback.extract_tb(eb):
			tlist.append((t[0],t[1],t[2],t[3]))

		fnt = pygame.font.SysFont('Calibri', 26)
		self.screen.blit(fnt.render(dtb.ERROR[0],True,(10,250,10)),(10,20))
		fnt = pygame.font.SysFont('Calibri', 22)
		self.screen.blit(fnt.render(str(et.__name__),True,(10,250,10)),(10,60))
		self.screen.blit(fnt.render(str(ev),True,(10,250,10)),(10,80))
		y = 100
		for j in tlist:
			self.screen.blit(fnt.render(str(j),True,(10,250,10)),(10,y))
			y += 20
		self.screen.blit(fnt.render(dtb.ERROR[1],True,(10,250,10)),(10,y + 20))
		print(str(et.__name__))
		print(str(ev))
		print(tlist)
		pygame.display.flip()
			
		again = False
		while again == False:
			for event in pygame.event.get():
				#EXIT
				if event.type == pygame.QUIT:
					self.classrun = 0
					res.recent_data(1,res.ID)
					pygame.quit()
					sys.exit()
					exit()
				#RESIZE
				if event.type == pygame.VIDEORESIZE:
					self.windowh = event.h
					sh = int(event.h/4)
					self.windoww = 6 * sh
					self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				#SKIP
				do = False
				if event.type == pygame.KEYDOWN: do = True
				if event.type == pygame.MOUSEBUTTONDOWN: do = True
				if do:
					self.loadmap()
					again = True

	def run(self,tr=True):
		if tr:
			#ACTQUEUE
			for i in range(len(self.actqueue)):
				self.actqueue[i]['BAR'] += self.actqueue[i]['SPEED']
				if self.actqueue[i]['BAR'] >= 100:
					#FOOD
					if self.actqueue[i]['ACT'] == 0:
						ch = res.CHARACTERS[self.actqueue[i]['CHARACTER']]
						it = res.INVENTORY[self.actqueue[i]['CHARACTER']][self.actqueue[i]['ITEM'][0]][self.actqueue[i]['ITEM'][1]]
						if ch['FLAW'] == 'celiac':
							if it[0] in dtb.GLUTEN_FOOD: good = False
							else: good = True
						elif ch['FLAW'] == 'lactose intolerant':
							if it[0] in dtb.LACTOSE_FOOD: good = False
							else: good = True
						else: good = True
						if good:
							self.ch_ton.play(res.SOUND['HEAL'])
							hl = dtb.ITEMS[it[0]][5]
							hg = dtb.ITEMS[it[0]][6]
							for ex in it[2::2]:
								if ex != '_': hl += dtb.ITEMS[ex][5]
							if it in res.CHARACTERS[self.inv.opt[2]]['FAVFOOD']:
								hl += int(hl/2)
								hg += int(hg/2)
							hpb = ch['HP']
							ch['HP'] += hl
							ch['HUNGER'] += hg
							if res.DISITEMS[it[0]] == 0:
								res.DISITEMS[it[0]] = 1
							if ch['HP'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
								ch['HP'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
						else:
							self.ch_ton.play(res.SOUND['INCONSCIOUS'])
							ch['HEALTH'] = 10
						if self.inv.allowtrash and len(dtb.ITEMS[it[0]]) > 8 and dtb.ITEMS[it[0]][8] != None:
							it = ['trash_' + dtb.ITEMS[it[0]][8],'0000']
						elif self.inv.allowtrash and it[0].endswith('_wasted') and dtb.ITEMS[it[0]][7] != None:
							it = ['trash_' + dtb.ITEMS[it[0]][7],'0000']
						else:
							it = ['_','0000']
						bbr = [dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']],ch['HP'],hpb]
						if bbr[1] > bbr[0]: bbr[1] = bbr[0]
						self.notification.append({'TEXT': '', 'COLOR': (255, 0, 0), 'HALIGN': 'left','X': -180,
						'IMAGE': pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][0]) + '.png'),'BAR': bbr})
						res.INVENTORY[self.actqueue[i]['CHARACTER']][self.actqueue[i]['ITEM'][0]][self.actqueue[i]['ITEM'][1]] = it
					del self.actqueue[i]
					i -= 1
			#WAITIME
			for i in range(len(self.waitlst)):
				if self.waitlst[i][1] < self.waitime:
					del self.waitlst[i]
					break
			for i in self.waitlst:
				if i[1] == self.waitime:
					#SUNNY WEATHER
					if i[0] == 'sun':
						res.WEATHER = 0
						self.waitlst.append(['rain',self.waitime + 3600])
					#RAINY WEATHER
					elif i[0] == 'rain':
						res.WEATHER = 1
						self.waitlst.append(['sun',self.waitime + 3600])
					#REPELLENT EFFECT
					elif i[0].startswith('repellent'):
						res.CHARACTERS[int(i[0][9])]['HEALTH'] = 0
					#CALLING
					elif i[0].startswith('cal'):
						self.ch_ton.play(res.SOUND['CALLING'],-1)
						self.ch_rng.play(res.SOUND['RINGTONE_' + str(self.dev.pbg)],-1)
						if self.rad.onoff: pygame.mixer.music.pause()
						self.cal.nb = i[0][3:]
						self.waitlst.append(['cutcal',self.waitime + 1200])
					#CUTTING CALL
					elif i[0].startswith('cutcal'):
						if self.cal.nb != '':
							self.ch_ton.stop()
							self.ch_rng.stop()
							self.cal.nb = ''
					#DELIVERY
					elif i[0] == 'delivery':
						if self.dlg['FADE'] > 0:
							self.dialog([(30,pygame.Rect(self.player[0]['RECT'].x - 430,self.player[0]['RECT'].y,0,0),i[2]['INDEX'],i[2]['WHO'],i[2]['TYPE']),
								(24,'n',(self.player[0]['RECT'].x - 30,self.player[0]['RECT'].y),3)])
					#RADIONEWS
					elif i[0].startswith('radionews'):
						pygame.mixer.music.load(res.MUSIC_PATH + 'battle_incoming.mp3',-1)
						pygame.mixer.music.play()
					#RADIOEE
					elif i[0].startswith('radioee'):
						self.ch_ton.stop()
						pygame.mixer.music.load(res.MUSIC_PATH + i[2] + '.mp3')
						pygame.mixer.music.play()
						self.rad.msc = -1
					#TIME WARNING
					elif i[0].startswith('advice'):
						if self.dlg['FADE'] > 0:
							self.dialog(dtb.DIALOGS['ADVICE'])
			#RADIONEWS AND RADIOEE
			if self.rad.onoff:
				for i in dtb.RADIONEWS:
					if i[1][0] == res.TIME[0] and i[1][1] == res.TIME[1]:
						if i[0] == None: ply = True
						elif i[0][0] == res.DATE[0] and i[1][1] == res.DATE[1]: ply = True
						else: ply = False
						if ply and self.rad.msc != -2:
							self.rad.nwsw = 1
							self.rad.nwsind = i[0][2]
							pygame.mixer.music.stop()
							self.ch_ton.play(res.SOUND['RADIONEWS'])
							self.waitlst.append(['radionews',self.waitime + 20,i[0]])
				for i in dtb.RADIOEE:
					if int(i[2][0:2]) == res.TIME[0] and int(i[2][2:4]) == res.TIME[1]:
						if i[1] == None: ply = True
						elif int(i[1][0:2]) == res.DATE[0] and int(i[1][2:4]) == res.DATE[1]: ply = True
						else: ply = False
						if ply and self.rad.msc != -2:
							self.rad.msc = -2
							pygame.mixer.music.stop()
							self.ch_ton.play(res.SOUND['NOISE'],-1)
							self.waitlst.append(['radioee',self.waitime + 60,i[0]])
			#ITEMS DURATION
			"""u = 0
			for b in res.INVENTORY:
				for j in b:
					for i in list(filter(lambda x: x[0] != '_', j)):
						self.inv.duration(i,u)
				u += 1"""
			#WASH
			"""for i in res.WASH:
				if i[2] != None and self.notification['X'] == 0:
					if res.TIME[0] >= int(i[2][0:2]):
						if res.TIME[1] >= int(i[2][2:4]):
							self.ch_sfx.play(res.SOUND['NOTIFICATION'])
							self.notification['TEXT'] = dtb.NOTINFO['WASH']
							self.notification['COLOR'] = (165, 255, 0)
							res.TASKS.append([(dtb.NOTINFO['WASH'],None,None), 0])
							i[2] = None"""
			#SECONDS
			self.waitime += 1
			if 'TIME' in dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]] and dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]]['TIME'][0] < 0:
				pom = -1
			else: pom = 1
			#BATTERY
			battery = res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1]
			if battery != 'infinite' and self.dev != None:
				battery = int(battery)
				if battery < 0:
					if self.rad.onoff:
						self.rad.onoff = False
						self.ch_ton.stop()
						pygame.mixer.music.stop()
					battery = 0
				self.dev.battery = battery
			sleep = False
			for p in self.player:
				if sleep == False: sleep = p['SLEEP']
			#SLEEP
			if sleep:
				res.TIME[1] += 5 * pom
				for p in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[p]['HP'] < dtb.CLASSES[res.CHARACTERS[p]['CLASS']]['RESISTANCE'][res.CHARACTERS[p]['LEVEL']]:
						res.CHARACTERS[p]['HP'] += 1
					if res.CHARACTERS[p]['SLEEP'] < 10000: res.CHARACTERS[p]['SLEEP'] += 50
			#NORMAL
			else:
				res.TIME[2] += 1 * pom
				if self.phone > 0 and battery != None:
					if res.CHAPTER > 0: battery -= 1
					elif res.SCENE > 0: battery -= 1
			res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1] = str(battery)
			if res.TIME == [0,0,0]:
				for i in res.PARTY[res.FORMATION]:
					res.CHARACTERS[i]['HP'] = 0
			#MINUTES
			if res.TIME[2] < 0: res.TIME[1] -= 1; res.TIME[2] = 59
			if res.TIME[2] >= 60:
				res.TIME[1] += 1; res.TIME[2] = 0
				#BASIC NECESITIES
				"""for p in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[p]['HUNGER'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 6
					else: res.CHARACTERS[p]['HUNGER'] -= 1
					if res.CHARACTERS[p]['THIRST'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 7
					else: res.CHARACTERS[p]['THIRST'] -= 1
					if res.CHARACTERS[p]['SLEEP'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 8
					else: res.CHARACTERS[p]['SLEEP'] -= 10"""
			#HOURS
			if res.TIME[1] < 0: res.TIME[0] -= 1; res.TIME[1] = 59
			if res.TIME[1] >= 60:
				res.TIME[0] += 1; res.TIME[1] = 0
				if sleep:
					for u in res.PARTY[res.FORMATION]:
						if res.CHARACTERS[u]['HEALTH'] in (4,5,9,10,11):
							res.CHARACTERS[u]['HEALTH'] = 0
			#DAYS
			if res.TIME[0] >= 24: res.DATE[0] += 1; res.DATE[3] += 1; res.TIME[0] = 0; res.TEMPERATURE = dtb.CITIES[self.map.properties['CITY']][1][res.DATE[1] - 1]
			#WEEKS
			if res.DATE[3] > 7: res.DATE[3] = 1; res.DATE[4] += 1
			if res.DATE[4] > 8: res.DATE[4] = 1
			#MONTHS
			if res.DATE[1] in [1,3,5,7,8,10,12] and res.DATE[0] > 31: res.DATE[1] += 1; res.DATE[0] = 1
			elif res.DATE[1] in [4,6,9,11] and res.DATE[0] > 30: res.DATE[1] += 1; res.DATE[0] = 1
			elif res.DATE[1] == 2 and res.DATE[0] > 28: res.DATE[1] += 1; res.DATE[0] = 1
			#YEARS
			if res.DATE[1] > 12: res.DATE[2] += 1; res.DATE[1] = 1
		for i in self.channels:
			if i[0].get_busy() == False: i[1] = None
		self.events()
		self.draw()
		if int(self.glock.get_fps()) > 0:
			jp = math.floor(res.FPS/int(self.glock.time()))
		else: jp = 1
		self.FPS += 1
		if self.FPS >= jp:
			#UPDATE
			try: pygame.display.flip()
			except: self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
			#FPS
			self.FPS = int()
			if self.FPS > 0:
				self.glock.tick(res.FPS)
			self.FPS = 0 
			res.GAMETIME += self.glock.get_rawtime()

g = Game()
while True:
	try: g.run()
	except: g.crash()