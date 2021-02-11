# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3
import pygame
import pytmx
import random
import sqlite3
import webbrowser
import datetime
import traceback
import platform
import math
import sys
import os

from Plugins import *
import resources as res
import minigames as mng
import GUI

if res.FILES[3] != []:
	if res.FILES[3][0] == 'PT': import database_PT as dtb
	if res.FILES[3][0] == 'EN': import database_EN as dtb
else: import database_PT as dtb

pygame.init()
pygame.display.set_caption(res.GNAME)
pygame.display.set_icon(pygame.image.load('icon.ico'))
pygame.mouse.set_visible(False)

class Title:
	def __init__(self):
		if platform.system() == 'Windows':
			self.windoww = 1200
			self.windowh = 800
			res.MOUSE = 1
		else:
			sz = pygame.display.Info()
			self.windoww = sz.current_w
			self.windowh = sz.current_h
			res.MOUSE == 2
		self.displayzw = int(self.windoww/res.GSCALE)
		self.displayzh = int(self.windowh/res.GSCALE)
		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((self.displayzw, self.displayzh)),pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
		self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', 30),'MINI': pygame.font.SysFont('Calibri', 20), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 30)}
		self.sfx = pygame.mixer.Channel(0)
		self.ton = pygame.mixer.Channel(1)
		self.msc = pygame.mixer.Channel(2)
		self.glock = pygame.time.Clock()
		self.FPS = 1
		self.winbar = int(self.windowh/2)
		self.wait = 0
		self.noise = 0
		self.tv = round(random.randint(1,10))
		self.transtype = 0
		self.transform = 0
		self.transpeed = 0
		self.rectrot = 0
		self.opt = 0
		self.lopt = -1
		self.mnu = -1
		self.scroll = 0
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
		mscpath = os.listdir(res.MUSIC_PATH[:-1])
		self.fload = (res.RANGE_SKIN * res.RANGE_FACE * res.RANGE_HAIR) + (res.RANGE_SKIN * res.RANGE_COSTUME) + res.RANGE_RADIO + len(sfxpath) + len(mscpath)

		for i in res.FILES[0]:
			if res.FILES[1][i] == 0:
				del res.FILES[0][i]
				del res.FILES[1][i]
				del res.FILES[2][i]
				del res.FILES[3][i]

		if res.GAMETIME == 0:
			res.new_data()
			res.recent_data(2)
		else:
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
		self.run()
		#LOADING MUSIC
		for j in mscpath: 
			res.music(j)
		self.mnu = 0
		if res.GAMETIME > 0: self.msc.play(res.SONGS['HERE_COMES_THE_DEATH'])
		#LOADING HEADS
		for w in range(res.RANGE_SKIN):
			for p in range(res.RANGE_FACE):
				for h in range(res.RANGE_HAIR):
					res.heads(p,w,h)
					self.run()
		#LOADING BODIES
		for w in range(res.RANGE_SKIN):
			for t in range(res.RANGE_COSTUME):
				res.bodies(w,t)
				self.run()
		#LOADING ATTACK ANIMATIONS
		res.battlesprites()
		res.animals()
		#LOADING SFX
		for j in sfxpath: 
			res.sfx(j)
			self.run()
		#LOADING SONGS
		for i in range(res.RANGE_RADIO): 
			res.radio(i)
			self.run()
		self.mnu = 3
		if res.GAMETIME == 0:
			self.msc.play(res.SONGS['THE_PRIMATERIA'])
			self.wait = 200
			self.msg = -1
				
	def events(self):
		#MOUSE
		mrect = pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png').get_rect()
		mrect.x = math.floor(pygame.mouse.get_pos()[0]/2)
		mrect.y = math.floor(pygame.mouse.get_pos()[1]/2)
		#EVENTS
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', math.floor(self.windoww/200) * 2)}
				self.display[1] = pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)
			#MOUSE
			if res.MOUSE > 0:
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.pressed = (1,1,1)
				else: self.pressed = (0,0,0)
				#SKIP
				if self.pressed[0]:
					if self.mnu < 2 and res.GAMETIME > 0: self.mnu += 1
					elif self.mnu == 6: self.skip = True
				#SELECT FILES
				if self.mnu == 3:
					self.lopt = -1
					for i in range(len(self.flrects)):
						if pygame.Rect.colliderect(mrect,self.flrects[i]) == True:
							self.lopt = i
							if self.pressed[0] and self.flrects[i].width == 250:
								#SELECT GAME
								if i < len(res.FILES[0]):
									res.ID = self.lopt
									self.lopt = -1
									self.mnu = 4
								#NEW GAME
								else:
									self.sfx.play(res.SOUND['FILE_NEW'])
									res.new_data()
									res.save_data()
									res.save_sett()
									res.recent_data(2,self.lopt)
									pygame.mixer.music.fadeout(3000)
									self.msc.fadeout(3000)
									self.ton.fadeout(3000)
									self.mnu = 7
				#SELECT CHAPTER
				elif self.mnu == 4: 
					self.lopt = -1
					for i in range(len(self.chrects)):
						if pygame.Rect.colliderect(mrect,self.chrects[i]) == True:
							self.lopt = i
							if self.pressed[0] and self.chrects[i].width == 250:
								#LOAD GAME
								if i < res.FILES[1][res.ID] + 1:
									res.CHAPTER = self.lopt
									res.load_data()
									pygame.mixer.music.stop()
									self.ton.play(res.SOUND['NOISE'],-1)
									self.msc.stop()
									self.wait = 100
									self.mnu = 8
									self.tv = 0
								#DELETE GAME
								else:
									res.delete_data()
									self.mnu -= 1
			#KEYBOARD
			if res.MOUSE < 2:
				self.pressed = pygame.key.get_pressed()
				if self.pressed[res.ACT[0]]:
					#SKIP
					if self.mnu < 3: self.mnu += 1
					elif self.mnu == 6: self.skip = True
					#FILE MENU
					elif self.winbar == 100:
						#SELECT GAME
						if self.lopt < len(res.FILES[0]):
							if self.mnu < 4: self.mnu += 1
							elif self.mnu == 4: 
								#LOAD GAME
								if self.opt == 0:
									res.ID = self.lopt
									res.load_data()
									pygame.mixer.music.stop()
									self.ton.play(res.SOUND['NOISE'],-1)
									self.msc.stop()
									self.wait = 100
									self.mnu = 8
									self.tv = 0
								#DELETE GAME
								else:
									res.ID = self.lopt
									res.delete_data()
									self.mnu -= 1
						#NEW GAME
						else:
							self.sfx.play(res.SOUND['FILE_NEW'])
							res.new_data()
							res.save_data()
							res.save_sett()
							res.recent_data(2,self.lopt)
							pygame.mixer.music.fadeout(3000)
							self.msc.fadeout(3000)
							self.ton.fadeout(3000)
							self.mnu = 7

				if self.pressed[res.RUN[0]]:
					if self.mnu == 4: self.mnu = 3
				#SELECT
				if self.pressed[res.UP[0]] and self.mnu == 3: self.lopt -= 1; self.sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[res.DOWN[0]] and self.mnu == 3: self.lopt += 1; self.sfx.play(res.SOUND['MENU_VER'])

				if self.pressed[res.LEFT[0]] and self.mnu == 4: self.opt = 0; self.sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[res.RIGHT[0]] and self.mnu == 4: self.opt = 1; self.sfx.play(res.SOUND['MENU_VER'])
				#RANGE LIMIT
				if self.lopt < 0: self.lopt = len(res.FILES[0])
				if self.lopt > len(res.FILES[0]): self.lopt = 0

	def random(self):
		self.msc.stop()
		pygame.mixer.music.stop()
		self.ton.play(res.SOUND['NOISE'],-1)
		self.tv = 0
		self.transform = 0
		self.rectrot = 0
		for i in range(round(random.randint(5,30)/self.FPS)): self.run()
		if self.mnu < 6:
			self.ton.stop()
			self.tv = round(random.randint(1,17))
			self.transtype = round(random.randint(0,5))
			spd = round(random.randint(0,100))
			if self.transtype == 5: self.transpeed = 2
			elif spd > 75: self.transpeed = -2
			elif spd > 50: self.transpeed = 2
			elif spd > 25: self.transpeed = -1
			else: self.transpeed = 1
			self.wait = round(random.randint(50,100))
			rd = round(random.randint(0,9))
			if len(res.RADIO[str(rd)]) > 0:
				sng = round(random.randint(0,len(res.RADIO[str(rd)]) - 1))
				msc = res.SONGS_PATH + str(rd) + '/' + res.RADIO[str(rd)][sng]
				if msc.endswith('.mp3'):
					audio = MP3(msc)
					pygame.mixer.music.load(msc)
					pygame.mixer.music.play(1,round(random.randint(20,int(audio.info.length) - 20)))
				elif msc.endswith('.wav'):
					audio = pygame.mixer.Sound(msc)
					self.msc.play(audio)
				elif msc.endswith('.ogg'):
					audio = pygame.mixer.Sound(msc)
					self.msc.play(audio)
			if self.transtype in [0,4] and self.transpeed < 0: self.transform = round(random.randint(200,300))
			if self.transtype == 5: self.transform = round(random.randint(1,2))
			if self.transtype in [1,4]:
				img = pygame.image.load(res.BACKG_PATH + 'tv_' + str(self.tv) + '.png').convert()
				self.rectrot = img.get_rect(center=pygame.Rect(0,0,600,400).center)
	
	def intro(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
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
			self.winbar -= 10 * self.FPS
		elif self.mnu == 4 and self.winbar < int(self.windowh/2):
			self.winbar += 10 * self.FPS
		elif self.mnu == 4:
			self.msc.fadeout(3000)
			self.classrun = False
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0,0,self.windoww,self.winbar))
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0,self.windowh - self.winbar,self.windoww,self.winbar))
		#MESSAGE
		if self.msg > -1 and self.msg < len(dtb.GINTRO):
			sz = self.fnt['DEFAULT'].size(dtb.GINTRO[self.msg])[0]
			self.screen.blit(self.fnt['DEFAULT'].render(dtb.GINTRO[self.msg], True, (200,200,200)), (int(self.windoww/2) - int(sz/2),self.windowh - 50))
		#TIME
		self.wait -= 1
		if self.wait == 0:
			self.msg += 1
			if self.msg >= len(dtb.GINTRO):
				self.mnu = 4
			self.wait = 50
		pygame.display.flip()
		self.glock.tick(60/self.FPS)
		
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
		if flp == True: self.screen.fill((0,0,0))
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
		if flp == True: pygame.display.flip()
		else:
			pygame.display.update(pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
			pygame.display.update(pygame.Rect(42,self.windowh - 68,self.windoww - 154,6))

	def menu(self):
		for i in self.display: i.fill((0,0,0,0))
		rztxt = math.floor((self.windoww/300)/2)
		#RANDOM SCREEN
		if self.mnu != 6:
			if self.tv == 0:
				self.noise += 1
				if self.noise == 3: self.noise = 0
				img = pygame.image.load(res.BACKG_PATH + 'noise_' + str(self.noise) + '.png')
				if self.windoww >= self.windowh: sz = self.windoww
				else: sz = self.windowh
				self.display[0].blit(pygame.transform.scale(img,(sz,sz)), (0, 0))
			else:
				self.transform += self.transpeed * self.FPS
				if self.windoww >= self.windowh: sz = self.windoww
				else: sz = self.windowh
				img = pygame.transform.scale(pygame.image.load(res.BACKG_PATH + 'tv_' + str(self.tv) + '.png'),(sz,sz)).convert()
				#SCALE
				if self.transtype == 0:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform * 2),img.get_rect().height + round(self.transform * 2)))
					self.display[0].blit(img, (600 - img.get_rect().width, 600 - img.get_rect().height))
				#ROTATE
				elif self.transtype == 1:
					img = pygame.transform.scale(img,(800,800))
					trs = pygame.transform.rotate(img,self.transform)
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot)
				#MOVE HORIZONTAL
				elif self.transtype == 2:
					self.display[0].blit(img, (self.transform, 0))
					if self.transform < 0: self.display[0].blit(img, (600 + self.transform, 0))
					if self.transform > 0: self.display[0].blit(img, (-600 + self.transform, 0))
				#MOVE VERTICAL
				elif self.transtype == 3:
					self.display[0].blit(img, (0, self.transform))
					if self.transform < 0: self.display[0].blit(img, (0, 600 + self.transform))
					if self.transform > 0: self.display[0].blit(img, (0, -600 + self.transform))
				#SCALE AND ROTATE
				if self.transtype == 4:
					img = pygame.transform.scale(img,(img.get_rect().width + round(self.transform/6),img.get_rect().height + round(self.transform/4)))
					trs = pygame.transform.rotate(img,self.transform)
					self.rectrot = trs.get_rect(center = self.rectrot.center)
					self.display[0].blit(trs, self.rectrot)
				#RANDOM
				if self.transtype == 5:
					if self.transform > 17: self.transform = 1
					img = pygame.image.load(res.BACKG_PATH + 'tv_' + str(self.transform) + '.png').convert()
					self.display[0].blit(img, (0,0))
		#FILES MENU
		if self.mnu == 3:
			for i in range(len(res.FILES[1])):
				if self.lopt == i:
					if self.flrects[i].width < 250:
						self.flrects[i].width += 4
						self.flrects[i].x -= 4
					col = (255,255,0)
				else:
					if self.flrects[i].width > 230:
						self.flrects[i].width -= 4
						self.flrects[i].x += 4
					col = (255,255,255)
				shd = pygame.Surface((self.flrects[i].width,self.flrects[i].height))
				shd.set_alpha(100)
				shd.fill((10,10,10))
				self.display[0].blit(shd,(self.flrects[i].x + 5,self.flrects[i].y + 5))
				pygame.draw.rect(self.display[0], col, self.flrects[i])
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[res.FILES[1][i]][0], True, (0,0,0)), ((self.flrects[i].x + 10) * 2, (110 + (i * 51)) * 2))
				self.display[1].blit(self.fnt['DEFAULT'].render(self.gmtim[i], True, (0, 0, 0)), ((self.flrects[i].x + 10) * 2, (130 + (i * 51)) * 2))

				'''if self.mnu > 3 and self.lopt == i:
					if self.opt == 0: pygame.draw.rect(self.display[0], (255,255,255), self.oprects[i][0])
					if self.opt == 1: pygame.draw.rect(self.display[0], (255,255,255), self.oprects[i][1])
					self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_7.png'), (self.displayzw - 70, 120 + (i * 51)))
					self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_8.png'), (self.displayzw - 48, 120 + (i * 51)))
				else:
					x = 0
					for p in res.FILES[4][i][::-1]:
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (self.displayzw - 50 - x, 120 + (i * 51)))
						x += 22'''
			#NEW FILE
			if self.lopt == len(res.FILES[0]):
				if self.flrects[len(res.FILES[1])].width < 250:
					self.flrects[len(res.FILES[1])].width += 4
					self.flrects[len(res.FILES[1])].x -= 4
				col = (255,255,0)
			else:
				if self.flrects[len(res.FILES[1])].width > 230:
					self.flrects[len(res.FILES[1])].width -= 4
					self.flrects[len(res.FILES[1])].x += 4
				col = (255,255,255)
			shd = pygame.Surface((self.flrects[len(res.FILES[1])].width,self.flrects[len(res.FILES[1])].height))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.display[0].blit(shd,(self.flrects[len(res.FILES[1])].x + 5,self.flrects[len(res.FILES[1])].y + 5))
			pygame.draw.rect(self.display[0], col, self.flrects[len(res.FILES[1])])
			self.display[1].blit(self.fnt['DEFAULT'].render(dtb.MENU[61], True, (0,0,0)), (self.windoww - 330, (120 + (len(res.FILES[1]) * 51)) * 2))
		#CHAPTERS MENU
		if self.mnu == 4:
			for i in range(res.FILES[1][res.ID] + 1):
				if self.lopt == i:
					if self.chrects[i].width < 250:
						self.chrects[i].width += 4
						self.chrects[i].x -= 4
					col = (255,255,0)
				else:
					if self.chrects[i].width > 230:
						self.chrects[i].width -= 4
						self.chrects[i].x += 4
					col = (255,255,255)
				shd = pygame.Surface((self.chrects[i].width,self.chrects[i].height))
				shd.set_alpha(100)
				shd.fill((10,10,10))
				self.display[0].blit(shd,(self.chrects[i].x + 5,self.chrects[i].y + 5))
				pygame.draw.rect(self.display[0], col, self.chrects[i])
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[i][0], True, (0,0,0)), ((self.chrects[i].x + 10) * 2, (110 + (i * 51)) * 2))
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[i][1], True, (0,0,0)), ((self.chrects[i].x + 10) * 2, (130 + (i * 51)) * 2))
			#DELETE FILE
			if self.lopt == res.FILES[1][res.ID] + 1:
				if self.flrects[res.FILES[1][res.ID] + 1].width < 250:
					self.flrects[res.FILES[1][res.ID] + 1].width += 4
					self.flrects[res.FILES[1][res.ID] + 1].x -= 4
				col = (255,255,0)
			else:
				if self.flrects[res.FILES[1][res.ID] + 1].width > 230:
					self.flrects[res.FILES[1][res.ID] + 1].width -= 4
					self.flrects[res.FILES[1][res.ID] + 1].x += 4
				col = (255,255,255)
			shd = pygame.Surface((self.chrects[res.FILES[1][res.ID] + 1].width,self.chrects[res.FILES[1][res.ID] + 1].height))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.display[0].blit(shd,(self.chrects[res.FILES[1][res.ID] + 1].x + 5,self.chrects[res.FILES[1][res.ID] + 1].y + 5))
			pygame.draw.rect(self.display[0], col, self.chrects[res.FILES[1][res.ID] + 1])
			self.display[1].blit(self.fnt['DEFAULT'].render('excluir', True, (0,0,0)), (self.windoww - 330, (120 + ((res.FILES[1][res.ID] + 1) * 51)) * 2))
		#RECAP
		if self.mnu == 6:
			lt = 0
			self.display[0].blit(pygame.image.load(res.BACKG_PATH + 'recap_' + str(res.CHAPTER) + '.png'), (0, -self.scroll))
			for y in dtb.CHAPTERS[res.CHAPTER - 1][2]:
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (0,0,0)), (101 * rztxt, 1 + (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (0,0,0)), (102 * rztxt, 2 + (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				self.display[1].blit(self.fnt['DEFAULT'].render(y, True, (255,255,255)), (100 * rztxt, (360 - math.floor(self.scroll * 2) + lt) * rztxt))
				lt += 20
			self.scroll += 1 * self.FPS
			if self.scroll > 340 + lt or self.skip == True:
				if self.winbar == 100:
					self.msc.fadeout(5000)
					self.mnu = 6
		if self.mnu == 7:
			if self.winbar < int(self.windowh/2):
				self.winbar += 10 * self.FPS
			if self.winbar == int(self.windowh/2):
				self.classrun = False
		#GRADIENT
		for i in range(len(self.grd)):
			self.display[1].blit(self.grd[i],(0,i))
			self.display[1].blit(self.grd[i],(0,self.windowh - i))
		#BLACK BARS
		if self.mnu in [3,4] and self.winbar > 100:
			self.winbar -= 10 * self.FPS
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,0,self.windoww,self.winbar))
		pygame.draw.rect(self.display[1], (0, 0, 0), pygame.Rect(0,self.windowh - self.winbar,self.windoww,self.winbar))
		#INFO
		if self.mnu > 1 and self.mnu < 6:
			'''self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[0] + ' ' + res.VERSION + ':' + str(self.glock.get_fps()), True, (240,240,240)), ((-35 + int(self.displayzw/(self.displayzh/self.winbar))), (-35 + self.winbar)))
			if self.stime > 0:
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[1], True, (240,240,240)), ((self.windoww - 140 - int(self.displayzw/(self.displayzh/self.winbar))), (self.windowh + 35) - self.winbar))'''
			self.display[1].blit(self.fnt['MINI'].render(dtb.ABOUT[0][:10], True, (240,240,240)), (50,25))
			self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[0][12:] + ' ' + res.VERSION + ':' + str(self.glock.get_fps()), True, (240,240,240)), (50,50))
			if self.stime > 0:
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ABOUT[1], True, (240,240,240)), (self.windoww - 200,self.windowh - 35))
			#HOLIDAYS
			for i in dtb.HOLIDAYS:
				if self.holiday.month == i[0] and self.holiday.day == i[1]:
					self.display[1].blit(self.fnt['DEFAULT'].render(i[2], True, (240,240,240)), (self.windoww - 240, 65))
			#SECRETS
			if self.stime > 0: self.stime -= 1 * self.FPS
			if self.stime <= 0:
				if self.sscroll > -20 - self.fnt['DEFAULT'].size(self.stext)[0]:
					self.sscroll -= 3 * self.FPS
					self.display[1].blit(self.fnt['DEFAULT'].render(self.stext, True, (240,240,240)),(self.sscroll,self.windowh - 50))
				else:
					self.sscroll = self.windoww + 20
					self.stext = dtb.TSECRETS[random.randint(0,len(dtb.TSECRETS) - 1)]
					self.stime = random.randint(600,1000)
		#WAIT
		if self.mnu > 0 and self.mnu < 7:
			if self.wait > 0: self.wait -= 1 * self.FPS
			prb = round(random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv > 0: self.random()
		#LOAD GAME RECAP
		if self.mnu == 8:
			if self.wait > 0: self.wait -= 1 * self.FPS
			prb = round(random.randint(0,100))
			if prb > 50 and self.wait == 0 and self.tv == 0:
				self.msc.play(res.SONGS['FATE_OCCURRENCES'],-1)
				self.ton.stop()
				self.mnu = 5
		#DRAW SURFACES
		self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (0, 0))
		#self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (0, 0))
		self.screen.blit(self.display[1], (0, 0))
		#MOUSE
		if res.MOUSE == 1:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'), pygame.mouse.get_pos())
		#UPDATE
		pygame.display.flip()
		self.glock.tick(int(60/self.FPS))
		
	def run(self):
		if self.mnu < 3 and self.mnu != -1: self.load += 1
		#SPLASH
		if self.mnu == -1:
			self.events()
			self.screen.fill((0,0,0))
			srf = pygame.image.load('splash.png')
			sz = srf.get_rect()
			self.screen.blit(srf, (int(self.windoww/2) - int(sz.width/2),int(self.windowh/2) - int(sz.height/2)))
			pygame.display.flip()
		#LOGO
		elif self.mnu < 2:
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
			if self.mnu == 0: srf.blit(pygame.image.load(res.BACKG_PATH + 'logo.png'), (0, 0))
			if self.mnu == 1: srf.blit(pygame.image.load(res.BACKG_PATH + 'source.png'), (0, 0))
			srf.set_alpha(self.logoalpha)
			self.screen.blit(srf, (int(self.windoww/2) - 300,int(self.windowh/2) - 200))
			pygame.display.flip()
		elif self.mnu == 2:
			self.loading()
		else:
			if res.GAMETIME == 0:
				self.intro()
			else:
				self.events()
				self.menu()

class Game:
	def __init__(self):
		#GAME SETTINGS
		self.windoww = pygame.display.get_window_size()[0]
		self.windowh = pygame.display.get_window_size()[1]
		self.displayzw = int(self.windoww/res.GSCALE)
		self.displayzh = int(self.windowh/res.GSCALE)
		self.displayx = 0
		self.displayy = 0
		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((self.displayzw, self.displayzh)), pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA),
			pygame.Surface((self.displayzw, self.displayzh), pygame.SRCALPHA), pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
		self.glock = pygame.time.Clock()
		self.FPS = 60
		self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', 30), 'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 30),
			'MININFO': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 25), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 15),
			'CONTROLKEYS': pygame.font.Font(res.FONTS_PATH + 'controlkeys.ttf', 15)}
		self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)
		self.driving = 0
		self.sleepin = False
		self.tilemation = 0
		self.room = ''
		self.rectdebug = False
		self.classrun = 1
		self.scrmov = None
		self.scrspd = 0
		self.hpctrl = []
		self.waitime = 0
		self.waitlst = [['advice',432000],['rain',3600]]
		#MIXER CHANNELS
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		self.ch_sfx = pygame.mixer.Channel(0) #for quick sounds
		self.ch_sfx.set_volume(res.SFX)
		self.ch_msc = pygame.mixer.Channel(1) #for background ambience loops
		self.ch_msc.set_volume(res.MSC)
		self.ch_ton = pygame.mixer.Channel(2) #for long sounds or jingles
		self.ch_ton.set_volume(res.SFX)
		self.ch_rad = pygame.mixer.Channel(3) #for radio songs
		self.ch_rad.set_volume(0.1)
		self.ch_stp = pygame.mixer.Channel(4) #for steps sounds
		self.ch_stp.set_volume(res.SFX)
		self.ch_rng = pygame.mixer.Channel(5) #for phone ringtone
		self.ch_rng.set_volume(res.MSC)
		self.ch_dlg = pygame.mixer.Channel(6) #for dialog text sound
		self.ch_dlg.set_volume(res.SFX)
		#MENU VARIABLES
		self.rad = GUI.Radio()
		self.pbr = GUI.PhoneBar()
		self.dev = self.rad
		self.inv = GUI.Inventory((self.displayzw,self.displayzh))
		self.shpmnu = GUI.Shop()
		self.nmenu = GUI.Naming()
		self.read = None
		self.dmenu = None
		self.opt = 1
		self.lopt = 0
		self.mnu = 1
		self.exvar = 0
		self.inventory = 0
		self.invfade = self.displayzw + 400
		self.phone = 0
		self.phofa = 0
		self.nb = ''
		self.shp = False
		self.basket = []
		self.products = []
		self.extract = [0,0,0,0,0,0]
		self.promo = 0
		self.build = ''
		self.winbar = int(self.displayzh/2)
		self.grd = []
		for g in range(200):
			srf = pygame.Surface((self.windoww,1),pygame.SRCALPHA)
			srf.fill((0,0,0,200 - g))
			self.grd.append(srf)
		self.rdscroll = 10
		self.nottxt = ''
		self.notcol = (0,0,0)
		self.notx = 0
		self.tutorial = {'TEXT': [], 'OUTPUT': [], 'FADE': 0, 'TIME': 0, 'WAIT': 0, 'NEXT': '','GO': 0}
		self.cityname = ''
		#DIALOG VARIABLES
		self.dlg = []
		self.dlgfa = 500
		self.dlgy = 0
		self.dmginfo = ''
		self.dmgy = 200
		self.dlgspd = res.SPEED
		self.speakin = 0
		#BATTLE VARIABLES
		self.equip = []
		self.battle = False
		self.effttack = None
		self.effgif = 0
		self.btime = 100
		self.bbg = ''
		self.bbm = 0
		self.bba = 0
		self.bbd = False
		self.obstacles = False
		self.hits = 0
		self.tdmg = 0
		self.hpl = 0
		self.tbt = 0
		self.turn = -1
		self.aim = pygame.Rect(300,200,30,30)
		self.barhp = []
		self.barpp = []
		self.barxp = []
		self.dices = []
		#BARS
		x = 0
		for i in res.PARTY[res.FORMATION]:
			#HP BAR
			res.CHARACTERS[i]['HP'] = dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
			self.barhp.append(int(100/(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]/res.CHARACTERS[i]['HP'])))
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
			x += 1
		#PLAYER
		self.player = []
		for i in res.PARTY[res.FORMATION]: pass
		for i in range(2):
			self.player.append({'RECT': pygame.Rect(res.PX,res.PY,20,20),'SPEED': 0,'JUMP': 0,'GRAVITY': -5,'STEP': 10,'SWIM': None,'HEAT': res.TEMPERATURE,
		'HEAD': 'BLANKD_' + res.CHARACTERS[i]['HAIR'] + res.CHARACTERS[i]['SKIN'],
		'SPRITE': 'STANDD_' + res.CHARACTERS[i]['COSTUME'] + res.CHARACTERS[i]['SKIN'],
		'GIF': 0.0,'BLINK': 100,'DMGTIM': 100,'SHK': 0,'DIRECTION': 3,'PAUSE': 0,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','PLAYING': True,'NODES': [],'HOLD': None})
		self.player[0]['PLAYING'] = True
		for i in range(len(self.player)):
			self.objects = [[0,i,self.player[i]['RECT'].y]]
		self.tilrect = []
		self.tilhide = False
		self.tilalpha = 0
		#MAP VARIABLES
		self.en = []
		self.foe = []
		self.fig = []
		self.mrc = []
		self.npcs = []
		self.vehicles = []
		self.portals = []
		self.signs = []
		self.lights = []
		self.particles = []
		self.portalgo = {}
		#BUTTONS
		self.buttons = [pygame.Rect(102,self.windowh - 264,80,80),pygame.Rect(102,self.windowh - 100,80,80),pygame.Rect(20,self.windowh - 182,80,80),pygame.Rect(184,self.windowh - 182,80,80),pygame.Rect(self.windoww - 190,self.windowh - 100,80,80),pygame.Rect(self.windoww - 100,self.windowh - 100,80,80),pygame.Rect(self.windoww - 190,40,80,80),pygame.Rect(self.windoww - 100,40,80,80)]
		#STARTING GAME
		if res.CHAPTER == 3 and res.SCENE == 0:
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
			self.rendermap('hauntedhouse_0')
			self.phone = 15
			self.mnu = 1
		else:
			self.rendermap('1urban_0')
			self.transiction(False,0)

	def people(self, i, t):
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
			if t == True:
				if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 23: visible = False
			#MAP ICON
			if res.MAP == 0:
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
			else:
				xsp = 0
				#BODY AND SHADE
				if i['SWIM'] == None:
					if i['SPRITE'].startswith('SEAT') == False or i['SPRITE'].startswith('DRIVE') == False: pass
						#self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'Items/it_shade.png'), (i['RECT'].x - self.cam.x - 1,i['RECT'].y - self.cam.y + 7))
					img = res.SPRITES[i['SPRITE']][math.floor(i['GIF'])]
					if res.TIME[0] < 12:
						tms = (12 - res.TIME[0]) * 2
						sxx = i['RECT'].x - self.cam.x - tms + 5
					else:
						tms = (res.TIME[0] - 12) * 2
						sxx = i['RECT'].x - self.cam.x
					if tms < 5: tms = 5
					shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,7))
					shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					shd.set_alpha(100)
					self.display[0].blit(shd, (sxx,i['RECT'].y - self.cam.y ))
					if visible == True:
						if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
						self.display[0].blit(img, (i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2),i['RECT'].y - self.cam.y - 10 - int(i['JUMP'])))
				#SWIMMING
				else:
					xsp += 21
					i['SWIM'] += 0.1
					if i['SWIM'] > 1.5: i['SWIM'] = 0.0
					self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'water_' + str(math.floor(i['SWIM'])) + '.png'), (i['RECT'].x - self.cam.x + 4,i['RECT'].y - self.cam.y + 9))
			if res.MAP > 0:
				#HOLDING ITEM
				if i['HOLD'] != None:
					xx = -5; yy = -20
					if i['DIRECTION'] in [1,2,8]: xx = 10
					if i['DIRECTION'] in [4,5,6]: xx = -20
					if i['DIRECTION'] in [2,3,4]: yy = 5
					if i['DIRECTION'] in [6,7,8]: yy = -30
					self.tilrect[2][i['HOLD']][1].x = i['RECT'].x + xx
					self.tilrect[2][i['HOLD']][1].y = i['RECT'].y + yy
				#EXTRA SPACEMENT
				if i['SPEED'] == 0 and i['GIF'] >= 1.0 and i['GIF'] < 3.0: xsp += 1
				if i['SPEED'] > 0:
					if i['GIF'] >= 0.0 and i['GIF'] < 1.0: pass
					elif i['GIF'] >= 4.0 and i['GIF'] < 5.0: pass
					else: xsp += 1
				if i['JUMP'] > 0: xsp = 1
				if i['HEAD'].startswith('BLANKDD'): xsp += 1
				#HEAD
				if i['BLINK'] < 2 and i['DIRECTION'] < 6 and i['GRAVITY'] == -5 and i['JUMP'] == 0:
					try: img = res.SPRITES[i['HEAD']][1]
					except: img = res.SPRITES[i['HEAD']][0]
				else: img = res.SPRITES[i['HEAD']][0]
				if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
				xx = i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2)
				yy = i['RECT'].y - self.cam.y - 21 + xsp - i['JUMP']
				if res.TIME[0] < 12:
					tms = 12 - res.TIME[0]
					sxx = xx - tms
				else:
					tms = res.TIME[0] - 12
					sxx = xx
				shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,5))
				shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
				shd.set_alpha(100)
				self.display[0].blit(shd, (sxx,yy + 21))
				if visible == True:
					self.display[0].blit(img, (xx,yy))
				#MOUTH
				if self.speakin == i['RECT'] and i['DIRECTION'] < 6:
					if i['DIRECTION'] == 1: ex1 = (0,1); ex2 = (1,1)
					elif i['DIRECTION'] == 2: ex1 = (4,6); ex2 = (4,5)
					elif i['DIRECTION'] == 3: ex1 = (4,6); ex2 = (5,6)
					elif i['DIRECTION'] == 4: ex1 = (3,5); ex2 = (4,5)
					elif i['DIRECTION'] == 5: ex1 = (8,9); ex2 = (8,8)
					pygame.draw.line(self.display[0],(81,9,0),(xx + ex1[0],yy + 9),(xx + ex1[1],yy + 9))
					if math.floor(i['GIF']) == 0: pygame.draw.line(self.display[0],(183,63,47),(xx + ex2[0],yy + 10),(xx + ex2[1],yy + 10))
					if math.floor(i['GIF']) == 1: pygame.draw.line(self.display[0],(183,63,47),(xx + ex2[0],yy + 9),(xx + ex2[1],yy + 9))
				#ACCESORIES
				if t == True and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ACCESORIES'] != None and int(i['DIRECTION']) < 6:
					if i['DIRECTION'] == 1: ex = 8
					elif i['DIRECTION'] == 2: ex = 3
					elif i['DIRECTION'] == 3: ex = 2
					elif i['DIRECTION'] == 4: ex = 1
					elif i['DIRECTION'] == 5: ex = 1
					else: ex = 0
					if i['DIRECTION'] == 1: acc = pygame.transform.flip(pygame.image.load(res.SPRITES_PATH + 'Characters/' + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ACCESORIES'] + '_1.png'),True,False)
					elif i['DIRECTION'] == 5: acc = pygame.image.load(res.SPRITES_PATH + 'Characters/' + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ACCESORIES'] + '_1.png')
					else: acc = pygame.image.load(res.SPRITES_PATH + 'Characters/' + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ACCESORIES'] + '_0.png')
					if self.turn == -6: acc.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					self.display[0].blit(acc, (i['RECT'].x - self.cam.x + math.floor((20 - img.get_rect().width)/2) + ex,i['RECT'].y - self.cam.y - 21 + xsp - int(i['JUMP']) + 7))
					
	def pet(self, i):
		#ANIMATION
		if self.player[0]['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(res.SPRITES[i['SPRITE']]): i['GIF'] = 0
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			
		if res.TIME[0] < 12:
			tms = (12 - res.TIME[0]) * 2
			sxx = i['RECT'].x - self.cam.x - tms + 5
		else:
			tms = (res.TIME[0] - 12) * 2
			sxx = i['RECT'].x - self.cam.x
		if tms < 5: tms = 5
		img = i['SPRITE'][math.floor(i['GIF'])]
		shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,7))
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
				if i['FILE'].startswith('DOG'):
					do = random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit':
							i[i['FILE'] + '_STAND']
							i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand':
							i[i['FILE'] + '_SIT']
							i['MOVE'] = 'sit'
					elif do == 1:
						i[i['FILE'] + '_WALK']
						i['MOVE'] = 'walk'
						dl = [1,5]
						i['DIRECTION'] = dl[random.randint(0,1)]
				elif i['FILE'].startswith('PIGEON'):
					do = random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit':
							i[i['FILE'] + '_STAND']
							i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand':
							i[i['FILE'] + '_SIT']
							i['MOVE'] = 'sit'
					elif do == 1:
						i[i['FILE'] + '_WALK']
						i['MOVE'] = 'walk'
						dl = [1,5]
						i['DIRECTION'] = dl[random.randint(0,1)]
				i['TIME'] = 20

	def enemy(self, i):
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
		img = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (i['FILE']) + '_mini.png')
		
		if res.TIME[0] < 12:
			tms = (12 - res.TIME[0]) * 2
			sxx = i['RECT'].x - self.cam.x - tms + 5
		else:
			tms = (res.TIME[0] - 12) * 2
			sxx = i['RECT'].x - self.cam.x
		if tms < 5: tms = 5
		shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,7))
		shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
		shd.set_alpha(100)
		self.display[0].blit(shd, (sxx, i['RECT'].y - self.cam.y))
		for b in res.BESTIARY:
			if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
				img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
		self.display[0].blit(img, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
		if i['PATH'] == 'notice': self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'notice.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - 30))
		#REPELLENT
		rplt = False
		for c in res.PARTY[res.FORMATION]:
			if res.CHARACTERS[c]['HEALTH'] == 2: rplt = True
		#MOVEMENT
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
				if rplt == True:
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
		#BATTLE ENTER
		if self.colide(i['RECT'], self.player[0]['RECT']) == True and i['DIRECTION'] > 0 and self.battle == False and self.dlgfa == 500:
			if i['FIGHTING'] == False and rplt == False:
				if i['TYPE'] != 'mercenary': self.foe.append(i)
				else: self.mrc.append(i)
				i['FIGHTING'] = True
				if (len(self.foe) + len(self.mrc)) == 1:
					for b in res.BESTIARY:
						if b['N'] == i['FILE'] and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
							self.turn = -6
							break
					self.notx = 0
					if self.phone > 0: self.turn = -2
					if self.inventory > 0: self.turn = -2
					if self.turn != -6: self.turn = -self.facing(i,self.player[0])
					self.fight()

	def npc(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,20,20)

		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if i['TYPE'] not in [1,5] and i['RECT'].width == 0: self.people(i,False)
		elif i['TYPE'] == 3:
			img = pygame.image.load(res.SPRITES_PATH + 'mercator.png')
			self.display[0].blit(img, (rect.x - self.cam.x - math.floor(img.get_rect().width/2) + 10, rect.y - self.cam.y - int(img.get_rect().height/2) - 3))
		elif i['TYPE'] == 5:
			self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'obj_' + str(i['INDEX']) + str(i['WHO']) + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y - 10))
			if self.sleepin == True and i['INDEX'] == 1: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'char_0_rest.png'), (rect.x - self.cam.x + 5, rect.y - self.cam.y + 5))
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
		if self.battle == False and i['TYPE'] == 0 and i['RECT'].width == 0 and i['FOLLOW'] == None:
			if i['MOVE'] == 'horizontal':
				i['SPEED'] = 1
				if i['DIRECTION'] not in [1,5]:
					i['DIRECTION'] = 1

				if i['TIME'] == 0:
					if i['DIRECTION'] == 1: i['DIRECTION'] = 5
					elif i['DIRECTION'] == 5: i['DIRECTION'] = 1
					i['TIME'] = 30
				i['TIME'] -= 1
			elif i['MOVE'] == 'nodeon':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(rect,n['RECT']):
						if n['GOING'] == 1: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'nodeoff':
				i['SPEED'] = 1
				for n in self.nodes:
					if self.colide(rect,n['RECT']):
						if n['GOING'] == 0: i['DIRECTION'] = n['TYPE']
			elif i['MOVE'] == 'fixed': i['SPEED'] = 0
		#MOVEMENT
		if self.player[0]['PAUSE'] < 3:
			if i['SPEED'] > 0:
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKR_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKRD_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKD_' + i['INDEX'][3:6]; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKLD_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']; i['RECT'].y += i['SPEED']
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKL_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKLU_' + i['INDEX'][3:6]; i['RECT'].x -= i['SPEED']; i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKU_' + i['INDEX'][3:6]; i['RECT'].y -= i['SPEED']
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'WALKRU_' + i['INDEX'][3:6]; i['RECT'].x += i['SPEED']; i['RECT'].y -= i['SPEED']
			elif i['MOVE'] == 'stand':
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'STANDRU_' + i['INDEX'][3:6]
				i['MOVE'] = 'fixed'
			elif i['MOVE'] == 'seat':
				if i['DIRECTION'] == 1: i['HEAD'] = 'BLANKR_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['HEAD'] = 'BLANKRD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['HEAD'] = 'BLANKD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['HEAD'] = 'BLANKLD_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['HEAD'] = 'BLANKL_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['HEAD'] = 'BLANKLU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['HEAD'] = 'BLANKU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['HEAD'] = 'BLANKRU_' + i['INDEX'][0:3] + i['INDEX'][5]; i['SPRITE'] = 'SEATRU_' + i['INDEX'][3:6]
			else:
				if i['DIRECTION'] == 1: i['SPRITE'] = 'STANDR_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 2: i['SPRITE'] = 'STANDRD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 3: i['SPRITE'] = 'STANDD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 4: i['SPRITE'] = 'STANDLD_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 5: i['SPRITE'] = 'STANDL_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 6: i['SPRITE'] = 'STANDLU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 7: i['SPRITE'] = 'STANDU_' + i['INDEX'][3:6]
				if i['DIRECTION'] == 8: i['SPRITE'] = 'STANDRU_' + i['INDEX'][3:6]

			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
					if self.colide(rect,i['FOLLOW']):
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
		if self.colide(self.player[0]['RECT'], rect) == True and self.portalgo == {} and i['WHO'] != None:
			if i['TALKING'] == False:
				if self.battle == False and self.speakin != rect and self.dlgfa > 0 and isinstance(i['TYPE'],str) == False:
					self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - rect.height * 2))
					self.hpctrl = dtb.HINTS['NPC_DIALOG']
				if isinstance(i['TYPE'],str) and i['TYPE'].startswith('scene'):
					if res.SCENE == int(i['TYPE'][5]) - 1:
						res.SCENE = int(i['TYPE'][5])
						act = True
					else: act = False
				else:
					act = False
					if self.pressed[4][0]:
						self.player[0]['PAUSE'] = 1
						act = True
				if act == True:
					i['FOLLOW'] = None
					i['TALKING'] = True
					#NPC DIALOG
					if i['TYPE'] in [0,None] or isinstance(i['TYPE'],str):
						if self.dlgfa > 0:
							i['SPEED'] = 0
							if i['DIRECTION'] == 1: i['HEAD'] = 'TALKR_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 2: i['HEAD'] = 'TALKRD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 3: i['HEAD'] = 'TALKD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 4: i['HEAD'] = 'TALKLD_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 5: i['HEAD'] = 'TALKL_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 6: i['HEAD'] = 'TALKLU_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 7: i['HEAD'] = 'TALKU_' + i['INDEX'][0:3] + i['INDEX'][5]
							if i['DIRECTION'] == 8: i['HEAD'] = 'TALKRU_' + i['INDEX'][0:3] + i['INDEX'][5]
							#DIALOG
							if i['WHO'] != 'REWARD':
								if isinstance(i['WHO'], int): self.dialog(dtb.DIALOGS['NPC_' + str(i['WHO'])][res.DLGSAV[i['WHO']]].copy(),rect)
								elif len(dtb.DIALOGS[i['WHO']]) > res.DLGSAV[i['WHO']]:
									self.dialog(dtb.DIALOGS[i['WHO']][res.DLGSAV[i['WHO']]].copy(),rect)
								else: self.dialog(dtb.DIALOGS['EMPTY CHEST'])
							#GET REWARD
							else:
								btls = None
								for b in res.PARTY[res.FORMATION]:
									for it in ['bottle100','bottle250']:
										btls = self.inv.find(b,it)
										if btls != None and int(btls[1]) > 0: break
									if btls != None and int(btls[1]) > 0: break
								if btls != None:
									if int(btls[1]) > 150: self.dialog(dtb.DIALOGS['REWARD'][3].copy(),rect)
									elif int(btls[1]) > 90: self.dialog(dtb.DIALOGS['REWARD'][2].copy(),rect)
									elif int(btls[1]) > 0: self.dialog(dtb.DIALOGS['REWARD'][1].copy(),rect)
									if self.notx == 0:
										src = self.inv.get_property('credit_card','wallet')
										src += btls[1]
										self.ch_sfx.play(res.SOUND['CASH_GET'])
										self.notification('Adquiriu $' + btls[1],(255, 255, 255))
										self.dlg = []
										btls[1] = '000'
								else: self.dialog(dtb.DIALOGS['REWARD'][0].copy(),rect)
					#MARKET CASHIER
					elif i['TYPE'] == 2:
						if i['WHO'].startswith('DRITHR'):
							if self.driving == 0:
								if self.dlgfa > 0: self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),rect)
							else:
								self.products = []
								for p in dtb.PRODUCTS[int(i['INDEX'])][0]:
									self.products.append(p)
								self.shp = True
								self.lopt = 0
								self.opt = 0
								self.mnu = 2
						elif self.basket == []:
							if self.dlgfa > 0: self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),rect)
						else:
							self.products = []
							for p in dtb.PRODUCTS[int(i['INDEX'])][0]:
								self.products.append(p)
							self.shp = True
							self.lopt = 0
							self.opt = 0
							self.mnu = 2
					#DEPOSIT ITEMS
					elif i['TYPE'] == 4:
						self.dialog(dtb.DIALOGS['DEPOSIT'][0],rect)
						self.inventory = 2
						self.ch_sfx.play(res.SOUND['INVENTORY_OPEN'])
						self.invfade = 0
						self.opt = 0
						self.lopt = 1
						self.mnu = 0
						self.exvar = 0
					elif i['TYPE'] == 5:
						#ATM MACHINE
						if i['INDEX'] == 0:
							self.extract = [0,0,0,0,0,0]
							self.opt = 0
							self.lopt = 1
							self.mnu = 0
							self.exvar = 0
						#BED
						elif i['INDEX'] == 1:
							self.sleepin = not self.sleepin
							if self.sleepin == False: self.player[0]['PAUSE'] = 1
							else: self.player[0]['PAUSE'] = 0
						#TRASH CAN
						elif i['INDEX'] == 2:
							self.inventory = 3
							self.ch_sfx.play(res.SOUND['INVENTORY_OPEN'])
							self.invfade = 0
							self.opt = 0
							self.lopt = 1
							self.mnu = 0
						#PHONE
						elif i['INDEX'] == 3:
							src = None
							for i in res.PARTY[res.FORMATION]:
								src = self.inv.find(i,'credit_card')
								if src == None:
									src = self.inv.find(i,'wallet')
							if src != None and int(src[1]) > 0:
								res.MONEY -= 1
								self.phone = 3
								self.wait()
								dtb.CALLHIST.insert(0,[dtb.CONTACTS[self.lopt][1],False])
								self.dialog(dtb.DIALOGS[dtb.CONTACTS[self.lopt][1]][0],rect)
							else:
								self.dialog([dtb.MENU[18]],rect)
						#BATTERY PLUG
						elif i['INDEX'] == 4:
							print('here')
							if self.inv.find(res.PARTY[res.FORMATION][0],'charger') != None: self.ch_sfx.play(res.SOUND['MENU_GO']); #res.BATTERY = 360
							else: self.ch_sfx.play(res.SOUND['MENU_GO']); self.dialog(dtb.DIALOGS['PLUG'])
						#REFUEL
						elif i['INDEX'] == 5 and self.driving > 0:
							while res.GAS < self.vehicles[self.driving - 1]['CAPACITY']:
								res.GAS += 1
								self.run()
					#PRODUCTS AND MERCATOR
					elif i['TYPE'] != None:
						if i['TYPE'] == 3:
							self.dialog(dtb.DIALOGS['MERCATOR'][0],rect)
							self.basket = []
							p = 0
							for u in res.PARTY[res.FORMATION]:
								self.basket.append([])
								for y in range(len(res.INVENTORY[u])):
									for x in range(len(res.INVENTORY[u][y])):
										if res.INVENTORY[u][y][x][0] != '_' and dtb.ITEMS[res.INVENTORY[u][y][x][0]][2] != 0:
											self.basket[p].append([y,x])
								p += 1
						if res.DATE[3] == dtb.PRODUCTS[0][1]:
							self.promo = dtb.PRODUCTS[0][2]
						self.products = []
						for p in dtb.PRODUCTS[0][0]:
							self.products.append(p)
						self.shp = True
						self.player[0]['PAUSE'] = 1
						self.lopt = 0
						self.opt = 0
						self.mnu = 2
		else: i['TALKING'] = False

	def vehicle(self, i):
		rect = pygame.Rect(i['RECT'].x - 5,i['RECT'].y - 5,60,30)
		if self.driving == i['N'] + 1:
			i['RECT'].x = self.player[0]['RECT'].x
			i['RECT'].y = self.player[0]['RECT'].y
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'moto_' + str(i['INDEX']) + '_walkL.png'), (rect.x - self.cam.x + 10, rect.y + rect.height - self.cam.y - 30))
		#MOVEMENT
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
		snd = pygame.mixer.Sound(res.SFX_PATH + 'step_vehicle.wav')
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
		if self.colide(self.player[0]['RECT'], rect) == True:
			if self.battle == False and self.driving == 0:
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - int(rect.height/2)))
				self.hpctrl = dtb.HINTS['VEHICLE_USE']
			if self.pressed[4][0] and self.driving == 0 and self.inventory == 0 and self.phone == 0 and self.shp == False:
				trigger = True
				self.driving = i['N'] + 1
				self.player[0]['RECT'].x = rect.x
				self.player[0]['RECT'].y = rect.y
				i['MOVE'] = 'fixed'
				'''self.displayzw = 1200
				self.displayzh = 800
				self.display = pygame.Surface((1200, 800))
				self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)'''

	def portal(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,30,30)
		goto = False
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			if self.colide(self.player[0]['RECT'], rect) == True and self.winbar > 0: spr = '1'
			else: spr = '0'
			if res.MAP > 0:
				if i['RECT'].width == 24: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_0' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
				if i['RECT'].width == 48: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_1' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
			else: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		#ENTERING DOOR
		if self.colide(self.player[0]['RECT'], rect) == True and self.winbar == 0 and self.portalgo == {}:
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
			else: goto = True

			if i['RECT'].width == 24 and self.driving > 0: goto = False
			elif i['RECT'].width == 48: goto = False

		if goto == True:
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
				self.ch_ton.play(res.SOUND['TREASURE'])
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
			#GOTO ROOM
			else:
				self.portalgo = [{'MATCH': None, 'RECT' : pygame.Rect(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y,i['RECT'].width,i['RECT'].height)},{}]
				self.portalgo[1] = self.player[0].copy()
				self.portalgo[1]['RECT'].x -= self.cam.x
				self.portalgo[1]['RECT'].y -= self.cam.y
				self.transiction(True, int(self.displayzh/2), spd)
				self.rendermap(i['MAP'])
				self.portalgo[0]['MATCH'] = i['MATCH']
				while self.portalgo[0]['MATCH'] != None: self.run()
				if i['TYPE'] > 0:
					self.ch_ton.play(res.SOUND['DOOR_CLOSE'])
				if i['MUSIC'] == 'outside': self.ch_msc.set_volume(1.0)
				elif i['MUSIC'] == 'inside': self.ch_msc.set_volume(0.2)
				elif i['MUSIC'] != None: self.ch_msc.play(res.SOUND[i['MUSIC'].upper()],-1)
				if self.cityname == '':
					self.transiction(False, 0, spd)
				else:
					self.transiction(False, 50, 5)
					for r in range(100): self.run()
					self.transiction(False, 0, 5)
					self.cityname = ''
				self.portalgo = {}
				for p in self.player:
					p['RECT'].x = i['PX']
					p['RECT'].y = i['PY']
					p['PAUSE'] = 0

	def colide(self, i1, i2):
		cld = False
		if isinstance(i2, list):
			ind = 0
			for i in i2[2]:
				if self.facing(i1,i[1]) == 2:
					cld = pygame.Rect.colliderect(i1['RECT'],i[1])
					if cld == True and i1['JUMP'] == 0:
						#HOLD OBJECT
						if i[0] == 'HOLD':
							self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (i[1].x - self.cam.x + int(i[1].width/2) - 5, i[1].y - self.cam.y - i[1].height))
							if self.pressed[4][0] and self.player[0]['HOLD'] == None:
								self.player[0]['HOLD'] = ind
							cld = False
						#CARRY OBJECT
						elif i[0] == 'CARRY':
							if i1['DIRECTION'] == 1: i[1].x += i1['SPEED']
							if i1['DIRECTION'] == 3: i[1].y += i1['SPEED']
							if i1['DIRECTION'] == 5: i[1].x -= i1['SPEED']
							if i1['DIRECTION'] == 7: i[1].y -= i1['SPEED']
						break
				ind += 1
			#JUMP
			if cld == False:
				for i in i2[3]:
					if self.facing(i1,i[1]) == 2:
						cld = pygame.Rect.colliderect(i1['RECT'],i[1])
						if cld == True and i1['JUMP'] == 0: break
			#TURN ON OFF AREAS
			if cld == False and i1['PLAYING'] == True:
				for i in i2[4]:
					if self.facing(i1,i[1]) == 2:
						if pygame.Rect.colliderect(i1['RECT'],i[1]) and i1['JUMP'] == 0:
							if i[0].endswith('ON') and self.tilhide == False: self.tilhide = True
							if i[0].endswith('OFF') and self.tilhide == True: self.tilhide = False
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

	def events(self):
		for event in pygame.event.get():
			#KEYBOARD OR MOUSE INPUT
			if res.MOUSE < 2:
				ky = pygame.key.get_pressed()
				self.pressed = [ky[res.UP],ky[res.DOWN],ky[res.LEFT],ky[res.RIGHT],ky[res.ACT],ky[res.RUN],ky[res.BAG],ky[res.PHONE]]
			else:
				self.pressed = []
				mp = pygame.mouse.get_pos()
				mr = pygame.Rect(mp[0],mp[1],2,2)
				for i in self.buttons:
					if self.colide(mr,i):
						if event.type == pygame.MOUSEBUTTONDOWN: self.pressed.append([1,0])
						else: self.pressed.append([0,0])
					else: self.pressed.append([0,0])
				
			#EXIT
			if event.type == pygame.QUIT:
				if self.confirmation() == 1:
					self.classrun = 0
					pygame.quit()
					sys.exit()
					exit()
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.FPS = int(event.w/20)
			#MOUSE
			'''if res.MOUSE == 1:	
				mrect = pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png').get_rect()
				mrect.x = math.floor(pygame.mouse.get_pos()[0]/2)
				mrect.y = math.floor(pygame.mouse.get_pos()[1]/2)
				#self.pressed = pygame.mouse.get_pressed()

				if self.phone > 0 and self.dev.battery > 0:
					if self.phone == 1:
						#self.opt = -1
						#self.lopt = -1
						for i in range(len(self.dev.optrects)):
							if self.colide(mrect, self.dev.optrects[i]):
								self.lopt = math.floor(i/3)
								self.opt = i - (self.lopt * 3)
								if self.pressed[0]:
									self.phone = self.opt + (self.lopt * 3) + 2

									if self.phone == 2:
										self.mnu = 200
										self.opt = 80
										self.lopt = 80
									if self.phone == 7: res.recent_data(0)

									self.ch_sfx.play(res.SOUND['MENU_GO'])
									self.dev.scroll = 0
									self.opt = 0
									self.lopt = 0
									self.mnu = 0'''
			#DEBUG
			ky = pygame.key.get_pressed()
			if ky[pygame.K_DELETE]:
				self.dmenu = GUI.Debug()
				while self.dmenu.classrun:
					self.dmenu.run()
					self.screen.fill((0,0,0),pygame.Rect(1120,720,30,30))
					self.screen.blit(self.dmenu.draw(), (0, 0))
					pygame.display.update(pygame.Rect(0,0,1200,50))
				self.dmenu.command()
				if self.dmenu.dlg == 'sleep':
					self.sleepin = not self.sleepin
				elif self.dmenu.dlg == 'rectdebug':
					self.rectdebug = not self.rectdebug
				elif self.dmenu.dlg == 'pacify':
					self.en = []
				elif self.dmenu.dlg == 'storage':
					self.inventory = 2
					self.invfade = 0
					self.opt = 0
					self.lopt = 1
					self.mnu = 0
					self.exvar = 0
				elif self.dmenu.dlg != []:
					self.dialog(self.dmenu.dlg)
					self.dmenu.dlg = []
				if self.dmenu.goto != '':
					try: self.rendermap(self.dmenu.goto)
					except: self.ch_sfx.play(res.SOUND['ERROR'])
					self.transiction(False,0)
				self.dmenu = None
			#BATTLE OPTIONS
			if self.battle == True and self.phone == 0 and self.dlgfa > 0 and self.winbar == 100:
				if self.turn == len(res.PARTY[res.FORMATION]):
					self.fight()
					tp = 0
				else:
					if self.turn == 0: tp = 0
					elif self.turn >= len(self.player): tp = 0
					elif self.player[self.turn]['PLAYING'] == True: tp = self.turn
					else: tp = 0
				#CHOOSING WEAPON
				if self.mnu == 1:
					if self.pressed[2][tp]: self.equip[self.turn] -=1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[3][tp]: self.equip[self.turn] +=1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
				
					if self.equip[self.turn] < 0: self.equip[self.turn] = 7
					if self.equip[self.turn] > 7: self.equip[self.turn] = 0

					if self.pressed[4][tp]:
						#WEAPONS
						if self.equip[self.turn] < 4:
							if res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('melee'):
								self.ch_sfx.play(res.SOUND['MELEE'])
								self.mnu = 2
							elif res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('tool'):
								self.ch_sfx.play(res.SOUND['MELEE'])
								self.mnu = 2
							elif res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('gun') and self.barpp[self.turn][self.equip[self.turn]] > 0:
								self.ch_sfx.play(res.SOUND['GUN_TRIGGER'])
								self.mnu = 2
							elif res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('grenade'):
								self.ch_sfx.play(res.SOUND['MELEE'])
								self.mnu = 2
							else:
								self.ch_sfx.play(res.SOUND['ERROR'])
						#TACTICAL
						elif self.equip[self.turn] == 4:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.mnu = 2
						#DIALOG
						elif self.equip[self.turn] == 5:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.fight()
							self.turn += 1
						#GUARD
						elif self.equip[self.turn] == 6:
							self.ch_ton.play(res.SOUND['GUARD'])
							self.pres[self.turn] += 3
							self.turn += 1
							if self.turn == len(self.fig): self.fight()
						#RUN AWAY
						elif self.equip[self.turn] == 7:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.fight()
							if self.battle == True:
								self.turn = len(res.PARTY[res.FORMATION])
								self.fight()
				#USING WEAPON
				elif self.mnu == 2:
					if self.equip[self.turn] == 4:
						if self.pressed[2][tp]: self.opt -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][tp]: self.opt += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[4][tp]:
						#SHOT OR HIT
						if self.equip[self.turn] < 4:
							self.fight()
							self.turn += 1
							self.mnu = 1
							if self.turn == len(res.PARTY[res.FORMATION]): self.fight()
						#TACTICAL ATTACK
						elif self.equip[self.turn] == 4:
							ttl = self.opt
							for i in self.fig:
								self.equip[self.turn] = res.TACTICAL[ttl][self.turn]
								if self.equip[self.turn] != 0:
									if self.equip[self.turn] + 1 < 5:
										self.equip[self.turn] -= 1
										self.ch_sfx.play(res.SOUND['GUN_TRIGGER'])
										self.mnu = 2
										self.wait()
									if self.equip[self.turn] != 6: self.fight()
									else:
										self.pres[self.turn] += 3
										self.ch_sfx.play(res.SOUND['GUARD'])
								self.turn += 1
							for i in self.equip: i = 4
					#CANCEL MOVE
					if self.pressed[5][tp]:
						self.ch_sfx.play(res.SOUND['MISS'])
						self.mnu = 1
					if self.opt < 0: self.opt = len(res.TACTICAL) - 1
					if self.opt > len(res.TACTICAL) - 1: self.opt = 0
			#SHOP OPTIONS
			if self.shp == True:
				if self.pressed[2][0]: self.opt -= 1 ; self.ch_sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[3][0]: self.opt += 1 ; self.ch_sfx.play(res.SOUND['MENU_HOR'])
				if self.pressed[0][0]: self.lopt -= 1 ; self.ch_sfx.play(res.SOUND['MENU_VER'])
				if self.pressed[1][0]: self.lopt += 1 ; self.ch_sfx.play(res.SOUND['MENU_VER'])
				#PRODUCTS
				if self.mnu == 0:
					if self.pressed[4][0]:
						if self.lopt < len(self.products):
							for i in range(self.opt): self.basket.append(self.products[self.lopt])
							self.ch_sfx.play(res.SOUND['MENU_GO'])
						else:
							self.ch_sfx.play(res.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0
					if self.opt < 1: self.opt = 10
					if self.opt > 10: self.opt = 1
					if self.lopt < 0: self.lopt = len(self.products)
					if self.lopt > len(self.products): self.lopt = 0
				#CASHIER
				if self.mnu == 1:
					if self.pressed[4][0]:
						if self.lopt == 0:
							for i in self.basket:
								src = self.inv.get_property('credit_card','wallet')
								if scr != None and int(scr[1]) >= dtb.ITEMS[i][2]:
									if self.inv.space(res.PARTY[res.FORMATION][0]) == False:
										self.dialog(dtb.DIALOGS['MERCATOR'][2])
									elif self.confirmation() == 1:
										self.inv.add(res.PARTY[res.FORMATION][0],i)
										self.ch_sfx.play(res.SOUND['BUY'])
										scr[1] = str(int(scr[1]) - dtb.ITEMS[i][2] - int(dtb.ITEMS[i][2]/self.promo))
								else:
									self.ch_sfx.play(res.SOUND['ERROR'])
									self.dialog(dtb.DIALOGS['MERCATOR'][1])
						else:
							self.ch_sfx.play(res.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0
					if self.opt < 1: self.opt = 1
					if self.lopt < 0: self.lopt = 1
					if self.lopt > 1: self.lopt = 0
				#MERCATOR
				if self.mnu == 2:
					if self.pressed[4][0]:
						src = None
						for i in res.PARTY[res.FORMATION]:
							src = self.inv.find(i,'credit_card')
							if src == None:
								src = self.inv.find(i,'wallet')
								if src != None: break
							if src != None: break
						#BUYING ITEMS
						if self.opt == 0:
							if self.lopt == len(self.products):
								self.player[0]['PAUSE'] = 0
								self.ch_sfx.play(res.SOUND['MENU_BACK'])
								self.shp = False
								self.lopt = 0
							else:
								if src != None and int(src[1]) >= dtb.ITEMS[self.products[self.lopt]][2]:
									if self.inv.space(res.PARTY[res.FORMATION][0]) == False:
										self.dialog(dtb.DIALOGS['MERCATOR'][2])
									elif self.confirmation() == 1:
										self.inv.add(res.PARTY[res.FORMATION][0],self.products[self.lopt])
										self.ch_sfx.play(res.SOUND['BUY'])
										if self.promo > 0:
											src[1] = str(int(src[1]) - (dtb.ITEMS[self.products[self.lopt]][2] - int(dtb.ITEMS[self.products[self.lopt]][2]/self.promo)))
										else:
											src[1] = str(int(src[1]) - dtb.ITEMS[self.products[self.lopt]][2])
								else:
									self.ch_sfx.play(res.SOUND['ERROR'])
									self.dialog(dtb.DIALOGS['MERCATOR'][1])
						#SELLING ITEMS
						else:
							if self.lopt == len(self.basket[self.opt - 1]):
								self.player[0]['PAUSE'] = 0
								self.ch_sfx.play(res.SOUND['MENU_BACK'])
								self.shp = False
								self.lopt = 0
							elif self.confirmation() == 1 and src != None:
								src[1] = str(int(src[1]) + math.floor(dtb.ITEMS[res.INVENTORY[res.PARTY[res.FORMATION][self.opt - 1]][self.basket[self.opt - 1][self.lopt][0]][self.basket[self.opt - 1][self.lopt][1]][0]][2]/2))
								res.INVENTORY[res.PARTY[res.FORMATION][self.opt - 1]][self.basket[self.opt - 1][self.lopt][0]][self.basket[self.opt - 1][self.lopt][1]] = ['_','0000','_','_']
								del self.basket[self.opt - 1][self.lopt]
								self.ch_sfx.play(res.SOUND['SELL'])
					if self.opt < 0: self.opt = len(res.PARTY[res.FORMATION])
					if self.opt > len(res.PARTY[res.FORMATION]): self.opt = 0
					if self.opt == 0:
						if self.lopt < 0: self.lopt = len(self.products)
						if self.lopt > len(self.products): self.lopt = 0
					else:
						if self.lopt < 0: self.lopt = len(self.basket[self.opt - 1])
						if self.lopt > len(self.basket[self.opt - 1]): self.lopt = 0
				#BANK
				if self.mnu == 11 or self.mnu == 12:
					if self.pressed[4][0]:
						self.ch_sfx.play(res.SOUND['CASH_GET'])
						self.shp = False
						self.opt = 0
						self.lopt = 0

					if self.opt < 0: self.opt = 5
					if self.opt > 5: self.opt = 0
					if self.lopt < 0: self.lopt = 9
					if self.lopt > 9: self.lopt = 0

					if self.pressed[2][0]: self.lopt = self.extract[self.opt]
					if self.pressed[3][0]: self.lopt = self.extract[self.opt]
					
					self.extract[self.opt] = self.lopt

					if self.pressed[0][0]:
						if self.mnu == 11:
							res.ATM -= 1
							res.MONEY += 1
						if self.mnu == 12:
							res.ATM += 1
							res.MONEY -= 1

					if self.pressed[1][0]:
						if self.mnu == 11:
							res.ATM += 1
							res.MONEY -= 1
						if self.mnu == 12:
							res.ATM -= 1
							res.MONEY += 1
					'''if self.pressed[res.UP[0]]:
						if self.mnu == 11:
							res.ATM -= int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
							res.MONEY += int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
						if self.mnu == 12:
							res.ATM += int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))
							res.MONEY -= int(str(self.extract[0]) + str(self.extract[1]) + str(self.extract[2]) + str(self.extract[3]) + str(self.extract[4]) + str(self.extract[5]))'''
				if self.mnu == 3:
					if self.pressed[4][0]:
						if self.lopt == 0:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.mnu = 11
							self.lopt = 0
							self.opt = 5
						if self.lopt == 1:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.mnu = 12
							self.lopt = 0
							self.opt = 5
						if self.lopt == 2:
							self.ch_sfx.play(res.SOUND['MENU_BACK'])
							self.shp = False
							self.lopt = 0

					if self.lopt < 0: self.lopt = 2
					if self.lopt > 2: self.lopt = 0
			#INVENTORY OPTIONS
			if self.pressed[6][0] and self.phone == 0 and self.shp == False and self.inv.itmov == '':
				#OPEN AND CLOSE
				if self.inventory > 0:
					if self.inventory == 2: tlk = True
					else: tlk = False
					self.inventory = 0
					self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
					if tlk == True and self.dlgfa > 0: self.dialog(dtb.DIALOGS['DEPOSIT'][1])
					self.player[0]['PAUSE'] = 0
					if self.battle == True: self.mnu = 1
				elif self.inventory == 0:
					self.inventory = 1
					self.ch_sfx.play(res.SOUND['INVENTORY_OPEN'])
					self.player[0]['PAUSE'] = 1
					self.invfade = 0
					self.opt = 0
					self.lopt = 1
					self.mnu = 0
			if self.inventory > 0:
				#HOLDING ITEM
				if self.inv.itmov != '':
					#ACCESORIES SELECT
					if self.inv.itmov[0] == 0:
						if self.pressed[2][0]:
							if self.exvar > 1: self.exvar -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][0]:
							if self.exvar < 3: self.exvar += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					#MOVING ITEM
					else:
						if self.pressed[2][0]: self.opt -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[3][0]: self.opt += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
						if self.pressed[0][0]: self.lopt -= 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
						if self.pressed[1][0]: self.lopt += 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
				#SELECT ITEM
				else:
					if self.pressed[2][0]: self.opt -= 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[3][0]: self.opt += 1; self.ch_sfx.play(res.SOUND['MENU_HOR'])
					if self.pressed[0][0]: self.lopt -= 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
					if self.pressed[1][0]: self.lopt += 1; self.ch_sfx.play(res.SOUND['MENU_VER'])
					
				if self.inventory == 1:
					if self.opt < 0: self.opt = 4; self.mnu -= 1
					if self.opt > 4: self.opt = 0; self.mnu += 1
					if self.lopt < 0: self.lopt = 4
					if self.lopt > 4: self.lopt = 0
				if self.inventory == 2:
					if self.opt < 0: self.opt = 9
					if self.opt > 9: self.opt = 0
					if self.opt < 5:
						if self.lopt < 0: self.lopt = 4; self.mnu -= 1
						if self.lopt > 4: self.lopt = 0; self.mnu += 1
					else:
						if self.lopt < 0: self.lopt = math.ceil(len(res.STORAGE)/5) - 1
						if self.lopt > math.ceil(len(res.STORAGE)/5) - 1: self.lopt = 0
					if self.exvar < 0: self.exvar = 1
					if self.exvar > 1: self.exvar = 0

				if self.mnu < 0: self.mnu = len(res.PARTY[res.FORMATION]) - 1
				if self.mnu > len(res.PARTY[res.FORMATION]) - 1: self.mnu = 0
				
				ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.mnu]]
				it = res.INVENTORY[res.PARTY[res.FORMATION][self.mnu]][self.lopt][self.opt]
				if self.pressed[4][0] and self.opt < 4:
					#USING ITEMS
					if self.inv.itmov == '':
						#FOOD
						if it[0].startswith('food') and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] not in [4,10]:
							if ch['FLAW'] == 'celiac':
								if it[0] in ['food_bread']:
									good = False
								else: good = True
							elif ch['FLAW'] == 'lactose intolerant':
								if it[0] in ['food_brigadeiro','food_cake_corn','food_cake_carrot','food_cake_chocolate','food_cookie_chocolate','food_cookie_strawberry','food_pizza_mussarella','food_pizza_shaggy','food_pizza_chicken','food_pizza_4cheese']:
									good = False
								else: good = True
							else: good = True
							if good:
								self.ch_ton.play(res.SOUND['HEAL'])
								hl = dtb.ITEMS[it[0]][5]
								hg = dtb.ITEMS[it[0]][6]
								if it[2] != '_': hl += dtb.ITEMS[it[2]][5]
								if it[4] != '_': hl += dtb.ITEMS[it[4]][5]
								if it in res.CHARACTERS[self.mnu]['FAVFOOD']:
									hl += int(hl/2)
									hg += int(hg/2)
								ch['HP'] += hl
								ch['HUNGER'] += hg
								if res.DISITEMS[it[0]] == 0:
									res.DISITEMS[it[0]] = 1
								if ch['HP'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
									ch['HP'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
							else:
								self.ch_ton.play(res.SOUND['INCONSCIOUS'])
								ch['HEALTH'] = 10
							if dtb.ITEMS[it[0]][8] != None:
								it = ['trash_' + dtb.ITEMS[it[0]][8],'0000','_','0000','_','0000']
							else:
								it = ['_','0000','_','0000','_','0000']
							res.INVENTORY[res.PARTY[res.FORMATION][self.mnu]][self.lopt][self.opt] = it
							self.notification('hp_'+str(hl),(255, 0, 0))
						#DRINK
						elif it[0].startswith('drink'):
							if ch['FLAW'] == 'lactose intolerant':
								if it[0] in ['drink_milk','drink_coffeenmilk','drink_chocolate','drink_yogurt']:
									good = False
								else: good = True
							else: good = True
							if good:
								self.ch_ton.play(res.SOUND['HEAL'])
								hl = dtb.ITEMS[it[0]][5]
								if it in res.CHARACTERS[self.mnu]['FAVFOOD']: hl += int(hl/2)
								ch['HP'] += hl
								ch['THIRST'] += dtb.ITEMS[it[0]][6]
								if res.DISITEMS[it[0]] == 0:
									res.DISITEMS[it[0]] = 1
								if ch['HP'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
									ch['HP'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
							else:
								self.ch_ton.play(res.SOUND['INCONSCIOUS'])
								ch['HEALTH'] = 10
							if dtb.ITEMS[it[0]][8] != None:
								it = ['trash_' + dtb.ITEMS[it[0]][8],'0000','_','0000','_','0000']
							else:
								it = ['_','0000','_','0000','_','0000']
							res.INVENTORY[res.PARTY[res.FORMATION][self.mnu]][self.lopt][self.opt] = it
							self.notification('hp_'+str(hp),(255, 0, 0))
						#GRENADES
						elif it[0].startswith('grenade') and self.battle == True and it in res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][1:]:
							self.ch_sfx.play(res.SOUND['MELEE'])
							it = ['_','0000','_','0000','_','0000']
							self.mnu = 1
							self.inventory = 0
						#REPELLENTS
						elif it[0].startswith('repellent'):
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							ch['HEALTH'] = 2
							self.waitlst.append(['repellent' + str(res.PARTY[res.FORMATION][self.mnu]),self.waitime + dtb.ITEMS[it[0]][5]])
							it = ['_','0000','_','0000','_','0000']
						#STRENGHT PILL
						elif it[0] == 'pill_strenght':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][0] += 1
							it = ['_','0000','_','0000','_','0000']
						#RESISTANCE PILL
						elif it[0] == 'pill_resistance':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][1] += 1
							it = ['_','0000','_','0000','_','0000']
						#AGILITY PILL
						elif it[0] == 'pill_agility':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][2] += 1
							it = ['_','0000','_','0000','_','0000']
						#KNOWLEDGE PILL
						elif it[0] == 'pill_knowledge':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][3] += 1
							it = ['_','0000','_','0000','_','0000']
						#CHARISMA PILL
						elif it[0] == 'pill_charism':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][4] += 1
							it = ['_','0000','_','0000','_','0000']
						#MISTERY PILL
						elif it[0] == 'pill_mistery':
							self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
							ch['BONUS'][random.randint(0,4)] += 1
							it = ['_','0000','_','0000','_','0000']
						#PHONE CARDS
						elif it[0].startswith('phone'):
							self.ch_ton.play(res.SOUND['MENU_GO'])
							self.inv.itmov = [0,it[2],it[4]]
							self.exvar = 1
						#LOCKSMITH KEYS
						elif it[0].startswith('locksmith'):
							self.ch_ton.play(res.SOUND['MENU_GO'])
							self.inv.itmov = [0,it[2],it[4]]
							self.exvar = 1
						#WALLET ITEMS
						elif it[0] == 'wallet':
							self.ch_ton.play(res.SOUND['MENU_GO'])
							self.inv.itmov = [0,it[2],it[4]]
							self.inv.money = True
							self.exvar = 1
						#TENTS
						elif it[0].startswith('tent'):
							self.ch_sfx.play(res.SOUND['INVENTORY_CLOSE'])
							self.build = it[0]
							it = ['_','0000','_','0000','_','0000']
							self.player[0]['PAUSE'] = 0
						#NEWSPAPERS
						elif it[0].startswith('newspaper'):
							self.ch_sfx.play(res.SOUND['PAGE_FLIP'])
							self.player[0]['PAUSE'] = 0
							self.read = GUI.Newspaper()
						#ERROR
						else: self.ch_ton.play(res.SOUND['ERROR'])
						if self.battle == True:
							self.turn += 1
							self.mnu = 1
							self.inventory = 0
					#ACCESORIES EXIT
					elif self.inv.itmov[0] == 0:
						if self.exvar == 3:
							self.ch_sfx.play(res.SOUND['MENU_GO'])
							self.inv.itmov = ''
							self.inv.money = False
						else: self.ch_ton.play(res.SOUND['ERROR'])
					#CRAFTING
					elif it[0] != '_':
						craft = False
						if self.inv.itmov[0].startswith('key') and it.startswith('locksmith'): craft = True
						if self.inv.itmov[0].startswith('id_card') and it.startswith('wallet'): craft = True
						if self.inv.itmov[0].startswith('credit_card') and it.startswith('wallet'): craft = True
						elif self.inv.itmov[0].startswith('condiment') and it.startswith('food'): craft = True
						elif self.inv.itmov[0].startswith('acc') and it.startswith('gun'): craft = True
						#RECHARGE WEAPONS
						if self.inv.itmov[0].startswith('ammo') and it.startswith('gun'):
							if dtb.ITEMS[self.inv.itmov[0]][5] == dtb.ITEMS[it[0]][5]['GAUGE']:
								craft = True
								self.ch_ton.play(res.SOUND['GUN_RECHARGE'])
								it[3] = dtb.ITEMS[it[0]][5]['CAPACITY']
								if self.lopt == 4 and self.opt > 0:
									if int(it[3]) > 0:
										plus = int(98/(dtb.ITEMS[it[0]][5]['CAPACITY']/int(it[3])))
									else: plus = 0
									self.barpp[self.mnu][self.opt - 1] = plus
							else: craft = False
						else: craft = False
						#ADDING ACCESORIES
						if craft == True:
							if it[2] == '_':
								self.ch_ton.play(res.SOUND['CRAFT'])
								it[2] = self.inv.itmov[0]
								it[3] = self.inv.itmov[1]
								self.inv.itmov = ''
							elif it[4] == '_':
								self.ch_ton.play(res.SOUND['CRAFT'])
								it[4] = self.inv.itmov[0]
								it[5] = self.inv.itmov[1]
								self.inv.itmov = ''
							else: self.ch_ton.play(res.SOUND['ERROR']); self.shake = 5
						else: self.ch_ton.play(res.SOUND['ERROR']); self.shake = 5

						if self.battle == True:
							self.turn += 1
							self.mnu = 1
							self.inventory = 0

				if self.pressed[5][0]:
					if self.inv.itmov != '':
						#TAKE SUB-ITEM
						if self.inv.itmov[0] == 0:
							if self.exvar < 3 and self.inv.itmov[self.exvar] != '_':
								self.ch_sfx.play(res.SOUND['MENU_GO'])
								itm = self.inv.itmov[self.exvar]
								it[self.exvar + 1] = '_'
								if self.exvar == 1:
									prp = it[3]
								if self.exvar == 2:
									if it[2] == '_':
										prp = it[3]
									else:
										prp = it[5]
								self.inv.itmov = [itm,prp,'_','_']
							else: self.ch_sfx.play(res.SOUND['ERROR']); self.inv.shake = 5
						#PLACE ITEM IN INVENTORY
						elif self.opt < 5 and it == '_' and self.inv.space(res.PARTY[res.FORMATION][self.mnu],self.exvar,self.opt,self.lopt) == True:
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = dtb.ITEMS[self.inv.itmov[0]][5]
							if self.inv.itmov[0].startswith('head'):
								ch['ACCESORIES'] = self.inv.itmov[0]
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
							self.ch_sfx.play(res.SOUND['EQUIP'])
							nw = self.inv.itmov.copy()
							self.inv.itmov = ''
							it = nw
							if self.battle == True:
								self.turn += 1
								self.mnu = 1
								self.inventory = 0
						#PLACE ITEM IN STORAGE
						elif self.opt > 4 and res.STORAGE[self.opt + (self.lopt * 5) - 5][0] == '_':
							self.ch_sfx.play(res.SOUND['EQUIP'])
							res.STORAGE[self.opt + (self.lopt * 5) - 5] = self.inv.itmov.copy()
							chk = True
							for j in res.STORAGE:
								if j[0] == '_': chk = False
							if chk == True:
								for i in range(5): res.STORAGE.append(['_','0000','_','_'])
							self.inv.itmov = ''
							#AMMO BAR
							self.barpp = []
							x = 0
							for i in res.PARTY[res.FORMATION]:
								self.barpp.append([])
								for j in res.INVENTORY[i][4][1:]:
									if j[0] != '_':
										if int(j[1]) > 0: b = int(100/(dtb.ITEMS[j[0]][5]['CAPACITY']/int(j[1])))
										else: b = 0
										self.barpp[x].append(b)
									else:
										self.barpp[x].append(0)
								x += 1
						#SWITCH ITEMS IN INVENTORY
						elif self.opt < 5 and self.inv.space(self.mnu,self.exvar,self.opt,self.lopt) == True:
							self.ch_sfx.play(res.SOUND['EQUIP'])
							trd = it.copy()
							it = self.inv.itmov
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = dtb.ITEMS[self.inv.itmov[0]][5]
							self.inv.itmov = trd
						#SWITCH ITEMS IN STORAGE
						elif self.opt > 4:
							self.ch_sfx.play(res.SOUND['EQUIP'])
							trd = res.STORAGE[self.opt + (self.lopt * 5) - 5].copy()
							res.STORAGE[self.opt + (self.lopt * 5) - 5] = self.inv.itmov.copy()
							if self.inv.itmov[0].startswith('clth'):
								ch['COSTUME'] = dtb.ITEMS[self.inv.itmov[0]][5]
							self.inv.itmov = trd
						else: self.ch_sfx.play(res.SOUND['ERROR']); self.inv.shake = 5
					#TAKE ITEM FROM INVENTORY
					elif self.opt < 5 and it != '_':
						self.ch_sfx.play(res.SOUND['MENU_GO'])
						self.inv.itmov = it.copy()
						it = ['_','0000','_','0000','_','0000']
					#TAKE ITEM FROM STORAGE
					elif res.STORAGE[self.opt + (self.lopt * 5) - 5][0] != '_':
						self.ch_sfx.play(res.SOUND['MENU_GO'])
						self.inv.itmov = res.STORAGE[self.opt + (self.lopt * 5) - 5].copy()
						res.STORAGE[self.opt + (self.lopt * 5) - 5] = ['_','0000','_','0000','_','0000']
					'''elif self.inventory == 3:
						if it != '_' and self.confirmation() == 1:
							it = ['_','0000','_','_']'''
				#DEVICES SHORTCUT
				if self.pressed[7][0]:
					self.ch_sfx.play(res.SOUND['MENU_GO'])
					self.inv.st = [self.opt,self.lopt,self.mnu]
					#PHONE
					if it[0].startswith('phone'):
						self.dev = GUI.Apps(0)
					#CAMERA
					elif it[0] == 'camera':
						self.dev = GUI.Camera()
					#MP3
					elif it[0] == 'mp3':
						self.dev = self.rad
					#PDA
					elif it[0] == 'PDA':
						self.dev = GUI.Apps(1)
					#GPS
					elif it[0] == 'GPS':
						self.dev = GUI.GPS(False, self.map, self.tilrect, self.player[0], self.en, self.signs)
				res.INVENTORY[res.PARTY[res.FORMATION][self.mnu]][self.lopt][self.opt] = it
				if self.inv.itmov != '' and self.inv.itmov[0] == '_':
					self.inv.itmov = ''
			#DEVICE OPTIONS
			if self.pressed[7][0] and self.inv.find(res.PARTY[res.FORMATION][0],'phone') != None and self.inventory == 0 and self.shp == False and self.nmenu.show == False:
				#OPEN AND CLOSE
				if self.phone == 0 or self.phone > 1:
					if self.phone == 0:
						wh = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HAIR'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
						cl = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['COSTUME'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
						self.player[0]['HEAD'] = 'BLANKDD_' + wh
						self.player[0]['SPRITE'] = 'PHONE_' + cl
						self.opt = 0; self.lopt = 0; self.player[0]['PAUSE'] = 1
					if self.phone == 6: self.ch_ton.stop(); self.ch_ton.set_volume(res.SFX)

					if self.phone == 0 and self.battle == True:
						self.phone = 18
						self.mnu = 2
					elif self.nb != '':
						if self.phone == 0: self.phone = 17; self.opt = 0
						elif self.phone == 17: self.phone = 0
					else:
						if self.phone > 1: self.ch_sfx.play(res.SOUND['MENU_BACK'])
						self.phone = 1
						self.mnu = 0
				else:
					self.phone = 0
					if self.battle == False:
						self.dev.opt = [0,0]
						self.player[0]['PAUSE'] = 0
					else:
						self.mnu = 1
			#DEVICE EVENTS
			if self.phone > 0 and self.dev.battery > 0:
				self.dev.inside_events(self.pressed)
				#CALL DIALOG
				if self.dev.ingame < 3:
					wh = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HAIR'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
					cl = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['COSTUME'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
					self.player[0]['SPRITE'] = 'CALL_' + cl
					self.phone = 0
					if self.dev.ingame == 1:
						gt = 0
						for i in self.waitlst:
							if i[0] == 'delivery': gt = 1
						self.dialog(dtb.DIALOGS[self.dev.nb][1][gt])
					if self.dev.ingame == 2:
						self.dialog(dtb.DIALOGS[self.dev.nb][1][0])
					self.player[0]['PAUSE'] = 1
					self.player[0]['SPRITE'] = 'PHONE_' + cl
					self.phone = 3
				#CAN'T CALL
				elif self.dev.ingame == 3:
					self.dialog([dtb.MENU[17]])
				#GET CALL
				elif self.dev.ingame < 6:
					wh = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HAIR'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
					cl = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['COSTUME'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
					self.phone = 0
					self.sfx.play(res.SOUND['MENU_GO'])
					self.player[0]['DIRECTION'] = 0
					self.player[0]['SPEED'] = 0
					self.player[0]['SPRITE'] = 'CALL_' + cl
					if self.dlgfa > 0:
						self.dialog(dtb.DIALOGS[self.nb][0])
						res.CALLHIST.append([self.nb,True])
						self.player[0]['SPRITE'] = 'STANDD_' + cl
					self.nb = ''
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
					pass
					#self.notification(self.foe[0]['NAME'] + ' registrada',(134, 0, 211))
			#READING OPTIONS
			if self.read != None:
				self.read.inside_events(self.pressed)
				if self.pressed[7][0]:
					self.ch_sfx.play(res.SOUND['PAGE_FLIP'])
					self.read = None
			#PLAYER HOLD AND DRIVE
			if self.battle == False and self.inventory == 0 and self.phone == 0 and self.shp == False and self.sleepin == False:
				p = 0
				for i in self.player:
					if i['PAUSE'] == 0 and i['PLAYING'] == True and self.invfade < self.displayzw + 400:
						if self.driving == 0:
							if i['JUMP'] == 0 and res.MAP > 0:
								#PLACE OBJECTS
								if self.pressed[4][p]:
									if i['HOLD'] != None:
										i['HOLD'] = None
						#DRIVING DIRECTIONS
						elif self.driving > 0:
							if res.GAS > 0:
								if self.pressed[2][p]:
									i['DIRECTION'] -= 1
									if i['DIRECTION'] == 0: i['DIRECTION'] = 8
								elif self.pressed[3][p]:
									i['DIRECTION'] += 1
									if i['DIRECTION'] == 9: i['DIRECTION'] = 1
					p += 1
			#BUILD ITEMS
			if self.pressed[4][0] and self.build != '' and self.battle == False and self.phone == 0 and self.shp == False and self.sleepin == False:
				if self.inventory == 0:
					if self.build.startswith('tent'):
						self.tents.append({'N': len(self.tents),'RECT': pygame.Rect(math.floor((self.player[0]['RECT'].x + 15)/30) * 30,math.floor((self.player[0]['RECT'].y + 15)/30) * 30,30,30),'SPRITE': pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')})
						self.objects.append([9,len(self.tents) - 1,self.player[0]['RECT'].y])
						self.build = ''
				else:
					self.inventory = 0
		#KEYBOARD OR MOUSE INPUT
		if res.MOUSE < 2:
			ky = pygame.key.get_pressed()
			self.pressed = [ky[res.UP],ky[res.DOWN],ky[res.LEFT],ky[res.RIGHT],ky[res.ACT],ky[res.RUN],ky[res.BAG],ky[res.PHONE]]
		else:
			self.pressed = []
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1],2,2)
			for i in self.buttons:
				if self.colide(mr,i):
					if pygame.mouse.get_pressed()[0]: self.pressed.append([1,0])
					else: self.pressed.append([0,0])
				else: self.pressed.append([0,0])
		#PHONE HOLDING OPTIONS
		if self.phone > 0: self.dev.outside_events(self.pressed)
		#READING SCROLL
		if self.read != None: self.read.outside_events(self.pressed)
		#PLAYER MOVEMENT
		p = 0
		for i in self.player:
			if i['PAUSE'] == 0 and i['PLAYING'] == True and self.battle == False:
				if self.driving == 0:
					if i['JUMP'] == 0:
						#MOVING OPTIONS
						if res.MAP > 0:
							#RUN
							if self.pressed[5][p]:
								i['SPEED'] = 6 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/2)
								if i['SWIM'] != None: i['SPEED'] -= 3
								elif self.inv.space(p) == False: i['SPEED'] -= 2
							#WALK
							else:
								i['SPEED'] = 3 + math.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/4)
								if i['SWIM'] != None: i['SPEED'] -= 1
								elif self.inv.space(p) == False: i['SPEED'] -= 1
						else: i['SPEED'] = 1
						#MOVE UP
						if self.pressed[0][p]:
							if self.pressed[2][p]: i['DIRECTION'] = 6
							elif self.pressed[3][p]: i['DIRECTION'] = 8
							else: i['DIRECTION'] = 7
						#MOVE DOWN
						elif self.pressed[1][p]:
							if self.pressed[2][p]: i['DIRECTION'] = 4
							elif self.pressed[3][p]: i['DIRECTION'] = 2
							else: i['DIRECTION'] = 3
						#MOVE LEFT
						elif self.pressed[2][p]:
							if self.pressed[0][p]: i['DIRECTION'] = 6
							elif self.pressed[1][p]: i['DIRECTION'] = 4
							else: i['DIRECTION'] = 5
						#MOVE RIGHT
						elif self.pressed[3][p]:
							if self.pressed[0][p]: i['DIRECTION'] = 8
							if self.pressed[1][p]: i['DIRECTION'] = 2
							else: i['DIRECTION'] = 1
						else: i['SPEED'] = 0
				#DRIVING OPTIONS
				elif self.driving > 0:
					if self.pressed[0][p]:
						self.driving = 0
						'''self.displayzw = 600
						self.displayzh = 400
						self.display[0] = pygame.Surface((600, 400))
						self.cam.width = self.displayzw
						self.cam.height = self.displayzh'''
						i['DIRECTION'] = 3
					if res.GAS > 0:
						if self.pressed[1][0]:
							if i['SPEED'] > 0.0: i['SPEED'] -= self.vehicles[self.driving - 1]['ACCELERATION']

						elif self.pressed[5][p]:
							if i['SPEED'] < self.vehicles[self.driving - 1]['SPEED'] and res.GAS > 0.0:
								i['SPEED'] += self.vehicles[self.driving - 1]['ACCELERATION']
							res.GAS -= self.vehicles[self.driving - 1]['GAS']
						else: i['SPEED'] -= self.vehicles[self.driving - 1]['ACCELERATION']
			#FOLLOW
			if i['FOLLOW'] != None:
				if i['FOLLOW'] != (None,None):
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
			if self.colide(i, self.tilrect) == False:
				wh = res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HAIR'] + res.CHARACTERS[res.PARTY[res.FORMATION][p]]['SKIN']
				cl = res.CHARACTERS[res.PARTY[res.FORMATION][p]]['COSTUME'] + res.CHARACTERS[res.PARTY[res.FORMATION][p]]['SKIN']
				#POSITION UPDATE
				if i['SPEED'] > 0 and i['JUMP'] == 0 and i['PLAYING'] == True:
					if i['DIRECTION'] == 1: i['RECT'].x += i['SPEED']
					elif i['DIRECTION'] == 2: i['RECT'].x += i['SPEED']; i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 3: i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 4: i['RECT'].x -= i['SPEED']; i['RECT'].y += i['SPEED']
					elif i['DIRECTION'] == 5: i['RECT'].x -= i['SPEED']
					elif i['DIRECTION'] == 6: i['RECT'].x -= i['SPEED']; i['RECT'].y -= i['SPEED']
					elif i['DIRECTION'] == 7: i['RECT'].y -= i['SPEED']
					elif i['DIRECTION'] == 8: i['RECT'].x += i['SPEED']; i['RECT'].y -= i['SPEED']
				elif i['JUMP'] > 0 and i['PLAYING'] == True:
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
				if i['JUMP'] > 0: spr = 'JUMP'
				elif self.driving > 0: spr = 'DRIVE'
				elif i['SPEED'] > 3: spr = 'RUN'
				elif i['SPEED'] > 0: spr = 'WALK'
				else: spr = 'STAND'
				if i['SPEED'] > 0 or i['FOLLEND'] == 'head':
					hed = 'BLANK'
					if i['DIRECTION'] == 1: i['HEAD'] = hed + 'R_' + wh
					elif i['DIRECTION'] == 2: i['HEAD'] = hed + 'RD_' + wh
					elif i['DIRECTION'] == 3: i['HEAD'] = hed + 'D_' + wh
					elif i['DIRECTION'] == 4: i['HEAD'] = hed + 'LD_' + wh
					elif i['DIRECTION'] == 5: i['HEAD'] = hed + 'L_' + wh
					elif i['DIRECTION'] == 6: i['HEAD'] = hed + 'LU_' + wh
					elif i['DIRECTION'] == 7: i['HEAD'] = hed + 'U_' + wh
					elif i['DIRECTION'] == 8: i['HEAD'] = hed + 'RU_' + wh
				if self.phone == 0:
					if i['DIRECTION'] == 1: i['SPRITE'] = spr + 'R_' + cl
					elif i['DIRECTION'] == 2: i['SPRITE'] = spr + 'RD_' + cl
					elif i['DIRECTION'] == 3: i['SPRITE'] = spr + 'D_' + cl
					elif i['DIRECTION'] == 4: i['SPRITE'] = spr + 'LD_' + cl
					elif i['DIRECTION'] == 5: i['SPRITE'] = spr + 'L_' + cl
					elif i['DIRECTION'] == 6: i['SPRITE'] = spr + 'LU_' + cl
					elif i['DIRECTION'] == 7: i['SPRITE'] = spr + 'U_' + cl
					elif i['DIRECTION'] == 8: i['SPRITE'] = spr + 'RU_' + cl

			if res.GAS < 1.0: i['DIRECTION'] = 0
			if i['SPEED'] < 0: i['SPEED'] = 0
			p += 1
		#DIALOG SPEED
		if self.dlgfa == 0:
			self.dlgspd = res.SPEED
			if self.pressed[4][0]: self.dlgspd = 1

	def dialog(self, tx, wh=0):
		self.dlg = []
		self.dlgy = 0
		self.lopt = 0
		self.speakin = wh
		self.player[0]['PAUSE'] = 1
		self.player[0]['SPEED'] = 0
		txt = tx
		tid = 0
		did = 0
		spd = 10
		while tid < len(txt):
			#TEXT
			if isinstance(txt[tid], str):
				while self.dlgfa > 0:
					if self.winbar < 50 and self.battle == False: self.winbar += 5
					self.dlgfa -= 50
					self.run()
				else:
					self.dlg.append('')
					for i in txt[tid]:
						while True:
							if spd > 0: spd -= 10/self.dlgspd
							else:
								if self.ch_dlg.get_busy(): self.ch_sfx.play(res.SOUND['TEXT_INPUT'])
								else: self.ch_dlg.play(res.SOUND['TEXT_INPUT'])
								self.dlg[did] += i
								if res.DISLEXIC == True:
									self.dlg[did] += ' '
								spd = 10
								break
							self.run()
					did += 1
			#DIALOG PROTOCOLS
			else:
				#SIDE MESSAGE
				if txt[tid] == 0:
					self.dlg.append(0)
					did += 1
				#WAIT FOR PRESS
				elif txt[tid] == 1:
					self.dlg.append(1)
					self.wait()
					self.ch_ton.play(res.SOUND['MENU_GO'])
					did += 1
				#CHAPTER INTRO
				elif txt[tid] == 2:
					res.SCENE = -1
					self.ch_msc.pause()
					self.ch_ton.play(res.SOUND['BAUM'])
					self.player[0]['PAUSE'] = 3
					for i in range(100): self.run()
					res.SCENE = 0
					self.player[0]['PAUSE'] = 1
					self.ch_msc.unpause()
				#CHAPTER END
				elif txt[tid] in [3,4]:
					self.scrmov = 0
					pygame.mixer.stop()
					self.player[0]['PAUSE'] = 3
					self.ch_ton.play(res.SOUND['CHAPTER_END'])
					for i in range(120): self.run()
					if txt[tid] == 3: res.CHAPTER += 1
					self.classrun = 2
				#MONEY GET
				elif txt[tid][0] == 0 and self.notx == 0:
					src = None
					for i in res.PARTY[res.FORMATION]:
						src = self.inv.find(i,'credit_card')
						if src == None:
							src = self.inv.find(i,'wallet')
							if src != None: break
						else: break
					if src != None:
						if len(src[1]) <= 6: src[1] = str(int(src[1]) + txt[tid][1])
						else: src[1] = str(int(src[1][0:6]) + txt[tid][1]) + src[1][6:]
						self.ch_sfx.play(res.SOUND['CASH_GET'])
						self.notification('Adquiriu $' + str(txt[tid][1]),(255, 255, 255))
				#ITEM GET
				elif txt[tid][0] == 1 and self.notx == 0:
					gt = True
					if txt[tid][2] != 0:
						src = self.inv.find('credit_card')
						if src == None: gt = False
						if int(src[1]) < txt[tid][2]: gt = False
					if len(txt[tid]) > 3:
						if res.DLGSAV[txt[tid][3]] == 0:
							res.DLGSAV[txt[tid][3]] = 1
						else: gt = False
					if len(txt[tid]) > 4: prp = txt[tid][4]
					else: prp = '0000'
					if gt == True:
						if txt[tid][2] != 0:
							if len(src[1]) <= 6: src[1] = str(int(src[1]) - txt[tid][2])
							else: src[1] = str(int(src[1][0:6]) - txt[tid][2]) + src[2][6:]
						self.inv.add(res.PARTY[res.FORMATION][0],txt[tid][1],prp)
						self.ch_sfx.play(res.SOUND['ITEM_GET'])
						self.notification('it_' + txt[tid][1],(255, 255, 255))
				#MORALITY
				elif txt[tid][0] == 2 and self.notx == 0:
					res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += txt[tid][1]
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					self.notification('ml_'+str(txt[tid][1]),(0, 0, 0))
				#INSERT TEXT
				elif txt[tid][0] == 3:
					if isinstance(txt[tid][1],int):
						adtxt = res.CHARACTERS[txt[tid][1]]['NAME']
					elif txt[tid][1] == 'self':
						adtxt = res.CHARACTERS[res.PARTY[res.FORMATION][0]]['NAME']
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
					else:
						adtxt = dtb.DTALKS[txt[tid][1]]
					if len(txt[tid]) > 2:
						adtxt += txt[tid][2]
					txt.insert(tid + 1, adtxt)
				#CALLING
				elif txt[tid][0] == 4:
					if txt[tid][1] != 'stop':
						self.ch_ton.play(res.SOUND['CALLING'],-1)
						self.ch_rng.play(res.SOUND['RINGTONE_' + str(res.PARTY[res.FORMATION][0])])
						if self.rad.onoff == True: pygame.mixer.music.pause()
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
						if cl == True:
							self.phone = 3
							self.mnu = 1
							txt.insert(tid + 1, [2,'stop'])
							txt.insert(tid + 1, 0)
							for i in self.dev.call(str(dtb.CONTACTS[txt[tid][1]][1]),0,False,False)[-1:0:-1]:
								txt.insert(tid + 1, i)
					else:
						self.phone = 0
						self.mnu = 0
				#NEW EMAIL
				elif txt[tid][0] == 5 and self.notx == 0:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					mail = dtb.EMAILS[txt[tid][1]].copy()
					mail.append(0)
					res.INBOX.append(mail)
					res.inbx_save(len(res.INBOX)-1,0)
					self.notification(dtb.NOTINFO['EMAIL'],(255, 221, 0))
				#NEW TASK
				elif txt[tid][0] == 6 and self.notx == 0:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					if txt[tid][2] == False:
						res.TASKS.append([dtb.TASKINDEX[txt[tid][1]], 0])
						if len(txt[tid]) > 3:
							res.MARKER.append(txt[tid][3])
						res.task_save(txt[tid][1],0)
						self.notification(dtb.TASKINDEX[txt[tid][1]][0],(255, 123, 0))
					elif self.inv.find(res.PARTY[res.FORMATION][0],txt[tid][1]):
						self.ch_ton.play(res.SOUND['ITEM_GET'])
						for j in txt[tid][3][::-1]:
							txt.insert(tid + 1, j)
					else:
						for j in txt[tid][2][::-1]:
							txt.insert(tid + 1, j)
				#NEW CONTACT
				elif txt[tid][0] == 7 and self.notx == 0:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					dtb.CONTACTS.append(dtb.NUMBERS[txt[tid][1]].copy())
					dtb.call_save(len(dtb.CONTACTS)-1)
					self.notification(dtb.NOTINFO['CONTACT'],(165, 255, 0))
				#ACHIEVEMENT
				elif txt[tid][0] == 8 and self.notx == 0:
					self.ch_sfx.play(res.SOUND['ACHIEVEMENT'])
					dtb.ACHIEVEMENTS[txt[tid][1]][2] = True
					self.notification(dtb.ACHIEVEMENTS[txt[tid][1]][0],(255, 191, 0))
				#RANKING
				elif txt[tid][0] == 9 and self.notx == 0:
					self.ch_sfx.play(res.SOUND['NOTIFICATION'])
					self.notification('Subiu de posição!',(56, 255, 0))
				#DIALOG CHOICES
				elif txt[tid][0] == 10:
					while self.dlgfa > 0:
						if self.winbar < 50 and self.battle == False: self.winbar += 5
						self.dlgfa -= 50
						self.run()
					else:
						self.speakin = 0
						self.dlg.append(0)
						for j in txt[tid][-1:0:-1]:
							if res.DISLEXIC == True:
								out = ''
								for t in j[0]:
									out += t + ' '
							else: out = j[0]
							self.dlg.append(out)
						self.dlg.append(0)
						self.diopt(len(txt[tid][1:]))
						self.speakin = wh
						for j in txt[tid][self.lopt][-1:0:-1]:
							txt.insert(tid + 1, j)
						self.lopt = 0
						did = len(self.dlg)
				#SKIP DIALOGS
				elif txt[tid][0] == 11:
					tid += txt[tid][1]
				#RETURN DIALOGS
				elif txt[tid][0] == 12:
					tid -= txt[tid][1]
				#BATTLE
				elif txt[tid][0] == 13:
					self.dlg = []
					pygame.mixer.music.stop()
					for i in txt[tid][1:]:
						fo = dtb.FREAKS[i].copy()
						fo['FILE'] = i
						fo['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (fo['FILE']) + '_stand.png')
						fo['DIRECTION'] = False
						fo['FIGHTING'] = False
						fo['HEALTH'] = 0
						if fo['TYPE'] == 'mercenary': self.mrc.append(fo)
						else: self.foe.append(fo)
					txt = []
					tid = 0
					self.mnu = 0
					self.turn = -5
					self.fight()
				#ARMY BATTLE
				elif txt[tid][0] == 14:
					self.dlg = []
					pygame.mixer.music.stop()
					for k in range(txt[tid][1]):
						for f in txt[tid][2]:
							i = dtb.FREAKS[f].copy()
							i['FILE'] = f
							i['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (i['FILE']) + '_stand.png')
							i['DIRECTION'] = False
							i['FIGHTING'] = False
							i['HEALTH'] = 0
							if i['TYPE'] == 'mercenary': self.mrc.append(i)
							else: self.foe.append(i)
					txt = []
					tid = 0
					self.mnu = 0
					self.turn = -4
					self.fight()
				#PLAY MUSIC
				elif txt[tid][0] == 15:
					if txt[tid][2] == 0:
						if len(txt[tid]) > 2: lp = txt[tid][2]
						else: lp = 0
						self.ch_sfx.play(res.SOUND[txt[tid][1]],lp)
					if txt[tid][2] == 1:
						pygame.mixer.music.load('Music/' + txt[tid][1] + '.mp3')
						pygame.mixer.music.play(-1)
				#CHECK CHARACTER
				elif txt[tid][0] == 16:
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
									ii = cc['HAIR'] + cc['COSTUME'] + cc['SKIN']
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
				#DECREASE STATUS
				elif txt[tid][0] == 19:
					for i in self.foe + self.mrc:
						prb = round(random.randint(0,20))
						if prb > 10:
							self.ch_sfx.play(res.SOUND['ATTRIBUTE_LOSS'])
							if i['TYPE'] == 'spirit': tst = self.fig[self.turn]['SPIRITS']
							else: tst = self.fig[self.turn]['INTIMIDATION']
							if txt[tid][1] == 0:
								i['STRENGHT'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.BATTLE[24].lower(), (200, 20, 20))
							if txt[tid][1] == 1:
								i['AGILITY'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.BATTLE[23].lower(), (20, 200, 20))
							if txt[tid][1] == 2:
								i['RESISTANCE'] -= txt[tid][2] + tst
								self.hitisplay(0, self.aim, '-' + str(txt[tid][2]) + ' ' + dtb.BATTLE[25].lower(), (20, 20, 200))
				#INCREASE STATUS
				elif txt[tid][0] == 20:
					prb = round(random.randint(0,20))
					if prb > 10:
						self.ch_sfx.play(res.SOUND['ATTRIBUTE_GAIN'])
						if txt[tid][1] == 0:
							self.pstr[self.turn] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.BATTLE[24].lower(), (200, 20, 20))
						if txt[tid][1] == 1:
							self.pagi[self.turn] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.BATTLE[23].lower(), (20, 200, 20))
						if txt[tid][1] == 2:
							self.pres[self.turn] += txt[tid][2] + self.fig[self.turn]['INSPIRATION']
							self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.BATTLE[25].lower(), (20, 20, 200))
				#NEXT SCENE
				elif txt[tid][0] == 21:
					if isinstance(txt[tid][1],str): res.DLGSAV[txt[tid][1]] = txt[tid][2]
					else: res.SCENE = txt[tid][1]
				#NAME INPUT
				elif txt[tid][0] == 22:
					snd = self.ch_msc.get_sound()
					self.ch_msc.stop()
					self.nmenu = GUI.Naming()
					self.nmenu.ninput = txt[tid][1]
					self.nmenu.show = True
					self.FPS = 0
					while self.nmenu.show == True:
						self.nmenu.events()
						self.nmenu.run()
						self.run()
					self.FPS = 60
					dtb.load_dialogs()
					if snd != None: self.ch_msc.play(snd,-1)
				#GET OTHER DIALOG
				elif txt[tid][0] == 23:
					dlg = txt[tid][1]
					idx = None
					if len(txt[tid]) > 2: idx = txt[tid][2]
					if self.battle == True:
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
					did = len(self.dlg)
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
						self.player[0]['HEAD'] = txt[tid][2] + '_' + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HAIR'] + res.CHARACTERS[res.PARTY[res.FORMATION][0]]['SKIN']
					else:
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								i['HEAD'] = txt[tid][2] + '_' + i['INDEX'][0:3] + i['INDEX'][5]
				#CAMERA
				elif txt[tid][0] == 26:
					if isinstance(txt[tid][1],int):
						for i in self.npcs:
							if i['N'] == txt[tid][1]:
								self.speakin = i['RECT']
					else: self.speakin = pygame.Rect(txt[tid][1][0],txt[tid][1][1],1,1)
				#WAIT
				elif txt[tid][0] == 27:
					ds = self.dlg.copy()
					self.dlg = []
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = 'TWNN'
					for i in range(txt[tid][1]): self.run()
					if len(txt[tid]) > 2 and txt[tid][2] == 'TWNN': self.cityname = ''
					self.dlg = ds
				#TUTORIAL
				elif txt[tid][0] == 28:
					if res.HINT == True:
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
					ds = self.dlg.copy()
					self.dlg = []
					self.transiction(True, 210, 10)
					self.rendermap(txt[tid][1])
					self.player[0]['RECT'].x = txt[tid][2]
					self.player[0]['RECT'].y = txt[tid][3]
					self.transiction(False, 50, 10)
					self.dlg = ds
				#PUT CHARACTER
				elif txt[tid][0] == 30:
					ind = 0
					for n in self.npcs:
						if n['N'] > ind: ind = n['N']
					ind += 1
					self.npcs.append({'N': ind, 'RECT': pygame.Rect(txt[tid][1][0], txt[tid][1][1], 0, 0), 'TYPE': txt[tid][4], 'INDEX': txt[tid][2], 'WHO': txt[tid][3],
					'GIF': 0.0,'BLINK': 100,'HEAD': 'BLANKD_' + txt[tid][2][0:3] + txt[tid][2][5],'SPRITE': 'STANDD_' + txt[tid][2][3:6],'MOVE': 'fixed','DIRECTION': 3,'SPEED': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None,'PAUSE': 0})
					self.objects.append([2,ind,txt[tid][1][1]])
				#CENSORSHIP
				elif txt[tid][0] == 31:
					if res.CENSORSHIP == False: txt.insert(tid + 1, txt[tid][2])
					elif res.CENSORSHIP == True: txt.insert(tid + 1, txt[tid][1])
				#PROBABILITY
				elif txt[tid][0] == 32:
					prb = random.randint(0,100)
					for i in txt[tid][1:]:
						if prb > i[0] - 100:
							txt.insert(tid + 1, i[1:])
			tid += 1
		#FINISH DIALOG
		self.dlg = []
		self.speakin = 0
		self.player[0]['PAUSE'] = 0
		while self.dlgfa < 500:
			self.dlgfa += 50
			if self.winbar > 0 and self.battle == False:
				self.winbar -= 5
				self.run()

	def diopt(self, ln):
		self.lopt = 1
		trigger = True
		while trigger:
			self.run()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					trigger = False
					pygame.quit()
					sys.exit()
				if self.pressed[0][0]:
					if self.lopt < ln: self.ch_sfx.play(res.SOUND['MENU_HOR']); self.lopt += 1
				if self.pressed[1][0]:
					if self.lopt > 1: self.ch_sfx.play(res.SOUND['MENU_VER']); self.lopt -= 1
				if self.pressed[4][0]:
					self.ch_ton.play(res.SOUND['MENU_GO'])
					i = 1
					crg = -1
					while i <= ln + 1:
						if i != self.lopt: del self.dlg[crg - i]; crg += 1; ln -= 1
						i += 1
					trigger = False
					break

	def wait(self):
		waiting = True
		while waiting == True:
			self.events()
			self.draw()
			self.glock.tick(self.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					waiting = False
				if event.type == pygame.MOUSEBUTTONUP and res.MOUSE > 0:
					waiting = False

	def confirmation(self):
		yesno = 0
		opt = 1
		brd = pygame.Surface((200,100))
		brd.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
		for x in range(20):
			for y in range(10):
				brd.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		pygame.draw.rect(brd, (0,0,0), pygame.Rect(10,10,180,80))
		txt = pygame.Surface((360,160))
		while yesno == 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if self.pressed[2][0]: self.ch_sfx.play(res.SOUND['MENU_HOR']); opt = 1
				if self.pressed[3][0]: self.ch_sfx.play(res.SOUND['MENU_VER']); opt = 2
				if self.pressed[4][0]:
					yesno = opt
					if yesno == 1: self.ch_sfx.play(res.SOUND['MENU_GO'])
					if yesno == 2: self.ch_sfx.play(res.SOUND['MENU_BACK'])
					opt = 0
			txt.fill((0,0,0))
			txt.blit(self.fnt['DEFAULT'].render(dtb.MENU[85], True, (255, 255, 255)), (90, 20))
			if opt == 1: txt.blit(self.fnt['DEFAULT'].render(dtb.MENU[83], True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (80, 100))
			else: txt.blit(self.fnt['DEFAULT'].render(dtb.MENU[83], True, (255, 255, 255)), (80, 100))
			if opt == 2: txt.blit(self.fnt['DEFAULT'].render(dtb.MENU[84], True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (220, 100))
			else: txt.blit(self.fnt['DEFAULT'].render(dtb.MENU[84], True, (255, 255, 255)), (220, 100))

			self.display[0].blit(brd,(195,145))
			self.display[1].blit(txt,(410,310))
			self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			pygame.display.update(400,300,380,180)
			self.glock.tick(self.FPS)

		return yesno

	def transiction(self, fade, limit, spd=5):
		if fade == False:
			while self.winbar > limit:
				self.winbar -= spd
				self.run()
			if self.winbar > limit: self.winbar = limit
		else:
			while self.winbar < limit:
				self.winbar += spd
				self.run()
			if self.winbar < limit: self.winbar = limit

	def fight(self):
		#BATTLE START
		if self.turn < 0:
			#PLAY SOUND
			self.inventory = 0
			self.phone = 0
			self.shp = False
			self.player[0]['PAUSE'] = 2
			self.player[0]['SPEED'] = 0
			if self.rad.onoff == True: pygame.mixer.music.pause()
			if self.turn == -1: self.ch_ton.play(res.SOUND['BATTLE_FOE'])
			elif self.turn == -2: self.ch_ton.play(res.SOUND['BATTLE_ENEMY'])
			elif self.turn == -3: self.ch_ton.play(res.SOUND['BATTLE_AMBUSH'])
			elif self.turn == -6: self.ch_ton.play(res.SOUND['BATTLE_FOE'])
			else: self.ch_ton.play(res.SOUND['BATTLE_BOSS'])
			if self.driving > 0: self.obstacles = True
			#ZOOM TRANSITION
			dw = int(self.windoww/100)
			dh = int(self.windowh/100)
			if self.turn != -6:
				acc = 0
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
					self.draw()
					acc += 1
				self.battle = True
			#MYSTERIOUS FREAK
			else:
				freakname = self.foe[0]['NAME'].lower()
				showname = ''
				self.speakin = self.foe[0]['RECT']
				for i in range(30): self.run()
				self.transiction(True,210)
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
				for i in range(60): self.run()
				self.cityname = ''
				self.speakin = 0
				self.battle = True
			self.fig = []
			tr = 0
			for i in res.PARTY[res.FORMATION]:
				dt = res.CHARACTERS[i]
				if dt['HP'] > 0:
					dt['N'] = tr
					self.fig.append(dt)
				tr += 1
			#BACKGROUND
			self.bbg = pygame.image.load(res.BACKG_PATH + 'bt_' + self.room[1:-2] + '.png')
			self.bbm = 0
			self.bba = 0
			self.bbd = False
			#SET UP PARTY
			self.player[0]['SPEED'] = 0
			self.pstr = []
			self.patt = []
			self.pagi = []
			self.pres = []
			self.pklg = []
			self.pchm = []
			self.tatt = []
			self.tagi = []
			self.tstr = []
			self.tres = []
			self.opt = 0
			p = 0
			for i in res.PARTY[res.FORMATION]:
				self.pstr.append(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['STRENGHT'][res.CHARACTERS[i]['LEVEL']])
				self.patt.append(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['STRENGHT'][res.CHARACTERS[i]['LEVEL']])
				self.pagi.append(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['AGILITY'][res.CHARACTERS[i]['LEVEL']])
				self.pres.append(dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']])
				self.tatt.append(0)
				self.tagi.append(0)
				p += 1
			#SET UP FREAKS
			enx = 0
			while enx < len(self.foe):
				sz = self.foe[enx]['SPRITE'].get_rect()
				self.foe[enx]['MASK'] = pygame.Rect(230,int(self.displayzh/2) - int(sz.height/2),sz.width,sz.height)
				self.foe[enx]['MASK'].x += enx * 80
				dprb = [1,5]
				self.foe[enx]['DIRECTION'] = dprb[round(random.randint(0,1))]
				self.foe[enx]['RESISTANCE'] = self.foe[enx]['HP']
				self.foe[enx]['FADE'] = 10
				self.foe[enx]['AWAY'] = 0
				enx += 1
			#SET UP MERCENARIES
			enx = 0
			while enx < len(self.mrc):
				sz = self.mrc[enx]['SPRITE'].get_rect()
				self.mrc[enx]['MASK'] = pygame.Rect(230,int(self.displayzh/2) - int(sz.height/2),sz.width,sz.height)
				self.mrc[enx]['MASK'].x += enx * 80
				self.mrc[enx]['DIRECTION'] = 5
				self.mrc[enx]['RESISTANCE'] = self.mrc[enx]['HP']
				self.mrc[enx]['FADE'] = 10
				self.mrc[enx]['AWAY'] = 0
				enx += 1
			#CONDITIONS
			if len(self.foe) > 0:
				if self.turn == -3: self.foe[0]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[0]['FILE']) + '_backwards.png'); self.foe[0]['HEALTH'] = 1
			else:
				if self.turn == -3: self.mrc[0]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[0]['FILE']) + '_backwards.png'); self.mrc[0]['HEALTH'] = 1
			#ZOOM TRANSITION
			if self.turn != -6:
				acc = 0
				while True:
					self.displayzw += acc * dw
					self.displayzh += acc * dh
					self.cam.x -= int(acc * (dw/2))
					self.cam.y -= int(acc * (dh/2))
					self.cam.width = self.displayzw
					self.cam.height = self.displayzh
					if self.displayzw < int(self.windoww/2): self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
					else:
						self.displayzw = int(self.windoww/2)
						self.displayzh = int(self.windowh/2)
						self.cam.x = 0
						self.cam.y = 0
						self.cam.width = int(self.windoww/2)
						self.cam.height = int(self.windowh/2)
						self.display[0] = pygame.Surface((self.displayzw, self.displayzh))
						break
					self.draw()
					acc += 1
			#PLAY SONG
			if len(self.foe) > 0: self.ch_msc.play(res.SONGS[self.foe[0]['SONG']],-1)
			elif len(self.mrc) > 0: self.ch_msc.play(res.SONGS[self.mrc[0]['SONG']],-1)
			self.player[0]['GIF'] = 0.0
			self.tilemation = 0.0
			#TRANSICTION
			if self.turn != -6: self.transiction(True, 100)
			else: self.turn = 0; self.transiction(False, 100)
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
			d = []
			for i in range(len(self.player)):
				if self.player[i]['PLAYING'] == True:
					d.append(dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][i]]['CLASS']]['AGILITY'][res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL']] + res.CHARACTERS[res.PARTY[res.FORMATION][i]]['BONUS'][2])
			if len(d) > 1:
				for i in range(30):
					self.dices = []
					for di in d:
						self.dices.append(random.randint(0,di))
					self.run()
				ord = []
				for i in self.dices:
					p = 0
					for o in ord:
						pass
				for i in range(30):
					self.run()
				self.dices = []
			self.mnu = 1
		#PLAYERS TURN
		elif self.turn < len(res.PARTY[res.FORMATION]):
			print(self.pstr)
			print(self.patt)
			print(self.pagi)
			print(self.pres)
			again = False
			self.mnu = 3
			#EQUIPMEMT
			if self.equip[self.turn] < 4:
				#SET AMMO
				pp = int(res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1])
				pp -= 1
				res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1] = str(pp)
				gottem = False
				#GRENADES
				if res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('grenade'):
					cld = pygame.Rect(self.aim.x - 30,self.aim.y - 30,self.aim.width + 30,self.aim.height + 30)
					self.attackimation(9)
					res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1] = ['_','0000','_','0000','_','0000']
				#GUNS N MELEE
				else:
					cld = self.aim
				for i in self.foe + self.mrc:
					if self.colide(cld, i['MASK']) and i['FIGHTING'] == True:
						gottem = True
						wpdmg = dtb.ITEMS[res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0]][5]['DAMAGE']
						dmg = int(random.randint(wpdmg - 2,wpdmg + 2)) - i['RESISTANCE'] + dtb.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]
						if res.CHARACTERS[res.PARTY[res.FORMATION][self.turn]]['HEALTH'] == 11: dmg = int(dmg/2)
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
						if dmg >= wpdmg + 2 - i['RESISTANCE'] + dtb.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]:
							if i['HP'] <= 0:
								self.ch_ton.play(res.SOUND['SCREAM_' + i['FILE'].upper()])
								i['AWAY'] = 1
								
							self.ch_sfx.play(res.SOUND['CRITICAL'])
							self.hitisplay(10, i['MASK'], dtb.BATTLE[3], (200, 0, 0))
						else:
							if res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('melee'):
								self.ch_sfx.play(res.SOUND['HIT'])
							elif res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('gun'):
								self.ch_sfx.play(res.SOUND['GUNSHOT_1'])
							if res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0].startswith('grenade'):
								self.ch_sfx.play(res.SOUND['HIT'])
							self.hitisplay(10, i['MASK'], str(dmg), (200, 0, 0))
						if i['HEALTH'] != 1 and i['HP'] > 0: i['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (i['FILE']) + '_stand.png')
						#CHECK WIN
						if i['HP'] <= 0:
							if dmg >= i['RESISTANCE']: again = True
							if i['AWAY'] == 0:
								self.ch_ton.play(res.SOUND['SCREAM_' + i['FILE'].upper()])
								while i['FADE'] > 0:
									i['FADE'] -= 1
									self.run()
							if i['ITEM'] != None:
								prb = round(random.randint(0,100))
								if prb > i['ITEM'][1]:
									self.inv.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
									self.ch_sfx.play(res.SOUND['ITEM_GET'])
									self.notification('Adquiriu ' + dtb.ITEMS[i['ITEM'][0]][0],(255, 255, 255))
							i['FIGHTING'] = False
				#MISS
				if gottem == False:
					self.ch_sfx.play(res.SOUND['MISS'])
					self.hitisplay(5, self.aim, dtb.BATTLE[4], (200, 200, 200))
				self.mnu = 0
			#BATTLE DIALOG
			elif self.equip[self.turn] == 5:
				self.dialog(dtb.DIALOGS['BATTLEDIALOG'])
				self.mnu = 1
			#RUN AWAY
			elif self.equip[self.turn] == 7:
				self.dialog([self.fig[self.turn]['NAME'] + dtb.BATTLE[15]])
				run = round(random.randint(0,30)) + self.fig[self.turn]['ATLETISM']
				if run > 20:
					self.ch_msc.fadeout(500)
					self.dialog([dtb.BATTLE[17]])
					self.transiction(True, int(self.displayzh/2))
					for i in self.en:
						i['FIGHTING'] = False
					self.turn = 0
					self.mnu = 0
					self.hits = 0
					self.tdmg = 0
					self.hpl = 0
					self.tbt = 0
					self.foe = []
					self.mrc = []
					self.battle = False
					self.opt = 1
					self.player[0]['RECT'].x += 150
					if self.rad.onoff == True: pygame.mixer.music.unpause()
					self.transiction(False, 0)
				else:
					self.dialog([dtb.BATTLE[16]])
			#EXTRA ATTACK
			dth = 0
			for d in self.foe + self.mrc:
				if d['HP'] <= 0: dth += 1
			if dth < len(self.foe) + len(self.mrc) and self.battle == True and again == True:
				self.ch_ton.play(res.SOUND['ONE_MORE'])
				self.hitisplay(0, self.aim, dtb.BATTLE[5], (10, 50, 255))
				self.turn -= 1
			if self.turn < len(self.fig):
				self.aim.x = 100 + dtb.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]
		#ENEMIES TURN
		else:
			self.inventory = 0
			self.phone = 0
			self.tbt += round(self.btime/10)
			self.btime = 100
			self.mnu = 3
			count = 0
			for i in self.foe + self.mrc:
				if i['HP'] > 0 and i['FIGHTING'] == True and i['HEALTH'] != 1 and len(self.fig) > 0:
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
					if i['TYPE'] != 'mercenary':
						otk = 0
						for d in self.mrc:
							if d['HP'] > 0: otk += 1
						if i['HEALTH'] == 9: pl = int(random.randint(-20,len(self.fig) - 1 + otk))
						else: pl = int(random.randint(-1,len(self.fig) - 1 + otk))
					else:
						otk = 0
						for d in self.foe:
							if d['HP'] > 0: otk += 1
						if i['HEALTH'] == 9: pl = int(random.randint(-20,len(self.fig) - 1 + otk))
						else: pl = int(random.randint(-1,len(self.fig) - 1 + otk))
					#DECREASE STATUS LIMIT
					if act[3] == 2 and self.tatt == 2: act = i['HABILITIES'][0]
					if act[3] == 3 and self.tagi == 2: act = i['HABILITIES'][0]
					#ATTACK
					if pl >= 0:
						if pl >= len(self.fig): act = ['','',-10,1]
						if act[3] == 1:
							#SIMPLE ATTACK
							if act[2] < 0:
								#ATTACK PARTY
								if pl < len(self.fig):
									for a in res.INVENTORY[pl][:-1]:
										if a[0][0] != '_':
											act[2] += int(dtb.ITEMS[a[0][0]][5])
											a[0][1] = int(a[0][1])
											a[0][1] -=1
											if a[0][1] == 0:
												self.dialog([a[0][0] + dtb.BATTLE[36],1])
												a[0] = ['_','0000','_','0000','_','0000']
											a[0][1] = str(a[0][1])
									#FEAR
									if self.fig[pl]['FEAR'] == i['TYPE']: act[2] -= math.floor(act[2]/5)
									act[2] -= i['STRENGHT'] + dtb.CLASSES[self.fig[pl]['CLASS']]['RESISTANCE'][self.fig[pl]['LEVEL']]
									self.turn = self.fig[pl]['N']
									self.ch_ton.play(res.SOUND['SCREAM_' + i['FILE'].upper()])
									self.ch_sfx.play(res.SOUND['DAMAGE_1'])
									#DODGE
									if self.attackimation(act[5]) == True:
										act[2] -= math.floor(act[2]/5)
										self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
									#HIT
									if -act[2] > 0:
										self.fig[pl]['HP'] += act[2] + self.pres[pl]
										self.hitisplay(-act[2] * 2, None, '', (0,0,0))
									#NO DAMAGE
									else:
										self.fig[pl]['HP'] += -1
										self.hitisplay(2, None, '', (0,0,0))
									self.hpl += act[2]
								else:
									#ATTACK MERCENARY
									if i['TYPE'] != 'mercenary':
										print(i['NAME'] + ' atacou ' + self.mrc[pl - len(self.fig)]['NAME'])
										self.ch_sfx.play(res.SOUND['HIT'])
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (self.mrc[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.mrc[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (self.mrc[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.mrc[pl - len(self.fig)]['HP'] += act[2]
									#ATTACK FREAK
									else:
										print(i['NAME'] + ' atacou ' + self.foe[pl - len(self.fig)]['NAME'])
										self.ch_sfx.play(res.SOUND['HIT'])
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (self.foe[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.foe[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (self.foe[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.foe[pl - len(self.fig)]['HP'] += act[2]
							#SELF HEALING
							elif act[2] > 0:
								self.ch_ton.play(res.SOUND['HEAL'])
								i['HP'] += act[2]
						elif act[3] == 2:
							#REDUCE DAMAGE
							if act[2] < 0:
								if self.tatt[pl] < 2:
									self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
									self.patt[pl] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[20] + str(act[2]) + dtb.BATTLE[22],1])
									self.tatt[pl] += 1
							#GROW DAMAGE
							elif act[2] > 0:
								act[2] += act[2]
								self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + dtb.BATTLE[21] + str(act[2]) + dtb.BATTLE[22],1])
						elif act[3] == 3:
							#REDUCE AGILITY
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tagi[self.turn] < 2:
									self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
									self.pagi[self.turn]+=act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[20] + str(act[2]) + dtb.BATTLE[23],1])
									self.tagi[self.turn]+=1
							#GROW AGILITY
							elif act[2] > 0:
								i['AGILITY']+=act[2]
								self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + dtb.BATTLE[21] + str(act[2]) + dtb.BATTLE[23],1])
						elif act[3] == 4:
							#REDUCE STRENGHT
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tstr[self.turn]<2:
									self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
									self.pstr[self.turn] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[20] + str(act[2]) + dtb.BATTLE[24],1])
									self.tstr[self.turn] += 1
							#GROW STRENGHT
							elif act[2] > 0:
								i['STRENGHT'] += act[2]
								self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + dtb.BATTLE[21] + str(act[2]) + dtb.BATTLE[24],1])
						elif act[3] == 5:
							#REDUCE RESISTANCE
							if act[2] < 0:
								self.turn = self.fig[pl]['N']
								if self.tagi[self.turn] < 2:
									self.ch_ton.play(res.SOUND['ATTRIBUTE_LOSS'])
									self.pres[self.turn] += act[2]
									self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[20] + str(act[2]) + dtb.BATTLE[25],1])
									self.tres[self.turn] += 1
							#GROW RESISTANCE
							elif act[2] > 0:
								i['RESISTANCE'] += act[2]
								self.ch_ton.play(res.SOUND['ATTRIBUTE_GAIN'])
								self.dialog([dd, i['NAME'] + dtb.BATTLE[21] + str(act[2]) + dtb.BATTLE[25],1])
						#INPUT CONDITION
						elif act[3] == 6:	
							self.fig[pl]['HEALTH'] = act[2]
							if self.dlgfa > 0:
								if act[2] == 2: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[26],1])
								if act[2] == 3: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[27],1])
								if act[2] == 4: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[28],1])
								if act[2] == 5: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[29],1])
								if act[2] == 6: self.dialog([dd, self.fig[pl]['NAME'] +  dtb.BATTLE[30],1])
								if act[2] == 7: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[31],1])
								if act[2] == 8: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[32],1])
								if act[2] == 9: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[33],1])
								if act[2] == 10 or act[2] == 11 or act[2] == 12: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[34],1])
								if act[2] == 13: self.dialog([dd, self.fig[pl]['NAME'] + dtb.BATTLE[35],1])
								self.fig[pl]['HEALTH'] = act[2]
								if self.fig[pl]['HEALTH'] == 5: self.pagi[pl] -= 20
								act[2] == 0
						#ADD ANOMALY
						elif act[3] == 7:
							prb = round(random.randint(0,100))
							if prb > 49:
								wh = round(random.randint(0,len(act[2]) - 1))
								nw = dtb.FREAKS[act[2][wh]].copy()
								nw['FILE'] = act[2][wh]
								nw['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (nw['FILE']) + '_stand.png')
								nw['MASK'] = pygame.Rect(230,180,44,85)
								nw['FIGHTING'] = True
								nw['HEALTH'] = 0
								nw['RESISTANCE'] = nw['HP']
								nw['DIRECTION'] = 1
								nw['FADE'] = 10
								if res.MAP == nw['HABITAT']:
									nw['AGILITY'] += 2
									nw['HP'] += 5
								self.foe.append(nw)
								if self.dlgfa > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,nw['NAME'] + dtb.BATTLE[37],1])
							else:
								if self.dlgfa > 0:
									self.dialog([i['NAME'] + ' usou ' + act[0],1,dtb.BATTLE[38],1])
						#RUN AWAY
						elif act[3] == 9:
							if self.dlgfa > 0: self.dialog([i['NAME'] + ' arregou!',1])
							while i['FADE'] > 0:
								i['FADE'] -= 1
								self.run()
							i['FIGHTING'] = False
							i['HP'] = 0
						#CHARGE ATTACK
						elif act[3] == 10:
							self.ch_ton.play(res.SOUND['CHARGE'])
							self.attackimation(act[5])
							self.turn = self.fig[pl]['N']
							self.ch_ton.play(res.SOUND['SCREAM_' + i['FILE'].upper()])
							self.ch_sfx.play(res.SOUND['DAMAGE_1'])
							if self.attackimation(act[5]) == False:
								act[2] -= int(act[2]/5)
								self.fig[pl]['HP'] += act[2] + self.pres[pl]
								self.hitisplay(-act[2] * 2, None, '', (0,0,0))
								self.hpl += act[2]
							else:
								self.ch_sfx.play(res.SOUND['HIT'])
								for p in range(dmg * 3):
									self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(random.randint(3,5)), 'DIRECTION': round(random.randint(0,360)), 'SPEED': round(random.randint(2,6))})
								self.hitisplay(10, i['MASK'], str(act[2]), (200, 0, 0))
								if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (i['FILE'])+ '_stand.png')
								i['HP'] -= act[2]
								self.hits += 1
								self.tdmg += act[2]
							#COUNTER DAMAGE
							if i['HP'] <= 0:
								self.ch_ton.play(res.SOUND['SCREAM_' + i['FILE'].upper()])
								while i['FADE'] > 0:
									i['FADE'] -= 1
									self.run()
								if i['ITEM'] != None:
									prb = round(random.randint(0,100))
									if prb > i['ITEM'][1]:
										self.inv.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
										self.ch_sfx.play(res.SOUND['ITEM_GET'])
										self.notification('Adquiriu ' + dtb.ITEMS[i['ITEM'][0]][0],(255, 255, 255))
								i['FIGHTING'] = False
						#CHECK DEATH
						if pl < len(self.fig) and self.fig[pl]['HP'] <= 0:
							self.mnu = 1
							if self.fig[pl]['BLESS'] == 0:
								self.fig[pl]['HEALTH'] = 15
								self.ch_ton.play(res.SOUND['INCONSCIOUS'])
							else:
								self.fig[pl]['BLESS'] -= 1
								self.fig[pl]['HP'] = dtb.CLASSES[self.fig[pl]['CLASS']]['RESISTANCE'][self.fig[pl]['LEVEL']]
						i['SPRITE'] = pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + (i['FILE']).lower() + '_stand.png')
					#MISS
					else:
						i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']).lower() + '_stand.png')
						self.ch_sfx.play(res.SOUND['MISS'])
				#TURN AROUND
				elif i['HEALTH'] == 1 and self.dlgfa > 0:
					i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_stand.png')
					i['HEALTH'] = 9
			if self.turn > -1:
				self.turn =  0
				self.mnu = 1
				for i in range(len(self.fig)):
					if self.pres[i] > dtb.CLASSES[self.fig[i]['CLASS']]['RESISTANCE'][self.fig[i]['LEVEL']]:
						self.pres[i] = dtb.CLASSES[self.fig[i]['CLASS']]['RESISTANCE'][self.fig[i]['LEVEL']]
		#OBSTACLES
		if self.obstacles == True:
			dmg = []
			self.mnu = 3
			for p in range(len(self.fig)):
				dmg.append(5)
				for a in res.INVENTORY[self.fig[p]['N']][:-1]:
					if a[0][0] != '_':
						dmg[p] += int(dtb.ITEMS[a[0][0]][5])
						a[0][1] = int(a[0][1])
						a[0][1] -= 1
						if a[0][1] == 0:
							self.dialog([a[0][0] + dtb.BATTLE[36],1])
							a[0] = ['_','0000','_','_']
						a[0][1] = str(a[0][1])

			if self.attackimation(1) == True:
				for p in range(len(self.fig)): dmg -= int(dmg/5)
				self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
			else:
				for p in range(len(self.fig)): self.fig[p]['HP'] += dmg[p] + self.pres[p]
				self.hitisplay(-dmg[p] * 2, None, '', (0,0,0))
				self.ch_sfx.play(res.SOUND['DAMAGE_1'])
				self.hpl += dmg[p]
			self.mnu = 1
		#VICTORY
		dth = 0
		for d in self.foe + self.mrc:
			if d['HP'] <= 0: dth += 1
		if dth == len(self.foe) + len(self.mrc) and self.battle == True:
			self.ch_msc.fadeout(500)
			if len(self.foe) >= 10: self.ch_ton.play(res.SOUND['BATTLE_BOSS_WON'])
			elif len(self.foe) > 0 and self.foe[0]['TYPE'] == 'boss': self.ch_ton.play(res.SOUND['BATTLE_BOSS_WON'])
			elif self.hpl == 0: self.ch_ton.play(res.SOUND['BATTLE_PERFECT'])
			else: self.ch_ton.play(res.SOUND['BATTLE_WON'])
			self.tbt += round(self.btime/10)
			xp = int(((self.hits*self.tdmg)-self.hpl+self.tbt)/len(self.fig))
			self.mnu = self.displayzw
			self.transiction(True, int(self.displayzh/2))
			self.turn = -4
			self.obstacles = False
			self.bbm = 0
			while self.mnu > 0:
				self.mnu -= 60
				self.run()
			self.wait()
			#GREENBLOOD
			btls = None
			for i in res.PARTY[res.FORMATION]:
				for it in ['bottle100','bottle250']:
					btls = self.inv.find(i,it)
					if btls != None and int(btls[1]) < dtb.ITEMS[btls[0]][5]: break
				if btls != None and int(btls[1]) < dtb.ITEMS[btls[0]][5]: break
			if btls != None:
				btls[1] = int(btls[1])
				gb = btls[1]
				for i in self.foe:
					gb += i['BLOOD']
				while btls[1] < gb:
					if (gb - btls[1]) > 100: btls[1] += 5
					else: btls[1] += 1
					if btls[1] >= dtb.ITEMS[btls[0]][5]: break
					self.run()
				btls[1] = str(btls[1])
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
						self.bbg = pygame.image.load(res.BACKG_PATH + 'level_up.png')
						self.ch_ton.play(res.SOUND['LEVEL_UP'],-1)
						self.transiction(False, 100, 10)
						lvlup = True
					if self.mnu < -self.displayzw:
						self.mnu = -self.displayzw
					while self.mnu > -(self.displayzw + 	100):
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
			if lvlup == True:
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
			if self.rad.onoff == True: pygame.mixer.music.unpause()
			self.player[0]['PAUSE'] = 0
			self.transiction(False, 0)
		#GAME OVER
		dth = 0
		for d in self.fig:
			if d['HP'] <= 0: dth += 1
			elif d['HEALTH'] in [8,13,14,15]: dth += 1
		if dth == len(self.fig):
			if self.rad.onoff == True: pygame.mixer.music.stop(); self.rad.onoff = False
			self.ch_msc.fadeout(500)
			self.ch_ton.play(res.SOUND['BATTLE_LOST'])
			self.turn = -5
			self.transiction(True, int(self.displayzh/2))
			self.obstacles = False
			self.bbm = 0
			self.mnu = self.displayzw
			acc = 60
			while self.mnu > 0:
				self.mnu -= acc
				acc -= 2
				self.run()
			self.turn = -5
			self.wait()
			res.load_data()
			res.PX = 315
			res.PY = 200
			src = None
			for i in res.PARTY[res.FORMATION]:
				src = self.inv.find(i,'credit_card')
				if src == None:
					src = self.inv.find(i,'wallet')
					if src != None:
						src[1] = str(int(scr[1][6:]) - 100) + scr[1][6:]
				else:
					src[1] = str(int(scr[1]) - 100)
			for i in res.PARTY[res.FORMATION]:
				res.CHARACTERS[i]['HP'] = res.CHARACTERS[i]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
				res.CHARACTERS[i]['HEALTH'] = 0
			self.__init__()
			if res.CHAPTER > 0: self.rendermap('hospital_0')
			self.transiction(False, 0)

	def hitisplay(self, ex, tar, dmg, col):
		self.dmgy = 200
		hitac = 8
		lgy = 1
		inf = 0
		wt = 0
		#SHAKE SCREEN
		if tar == None:
			while ex != 0:
				self.screen.fill((255, 0, 0))
				if ex > 0:
					self.displayx = ex
					self.displayy = ex
					ex = -ex
				elif ex < 0:
					self.displayx = ex
					self.displayy = ex
					ex = -ex
					ex -= 1
				self.run()
			self.displayx = 0
			self.displayy = 0
			self.run()
		#DAMAGE INFORMATION
		else:
			self.dmginfo = pygame.Surface((9 + (len(dmg) * 17),40), pygame.SRCALPHA, 32)
			self.dmginfo.convert_alpha()

			sx = tar.x
			sy = tar.y
			while wt < 10:
				tar.x = sx
				tar.y = sy
				if ex > 0:
					tar.x += ex
					tar.y += ex
					ex = -ex
				elif ex < 0:
					tar.x += ex
					tar.y += ex
					ex = -ex
					ex -= 1
				if inf == 0:
					self.dmgy -= hitac
					hitac -= 1
					lgy += 1
					if hitac == 0: inf = 1
				elif inf == 1:
					self.dmgy += hitac
					hitac += 1
					if hitac == 8: inf = 2
				elif ex == 0:
					wt += 1
				if self.dmginfo != '':
					self.dmginfo.blit(self.fnt['MININFO'].render(dmg, True, (0,0,0)), (11 - lgy, 11 - lgy))
					self.dmginfo.blit(self.fnt['MININFO'].render(dmg, True, col), (10 - lgy, 10 - lgy))
				self.run()
			tar.x = sx
			tar.y = sy
		self.run()
		self.dmginfo = ''

	def attackimation(self, wh):
		self.effttack = wh
		self.effgif = 0
		ddg = False
		counter = False
		if wh != 10:
			while self.effgif < len(res.SPRITES['ATTACKIMATION_' + str(wh)]):
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[res.ACT[0]] and self.effgif == len(res.SPRITES['ATTACKIMATION_' + str(wh)]):
						ddg = True
				self.run()
				self.effgif += 0.5
		else:
			while True:
				for event in pygame.event.get():
					self.pressed = pygame.key.get_pressed()
					if self.pressed[res.ACT[0]] and self.effgif > 4.0:
						counter = True
				if counter == False: self.effgif += 0.25
				if counter == True: self.effgif -= 0.25

				if self.effgif == len(res.SPRITES['ATTACKIMATION_' + str(wh)]): ddg = False; break
				elif self.effgif == 0.0: ddg = True; break
				self.run()

		self.effttack = None
		self.effgif = 0

		return ddg

	def rendermap(self, mp):
		if mp == 'rodoviary':
			self.map = pytmx.load_pygame(res.MAPS_PATH + mp + '.tmx')
			res.MAP = 0
		elif mp[1:8] == 'highway':
			res.MAP = int(mp[0]) + 1
			self.map = pytmx.load_pygame(res.MAPS_PATH + mp[1:11] + '.tmx')
			self.cityname = dtb.CITIES[res.MAP - 1][0]
		else: self.map = pytmx.load_pygame(res.MAPS_PATH + mp + '.tmx')
		self.room = mp
		self.cam.x = 0
		self.cam.y = 0
		self.tilmap = [[],[],[],[],[],[],[]]
		self.objects = []
		for i in range(len(self.player)):
			self.objects.append([0,i,self.player[i]['RECT'].y])
		self.tilrect = [[],[],[],[],[],[]]
		self.en = []
		self.foe = []
		self.pets = []
		self.npcs = []
		self.vehicles = []
		self.portals = []
		self.signs = []
		self.radars = []
		self.tolls = []
		self.lights = []
		self.tents = []
		self.nodes = []
		self.areas = []
		self.particles = []
		self.loadingif = 0
		self.bbm = 0
		for i in self.player: i['NODES'] = []

		#DRAW MAP BOUNDARIES
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, (self.map.height * self.map.tileheight) + self.map.tileheight,self.map.tilewidth * self.map.width,self.map.tileheight)])
		self.tilrect[3].append(['WALL',pygame.Rect(-self.map.tilewidth, -self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		self.tilrect[3].append(['WALL',pygame.Rect((self.map.width * self.map.tilewidth) + self.map.tilewidth,-self.map.tileheight,self.map.tilewidth,self.map.tileheight * self.map.height)])
		#DRAW MAP
		for i in range(3):
			for a in range(2):
				self.tilmap[i].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
				for y in range(0, self.map.height):
					for x in range(0, self.map.width):
						try: gid = self.map.get_tile_gid(x, y, i)
						except: gid = None
						#NO TILE
						if gid == None and i == 0:
							self.tilrect[0].append(['WALL',pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
							if self.tilrect[3][len(self.tilrect[3]) - 1][0] == 'WALL': self.tilrect[3][len(self.tilrect[3]) - 1][1].width += self.map.tilewidth
							else: self.tilrect[3].append(['WALL',pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
						#FOUND TILE
						else:
							tl = self.map.get_tile_properties_by_gid(gid)
							if tl != None:
								#TILE FRAME ANIMATION
								if tl['frames'] != []: image = self.map.get_tile_image_by_gid(tl['frames'][a].gid)
								else: image = self.map.get_tile_image_by_gid(gid)
								image.convert()
								#TILE IMAGE
								try: t = self.map.get_tile_properties(x, y, i)['TYPE'].upper()
								except: t = 'CLOTH'
								#PARALLAX SCROLLING
								if t.startswith('BACKGROUND'):
									if len(self.tilmap[int(t[10])]) < a + 1:
										self.tilmap[int(t[10])].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
									if res.TIME[0] >= 18: fr = 1
									elif res.TIME[0] >= 6: fr = 0
									else: fr = 1
									if tl['frames'] != []: image = self.map.get_tile_image_by_gid(tl['frames'][fr].gid).convert()
									else: image = self.map.get_tile_image_by_gid(gid).convert()
									self.tilmap[int(t[10])][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#MOON
								elif t == 'MOON':
									if len(self.tilmap[4]) < a + 1:
										self.tilmap[4].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
									if res.TIME[0] >= 18: fr = res.DATE[4]
									elif res.TIME[0] >= 6: fr = 0
									else: fr = res.DATE[4]
									image = self.map.get_tile_image_by_gid(tl['frames'][fr].gid).convert()
									self.tilmap[4][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#NORMAL TILE
								elif t not in ['CARRY','HOLD','HIDEON','HIDEOFF']:
									self.tilmap[i][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								#TILRECT
								if i < 2 and a == 0:
									#STEP TILES
									if i == 0:
										self.tilrect[0].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
									#MOVABLE OBJECTS
									if t in ['CARRY','HOLD']:
										self.tilrect[2].append([image,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight),image])
									#MIRROR SURFACES
									if t == 'WATER':
										self.tilrect[5].append([pygame.Surface((self.map.tilewidth,self.map.height),pygame.SRCALPHA),pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
									#WALLS
									elif t == 'WALL':
										#GLUE WALLS
										bft = self.tilrect[3][len(self.tilrect[3]) - 1]
										if bft[1].y == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										elif bft[1].height == (y - 1) * self.map.tileheight: bft[1].height += self.map.tileheight
										#APPEND WALLS
										else: self.tilrect[3].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
								#HIDE TILES
								else:
									if t.startswith('HIDE'): self.tilrect[4].append([t,pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,int(self.map.tilewidth),int(self.map.tileheight))])
								self.loading()
		#OBJECTS
		vhn = -1
		for lyr in self.map.layers:
			if lyr.name.startswith('Camada'): continue
			for i in lyr:
				#NPCS
				if i.name.startswith('npc'):
					obj = self.map.get_object_by_name(i.name)
					npc = {'N': int(i.name[4:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'TYPE': 0, 'INDEX': '000000', 'WHO': None,
					'GIF': 0.0,'BLINK': 100,'HEAD': 'BLANKD_0000','SPRITE': 'STANDD_000','MOVE': 'fixed','DIRECTION': 3,'SPEED': 0, 'PAUSE': 0,
					'JUMP': 0,'GRAVITY': -5,'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','TALKING': False,'SWIM': None,'HOLD': None}

					add = True
					if obj.type == 'None': npc['TYPE'] = None
					elif obj.type.startswith('scene'): npc['TYPE'] = obj.type
					elif obj.type.startswith('if'):
						if res.SCENE == int(obj.type[2:]): npc['TYPE'] = 0
						else: add = False
					else: npc['TYPE'] = int(obj.type)

					for pr in obj.properties.items():
						if pr[0] == 'INDEX':
							npc['INDEX'] = pr[1]
							npc['HEAD'] = 'BLANKD_' + pr[1][0:3] + pr[1][5]
							npc['SPRITE'] = 'STANDD_' + pr[1][3:6]
						if pr[0] == 'WHO': npc['WHO'] = pr[1]
						if pr[0] == 'DIRECTION': npc['DIRECTION'] = int(pr[1]); npc['MOVE'] = 'stand'
						if pr[0] == 'MOVE': npc['MOVE'] = pr[1]

					if add == True:
						self.npcs.append(npc)
						self.objects.append([2,int(i.name[4:]),int(obj.y)])
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
					self.objects.append([3,int(i.name[8:]),int(obj.y)])
				#PORTALS
				if i.name.startswith('portal'):
					obj = self.map.get_object_by_name(i.name)
					dt = {'N': int(i.name[7:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'TYPE': int(obj.type), 'PX': obj.properties['PX'], 'PY': obj.properties['PY'], 'MAP': None,
					'OPENING': None,'CLOSURE': None,'MUSIC': None,'MATCH': None}
					for pr in obj.properties.items():
						if pr[0] == 'TIME':
							if obj.properties['TIME'].startswith('key'):
								dt['OPENING'] = obj.properties['TIME'][0:3]
								dt['CLOSURE'] = obj.properties['TIME'][3:7]
							else:
								dt['OPENING'] = [int(obj.properties['TIME'][0:2]),int(obj.properties['TIME'][2:4])]
								dt['CLOSURE'] = [int(obj.properties['TIME'][4:6]),int(obj.properties['TIME'][6:8])]
						if pr[0] == 'MUSIC':
							dt['MUSIC'] = obj.properties['MUSIC']
						if pr[0] == 'MATCH':
							dt['MATCH'] = obj.properties['MATCH']
						if pr[0] == 'MAP':
							dt['MAP'] = obj.properties['MAP']
						if pr[0].startswith('IF'):
							if pr[0][3:6] == 'NOT':
								pass
							elif res.CHAPTER == int(pr[0][3:5]):
								dt['MAP'] = pr[1]
							else: dt['MAP'] = obj.properties['IF NOT']
					self.portals.append(dt)
					self.objects.append([4,int(i.name[7:]),int(obj.y)])
				#SIGNS
				if i.name.startswith('sign'):
					obj = self.map.get_object_by_name(i.name)
					sg = {'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), len(obj.type) * 10, int(obj.height)), 'TEXT': obj.type}
					for pr in obj.properties.items():
						if pr[0] == 'ICON': sg['ICON'] = pr[1]
					self.signs.append(sg)
					self.objects.append([5,int(i.name[5:]),int(obj.y)])
				#LIGHTS
				if i.name.startswith('light'):
					obj = self.map.get_object_by_name(i.name)
					img = pygame.Surface((int(obj.width),int(obj.height)),pygame.SRCALPHA)
					if obj.type == '0':
						pygame.draw.ellipse(img, (255, 255, 255, 100), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					elif obj.type == '1':
						for r in range(math.floor(obj.height/2)):
							srf = pygame.Surface((obj.width,obj.height),pygame.SRCALPHA)
							pygame.draw.circle(srf, (255, 255, 255, r), (math.floor(obj.width/2),math.floor(obj.height/2)), r)
							img.blit(srf,(0,0))
					elif obj.type == '2':
						pygame.draw.ellipse(img, (255, 208, 0, 100), pygame.Rect(0,0,int(obj.width),int(obj.height)))
					self.lights.append({'N': int(i.name[6:]), 'TYPE': obj.type, 'IMAGE': img, 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))})
					self.objects.append([6,int(i.name[6:]),self.map.height * self.map.tileheight])
				#TOLLS
				if i.name.startswith('toll'):
					obj = self.map.get_object_by_name(i.name)
					tl = {'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'CENTER': pygame.Rect(0,0,44,16).center, 'ANGLE': int(obj.rotation), 'TIME': 0}
					self.tolls.append(tl)
					self.objects.append([7,int(i.name[5:]),int(obj.y)])
				#RADARS
				if i.name.startswith('radar'):
					obj = self.map.get_object_by_name(i.name)
					self.radars.append({'N': int(i.name[6:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'LIMIT': 80})
					self.objects.append([7,int(i.name[5:]),int(obj.y)])
				#NODES
				if i.name.startswith('node'):
					obj = self.map.get_object_by_name(i.name)
					self.nodes.append({'N': int(i.name[5:]), 'TYPE': int(obj.type), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)), 'GOING': int(obj.properties['GOING'])})
					self.objects.append([7,int(i.name[5:]),int(obj.y)])
				#AREAS
				if i.name.startswith('area'):
					obj = self.map.get_object_by_name(i.name)
					self.areas.append({'N': int(i.name[5:]), 'RECT': pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))})
			self.loading()
		#VEHICLE
		if self.driving > 0:
			vh = dtb.VEHICLES['moto_0'].copy()
			vh['N'] = vhn + 1
			vh['RECT'] = pygame.Rect(int(self.player[0]['RECT'].x), int(self.player[0]['RECT'].y), 60, 10)
			vh['INDEX'] = 0
			vh['DIRECTION'] = 1
			vh['MOVE'] = 'fixed'
			self.vehicles.append(vh)
			self.objects.append([3,vhn + 1,int(self.player[0]['RECT'].y)])
			self.driving = vhn + 2
		#ENEMIES
		for prp in self.map.properties.items():
			if prp[0] == 'ENEMIES':
				st = 0
				en = 0
				lst = []
				for i in self.map.properties['ENEMIES']:
					if i == '-':
						lst.append(self.map.properties['ENEMIES'][st:en])
						st = en + 1
					en += 1
				for i in range(round(random.randint(3,10))):
					wh = lst[round(random.randint(0,len(lst) - 1))]
					self.en.append(dtb.FREAKS[wh].copy())
					self.en[i]['N'] = i
					self.en[i]['FILE'] = wh
					self.en[i]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.en[i]['FILE']) + '_stand.png')
					sz = pygame.image.load(res.FREAKS_PATH + self.en[i]['FILE'] + '_mini.png').get_rect()
					self.en[i]['RECT'] = pygame.Rect(self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].x,self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].y,sz.width,sz.height)
					self.en[i]['DIRECTION'] = 1
					self.en[i]['FIGHTING'] = False
					self.en[i]['HEALTH'] = 0
					self.en[i]['TIME'] = 20
					self.en[i]['EFFECT'] = 0.0
					self.en[i]['JUMP'] = 0
					if mp[1:-2] == self.en[i]['HABITAT']:
						self.en[i]['AGILITY'] += 2
						self.en[i]['HP'] += 5
					self.objects.append([1,i,self.en[i]['RECT'].y])
			elif prp[0] == 'SIGNAL':
				res.SIGNAL = self.map.properties['SIGNAL']
		#PETS
		for i in range(random.randint(0,5)):
			lst = ['PIGEON','DOG0']
			prb = random.randint(0,len(lst) - 1)
			img = res.SPRITES[lst[prb] + '_WALK'][0]
			sz = img.get_rect()
			rct = pygame.Rect(self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].x,self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))][1].y,sz.width,sz.height)
			self.pets.append({'N': i,'FILE': lst[prb],'RECT': rct,'SPRITE': res.SPRITES[lst[prb] + '_WALK'],'GIF': 0.0,'DIRECTION': 1,'SPEED': 2,'MOVE': 'walk','TIME': 20})
			self.objects.append([10,i,self.pets[i]['RECT'].y])
		self.loadingif = None

	def notification(self, txt, col):
		if txt.startswith('hp_') == False and txt.startswith('ml_') == False and txt.startswith('it_') == False:
			if res.DISLEXIC == True:
				self.nottxt = ''
				for t in txt:
					self.nottxt += t + ' '
			else: self.nottxt = txt
		else: self.nottxt = txt
		self.notcol = col
		self.notx = 0
		w = 0
		while self.notx < 180:
			self.run()
			self.notx += 20
		while w < 50:
			self.run()
			w += 1
		self.notx = 0

	def draw(self):
		for i in self.display: i.fill((0,0,0,0))
		if self.battle == True and self.turn < 0: self.hpctrl = []
		elif self.dlgfa < 500: self.hpctrl = []
		else: self.hpctrl = dtb.HINTS['MENUS']
		#TILEMATION
		if self.player[0]['PAUSE'] < 2: self.tilemation += 0.1
		if self.tilemation >= 2.0: self.tilemation = 0.0
		#TILED MAP
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 12:
			self.display[0].fill((0,0,0))
		elif self.turn != -6:
			if len(self.tilmap[3]) > 0: self.display[0].blit(self.tilmap[3][math.floor(self.tilemation)], (0, 0))
			if len(self.tilmap[4]) > 0: self.display[0].blit(self.tilmap[4][math.floor(self.tilemation)], (-math.floor(self.cam.x/5), -math.floor(self.cam.y/5)))
			if len(self.tilmap[5]) > 0: self.display[0].blit(self.tilmap[5][math.floor(self.tilemation)], (-math.floor(self.cam.x/2), -math.floor(self.cam.y/2)))
			self.display[0].blit(self.tilmap[0][math.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
			self.display[0].blit(self.tilmap[1][math.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
			#MOVABLE OBJECTS
			for i in self.tilrect[2]:
				srf = i[0]
				for p in self.player:
					ref = pygame.transform.flip(p['SPRITE'][p['GIF']],(False,True))
					srf.blit(ref,(p['RECT'].x - i[1].x - self.cam.x,['RECT'].y - i[1].y - self.cam.y))
				self.display[0].blit(srf, (i[1].x - self.cam.x, i[1].y - self.cam.y + 20))
			#MIRROR SURFACES
			for i in self.tilrect[5]:
				self.display[0].blit(i[1], (i[1].x - self.cam.x, i[1].y - self.cam.y))
		else: self.display[0].fill((250,10,10))
		'''for i in self.tilrect[4]:
			srf = pygame.Surface((20,20))
			srf.blit(self.display,(-i[1].x,-i[1].y))
			self.display[0].blit(srf,(i[1].x + 6,i[1].y + 6))'''
		#DEPTH
		dpth = 0
		for i in range(len(self.objects)):
			if i!= len(self.objects) - 1:
				if self.objects[i][2] > self.objects[i + 1][2]:
					self.objects.insert(i, self.objects[i + 1])
					del self.objects[i + 2]
		#DELETE OBJECTS
		for i in range(len(self.en)):
			if self.en[i]['HP'] <= 0: del self.en[i]; break
		for i in range(len(self.npcs)):
			if self.npcs[i]['DIRECTION'] == 0: del self.npcs[i]; break
		#OVERWORLD
		if self.battle == False:
			#OBJECTS
			cm = pygame.Rect(self.cam.x - 100,self.cam.y - 100,self.cam.width + 200,self.cam.height + 200)
			for y in self.objects:
				if y[0] == 0:
					#PLAYER
					p = 0
					for i in self.player:
						if y[1] == p and self.colide(i['RECT'],cm):
							if self.rectdebug == True: pygame.draw.rect(self.display[0], (0,0,255), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
							self.people(i,True)
							#CONDITIONS
							if res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HEALTH'] > 1:
								if i['SHK'] == 0:
									pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								else: pygame.draw.rect(self.display[0], (255,10,10), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HEALTH']) + '.png'), (i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40))
							#TILE COLISION
							if i['STEP'] > 0: i['STEP'] -= 1
							if self.rectdebug == True:
								for t in self.tilrect[3]:
									if t[0] == 'WALL': pygame.draw.rect(self.display[0],(255,0,0,10),pygame.Rect(t[1].x + 2 - self.cam.x,t[1].y + 2 - self.cam.y,t[1].width - 4,t[1].height - 4))
							for tl in range(1):
								try:
									t = self.tilrect[0][(math.floor(self.player[p]['RECT'].y/self.map.tilewidth) * self.map.width) + math.floor(self.player[p]['RECT'].x/self.map.tilewidth)]
								except: t = None
								if t != None:
									if i['SPEED'] > 0 and self.dlgfa > 0 and i['PAUSE'] == 0:
										if self.driving == 0:
											#JUMP
											if t[0].startswith('JUMP') and i['DIRECTION'] == int(t[0][4]) and i['GRAVITY'] == -5:
												i['GRAVITY'] = 4.5 + float(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ACROBATICS']/2)
												i['STEP'] = 0
												self.ch_sfx.play(res.SOUND['FALL'])
											#STEP SOUNDS
											elif t[0] != 'WALL' and t[0] != 'NONE' and t[0].startswith('JUMP') == False and i['JUMP'] == 0:
												if i['STEP'] == 0 and res.MAP > 0:
													#self.ch_stp.stop()
													self.ch_stp.play(res.SOUND['STEP_' + t[0]])
													if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
												#SWIMMING
												if t[0] == 'WATER':
													if i['SWIM'] == None: i['SWIM'] = 0.0
												else: i['SWIM'] = None
										#DRIVING
										elif t[0] != 'WALL' and t[0].startswith('JUMP') == False and i['JUMP'] == 0:
											if i['STEP'] == 0 and res.MAP > 0:
												self.ch_stp.stop()
												self.ch_stp.play(res.SOUND['STEP_VEHICLE'])
												if i['SPEED'] > 0: i['STEP'] = math.floor(12/i['SPEED'])
							y[2] = i['RECT'].y
						p += 1
				#ENEMIES
				if y[0] == 1:
					for i in self.en:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.enemy(i); y[2] = i['RECT'].y
				#NPCS
				elif y[0] == 2:
					for i in self.npcs:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.npc(i); y[2] = i['RECT'].y
				#VEHICLES
				elif y[0] == 3:
					for i in self.vehicles:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.vehicle(i); y[2] = i['RECT'].y
				#PORTALS
				elif y[0] == 4:
					for i in self.portals:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.portal(i); y[2] = i['RECT'].y
				#SIGNS
				elif y[0] == 5:
					for i in self.signs:
						if i['N'] == y[1] and self.colide(i['RECT'],cm):
							if self.colide(i['RECT'], self.cam) and self.turn != -6 and i['TEXT'].startswith('radar') == False:
								if res.MAP != 0:
									sz = self.fnt['DEFAULT'].size(dtb.SIGNS[i['TEXT']])
									pygame.draw.rect(self.display[0], (250, 250, 250), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, math.floor(sz[0]/2) + 10, math.floor(sz[1]/2) + 10))
									self.display[1].blit(self.fnt['DEFAULT'].render(dtb.SIGNS[i['TEXT']], True, (0,0,0)), ((5 + i['RECT'].x - self.cam.x) * 2,(5 + i['RECT'].y - self.cam.y) * 2))
								else: self.display[1].blit(self.fnt['DEFAULT'].render(i['TEXT'], True, (250,250,250)), ((i['RECT'].x - self.cam.x - math.floor(self.cam.x/5)) * 2,(i['RECT'].y - self.cam.y - math.floor(self.cam.y/5)) * 2))
							y[2] = i['RECT'].y
				#TOLLS
				elif y[0] == 7:
					for i in self.tolls:
						if i['N'] == y[1] and self.colide(i['RECT'],cm):
							srf = pygame.Surface((44,44), pygame.SRCALPHA)
							trs = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'toll.png'),i['ANGLE'] + 90)
							#i['CENTER'] = trs.get_rect(center = i['CENTER'].center)
							srf.blit(trs,(0,0))
							self.display[0].blit(srf,(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
							if i['TIME'] > 0: i['TIME'] -= 1
							if self.colide(self.player[0]['RECT'],i['RECT']):
								if i['TIME'] == 0:
									mny = self.inv.find(0,'credit_card')
									print('monye')
									print(mny)
									if mny != None and int(mny[1]) >= 10:
										self.ch_sfx.play(res.SOUND['BUY'])
										mny[1] = str(int(mny[1]) - 10)
										i['TIME'] = 180
										self.notification('Pedágio -$ 10',(255, 255, 255))
									elif self.facing(self.player[0],i['RECT']) == 2:
										self.player[0]['SPEED'] = 0
							y[2] = i['RECT'].y
				#RADARS
				elif y[0] == 8:
					for i in self.radars:
						if i['N'] == y[1] and self.colide(i['RECT'],cm):
							if self.colide(self.player[0]['RECT'],i['RECT']):
								for j in self.signs:
									if j['TEXT'] == 'radar' + str(i['N']):
										j['TEXT'] = self.player[0]['SPEED']
								if self.player[0]['SPEED'] > i['LIMIT']:
									self.ch_sfx.play(res.SOUND['BUY'])
									res.MONEY -= 10
							y[2] = i['RECT'].y
				#TENTS
				elif y[0] == 9:
					for i in self.tents:
						if i['N'] == y[1] and self.colide(i['RECT'],cm):
							self.display[0].blit(i['SPRITE'],(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y - 20))
							if self.colide(self.player[0]['RECT'],i['RECT']):
								 self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (i['RECT'].x - self.cam.x + int(i['RECT'].width/2) - 5,i['RECT'].y - self.cam.y - i['RECT'].height * 2))
								 if self.pressed[4][0]:
								 	self.sleepin = not self.sleepin
							y[2] = i['RECT'].y
				#PETS
				elif y[0] == 10:
					for i in self.pets:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.pet(i); y[2] = i['RECT'].y
			#BUILD ITEMS
			if self.build != '':
				srf = pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')
				srf.set_alpha(100)
				self.display[0].blit(srf,((math.floor((self.player[0]['RECT'].x + 15)/30) * 30) - self.cam.x,(math.floor((self.player[0]['RECT'].y + 15)/30) * 30) - self.cam.y - 20))
			#NODES DEBUG
			if self.rectdebug == True:
				for i in self.nodes: pygame.draw.rect(self.display[0], (250,250,10),pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			#OVER TILES & CLOUDS
			if res.MAP > 0:
				if self.turn != -6 and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] != 12:
					self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
			else:
				self.bbm += 0.2
				if math.floor(self.bbm) > (self.map.width * self.map.tilewidth): self.bbm = 0.0
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbm) - self.cam.x, -self.cam.y))
				self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)], (math.floor(self.bbm) - (self.map.width * self.map.tilewidth) - self.cam.x, -self.cam.y))
			'''for t in self.tilrect[4 + math.floor(self.tilemation)]:
				if self.colide(t[1],self.cam): self.display[0].blit(t[2], (t[1].x - self.cam.x, t[1].y - self.cam.y))'''
			#DAYTIME & WEATHER
			if res.TIME[0] >= 18: tim = 100
			elif res.TIME[0] >= 6: tim = 0
			else: tim = 100
			srf = pygame.Surface((self.displayzw,self.displayzh))
			srf.set_alpha(tim)
			srf.fill((0, 58, 160))
			if self.map.properties['INTERIOR'] == '0': self.display[0].blit(srf, (0,0))
			if len(self.tilmap[6]) > 0: self.display[0].blit(self.tilmap[6][math.floor(self.tilemation)], (0, 0))
			#LIGHTS
			for y in self.objects:
				if y[0] == 6:
					for i in self.lights:
						if i['N'] == y[1]:
							if self.colide(i['RECT'], self.cam):
								self.display[0].blit(i['IMAGE'], (i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
			#RAIN
			if self.map.properties['INTERIOR'] == '0' and res.WEATHER == 1 and res.MAP > 0:
				if len(self.particles) < 50:
					for i in range(5):
						self.particles.append({'TYPE': 'raindrop', 'X': round(random.randint(0,self.cam.width + int(self.cam.width/4))), 'Y': -int(self.cam.height/2),
							'RADIUS': 2, 'DIRECTION': 90, 'SPEED': 15, 'TIME': round(random.randint(10,60)), 'GIF': 0})
						for p in range(len(self.particles)):
							if self.particles[p]['TYPE'] == 'raindrop' and self.particles[p]['GIF'] > 8:
								del self.particles[p]; break

				if len(self.particles) > 0:
					for p in self.particles:
						if p['TYPE'] == 'raindrop':
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
								img = pygame.Surface((p['RADIUS'],p['RADIUS']))
								img.fill((0, 148, 255))
								img.set_alpha(120)
								self.display[0].blit(img, (p['X'],p['Y']))
								if p['TIME'] == 0:
									p['X'] = p['X'] + self.cam.x
									p['Y'] = p['Y'] + self.cam.y
							elif p['GIF'] <= 8:
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'raindrop_' + str(p['GIF']) + '.png'), (p['X'] - self.cam.x + 4,p['Y'] -self.cam.y + 6))
								p['GIF'] += 1
			#HIDE PLACES
			if self.tilhide == False and self.tilalpha > 0: self.tilalpha -= 20
			if self.tilhide == True and self.tilalpha < 255: self.tilalpha += 20
			if self.tilalpha < 0: self.tilalpha = 0
			if self.tilalpha > 255: self.tilalpha = 255
			al = 255 - self.tilalpha
			for i in self.tilrect[4]:
				srf = pygame.Surface((i[1].width,i[1].height))
				if i[0].endswith('ON'): srf.set_alpha(al); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
				if i[0].endswith('OFF'): srf.set_alpha(self.tilalpha); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
			#MINI MAP
			if res.MINIMAP == True:
				try:
					xx = 100 + ((200/self.phn.mp.get_height()) * self.player[0]['RECT'].x * self.phn.mp.get_width()/(self.map.width * self.map.tilewidth))
					yy = 100 + ((200/self.phn.mp.get_height()) * self.player[0]['RECT'].y * self.phn.mp.get_height()/(self.map.height * self.map.tileheight))
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - (106 * int(self.displayzh/400)),106 * int(self.displayzw/600),106 * int(self.displayzh/400)))
					self.display[0].blit(self.phn.map(True, self.map, self.tilrect, self.player[0], self.en, self.signs), (3 * int(self.displayzh/400),self.displayzh - (103 * int(self.displayzh/400))))
				except: pass
			#MAP COMPASS
			if len(res.MARKER) > 0:
				xx = (self.player[0]['RECT'].x - self.cam.x) - (res.MARKER[0][1] - self.cam.x)
				yy = (self.player[0]['RECT'].y - self.cam.y) - (res.MARKER[0][2] - self.cam.y)
				dir = (xx,yy)
				lth = math.hypot(*dir)
				if lth == 0.0: dir = (0, -1)
				else: dir = (dir[0]/lth,dir[1]/lth)
				img = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'mp_compass.png'),(math.degrees((math.atan2(-dir[1],dir[0]))) + 90))
				try:
					self.mpcrct = img.get_rect(center = self.mpcrct.center)
				except:
					self.mpcrct = img.get_rect(center=pygame.Rect(self.displayzw - 70,20,50,50).center)
				self.display[0].blit(img,self.mpcrct)
				if self.colide(self.player[0]['RECT'],pygame.Rect(res.MARKER[0][1] - 40,res.MARKER[0][2] - 40,80,80)):
					del res.MARKER[0]
			#DRIVING BARS
			if self.driving > 0:
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,20,100,20))
				if res.GAS >= 1: pygame.draw.rect(self.display[0], (255,155,66), pygame.Rect(20,20,int(100/(self.vehicles[self.driving - 1]['CAPACITY']/round(res.GAS))),20))
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(20,42,100,20))
				if self.player[0]['SPEED'] > 0: pygame.draw.rect(self.display[0], (0,255,0), pygame.Rect(20,42,int(100/(20/self.player[0]['SPEED'])),20))
				self.hpctrl = dtb.HINTS['VEHICLE_CONTROLS']
			#BLACK BARS
			if self.winbar > 0:
				#MYSTERIOUS FREAK
				if self.turn == -6:
					if self.winbar < 175:
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
					else:
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,175))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - 165,self.displayzw,165))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,175,-(self.displayzw - 190) + (self.winbar * 3),60))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(280,0,(self.displayzw - 280),self.winbar))
						pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(280,self.displayzh,(self.displayzw - 280) - self.winbar,self.winbar))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'aim_mysterious.png'), (-(self.displayzw - 190) + (self.winbar * 3), 175))
						sz = self.fnt['MININFO'].size(self.cityname)[0] + 20
						self.display[0].blit(self.fnt['MININFO'].render(self.cityname, True, (250,250,250)), ((self.displayzw - sz), 200))
				#REGULAR BARS
				else:
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
					pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
			#RADIOPLAY
			if self.rad.onoff == True and self.turn != -6:
				rdsrf = pygame.Surface((360,50))
				rdsrf.fill((255, 0, 135))
				if self.rad.msc < 0:
					ttsz = math.floor(self.fnt['DEFAULT'].size('?????')[0]/2)
					rdsrf.blit(self.fnt['DEFAULT'].render('?????', True, (0, 0, 0)), (-self.rdscroll * 2, 5 * 2))
				else:
					if res.DISLEXIC == True:
						out = ''
						for t in res.RADIO[str(math.floor(self.rad.fm/20))][self.rad.msc][:-4]:
							out += t + ' '
					else: out = res.RADIO[str(math.floor(self.rad.fm/20))][self.rad.msc][:-4]
					ttsz = math.floor(self.fnt['DEFAULT'].size(out)[0]/2)
					rdsrf.blit(self.fnt['DEFAULT'].render(out, True, (0, 0, 0)), (-self.rdscroll * 2, 5 * 2))
				self.display[1].blit(rdsrf, (0,0))
				self.rdscroll += 1
				if self.rdscroll > ttsz:
					self.rdscroll = -180
				
				if pygame.mixer.music.get_busy() == False and self.rad.msc > -2:
					self.rad.msc += 1
					if self.rad.msc >= len(res.RADIO[str(round(self.rad.fm/20))]): self.rad.msc = 0
					if res.RADIO[str(round(self.rad.fm/20))] != []:
						self.song = res.SONGS_PATH + str(math.floor(self.rad.fm/20)) + '/' + res.RADIO[str(math.floor(self.rad.fm/20))][self.rad.msc]
						pygame.mixer.music.load(self.song)
						pygame.mixer.music.play()
			#CITY NAME
			if self.cityname != '' and self.winbar >= 50 and self.turn != -6:
				self.display[0].blit(self.fnt['MONOTYPE'].render(self.cityname, True, (250,250,250)), (420, 360))
			#PORTALGO
			if self.portalgo != {}:
				if self.rectdebug == True: pygame.draw.rect(self.display[0], (255,0,0), pygame.Rect(self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y, self.portalgo[0]['RECT'].width, self.portalgo[0]['RECT'].height))
				if self.portalgo[0]['RECT'].width == 24: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_01.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				if self.portalgo[0]['RECT'].width == 48: self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_11.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				self.portalgo[1]['RECT'].x = self.portalgo[0]['RECT'].x + self.cam.x
				self.portalgo[1]['RECT'].y = self.portalgo[0]['RECT'].y + self.cam.y + 20
				self.people(self.portalgo[1],True)
				for i in self.portals:
					if self.portalgo[0]['MATCH'] != None and i['MATCH'] == self.portalgo[0]['MATCH']:
						self.cam.x += int((i['RECT'].x  - self.cam.x - self.displayzw/2)/15)
						self.cam.y += int((i['RECT'].y  - self.cam.y - self.displayzh/2)/15)
						chk = 0
						if i['RECT'].x - self.cam.x < self.portalgo[0]['RECT'].x:
							self.portalgo[0]['RECT'].x -= 10
							if i['RECT'].x - self.cam.x >= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif i['RECT'].x - self.cam.x > self.portalgo[0]['RECT'].x and chk == 0:
							self.portalgo[0]['RECT'].x += 10
							if i['RECT'].x - self.cam.x <= self.portalgo[0]['RECT'].x and chk == 0: chk += 1
						elif chk == 0: chk += 1
						if i['RECT'].y - self.cam.y < self.portalgo[0]['RECT'].y:
							self.portalgo[0]['RECT'].y -= 10
							if i['RECT'].y - self.cam.y >= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif i['RECT'].y - self.cam.y > self.portalgo[0]['RECT'].y and chk != 2:
							self.portalgo[0]['RECT'].y += 10
							if i['RECT'].y - self.cam.y <= self.portalgo[0]['RECT'].y and chk == 1: chk += 1
						elif chk == 1: chk += 1

						if chk == 2: self.portalgo[0]['MATCH'] = None
						#if self.colide(self.portalgo['RECT'],i['RECT']):
						#	self.portalgo['MATCH'] = None
		#HEALTH DAMAGE
		u = 0
		for i in res.PARTY[res.FORMATION]:
			if res.CHARACTERS[i]['HEALTH'] in [4,5,6,7,16,17,18,19,20,21] and self.dlgfa > 0:
				self.player[u]['DMGTIM'] -= 1
				if self.player[u]['DMGTIM'] == 0:
					self.player[u]['DMGTIM'] = 100
					self.player[u]['SHK'] = 3
					res.CHARACTERS[i]['HP'] -= 1
					if res.CHARACTERS[i]['HEALTH'] == 17:
						chc = round(random.randint(0,100))
						if chc > 70: res.CHARACTERS[i]['HEALTH'] = 0
					'''dth = 0
					for d in self.fig:
						if d['HP'] <= 0: dth += 1
					if dth == len(self.fig):'''
					if res.CHARACTERS[i]['HP'] <= 0:
						res.CHARACTERS[i]['HEALTH'] = 0
						if self.rad.onoff == True: pygame.mixer.music.unpause(); self.rad.onoff = False
						self.ch_msc.fadeout(500)
						self.ch_ton.play(res.SOUND['BATTLE_LOST'])
						self.transiction(True, int(self.displayzh/2))
						self.battle = True
						self.turn = -5
						self.mnu = 600
						acc = 60
						while self.mnu > 0:
							self.mnu -= acc
							acc -= 2
							self.run()
						self.turn = -5
						self.wait()
						res.load_data()
						res.PX = 315
						res.PY = 200
						src = None
						for i in res.PARTY[res.FORMATION]:
							src = self.inv.find(i,'credit_card')
							if src == None:
								src = self.inv.find(i,'wallet')
								if src != None:
									src[1] = str(int(scr[1][6:]) - 100) + scr[1][6:]
							else:
								src[1] = str(int(scr[1]) - 100)
						for w in res.PARTY[res.FORMATION]:
							res.CHARACTERS[w]['HP'] = res.CHARACTERS[w]['RESISTANCE'][res.CHARACTERS[w]['LEVEL']]
							res.CHARACTERS[w]['HEALTH'] = 0
						self.__init__()
						self.rendermap('hospital_1')
						self.transiction(False, 0)

					self.ch_ton.play(res.SOUND['DAMAGE_1'])
				if self.player[u]['SHK'] > 0: self.player[u]['SHK'] = -self.player[u]['SHK']
				elif self.player[u]['SHK'] < 0: self.player[u]['SHK'] = -self.player[u]['SHK'] - 1
			u += 1
		#BATTLE
		if self.battle == True:
			#BACKGROUND
			if self.turn == -4:
				self.display[0].blit(self.bbg, (self.bbm, 0))
				self.display[0].blit(self.bbg, (self.bbm - 600, 0))
				if self.displayzw > 600:
					self.display[0].blit(self.bbg, (self.bbm + 600, 0))
				self.bbm += 5
				if self.bbm > 600: self.bbm = 0
			elif self.bbg != '':
				self.display[0].blit(self.bbg, (int(self.bbm * 0.5), 0))
				if self.displayzw > 595:
					self.display[0].blit(self.bbg, (int(self.bbm * 0.5) + 600, 0))
				if self.obstacles == True:
					self.display[0].blit(self.bbg, (int(self.bbm * 0.5) - 600, 0))
					self.bbm += 5
					if self.bbm > 600: self.bbm = 0
					self.bba = 0
				else:
					if self.bbd == True:
						self.bba += 0.05
						if self.bba > 1:
							self.bbd = False
					elif self.bbd == False:
						self.bba -= 0.05
						if self.bba < -1:
							self.bbd = True
					self.bbm += self.bba
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
				if i['FADE'] > 0 and i['HEALTH'] != 9:
					i['FIGHTING'] = True
					if i['MASK'].x < 600:
						#MOVE
						if self.mnu == 2 and self.equip[self.turn] < 4 and i['HEALTH'] != 1:
							if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
							if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']

							if i['MASK'].x < int(self.displayzw/6): i['DIRECTION'] = 1
							if i['MASK'].x > (self.displayzw - int(self.displayzw/6)): i['DIRECTION'] = 5
						if i['FADE'] < 10: i['SPRITE'].blit(pygame.image.load(res.SPRITES_PATH + 'eff_death_' + str(i['FADE']) + '.png'), (0,0), special_flags=pygame.BLEND_SUB)
						
						#NORMAL SPRITE
						if i['AWAY'] == 0:
							self.display[0].blit(i['SPRITE'], (i['MASK'].x + int(self.bbm * 1.5), i['MASK'].y))
						#GO AWAY
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
							self.display[0].blit(res.SPRITES['EFFECT_' + str(i['HEALTH'])][math.floor(i['EFFECT'])], (i['MASK'].x + 5 + math.floor(self.bbm/3), i['MASK'].y - 10))
							i['EFFECT'] += 0.5
							if i['EFFECT'] >= len(res.SPRITES['EFFECT_' + str(i['HEALTH'])]): i['EFFECT'] = 0.0
						count += 1
					else: i['MASK'].x -= i['AGILITY']
			#SKIP PLAYER & BLINDNESS
			if self.mnu < 3 and self.turn >= 0 and self.turn < len(self.fig):
				if self.fig[self.turn]['HEALTH'] == 12: self.display[0].fill((0,0,0))
				if self.fig[self.turn]['HP'] <= 0: self.turn += 1
				elif self.fig[self.turn]['HEALTH'] in [8,13,14,15]: self.turn += 1
				if self.turn >= len(self.fig): self.fight()
			#BLACK BARS
			if self.windoww > self.windowh: wbrh = self.winbar
			else: wbrh = self.winbar * 2
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
			pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - wbrh,self.displayzw,wbrh))
			#ENEMIES COUNT
			if self.winbar <= 100 and self.turn != -4:
				ce = 0
				if len(self.mrc) == 0:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (500, -70 + self.winbar))
				else:
					for i in self.foe:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (500, -85 + self.winbar))
					ce = 0
					for i in self.mrc:
						if i['HP'] > 0: ce += 1
					self.display[0].blit(self.fnt['MININFO'].render(str(ce) + '/' + str(len(self.mrc)), True, (255,255,255)), (500, -50 + self.winbar))
				#PLAYER BARS
				p = 0
				low = False
				while p < len(res.PARTY[res.FORMATION]):
					#NAME
					ctr = res.PARTY[res.FORMATION][p]
					if p == self.turn:
						pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(p * 120, self.winbar - 100,120,100))
						self.display[0].blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, (0,0,0)), (10 + p * 120, -90 + self.winbar))
					else: 
						self.display[0].blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, (res.COLOR[0],res.COLOR[1],res.COLOR[2])), (10 + p * 120, -90 + self.winbar))
					#VITALITY GRAY
					pygame.draw.rect(self.display[0], (10, 10, 10), pygame.Rect(10 + p * 120, -60 + self.winbar,100,20))
					if res.CHARACTERS[ctr]['HP'] > 0:
						minush = int(98/(dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]/res.CHARACTERS[ctr]['HP']))
					else: minush = 0
					if self.barhp[p] > minush:
						self.ch_sfx.play(res.SOUND['HP_LOSS'])
						self.barhp[p] -= 1
					pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(11 + p * 120, -59 + self.winbar,98,18))
					if low == True:
						if self.ch_ton.get_busy() == False: self.ch_ton.play(res.SOUND['HP_LOW'])
					if self.barhp[p] > 0: pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(11 + p * 120, -59 + self.winbar,self.barhp[p],18))
					#LIFE BAR
					if self.equip[p] == 6 and self.turn > p: hpcol = (100, 100, 100)
					elif res.CHARACTERS[ctr]['HP'] > dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]/5: hpcol = (0, 255, 0)
					elif res.CHARACTERS[ctr]['HP'] > 0:
						hpcol = (255, 0, 0)
						low = True
					else: hpcol = (255, 0, 0)
					if res.CHARACTERS[ctr]['HP'] > 0:
						pygame.draw.rect(self.display[0], hpcol, pygame.Rect(11 + p * 120, -59 + self.winbar,int(98/(dtb.CLASSES[res.CHARACTERS[ctr]['CLASS']]['RESISTANCE'][res.CHARACTERS[ctr]['LEVEL']]/res.CHARACTERS[ctr]['HP'])),18))
					#CONDITION ICON
					if res.CHARACTERS[ctr]['HEALTH'] > 1:
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[ctr]['HEALTH']) + '.png'), (14 + p * 120, -56 + self.winbar))
					#AMMO BAR
					if self.equip[p] < 4:
						if int(res.INVENTORY[ctr][4][self.equip[p] + 1][1]) > 0:
							try: minush = int(98/(dtb.ITEMS[res.INVENTORY[ctr][4][self.equip[p] + 1][0]][5]['CAPACITY']/int(res.INVENTORY[ctr][4][self.equip[p] + 1][1])))
							except: minush = 0
						else: minush = 0
						if self.barpp[p][self.equip[p]] > minush:
							self.barpp[p][self.equip[p]] -= 1
						pygame.draw.rect(self.display[0], (10, 10, 10), pygame.Rect(10 + p * 120, -30 + self.winbar,100,20))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(11 + p * 120, -29 + self.winbar,98,18))
						if self.barpp[p][self.equip[p]] > 0:
							pygame.draw.rect(self.display[0], (0, 100, 255), pygame.Rect(11 + p * 120, -29 + self.winbar,self.barpp[p][self.equip[p]],18))
					p += 1
				if self.turn < len(res.PARTY[res.FORMATION]) and self.turn >= 0:
					#TIME BAR:
					if self.btime > 0:
						pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,self.displayzh - wbrh,int(self.displayzw/(100/self.btime)),10))
					if ce > 0 and self.mnu < 3 and self.turn < len(self.fig): self.btime -= 0.5
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
						for i in res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][1:]:
							if self.equip[self.turn] == x: pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + (x * 35),(self.displayzh + 38) - wbrh,32,32))
							else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(brdx + (x * 35),(self.displayzh + 38) - wbrh,32,32))
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(brdx + 2 + (x * 35),(self.displayzh + 40) - wbrh,28,28))
							if res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][x + 1][0] != '_':
								self.display[0].blit(pygame.image.load(res.ITEMS_PATH + res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][x + 1][0] + '.png'), (brdx + 2 + (x * 35), (self.displayzh + 40) - wbrh))
							x += 1
						if wbrh == self.winbar * 2: wbrh -= 35
						if self.displayzw < self.displayzh: brdx -= (35 * 4) + 46
						if self.equip[self.turn] == 4:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 186,(self.displayzh + 38) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_TACTICS']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 186,(self.displayzh + 38) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_tactical.png'), (brdx + 186, (self.displayzh + 38) - wbrh))
						if self.equip[self.turn] == 5:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 221,(self.displayzh + 38) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_DIALOG']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 221,(self.displayzh + 38) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_talk.png'), (brdx + 221, (self.displayzh + 38) - wbrh))
						if self.equip[self.turn] == 6:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 256,(self.displayzh + 38) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_GUARD']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 256,(self.displayzh + 38) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_guard.png'), (brdx + 256, (self.displayzh + 38) - wbrh))
						if self.equip[self.turn] == 7:
							pygame.draw.rect(self.display[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(brdx + 291,(self.displayzh + 38) - wbrh,30,30))
							self.hpctrl = dtb.HINTS['BATTLE_RUN']
						else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(brdx + 291,(self.displayzh + 38) - wbrh,30,30))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_run.png'), (brdx + 291, (self.displayzh + 38) - wbrh))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_invphn.png'), (brdx + 324, (self.displayzh + 38) - wbrh))
					#AIM BAR
					elif self.mnu == 2:
						if self.equip[self.turn] < 4:
							if res.CHARACTERS[res.PARTY[res.FORMATION][self.turn]]['HEALTH'] == 9:
								prb = random.randint(0,10)
								if prb > 5: self.aim.x += round(random.randint(30,60))
								if prb < 5: self.aim.x -= round(random.randint(30,60))
							else: self.aim.x += 20 - self.pagi[self.turn]
							if self.aim.x > (self.displayzw - int(self.displayzw/6)):
								self.aim.x = int(self.displayzw/6)
							chk = False
							for i in res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][1:]:
								if isinstance(i,str) and i.startswith('aim') == True: chk = True; break
							if chk == True:
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'aim_' + str(dtb.ITEMS[i][5]) + '.png'), (self.aim.x - 15, self.aim.y))
							else:
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'aim_0.png'), (self.aim.x-15, self.aim.y))
							#self.display[0].blit(pygame.image.load(res.SPRITES_PATH + '' + res.INVENTORY[res.PARTY[res.FORMATION][self.turn]][4][self.equip[self.turn] + 1][0] + '.png'), (150 + int(self.aim.x/2), 255))
							self.hpctrl = dtb.HINTS['BATTLE_SHOT']
						#TACTICS
						elif self.equip[self.turn] == 4:
							x = 0
							for i in res.TACTICAL:
								if self.opt == x: pygame.draw.rect(self.display[0], (255, 0, 0), pygame.Rect(118 + x * 35,338,32,32))
								else: pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect(118 + x * 35,338,32,32))
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(120 + x * 35,340,28,28))
								x += 1
			#PARTICLES
			if len(self.particles) > 0:
				for p in range(len(self.particles)):
					if self.particles[p]['TYPE'] == 'blood' and self.particles[p]['RADIUS'] <= 0.0:
						del self.particles[p]; break
				for p in self.particles:
					if p['TYPE'] == 'blood':
						p['X'] += int(math.cos(p['DIRECTION']) * p['SPEED'])
						p['Y'] += int(math.sin(p['DIRECTION']) * p['SPEED'])
						pygame.draw.circle(self.display[0], p['COLOR'], (p['X'],p['Y']), math.ceil(p['RADIUS']))
						p['RADIUS'] -= 0.25
						if p['RADIUS'] < 0.0: p['RADIUS'] = 0.0
			#INFOHIT
			if self.dmginfo != '':
				self.display[0].blit(self.dmginfo, (self.aim.x, self.dmgy))
			#ATTACKIMATION
			if self.effttack != None:
				srf = pygame.Surface((self.displayzw,self.displayzh))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.display[0].blit(srf, (0,0))
				img = res.SPRITES['ATTACKIMATION_' + str(self.effttack)][math.floor(self.effgif)]
				sz = img.get_rect()
				self.display[0].blit(img, (int(self.displayzw/2) - int(sz.width/2),int(self.displayzh/2) - int(sz.height/2)))
			#DICES
			if self.dices != []:
				y = 0
				for i in self.dices:
					pygame.draw.rect(self.display[0],(10,10,10),pygame.Rect(int(self.displayzw/2) - 30,(y * 80) + int(self.displayzh/2) - 30,60,60))
					self.display[1].blit(self.fnt['DEFAULT'].render(i,True,(200,200,200)),(int(self.windoww/2) - 60,(y * 160) + int(self.windowh/2) - 60))
					y += 1
			#GRADIENT
			for i in range(len(self.grd)):
				self.display[1].blit(self.grd[i],(0,i))
				self.display[1].blit(self.grd[i],(0,self.windowh - i))
			#WIN SCREEN
			if self.winbar >= 100:
				if self.turn == -4:
					#LABEL
					if self.hpl < 0: self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[6], True, (255,255,255)), (130 + self.mnu, 70))
					else: self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[7], True, (255,255,255)), (130 + self.mnu, 70))
					#GREENBLOOD
					btls = None
					for i in res.PARTY[res.FORMATION]:
						for it in ['bottle100','bottle250']:
							btls = self.inv.find(i,it)
							if btls != None and int(btls[1]) < dtb.ITEMS[btls[0]][5]: break
						if btls != None and int(btls[1]) < dtb.ITEMS[btls[0]][5]: break
					if btls != None:
						if int(btls[1]) > 0 and int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1]))) >= 1:
							pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect((self.displayzw - 140) + self.mnu,300 - int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1]))),30,int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1])))))
							if int(btls[1]) < 90:
								pygame.draw.ellipse(self.display[0], (32, 219, 166), pygame.Rect((self.displayzw - 140) + self.mnu,291 - int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1]))),30,13))
							pygame.draw.rect(self.display[0], (255, 255, 255), pygame.Rect((self.displayzw - 100) + self.mnu,280 - int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1]))),50,20))
							self.display[1].blit(self.fnt['DEFAULT'].render(str(btls[1]) + 'ml', True, (0,0,0)), (((self.displayzw - 95) + self.mnu) * 2, (285 - int(200/(dtb.ITEMS[btls[0]][5]/int(btls[1])))) * 2))
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'gbbar.png'), ((self.displayzw - 140) + self.mnu, 100))
					#PARTY XP
					for i in range(len(res.PARTY[res.FORMATION])):
						if self.mnu > 0: mvx = self.mnu
						else: mvx = 0
						self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][i]) + '.png'), (100 + mvx, 120 + i * 30))
						pygame.draw.rect(self.display[0], (50, 50, 50), pygame.Rect(130 + mvx,120 + i * 30,100,20))
						if self.barxp[i] > 0: pygame.draw.rect(self.display[0], (0, 255, 100), pygame.Rect(130 + mvx,120 + i * 30,self.barxp[i],20))
					#LEVEL UP
					bw = (self.displayzw * 2) - 100
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
						self.display[1].blit(self.fnt['DEFAULT'].render(str(n), True, (240,240,240)), ((bw + 115 + self.mnu) * 2, 295))
						
						if self.mnu <= 0:
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,0,self.displayzw,self.winbar))
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(0,self.displayzh - self.winbar,self.displayzw,self.winbar))
						
						self.display[0].blit(self.fnt['MININFO'].render(ch['NAME'].lower(), True, (255,255,255)), (800 + self.mnu, 30))
						self.display[1].blit(self.fnt['DEFAULT'].render(dtb.BATTLE[14] + str(dtb.CNAMES[ch['CLASS']][ch['LEVEL'] - 1]) + ' !', True, (255,255,255)), ((800 + self.mnu) * 2, 140))
				#LOST SCREEN
				elif self.turn == -5:
					self.display[0].blit(self.fnt['MININFO'].render(dtb.BATTLE[8], True, (255,255,255)), (200 + self.mnu, 70))
					self.display[1].blit(self.fnt['DEFAULT'].render('-$100', True, (255,255,255)), ((200 + self.mnu) * 2, 240))
		#INVENTORY
		if self.invfade < self.displayzw + 400:
			if self.inventory == 2: t = 1
			else: t = 0
			isrf = self.inv.show(self.opt, self.lopt, self.mnu, self.exvar, t)
			hh = int(self.displayzh/2) - int(isrf[0].get_height()/2)
			shd = pygame.Surface((isrf[0].get_width(),isrf[0].get_height()))
			shd.set_alpha(100)
			shd.fill((10,10,10))
			self.display[0].blit(shd,((self.displayzw + 20) - self.invfade,hh + 10))
			self.display[0].blit(isrf[0], ((self.displayzw + 10) - self.invfade,hh))
			self.display[1].blit(isrf[1], (((self.displayzw + 20) - self.invfade) * 2,(hh + 10) * 2))
		if self.inventory > 0:
			if self.inv.itmov == '': self.hpctrl = dtb.HINTS['INVENTORY_ITEMS']
			elif self.inv.itmov[0] != 0: self.hpctrl = dtb.HINTS['INVENTORY_HOLD']
			else: self.hpctrl = dtb.HINTS['INVENTORY_ACCESORIES']
			if self.invfade < int(self.displayzw/2) + 200: self.invfade += 50
		else:
			if self.invfade < self.displayzw + 400: self.invfade += 50
		#SHOP
		if self.shp == True:
			if self.mnu == 0:
				self.display[0].blit(self.shpmnu.products(self.opt, self.lopt, self.products), (100,60))
			if self.mnu == 1:
				self.display[0].blit(self.shpmnu.buy(self.opt, self.lopt, self.basket), (100,60))
			if self.mnu == 2:
				lst = []
				if self.opt == 0: lst = self.products
				else: lst = self.basket[self.opt - 1]
				ssrf = self.shpmnu.mercator(self.opt, self.lopt, lst, self.promo)
				self.display[0].blit(ssrf[0], (100,60))
				self.display[1].blit(ssrf[1], (220,140))
			if self.mnu == 3 or self.mnu == 11 or self.mnu == 12:
				self.display[0].blit(self.shpmnu.bank(self.opt, self.lopt, self.mnu, self.extract), (100,60))
		#PHONE
		pps = math.floor(self.displayzw/2) - math.floor(self.dev.scr[1].get_width()/4)
		if self.phofa > 0:
			if self.battle == False: pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(pps,self.displayzh + 30 - self.phofa,math.floor(self.dev.scr[1].get_width()/2),250))
			self.display[0].blit(pygame.image.load(res.BACKG_PATH + 'phone.png'), (pps - 10, self.displayzh - self.phofa))
		if self.phone > 0:
			if self.phofa == 320: self.ch_sfx.play(res.SOUND['PHONE_UNLOCK'])
			if self.phofa < 360: self.phofa += 40
		else:
			if self.phofa == 360: self.ch_sfx.play(res.SOUND['PHONE_LOCK'])
			if self.phofa > 0: self.phofa -= 40
		if self.phofa == 360 and self.dev.battery > 0:
			bsrf = self.pbr.draw()
			hh = self.displayzh - self.phofa + 30
			self.display[0].blit(bsrf[0], (pps,hh))
			self.display[1].blit(bsrf[1], (pps * 2,hh * 2))
			if self.battle == False:
				srf = self.dev.draw()
				self.hpctrl = dtb.HINTS[self.dev.hpctrl]
			else:
				srf = GUI.Photo(self.bbg, self.foe, pps).draw()
				self.hpctrl = dtb.HINTS[self.dev.hpctrl]
			hh = self.displayzh - self.phofa + 48
			self.display[0].blit(srf[0], (pps,hh))
			self.display[1].blit(srf[1], (pps * 2,hh * 2))
		elif self.phofa == 360:
			self.display[0].blit(pygame.image.load(res.BACKG_PATH + 'battery_low.png'), (pps + 60, 510 - self.phofa))
			if self.battle == True: pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(pps,(self.displayzh + 30) - self.phofa,180,250))
		#READING
		if self.read != None:
			srf = self.read.draw()
			self.display[0].blit(srf[0], (200, 100))
			self.display[1].blit(srf[1], (420, 220))
		#NAMING
		if self.nmenu.show == True:
			self.display[0].blit(self.nmenu.run()[0], (200, 100))
			self.display[1].blit(self.nmenu.run()[1], (420, 220))
			if self.nmenu.ninput == True: self.hpctrl = dtb.HINTS['NAMING']
		#DIALOG
		if self.dlgfa < 500 and res.SCENE != -1 and self.nmenu.show == False:
			if self.dlg != []:
				self.dlgy = 0
				sd = False
				opt = 1
				ind = 0
				for i in self.dlg:
					if i == 0: sd = not sd
				for i in self.dlg[::-1]:
					if isinstance(i,str):
						txt = self.fnt['DEFAULT'].render(i, True, (255, 255, 255))
						txtsz = math.floor(self.fnt['DEFAULT'].size(i)[0]/2) + 10
					if i != 1 and i != 0 and len(i) != 0:
						if sd == False:
							pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect(20,(self.displayzh - 200) - self.dlgy,5 + txtsz,25))
							pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(20,(self.displayzh - 175) - self.dlgy,5 + txtsz,5))
							pygame.draw.polygon(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), ((25,(self.displayzh - 175) - self.dlgy),(45,(self.displayzh - 175) - self.dlgy),(25,(self.displayzh - 165) - self.dlgy)))
							pygame.draw.polygon(self.display[0], (0, 0, 0), ((25,(self.displayzh - 179) - self.dlgy),(45,(self.displayzh - 179) - self.dlgy),(25,(self.displayzh - 169) - self.dlgy)))
						else:
							if self.lopt == opt:
								pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect((self.displayzw - 22) - txtsz,(self.displayzh - 200) - self.dlgy,5 + txtsz,25))
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect((self.displayzw - 22) - txtsz,(self.displayzh - 175) - self.dlgy,5 + txtsz,5))
								pygame.draw.polygon(self.display[0], (0, 0, 0), (((self.displayzw - 42),(self.displayzh - 175) - self.dlgy),((self.displayzw - 22),(self.displayzh - 175) - self.dlgy),((self.displayzw - 22),(self.displayzh - 165) - self.dlgy)))
								pygame.draw.polygon(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), (((self.displayzw - 42),(self.displayzh - 179) - self.dlgy),((self.displayzw - 22),(self.displayzh - 179) - self.dlgy),((self.displayzw - 22),(self.displayzh - 169) - self.dlgy)))
							else:
								pygame.draw.rect(self.display[0], (0, 0, 0), pygame.Rect((self.displayzw - 22) - txtsz,(self.displayzh - 200) - self.dlgy,5 + txtsz,25))
								pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect((self.displayzw - 22) - txtsz,(self.displayzh - 175) - self.dlgy,5 + txtsz,5))
								pygame.draw.polygon(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), (((self.displayzw - 42),(self.displayzh - 175) - self.dlgy),((self.displayzw - 22),(self.displayzh - 175) - self.dlgy),((self.displayzw - 22),(self.displayzh - 165) - self.dlgy)))
								pygame.draw.polygon(self.display[0], (0, 0, 0), (((self.displayzw - 42),(self.displayzh - 179) - self.dlgy),((self.displayzw - 22),(self.displayzh - 179) - self.dlgy),((self.displayzw - 22),(self.displayzh - 169) - self.dlgy)))
							opt += 1
					if i == 0:
						if sd == False: sd = True
						elif sd == True: sd = False
					elif isinstance(i, str):
						if sd == False: self.display[1].blit(txt, (30 * 2, ((self.displayzh - 193) - self.dlgy) * 2))
						else: self.display[1].blit(txt, (((self.displayzw - 12) - txtsz) * 2, ((self.displayzh - 193) - self.dlgy) * 2))
						self.dlgy += 40
					ind += 1
		#EASTER EGG
		if self.cityname == 'TWNN': self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'TWNN.png'), (35,0))
		#NOTIFICATIONS
		if self.notx > 0:
			ch = res.CHARACTERS[res.PARTY[res.FORMATION][0]]
			#HP BAR
			if self.nottxt.startswith('hp_'):
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(-170 + self.notx,40,160,30))
				pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(-168 + self.notx,42,156,26))
				pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(-130 + self.notx,45,50,20))
				pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-130 + self.notx,45,int(50/(dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]/ch['HP'])),20))
				pygame.draw.rect(self.display[0], (0,255,0), pygame.Rect(-130 + self.notx,45,int(50/(dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]/ch['HP'] - int(self.nottxt[3:]))),20))
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (-160 + self.notx,45))
			#MORALITY BAR
			elif self.nottxt.startswith('ml_'):
				pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(-170 + self.notx,40,160,30))
				pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-168 + self.notx,42,156,26))
				if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] > 0:
					pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-90 + self.notx,45,int(70/(10/ch['MORALITY'])),20))
					pygame.draw.rect(self.display[0], (0,175,0), pygame.Rect(-90 + self.notx,45,int(70/(10/ch['MORALITY'] - int(self.nottxt[3:]))),20))
				if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] < 0:
					pygame.draw.rect(self.display[0], (255,255,0), pygame.Rect(-int(70/(10/ch['MORALITY'])) - 160 + self.notx,45,int(70/(10/ch['MORALITY'])),20))
					pygame.draw.rect(self.display[0], (175,0,0), pygame.Rect(-int(70/(10/ch['MORALITY'])) - 160 + self.notx,45,int(70/(10/ch['MORALITY'] - int(self.nottxt[3:]))),20))
				pygame.draw.line(self.display[0], (255,255,255), (-90 + self.notx,42),(-90 + self.notx,68),2)
			#ITEM
			elif self.nottxt.startswith('it_'):
				szw = math.floor(self.fnt['DEFAULT'].size(self.nottxt)[0]/2) + 70
				szh = math.floor(self.fnt['DEFAULT'].size(self.nottxt)[1]/2) + 45
				pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-183 + self.notx,27,szw,szh))
				pygame.draw.rect(self.display[0], self.notcol, pygame.Rect(-180 + self.notx,30,szw - 6,szh - 6))
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'Items/' + self.nottxt + '.png'), (-170 + self.notx, 40))
				self.display[1].blit(self.fnt['DEFAULT'].render(dtb.ITEMS[self.nottxt[3:]][0], True, (0, 0, 0)), ((-140 + self.notx) * 2, 50 * 2))
			#MESSAGE
			else:
				szw = math.floor(self.fnt['DEFAULT'].size(self.nottxt)[0]/2) + 30
				szh = math.floor(self.fnt['DEFAULT'].size(self.nottxt)[1]/2) + 45
				if self.notcol != (0,0,0): pygame.draw.rect(self.display[0], (0,0,0), pygame.Rect(-183 + self.notx,27,szw,szh))
				else: pygame.draw.rect(self.display[0], (255,255,255), pygame.Rect(-183 + self.notx,27,szw,szh))
				pygame.draw.rect(self.display[0], self.notcol, pygame.Rect(-180 + self.notx,30,szw - 6,szh - 6))
				self.display[1].blit(self.fnt['DEFAULT'].render(self.nottxt, True, (0, 0, 0)), ((-170 + self.notx) * 2, 45 * 2))
		#TUTORIALS
		if self.tutorial['OUTPUT'] != []:
			nxt = False
			if self.tutorial['GO'] > 0 and self.phone == self.tutorial['GO']: self.tutorial['TIME'] = self.tutorial['WAIT']; nxt = True

			if self.tutorial['TIME'] < self.tutorial['WAIT']:
				if self.tutorial['FADE'] < 200: self.tutorial['FADE'] += 20
			elif self.tutorial['TIME'] >= self.tutorial['WAIT']: nxt = True
			if nxt == True:
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
			srf = pygame.Surface((self.displayzw,self.displayzh))
			srf.set_alpha(200)
			srf.fill((221, 0, 0))
			self.display[0].blit(srf, (0,0))
			pygame.draw.rect(self.display[0], (250,250,250), pygame.Rect(0,160,600,80))
			self.display[0].blit(self.fnt['MININFO'].render(dtb.CHAPTERS[res.CHAPTER][0].lower(), True, (10, 10, 10)), (10, 200))
			pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,167,600,3))
			pygame.draw.rect(self.display[0], (10,10,10), pygame.Rect(0,170,600,22))
			pygame.draw.rect(self.display[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,192,600,3))
			self.display[1].blit(self.fnt['DEFAULT'].render(dtb.CHAPTERS[res.CHAPTER][1], True, (250, 250, 250)), (20, 350))
		#HELP CONTROLS
		if self.hpctrl != [] and res.MOUSE < 2:
			hpsz = 0
			for i in self.hpctrl[::-1]:
				if isinstance(i,str):
					hptxt = self.fnt['DEFAULT'].render(' ' + i + ' ', True, (250, 250, 250))
					hpsz += self.fnt['DEFAULT'].size(' ' + i + ' ')[0]
					self.display[1].blit(hptxt, (self.windoww - 40 - hpsz, self.windowh - 40))
				elif isinstance(i,int):
					ky = [res.UP[0],res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.RUN[0],res.BAG[0],res.PHONE[0]]
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
					self.display[0].blit(self.fnt['CONTROLKEYS'].render(out, True, (250, 250, 250)), (self.displayzw - 20 - math.floor(hpsz/2), self.displayzh - 20))
		#TOUCH BUTTONS
		for i in self.buttons:
			b = pygame.Rect(i.x - 3,i.y - 3,i.width + 6,i.height + 6)
			pygame.draw.rect(self.display[1],(10,10,10,100),b)
			pygame.draw.rect(self.display[1],(res.COLOR[0],res.COLOR[1],res.COLOR[2],100),i)
		#CAMERA X
		if (self.map.width * self.map.tilewidth) > self.displayzw:
			if self.portalgo == {}:
				#PLAYERS CAMERA
				if self.speakin == 0:
					camx = 0
					for i in self.player: camx += i['RECT'].x
					self.cam.x += int(((camx/len(self.player))  - self.cam.x - self.displayzw/2)/15)
				#DIALOG CAMERA
				else: self.cam.x += int((self.speakin.x  - self.cam.x - self.displayzw/2)/15)
			if self.cam.x < 0: self.cam.x = 0
			if self.cam.x > (self.map.width * self.map.tilewidth) - self.displayzw: self.cam.x = (self.map.width * self.map.tilewidth) - self.displayzw
		else: self.cam.x = -int((self.displayzw - (self.map.width * self.map.tilewidth))/2)
		#CAMERA Y
		if (self.map.height * self.map.tileheight) > self.displayzh:
			if self.portalgo == {}:
				#PLAYERS CAMERA
				if self.speakin == 0:
					camy = 0
					for i in self.player: camy += i['RECT'].y
					self.cam.y += int(((camy/len(self.player))  - self.cam.y - self.displayzh/2)/15)
				#DIALOG CAMERA
				else: self.cam.y += int((self.speakin.y  - self.cam.y - self.displayzh/2)/15)
			if self.cam.y < 0: self.cam.y = 0
			if self.cam.y > (self.map.height * self.map.tileheight) - self.displayzh: self.cam.y = (self.map.height * self.map.tileheight) - self.displayzh
		else: self.cam.y = -int((self.displayzh - (self.map.height * self.map.tileheight))/2)
		#UPDATE SCREEN & PAUSE SOUND
		if pygame.display.get_active():
			if self.ch_msc.get_busy() == False: self.ch_msc.unpause()
			if self.ch_rad.get_busy() == False: self.ch_rad.unpause()
			if self.ch_rng.get_busy() == False: self.ch_rng.unpause()
			#UPDATE SCREEN
			if self.scrmov == None:
				chk = False
				for i in res.INVENTORY[res.PARTY[res.FORMATION][0]]:
					if i[0][0].startswith('head_glasses'): chk = True; break
				if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['FLAW'] != 'myopia': chk = not chk
				if chk == False:
					srf = pygame.transform.scale(self.display[0], (self.windoww, self.windowh))
					srf.set_alpha(100)
					self.screen.blit(srf, (self.displayx - 20, self.displayy))
					self.screen.blit(srf, (self.displayx + 10, self.displayy))
					srf = pygame.transform.scale(self.display[1], (self.windoww, self.windowh))
					srf.set_alpha(100)
					self.screen.blit(srf, (self.displayx - 20, self.displayy))
					self.screen.blit(srf, (self.displayx + 10, self.displayy))
				else:
					self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy))
					self.screen.blit(pygame.transform.scale(self.display[1], (self.windoww, self.windowh)), (self.displayx, self.displayy))
			else:
				self.scrspd += 2
				self.scrmov += self.scrspd
				if self.scrmov > self.windowh: self.scrmov = 0
				self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy + self.scrmov - self.windowh - 20))
				self.screen.blit(pygame.transform.scale(self.display[0], (self.windoww, self.windowh)), (self.displayx, self.displayy + self.scrmov))
			#MOUSE
			if res.MOUSE == 1:
				self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'), pygame.mouse.get_pos())
			#FLIP
			pygame.display.flip()
		else:
			self.ch_msc.pause()
			self.ch_rad.pause()
			self.ch_rng.pause()

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
				self.FPS = int(event.w/20)
		self.screen.fill((0,0,0),pygame.Rect(self.windoww - 80, self.windowh - 80,30,30))
		if self.loadingif != None:
			self.loadingif += 0.01
			if str(self.loadingif)[2] == '0': upd = True
			else: upd = False
			if self.loadingif >= 8.0: self.loadingif = 0.0
		if upd == True:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'loading_' + str(math.floor(self.loadingif)) + '.png'), (self.windoww - 80, self.windowh - 80))
			pygame.display.update(pygame.Rect(self.windoww - 80,self.windowh - 80,30,30))

	def crash(self):
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
					self.FPS = int(event.w/20)
				#SKIP
				if event.type == pygame.KEYDOWN:
					self.__init__()
					again = True
			self.screen.fill((0,0,0))

			et, ev, eb = sys.exc_info()
			tlist = []
			for t in traceback.extract_tb(eb):
				tlist.append((t[0],t[1],t[2],t[3]))

			fnt = pygame.font.SysFont('Calibri', 22)
			self.screen.blit(fnt.render(str(et.__name__),True,(10,250,10)),(10,20))
			self.screen.blit(fnt.render(str(ev),True,(10,250,10)),(10,40))
			y = 60
			for j in tlist:
				self.screen.blit(fnt.render(str(j),True,(10,250,10)),(10,y))
				y += 20
			pygame.display.flip()

	def run(self):
		if self.FPS > 0: self.glock.tick(self.FPS)
		if self.nmenu.show == False:
			self.events()
		self.draw()
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
					if self.rad.onoff == True: pygame.mixer.music.pause()
					if self.phone > 0: self.phone = 17
					self.nb = i[0][3:]
					self.waitlst.append(['cutcal',self.waitime + 1200])
				#CUTTING CALL
				elif i[0].startswith('cutcal'):
					if self.nb != '':
						self.ch_ton.stop()
						self.ch_rng.stop()
						self.nb = ''
						if self.phone == 17: self.phone = 1
				#DELIVERY
				elif i[0] == 'delivery':
					if self.dlgfa > 0:
						self.dialog([(30,pygame.Rect(self.player[0]['RECT'].x - 430,self.player[0]['RECT'].y,0,0),i[2]['INDEX'],i[2]['WHO'],i[2]['TYPE']),
							(24,'n',(self.player[0]['RECT'].x - 30,self.player[0]['RECT'].y),3)])
				#RADIOEE
				elif i[0].startswith('radioee'):
					self.ch_ton.stop()
					pygame.mixer.music.load('Music/' + i[2] + '.mp3')
					pygame.mixer.music.play()
					self.rad.msc = -1
				#TIME WARNING
				elif i[0].startswith('advice'):
					if self.dlgfa > 0:
						self.dialog(dtb.DIALOGS['ADVICE'])
		#FOOD WASTE AND CLOTH DIRT
		u = 0
		for b in res.INVENTORY:
			for j in b:
				for i in j:
					if i[0].startswith('food') == True and i[0].endswith('wasted') == False:
						if int(i[1][2:4]) <= res.DATE[1]:
							if int(i[1][0:2]) <= res.DATE[0]:
								i[0] += '_wasted'
					elif i[0].startswith('drink') == True and i[0].endswith('wasted') == False:
						if int(i[1][2:4]) <= res.DATE[1]:
							if int(i[1][0:2]) <= res.DATE[0]:
								i[0] += '_wasted'
					elif i[0].startswith('clth') == True:
						if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
						if int(i[1]) == 0: res.CHARACTERS[u]['HEALTH'] = 3
			u += 1
		#SECONDS
		self.waitime += 1
		battery = self.inv.find(res.PARTY[res.FORMATION][0],'phone')
		#NORMAL
		if self.sleepin == False:
			res.TIME[2] += 1
			#BASIC NECESITIES
			for p in res.PARTY[res.FORMATION]:
				if res.CHARACTERS[p]['HUNGER'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 6
				else: res.CHARACTERS[p]['HUNGER'] -= 1
				if res.CHARACTERS[p]['THIRST'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 7
				else: res.CHARACTERS[p]['THIRST'] -= 1
				if res.CHARACTERS[p]['SLEEP'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 8
				else: res.CHARACTERS[p]['SLEEP'] -= 10 + res.CHARACTERS[p]['STAMINA']
			if self.phone > 0 and battery != None:
				if res.CHAPTER > 0: battery[1] = str(int(battery[1]) - 1)
				elif res.SCENE > 0: battery[1] = str(int(battery[1]) - 1)
		#SLEEP
		else:
			res.TIME[1] += 5
			for p in res.PARTY[res.FORMATION]:
				if res.CHARACTERS[p]['HP'] < dtb.CLASSES[res.CHARACTERS[p]['CLASS']]['RESISTANCE'][res.CHARACTERS[p]['LEVEL']]:
					res.CHARACTERS[p]['HP'] += 1
				if res.CHARACTERS[p]['SLEEP'] < 10000: res.CHARACTERS[p]['SLEEP'] += 50 + (res.CHARACTERS[p]['STAMINA'] * 10)
		#BATTERY
		if battery != None:
			self.dev.battery = int(battery[1])
			if int(battery[1]) < 0:
				if self.rad.onoff == True:
					self.rad.onoff = False
					self.ch_ton.stop()
					pygame.mixer.music.stop()
				battery[1] = '0'
		#MINUTES
		if res.TIME[2] >= 60:
			res.TIME[1] += 1
			res.TIME[2] = 0
		#HOURS
		if res.TIME[1] >= 60:
			res.TIME[0] += 1
			res.TIME[1] = 0
			if self.sleepin == True:
				for u in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[u]['HEALTH'] in (4,5,9,10,11):
						res.CHARACTERS[u]['HEALTH'] = 0
			#DAYTIME CHANGE
			if res.TIME[0] in [6,18]: self.rendermap(self.room)
		#DAYS
		if res.TIME[0] >= 24:
			res.DATE[0] += 1
			res.DATE[3] += 1
			res.TIME[0] = 0
			res.TEMPERATURE = dtb.CITIES[res.MAP - 1][1][res.DATE[1] - 1]
		#WEEKS
		if res.DATE[3] > 7:
			res.DATE[3] = 1
			res.DATE[4] += 1
		if res.DATE[4] > 8:
			res.DATE[4] = 1
		#MONTHS
		if res.DATE[1] in [1,3,5,7,8,10,12]:	
			if res.DATE[0] > 31:
				res.DATE[1] += 1
				res.DATE[0] = 1
		elif res.DATE[1] in [4,6,9,11]:	
			if res.DATE[0] > 30:
				res.DATE[1] += 1
				res.DATE[0] = 1
		elif res.DATE[1] == 2:	
			if res.DATE[0] > 28:
				res.DATE[1] += 1
				res.DATE[0] = 1
		#YEARS
		if res.DATE[1] > 12:
			res.DATE[2] += 1
			res.DATE[1] = 1
		#RADIOEE
		if self.rad.onoff == True:
			for i in dtb.RADIOEE:
				if int(i[2][0:2]) == res.TIME[0] and int(i[2][2:4]) == res.TIME[1]:
					if i[1] == None: ply = True
					elif int(i[1][0:2]) == res.DATE[0] and int(i[1][2:4]) == res.DATE[1]: ply = True
					else: ply = False
					if ply == True and self.rad.msc != -2:
						self.rad.msc = -2
						pygame.mixer.music.stop()
						self.ch_ton.play(res.SOUND['NOISE'],-1)
						self.waitlst.append(['radioee',self.waitime + 60,i[0]])
		#GAMETIME
		res.GAMETIME += self.glock.get_rawtime()

t = Title()
while True:
	while t.classrun == True: t.run()
	g = Game()
	if res.GAMETIME > 0: g.transiction(False, 0)
	while g.classrun == 1:
		try: g.run()
		except: g.crash()
	if g.classrun == 0: break
	if g.classrun == 2:
		pygame.mixer.stop()
		t.ton.play(res.SOUND['NOISE'],-1)
		t.classrun = True
		t.winbar = 50
		t.wait = 100
		t.mnu = 7
		t.tv = 0
