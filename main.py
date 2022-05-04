# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0,"C:/Users/kaixtr/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages")

import pygame
import xml.sax
import urllib
import plyer
import threading
import datetime
import platform
import numpy as np
import psutil

import tools
import resources as res
import minigames as mng
import GUI

if res.FILES != []: exec(f'import databases.database_{res.FILES[0][4]} as dtb')
else: exec(f'import databases.database_{res.MAINLANG} as dtb')

class Initialize:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()

		osinfo = platform.uname()
		print(res.GNAME.upper() + ' v.' + res.VERSION + ' - ' + res.AUTHOR + ' ' + res.YEAR)
		print(osinfo.system + ' ' + osinfo.machine + ' ' + osinfo.node + ' ' + osinfo.release + ' ' + osinfo.version)

		#DISPLAY
		pygame.display.set_caption(res.GNAME)
		pygame.display.set_icon(pygame.image.load(res.ICON))
		pygame.mouse.set_visible(False)
		self.glock = pygame.time.Clock()
		if osinfo.system == 'Windows':
			self.windoww = 800
			self.windowh = 600
			res.MOUSE = 1
			res.GSCALE = 2
		else:
			res.FULLSCREEN = True
			res.MOUSE = 2
			res.GSCALE = 2
		if res.FULLSCREEN:
			sz = pygame.display.Info()
			self.windoww = sz.current_w
			self.windowh = sz.current_h
			self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.FULLSCREEN)
		else: self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)

		#SPLASH SCREEN
		if res.SPLASH:
			img = pygame.image.load(res.SPLASH)
			self.screen.blit(img,(int(self.windoww/2) - int(img.get_width()/2),int(self.windowh/2) - int(img.get_height()/2)))
			pygame.display.update()

		if res.TTS: plyer.tts.speak('')
		if res.VIBRATE: plyer.vibrator.vibrate(0.01)
		self.srf = pygame.Surface((600,400),pygame.SRCALPHA)
		self.alpha = 0
		self.wait = 0
		self.mnu = 0
		self.lspd = 0

		#CHANNELS
		pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
		pygame.mixer.music = pygame.mixer.Channel(1)
		pygame.mixer.music.set_volume(res.MSC)
		for i in range(4):
			res.MIXER.append(pygame.mixer.Channel(i))
			res.MIXER[i].set_volume(res.SFX)
		
		self.bump = pygame.image.load(res.BACKG_PATH + 'bump_' + str(np.random.randint(0,res.RANGE_BUMP)) + '.png')
		
		self.holiday = datetime.datetime.now()
		
		self.sscroll = self.windoww + 20
		self.stext = dtb.TSECRETS[np.random.randint(0,len(dtb.TSECRETS) - 1)]
		self.stime = np.random.randint(600,1000)
		self.gmtim = []
		
		self.load = 0
		self.msg = 0
		self.tim = 1.0
		self.gif = 0
		self.stars = []
		
		self.fload = res.RANGE_RADIO + len(os.listdir(res.SFX_PATH[:-1])) + 3 + (13 * 2)
		#LOAD ASSETS
		th = [
			threading.Thread(target=res.spr,args=()),
			threading.Thread(target=res.battlesprites,args=()),
			threading.Thread(target=res.animals,args=()),
			threading.Thread(target=res.sfx,args=()),
			threading.Thread(target=res.fonts,args=()),
			threading.Thread(target=self.run,args=())
		]
		for i in th: i.start()
		for i in th: i.join()

		#LOAD PLUGINS
		for p in os.listdir('plugins'):
			pth = './plugins/' + p + '/'
			sprpth = res.SPRITES_PATH
			itpth = res.ITEMS_PATH
			sfxpth = res.SFX_PATH

			res.SPRITES_PATH = pth + 'sprites/'
			res.ITEMS_PATH = pth + 'sprites/items/it_'
			res.SFX_PATH = pth + 'sfx/'
			
			if res.FILES != []: pdtb = 'plugins.' + p + '.' + 'addons_' + res.MAINLANG 
			else: pdtb = 'plugins.' + p + '.' + 'addons_PT'
			exec(f'import {pdtb}')

			dtb.FREAKS = {**dtb.FREAKS,**eval(pdtb).FREAKS}
			dtb.ITEMS = {**dtb.ITEMS,**eval(pdtb).ITEMS}
			dtb.MENU = {**dtb.MENU,**eval(pdtb).MENU}

			th = [
				threading.Thread(target=res.sfx,args=()),
				threading.Thread(target=self.run,args=())
			]
			for i in th: i.start()
			for i in th: i.join()
			res.SPRITES_PATH = sprpth
			res.ITEMS_PATH = itpth
			res.SFX_PATH = sfxpth
		
		if res.GAMETIME > 0: self.msc.play(pygame.mixer.Sound(res.MUSIC_PATH + 'alchimera.mp3'))
		print('Boot time: ' + str(float(self.lspd/1000)) + 's')
		if res.QUICKSTART > 0: self.mnu = 2
		while self.mnu < 2: self.run()
	
	def intro(self):
		self.screen.fill((0,0,10))
		#STARS
		if len(self.stars) < 10000:
			'''self.stars.append([(np.random.randint((self.windoww/2) - 5,(self.windoww/2) + 5),
			np.random.randint((self.windowh/2) - 5,(self.windowh/2) + 5)),np.random.randint(1,9)])'''
			prb = np.random.randint(0,100)
			if prb > 50: self.stars.append([[self.windoww,np.random.randint(0,self.windowh)],np.random.randint(3,12)])
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
			sz = res.FONTS['DEFAULT'].size(dtb.CHAPTERS[0][2][self.msg])[0]
			self.screen.blit(res.FONTS['DEFAULT'].render(dtb.CHAPTERS[0][2][self.msg], True, (200,200,200)), (int(self.windoww/2) - int(sz/2),self.windowh - 50))
		#TIME
		self.wait -= 1
		if self.wait == 0:
			self.msg += 1
			if self.msg >= len(dtb.GINTRO):
				self.mnu = 4
			self.wait = 50
	
	def updates(self):
		f = open('README.md','r')
		print(f.readlines())
		f.close()

	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				res.fonts()
		
		self.screen.fill((0,0,0))
		if self.alpha < 255 and self.wait == 0: self.alpha += 5
		elif self.wait != 30: self.wait += 1
		elif self.alpha > 0 and self.wait == 30: self.alpha -= 10
		else: self.wait = 0; self.mnu += 1
		
		if self.mnu == 0: self.srf.blit(self.bump, (0, 0))
		if self.mnu == 1: self.srf.blit(pygame.image.load(res.BACKG_PATH + 'source.png'), (0, 0))
		self.srf.set_alpha(self.alpha)
		self.screen.blit(self.srf, (int(self.windoww/2) - 300,int(self.windowh/2) - 200))
		
		try: pygame.display.flip()
		except: self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.glock.tick(res.FPS)
		self.lspd += pygame.time.get_ticks()

class Avatar:
	def __init__(self,index,testing=False):
		self.index = index
		self.testing = testing
		if self.testing: self.window = pygame.display.set_mode((600, 600))
		else: self.window = pygame.Surface((600, 600))
		self.brd = pygame.Surface((200,150))
		for x in range(np.ceil(self.brd.get_width()/10).astype(int)):
			for y in range(np.ceil(self.brd.get_height()/10).astype(int)):
				self.brd.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))

		'''self.guis['INVENTORY'].gui = GUI.Inventory((0,0),0)
		self.player = {'HEAT': res.TEMPERATURE,'HEAD': 'D','SPRITE': 'STANDD',
			'HAIR': res.CHARACTERS[0]['HAIR'],'SKIN': res.CHARACTERS[0]['SKIN'],
			'ACCESORIES': self.guis['INVENTORY'].gui.find(0,['head'],'position'),'COSTUME': self.guis['INVENTORY'].gui.find(0,['clth_shirt1'],'position'),
			'INVFRM': 0,'DMGTIM': 100,'SHK': 0,'NODES': []}'''
		self.humanoid = {'HEAD': None,'SPRITE': None,'SKIN': 0,'HAIR': [0,0,0],'SHIRT': [0,(0,0,0)],'PANTS': [0,(0,0,0)],
			'ITEM': None,'ACCESORIES': []}
		self.ship = {'WING': [6,(180,10,10)],'BASE': [1,(250,10,10)],'COCKPIT': [0,(10,10,200)],'SPOILER': [0,(250,50,50)],
			'PROPULSOR': [0,(100,100,100)],'TEXTURE': 0,'STICKERS': []}#[[0,20,20],[0,40,20]]}

		self.mask = pygame.Rect(0,0,0,0)
		self.headpos = [0,0]
		self.headacc = 0.0
		self.dotfind = (255,0,0)
		self.eyes = [0,0]
		self.blink = 100
		self.emote = 'regular'
		self.gif = 0.0
		self.donesprites = {}
		self.editing = True
		self.opt = [0,0,0,0]
		self.optrects = []
		for i in range(8):
			self.optrects.append(pygame.Rect(self.window.get_width() - 130,10 + (75 * i),120,70))

	def doll(self):
		doll = None
		#ANIMATION
		if i['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(res.SPRITES[i['SPRITE']]): i['GIF'] = 0
		if i['PAUSE'] < 2: i['BLINK'] -= 1
		if i['BLINK'] < 0: i['BLINK'] = round(np.random.randint(30,90))
		#JUMP
		if i['GRAVITY'] > -5:
			i['JUMP'] += i['GRAVITY']
			i['GRAVITY'] -= 0.5
		if i['SPRITE'].startswith('SLEEP') == False:
			#MAP ICON
			if res.MAP == 'rodoviary':
				self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
			else:
				#DONE SPRITE
				sprstr = str(i['HAIR'][0]) + str(i['HAIR'][1]) + str(i['HAIR'][2]) + i['HEAD'] + str(np.floor(i['BLINK'])) + \
				'_' + i['SPRITE'] + str(i['SKIN']) + str(np.floor(i['GIF']))
				if sprstr in self.donesprites: doll = self.donesprites[sprstr]
				else:
					#EXTRA SPACEMENT
					if i['SPRITE'].startswith('STAND'): lst = [0,1,1,0]
					elif i['SPRITE'].startswith('TIREDSTAND'): lst = [0,1]
					elif i['SPRITE'].startswith('JUMP'): lst = [0,1]
					elif i['SPRITE'].startswith('WALK'): lst = [0,1,1,1,0,1,1,1]
					elif i['SPRITE'].startswith('RUN'): lst = [0,1,2,1,0,1,2,1]
					else: lst = [0]
					try: xsp = lst[np.floor(i['GIF'])]
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
						if True: #self.dlg['CAMERA'] == i['RECT']:
							mouth_img = pygame.image.load(res.TEMP_PATH + 'mouth_' + str(np.floor(i['GIF']).astype(int)) + '.png')
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
					face_srf.blit(head_img,(int(hair_rect.width/2) - int(head_rect.width/2),1 + int(hair_rect.height/2) - int(head_rect.height/2)))
					face_srf.blit(hair_img,(0,0))
					if fh_img != None:
						face_srf.blit(fh_img,(int(hair_rect.width/2) - int(head_rect.width/2),7 + int(hair_rect.height/2) - int(head_rect.height/2)))
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
						else: body_img = res.SPRITES[i['SPRITE']][np.floor(i['GIF']).astype(int)].copy()
						body_img.fill((res.PALETTES[0][int(i['SKIN'])]),None,pygame.BLEND_RGBA_MULT)
						#CLOTHES
						clth_img = []
						'''if t and i['COSTUME'] and int(i['DIRECTION']) < 6:
							for clth in i['COSTUME']:
								it = res.INVENTORY[clth[0]][clth[1]][clth[2]][clth[3]]
								cc = pygame.image.load(res.TEMP_PATH + it[0:-1] + '_' + i['SPRITE'] + '.png')
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
						body_img = pygame.image.load(res.SPRITES_PATH + 'water_' + str(np.floor(i['SWIM'])) + '.png')
					#DRAW
					fsz = face_srf.get_rect()
					bsz = body_img.get_rect()
					if bsz.width > fsz.width: wd = bsz.width
					else: wd = fsz.width
					doll = pygame.Surface((wd,fsz.height + bsz.height),pygame.SRCALPHA)
					doll.blit(body_img,(int(wd/2) - int(bsz.width/2),fsz.height))
					doll.blit(face_srf,(int(wd/2) - int(fsz.width/2),xsp))
					#doll = pygame.transform.scale(doll,(wd * 2,(fsz.height + bsz.height) * 2))
					self.donesprites[sprstr] = doll
				#SHADE
				xxx = False
				if xxx:# i['SPRITE'].startswith('SEAT') == False or i['SPRITE'].startswith('DRIVE') == False:
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
				img = doll.copy()
				#if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
				#self.display[0].blit(img,(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y - i['RECT'].height - i['JUMP']))
		return doll

	def bigsprite(self):
		if res.PAUSE < 2:
			self.gif += 0.4
			if int(self.gif) > 1: self.gif = 0
			self.blink -= 1
			if self.blink < 0: self.blink = np.random.randint(30,90)
			self.headpos[1] = int(np.sin(self.headacc) * 3)
			self.headacc += 0.1

		if self.blink > 5: blk = 0
		else: blk = 1
		sprstr = self.index + '.' + self.emote + '.ex' + str(self.eyes[0]) + '.ey' + str(self.eyes[1]) + \
			'.hy' + str(self.headpos[0]) + '.hy' + str(self.headpos[1]) + '.' + str(int(self.gif)) + '.' + str(blk)
		if sprstr in self.donesprites: srf = self.donesprites[sprstr]
		else:
			srf = pygame.Surface((96,128),pygame.SRCALPHA)
			lst = ['head','eyebrown','eye','glasses','nose','mouth','torso']
			for i in [x for x in lst if x in dtb.FREAKS[self.index]['AVATAR']]:
				if i == 'eye':
					for x in [-1,1]:
						if self.blink > 5: add = self.emote
						else: add = 'blink'
						img = pygame.image.load('{}{}_eye_{}.png'.format(res.FREAKS_PATH,self.index,add)).convert()
						#if self.cursor.x > xx - 5 and self.cursor.x < xx + 5: self.eyes[0] = self.cursor.x - xx
						#if self.cursor.y > yy - 5 and self.cursor.y < yy + 5: self.eyes[0] = self.cursor.y - yy
						cc = (1 + int(srf.get_width()/2) - int(img.get_width()/2) + int(not (img.get_width()%2)) + int(dtb.FREAKS[self.index]['EYES'][0] * x) - self.headpos[0],
							int(srf.get_height()/2) - int(img.get_height()/2) + dtb.FREAKS[self.index]['EYES'][1] - self.headpos[1])
						srf.blit(img, cc, pygame.Rect(1 - self.eyes[0],self.eyes[1],19,19))
				else:
					if i == 'head':
						img = pygame.image.load('{}humanoid_{}_{}.png'.format(res.FREAKS_PATH,self.index,self.emote)).convert_alpha()
					if i == 'body':
						if self.posture == 'backwards': add = '_backwards'
						else: add = ''
						img = pygame.image.load('{}{}_body{}.png'.format(res.FREAKS_PATH,self.index,add)).convert_alpha()
					offset = [0,0]
					for y in range(img.get_height()):
						for x in range(img.get_width()):
							if img.get_at((x,y))[0:3] == self.dotfind:
								offset = [x,y]
								img.set_at((x,y),c)
							else: c = img.get_at((x,y))
					if i == 'head':
						offset[0] += self.headpos[0]
						offset[1] += self.headpos[1]
					cc = (int(srf.get_width()/2) - offset[0],int(srf.get_height()/2) - offset[1])
					srf.blit(img,cc)
				
			if self.testing: mg = 2
			else: mg = 1
			srf = pygame.transform.scale(srf,(srf.get_width() * res.GSCALE * mg,srf.get_height() * res.GSCALE * mg))
			self.donesprites[sprstr] = srf

		return srf

	def freak(self):
		if res.PAUSE < 2:
			self.gif += 0.4
			if int(self.gif) > 1: self.gif = 0
			self.blink -= 1
			if self.blink < 0: self.blink = np.random.randint(30,90)
			self.headpos[1] = int(np.sin(self.headacc) * 3)
			self.headacc += 0.1

		'''for i in range(1):
			self.eyes[i] += 1
			if self.eyes[i] > 9: self.eyes[i] = -9'''
		if self.blink > 5: blk = 0
		else: blk = 1
		sprstr = self.index + '.' + self.emote + '.ex' + str(self.eyes[0]) + '.ey' + str(self.eyes[1]) + \
			'.hy' + str(self.headpos[0]) + '.hy' + str(self.headpos[1]) + '.' + str(int(self.gif)) + '.' + str(blk)
		if sprstr in self.donesprites: srf = self.donesprites[sprstr]
		else:
			srf = pygame.Surface((96,128),pygame.SRCALPHA)
			lst = ['body','eye','head']
			for i in [x for x in lst if x in dtb.FREAKS[self.index]['AVATAR']]:
				if i == 'eye':
					for x in [-1,1]:
						if self.blink > 5: add = self.emote
						else: add = 'blink'
						img = pygame.image.load('{}{}_eye_{}.png'.format(res.FREAKS_PATH,self.index,add)).convert()
						#if self.cursor.x > xx - 5 and self.cursor.x < xx + 5: self.eyes[0] = self.cursor.x - xx
						#if self.cursor.y > yy - 5 and self.cursor.y < yy + 5: self.eyes[0] = self.cursor.y - yy
						cc = (1 + int(srf.get_width()/2) - int(img.get_width()/2) + int(not (img.get_width()%2)) + int(dtb.FREAKS[self.index]['EYES'][0] * x) - self.headpos[0],
							int(srf.get_height()/2) - int(img.get_height()/2) + dtb.FREAKS[self.index]['EYES'][1] - self.headpos[1])
						srf.blit(img, cc, pygame.Rect(1 - self.eyes[0],self.eyes[1],19,19))
				else:
					if i == 'head':
						img = pygame.image.load('{}{}_head_{}.png'.format(res.FREAKS_PATH,self.index,self.emote)).convert_alpha()
					if i == 'body':
						if self.posture == 'backwards': add = '_backwards'
						else: add = ''
						img = pygame.image.load('{}{}_body{}.png'.format(res.FREAKS_PATH,self.index,add)).convert_alpha()
					offset = [0,0]
					for y in range(img.get_height()):
						for x in range(img.get_width()):
							if img.get_at((x,y))[0:3] == self.dotfind:
								offset = [x,y]
								img.set_at((x,y),c)
							else: c = img.get_at((x,y))
					if i == 'head':
						offset[0] += self.headpos[0]
						offset[1] += self.headpos[1]
					cc = (int(srf.get_width()/2) - offset[0],int(srf.get_height()/2) - offset[1])
					srf.blit(img,cc)
				
			if self.testing: mg = 2
			else: mg = 1
			srf = pygame.transform.scale(srf,(srf.get_width() * res.GSCALE * mg,srf.get_height() * res.GSCALE * mg))
			self.donesprites[sprstr] = srf

		return srf

	def spaceship(self):
		if res.PAUSE < 2: self.gif += 0.2
		if int(self.gif) > 1: self.gif = 0

		if self.direction == 3: gg = 0
		elif self.direction == 7: gg = 2
		else: gg = 1

		stk = ''
		for i in self.ship['STICKERS']: stk += str(i[0]) + '.x' + str(i[1]) + '.y' + str(i[2])
		sprstr = ''
		for i in ['BASE','WING','COCKPIT','SPOILER','PROPULSOR']:
			sprstr += str(self.ship[i][0]) + 'r' + str(self.ship[i][1][0]) + 'g' + str(self.ship[i][1][1]) + 'b' + str(self.ship[i][1][2]) + '.'
		sprstr += str(self.ship['TEXTURE']) + '.' + stk + str(gg + int(self.gif))
		if sprstr in self.donesprites: srf = self.donesprites[sprstr]
		else:
			srf = pygame.Surface((64,96),pygame.SRCALPHA)
			coords = {'BASE': (0,0),'COCKPIT': (0,0),'SPOILER': (0,0),'PROPULSOR': (0,20)}
			for i in [-1,1]: coords['WING_' + str(i)] = (9 * i,2)
			for i in self.ship['STICKERS']: coords['STICKERS_' + str(self.ship['STICKERS'][i][0])] = self.ship['STICKERS'][i][1:3]
			
			#JET
			img = pygame.image.load('{}spaceship_jet_{}_{}.png'.format(res.TEMP_PATH,str(0),str(gg + int(self.gif)))).convert_alpha()
			cc = (int(srf.get_width()/2) + coords['PROPULSOR'][0] - int(img.get_width()/2),
				int(srf.get_height()/2) + coords['PROPULSOR'][1])
			srf.blit(img,cc)

			#DRAW PARTS
			for i in self.ship:
				#PAIR OF WINGS
				if i == 'WING' and self.ship[i][0] > -1:
					for w in [-1,1]:
						img = pygame.image.load('{}spaceship_{}_{}.png'.format(res.TEMP_PATH, i.lower(), str(self.ship[i][0]))).convert_alpha()
						if w == 1: img = pygame.transform.flip(img,True,False)
						offset = (0,0)
						for y in range(img.get_height()):
							for x in range(img.get_width()):
								if img.get_at((x,y))[0:3] == self.dotfind:
									offset = (x,y)
									img.set_at((x,y),c)
								else: c = img.get_at((x,y))
						cc = (int(srf.get_width()/2) + coords[i + '_' + str(w)][0] - offset[0],int(srf.get_height()/2) + coords[i + '_' + str(w)][1] - offset[1])
						img.fill(self.ship[i][1],None,pygame.BLEND_RGBA_MULT)
						srf.blit(img,cc)
				#STICKERS
				elif i == 'STICKERS':
					for s in self.ship[i]:
						img = pygame.image.load('{}spaceship_{}_{}.png'.format(res.TEMP_PATH, i.lower(), str(self.ship[i][s][0]))).convert_alpha()
						offset = (0,0)
						for y in range(img.get_height()):
							for x in range(img.get_width()):
								if img.get_at((x,y))[0:3] == self.dotfind:
									offset = (x,y)
									img.set_at((x,y),c)
								else: c = img.get_at((x,y))
						cc = (int(srf.get_width()/2) + coords[i + '_' + str(self.ship[i][s][0])][0] - offset[0],
							int(srf.get_height()/2) + coords[i + '_' + str(self.ship[i][s][0])][1] - offset[1])
						srf.blit(img,cc)
				#BLEND TEXTURES
				elif i == 'TEXTURE': pass
				#EVERY OTHER PART
				elif self.ship[i][0] > -1:
					img = pygame.image.load('{}spaceship_{}_{}.png'.format(res.TEMP_PATH, i.lower(), str(self.ship[i][0]))).convert_alpha()
					offset = (0,0)
					for y in range(img.get_height()):
						for x in range(img.get_width()):
							if img.get_at((x,y))[0:3] == self.dotfind:
								offset = (x,y)
								img.set_at((x,y),c)
							else: c = img.get_at((x,y))
					cc = (int(srf.get_width()/2) + coords[i][0] - offset[0],int(srf.get_height()/2) + coords[i][1] - offset[1])
					img.fill(self.ship[i][1],None,pygame.BLEND_RGBA_MULT)
					srf.blit(img,cc)

			if self.testing: mg = 2
			else: mg = 1
			srf = pygame.transform.scale(srf,(srf.get_width() * res.GSCALE * mg,srf.get_height() * res.GSCALE * mg))
			self.donesprites[sprstr] = srf

		self.mask = pygame.Rect(25,70,82,70)
		return srf

	def inside_events(self,pressed,mouse):
		if pressed[0][0] and self.opt[1] > 0: self.opt[1] -= 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[1][0] and self.opt[1] < 7: self.opt[1] += 1; res.MIXER[0].play(res.SOUND['MENU_VER'])
		if pressed[4][0] and self.opt[1] == 0:
			self.opt[2] = not self.opt[2]
			if self.opt[2] == 0: res.MIXER[0].play(res.SOUND['MENU_BACK'])
			if self.opt[2] == 1: res.MIXER[0].play(res.SOUND['MENU_GO'])

		lst = ['COLORS','BASE','WING','COCKPIT','SPOILER','PROPULSOR','TEXTURE','STICKERS']
		rng = [(0,0),(0,3),(0,6),(0,3),(-1,2),(0,0),(-1,1),(-1,1)]
		for i in range(len(lst)):
			if self.opt[1] == i:
				if lst[i] == 'TEXTURE':
					if pressed[2][0] and self.ship[lst[i]] > rng[i][0]: self.ship[lst[i]] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
					if pressed[3][0] and self.ship[lst[i]] < rng[i][1]: self.ship[lst[i]] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				elif lst[i] != 'COLORS':
					if self.opt[2] == 0:
						if pressed[2][0] and self.ship[lst[i]][0] > rng[i][0]: self.ship[lst[i]][0] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
						if pressed[3][0] and self.ship[lst[i]][0] < rng[i][1]: self.ship[lst[i]][0] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
					if self.opt[2] == 1:
						if pressed[4][0] and self.opt[3] > 0: self.opt[3] -= 1; res.MIXER[0].play(res.SOUND['MENU_GO'])
						if pressed[5][0] and self.opt[3] < 2: self.opt[3] += 1; res.MIXER[0].play(res.SOUND['MENU_GO'])
		#if pressed[2][0]: self.page = 0; self.sfx.play(res.SOUND['PAGE_FLIP'])
		#if pressed[3][0]: self.page = 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		lst = ['COLORS','BASE','WING','COCKPIT','SPOILER','PROPULSOR','TEXTURE','STICKERS']
		for i in range(len(lst)):
			if self.opt[1] == i:
				if lst[i] == 'TEXTURE':
					if pressed[2][0] and self.ship[lst[i]] > rng[i][0]: self.ship[lst[i]] -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
					if pressed[3][0] and self.ship[lst[i]] < rng[i][1]: self.ship[lst[i]] += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				elif lst[i] != 'COLORS':
					if self.opt[2] == 1:
						nw = list(self.ship[lst[i]][1])
						if pressed[2][0] and nw[self.opt[3]] > 10: nw[self.opt[3]] -= 1
						if pressed[3][0] and nw[self.opt[3]] < 255: nw[self.opt[3]] += 1
						self.ship[lst[i]][1] = tuple(nw)

	def test(self):
		for event in pygame.event.get():
			pressed, mouse = tools.event.get_pressed(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			self.inside_events(pressed,mouse)
		pressed, mouse = tools.event.get_pressed(None)
		self.outside_events(pressed)
		self.window.fill((0,0,0))
		if self.index in [i for i in range(10)]: img = self.doll()
		elif self.index in dtb.FREAKS.keys(): img = self.freak()
		elif self.index == 'ship': img = self.spaceship()
		self.window.blit(img,(0,0))

		lst = ['COLORS','BASE','WING','COCKPIT','SPOILER','PROPULSOR','TEXTURE','STICKERS']
		for i in range(len(self.optrects)):
			if self.opt[1] == i: cl = res.COLOR
			else: cl = (200,200,200)
			pygame.draw.rect(self.window,cl,self.optrects[i])
			self.window.blit(res.FONTS['CALIBRI'].render(dtb.MENU['spaceship_' + lst[i].lower()],True,(10,10,10)),(self.optrects[i].x + 10,self.optrects[i].y + 10))
			if self.opt[2] == 0 and lst[i] not in ['COLORS','TEXTURE','STICKERS']: self.window.blit(res.FONTS['CALIBRI'].render('< ' + dtb.AVATAR['spaceship_' + lst[i].lower()][self.ship[lst[i]][0]] + ' >',True,(10,10,10)),(self.optrects[i].x + 10,self.optrects[i].y + 40))
			elif self.opt[2] == 1 and lst[i] not in['COLORS','TEXTURE','STICKERS']:
				cc = [(200,10,10),(10,200,10),(10,10,200)]
				for b in range(3):
					pygame.draw.rect(self.window,cc[b],pygame.Rect(self.optrects[i].x,self.optrects[i].y + 40 + (b * 10),self.optrects[i].width,10))
					pygame.draw.rect(self.window,(10,10,10),pygame.Rect(self.optrects[i].x + int(self.optrects[i].width/(255/self.ship[lst[i]][1][b])),self.optrects[i].y + 40 + (b * 10),10,10))

		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

class Character:
	def __init__(self,index,pos,file='dialogs',testing=False):
		if testing: self.window = pygame.display.set_mode((600, 600))
		self.surface = pygame.Surface((400, 600))
		self.testing = testing
		self.id = 0
		self.file = index
		self.item = None
		self.doll = Avatar(index)
		self.playing = False
		self.talk = None

		#PLAYERS
		if index in [str(i) for i in range(10)] + [i for i in range(10)]:
			self.playing = True
			self.index = int(index)
			self.doll.direction = 0
			self.sprite = self.doll.spaceship()
			self.mask = self.doll.mask
			self.hp = res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['VITALITY']
		#ENEMIES
		elif index in dtb.FREAKS.keys():
			self.index = index
			for i in dtb.FREAKS[index].items(): self.__dict__[i[0].lower()] = i[1]
			self.sprite = pygame.image.load(res.FREAKS_PATH + (self.index) + '_mini.png').convert_alpha()
			self.mask = pygame.Rect(0,0,self.sprite.get_width(),self.sprite.get_height())
			self.hp = self.vitality
		#NPCS
		else:
			self.index = index
			self.talk = file
			self.doll.direction = 0
			self.sprite = self.doll.spaceship()
			self.mask = self.doll.mask
			self.hp = 1
		self.inv = GUI.Inventory(None,0)

		self.click = pygame.Rect(0,0,0,0)
		self.rect = pygame.Rect(int(pos[0]),int(pos[1]),self.sprite.get_width(),self.sprite.get_height())
		self.btrng = [20,200]
		self.animation = ''
		self.direction = 0
		self.posture = 'regular'
		self.holdfire = 0
		self.speed = 2
		self.hdpos = [0,0]
		self.acc = 0
		self.speedlock = 0
		self.jump = 0
		self.gravity = -5
		self.step = 10
		#self.sprite = 'STANDD'
		self.fighting = False
		self.destroy = False
		self.depth = 0

		self.score = 0
		self.condition = []
		self.hold = None

		self.dialog = None
		self.particles = []
		self.follow = None
		self.follmov = None
		self.follend = None
					
		self.time = 20
		self.invfrm = 0
		self.fade = 10
		self.away = 0
		self.effect = 0.0
		self.btimes = [0,0,0,0]
		#if self.map.properties['HABITAT'] == self.habitat:
		if self.jump == 6:
			self.strenght = int(self.strenght * 1.25)
			self.agility = int(self.agility * 1.25)
			self.resistance = int(self.resistance * 1.25)
			self.hp = int(self.hp * 1.25)
		
	def overworld_move(self):
		#REPELLENT
		rplt = False
		for c in res.PARTY[res.FORMATION]:
			if res.CHARACTERS[c]['HEALTH'] == 2: rplt = True
		if self.fighting == False:
			#NOTICING
			if self.path == 'notice' and self.time == 0: self.path = 'follow'
			#STEALTH MOVEMENT
			elif self.path == 'stealth':
				if self.facing(i,self.player[0]) == 2 and rplt == False:
					res.MIXER[0].play(res.SOUND['NOTICED'])
					self.path = 'notice'
					self.time = 10
				else:
					if self.direction == 0: self.direction = 1
					if self.time == 0:
						if self.direction == 1: self.direction = 5
						elif self.direction == 5: self.direction = 1
						self.time = 20
			#FOLLOW MOVEMENT
			elif self.path == 'follow':
				self.direction = tools.physics.follow(self.rect,self.player[0]['RECT'])
				if rplt:
					self.path = 'horizontal'
					self.direction = 0
					self.time = 20
			#HORIZONTAL MOVEMENT
			elif self.path == 'horizontal':
				if self.direction == 0: self.direction = 1
				if self.time == 0:
					if self.direction == 1: self.direction = 5
					elif self.direction == 5: self.direction = 1
					self.time = 20
			#TRAIL MOVEMENT
			elif isinstance(self.path,tuple):
				if self.follow != None:
					if (self.rect.x,self.rect.y) == self.follend:
						self.follow += 1
						if self.follow >= len(self.path): self.path = 'stay'
						else: self.follend = (self.rect.x + self.path[self.follow][0],self.rect.y + self.path[self.follow][1])
					else:
						self.rect.x += int(self.path[self.follow][0]/self.speed)
						self.rect.y += int(self.path[self.follow][1]/self.speed)
				else: self.follow = 0; self.speed = 200; self.follend = (self.rect.x + self.path[self.follow][0],self.rect.y + self.path[self.follow][1])

				self.time -= 1
				if self.time == 0:
					self.particles.append(['particle',{'TYPE': 'gunshot', 'RECT': pygame.Rect(self.rect.x,self.rect.y,6,6),'COLOR': (100,150,200),'RADIUS': 3,
					'DIRECTION': 2 * ((np.pi * 2)/8), 'SPEED': 8,'WALL' : 0,'FOLLOW': 0,'POWER': 0,'DAMAGE': 3,
					'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
					self.time = 60
			#MOVING
			if isinstance(self.path,str) and self.path != 'stay':
				chk = []
				lst = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
				for c in range(len(lst)):
					if self.direction == c + 1: self.rect.x += lst[c][0] * self.agility; self.rect.y += lst[c][1] * self.agility
					chk.append([self.rect.x + (lst[c][0] * 30),self.rect.y + (lst[c][1] * 30)])
				self.time -= 1
				
	def inside_events(self,pressed,mouse):
		self.click = mouse
		if pygame.Rect.colliderect(mouse,self.mask): self.emote = 'hurt'
		#PLAYER OPTIONS
		if self.playing and res.PAUSE == 0:
			self.posture = 1
			for a in range(6):
				if pressed[a][self.index]:
					#BOMB
					if res.ACTION[a] == 'bomb':
						sht = None
						for f in ['regular','slime','bolt','grenade','tactical']:
							if sht == None: sht = self.guis['INVENTORY'].gui.find(res.PARTY[res.FORMATION][p],'bomb_' + f,'value')
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
								'X': np.floor(i['RECT'].x/self.map.tilewidth) * self.map.tilewidth,
								'Y': np.floor(i['RECT'].y/self.map.tileheight) * self.map.tileheight,
								'IMAGE': img,'GIF': 0.0,'POWER': pp})
								res.MIXER[0].play(res.SOUND['EQUIP'])
								sht[1] -= 1
								if sht[1] == 0: nn = 'bomb_regular'
								res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]] = nn
								res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3] + 1] = str(sht[1])
							else: res.MIXER[0].play(res.SOUND['ERROR'])
					#SHOOTING
					if res.ACTION[a] == 'shoot':
						sht = None
						for f in ['pow_bubble','pow_doublebubble','pow_triplebubble','pow_bounce','pow_plasma','pow_phantom','pow_follow',
							'reactor1','reactor2','reactor2','reactor3','reactor4','reactor5','reactor6','reactor7']:
							if sht == None: sht = self.inv.find(res.PARTY[res.FORMATION][self.index],f,'value')
						if sht != None:
							if sht[1] > 0:
								nn = res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]]
								qq = 1
								if nn == 'pow_doublebubble': qq = 2
								if nn == 'pow_triplebubble': qq = 3
								if nn.startswith('reactor'):
									if sht[1] < 4: qq = sht[1]

								for q in range(qq):
									pdict = {'TYPE': 'gunshot','RECT': pygame.Rect(self.rect.x + self.mask.x + int(self.mask.width/2) - 3,self.rect.y + self.mask.y + int(self.mask.height/2) - 3,6,6),
										'DAMAGE': 1,'COLOR': (100,150,200),'RADIUS': 3,'DIRECTION': 0, 'SPEED': dtb.ITEMS[nn][5]['SPEED'],'DAMAGE': 3,'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False}
									
									pdict['DIRECTION'] = 6 * ((np.pi * 2)/8)
									#pdict['DIRECTION'] = (self.direction - 1) * ((np.pi * 2)/8)

									if nn == 'pow_plasma': pdict['TYPE'] = 'megunshot'
									if nn == 'pow_bounce': pdict['WALL'] = 1
									if nn == 'pow_phantom': pdict['WALL'] = 2
									if nn == 'pow_follow': pdict['FOLLOW'] = None

									if nn.startswith('reactor'):
										if sht[1] == 2: pdict['RECT'].x += (q * dtb.ITEMS[nn][5]['SPACING']) - int(dtb.ITEMS[nn][5]['SPACING']/2)
										if sht[1] == 3: pdict['DIRECTION'] = (np.pi * (4/dtb.ITEMS[nn][5]['ANGLE'])) + ((np.pi * 2)/dtb.ITEMS[nn][5]['ANGLE']) * q
										if sht[1] == 4:
											pdict['GIF'] = 0.0
											pdict['IMAGE'] = []
											for a in (0,1,2,1): pdict['IMAGE'].append(pygame.image.load(res.SPRITES_PATH + 'missile_' + str(a) + '.png').convert_alpha())
									self.particles.append(['particle',pdict,0])
								
								res.MIXER[0].play(res.SOUND['SHOOT_1'])
								if nn.startswith('pow_'): sht[1] -= 1
								if sht[1] == 0: nn = 'pow_bubble'

								res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3]] = nn
								res.INVENTORY[sht[0][0]][sht[0][1]][sht[0][2]][sht[0][3] + 1] = str(sht[1])
							else: res.MIXER[0].play(res.SOUND['ERROR'])
					#JUMP
					if res.ACTION[a] == 'jump':
						res.MIXER[0].play(res.SOUND['FALL'])
						self.gravity = 4.5 + float(res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['ACROBATICS']/2)
						self.step = 0
					#RUN
					if res.ACTION[a] == 'run' and res.MOUSE == 2:
						spd = [3 + np.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/4),
							6 + np.floor(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ATLETISM']/2)]
						if self.posture == 'swim': spd[0] -= 3; spd[1] -= 1
						#elif self.guis['INVENTORY'].gui.space(p) == False: spd[0] -= 2; spd[1] -= 1
						self.speedlock = not self.speedlock
						if self.speedlock: self.speed = spd[1]
						else: self.speed = spd[0]
			#DRIVING OPTIONS
			if self.posture == 'driving':
				if res.GAS > 0:
					if pressed[2][p]:
						self.direction -= 1
						if self.direction == 0: self.direction = 8
					elif pressed[3][p]:
						self.direction += 1
						if self.direction == 9: self.direction = 1
			else:
				if self.jump == 0 and res.MAP != 'rodoviary':
					#PLACE OBJECTS
					if pressed[4][self.index] and self.hold != None: self.hold  = None

		#NPCS OPTIONS
		if self.talk and res.PAUSE == 0:
			self.dialog = None
			cld = 0
			#if pygame.Rect.colliderect(p['RECT'],self.rect) and p['PLAYING']:
			#	if pressed[4][0]: cld = 2
			#	else: cld = 1
			if pygame.Rect.colliderect(mouse,self.rect) and pressed[4][0]: cld = 2
			if cld:
				res.HINTEXT = 'NPC_DIALOG'
				#SCENE CHANGE
				'''if isinstance(i['TYPE'],str) and i['TYPE'].startswith('scene'):
					if res.SCENE == int(i['TYPE'][5]) - 1:
						res.SCENE = int(i['TYPE'][5])
						act = True
					else: act = False'''
				if cld > 1:
					res.PAUSE = 1
					self.follow = None
					#DRIVE THRU
					if self.talk.startswith('DRITHR'):
						if p['DRIVING'] != None:
							if self.dlg['FADE'] > 0: self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),i['RECT'])
						else:
							self.guis['INVENTORY'].gui.type = 3
							self.guis['INVENTORY'].gui.fade = 0
							self.lopt = 1
							self.opt = 0
							self.mnu = 0
					else: self.dialog = self.index
					#MARKET CASHIER
					'''if i['TYPE'] == 2:
						#NOTHING IN BASKET
						if res.BASKET == []:
							if self.dlg['FADE'] > 0:
								self.dialog(dtb.DIALOGS[i['WHO']][0].copy(),i['RECT'])
						#BUY ITEMS
						else:
							self.guis['INVENTORY'].gui.type = 3
							self.guis['INVENTORY'].gui.fade = 0
							self.lopt = 1
							self.opt = 0
							self.mnu = 0'''

	def outside_events(self,pressed):
		#INVENCIBILITY FRAMES
		if self.invfrm > 0: self.invfrm -= 1

		sprupd = True
		if self.playing and res.PAUSE == 0:
			#DRIVING OPTIONS
			if self.posture == 'driving':
				if pressed[0][self.index]:
					self.posture = 'regular'
					'''self.display.width = 600
					self.display.height = 400
					self.surfaces[0] = pygame.Surface((600, 400))
					self.cam.width = self.display.width
					self.cam.height = self.display.height'''
					self.direction = 3
				if res.GAS > 0:
					if pressed[1][self.index]:
						if self.speed > 0.0: self.speed -= self.vehicles[i['DRIVING']]['ACCELERATION']
					elif pressed[5][self.index]:
						if self.speed < self.vehicles[i['DRIVING']]['SPEED'] and res.GAS > 0.0:
							self.speed += self.vehicles[i['DRIVING']]['ACCELERATION']
						res.GAS -= self.vehicles[i['DRIVING']]['GAS']
					else: self.speed -= self.vehicles[i['DRIVING']]['ACCELERATION']
			#REGULAR OPTIONS
			elif self.jump == 0:
				hld = False
				for a in range(6):
					#POSTURE
					if pressed[a][self.index] and res.ACTION[a] in ['look','squat'] and self.posture not in ['swim','sleep']:
						self.posture = res.ACTION[a]
					#HOLDFIRE
					if pressed[a][self.index] and res.ACTION[a] == 'shoot':
						if self.holdfire > 20:
							self.particles.append(['particle',{'TYPE': 'blood',
								'RECT': pygame.Rect(self.rect.x + self.mask.x + int(self.mask.width/2) - 10 + np.random.randint(-5,5),
									self.rect.y + self.mask.y + int(self.mask.height/2) - 10 + np.random.randint(-5,5),0,0),
								'COLOR': (200,200,200),'RADIUS': np.random.randint(2,2 + int(self.holdfire/10)),'FADE': np.random.uniform(0.1,0.2),
								'DIRECTION': (np.random.uniform(0,8)) * ((np.pi * 2)/8), 'SPEED': np.random.randint(1,1 + int(self.holdfire/20)),'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						if self.holdfire < 100: self.holdfire += 1
						hld = True
				#HOLDFIRE RELEASE
				if hld == False:
					if self.holdfire >= 100:
						rt = 6
						#rt = self.direction - 1
						self.particles.append(['particle',{'TYPE': 'megunshot',
						'RECT': pygame.Rect(self.rect.x + self.mask.x + int(self.mask.width/2) - 10,self.rect.y + self.mask.y + int(self.mask.height/2) - 10,20,20),
						'COLOR': (200,10,10),'RADIUS': 10,'DIRECTION': (rt) * ((np.pi * 2)/8), 'SPEED': 8,'WALL' : 0,'FOLLOW': 0,
						'POWER': 1,'DAMAGE': 30,'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						res.MIXER[0].play(res.SOUND['SHOOT_2'])
					self.holdfire = 0

				#MOVE DIRECTIONS
				prs = 0
				bt = [3,1,2,0,3,0]
				for d in range(4):
					if pressed[bt[d]][self.index] and res.ACTION[bt[d]] in ['move','walk']:
						if res.ACTION[bt[d]] == 'move': sprupd = False
						if self.direction in [(d * 2),(d * 2) + 1,(d * 2) + 2]: prs = 2
						if pressed[bt[d - 1]][self.index]: self.direction = (d * 2)
						elif pressed[bt[d + 1]][self.index]: self.direction = (d * 2) + 2
						else: self.direction = (d * 2) + 1
						if prs == 0: prs = 1

				#SPEED SET
				spd = [3 + np.floor(res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['ATLETISM']/4).astype(int),
					6 + np.floor(res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['ATLETISM']/2).astype(int)]
				if self.posture == 'swim': spd[0] -= 3; spd[1] -= 1
				#INVENTORY WEIGHT AFFECTS SPEED
				#elif self.guis['INVENTORY'].gui.space(self.index) == False: spd1 -= 2; spd2 -= 1
				if res.MAP != 'rodoviary' and res.MOUSE < 2:
					if pressed[5][self.index]: self.speed = spd[1]
					else: self.speed = spd[0]
				elif res.MOUSE < 2: self.speed = 1
				else:
					if self.speedlock: self.speed = spd[1]
					else: self.speed = spd[0]

				if self.direction == 0: self.direction = 8
				if prs == 0 and self.acc > 0.0 and self.speed > 0.0: self.speed -= self.acc
				#elif prs == 2 and self.speed > 0.0: self.speed -= 0.5
				elif prs == 0: self.speed = 0
			
			#FOLLOW
			if self.follow != None:
				end = False
				if self.follow != (None,None):
					self.speed = 3
					self.direction = tools.physics.follow(self.rect,self.follow)
					if self.colide(i['RECT'],i['FOLLOW']): end = True
				else: end = True
				if end:
					self.direction = self.follend
					self.follow = None
					self.follend = 'head'
					self.speed = 0
			#MOVING CHARACTER
		'''dx = 0; dy = 0
		if i['DIRECTION'] in [8,1,2]: dx = self.map.tilewidth
		if i['DIRECTION'] in [2,3,4]: dy = self.map.tileheight
		if i['DIRECTION'] in [4,5,6]: dx = -self.map.tilewidth
		if i['DIRECTION'] in [6,7,8]: dy = -self.map.tileheight
		ind = (np.floor((i['RECT'].y + dy)/self.map.tileheight) * self.map.width) + np.floor((i['RECT'].x + dx)/self.map.tilewidth)
		rct = self.tilrect[3][ind]
		if rct == None: cld = False
		else:
			cld = self.colide(i['RECT'],rct[1])
			#if cld == False:
			#	for obj in self.objects:
			#		if obj[0] == 'move': cld = self.colide(i['RECT'],obj[1]['RECT'])'''
		cld = False
		if cld: self.speed = 0
		else:
			#POSITION UPDATE
			if self.speed > 0 and self.jump == 0 and self.playing:
				chk = []
				lst = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
				for c in range(len(lst)):
					if self.direction == c + 1: self.rect.x += lst[c][0] * int(self.speed); self.rect.y += lst[c][1] * int(self.speed)
					chk.append([self.rect.x + (lst[c][0] * 30),self.rect.y + (lst[c][1] * 30)])
				#ALIGN
				algn = 1
				if algn > 1:
					if self.direction in [3,7]: self.rect.x = (int(self.rect.x/algn) * algn) + int(algn/2) - int(self.rect.width/2)
					if self.direction in [1,5]: self.rect.y = (int(self.rect.y/algn) * algn) + int(algn/2) - int(self.rect.height/2)
				#i['RECT'].x += int(np.cos(i['DIRECTION']) * i['SPEED'])
				#i['RECT'].y += int(np.sin(i['DIRECTION']) * i['SPEED'])
			elif self.jump > 0 and self.playing:
				if self.direction == 3: self.rect.y += self.speed
				elif self.direction == 7: self.rect.y -= self.speed
			#PARTY FOLLOW
			'''if i['PLAYING'] == False:
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
			'''
			#SPRITE UPDATE
			sprupd = False
			if sprupd:
				ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]
				if self.jump > 0: spr = 'JUMP'
				elif self.posture != 'regular': spr = self.posture.upper()
				elif self.speed > 3: spr = 'RUN'
				elif self.speed > 0: spr = 'WALK'
				elif ch['VITALITY'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch]['LEVEL']/5: spr = 'STAND'
				else: spr = 'TIREDSTAND'

				lst = ['R','RD','D','LD','L','LU','U','RU']
				for c in lst:
					if self.direction == c + 1:
						if self.speed > 0 or self.folled == 'head': self.head = lst[c]
						self.animation = spr + lst[c]
		if self.speed < 0: self.speed = 0
	
	def colide(self,i):
		do = False
		msk = pygame.Rect(self.rect.x + self.mask.x,self.rect.y + self.mask.y,self.mask.width,self.mask.height)
		if i[0] == 'char' and i[1].talk == None and pygame.Rect.colliderect(msk, pygame.Rect \
			(i[1].rect.x + i[1].mask.x,i[1].rect.y + i[1].mask.y,i[1].mask.width,i[1].mask.height)): do = True
		if i[0] == 'particle' and i[1]['TYPE'] in ['gunshot','megunshot'] and i[1]['EMISSOR'] != self.file and pygame.Rect.colliderect(msk, i[1]['RECT']): do = True

		if i[0] == 'char' and do:
			if isinstance(self.file,int):
				if isinstance(i[1].file,int): do = False
				elif i[1].talk: do = False
				if len([1 for c in res.CHARACTERS if 2 in c['HEALTH']]): do = False
			else: do = False
		if self.talk: do = False

		if do and self.fighting == False:
			#BATTLE ENTER
			if res.BTYPE < 3 and i[0] == 'char':
				if i[1].fighting != 'mercenary': self.foe.append(i[1])
				else: self.mrc.append(i[1])
				i[1].fighting = True

				if (len(self.foe) + len(self.mrc)) == 1:
					if res.BESTIARY[i[1].file]['SEEN'] == 0 and int(i[1].type[0:2]) < 1: self.turn = -6
					#if self.turn != -6: self.turn = -self.facing(i,self.player[0])
					self.turn = -1
					self.fight()
			#DAMAGE
			elif self.invfrm == 0:
				#REGULAR DAMAGE
				if self.hp > 0:
					if i[0] == 'particle':
						dmg = i[1]['DAMAGE']
						if i[1]['TYPE'] == 'gunshot': i[1]['DESTROY'] = True
					else: dmg = i[1].strenght
					self.hp -= dmg
					self.particles.append(['particle',{'TYPE': 'text','TEXT': str(dmg),'RECT': pygame.Rect(self.rect.x + np.random.randint(-5,5),self.rect.y,self.rect.width,self.rect.height),
							'GRAVITY': -5,'GRAVACC': 0.5,'GRAVLIMIT': 0,'SHADE': 1, 'SHAKE': 0, 'COLOR': (200,200,200),
							'ALPHA': 250,'ALPHADE': 10,'TIME': 10,'LIMIT': 3,'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						
					if isinstance(self.file,int):
						res.MIXER[1].play(res.SOUND['DAMAGE_1'])
						res.CHARACTERS[res.PARTY[res.FORMATION][self.file]]['VITALITY'] = self.hp
						self.invfrm = 120
					elif self.file in dtb.FREAKS.keys(): res.MIXER[1].play(res.SOUND['SCREAM1'])
					#self.guis['STATUS'].show = True
				#DEATH
				if self.hp <= 0:
					#GAME OVER
					if isinstance(self.file,int): res.MIXER[1].play(res.SOUND['BATTLE_LOST'])
					#ENEMY PURGE
					elif self.file in dtb.FREAKS.keys():
						sc = 10
						if i[0] == 'particle':
							if i[1]['TYPE'] == 'gunshot':
								i[1]['DESTROY'] = True
								sc = 25
							else: sc = 30
						res.MIXER[2].play(res.SOUND['EXPLOSION_1'])
						res.CHARACTERS[res.PARTY[res.FORMATION][i[1]['EMISSOR']]]['SCORE'] += sc
						self.particles.append(['particle',{'TYPE': 'explode', 'RECT': self.rect.copy(),'GIF': 0.0,'TIME': 0,'LIMIT': 3,'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						self.particles.append(['particle',{'TYPE': 'text','TEXT': str(sc),'RECT': self.rect.copy(),'GRAVITY': -5,'GRAVACC': 0.2,'GRAVLIMIT': 5,'SHADE': 1, 'SHAKE': 0, 'COLOR': (200,200,200),
							'ALPHA': 250,'ALPHADE': 10,'TIME': 30,'LIMIT': 3,'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						for p in range(50):
							self.particles.append(['particle',{'TYPE': 'blood',
								'RECT': pygame.Rect(self.rect.x + self.mask.x + int(self.mask.width/2) - 10 + np.random.randint(-5,5),
									self.rect.y + self.mask.y + int(self.mask.height/2) - 10 + np.random.randint(-5,5),0,0),
								'COLOR': (200,200,200),'RADIUS': np.random.randint(2,6),'FADE': 0.05,
								'DIRECTION': (np.random.uniform(0,8)) * ((np.pi * 2)/8), 'SPEED': np.random.randint(1,6),'EMISSOR': self.file,'DEPTH': self.rect.y,'DESTROY': False},self.rect.y])
						if self.item:
							img = self.inv.itimg(self.item)
							self.particles.append(['item',{'IMAGE': img,'ITEM': self.item,'RECT': self.rect.copy(),'FLOAT': 0,'ACC': 2,'ACCLIMIT': 5,'ACCSPD': 0.1,'DESTROY': False},100])
						self.destroy = True
		#GET ITEM
		elif i[0] == 'item' and isinstance(self.file,int) and pygame.Rect.colliderect(self.rect,i[1]['RECT']):
			if i[1]['ITEM'].startswith('bomb'):
				res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][1][0] = i[1]['ITEM']
				res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][1][1] = '3'
			elif i[1]['ITEM'].startswith('pow_bubble'):
				res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][2][0] = i[1]['ITEM']
				res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][2][1] = '3'
			elif i[1]['ITEM'].startswith('reactor'):
				for s in range(2):
					if res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][1 + s][0] in ['_','reactor0']:
						res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][1 + s][0] = i[1]['ITEM']
						res.INVENTORY[res.PARTY[res.FORMATION][self.file]][4][1 + s][1] = '0'
			else: self.guis['INVENTORY'].gui.add(res.PARTY[res.FORMATION][0],i[1]['ITEM'])
			res.MIXER[0].play(res.SOUND['ITEM_GET'])

			img = []
			for a in range(8): img.append(pygame.image.load(res.SPRITES_PATH + 'pop_' + str(a) + '.png').convert_alpha())
			self.particles.append(['particle',{'TYPE': 'pop','IMAGE': img,'GIF': 0.0,'RECT': i[1]['RECT'].copy(),'DESTROY': False},0])
			i[1]['DESTROY'] = True

	def overworld_draw(self,target,camera=pygame.Rect(0,0,0,0)):
		#VISIBLITY
		visible = True
		if isinstance(self.file,int):
			visible = not bool(self.invfrm%2)
			if 23 in res.CHARACTERS[res.PARTY[res.FORMATION][self.file]]['HEALTH']: visible = False

		if visible:
			#RECTDEBUG
			rectdebug = False
			if rectdebug:
				srf = pygame.Surface((self.mask.width,self.mask.height)); srf.fill((200,0,0))
				target.blit(srf,(self.rect.x + self.mask.x,self.rect.y + self.mask.y))
				pygame.draw.rect(target,(200,0,0),self.rect,3)

			#DRAW
			if self.doll:
				self.doll.direction = self.direction
				img = self.doll.spaceship().copy()
			if self.index in dtb.FREAKS.keys():
				img = pygame.image.load(res.FREAKS_PATH + (self.index) + '_mini.png')

			#SHADE
			if res.TIME[0] < 12:
				tms = (12 - res.TIME[0]) * 2
				sxx = self.rect.x + int(self.rect.width/2) - tms + 5
			else:
				tms = (res.TIME[0] - 12) * 2
				sxx = self.rect.x + int(self.rect.width/2)
			if tms < 5: tms = 5
			shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,7))
			shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
			shd.set_alpha(100)
			target.blit(shd, (sxx, self.rect.y))

			#ARROW
			if pygame.Rect.colliderect(self.click,pygame.Rect(self.mask.x + self.rect.x,self.mask.y + self.rect.y,self.mask.width,self.mask.height)):
				target.blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (self.rect.x + int(self.rect.width/2) - camera.x, self.rect.y - camera.y - self.mask.height))
			
			#CONDITIONS
			if isinstance(self.file,int):
				if 1 in res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['HEALTH']:
					if i['SHK'] == 0:
						pygame.draw.rect(target, res.COLOR, pygame.Rect(i['RECT'].x - camera.x + 10 + i['SHK'],i['RECT'].y - camera.y - 40,16,13))
					else: pygame.draw.rect(target, (255,10,10), pygame.Rect(i['RECT'].x - camera.x + 10 + i['SHK'],i['RECT'].y - camera.y - 40,16,13))
					target.blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[res.PARTY[res.FORMATION][self.index]]['HEALTH']) + '.png'), (i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40))
			
			#HIDE FREAK AND NOTICE
			if isinstance(self.index,str) and self.talk == None:
				if res.BESTIARY[self.index]['SEEN'] == 0 and int(self.index[0:2]) > 1 != 'mercenary': img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
				if self.path == 'notice': target.blit(pygame.image.load(res.SPRITES_PATH + 'notice.png'), (self.rect.x, self.rect.y - 30))
			
			self.sprite = img
		target.blit(self.sprite,(self.rect.x,self.rect.y))
		return self.sprite
	
	def inbattle_draw(self):
		#BATTLE IMAGE
		if self.fade > 0 and 9 not in self.condition:
			self.fighting = True
			if self.mask.x > 0:
				#MOVE
				if 1 not in self.condition:
					if self.dodge == 'walk':
						if self.direction == 1: self.mask.x += self.agility
						if self.direction == 5: self.mask.x -= self.agility
						if self.mask.x < self.btrng[0]: self.direction = 1
						if self.mask.x > self.btrng[1]: self.direction = 5
					if self.dodge == 'jump':
						if i['DIRECTION'] == 1: i['MASK'].x += i['AGILITY']
						if i['DIRECTION'] == 5: i['MASK'].x -= i['AGILITY']
						if i['MASK'].x < self.btrng[0]: self.direction = 1
						if i['MASK'].x > self.btrng[1]: self.direction = 5
						self.mask.y += self.speed
						i['SPEED'] -= 0.5
						if i['SPEED'] == -3.0:
							i['DIRECTION'] = 5
							i['SPEED'] = 3
					if self.dodge == 'fly':
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
					if self.dodge == 'spin':
						i['MASK'].x += i['SPEED']
						if i['DIRECTION'] == 1:
							i['SPEED'] -= 0.5
							if i['SPEED'] == -3.0: i['DIRECTION'] = 5
						if i['DIRECTION'] == 5:
							i['SPEED'] += 0.5
							if i['SPEED'] == 3.0: i['DIRECTION'] = 1
					if self.dodge == 'circle':
						i['MASK'].x = int(np.cos(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzw/2) - 50
						i['MASK'].y = int(np.sin(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzh/2) - 50
						i['SPEED'] += 0.5
				else:
					if self.dodge == 'jump': i['SPEED'] = 3.0
					if self.dodge in ['fly','spin','circle']: i['SPEED'] = 0.0
				if self.fade < 10:
					#i['SPRITE'].blit(pygame.image.load(res.SPRITES_PATH + 'eff_death_' + str(i['FADE']) + '.png'), (0,0), special_flags=pygame.BLEND_SUB)
					if i['FADE'] > 5: i['SPRITE'].fill((int((i['FADE'] - 5) * 50),10,10),None,pygame.BLEND_RGBA_MULT)
					elif i['FADE'] > 0: i['SPRITE'].fill((200,10,10,int(i['FADE'] * 50)),None,pygame.BLEND_RGBA_MULT)
				
				#DRAW
				if self.away == 0:
					self.sprite = self.doll.freak()
				else:
					self.away += 1
					szw = self.btsprite.get_width() - (int(self.btsprite.get_width()/20) * self.away)
					szh = self.btsprite.get_height() - (int(self.btsprite.get_height()/20) * self.away)
					if szw < 0: szw = 0
					if szh < 0: szh = 0
					if szw == 0 and szh == 0:
						self.fighting = False
						self.fade = 0
					self.display[0].blit(pygame.transform.scale(i['SPRITE'],(szw,szh)), (i['MASK'].x, i['MASK'].y - i['AWAY']))
				#EFFECTS ANIMATION
				if self.condition:
					self.surface.blit(res.SPRITES['EFFECT_' + str(i['HEALTH'])][np.floor(self.effect)], (self.mask.x + 5, self.mask.y - 10))
					self.effect += 0.5
					#self.effect >= len(res.SPRITES['EFFECT_' + str(i['HEALTH'])]): self.effect = 0.0
			else: self.mask.x -= self.agility
		#SHOOT
		if res.BTYPE == 3:
			ind = 0
			for p in self.particles:
				if p['TYPE'] == 'gunshot' and self.colide(i['RECT'],p['RECT']):
					res.MIXER[0].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
					self.hitisplay(10, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y,1,1), '50', (200, 200, 200))
					self.player[p['PLAYER']]['SCORE'] += 10
					i['FIGHTING'] = False
					i['VITALITY'] = 0
					del self.particles[ind]
					break
				ind += 1
		
	def test(self):
		for event in pygame.event.get():
			pressed, click = tools.event.get_pressed(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if self.playing: self.inside_events(pressed,click)
		pressed, click = tools.event.get_pressed(None)
		if self.playing: self.outside_events(pressed)
		self.surface.fill((100,100,100))
		#self.overworld_move()
		#self.inbattle_draw()
		#self.surface.blit(self.overworld_draw(),(self.rect.x - 50,self.rect.y))

		for p in self.particles:
			if p['TYPE'] in ['blood','gunshot']:
				p['RECT'].x += int(np.cos(p['DIRECTION']) * p['SPEED'])
				p['RECT'].y += int(np.sin(p['DIRECTION']) * p['SPEED'])
				if p['TYPE'] == 'blood':
					p['RADIUS'] -= 0.25
					if p['RADIUS'] < 0.0: p['RADIUS'] = 0.0
					cor = (p['RECT'].x,p['RECT'].y)
				else: cor = (p['RECT'].x,p['RECT'].y)
				pygame.draw.circle(self.surface, p['COLOR'], cor, np.ceil(p['RADIUS']))
				#if p['TYPE'] == 'gunshot':
				#	if pygame.rect.colliderect(pygame.Rect(p['RECT'].x,p['RECT'].y,2,2),self.cam) == False: p['DESTROY']

		if self.index in [i for i in range(10)]: img = self.doll.doll()
		elif self.index in dtb.FREAKS.keys(): img = self.doll.freak()
		elif self.index == 'ship': img = self.doll.spaceship()
		self.surface.blit(self.sprite,(self.rect.x - int(self.sprite.get_width()/2),self.rect.y - int(self.sprite.get_height()/2)))

		if self.testing: self.window.blit(self.surface,(0,0))
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

class TileHandler(xml.sax.ContentHandler):
	def __init__(self,file,lst=None,first=0):
		#self.window = pygame.display.set_mode((600,600))
		self.window = pygame.Surface((1,1))
		self.name = file[:-4]
		self.first = first
		self.ind = ''
		self.img = None
		self.imgpath = None
		self.tileset = lst
		self.tiles = {}
		self.tilprp = {} #for old tiled tileset versions
		self.tilani = {}
		self.tilidx = 0
		self.terrains = {}
		self.content = ''
		self.gid = 0
		self.cor = [0,0]

		self.rows = None
		self.columns = None

		parser = xml.sax.make_parser()
		parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		parser.setContentHandler(self)
		parser.parse(res.TILESETS_PATH + file)

	def startElement(self, tag, attributes):
		if tag == 'tileset':
			for i in [i[0] for i in attributes.items() if i[0] not in ['version','tiledversion','name']]:
				setattr(self, i, int(attributes[i]))
			if self.rows == None: self.rows = int(self.tilecount/self.columns)
			self.length = self.rows * self.columns
		if tag in ['img','image']:
			self.img = pygame.image.load(res.TILESETS_PATH + attributes['source']).convert_alpha()
			self.imgpath = attributes['source']
			self.width = self.img.get_width(); self.height = self.img.get_height()
		if tag == 'tile':
			if self.img:
				self.gid = int(attributes['id']) + self.first
				self.cor[1] = int(int(attributes['id'])/self.columns)
				self.cor[0] = int(attributes['id']) - (self.cor[1] * self.columns)
				if self.tileset:
					if self.gid in self.tileset: do = True
					elif self.gid in [i['TILE'] + self.first for t in self.tilani for i in self.tilani[t]]: do = True
					else: do = False
				else: do = True
				if do:
					lid = int(attributes['id'])
					rct = (self.cor[0] * self.tilewidth,self.cor[1] * self.tileheight,self.tilewidth,self.tileheight)
					self.tiles[self.gid] = {'ID': lid,'GID': self.gid,'IMG': self.img.subsurface(rct).copy(),'MASK': (0,0,self.tilewidth,self.tileheight),'ANIMATION': [],
						'DEPTH': 0,'DIRECTION': 3,'SPEED': 2,'TIME': 120}
					for x in attributes.items(): self.tiles[self.gid][x[0].upper()] = x[1]
			else: print(dtb.ERROR['img_noload'])
		if tag == 'properties': self.tilprp = {}
		if tag == 'property': self.tilprp[attributes['name']] = attributes['value']

		if self.tileset:
			if self.gid in self.tileset: do = True
			else: do = False
		else: do = True
		if do:
			if tag == 'animation':
				if 'tile' in attributes.keys(): self.gid = int(attributes['tile']) + self.first
				self.tilani[self.gid] = []
			if tag == 'frame':
				if 'tileid' in attributes.keys():
					self.tilani[self.gid].append({'TILE': int(attributes['tileid']),'DURATION': int(attributes['duration'])})
				else: self.tilani[self.gid].append({'TILE': int(attributes['tile']),'DURATION': int(attributes['duration'])})
		if tag == 'terrain':
			if 'id' in attributes.keys(): self.terrains[int(attributes['id'])] = {i[0].upper(): i[1] for i in attributes.keys() if i[0] != 'id'}
			else: self.terrains[len(self.terrains)] = {'NAME': attributes['name']}
		self.ind = tag

	def characters(self, content):
		content = content.lower()
		if self.ind == 'terrain' and content:
			tt = content
			for i in ['\n',' ','	',',']:
				tt = tt.replace(i,'')
			self.content += tt

	def endElement(self, tag):
		if self.tileset:
			if self.gid in self.tileset: do = True
			else: do = False
		else: do = True

		if tag == 'tile' and self.gid > 0 and do:
			for i in self.tilprp.items(): self.tiles[self.gid][i[0]] = i[1]
		if tag == 'terrain' and self.content:
			for t in range(len(self.content[::3])):
				self.terrains[len(self.terrains) - 1]['DATA'].append(int(self.content[t * 3:(t + 1) * 3]))
		
		#SET ANIMATION FRAMES
		if tag == 'animation' and do: self.tiles[self.gid]['ANIMATION'] = self.tilani[self.gid]
		if tag == 'tileset':
			for a in self.tilani:
				if self.tileset:
					if a in self.tileset: do = True
					else: do = False
				else: do = True
				if do:
					for f in range(len(self.tilani[a])):
						img = self.tiles[self.tilani[a][f]['TILE'] + self.first]['IMG']
						self.tiles[a]['ANIMATION'][f]['IMG'] = img
		self.ind = ''
	
	def save(self, name=None):
		if self.tileset == None:
			contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
			'<tileset version="1.2" name="{}" first="{}" tilewidth="{}" tileheight="{}" rows="{}" columns="{}">\n'.format(self.name,self.first,self.tilewidth,self.tileheight,self.rows,self.columns)
			contents += ' <img source="{}" width="{}" height="{}" length="{}"/>\n'.format(self.imgpath,self.width,self.height,self.length)
			for i in self.tiles:
				tt = ' <tile id="{}"'.format(self.tiles[i]['ID'])
				for p in self.tiles[i].keys():
					if p not in ['ID','IMG','RECT','ANIMATION','TERRAIN'] and self.tiles[i][p]: tt += ' {}="{}"'.format(p.lower(),self.tiles[i][p])
				contents += tt + '/>\n'
			if self.tilani:
				contents += '\n'
				for i in self.tilani:
					contents += ' <animation tile="{}">\n'.format(i - self.first)
					for f in self.tilani[i]:
						contents += '  <frame tile="{}" duration="{}"/>\n'.format(f['TILE'] - self.first,f['DURATION'])
					contents += ' </animation>\n'
			if self.terrains:
				contents += '\n'
				for i in self.terrains:
					if self.terrains[i]:
						contents += ' <terrain id="{}">\n'.format(i)
						dd = ''
						for d in range(4):
							dd += '			'
							for t in range(4):
								dd += tools.text.digitstring(self.terrains[i][(d * 4) + t],3) + ','
							dd += '\n'
						contents += dd + '		</terrain>\n'
			contents += '</tileset>'
			
			if name: fn = name + '.xml'
			else: fn = self.name
			file = open(res.TILESETS_PATH + fn,'w')
			file.write(contents)
			file.close()
		else: print(dtb.ERROR['tileset_save'])

	def test(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		self.window.fill((100,100,100))
		pos = [0,0]
		for i in self.tiles:
			self.window.blit(self.tiles[i]['IMG'],(pos[0] * self.tilewidth,pos[1] * self.tileheight))
			pos[0] += 1
			if pos[0] >= self.columns:
				pos[0] = 0
				pos[1] += 1
				
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

class MapHandler(xml.sax.ContentHandler):
	def __init__(self,file,testing=False):
		self.name = file
		self.testing = testing
		if self.testing: self.window = pygame.display.set_mode((600,600))
		else: self.window = pygame.Surface((1,1))
		self.vkeyboard = GUI.Vkeyboard(pygame.Rect(0,200,600,400),display=True)
		self.cam = pygame.Rect(0,0,3000,3000)
		self.zoom = 1
		self.rotate = [2,4,0] #isometric
		self.surfaces = [None for i in range(5)]
		self.layers = [[] for i in range(5)]
		self.tileset = []
		self.tilesets = []
		self.tilelist = {}
		self.chunksize = (10,10)
		self.objects = {}
		self.srflvl = 0
		self.current = None
		self.content = ''

		self.enemies = []
		self.habitat = None
		self.interior = 0
		self.hscroll = 0
		self.vscroll = 0
		self.city = 0

		#ENVIROMENT
		self.waterwave = 0
		self.rainimgs = [pygame.image.load(res.TILES_PATH + 'rain_' + str(f) + '.png').convert_alpha() for f in range(3)]
		self.rainimation = 0.0

		#ROGUE
		self.reveal = []
		self.player = [3,4]
		self.hp = 10
		self.enemies = [[1,2],[8,5]]
		self.items = [[1,8]]
		self.inv = []
		
		self.listener = (150,150)
		self.obj = {'PLAYER_0': Character(0,(3 * 30,4 * 30)),'ITEM_0': {'RECT': pygame.Rect(30,8 * 30,25,25)}}
		for x in range(1): self.obj['NPC_' + str(x)] = Character('4.1.1',(x * 30,2 * 30))
		for x in range(1): self.obj['CAR_' + str(x)] = Character('4.1.1',(x * 30,4 * 30))
		self.obj['PLAYER_0'].playing = True
		self.paths = {'SIDEWALK': [],'STREET': [],'CROSSING': []}
		self.traflight = 0

		#STUDIO
		self.edit = True
		self.click = None
		self.stbts = [[pygame.Rect(10 + (x * 35),600 - 50,30,30),0] for x in range(16)]
		self.stbtlyr = [[pygame.Rect(10,10 + (y * 32),60,30),0] for y in range(len(self.layers))]
		self.tool = [0,1,0]
		self.stsrct = pygame.Rect(0,0,0,0)
		self.stlyr = [0,0]
		self.build = ''
		self.hstlst = []
		self.hstidx = 0
		self.clipboard = []
		self.rqst = None

		if file:
			if file.endswith('png'):
				import PIL.Image
				self.pixelmap(PIL.Image.open(res.MAPS_PATH + file))
			else:
				parser = xml.sax.make_parser()
				parser.setFeature(xml.sax.handler.feature_namespaces, 0)
				parser.setContentHandler(self)
				parser.parse(res.MAPS_PATH + file)

	def startElement(self, tag, attributes):
		tag = tag.lower()
		lst = ['floor','walls','ceil']
		if tag == 'map':
			for i in attributes.items():
				if i[0] in ['version','orientation','renderorder']: setattr(self, i[0], i[1])
				else: setattr(self, i[0], int(i[1]))
			self.surfaces = [pygame.Surface((int(attributes['width']) * int(attributes['tilewidth']),int(attributes['height']) * int(attributes['tileheight'])),pygame.SRCALPHA) for i in range(5)]
		if tag == 'property': setattr(self, attributes['name'], attributes['value'])
		if tag == 'tileset':
			dt = {i[0]: i[1] for i in attributes.items()}
			if 'source' in attributes.keys(): dt['src'] = dt['source']
			self.tilesets.append(dt)
		if tag in lst: self.srflvl = lst.index(tag)
		if tag == 'layer':
			dct = {i[0]: i[1] for i in attributes.items()}
			if 'name' not in dct.keys(): dct['name'] = 'layer ' + str(self.srflvl)
			dct['data'] = []
			dct['tiles'] = []
			self.layers[self.srflvl].append(dct)

		#ITEMS
		if tag == 'item':
			sz = [0,0]
			if 'width' in attributes.keys(): sz[0] = int(attributes['width']) * self.tilewidth
			if 'height' in attributes.keys(): sz[1] = int(attributes['height']) * self.tileheight
			obj = {'INDEX': attributes['index'],'RECT': pygame.Rect(int(attributes['x']) * self.tilewidth,int(attributes['y']) * self.tileheight,sz[0],sz[1]),
				'FLOAT': 0,'ACC': 3,'DIRECTION': False,'DESTROY': False}
			if 'ITEMS' not in self.objects.keys(): self.objects['ITEMS'] = []
			self.objects['ITEMS'].append(obj)
		#PORTALS
		if tag == 'portal':
			sz = [0,0]
			g = [int(attributes['gotox']) * self.tilewidth,int(attributes['gotoy']) * self.tileheight]
			if 'width' in attributes.keys(): sz[0] = int(attributes['width']) * self.tilewidth
			if 'height' in attributes.keys(): sz[1] = int(attributes['height']) * self.tileheight
			if 'gotoroom' in attributes.keys(): g.append(attributes['gotoroom'])
			obj = {'RECT': pygame.Rect(int(attributes['x']) * self.tilewidth,int(attributes['y']) * self.tileheight,sz[0],sz[1]),'GOTO': g}
			for i in ['open','close','key']:
				if i in attributes.keys(): obj[i.upper()] = attributes[i]
			if 'PORTALS' not in self.objects.keys(): self.objects['PORTALS'] = []
			self.objects['PORTALS'].append(obj)
		#SIGNS
		if tag == 'sign':
			sz = [0,0]
			if 'width' in attributes.keys(): sz[0] = int(attributes['width']) * self.tilewidth
			if 'height' in attributes.keys(): sz[1] = int(attributes['height']) * self.tileheight
			obj = {'RECT': pygame.Rect(int(attributes['x']) * self.tilewidth,int(attributes['y']) * self.tileheight,sz[0],sz[1]),'TEXT': attributes['text']}
			for i in ['font','size']:
				if i in attributes.keys(): obj[i.upper()] = attributes[i]
			if 'SIGNS' not in self.objects.keys(): self.objects['SIGNS'] = []
			self.objects['SIGNS'].append(obj)
		#ROADPROPS
		if tag == 'roadprop':
			sz = [0,0]
			if 'width' in attributes.keys(): sz[0] = int(attributes['width']) * self.tilewidth
			if 'height' in attributes.keys(): sz[1] = int(attributes['height']) * self.tileheight
			obj = {'RECT': pygame.Rect(int(attributes['x']) * self.tilewidth,int(attributes['y']) * self.tileheight,sz[0],sz[1]),'TYPE': attributes['type']}
			for i in ['price','speed']:
				if i in attributes.keys(): obj[i.upper()] = int(attributes[i])
			if 'ROADPROPS' not in self.objects.keys(): self.objects['ROADPROPS'] = []
			self.objects['ROADPROPS'].append(obj)
		self.current = tag

	def characters(self, content):
		content = content.lower()
		if self.current == "layer" and content:
			tt = content
			for i in ['\n',' ','	',',']:
				tt = tt.replace(i,'')
			self.content += tt
	
	def endElement(self, tag):
		tag = tag.lower()
		lst = ['floor','walls','ceil']

		if tag == 'layer' and self.content:
			ldx = len(self.layers[self.srflvl]) - 1
			for t in range(len(self.content[::3])):
				lid = self.content[t * 3:(t + 1) * 3]
				if int(lid) not in self.tileset: self.tileset.append(int(lid))
				self.layers[self.srflvl][ldx]['data'].append(int(lid))
		if tag == 'map':
			gid = 1
			#GET TILES FROM MAP
			for t in self.tilesets:
				if self.edit: tt = None
				else: tt = self.tileset
				tset = TileHandler(t['src'],tt,gid)
				self.tilelist = {**self.tilelist,**tset.tiles}
				if len(tset.tiles) > 0: gid += tset.length
			for i in range(5):
				for ldx in range(len(self.layers[i])):
					#GET TILE PROPERTIES FROM DATA
					for y in range(int(self.layers[i][ldx]['height'])):
						for x in range(int(self.layers[i][ldx]['width'])):
							t = self.layers[i][ldx]['data'][x + (y * int(self.layers[i][ldx]['height']))]
							if t > 0:
								til = self.tilelist[t].copy()
								til['GIF'] = 0.0
								til['RECT'] = pygame.Rect(x * self.tilewidth,y * self.tileheight,self.tilewidth,self.tileheight)
								self.layers[i][ldx]['tiles'].append(til)
								if til['TYPE'] in ['sidewalk','street','crossing']:
									self.paths[til['TYPE'].upper()].append((til['RECT'].x,til['RECT'].y))
		self.current = None
		self.content = ''

	def pixelmap(self, img):
		for i in {'width': img.size[0],'height': img.size[1],'tilewidth': 32,'tileheight': 32,\
			'orientation': 'isometric','version': '0.1','renderorder': 'right-down'}.items(): setattr(self, i[0], i[1])
		self.surfaces = [pygame.Surface((self.width * self.tilewidth,self.height * self.tileheight),pygame.SRCALPHA) for i in range(5)]
		self.tilesets = [{'name': 'nature','src': 'nature.xml'},{'name': 'streets','src': 'streets.xml'}]
		for i in range(2): self.layers[i].append({'id': 0,'name': 'layer ' + str(i),'width': self.width,'height': self.height,'data': [],'tiles': []})
		
		srf = img.load()
		tiles = {(0,255,0): 1,(0,0,255): 5,(90,90,0): 6,(75,75,75): 20,(150,150,150): 31}
		for y in range(self.width):
			for x in range(self.height):
				tt = srf[x,y][0:3]
				if tt == (90,90,0):
					self.layers[0][0]['data'].append(tiles[tt])
					self.layers[1][0]['data'].append(tiles[tt])
				else:
					self.layers[0][0]['data'].append(tiles[tt])
					self.layers[1][0]['data'].append(0)
				self.tileset.append(tiles[tt])
		self.endElement('map')
		self.save()
	
	def roguemap(self):
		cmd = ''
		msg = ''
		while cmd != 'quit':
			lyr = self.layers[0][0]
			for y in range(lyr['height'] + 1):
				row = ''
				for x in range(lyr['width'] + 1):
					cor = x + int(y * lyr['height'])
					#BORDERS
					if [x,y] == [0,0]: row += '╔'
					elif [x,y] == [lyr['width'],0]: row += '╗'
					elif [x,y] == [0,lyr['height']]: row += '╚'
					elif [x,y] == [lyr['width'],lyr['height']]: row += '╝'
					elif y in [0,lyr['height']]: row += '═'
					elif x in [0,lyr['width']]: row += '║'
					#PLAYER
					if [x,y] == self.obj['PLAYER_0']: row += '@'
					elif cor in self.reveal:
						#OBJECTS
						if [x,y] in self.enemies: row += '∆'
						elif [x,y] in self.items: row += '$'
						#TILES
						elif lyr['data'][cor] == 347: row += '#'
						elif lyr['data'][cor] == 357: row += 'W'
						elif lyr['data'][cor] == 376: row += '+'
						elif lyr['data'][cor] == 379: row += 'O'
						else: row += '·'
					else: row += ' '
				print(row)
			print(msg)
			cmd = input('> ')
			msg = ''
			if 'help' in cmd:
				msg += ' • u: move up\n • d: move down\n • l: move left\n • r: move right\n' \
				+ ' • inv: show inventory\n • restart: restart game\n • quit: exit game'
			else:
				#COMMANDS
				if 'l' in cmd: self.obj['PLAYER_0'].rect.x -= cmd.count('l')
				if 'r' in cmd: self.obj['PLAYER_0'].rect.x += cmd.count('r')
				if 'u' in cmd: self.obj['PLAYER_0'].rect.y -= cmd.count('u')
				if 'd' in cmd: self.obj['PLAYER_0'].rect.y += cmd.count('d')
				for y in [-1,0,1]:
					for x in [-1,0,1]:
						cor = self.obj['PLAYER_0'].rect.x + x + int((self.obj['PLAYER_0'].rect.y + y) * lyr['height'])
						if cor not in self.reveal: self.reveal.append(cor)

				if 'hp' in cmd: msg += 'HP: ' + str(self.hp) + '/10'
				if 'inv' in cmd:
					msg += 'INVENTORY\n'
					if len(self.inv) == 0: msg += ' <empty>'
					for i in self.inv:
						msg += ' • ' + i + '\n'
				if 'restart' in cmd: self.__init__()
				
				#PLAYER INTERACTIONS
				if self.colide(self.obj['PLAYER_0'].rect,self.obj['ENEMY_0'].rect):
					self.hp -= 1
					msg = 'Ouch! =(\n -1 HP'
					if self.hp < 0:
						cmd = 'quit'
				if self.colide(self.obj['PLAYER_0'].rect,self.obj['ITEM_0'].rect):
					self.inv.gui.append('coin')
					del self.obj['ITEM_0']
					msg = 'got item!'
			os.system('cls')
		print('game over')

	def events(self):
		for event in pygame.event.get():
			#TILE OBJECTS
			for i in self.layers[1][0]['tiles']:
				if pygame.Rect.colliderect(i['RECT'],self.cam):
					#BED
					if i['TYPE'] == 'bed':
						#i['RECT'].x = i['RECT'].x + 5
						#i['RECT'].y = i['RECT'].y + 5
						i['SLEEP'] = not i['SLEEP']
						if i['SLEEP'] == False: i['PAUSE'] = 1
						else: i['PAUSE'] = 0
					#TELEPHONE CABINE
					elif i['TYPE'] == 'telephone':
						for m in ['credit_card','wallet']:
							mny = self.guis['INVENTORY'].gui.find(None,m,'value')
						if mny != None and mny[1] > 0:
							res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1] - 1)
							self.dev = self.guis['INVENTORY'].gui.dev('phone')
							self.wait()
							dtb.CALLHIST.insert(0,[dtb.CONTACTS[self.lopt][1],False])
							self.dialog(dtb.DIALOGS[dtb.CONTACTS[self.lopt][1]][0],i['RECT'])
						else:
							self.dialog([dtb.MENU[18]],i['RECT'])
					#BATTERY PLUG
					elif i['TYPE'] == 'battery':
						if self.guis['INVENTORY'].gui.find(res.PARTY[res.FORMATION][0],'charger') != None:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
							bt = self.guis['INVENTORY'].gui.find(None,'phone')
							bt[1] = '3600'
							self.dialog(dtb.DIALOGS['PLUG'][1])
						else: self.dialog(dtb.DIALOGS['PLUG'][0])
					#REFUEL
					elif i['TYPE'] == 'refuel' and p['DRIVING'] != None:
						while res.GAS < self.vehicles[p['DRIVING']]['CAPACITY']:
							res.GAS += 1
							self.run()

			#SAVE AND LOAD FILES
			if self.vkeyboard.active:
				self.vkeyboard.events(event)
				if self.vkeyboard.active == False:
					self.name = self.vkeyboard.output
					if self.rqst == 'load': self.__init__(self.name)
					if self.rqst == 'save': self.save(self.name)
					self.rqst = None
			pressed, self.click = tools.event.get_pressed(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			#KEYBOARD EVENTS
			if self.edit and event.type == pygame.KEYDOWN:
				#ORIENTATION
				if pygame.key.get_pressed()[pygame.K_o]:
					if self.orientation == 'orthogonal': self.orientation = 'isometric'
					elif self.orientation == 'isometric': self.orientation = 'orthogonal'
					for i in self.surfaces: i.fill((0,0,0,0))
			#MOUSE EVENTS
			if self.edit and event.type == pygame.MOUSEBUTTONDOWN and not self.vkeyboard.active:
				#LAYERS
				for i in range(len(self.stbtlyr)):
					self.stbtlyr[i][1] = 0
					if pygame.Rect.colliderect(self.click,self.stbtlyr[i][0]):
						self.stbtlyr[i][1] = 1
						if event.type == pygame.MOUSEBUTTONDOWN:
							if len(self.layers[i]) == 0:
								self.layers[i].append({'id': i,'name': 'layer ' + str(i),'width': self.width,'height': self.height,'data': [],'tiles': []})
							self.stlyr[0] = i
				#TOOLS
				for i in range(len(self.stbts)):
					self.stbts[i][1] = 0
					if pygame.Rect.colliderect(self.click,self.stbts[i][0]):
						self.stbts[i][1] = 1
						if event.type == pygame.MOUSEBUTTONDOWN: self.tool[0] = i
				#SELECT START
				if self.tool[0] in [0,6]:
					self.stsrct.x = int(self.click.x/self.tilewidth) * self.tilewidth
					self.stsrct.y = int(self.click.y/self.tileheight) * self.tileheight
				#CUT AND COPY
				if self.tool[0] in [7,8] and self.stsrct.width > 0 and self.stsrct.height > 0:
					lst = self.layers[self.stlyr[0]][self.stlyr[1]]['tiles']
					for i in range(len(lst)):
						if pygame.Rect.colliderect(lst[i]['RECT'],self.stsrct):
							self.clipboard.append(lst[i])
							if self.tool[0] == 8: lst[i]['RECT'] = pygame.Rect(0,0,0,0)
					self.layers[self.stlyr[0]][self.stlyr[1]]['tiles'] = \
					[i for i in self.layers[self.stlyr[0]][self.stlyr[1]]['tiles'] if i['RECT'] != pygame.Rect(0,0,0,0)]
				#PASTE
				if self.tool[0] == 9:
					self.clipboard = []
				#LOAD FILE
				if self.tool[0] == 10: self.vkeyboard.active = True; self.rqst = 'load'
				#SAVE FILE
				if self.tool[0] == 11: self.vkeyboard.active = True; self.rqst = 'save'
				#UNDO AND REDO
				if self.tool[0] in [12,13]:
					if self.tool[0] == 12 and self.hstidx > 0: self.hstidx -= 1
					if self.tool[0] == 11 and self.hstidx < len(self.hstlst) - 1: self.hstidx += 1
					self.stlyr = self.hstlst[self.hstidx]['LAYER']
					self.layers[self.stlyr[0]][self.stlyr[1]]['tiles'] = self.hstlst[self.hstidx]['TILES']
				#ZOOM
				if self.tool[0] == 14 and self.zoom < 100: self.zoom += 0.2
				if self.tool[0] == 15 and self.zoom > 0: self.zoom -= 0.2
			#OBJECTS
			if self.testing:
				for i in self.obj:
					if i.startswith('ITEM_'): pass
					else: self.obj[i].inside_events(pressed,self.click)
		pressed, self.click = tools.event.get_pressed(None)
		if self.edit and pygame.mouse.get_pressed()[0] and not self.vkeyboard.active:
			lst = self.layers[self.stlyr[0]][self.stlyr[1]]['tiles']
			trct = pygame.Rect(int((self.click.x + self.tilewidth)/self.tilewidth) * self.tilewidth,
				int((self.click.y + self.tileheight)/self.tileheight) * self.tileheight,self.tilewidth,self.tileheight)
			trct = pygame.Rect(int(trct.x/self.zoom),int(trct.y/self.zoom),int(trct.width/self.zoom),int(trct.height/self.zoom))
			
			#SELECT DRAG
			if self.tool[0] in [0,6]:
				self.stsrct.width = trct.x - self.stsrct.x
				self.stsrct.height = trct.y - self.stsrct.y
			#MOVE
			if self.tool[0] == 1:
				self.stsrct.x = trct.x
				self.stsrct.y = trct.y
				for i in range(len(lst)):
					if pygame.Rect.colliderect(lst[i]['RECT'],self.stsrct):
						lst[i]['RECT'].x += lst[i]['RECT'].x - self.stsrct.x
						lst[i]['RECT'].y += lst[i]['RECT'].y - self.stsrct.y
			#PAINT TILES
			if self.tool[0] in [2,3,4,5,6]:
				addtl = self.tilelist[self.tool[1]].copy()
				addtl['RECT'] = trct
				addtl['GIF'] = 0.0
				hstadd = False
				rchk = False
				for i in range(len(lst)):
					#RECT
					if self.tool[0] == 6 and pygame.Rect.colliderect(lst[i]['RECT'],self.stsrct):
						nwrct = lst[i]['RECT'].copy()
						addtl['RECT'] = nwrct
						lst[i] = addtl
					elif lst[i]['RECT'] == trct:
						#PENCIL
						if self.tool[0] == 2: lst[i] = addtl; rchk = True; hstadd = True
						#ERASE
						if self.tool[0] == 3: lst[i]['RECT'] = pygame.Rect(0,0,0,0); hstadd = True
						#PICK
						if self.tool[0] == 4: self.tool[1] = lst[i]['GID']
						#FILL
						if self.tool[0] == 5: hstadd = True
				if self.tool[0] == 2 and rchk == False: lst.append(addtl)
				#HISTORY
				if hstadd:
					#LIST BY DEPTH
					#lst = {y[0]: y[1] for y in {i[0]: i[1]['RECT'].y for i in lst.items()}.sort()}

					addhst = {'TYPE': 'PAINT','LAYER': self.stlyr,'TILES': lst}
					if self.hstidx < len(self.hstlst) - 1: self.hstlst[self.hstidx] = addhst
					else: self.hstlst.append(addhst)
					self.hstidx += 1
					if self.hstidx > 50: self.hstlst = self.hstlst[1:51]; self.hstidx = 50
			lst = [i for i in lst if i['RECT'] != pygame.Rect(0,0,0,0)]
			self.layers[self.stlyr[0]][self.stlyr[1]]['tiles'] = lst
		#OBJECTS
		if self.testing:
			for i in self.obj:
				if i.startswith('ITEM_'): pass
				else: self.obj[i].outside_events(pressed)
	
	def colision(self,rect,layer):
		offset = (0,0)
		tile = None
		for lyr in self.layers[layer]:
			chunk = []
			for y in range(self.width):
				for x in lyr['tiles'][offset[0] * y:(offset[0] + self.chunksize[0]) * y]:
					chunk.append(x)
			for l in chunk:
				if pygame.Rect.colliderect(rect,l['RECT']):
					#COLOR TILES
					if l['TYPE'] == 'COLOR':
						if l['SCALE'] == 30 and l['COLOR'] > 0:
							#self.dmg.append({'INFO': pygame.Surface((43,40), pygame.SRCALPHA, 32), 'TYPE': 2,
							#'TEXT': '10','RECT': pygame.Rect(i['RECT'].x, i['RECT'].y,1,1),
							#'GRAVITY': -8, 'SHADE': 1, 'SHAKE': 0, 'COLOR': (200,200,200), 'ALPHA': 250, 'TIME': 10})
							res.CHARACTERS[0]['SCORE'] += 10
							l['COLOR'] -= 1
							l['SCALE'] = 0
							#self.audioedit(res.SOUND['STEP_COLOR'],'pitch',t[0]['COLOR'])
							res.MIXER[2].play(res.SOUND['STEP_COLOR'])
						else: res.MIXER[2].play(res.SOUND['STEP_BRICK'])
					#REGULAR COLISION
					elif res.MIXER[2].get_busy() == False: res.MIXER[2].play(res.SOUND['STEP_' + l['STEP'].upper()])
					tile = l.copy()
		return tile

	def save(self, name=None):
		#SAVE LAYERS DATA
		for lyr in range(len(self.layers)):
			for sublyr in range(len(self.layers[lyr])):
				for tl in range(len(self.layers[lyr][sublyr]['tiles'])):
					self.layers[lyr][sublyr]['data'][tl] = self.layers[lyr][sublyr]['tiles'][tl]['GID']
		#SAVE MAP PROPERTIES
		contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
		'<map version="{}" orientation="{}" renderorder="{}" width="{}" height="{}" '.format(self.version,self.orientation,self.renderorder,self.width,self.height)
		contents += 'tilewidth="{}" tileheight="{}" infinite="0">\n'.format(self.tilewidth,self.tileheight)
		#SAVE TILE SETS
		for i in self.tilesets: contents += '	<tileset name="{}" src="{}"/>\n'.format(i['name'],i['src'])
		#SAVE TILE LAYERS
		lst = ['floor','walls','ceil']
		for l in range(len(lst)):
			if len(self.layers[l]) > 0:
				contents += '	<{}>\n'.format(lst[l])
				for i in self.layers[l]:
					exprp = ''
					for p in ['offsetx','offsety']:
						if p in i.keys(): exprp += ' {}="{}"'.format(p,i[p])
					contents += '		<layer id="{}" width="{}" height="{}"{}>\n'.format(i['id'],i['width'],i['height'],exprp)
					dd = ''
					for d in range(len(i['data'][::int(i['width'])])):
						dd += '			'
						for t in range(int(i['width'])):
							dd += tools.text.digitstring(i['data'][(d * int(i['width'])) + t],3) + ','
						dd += '\n'
					contents += dd + '		</layer>\n'
				contents += '	</{}>\n'.format(lst[l])
		
		#SAVE OBJECTS
		lst = ['ITEMS','PORTALS','SIGNS','ROADPROPS']
		if len(self.objects) > 0:
			contents += '	<objects>\n'
			for o in lst:
				for i in self.objects[o]:
					prp = 'x="{}" y="{}"'.format(int(i['RECT'].x/self.tilewidth),int(i['RECT'].y/self.tileheight))
					if i['RECT'].width > 0: prp += ' width="{}"'.format(int(i['RECT'].width/self.tilewidth))
					if i['RECT'].height > 0: prp += ' height="{}"'.format(int(i['RECT'].height/self.tileheight))
					if o == 'PORTALS':
						prp += ' gotox="{}" gotoy="{}"'.format(int(i['GOTO'][0]/self.tilewidth),int(i['GOTO'][1]/self.tileheight))
						if len(i['GOTO']) > 2: prp += ' gotoroom="{}"'.format(i['GOTO'][2])
					for p in i.keys():
						if p not in ['RECT','GOTO','FLOAT','ACC','DESTROY']: prp += ' {}="{}"'.format(p.lower(),i[p])
					contents += '		<{} {}/>\n'.format(o[:-1].lower(),prp)
			contents += '	</objects>\n'
		contents += '</map>'

		if name: fn = name
		else: fn = self.name
		print('salvo em :' + self.name)
		file = open(res.MAPS_PATH + fn,'w')
		file.write(contents)
		file.close()
		
	def draw(self):
		for i in self.surfaces: i.fill((0,0,0,0))
		for lyr in range(len(self.layers)):
			for l in self.layers[lyr]:
				for i in l['tiles']:
					if pygame.Rect.colliderect(i['RECT'],self.cam):
						if 'offsetx' in l.keys(): cor = (int(l['offsetx']) * self.tilewidth,int(l['offsety']) * self.tileheight)
						else: cor = (0,0)
						#ANIMATION
						if len(i['ANIMATION']) > 0:
							img = i['ANIMATION'][np.floor(i['GIF']).astype(int)]['IMG']
							i['GIF'] += 0.05
							if i['GIF'] > len(i['ANIMATION']): i['GIF'] = 0.0
						else: img = i['IMG']

						#FALLING TILES
						if i['TYPE'] == 'fall': i['DEPTH'] += 1
						#MOVING PLATFORMS
						if i['TYPE'] == 'moving':
							lst = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
							if i['DIRECTION']:
								i['RECT'].x += lst[i['DIRECTION'] - 1][0] * i['SPEED']
								i['RECT'].y += lst[i['DIRECTION'] - 1][1] * i['SPEED']
							i['TIME'] -= 2
							if i['TIME'] < 0:
								if i['DIRECTION'] == 3: i['DIRECTION'] = 7
								elif i['DIRECTION'] == 7: i['DIRECTION'] = 3
								i['TIME'] = 120
						#WATERWAVES
						wvsz = 4 #size of waterwave in tiles
						if i['TYPE'] == 'water': ww = np.sin(int(self.waterwave - (wvsz * int(i['RECT'].y/self.tileheight))))
						else: ww = 0

						if self.orientation == 'orthogonal':
							self.surfaces[lyr].blit(img,(i['RECT'].x + cor[0],i['RECT'].y + cor[1] + ww))
						if self.orientation == 'isometric':
							offset = [(self.width * int(self.tilewidth/2)) - int(self.tilewidth/2),0]
							cc = [i['RECT'].x,i['RECT'].y]
							cor = (offset[0] + int((cc[0] - cc[1])/np.floor(self.rotate[0]).astype(int)),
								offset[1] + int((cc[0] + cc[1])/np.floor(self.rotate[1]).astype(int)) + i['DEPTH'] - (lyr * int(self.tileheight/2)) - ww)
							#REFLEXIONS
							srf = pygame.transform.flip(img,0,0)
							self.surfaces[lyr].blit(srf,(cor[0],cor[1] + ((lyr + 1) * int(self.tileheight/2))))
							#REGULAR DRAW
							self.surfaces[lyr].blit(img,cor)
							#SHADOWS
							if lyr > 1:
								srf = pygame.Surface((self.tilewidth,self.tileheight),pygame.SRCALPHA)
								pygame.draw.polygon(srf,(10,10,10),((int(self.tilewidth/2),0),(self.tilewidth,int(self.tileheight/4)),(int(self.tilewidth/2),int(self.tileheight/2)),(0,int(self.tileheight/4))))
								aa = int(100/lyr)
								if aa > 0: srf.set_alpha(aa)
								self.surfaces[lyr].blit(srf,(cor[0],cor[1] + (lyr * int(self.tileheight/2))))
		#RAINING
		if res.WEATHER and self.orientation == 'isometric':
			for lyr in range(8):
				for y in range(self.height):
					for x in range(self.width):
						img = self.rainimgs[np.floor(self.rainimation).astype(int)]
						self.rainimation += 0.05
						if self.rainimation > 3: self.rainimation = 0.0

						cc = [x * self.tilewidth,y * self.tileheight]
						offset = [(self.width * int(self.tilewidth/2)) - int(self.tilewidth/2),0]
						cor = (offset[0] + int((cc[0] - cc[1])/np.floor(self.rotate[0]).astype(int)),
							offset[1] + int((cc[0] + cc[1])/np.floor(self.rotate[1]).astype(int)))
						self.surfaces[0].blit(img,(cor[0],cor[1] - ((lyr + 1) * int(self.tileheight/2))))
		
		if self.orientation != 'isometric': yy = 0
		else: yy = int((self.height * self.tileheight)/4)
		offset = (int(600/2) - int((self.width * self.tilewidth)/2),int(600/2) - int((self.height * self.tileheight)/2) + yy)
		for i in self.surfaces:
			if self.zoom != 1: i = pygame.transform.scale(i,(int(i.get_width() * self.zoom),int(i.get_height() * self.zoom)))
			self.window.blit(i,offset)
		self.waterwave += 0.1
		#try to mess around ;)
		#self.zoom[0] += 0.2
		#self.zoom[1] += 0.2

		#DISPLAY HOVER TILE
		if self.testing:
			trct = pygame.Rect(offset[0] + (int((self.click.x + self.tilewidth)/self.tilewidth) * self.tilewidth),
				offset[1] - yy + (int((self.click.y + self.tileheight)/self.tileheight) * self.tileheight),self.tilewidth,self.tileheight)
			trct = pygame.Rect(int(trct.x/self.zoom),int(trct.y/self.zoom),int(trct.width/self.zoom),int(trct.height/self.zoom))
			if self.colision(trct,0): cl = (200,0,0)
			else: cl = (0,0,0)
			pygame.draw.rect(self.window,cl,trct,3)

		self.traflight += 1
		if self.traflight > 240: self.traflight = 0
		
		if self.orientation == 'orthogonal':
			for i in self.paths['SIDEWALK']: pygame.draw.rect(self.window,(100,100,200),pygame.Rect(i[0] + offset[0],i[1] + offset[1],self.tilewidth,self.tileheight),2)
			for i in self.paths['STREET']: pygame.draw.rect(self.window,(200,100,100),pygame.Rect(i[0] + offset[0],i[1] + offset[1],self.tilewidth,self.tileheight),2)
			for i in self.paths['CROSSING']:
				if self.traflight < 120: pygame.draw.rect(self.window,(200,100,100),pygame.Rect(i[0] + offset[0],i[1] + offset[1],self.tilewidth,self.tileheight),2)
				else: pygame.draw.rect(self.window,(100,100,200),pygame.Rect(i[0] + offset[0],i[1] + offset[1],self.tilewidth,self.tileheight),2)
		#lst = [self.npcs,self.cars]
		lst = []
		rr = 100
		#pygame.draw.circle(self.window,(200,200,200),self.listener,5)
		#pygame.draw.circle(self.window,(200,200,200),(self.listener[0],self.listener[1]),rr,2)
		for l in range(len(lst)):
			for i in range(len(lst[l])):
				rct = lst[l][i]['RECT']
				cl = [(100,100,200),(200,100,100)]
				#pygame.draw.ellipse(self.window,cl[l],rct)
				#pygame.draw.circle(self.window,cl[l],(rct.x,rct.y),rr,2)

				chk = []
				cors = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
				for c in range(len(cors)):
					if lst[l][i]['DIRECTION'] == c + 1: rct.x += cors[c][0] * 0.5; rct.y += cors[c][1] * 0.5
					chk.append([rct.x + (cors[c][0] * 30),rct.y + (cors[c][1] * 30)])

				#SOUND
				snd = res.SOUND['STEP_MOTOR']
				#dst = np.hypot(*(self.listener[0] - rct.x,self.listener[1] - rct.y))
				cor = abs(self.listener[0] - rct.x) - abs(self.listener[1] - rct.y)

				cor = [(rct.x + rr,rct.y + rr),

					(self.listener[0] + rr,self.listener[1] + rr)]
				rng = self.listener[0] + rr
				#if dst > 0: dst = 2/dst
				#snd.set_volume(dst)
				#if self.sfx.get_busy() == False: self.sfx.play(snd)
				#self.window.blit(res.FONTS['DEFAULT'].render(str(rng)[0:4],True,(10,10,10)),(rct.x,rct.y))
				#pygame.draw.line(self.window,(10,10,10),(rct.x,rct.y),cor[0],3)

				if l == 0: ls = self.paths['STREET']; eq = 'self.traflight < 120'
				else: ls = self.paths['SIDEWALK']; eq = 'self.traflight >= 120'
				ntil = [cor for x in ls for cor in range(len(chk)) if x[0] == int(chk[cor][0]/self.tilewidth) * self.tilewidth and x[1] == int(chk[cor][1]/self.tileheight) * self.tileheight]
				if eval(eq): ntil += [x for x in self.paths['CROSSING'] for cor in chk if x[0] == int(cor[0]/self.tilewidth) * self.tilewidth and x[1] == int(cor[1]/self.tileheight) * self.tileheight]
				dirs = [x for x in [1,3,5,7] if x not in ntil]
				if len(dirs) == 0: lst[l][i]['DIRECTION'] = 0
				elif lst[l][i]['DIRECTION'] not in dirs: lst[l][i]['DIRECTION'] = dirs[np.random.randint(0,len(dirs) - 1)]

		'''#SKY
			if len(self.tilmap) > 2:
				tt = (res.TIME[0] * 60) + res.TIME[1]
				img = self.tilmap[3][0]
				self.surfaces[0].blit(img, (0, -int(tt * ((img.get_height() - (img.get_height()/self.display.height))/1440))))
				if len(self.tilrect) > 5:
					for i in range(2):
						aa = ((tt)/240) + 2 + (i * 3)
						xx = int(np.cos(aa) * 100) + int(self.display.width/2)
						yy = int(np.sin(aa) * 100) + int(self.display.height/2)
						if i == 0: frm = 0
						else: frm = res.DATE[4]
						self.surfaces[0].blit(self.tilrect[6][0][0]['IMAGE'][frm],(xx,yy))	
			#PARALLAX SCROLLING
			px = 2
			for t in self.tilmap[4:]:
				if len(t) > 0: self.surfaces[0].blit(t[np.floor(self.tilemation)], (-np.floor(self.cam.x/px), -np.floor(self.cam.y/px)))
				px += 3'''
		'''
		if self.map and len(self.tilrect) > 3:
				if self.tilhide == False and self.tilalpha > 0: self.tilalpha -= 20
				if self.tilhide and self.tilalpha < 255: self.tilalpha += 20
				if self.tilalpha < 0: self.tilalpha = 0
				if self.tilalpha > 255: self.tilalpha = 255
				al = 255 - self.tilalpha
				for i in self.tilrect[4]:
					srf = pygame.Surface((i[1].width,i[1].height))
					if i[0].endswith('ON') and al > 0: srf.set_alpha(al); srf.fill((0,0,0)); self.surfaces[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
					if i[0].endswith('OFF') and self.tilalpha > 0: srf.set_alpha(self.tilalpha); srf.fill((0,0,0)); self.surfaces[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
			'''

		'''
		#REGULAR GROUND
		self.surfaces[0].blit(self.tilmap[0][np.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
		if len(self.tilmap[1]) > 0: self.display[0].blit(self.tilmap[1][np.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
		#MIRROR SURFACES
		for i in self.tilrect[5]:
			self.display[0].blit(i[0],(i[1].x - self.cam.x, i[1].y - self.cam.y))
			if self.rectdebug: pygame.draw.rect(self.display[0],(0,0,255),pygame.Rect(i[1].x - self.cam.x,i[1].y - self.cam.y,i[1].width,i[1].height),3)
		
			if res.MAP != 'rodoviary':
				if self.turn != -6 and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] != 12:
					if len(self.tilmap) > 1: self.display[0].blit(self.tilmap[2][np.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
			else:
				self.bbg['X'] += 0.2
				if np.floor(self.bbg['X']) > (self.map.width * self.map.tilewidth): self.bbg['X'] = 0.0
				self.display[0].blit(self.tilmap[2][np.floor(self.tilemation)], (np.floor(self.bbg['X']) - self.cam.x, -self.cam.y))
				self.display[0].blit(self.tilmap[2][np.floor(self.tilemation)], (np.floor(self.bbg['X']) - (self.map.width * self.map.tilewidth) - self.cam.x, -self.cam.y))
				for t in self.tilrect[4 + np.floor(self.tilemation)]:
					if self.colide(t[1],self.cam): self.display[0].blit(t[2], (t[1].x - self.cam.x, t[1].y - self.cam.y))
		'''

		#STUDIO
		if self.edit:
			stt = None
			#LAYERS BUTTONS
			for i in range(len(self.stbtlyr)):
				if self.stlyr[0] == i: col = res.COLOR
				else: col = (200,200,200)
				if self.stbtlyr[i][1] == i: xx = 5
				else: xx = 0
				pygame.draw.rect(self.window,col,pygame.Rect(self.stbtlyr[i][0].x,self.stbtlyr[i][0].y,self.stbtlyr[i][0].width + xx,self.stbtlyr[i][0].height))
				if len(self.layers[i]) > 0: self.window.blit(res.FONTS['DEFAULT'].render(self.layers[i][0]['name'],True,(10,10,10)),(self.stbtlyr[i][0].x + 5,self.stbtlyr[i][0].y + 5))
			#TOOLS BUTTONS
			lst = ['select','transform','pencil','erase','pick','fill','rect','cut','copy','paste','load','save','undo','redo','zoomin','zoomout']
			for i in range(len(self.stbts)):
				if self.tool[0] == i: col = res.COLOR
				else: col = (200,200,200)
				if self.stbts[i][1]: yy = 5; stt = i
				else: yy = 0
				pygame.draw.rect(self.window,col,self.stbts[i][0])
				self.window.blit(pygame.image.load(res.SPRITES_PATH + 'guit_' + lst[i] + '.png'),(self.stbts[i][0].x,self.stbts[i][0].y - yy))
			#VKEYBOARD
			if self.vkeyboard.active: self.window.blit(self.vkeyboard.draw(),(self.vkeyboard.rect.x,self.vkeyboard.rect.y))

			if stt != None: self.window.blit(res.FONTS['DEFAULT'].render(dtb.MAPTOOLS[lst[stt]][0] + ': ' + dtb.MAPTOOLS[lst[stt]][1],True,(10,10,10)),(10,580))
			if self.stsrct.width > 0 and self.stsrct.height > 0: pygame.draw.rect(self.window,res.COLOR,self.stsrct,3)
			
	def run(self):
		self.events()
		self.window.fill((100,100,100))
		self.draw()
		for i in self.obj:
			if i.startswith('PLAYER_'): do = True
			elif i.startswith('NPC_'): do = True
			elif i.startswith('CAR_'): do = True
			else: do = False
			if do:
				obj = self.obj[i]
				if obj.doll: img = obj.doll.spaceship()
				if self.orientation == 'orthogonal':
					cor = (obj.rect.x - int(obj.sprite.get_width()/2),obj.rect.y - int(obj.sprite.get_height()/2))
				else:
					offset = [(self.width * int(self.tilewidth/self.rotate[0])) - int(self.tilewidth/2),(self.height * int(self.tileheight/self.rotate[1])) - int(self.tileheight/2)]
					cor = (offset[0] + int((obj.rect.x - obj.rect.y)/np.floor(self.rotate[0]).astype(int)),
						offset[1] + int((obj.rect.x + obj.rect.y)/np.floor(self.rotate[1]).astype(int)) - (obj.depth * int(self.tileheight/2)))
							
				self.window.blit(obj.sprite,cor)
					
		if res.MOUSE == 1 and self.click: self.window.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'),(self.click.x,self.click.y))
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

class Dialog(xml.sax.ContentHandler):
	def __init__(self,key,file='dialogs',testing=False):
		self.testing = testing
		self.inv = GUI.Inventory((0,0),0)
		self.parent = None
		if self.testing: self.window = pygame.display.set_mode((600,700))
		else: sz = pygame.display.Info(); self.window = pygame.Surface((sz.current_w,sz.current_h),pygame.SRCALPHA)

		self.bxsize = 50
		self.bxmargin = self.bxsize + 20
		self.iblk = 0

		self.key = key
		self.file = file
		self.scene = 0
		self.current = ''
		self.content = ''
		self.emote = None
		self.text = ['']
		self.choices = []
		self.idx = 0
		self.stidx = 0
		self.speaker = False
		self.rects = []
		self.optrects = []
		self.opt = None
		self.scroll = 0
		self.read = False
		self.speed = res.SPEED
		self.shake = False
		self.task = 0
		self.censor = 0
		self.voice = 1
		self.curfnt = 'DEFAULT'
		self.type = res.DTYPE
		self.chapter = None

		if key in ['chat','CHAT']:
			self.read = True
			self.text = res.CHAT.copy()
			for i in range(len(self.text)):
				sz = res.FONTS[self.curfnt].size(self.text[i])[0] + 10
				self.rects.append(pygame.Rect(30,200 + (i * self.bxmargin),sz,self.bxsize))
			self.idx = len(res.CHAT) - 1
			while True: self.test()
		elif key in ['debug','DEBUG']: pass
		elif testing: self.start()

	def start(self):
		self.rects.append(pygame.Rect(30,200,0,self.bxsize))
		parser = xml.sax.make_parser()
		parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		parser.setContentHandler(self)
		parser.parse('databases/{}_{}.xml'.format(self.file,res.LANG))

	def startElement(self, tag, attributes):
		tag = tag.lower()
		if tag == 'dialog' and attributes['key'] == self.key:
			if 'scenes' in attributes.keys(): self.scene = 1
			else: self.read = True

		#DIALOG SAVING AND SCENES
		if tag == 'scene' and self.scene == 1:
			if 'id' in attributes.keys(): sid = int(attributes['id'])
			else: sid = 0
			if self.key not in res.DLGSAV: res.DLGSAV[self.key] = sid
			if res.DLGSAV[self.key] == sid: self.read = True
		if self.read:
			#DIALOG SETTINGS
			if tag == 'voice': self.voice = int(attributes['value'])
			if tag == 'type': self.type = attributes['value']
			if tag == 'font': self.font = attributes['value']
			if tag in ['shk','shake']: self.shake = True

			if len(self.choices) > 0: txt = self.choices[len(self.choices)-1]
			else: txt = self.text

			#PROLOGUE AND EPILOGUE
			if tag == 'prologue':
				pygame.mixer.music.pause()
				res.MIXER[0].play(res.SOUND['BAUM'])
				for i in range(100): self.chapter = res.CHAPTER; self.run()
				self.chapter = None
				pygame.mixer.music.unpause()

			#TALK BALLONS
			if tag in ['spk','speaker','answer']: self.speaker = not self.speaker
			if tag in ['br','input','spk','answer','get']:
				if tag in ['input','answer'] and len(self.choices) == 0:
					self.iblk = 1
					while tools.event.wait(): self.run()
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					self.iblk = 0
				self.idx += 1
				txt.append('')
				if len(self.choices) == 0: self.rects.append(pygame.Rect(30,200 + (self.idx * self.bxmargin),0,self.bxsize))
			if tag == 'option':
				if 'text' in attributes.keys():
					if len(self.choices) == 0:
						self.opt = 0
						self.stidx = self.idx + 1
					self.idx = 0
					sz = res.FONTS[self.curfnt].size(attributes['text'])[0] + 10
					self.optrects.append(pygame.Rect(self.window.get_width() - 30 - sz,200 + ((self.stidx + len(self.choices)) * self.bxmargin),sz,self.bxsize))
					self.choices.append([attributes['text'],''])
					self.idx += 1

			#MOVE THROUGH DIALOG
			if tag in ['sleep','input','answer','spk'] and 'time' in attributes.keys():
				for i in range(int(attributes['time'])): self.run()
			if tag == 'go': self.idx += 1
			if tag == 'return': self.idx = self.stidx
			if tag in ['jump','jmp']:
				if self.key not in res.DLGSAV: res.DLGSAV[self.key] = 0
				if 'scene' in attributes.keys(): res.DLGSAV[self.key] = int(attributes['scene'])
				else: res.DLGSAV[self.key] += 1
				self.scene = 2
			if tag in ['cls','clear']: self.idx = 0; self.text = ['']; self.scroll = 0; self.rects = [pygame.Rect(30,200,0,50)]

			#GET AND CHANGE VARIABLES
			if tag == 'get' and len(self.choices) > 0:
				if 'map' in attributes.keys(): res.MAP = attributes['map']
				if 'time' in attributes.keys(): res.TIME[0] += int(attributes['time'])
				if 'date' in attributes.keys(): res.DATE[0] += int(attributes['date'])
				if 'item' in attributes.keys():
					self.inv.add(0,attributes['item'])
					res.MIXER[0].play(res.SOUND['ITEM_GET'])
				if 'money' in attributes.keys():
					res.MIXER[0].play(res.SOUND['CASH_GET'])
				if 'ethic' in attributes.keys(): res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += int(attributes['ethic'])
				if 'relation' in attributes.keys(): res.RELATIONS[res.PARTY[res.FORMATION][0]][0] += int(attributes['relation'])
				if ['strenght','agility','resistance','knowledge','charsisma'] in attributes.keys(): 
					res.MIXER[0].play(res.SOUND['ATTRIBUTE_GAIN'])
					if attributes['index'] in dtb.FREAKS.keys(): pass#enemies var[attributes['index']] += int(attributes['value'])
					else: res.CHARACTERS[res.PARTY[res.FORMATION][int(attributes['index'])]] += int(attributes['value'])
					self.hitisplay(0, self.aim, '+' + str(txt[tid][2]) + ' ' + dtb.PROFNAMES[attributes[''].upper()].lower(), (20, 200, 20))
			if tag == 'queue': pass#self.main.waitlst.append([attributes['type'],self.waitime + int(attributes['time']),attributes['who']])

			#ADD AND CHANGE TEXT
			if tag == 'add':
				cc = ''
				if attributes['type'] == 'name': cc += dtb.NAMES[int(attributes['value']) * 2]
				if attributes['type'] == 'time':
					if res.TIME[0] < 18: add = 'good afternoon'
					elif res.TIME[0] >= 6: add = 'good morning'
					else: add = 'good evening'
					cc += dtb.DTALKS[add]
				if attributes['type'] == 'pronoun': cc += dtb.DTALKS[res.CHARACTERS[res.PARTY[res.FORMATION][0]]['PRONOUN'] + '1']
				if attributes['type'] == 'deaths': cc += str(res.CHARACTERS[res.PARTY[res.FORMATION][0]]['DEATHS'])
				if 'ckey' in attributes: cc += pygame.key.name(res.ACTIONS[0][int(attributes['ckey'])])
				self.characters(cc)
			if tag == 'name': self.characters(dtb.NAMES[int(attributes['value']) * 2])
			if tag == 'task':
				'''if res.TASKS[int(attributes['index'])][1] == 100: self.task = 1
				else: self.task = 2'''
				pass
			if tag == 'if':
				add = False
				if 'ethic' in attributes.keys() and res.CHARACTERS[res.PARTY[res.FORMATION][0]] >= int(attributes['ethic']): add = True
				if 'relation' in attributes.keys() and res.RELATIONS[res.PARTY[res.FORMATION][0]][0] >= int(attributes['relation']): add = True
				if 'char' in attributes.keys() and int(attributes['char']) in res.PARTY[res.FORMATION]: add = True
				if 'char' in attributes.keys() and int(attributes['char']) in res.PARTY[res.FORMATION]: add = True
			if tag == 'chance':
				self.choices.append([attributes['text'],''])
				prb = np.random.randint(0,100)
				for i in txt[tid][1:]:
					if prb > i[0] - 100:
						txt.insert(tid + 1, i[1:])
			if tag in ['censor','censorship']:
				if res.CENSORSHIP:
					if 'alt' in attributes.keys(): txt[self.idx] = attributes['alt']; self.censor = 1
					else: self.censor = 2
			if tag == 'insert': self.__init__(attributes['index'],None)

			#RESOURCES
			if tag == 'play':
				lp = 0
				if 'loop' in attributes.keys(): lp = attributes['loop']
				if attributes['src'] in res.SOUND:
					res.MIXER[0].play(res.SOUND[attributes['src']],lp)
				else:
					pygame.mixer.music.load(res.MUSIC_PATH + attributes['src'] + '.mp3')
					pygame.mixer.music.play(-1)

			#GUIS AND DATA
			if tag == 'gui': self.callback = attributes['value']
			if tag == 'mail':
				res.MIXER[0].play(res.SOUND['NOTIFICATION'])
				res.INBOX.append(attributes['index'])
				res.inbx_save(len(res.INBOX)-1,0)
				#self.notification.append({'TEXT': dtb.MENU['not_email'], 'COLOR': (255, 221, 0), 'HALIGN': 'left','X': 0})
			if tag == 'contact':
				res.MIXER[0].play(res.SOUND['NOTIFICATION'])
				dtb.CONTACTS.append(dtb.NUMBERS[attributes['index']].copy())
				dtb.call_save(len(dtb.CONTACTS)-1)
				#self.notification.append({'TEXT': dtb.MENU['not_contact'], 'COLOR': (165, 255, 0), 'HALIGN': 'left','X': 0})
			if tag == 'achievement':
				res.MIXER[0].play(res.SOUND['ACHIEVEMENT'])
				dtb.ACHIEVEMENTS[int(attributes['index'])][2] = True
				#self.notification.append({'TEXT': dtb.ACHIEVEMENTS[txt[tid][1]][0], 'COLOR': (255, 191, 0), 'HALIGN': 'right','X': 0})
		self.current = tag

	def characters(self, content):
		if len(self.choices) > 0: txt = self.choices[len(self.choices)-1]
		else: txt = self.text

		for i in ['\n','\t']: content = content.replace(i,'')
		if self.current == 'cc' and not res.CC: content = False
		if self.read and content:
			wrp = tools.text.wrap([content],res.FONTS[self.curfnt],self.window.get_width() - 40)
			for tt in [i[1:] for i in wrp]:
				#ADDING OPTIONS
				if len(self.choices) > 0: self.choices[-1][self.idx] += tt
				#NORMAL DIALOG
				else:
					#SOUND
					snd = False
					if res.TTS: plyer.tts.speak(tt)
					if snd: res.MIXER[0].play(res.SOUND['TTS' + str(self.voice)])
					for i in range(len(tt)):
						if not res.TTS and not snd: res.MIXER[0].play(res.SOUND['TEXT_INPUT'])
						#EMOTICONS
						if self.emote != None:
							self.emote += tt[i]
							if tt[i] == ':': pass#character show emote ballon
						elif tt[i] == ':': self.emote = ''

						#TEXT ADAPTATIONS
						if self.censor == 2 and tt[i]:
							if tt[i] == ' ': txt[self.idx] += ' '
							elif res.CENSORSHIP == 1: txt[self.idx] += '*'
							else: lst = '@#%$*&'; txt[self.idx] += lst[np.random.randint(0,len(lst)-1)]
						elif self.censor == 0: txt[self.idx] += tt[i]
						if res.DISLEXIC: txt[self.idx] += ' '

						halign = 60
						if self.speaker: halign = self.window.get_width() - res.FONTS[self.curfnt].size(self.text[self.idx])[0]
						self.rects[-1].x = halign - 30
						self.rects[-1].width = res.FONTS[self.curfnt].size(self.text[self.idx])[0] + 10
						self.run()
					if len(wrp) > 1:
						self.idx += 1
						txt.append('')
						self.rects.append(pygame.Rect(30,200 + (self.idx * self.bxmargin),0,self.bxsize))

	def endElement(self, tag):
		if tag == 'data' and self.text == ['']: print(dtb.ERROR['dialog_key'] + self.key)
		if self.read:
			if tag == 'dialog': self.read = False
			if tag == 'scene' and self.scene: self.read = False
			if tag in ['shk','shake']: self.shake = False
			if tag in ['censor','censorship']: self.censor = 0
			#SELECT OPTION
			if len(self.choices) > 0:
				if tag == 'option' and self.choices[-1][-1] == '': del self.choices[len(self.choices)-1][-1]
				if tag == 'select':
					while tools.event.wait(): self.run()
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					lst = self.choices[self.opt][1:].copy()
					self.idx = self.stidx + 1
					self.text.append(self.choices[self.opt][0])
					self.text.append('')
					self.rects.append(self.optrects[0])
					self.rects.append(pygame.Rect(30,200 + (self.idx * self.bxmargin),0,self.bxsize))
					self.choices = []
					self.optrects = []
					self.opt = None
					for i in lst: self.characters(i)
		self.current = ''
	
	def dialog(self, txt, wh=0):
		self.dlg = {'CAMERA': 0}
		self.player[0]['PAUSE'] = 1
		self.player[0]['SPEED'] = 0
		while tid < len(txt):
			#TEXT
			if isinstance(txt[tid], str):
				while self.dlg['FADE'] > 0:
					if self.winbar < 50 and self.battle == False:
						self.winbar += 5
					self.dlg['FADE'] -= 50
					self.run(False)
			#DIALOG PROTOCOLS
			else:
				#CHAPTER END
				if txt[tid] in [4,5]:
					pygame.mixer.stop()
					self.player[0]['PAUSE'] = 3
					res.MIXER[1].play(res.SOUND['CHAPTER_END'])
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
				#ITEM GET
				elif txt[tid][0] == 1:
					if isinstance(txt[tid][1],int):
						mny = None
						for it in ['credit_card','wallet']:
							if mny == None: mny = self.guis['INVENTORY'].gui.find(None,it,'value')
						if mny != None:
							mny[1] += txt[tid][1]
							res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1])
							res.MIXER[0].play(res.SOUND['CASH_GET'])
							self.notification.append({'TEXT': 'Adquiriu $' + str(txt[tid][1]), 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
					elif txt[tid][1] == 'greenblood':
						gb = self.guis['INVENTORY'].gui.find(None,'tube','value')
						if gb != None:
							if gb[1] > 150: self.dialog(dtb.DIALOGS['REWARD'][3].copy(),i['RECT'])
							elif gb[1] > 90: self.dialog(dtb.DIALOGS['REWARD'][2].copy(),i['RECT'])
							elif gb[1] > 0: self.dialog(dtb.DIALOGS['REWARD'][1].copy(),i['RECT'])
							else: self.dialog(dtb.DIALOGS['REWARD'][0].copy(),i['RECT'])
							if gb[1] > 0 and self.notification['X'] == 0:
								mny = None
								for m in ['credit_card','wallet']:
									if mny == None: mny = self.guis['INVENTORY'].gui.find(None,m,'value')
								if mny!= None:
									res.INVENTORY[mny[0][0]][mny[0][1]][mny[0][2]][mny[0][3]] = str(mny[1] + gb[1])
									res.MIXER[0].play(res.SOUND['CASH_GET'])
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
								mny = self.guis['INVENTORY'].gui.find(None,'credit_card','value')
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
								self.guis['INVENTORY'].gui.add(res.PARTY[res.FORMATION][0],txt[tid][1],prp)
								res.MIXER[0].play(res.SOUND['ITEM_GET'])
								self.notification.append({'TEXT': dtb.ITEMS[txt[tid][1]][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': -180,'IMAGE': pygame.image.load(res.ITEMS_PATH + txt[tid][1] + '.png')})
				#CALLING
				elif txt[tid][0] == 4:
					if txt[tid][1] != 'stop':
						res.MIXER[1].play(res.SOUND['CALLING'],-1)
						res.MIXER[3].play(res.SOUND['RINGTONE_' + str(res.PARTY[res.FORMATION][0])])
						if self.rad.onoff: pygame.mixer.music.pause()
						tw = 0
						cl = False
						while tw < 2000 and cl == False:
							pygame.time.wait(10)
							for event in pygame.event.get():
								if event.type == pygame.KEYUP:
									cl = True
							tw += 1
						res.MIXER[1].stop()
						res.MIXER[3].stop()
						res.MIXER[0].play(res.SOUND['EQUIP'])
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
				#TASKS
				elif txt[tid][0] == 6:
					res.MIXER[0].play(res.SOUND['NOTIFICATION'])
					if txt[tid][1] in dtb.TASKINDEX:
						res.TASKS.append([txt[tid][1], 0])
						if 'TIME' in dtb.TASKINDEX[txt[tid][1]][0]:
							res.TIME = dtb.TASKINDEX[txt[tid][1]][0]['TIME']
						if 'MARKER' in dtb.TASKINDEX[txt[tid][1]][0]:
							res.MARKER.append(dtb.TASKINDEX[txt[tid][1]][0]['MARKER'])
						#res.task_save(txt[tid][1],0)
						self.notification.append({'TEXT': dtb.TASKINDEX[txt[tid][1]][0]['NAME'], 'COLOR': (255, 123, 0), 'HALIGN': 'left','X': 0})
					elif self.guis['INVENTORY'].gui.find(res.PARTY[res.FORMATION][0],txt[tid][1]):
						res.MIXER[1].play(res.SOUND['ITEM_GET'])
						for j in txt[tid][3][::-1]:
							txt.insert(tid + 1, j)
					else:
						for j in txt[tid][2][::-1]:
							txt.insert(tid + 1, j)
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
				#BATTLE
				elif txt[tid][0] == 13:
					self.dlg['TEXT'] = []
					pygame.mixer.music.stop()
					if len(txt[tid]) > 2: rpt = txt[tid][2]
					else: rpt = 1
					x = 0
					for k in range(rpt):
						for f in txt[tid][1]:
							i = Enemy(f,(0,0))
							if i.type == 'mercenary': self.mrc.append(i)
							else: self.foe.append(i)
							x += 1
					txt = []
					tid = 0
					if self.battle == False:
						self.mnu = 0
						self.turn = -4
						self.fight()
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
				#INCREASE/DECREASE STATUS
				elif txt[tid][0] == 20:
					if txt[tid][2] < 2:
						for i in self.foe + self.mrc:
							prb = round(np.random.randint(0,20))
							if prb > 10:
								res.MIXER[0].play(res.SOUND['ATTRIBUTE_LOSS'])
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
				#KEYBOARD INPUT
				elif txt[tid][0] == 22:
					snd = pygame.mixer.music.get_sound()
					pygame.mixer.music.stop()
					yy = 0
					self.dlg['TEXT'].append(0)
					self.dlg['TEXT'].append('')
					txtsz = np.floor(res.FONTS['DEFAULT'].size(self.dlg['TEXT'][-1])[0]/res.GSCALE) + 10
					self.dlgrct.append(pygame.Rect((self.displayzw - 22) - txtsz,self.displayzh - 100 + self.dlg['Y'] - yy,5 + txtsz,25))
					self.dlg['Y'] += 40
					self.vkb.active = True
					while self.vkb.active:
						self.dlg['TEXT'][-1] = self.vkb.output
						txtsz = np.floor(res.FONTS['DEFAULT'].size(self.dlg['TEXT'][-1])[0]/res.GSCALE) + 10
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
									if len(cmd) > 1: self.guis['INVENTORY'].gui.type = int(cmd[1])
									else: txt.insert(tid + 1,'missing arguments in "inventory": (value)')
								if cmd[0].lower() == 'gui':
									if len(cmd) > 1: txt.insert(tid + 1,(12,cmd[1]))
									else: txt.insert(tid + 1,'missing arguments in "gui": (class)')
					if txt[tid][1] in [0,1,2,3,4,5]:
						res.CHARACTERS[txt[tid][1]]['NAME'] = self.vkb.output
					if snd != None: pygame.mixer.music.play(snd,-1)
					self.dlg['TEXT'].append(0)
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

	def events(self,pressed,mouse):
		for i in range(len(self.optrects)):
			rct = self.optrects[i].copy()
			rct.y -= self.scroll
			if pygame.Rect.colliderect(mouse,rct): self.opt = i
			
		if pressed[4][0]: self.speed = 3
		else: self.speed = res.SPEED

	def draw(self):
		self.window.fill((0,0,0,0))
		if self.chapter:
			sz = res.FONTS[self.curfnt].size(self.chapter)
			pygame.draw.rect(self.window,res.COLOR,pygame.Rect(0,self.window.get_height() - 25,self.window.get_width(),50))
			self.window.blit(res.FONTS[self.curfnt].render(dtb.CHAPTERS[self.chapter][0],True,(10,10,10)),(int(self.window.get_width()/2) - int(sz[0]/2),self.window.get_height() - 25))
			self.window.blit(res.FONTS[self.curfnt].render(dtb.CHAPTERS[self.chapter][1],True,(10,10,10)),(int(self.window.get_width()/2) - int(sz[0]/2),self.window.get_height() - 50))
		else:
			if self.scroll < (self.idx * 60): self.scroll += 4
			lst = [self.rects,self.optrects]
			for r in range(len(lst)):
				for i in range(len(lst[r])):
					if r == 0: txt = self.text[i]
					else: txt = self.choices[i][0]
					if txt != '':
						rct = lst[r][i].copy()
						rct.y -= self.scroll
						if self.shake: shk = (np.random.randint(-5,5),np.random.randint(-5,5))
						else: shk = (0,0)
						if r == 1 and self.opt == i: col = ((10,10,10),res.COLOR)
						else: col = (res.COLOR,(10,10,10))
						#DRAW BOXES
						for l in [0,rct.width]:
							pygame.draw.ellipse(self.window,col[1],pygame.Rect(rct.x + l - (rct.height/2),rct.y + 10,rct.height,rct.height))
							pygame.draw.ellipse(self.window,col[0],pygame.Rect(rct.x + l - (rct.height/2),rct.y,rct.height,rct.height))
						pygame.draw.rect(self.window,col[0],rct)
						pygame.draw.rect(self.window,col[1],pygame.Rect(rct.x,rct.y + rct.height,rct.width,10))
						#DRAW TEXT
						sz = res.FONTS[self.curfnt].size(txt)
						self.window.blit(res.FONTS[self.curfnt].render(txt,True,col[1]),(rct.x + 5 + shk[0],rct.y + int(rct.height/2) - int(sz[1]/2) + shk[1]))
			if self.iblk > 0:
				cor = (self.window.get_width() - 30,200 + ((self.idx + 1) * self.bxmargin) - self.scroll)
				if self.iblk < 50:
					pygame.draw.polygon(self.window,res.COLOR,((cor[0],cor[1]),(cor[0] + 10,cor[1]),(cor[0] + 5,cor[1] + 10)))
					pygame.draw.polygon(self.window,(10,10,10),((cor[0] - 2,cor[1] - 2),(cor[0] + 12,cor[1] - 2),(cor[0] + 5,cor[1] + 12)),2)
				self.iblk += 4
				if self.iblk > 100: self.iblk = 1
		return self.window

	def run(self):
		if self.testing:
			for event in pygame.event.get():
				pressed, mr = tools.event.get_pressed(event)
				if event.type == pygame.QUIT: pygame.quit(); exit()
				self.events(event,mr)
			self.draw()
			pygame.display.flip()
			pygame.time.Clock().tick(res.FPS)
		else: self.parent.run()

class Map:
	def loadmap(self, mp=None):
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
		self.bbg['X'] = 0
		for i in self.player: i['NODES'] = []
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
		#SKY
		if t['TYPE'] == 'SKY':
			if len(self.tilmap[3]) == 0:
				img = pygame.image.load(res.BACKG_PATH + 'sky.png').convert_alpha()
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
			if t['frames'] != []: image = self.map.get_tile_image_by_gid(t['frames'][fr].gid).convert_alpha()
			else: image = self.map.get_tile_image_by_gid(gid).convert_alpha()
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
				img.append(self.map.get_tile_image_by_gid(t['frames'][fi].gid).convert_alpha())
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
				if t['TYPE'] != 'TREADMILL': frm = self.map.get_tile_image_by_gid(t['frames'][fi].gid).convert_alpha()
				else: frm = pygame.transform.rotate(self.map.get_tile_image_by_gid(t['frames'][fi].gid).convert_alpha(),45 * (int(t['DIRECTION']) - 1))
				img.append(frm)
			t['IMAGE'] = img
		#MOVING
		elif t['TYPE'] == 'MOVING':
			t['IMAGE'] = image
			t['INOUT'] = True
			t['TIME'] = 0
		#NORMAL TILE
		elif t['TYPE'] not in ['INVISIBLE','CARRY','HOLD','HIDEON','HIDEOFF','WATER']:
			#this coordinates functions is suposed to draw tiles at the current camera position,however
			# nothing is drawn when executed. <WORK ON IT>
			#self.tilmap[i][a].blit(image, ((x * self.map.tilewidth) - self.cam.x, (y * self.map.tileheight) - self.cam.y))
			self.tilmap[i][a].blit(image, (x * self.map.tilewidth, y * self.map.tileheight))
		#TILRECT
		try: 
			p = self.map.get_tile_properties(x, y, i)
			trct = pygame.Rect((x + int(p['X'])) * self.map.tilewidth, (y + int(p['RECT'].y)) * self.map.tileheight,int(p['WIDTH']),int(p['HEIGHT']))
		except: trct = pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)
		if i < 2 and a == 0:
			#STEP TILES
			if i == 0: self.tilrect[i].append([t,trct])
			#MOVABLE OBJECTS
			if t['TYPE'] in ['CARRY','HOLD','DESTROY']:
				if t['frames'] != []:
					trct = pygame.Rect(x * self.map.tilewidth, (y * self.map.tileheight) + self.map.tileheight,self.map.tilewidth,self.map.tileheight)
					srf = pygame.Surface((self.map.tilewidth,self.map.tileheight * 2), pygame.SRCALPHA)
					srf.blit(self.map.get_tile_image_by_gid(t['frames'][1].gid).convert_alpha(),(0,0))
					srf.blit(self.map.get_tile_image_by_gid(t['frames'][0].gid).convert_alpha(),(0,self.map.tileheight))
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
		#FOR GRID
		if i in [0,1]:
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
						for r in range(np.floor(obj.height/2)):
							srf = pygame.Surface((obj.width,obj.height),pygame.SRCALPHA)
							pygame.draw.circle(srf, (255, 255, 255, r), (np.floor(obj.width/2),np.floor(obj.height/2)), r)
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
				for i in range(round(np.random.randint(5,10))):
					wh = lst[round(np.random.randint(0,len(lst) - 1))]
					eny = Enemy(wh,(0,0))
					eny.id = i
					rct = None
					while rct == None: rct = self.tilrect[0][round(np.random.randint(0, len(self.tilrect[0])))]
					eny.rect.x = rct[1].x
					eny.rect.y = rct[1].y
					self.enemies.append(eny)
					self.objects.append(['enemy',eny.id,eny.rect.y])
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
				for i in range(np.random.randint(0,5)):
					prb = np.random.randint(0,len(lst) - 1)
					img = res.SPRITES[lst[prb] + '_WALKL'][0]
					sz = img.get_rect()
					rct = None
					while rct == None: rct = self.tilrect[0][round(np.random.randint(0, len(self.tilrect[0])))]
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
			
class Game:
	def __init__(self):
		res.FONTS = {**res.FONTS,**{'SCORETXT': pygame.font.Font(res.FONTS_PATH + 'BohemianTypewriter.ttf', 10 * res.GSCALE)}}
		self.running = True
		self.log = ''
		self.rectdebug = False
		self.disdbg = False
		self.waitime = 0
		self.waitlst = [['advice',432000],['rain',3600]]
		self.glock = pygame.time.Clock()
		
		#MENU VARIABLES
		self.player = []
		self.dvmp = pygame.Rect(0,0,2,2)
		self.dlg = None
		self.trsction = None
		self.counters = [GUI.Counter(7)]
		self.vkb = GUI.Vkeyboard(pygame.Rect(0,0,400,400))
		self.guis = {'FILES': GUI.Files(pygame.Rect(0,100,300,400)),'BKG': GUI.Backgrounds((0,0),'stars'),
			'VECTOR': GUI.VectorialDraw(),'3D': GUI.Pseudo3d(),'LEVEL': GUI.LevelMenu((0,0)),
			'INVENTORY': GUI.Popup('Inventory',(400,300),0),'STATUS': GUI.Popup('Status',(300,300)),
			'TACTICS': GUI.Popup('Tactics',(300,300)),'RADIO': GUI.Popup('Radio',(300,300)),'POPUPS': []
			}

		#SURFACES AND DISPLAY
		sz = pygame.display.Info()
		self.resize((sz.current_w,sz.current_h))
		for i in self.guis:
			if i not in ['POPUPS','FILES','BKG']: self.guis[i].show = False
			elif i == 'POPUPS':
				for p in self.guis['POPUPS']: self.guis['POPUPS'][p].show = False
			else: self.guis[i].show = True
			if i in ['STATUS']: self.guis[i].min = True

		
		#QUICKSTART
		if res.QUICKSTART > 3:
			self.guis['FILES'].show = False
			self.guis['FILES'].mnu = 1
			res.PAUSE = 0
		elif res.QUICKSTART > 2: self.guis['FILES'].mnu = 3
		elif res.QUICKSTART > 1: self.guis['FILES'].mnu = 2

		self.dmg = []
		self.actqueue = []
		self.notification = []
		self.cityname = ''
		self.build = ''

		#BATTLE VARIABLES
		self.equip = []
		self.battle = False
		self.obstacles = False
		self.hits = 0
		self.tdmg = 0
		self.hpl = 0
		self.tbt = 0
		self.turn = -1
		self.dices = []
		self.sttsy = 0
		self.objects = []
		res.MAP = 'savetest'
		res.PX = 100
		res.PY = 100
		#PLAYERS
		for i in range(1): self.objects.append(['char',Character(i,(res.PX,res.PY)),res.PY])
		self.objects[0][1].playing = True
		self.objects += [['char',Character('4.1.1',(10,10)),10],['char',Character('CH1BLUEBULLDOG',(10,300),file='chapter_01'),30]]

		#MAP VARIABLES
		self.map = None
		self.mapcache = {}
		self.enemies = []
		self.foe = []
		self.fig = []
		self.mrc = []
		self.portalgo = {}
		#STARTING GAME
		if res.CHAPTER == 0:
			for j in self.tutorial['TEXT']:
				if isinstance(j,list):
					if j[0] == 'phone':
						self.tutorial['GO'] = j[1]
					if j[0] == 'wait':
						self.tutorial['WAIT'] = j[1]
						if len(j) > 2: self.tutorial['NEXT'] = j[2]
				else: self.tutorial['OUTPUT'].append(j)
		else:
			pass
			'''self.map = MapHandler('savetest.xml')
			self.mapcache['savetest.xml'] = self.map
			self.tilmap = [[i,i] for i in self.map.surfaces]'''
		for i in tools.draw.transiction((self.window.width,self.window.height),1,-100,'fade'): self.trsction = i; self.run()
	
	def resize(self, size):
		#WINDOW
		if size == 'fullscreen':
			self.screen = pygame.display.set_mode((800,600), pygame.FULLSCREEN)
			size = self.screen.get_size()
			if (self.window.width,self.window.height) == size:
				size = (800,600)
				self.screen = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
		else: self.screen = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)

		#SURFACES
		self.window = pygame.Rect(0,0,size[0],size[1])
		self.display = pygame.Rect(0,0,int(size[0]/res.GSCALE),int(size[1]/res.GSCALE))
		self.surfaces = [pygame.Surface(size), pygame.Surface(size, pygame.SRCALPHA)]
		self.cam = pygame.Rect(0,0,size[0],size[1])
		self.camgrid = 1
		self.campos = [0,0]
		self.blackbars = [pygame.Rect(0,(size[1] - 60) * i,size[0],60) for i in range(2)]

		#MENUS
		#halign = 0 #left
		#halign = int(size[0]/2) - int((460/res.GSCALE)/2) #center
		halign = size[0] - 310 #right
		self.vkb.rect.width = size[0]
		self.guis['FILES'].rect.x = halign
		self.guis['BKG'].__init__(size,self.guis['BKG'].type)
		self.guis['LEVEL'].surface = pygame.Surface(size)

		#GRADIENTS
		self.grd = []
		for g in range(200):
			srf = pygame.Surface((size[0],1),pygame.SRCALPHA)
			srf.fill((0,0,0,200 - g))
			self.grd.append(srf)

		#TOUCHPAD
		if res.MOUSE == 2:
			self.buttons = [pygame.Rect(20,size[1] - 264,240,80),pygame.Rect(20,size[1] - 100,240,80),pygame.Rect(20,size[1] - 264,80,240),
				pygame.Rect(184,size[1] - 264,80,240),pygame.Rect(size[0] - 190,size[1] - 100,80,80),pygame.Rect(size[0] - 100,size[1] - 100,80,80),
				pygame.Rect(size[0] - 190,40,80,80),pygame.Rect(size[0] - 100,40,80,80),pygame.Rect(20,40,80,80)]
		else: self.buttons = []

		#OTHERS
		self.aim = pygame.Rect(300,int(self.display.height/2),30,30)

	def pet(self, i):
		#ANIMATION
		if self.player[0]['PAUSE'] < 2: i['GIF'] += 0.5
		if i['GIF'] >= len(i['SPRITE']): i['GIF'] = 0
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.surfaces[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
		if res.TIME[0] < 12:
			tms = (12 - res.TIME[0]) * 2
			sxx = i['RECT'].x - self.cam.x - tms + 5
		else:
			tms = (res.TIME[0] - 12) * 2
			sxx = i['RECT'].x - self.cam.x
		if tms < 5: tms = 5
		img = i['SPRITE'][np.floor(i['GIF'])]
		shd = pygame.transform.scale(pygame.transform.rotate(img,90),(tms,4))
		shd.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
		shd.set_alpha(100)
		self.surfaces[0].blit(shd, (sxx, i['RECT'].y - self.cam.y))
		self.surfaces[0].blit(img, (i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y))
		#MOVEMENT
		if self.winbar == 0:
			#FOLLOW MOVEMENT
			if i['MOVE'] == 'follow': i['DIRECTION'] = tools.physics.follow(i['RECT'],self.player[0]['RECT'])
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
					do = np.random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit': i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand': i['MOVE'] = 'sit'
					elif do == 1:
						dl = [1,5]
						i['DIRECTION'] = dl[np.random.randint(0,1)]
						i['MOVE'] = 'walk'
				elif i['FILE'].startswith('DOG'):
					do = np.random.randint(0,1)
					if do == 0:
						if i['MOVE'] == 'sit': i['MOVE'] = 'stand'
						elif i['MOVE'] == 'stand': i['MOVE'] = 'sit'
					elif do == 1:
						dl = [1,5]
						i['DIRECTION'] = dl[np.random.randint(0,1)]
						i['MOVE'] = 'walk'
				if i['DIRECTION'] == 1: dr = 'L'
				if i['DIRECTION'] == 5: dr = 'R'
				i['SPRITE'] = res.SPRITES[i['FILE'] + '_' + i['MOVE'].upper() + dr]
				i['TIME'] = 20

	def npc(self, i):
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.surfaces[0], (255,0,0), pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
		if i['TYPE'] in [0,2,3,4]: imgrct = self.doll(i,False)
		elif i['TYPE'] >= 5:
			shk = 0
			if i['TYPE'] == 11:
				for w in res.WASH:
					if w[1] == i['WHO']:
						shk = int(np.random.randint(-2,2))
						break
			imgrct = pygame.image.load(res.SPRITES_PATH + 'obj_' + str(i['INDEX']) + '.png')
			self.surfaces[0].blit(imgrct, (i['RECT'].x - self.cam.x + shk, i['RECT'].y - self.cam.y - 10))
			if self.player[0]['SLEEP'] and i['TYPE'] == 6: self.doll(self.player[0],False)
		else: imgrct = pygame.Surface((i['RECT'].width,i['RECT'].height))
		#FOLLOW
		if i['FOLLOW'] != None and i['FOLLOW'] != (None,None):
			i['SPEED'] = 3
			i['DIRECTION'] = tools.physics.follow(i['RECT'],i['FOLLOW'])
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
				try: t = self.tilrect[1][(np.floor((i['RECT'].y + 15)/self.map.tilewidth) * self.map.width) + np.floor((i['RECT'].x + 15)/self.map.tilewidth)]
				except: t = None
				if self.rectdebug and t != None:
					pygame.draw.rect(self.surfaces[0], (255,200,0), pygame.Rect(t[1].x - self.cam.x, t[1].y - self.cam.y, t[1].width, t[1].height),3)
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
		
	def vehicle(self, i):
		rect = pygame.Rect(i['RECT'].x - 5,i['RECT'].y - 5,60,30)
		for p in self.player:
			if p['DRIVING'] == i['N']:
				i['RECT'].x = p['RECT'].x
				i['RECT'].y = p['RECT'].y
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.surfaces[0], (255,0,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height))
		if self.colide(rect, self.cam) and self.turn != -6:
			self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'moto_' + str(i['INDEX']) + '_walkL.png'), (rect.x - self.cam.x + 10, rect.y + rect.height - self.cam.y - 30))
		#MOVEMENT
		if i['MOVE'] == 'street':
			try: t = self.tilrect[0][(np.floor(i['RECT'].y/self.map.tilewidth) * self.map.width) + np.floor(i['RECT'].x/self.map.tilewidth)]
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
		dst = np.hypot(*dir)
		if dst == 0.0: dir = (0, -1)
		else: dir = (dir[0]/dst,dir[1]/dst)
		'''if dst < 0: dst = -dst
		if dst == 0: dst = 1'''
		snd.set_volume(2/dst)
		snd.play()
		pygame.draw.line(self.surfaces[0],(200,10,10),(self.player[0]['RECT'].x - self.cam.x,self.player[0]['RECT'].y - self.cam.y),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		self.surfaces[0].blit(res.FONTS['DEFAULT'].render(str(dst),True,(200,200,200)),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		#ACTION
		for p in self.player:
			if self.colide(p['RECT'], rect) and p['DRIVING'] == None:
				if self.battle == False:
					self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (rect.x - self.cam.x + int(rect.width/2) - 5, rect.y - self.cam.y - int(rect.height/2)))
					res.HINTEXT = 'VEHICLE_USE'
				if self.pressed[4][0] and self.guis['INVENTORY'].gui.type == 0 and self.phone == 0:
					trigger = True
					p['DRIVING'] = i['N']
					p['RECT'].x = rect.x
					p['RECT'].y = rect.y
					i['MOVE'] = 'fixed'
					'''self.display.width = 1200
					self.display.height = 800
					self.display = pygame.Surface((1200, 800))
					self.cam = pygame.Rect(0,0,self.display.width,self.display.height)'''

	def portal(self, i):
		if i['RECT'].width > 0: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,i['RECT'].width,i['RECT'].height)
		else: rect = pygame.Rect(i['RECT'].x,i['RECT'].y,30,30)
		#DRAW
		if self.rectdebug: pygame.draw.rect(self.surfaces[0], (255,255,0), pygame.Rect(rect.x - self.cam.x, rect.y - self.cam.y, rect.width, rect.height),3)
		if self.colide(self.player[0]['RECT'], rect) and self.winbar > 0: spr = '1'
		else: spr = '0'
		if res.MAP != 'rodoviary':
			if i['RECT'].width == 24: self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_0' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
			if i['RECT'].width == 48: self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_1' + spr + '.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		else: self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_player.png'), (rect.x - self.cam.x, rect.y - self.cam.y))
		goto = False
		#ENTERING DOOR
		if self.colide(self.player[0]['RECT'], rect) and self.winbar == 0 and self.portalgo == {}:
			if i['OPENING'] == 'key':
				fnd = self.guis['INVENTORY'].gui.find(res.PARTY[res.FORMATION][0],'key_bedroom')
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
				res.MIXER[1].play(res.SOUND['DOOR_OPEN'])
			if i['MUSIC'] not in ['inside','outside',None]:
				pygame.mixer.music.fadeout(1000)
				spd = 5
			else: spd = 10
			#BATHROOM
			if i['MAP'] == 'bathroom':
				self.transiction(True, int(self.display.height/2))
				for i in range(30): self.run()
				res.MIXER[1].play(res.SOUND['TREASURE_GET'])
				for i in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[i]['HEALTH'] in [3,5]:
						res.CHARACTERS[i]['HEALTH'] = 0
				for i in range(60): self.run()
				res.MIXER[1].play(res.SOUND['DOOR_CLOSE'])
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
					self.transiction(True, int(self.display.height/2), spd, "side")
					self.loadmap(i['MAP'])
				#OUT
				self.portalgo[0]['MATCH'] = i['MATCH']
				while self.portalgo[0]['MATCH'] != None: self.run()
				if i['TYPE'] > 0: res.MIXER[1].play(res.SOUND['DOOR_CLOSE'])
				if i['MUSIC'] == 'outside': pygame.mixer.music.set_volume(1.0)
				elif i['MUSIC'] == 'inside': pygame.mixer.music.set_volume(0.2)
				elif i['MUSIC'] != None: pygame.mixer.music.play(res.SOUND[i['MUSIC'].upper()],-1)
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
							prb = np.random.randint(0,len(lst) - 1)
							p['RECT'].x = lst[prb][0]
							p['RECT'].y = lst[prb][1]
					p['PAUSE'] = 0
	
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
							self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (i[1].x - self.cam.x + int(i[1].width/2) - 5, i[1].y - self.cam.y - i[1].height))
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
	
	def events(self):
		if self.battle and self.turn < 0: res.HINTEXT = None
		else: res.HINTEXT = 'MENUS'
		for event in pygame.event.get():
			#GENERAL EVENTS
			self.pressed, self.click = tools.event.get_pressed(event)
			if event.type == pygame.QUIT: self.running = False #QUIT
			if event.type == pygame.VIDEORESIZE: self.resize((event.w,event.h)) #RESIZE
			if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
				if res.FULLSCREEN < 2: self.resize('fullscreen') #FULLSCREEN
				else: self.running = False #QUIT WHEN FULLSCREEN ONLY
			if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]: self.__init__() #RESET
			if self.pressed[8][0] and res.DEBUG: self.dialog(['',(22,'debug')]) #DEBUG
			
			#CLICK
			if res.MOUSE == None:#1:
				for i in range(2):
					if res.CLICK[i] == 'move' and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[i]:
						rct = pygame.Rect(int(np.floor(((self.click.x/res.GSCALE) + self.cam.x)/self.map.tilewidth) * self.map.tilewidth),
						int(np.floor(((self.click.y/res.GSCALE) + self.cam.y)/self.map.tileheight) * self.map.tileheight),10,10)
						img = []
						for a in range(2): img.append(pygame.image.load(res.SPRITES_PATH + 'click_' + str(a) + '.png'))
						self.objects.append(['click',{'RECT': rct,'IMAGE': img,'GIF': 0.0,'DESTROY': False},rct.y])
						self.player[0]['FOLLOW'] = rct
						self.player[0]['FOLLEND'] = 3

			#BATTLE OPTIONS
			if self.battle and self.phone == 0 and self.dlg['FADE'] > 0 and self.turn >= 0:
				if self.turn == len(res.PARTY[res.FORMATION]): self.fight()
				else:
					if self.turn == 0: tp = 0
					elif self.turn >= len(self.player): tp = 0
					elif self.player[self.fig[self.turn]['N']]['PLAYING']: tp = self.turn
					else: tp = 0
				#CHOOSING WEAPON
				if self.mnu == 1:
					if self.pressed[2][tp]: self.equip[self.fig[self.turn]['N']] -=1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
					if self.pressed[3][tp]: self.equip[self.fig[self.turn]['N']] +=1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
				
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
									res.MIXER[0].play(res.SOUND['MELEE'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('tool'):
									res.MIXER[0].play(res.SOUND['MELEE'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('gun') and self.barpp[self.turn][self.equip[self.fig[self.turn]['N']]] > 0:
									res.MIXER[0].play(res.SOUND['GUN_TRIGGER'])
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0].startswith('grenade'):
									res.MIXER[0].play(res.SOUND['MELEE'])
									res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][1] = '300'
									self.mnu = 2
								elif res.INVENTORY[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]][4][self.equip[self.fig[self.turn]['N']] + 1][0] == '_':
									self.mnu = 2
								else: res.MIXER[0].play(res.SOUND['ERROR'])
							else: res.MIXER[0].play(res.SOUND['ERROR'])
						#TACTICAL
						elif self.equip[self.fig[self.turn]['N']] == 4:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
							self.mnu = 2
						#DIALOG
						elif self.equip[self.fig[self.turn]['N']] == 5:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
							if self.dlg['TEXT'] == []: self.dialog(dtb.DIALOGS['BATTLEDIALOG'])
							self.mnu = 1
							self.turn += 1
						#GUARD
						elif self.equip[self.fig[self.turn]['N']] == 6:
							res.MIXER[1].play(res.SOUND['GUARD'])
							self.fig[self.turn]['RESISTANCE'] += 3
							self.turn += 1
							if self.turn == len(self.fig): self.fight()
						#RUN AWAY
						elif self.equip[self.fig[self.turn]['N']] == 7:
							res.MIXER[0].play(res.SOUND['MENU_GO'])
							self.fight()
							if self.battle:
								self.turn = len(res.PARTY[res.FORMATION])
								self.fight()
				#USING WEAPON
				elif self.mnu == 2:
					if self.equip[self.fig[self.turn]['N']] == 4:
						if self.pressed[2][tp]: self.opt -= 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
						if self.pressed[3][tp]: self.opt += 1; res.MIXER[0].play(res.SOUND['MENU_HOR'])
					sht = False
					if self.pressed[4][tp]: sht = True
					elif res.MOUSE > 0:
						self.aim.x = int(pygame.mouse.get_pos()[0]/res.GSCALE)
						self.aim.y = int(pygame.mouse.get_pos()[1]/res.GSCALE)
						if event.type == pygame.MOUSEBUTTONUP:
							if self.colide(self.aim,pygame.Rect(0,self.winbar,self.display.width,self.display.height - (self.winbar * 2))):
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
										res.MIXER[0].play(res.SOUND['GUN_TRIGGER'])
										self.mnu = 2
										self.wait()
									if self.equip[self.fig[self.turn]['N']] != 6: self.fight()
									else:
										self.fig[self.fig[self.turn]['N']]['RESISTANCE'] += 3
										res.MIXER[0].play(res.SOUND['GUARD'])
								self.turn += 1
							for i in self.equip: i = 4
					#CANCEL MOVE
					if self.pressed[5][tp]:
						res.MIXER[0].play(res.SOUND['MISS'])
						self.mnu = 1
					if self.opt < 0: self.opt = len(res.TACTICAL) - 1
					if self.opt > len(res.TACTICAL) - 1: self.opt = 0
			
			#OPEN N' CLOSE MENUS AND UPGRADE
			for i in range(len(res.ACTION)):
				if self.pressed[i][0]:
					if res.ACTION[i] == 'pause' and self.guis['FILES'].mnu == 1:
						self.guis['FILES'].show = not self.guis['FILES'].show
						if self.guis['FILES'].show: res.PAUSE = 2
						else: res.PAUSE = 0
					if res.ACTION[i] == 'chat': res.PAUSE = 1; self.dlg = Dialog('chat'); res.PAUSE = 0
					if res.ACTION[i] == 'inventory' and self.guis['INVENTORY'].gui.itmov == '':
						self.guis['INVENTORY'].show = not self.guis['INVENTORY'].show
						#OPEN AND CLOSE
						if self.guis['INVENTORY'].show and self.guis['INVENTORY'].gui.hld < 20:
							self.guis['INVENTORY'].gui.type = 1
							self.guis['INVENTORY'].gui.fade = 0
							self.guis['INVENTORY'].gui.opt = [0,0,0,0]
							res.MIXER[0].play(res.SOUND['INVENTORY_OPEN'])
							res.PAUSE = 1
						else:
							res.PAUSE = 0
							res.MIXER[0].play(res.SOUND['INVENTORY_CLOSE'])
							if self.guis['INVENTORY'].gui.type == 2: self.dlg = Dialog('DEPOSIT')
							if self.battle: self.mnu = 1
					if res.ACTION[i] == 'shortcut': pass
					if res.ACTION[i] == 'upgrade':
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ENERGY'] > 0:
							res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ENERGY'] -= 33
							res.INVENTORY[res.PARTY[res.FORMATION][0]][4][1][1] = int(res.INVENTORY[res.PARTY[res.FORMATION][0]][4][1][1]) + 1
							res.MIXER[1].play(res.SOUND['EQUIP'])
						if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ENERGY'] < 0:
							res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ENERGY'] = 0
			
			#DEVICE OPTIONS
			mnuchk = None
			if mnuchk and self.pressed[mnuchk[3]][0] and self.dev != None and self.guis['INVENTORY'].gui.find(res.PARTY[res.FORMATION][0],'phone') != None and self.guis['INVENTORY'].gui.type == 0:
				#OPEN AND CLOSE
				if self.phone == 0:
					self.player[0]['HEAD'] = 'DD'
					self.player[0]['SPRITE'] = 'PHONE'
					self.player[0]['PAUSE'] = 1
					self.phone = 1

					dv = self.dev()
					self.dev = dv[0]
					if self.dev == 'radio': self.dev = self.rad
					if self.dev != None: self.dev.battery = dv[1]
				else:
					self.phone = 0
					if self.battle == False:
						self.dev.opt = [0,0]
						self.player[0]['PAUSE'] = 0
					else: self.mnu = 1
			#DEVICE EVENTS
			'''if self.phone > 0 and self.dev != None and self.dev.battery > 0:
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
				elif self.dev.ingame == 3: self.dialog([dtb.MENU[17]])
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
						pygame.mixer.music.play(res.SOUND['AMBIENCE_SIREN'],-1)
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
			'''
			#OBJECTS INSIDE EVENTS
			rqst = None
			if not self.dlg:
				for i in self.objects:
					if i[0] == 'char':
						i[1].inside_events(self.pressed,self.click)
						if i[1].dialog: rqst = i[1]
			
			#DIALOG EVENTS
			if self.dlg: self.dlg.events(self.pressed,self.click)
			if rqst:
				res.PAUSE = 1
				self.dlg = Dialog(rqst.dialog,file=rqst.talk)
				self.dlg.parent = self
				self.dlg.start()
				self.dlg = None
				res.PAUSE = 0
			
			#GUI INSIDE EVENTS
			nw = {}
			rcts = []
			for i in self.guis:
				if i == 'POPUPS':
					for p in self.guis[i]:
						do = True
						for r in rcts:
							if pygame.Rect.colliderect(self.click,r): do = False
						rcts.append(self.guis[i][p].rect)
						if do and self.guis[i][p].show: self.guis[i][p].inside_events(self.pressed,self.click)
						if self.guis[i][p].gui != None: nw[i]['POPUPS'] = self.guis[i][p]
				else:
					if self.guis[i].show: self.guis[i].inside_events(self.pressed,self.click)
					nw[i] = self.guis[i]
			self.guis = nw

			#BUILD ITEMS
			if self.pressed[4][0] and self.build != '' and self.battle == False and self.player[0]['SLEEP'] == False:
				if self.guis['INVENTORY'].gui.type == 0:
					if self.build.startswith('tent'):
						self.objects.append(['tent',{'RECT': pygame.Rect(np.floor((self.player[0]['RECT'].x + 15)/30) * 30,np.floor((self.player[0]['RECT'].y + 15)/30) * 30,30,30),'SPRITE': pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')},self.player[0]['RECT'].y])
						self.build = ''
			#VKEYBOARD
			if self.vkb.active == True: self.vkb.events(event)
		self.pressed, self.click = tools.event.get_pressed(None)
		#OBJECTS OUTSIDE EVENTS
		rqstlst = []
		for i in self.objects:
			if i[0] == 'char':
				i[1].outside_events(self.pressed)
				rqstlst += i[1].particles.copy()
				i[1].particles = []
		self.objects += rqstlst
		#GUI OUTSIDE EVENTS
		nw = {}
		rcts = []
		for i in self.guis:
			if i == 'POPUPS':
				for p in self.gui[i]:
					do = True
					for r in rcts:
						if pygame.Rect.colliderect(self.click,r): do = False
					rcts.append(self.guis[i][p].rect)
					if do and self.guis[i][p].show: self.guis[i][p].outside_events(self.pressed)
					if self.guis[i][p].gui != None: nw[i]['POPUPS'] = self.guis[i][p]
			else:
				if self.guis[i].show: self.guis[i].outside_events(self.pressed)
				nw[i] = self.guis[i]
		self.guis = nw
		#PHONE HOLDING OPTIONS
		#if self.phone > 0 and self.dev != None: self.dev.outside_events(self.pressed)
		#MOVE CAMERA
		if self.map:
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

	def fight(self):
		#BATTLE START
		if self.turn < 0:
			res.PAUSE = 1

			#GUI HANDLE
			for i in self.guis:
				if i in ['STATUS','BKG']: self.guis[i].show = True
				elif i == 'POPUPS':
					for p in self.guis['POPUPS']: self.guis['POPUPS'][p].show = False
				else: self.guis[i].show = False
			#pygame.image.load(res.BACKG_PATH + 'bt_' + self.map.habitat + '.png')

			#PLAY SOUND
			if self.guis['RADIO'].gui.onoff: pygame.mixer.music.pause()
			if self.turn == -1: res.MIXER[1].play(res.SOUND['BATTLE_FOE'])
			elif self.turn == -2:
				res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += 1
				res.MIXER[1].play(res.SOUND['BATTLE_ENEMY'])
			elif self.turn == -3:
				res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] -= 1
				res.MIXER[1].play(res.SOUND['BATTLE_AMBUSH'])
			elif self.turn == -6: res.MIXER[1].play(res.SOUND['BAUM'])
			elif self.foe[0]['TYPE'] == 'boss': res.MIXER[1].play(res.SOUND['BATTLE_BOSS'])
			
			'''if self.player[0]['DRIVING'] != None: self.obstacles = True
			
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
				i['MASK'] = pygame.Rect(230 - ((len(self.foe + self.mrc) - 1) * 80) + (x * 80),self.display.height - (50 + sz.height),sz.width,sz.height)
				dprb = [1,5]
				i['DIRECTION'] = dprb[round(np.random.randint(0,1))]
				i['SPEED'] = 0
				i['VITALITY'] = i['VITALITY']
				i['BTIMES'] = [0,0,0,0]
				i['FADE'] = 10
				i['AWAY'] = 0
				i['N'] = x
				x += 1'''

			#CONDITIONS
			if len(self.foe) > 0:
				if self.turn == -3:
					self.foe[0].sprite = pygame.image.load(res.FREAKS_PATH + (self.foe[0].file) + '_backwards.png')
					self.foe[0].health.append(1)
			else:
				if self.turn == -3:
					self.mrc[0].sprite = pygame.image.load(res.FREAKS_PATH + (self.mrc[0].file) + '_backwards.png')
					self.mrc[0].health.append(1)
			
			#ZOOM TRANSITION
			if self.turn != -6:
				for i in tools.draw.transiction((self.window.width,self.window.height),1,-50,'fade'): self.trsction = i; self.run()
			#MYSTERIOUS FREAK
			else:
				freakname = self.foe[0]['NAME'].lower()
				showname = ''
				self.dlg['CAMERA'] = self.foe[0]['RECT']
				abc = 'abcdefghijklmnopqrstuvwxyz'
				for r in range(20):
					showname = ''
					for i in range(len(freakname)):
						res.MIXER[0].play(res.SOUND['TEXT_INPUT'])
						showname += abc[np.random.randint(0,len(abc) - 1)]
					self.cityname = showname
					self.run()
				for i in range(len(freakname)):
					res.MIXER[0].play(res.SOUND['MENU_GO'])
					showname = showname[:i] + freakname[i] + showname[i + 1:]
					self.cityname = showname
					self.run()
				res.MIXER[1].play(res.SOUND['FREAK_DISCOVER'])
				self.transiction(300,100,type="image")
				for i in range(60): self.run()
				self.cityname = ''
				self.transtype = 'bars'
				self.dlg['CAMERA'] = 0

			self.guis['BKG'].__init__((self.window.width,self.window.height),'mirrors')
			
			#PLAY SONG
			'''if len(self.foe) > 0: sng = res.MUSIC_PATH + self.foe[0].song.lower() + '.mp3'
			elif len(self.mrc) > 0: sng = res.MUSIC_PATH + self.mrc[0].song.lower() + '.mp3'
			pygame.mixer.music.load(sng)
			pygame.mixer.music.play()'''
			
			#self.player[0]['GIF'] = 0.0

			self.battle = True
			#self.sttsy = 120
			
			#TRANSITION
			if self.turn != -6:
				for i in tools.draw.transiction((self.window.width,self.window.height),1): self.trsction = i; self.run()
			if res.GSCALE < 3: nb = 100
			else: nb = 60
			
			#if self.turn != -6: self.transiction(True, nb)
			#else: self.turn = 0; self.transiction(100,500,type="image")
			
			#SEEN ANOMALY
			chk = None
			if res.BESTIARY[self.foe[0].file]['SEEN'] == 0:
				res.BESTIARY[self.foe[0].file]['SEEN'] = 1
				chk = self.foe[0].name
			if chk == None and len(self.mrc) > 0: chk = self.mrc[0].name
			
			#AMBUSH
			if self.turn == -2: self.turn = len(self.fig)
			else: self.turn = 0
			
			#INITIATIVE DICES
			'''l = 0
			for i in self.player:
				if i['PLAYING']: l += 1
			if l > 1:
				for i in range(30):
					self.dices = []
					for d in range(len(self.player)):
						if self.player[d]['PLAYING']:
							di = dtb.CLASSES[self.fig[d]['CLASS']]['AGILITY'][self.fig[d]['LEVEL']] + self.fig[d]['BONUS'][2]
							self.dices.append([np.random.randint(0,di),d])
						else: self.dices.append([-1,d])
					self.run()
				for i in range(30):
					self.run()
				self.dices.sort(reverse=True)
				ord = []
				for i in self.dices:
					ord.append(self.fig[i[1]])
				self.dices = []
				self.fig = ord'''
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
						dmg = int(np.random.randint(wpdmg - 2,wpdmg + 2)) - i['RESISTANCE'] + self.fig[self.turn]['STRENGHT']
						if res.CHARACTERS[res.PARTY[res.FORMATION][self.fig[self.turn]['N']]]['HEALTH'] == 11: dmg = int(dmg/2)
						if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_damage.png')
						#HIT
						if dmg <= 0:
							dmg = 1
						for p in range(dmg * 2):
							if i['TYPE'] == 'mercenary': cl = (150, 25, 29)
							else: cl = (10, 255, 50)
							self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(np.random.randint(3,5)), 'DIRECTION': round(np.random.randint(0,360)),
								'SPEED': round(np.random.randint(2,6)), 'COLOR': cl})
						i['VITALITY'] -= dmg
						self.hits += 1
						self.tdmg += dmg
						if dmg >= wpdmg + 2 - i['RESISTANCE'] + dtb.CLASSES[self.fig[self.fig[self.turn]['N']]['CLASS']]['STRENGHT'][self.fig[self.fig[self.turn]['N']]['LEVEL']]:
							if i['VITALITY'] <= 0:
								res.MIXER[1].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								i['AWAY'] = 1
							res.MIXER[0].play(res.SOUND['CRITICAL'])
							self.hitisplay(10, i['MASK'], dtb.MENU['critical'], (200, 0, 0))
						else:
							if it.startswith('melee'): res.MIXER[0].play(res.SOUND['HIT'])
							if it.startswith('gun'): res.MIXER[0].play(res.SOUND['GUNSHOT_1'])
							if it.startswith('grenade'): res.MIXER[0].play(res.SOUND['HIT'])
							else: res.MIXER[0].play(res.SOUND['HIT'])
							self.hitisplay(10, i['MASK'], str(dmg), (200, 0, 0))
						if i['HEALTH'] != 1 and i['VITALITY'] > 0: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']) + '_stand.png')
						#CHECK WIN
						if i['VITALITY'] <= 0:
							if dmg >= i['RESISTANCE']: again = True
							if i['ITEM'] != None:
								prb = round(np.random.randint(0,100))
								if prb > i['ITEM'][1]:
									self.guis['INVENTORY'].gui.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
									res.MIXER[0].play(res.SOUND['ITEM_GET'])
									self.notification.append({'TEXT': 'it_' + i['ITEM'][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
							if i['AWAY'] == 0:
								res.MIXER[1].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								while i['FADE'] > 0:
									i['FADE'] -= 0.5
									self.run()
							i['FIGHTING'] = False
				#MISS
				if gottem == False:
					res.MIXER[0].play(res.SOUND['MISS'])
					self.hitisplay(5, self.aim, dtb.MENU['miss'], (200, 200, 200))
				self.mnu = 0
			#RUN AWAY
			elif self.equip[self.turn] == 7:
				self.dialog([self.fig[self.turn]['NAME'] + dtb.BATTLE[15]])
				run = round(np.random.randint(0,30)) + self.fig[self.turn]['ATLETISM']
				if run > 20:
					pygame.mixer.music.fadeout(500)
					pygame.mixer.music.fadeout(500)
					self.dialog([dtb.BATTLE[17]])
					res.CHARACTERS[res.PARTY[res.FORMATION][0]]['MORALITY'] += 1
					self.transiction(True, int(self.display.height/2))
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
				if d['VITALITY'] <= 0: dth += 1
			if dth < len(self.foe) + len(self.mrc) and self.battle and again:
				res.MIXER[1].play(res.SOUND['ONE_MORE'])
				self.hitisplay(0, self.aim, dtb.MENU['one_more'], (10, 50, 255))
				self.turn -= 1
			if self.turn < len(self.fig):
				self.aim.x = 100 + dtb.CLASSES[self.fig[self.turn]['CLASS']]['STRENGHT'][self.fig[self.turn]['LEVEL']]
		#ENEMIES TURN
		else:
			self.guis['INVENTORY'].gui.type = 0
			self.phone = 0
			self.tbt += round(self.btime/10)
			self.btime = 100
			self.mnu = 3
			count = 0
			for i in self.foe + self.mrc:
				if i['VITALITY'] > 0 and i['FIGHTING'] and i['HEALTH'] != 1 and len(self.fig) > 0:
					count += 1
					if count == 6: break
					#CONDITION DAMAGE
					if i['HEALTH'] > 15:
						i['VITALITY'] -= 5
						self.hitisplay(5, i['MASK'], str(5), (200, 0, 0))
					#HABILITY
					prb = []
					for h in i['HABILITIES']:
						prb.append(h[4])
					opt = int(np.random.randint(0,100))
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
						if d['VITALITY'] > 0: otk += 1
					if i['HEALTH'] == 9: pl = int(np.random.randint(-20,len(self.fig) - 1 + otk))
					else: pl = int(np.random.randint(-1,len(self.fig) - 1 + otk))
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
									vst = self.guis['INVENTORY'].gui.find(pl,'vest','value')
									if vst != None:
										act[2] += int(dtb.ITEMS[res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3]]][5])
										vst[1] -= 1
										if vst[1] <= 0: res.MIXER[1].play(res.SOUND['MENU_BACK'])
										res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3] + 1] = str(vst[1])
									#FEAR
									if self.fig[pl]['FEAR'] == i['TYPE']: act[2] *= 1.5
									act[2] += i['RESISTANCE'] - self.fig[pl]['RESISTANCE']
									self.turn = self.fig[pl]['N']
									res.MIXER[1].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
									res.MIXER[0].play(res.SOUND['DAMAGE_1'])
									#DODGE
									if self.attackimation(act[5]):
										act[2] -= np.floor(act[2]/5)
										self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
									#CRITICAL
									if -act[2] > int(self.fig[self.turn]['RESISTANCE']/4):
										if self.fig[pl]['VITALITY'] <= 0: self.fig[pl]['VITALITY'] -= 1
										else: self.fig[pl]['VITALITY'] += act[2] + self.fig[pl]['RESISTANCE']
										self.hitisplay(-act[2] * 2, True, '', (0,0,0))
										self.fig[pl]['HEALTH'] = 15
										res.MIXER[1].play(res.SOUND['INCONSCIOUS'])
									#HIT
									elif -act[2] > 0:
										if self.fig[pl]['VITALITY'] <= 0: self.fig[pl]['VITALITY'] -= 1
										else: self.fig[pl]['VITALITY'] += act[2] + self.fig[pl]['RESISTANCE']
										self.hitisplay(-act[2] * 2, False, '', (0,0,0))
									#NO DAMAGE
									else:
										if self.fig[pl]['VITALITY'] > 0: self.fig[pl]['VITALITY'] += -1
										self.hitisplay(2, None, '', (0,0,0))
									self.hpl += act[2]
								else:
									#ATTACK MERCENARY
									if i['TYPE'] != 'mercenary':
										res.MIXER[0].play(res.SOUND['HIT'])
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.mrc[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.mrc[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.mrc[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.mrc[pl - len(self.fig)]['VITALITY'] += act[2]
									#ATTACK FREAK
									else:
										res.MIXER[0].play(res.SOUND['HIT'])
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[pl - len(self.fig)]['FILE']) + '_damage.png')
										self.hitisplay(10, self.foe[pl - len(self.fig)]['MASK'], str(act[2]), (0, 200, 0))
										self.foe[pl - len(self.fig)]['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (self.foe[pl - len(self.fig)]['FILE']) + '_stand.png')
										self.foe[pl - len(self.fig)]['VITALITY'] += act[2]
							#SELF HEALING
							elif act[2] > 0:
								res.MIXER[1].play(res.SOUND['HEAL'])
								i['VITALITY'] += act[2]
						elif act[3] in [2,3,4,5]:
							lst = ('STRENGHT','AGILITY','RESISTANCE','CHARISMA')
							#REDUCE ATTRIBUTE
							if act[2] < 0 and ['BTIMES'][act[3] - 2] < 2:
								self.turn = self.fig[pl]['N']
								res.MIXER[1].play(res.SOUND['ATTRIBUTE_LOSS'])
								self.fig[pl]['STRENGHT'] += act[2]
								self.hitisplay(5, i['MASK'], '-' + str(act[2]) + ' ' + dtb.PROFNAMES[lst[act[3] - 2]], (200, 10, 10))
								i['BTIMES'][act[3] - 2] += 1
							#GROW ATTRIBUTE
							elif act[2] > 0:
								i[lst[act[3] - 2]] += act[2]
								res.MIXER[1].play(res.SOUND['ATTRIBUTE_GAIN'])
								self.hitisplay(5, i['MASK'], '+' + str(act[2]) + ' ' + dtb.PROFNAMES[lst[act[3] - 2]], (200, 10, 10))
						#INPUT CONDITION
						elif act[3] == 6:
							self.fig[pl]['HEALTH'] = act[2]
							if self.fig[pl]['HEALTH'] == 5: self.fig[pl]['AGILITY'] -= 20
							res.MIXER[1].play(res.SOUND['ATTRIBUTE_LOSS'])
							self.hitisplay(5, i['MASK'], dtb.FCONDITIONS[act[2]], (10, 10, 10))
						#ADD ANOMALY
						elif act[3] == 7:
							prb = round(np.random.randint(0,100))
							if prb > 49:
								wh = round(np.random.randint(0,len(act[2]) - 1))
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
							i['VITALITY'] = 0
						#CHARGE ATTACK
						elif act[3] == 10:
							res.MIXER[1].play(res.SOUND['CHARGE'])
							self.attackimation(act[5])
							self.turn = self.fig[pl]['N']
							res.MIXER[1].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
							res.MIXER[0].play(res.SOUND['DAMAGE_1'])
							if self.attackimation(act[5]) == False:
								act[2] -= int(act[2]/5)
								self.fig[pl]['VITALITY'] += act[2] + self.fig[pl]['RESISTANCE']
								self.hitisplay(-act[2] * 2, None, '', (0,0,0))
								self.hpl += act[2]
							else:
								res.MIXER[0].play(res.SOUND['HIT'])
								for p in range(dmg * 3):
									self.particles.append({'TYPE': 'blood', 'X': self.aim.x, 'Y': self.aim.y, 'RADIUS': round(np.random.randint(3,5)), 'DIRECTION': round(np.random.randint(0,360)), 'SPEED': round(np.random.randint(2,6))})
								self.hitisplay(10, i['MASK'], str(act[2]), (200, 0, 0))
								if i['HEALTH'] != 1: i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE'])+ '_stand.png')
								i['VITALITY'] -= act[2]
								self.hits += 1
								self.tdmg += act[2]
							#COUNTER DAMAGE
							if i['VITALITY'] <= 0:
								res.MIXER[1].play(res.SOUND['SCREAM' + str(dtb.FREAKS[i['FILE']]['SCREAM'])])
								while i['FADE'] > 0:
									i['FADE'] -= 0.5
									self.run()
								if i['ITEM'] != None:
									prb = round(np.random.randint(0,100))
									if prb > i['ITEM'][1]:
										self.guis['INVENTORY'].gui.add(res.PARTY[res.FORMATION][0],i['ITEM'][0])
										res.MIXER[0].play(res.SOUND['ITEM_GET'])
										self.notification.append({'TEXT': 'it_' + i['ITEM'][0], 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
								i['FIGHTING'] = False
						#CHECK DEATH
						if pl < len(self.fig) and self.fig[pl]['VITALITY'] <= 0:
							self.mnu = 1
							#PERMADEATH
							if self.fig[pl]['HEALTH'] == 15 and self.fig[pl]['VITALITY'] < 0:
								if self.fig[pl]['VITALITY'] > -5: self.fig[pl]['VITALITY'] -= 1
								else: res.MIXER[1].play(res.SOUND['DEATH'])
							else:
								#FAINT
								if self.fig[pl]['BLESS'] == 0:
									self.fig[pl]['VITALITY'] = 0
									self.fig[pl]['HEALTH'] = 15
									res.MIXER[1].play(res.SOUND['INCONSCIOUS'])
								#REVIVE
								else:
									self.fig[pl]['BLESS'] -= 1
									self.fig[pl]['VITALITY'] = dtb.CLASSES[self.fig[pl]['CLASS']]['RESISTANCE'][self.fig[pl]['LEVEL']]
									res.MIXER[1].play(res.SOUND['REVIVE'])
						i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']).lower() + '_stand.png')
					#MISS
					else:
						i['SPRITE'] = pygame.image.load(res.FREAKS_PATH + (i['FILE']).lower() + '_stand.png')
						res.MIXER[0].play(res.SOUND['MISS'])
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
				vst = self.guis['INVENTORY'].gui.find(pl,'vest','value')
				if vst != None:
					dmg[p] += int(dtb.ITEMS[res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3]]][5])
					vst[1] -= 1
					if vst[1] <= 0: res.MIXER[1].play(res.SOUND['MENU_BACK'])
					res.INVENTORY[vst[0][0]][vst[0][1]][vst[0][2]][vst[0][3] + 1] = str(vst[1])
			if self.attackimation(1):
				for p in range(len(self.fig)): dmg -= int(dmg/5)
				self.hitisplay(5, i['MASK'], 'dodge', (0, 200, 0))
			else:
				for p in range(len(self.fig)): self.fig[p]['VITALITY'] += dmg[p] + self.fig[p]['RESISTANCE']
				self.hitisplay(-dmg[p] * 2, None, '', (0,0,0))
				res.MIXER[0].play(res.SOUND['DAMAGE_1'])
				self.hpl += dmg[p]
			self.mnu = 1
		#VICTORY
		dth = 0
		for d in self.foe + self.mrc:
			if d['VITALITY'] <= 0: dth += 1
		if dth == len(self.foe) + len(self.mrc) and self.battle:
			pygame.mixer.music.fadeout(500)
			pygame.mixer.music.fadeout(500)
			if len(self.foe) >= 10: res.MIXER[1].play(res.SOUND['BATTLE_BOSS_WON'])
			elif len(self.foe) > 0 and self.foe[0]['TYPE'] == 'boss': res.MIXER[1].play(res.SOUND['BATTLE_BOSS_WON'])
			elif self.hpl == 0: res.MIXER[1].play(res.SOUND['BATTLE_PERFECT'])
			else: res.MIXER[1].play(res.SOUND['BATTLE_WON'])
			self.tbt += round(self.btime/10)
			xp = int(((self.hits*self.tdmg)-self.hpl+self.tbt)/len(self.fig))
			self.mnu = self.display.width
			while self.sttsy > 120:
				self.sttsy -= 10
				self.run()
			self.transiction(True, int(self.display.height/2) + 10)
			self.turn = -4
			self.obstacles = False
			while self.mnu > 0:
				self.mnu -= 60
				self.run()
			self.wait()
			#GREENBLOOD
			btls = None
			for i in res.PARTY[res.FORMATION]:
				for it in ['tube100','tube250']:
					btls = self.guis['INVENTORY'].gui.find(i,it,'value')
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
				res.CHARACTERS[i]['EXPERIENCE'] += xp
				plux = int(100/(dtb.NEXTLEVEL[res.CHARACTERS[i]['LEVEL']]/res.CHARACTERS[i]['EXPERIENCE']))
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
						self.bbg.index = pygame.image.load(res.BACKG_PATH + 'level_up.png')
						res.MIXER[1].play(res.SOUND['LEVEL_UP'],-1)
						self.transiction(False, int(200/res.GSCALE), 10)
						lvlup = True
					if self.mnu < -self.display.width:
						self.mnu = -self.display.width
					while self.mnu > -(self.display.width + 100):
						self.mnu -= 50
						self.run()
					self.exvar += 1
					self.barxp[i] = 0
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL'] += 1
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['VITALITY'] += dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][i]]['CLASS']]['RESISTANCE'][res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL']] - dtb.CLASSES[res.CHARACTERS[res.PARTY[res.FORMATION][i]]['CLASS']]['RESISTANCE'][res.CHARACTERS[res.PARTY[res.FORMATION][i]]['LEVEL'] - 1]
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['EXPERIENCE'] = 0
					self.wait()
					self.lopt = np.random.randint(0,6)
					res.CHARACTERS[res.PARTY[res.FORMATION][i]]['BONUS'][1] += self.lopt
					self.wait()
					while self.mnu > -((self.display.width * 2) + 200):
						self.mnu -= 50
						self.run()
			if lvlup:
				self.transiction(True, 210, 10)
				res.MIXER[1].fadeout(2500)
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
					self.display.x = dv * res.GSCALE
					self.display.y = 0
					dv += ex * 10
					if dv > self.display.width * 1.25:
						dv = 1
						ex -= 3
						if ex < 0: ex = 0
				else:
					self.display.x = ex
					self.display.y = ex
					if ex > 0:
						ex = -ex
					elif ex < 0:
						ex = -ex
						ex -= dv
				self.run()
			self.display.x = 0
			self.display.y = 0
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
		rectdebug = False
		if rectdebug: rctdbg = pygame.Surface((p['RECT'].width,p['RECT'].height)); rctdbg.fill((200,0,0))
		#POP
		if p['TYPE'] == '':
			img = pygame.image.load(res.SPRITES_PATH + 'pop_' + str(int(p['GIF'])) + '.png').convert_alpha()
			self.surfaces[1].blit(img,(p['RECT'].x - self.cam.x,p['RECT'].y - self.cam.y))
			if p['GIF'] < 8: p['GIF'] += 0.5
			if p['GIF'] >= 8: p['DESTROY'] = True
		
		#TEXT
		elif p['TYPE'] == 'text':
			srf = pygame.Surface((100,50),pygame.SRCALPHA)
			srf.fill((0,0,0,0))
			srf.set_alpha(p['ALPHA'])
			if p['TIME'] > 0:
				if p['SHAKE'] != 0:
					p['RECT'].x += p['SHAKE']
					p['RECT'].y += p['SHAKE']
					p['SHAKE'] = -p['SHAKE']
					if p['SHAKE'] > 0: p['SHAKE'] -= 1

				if p['GRAVITY']  < p['GRAVLIMIT']:
					p['RECT'].y += p['GRAVITY']
					p['GRAVITY'] += p['GRAVACC']
					if p['GRAVITY'] < 0 and p['TYPE'] == 1: p['SHADE'] += 1
				elif p['SHAKE'] == 0: p['TIME'] -= 1
				srf.blit(res.FONTS['SCORETXT'].render(p['TEXT'], True, (0,0,0)), (11 - p['SHADE'], 11 - p['SHADE']))
				srf.blit(res.FONTS['SCORETXT'].render(p['TEXT'], True, p['COLOR'] ), (10 - p['SHADE'], 10 - p['SHADE']))
			elif p['ALPHA'] > 0: p['ALPHA'] -= p['ALPHADE']
			else: p['DESTROY'] = True
			self.surfaces[1].blit(srf,(p['RECT'].x, p['RECT'].y))
		
		#BOMB
		elif p['TYPE'] == 'bomb':
			if np.floor(p['GIF']) < len(p['IMAGE']):
				self.surfaces[1].blit(p['IMAGE'][np.floor(p['GIF'])],(p['RECT'].x - self.cam.x,p['RECT'].y - self.cam.y))
			p['GIF'] += 0.5
			if int(p['GIF']) >= len(p['IMAGE']):
				#DESTROY BRICKS
				if p['POWER'] == 0:
					for obj in self.objects:
						if obj[0] == 'move' and obj[1]['TYPE'] == 'DESTROY':
							if self.colide(obj[1]['RECT'], pygame.Rect(p['RECT'].x - int((self.map.tilewidth * 3)/2),p['RECT'].y - int((self.map.tileheight * 3)/2),self.map.tilewidth * 3,self.map.tileheight * 3)):
								prb = np.random.randint(0,30)
								if prb > 20:
									pit = np.random.randint(0,100)
									if pit > 90: it = 'pow_speed'
									elif pit > 80: it = 'pow_speed'
									elif pit > 40: it = 'pow_bubble'
									else: it = 'bomb_regular'
									img = pygame.image.load(res.ITEMS_PATH + it + '.png')
									self.objects.append(['item',{'IMAGE': img,'ITEM': it,'RECT':p['RECT'],'FLOAT': 0,'ACC': 3,'DIRECTION': False,'DESTROY': False},100])
								for i in range(10):
									self.particles.append({'TYPE': 'spin','IMAGE': pygame.image.load(res.SPRITES_PATH + 'brick.png'),'DIRECTION': np.random.randint(1,6),'SPIN': 0,'TIME': 0,'X': obj[1]['RECT'].x,'Y': obj[1]['RECT'].y})
								obj[1]['DESTROY'] = True
					self.particles.append({'TYPE': 'explode','GIF': 0.0,'TIME': 0,'RECT': p['RECT'].copy(),'LIMIT': 3})
					res.MIXER[1].play(res.SOUND['EXPLOSION_' + str(np.random.randint(1,4))])
				if p['POWER'] == 1:
					rct = [{'TYPE': 'SLIME'},pygame.Rect(np.floor(p['RECT'].x/self.map.tilewidth) * self.map.tilewidth,np.floor(p['RECT'].y/self.map.tileheight) * self.map.tileheight,self.map.tilewidth,self.map.tileheight)]
					self.tilrect[1][(np.floor((p['RECT'].y + 15)/self.map.tilewidth) * self.map.width) + np.floor((p['RECT'].x + 15)/self.map.tilewidth)] = rct
		
		#EXPLODE
		elif p['TYPE'] == 'explode':
			img = pygame.image.load(res.SPRITES_PATH + 'explode_' + str(np.floor(p['GIF']).astype(int)) + '.png').convert_alpha()
			self.surfaces[1].blit(img,(p['RECT'].x - int(img.get_width()/2) - self.cam.x,p['RECT'].y - int(img.get_height()/2) - self.cam.y))
			p['GIF'] += 1
			if p['GIF'] >= p['LIMIT']: p['GIF'] = 0
			p['TIME'] += 1
			if p['TIME'] >= 30: p['DESTROY'] = True
		
		#RAINDROP
		elif p['TYPE'] == 'raindrop' and self.turn != -6:
			rd = False
			if p['TIME'] <= 0:
				rd = True
				for i in self.areas:
					if self.colide(i['RECT'],p['RECT']):
						rd = False
						break
			if rd == False:
				p['TIME'] -= 1
				p['RECT'].x += int(np.cos(p['DIRECTION']) * p['SPEED'])
				p['RECT'].y += int(np.sin(p['DIRECTION']) * p['SPEED'])
				self.surfaces[1].blit(p['IMAGE'], (p['RECT'].x,p['RECT'].y))
				if p['TIME'] == 0:
					p['RECT'].x = p['RECT'].x + self.cam.x
					p['RECT'].y = p['RECT'].y + self.cam.y
			elif p['GIF'] <= 8:
				self.surfaces[1].blit(pygame.image.load(res.SPRITES_PATH + 'raindrop_' + str(p['GIF']) + '.png'), (p['RECT'].x - self.cam.x + 4,p['RECT'].y -self.cam.y + 6))
				p['GIF'] += 1
			if p['GIF'] > 8: p['DESTROY'] = True
		
		#GREENBLOOD & GUNSHOT
		elif p['TYPE'] in ['pop','blood','gunshot','megunshot']:
			p['RECT'].x += int(np.cos(p['DIRECTION']) * p['SPEED'])
			p['RECT'].y += int(np.sin(p['DIRECTION']) * p['SPEED'])
			if p['TYPE'] == 'blood':
				p['RADIUS'] -= p['FADE']
				if p['RADIUS'] < 0.0: p['RADIUS'] = 0.0
				rct = pygame.Rect(p['RECT'].x,p['RECT'].y,p['RADIUS'] * 2,p['RADIUS'] * 2)
			else: rct = pygame.Rect(p['RECT'].x - self.cam.x,p['RECT'].y - self.cam.y,p['RECT'].width,p['RECT'].height)

			if 'IMAGE' in p.keys():
				if p['GIF'] < len(p['IMAGE']) - 1: p['GIF'] += 0.5
				if p['GIF'] >= len(p['IMAGE']) - 1:
					if p['IMAGE'][np.floor(p['GIF']).astype(int)] == None: p['DESTROY'] = True
					p['GIF'] = 0.0
				if p['IMAGE'][np.floor(p['GIF']).astype(int)]:
					self.surfaces[1].blit(p['IMAGE'][np.floor(p['GIF']).astype(int)], (rct.x,rct.y))
			else: pygame.draw.ellipse(self.surfaces[1], p['COLOR'], rct)
			
			if p['RADIUS'] <= 0.0: p['DESTROY'] = True
			if p['TYPE'] == 'gunshot':
				if pygame.Rect.colliderect(p['RECT'],self.cam) == False: p['DESTROY'] = True

			if p['TYPE'] == 'megunshot':
				self.objects.append(['particle',{'TYPE': 'blood','RECT': p['RECT'].copy(),'COLOR': (200,200,200),'RADIUS': 6,'FADE': 0.5,
					'DIRECTION': 0, 'SPEED': 0,'EMISSOR': p,'DEPTH': 0,'DESTROY': False},0])
		
		#SPIN
		elif p['TYPE'] == 'spin':
			p['RECT'].x += int(np.cos(p['DIRECTION']) * 5)
			p['RECT'].y += int(np.sin(p['DIRECTION']) * 5)
			cor = (p['RECT'].x - self.cam.x,p['RECT'].y - self.cam.y)
			self.surfaces[1].blit(pygame.transform.rotate(p['IMAGE'],p['SPIN']),cor)
			p['SPIN'] += 10
			p['TIME'] += 1
			if p['TIME'] >= 30: p['DESTROY'] = True
	
	def draw(self):
		for i in self.surfaces: i.fill((0,0,0,0))
		if self.guis['BKG'].show: self.surfaces[1].blit(self.guis['BKG'].draw(), (0,0))
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 12: self.surfaces[0].fill((0,0,0))
		
		#TILED MAP
		elif self.map and self.turn != -6:
			self.map.draw()
			for i in self.map.surfaces: self.surfaces[1].blit(i,(0,0),(self.cam.x,self.cam.y,self.display.width,self.display.height))
			#PROPS
			xxxx = False
			if xxxx:
				ind = 0
				for i in list(filter(lambda item: item != None, self.tilrect[0] + self.tilrect[1])):
					if i != None:
						if i[0]['TYPE'] == 'COLOR':
							if i[0]['SCALE'] == self.map.tilewidth: img = i[0]['IMAGE'][i[0]['COLOR']]
							else:
								img = pygame.transform.scale(i[0]['IMAGE'][i[0]['COLOR']],(i[0]['SCALE'],self.map.tileheight))
								i[0]['SCALE'] += 1
							self.surfaces[0].blit(img, (i[1].x - self.cam.x, i[1].y - self.cam.y))
						if i[0]['TYPE'] in ['TREADMILL','PORTAL']:
							self.surfaces[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
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
							res.MIXER[1].set_volume(i[0]['SFX'] * res.SFX)
							res.MIXER[1].play(res.SOUND['STEP_MOTOR'])"""
						if i[0]['TYPE'] == 'MOVING':
							self.surfaces[0].blit(i[0]['IMAGE'], (i[1].x - self.cam.x, i[1].y - self.cam.y))
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
							self.surfaces[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
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
							self.surfaces[0].blit(i[0]['IMAGE'][int(i[0]['GIF'])], (i[1].x - self.cam.x, i[1].y - self.cam.y))
							if i[0]['GIF'] > 0: i[0]['GIF'] += 0.5
							if int(i[0]['GIF']) == len(i[0]['IMAGE']) - 1: i[0]['GIF'] = 0
						if i[0]['TYPE'] == 'SLIME':
							self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'slime.png'), (i[1].x - self.cam.x, i[1].y - self.cam.y))
					ind += 1
		#for t in self.tilrect[3]:
		#	if self.rectdebug and t!= None: pygame.draw.rect(self.surfaces[0],(255,0,0),pygame.Rect(t[1].x - self.cam.x,t[1].y - self.cam.y,t[1].width,t[1].height),3)
		
		#DEPTH
		dpth = 0
		for i in range(len(self.objects)):
			if i != len(self.objects) - 1:
				if self.objects[i][2] > self.objects[i + 1][2]:
					self.objects.insert(i, self.objects[i + 1])
					del self.objects[i + 2]
		#DELETE OBJECTS
		self.objects = [i for i in self.objects if i[0] in ['char','sign'] if i[1].destroy == False] + \
			[i for i in self.objects if i[0] in ['item','move','click','particle'] and i[1]['DESTROY'] == False]
		#OVERWORLD
		if self.battle == False:
			#OBJECTS
			rqstlst = []
			cm = pygame.Rect(self.cam.x - 100,self.cam.y - 100,self.cam.width + 200,self.cam.height + 200)
			#print([i[0] for i in self.objects])
			for y in self.objects:
				obj = y[1]
				#CHARACTER
				if y[0] == 'char' and self.colide(obj.rect,cm):
					obj.overworld_draw(self.surfaces[1],self.cam)
					if obj.file in dtb.FREAKS.keys(): obj.overworld_move()

					#HOLDFIRE BAR
					if obj.holdfire > 15: self.surfaces[1].blit(tools.draw.bar((obj.holdfire,100),(20,40),(10,10,10),(200,10,10),'stack',5),(obj.rect.x,obj.rect.y))

					#if self.map.hscroll != 0 and i['RECT'].x < self.cam.x - self.map.tilewidth: res.CHARACTERS[res.PARTY[res.FORMATION][obj.index]]['VITALITY'] = 0
					#if self.map.vscroll != 0 and i['RECT'].y < self.cam.y - self.map.tileheight: res.CHARACTERS[res.PARTY[res.FORMATION][obj.index]]['VITALITY'] = 0

					#CHARACTER COLISION
					for i in [o for o in self.objects if o[0] in ['char','particle','item'] and o[1] != obj]: obj.colide(i)

					#TILE COLISION
					for tl in range(0):
						if i['STEP'] > 0: i['STEP'] -= 1
						ind = (np.floor((i['RECT'].y + 15)/self.map.tileheight) * self.map.width) + np.floor((i['RECT'].x + 15)/self.map.tilewidth)
						t = self.tilrect[tl][ind]
						if t != None:
							if self.rectdebug:
								if tl == 0: pygame.draw.rect(self.surfaces[0],(255,255,0),pygame.Rect(t[1].x + 2 - self.cam.x,t[1].y + 2 - self.cam.y,t[1].width - 4,t[1].height - 4),3)
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
											if res.CHARACTERS[res.PARTY[res.FORMATION][p]]['VITALITY'] > 0:
												res.CHARACTERS[res.PARTY[res.FORMATION][p]]['VITALITY'] -= 5
												res.MIXER[1].play(res.SOUND['BATTLE_LOST'])
												self.player[p]['INVFRM'] = 60
												while self.sttsy < 120:
													self.sttsy += 10
													self.run()
											else:
												res.MIXER[1].play(res.SOUND['GAME_OVER'])
									#JUMP
									elif t[0]['TYPE'] == 'JUMP' and i['GRAVITY'] == -5:
										if t[0]['DIRECTION'] == 0: i['GIF'] = 1; do = True
										elif i['DIRECTION'] == int(t[0]['DIRECTION']): do = True
										else: do = False
										if do:
											i['GRAVITY'] = 4.5 + float(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['ACROBATICS']/2)
											i['STEP'] = 0
											res.MIXER[0].play(res.SOUND['FALL'])
									#HOLE
									elif t[0]['TYPE'] == 'HOLE' and self.colide(i['RECT'],t[1]):
										res.CHARACTERS[res.PARTY[res.FORMATION][p]]['VITALITY'] = 0
									#SLIME
									elif t[0]['TYPE'] == 'SLIME' and self.colide(i['RECT'],t[1]): i['ACC'] = 0.5
									else: i['ACC'] = 0
								if i['DRIVING'] == None and i['SPEED'] > 0:
									#STEP SOUNDS
									if t[0]['TYPE'] not in ['NONE','BACKGROUND','SKY','CLOTH','JUMP','SPIKE','HOLE','SLIME','TUNNEL'] and i['JUMP'] == 0:
										if i['STEP'] == 0 and res.MAP != 'rodoviary':
											'''#PROPS SOUND
											elif t[0]['TYPE'] in ['TREADMILL','MOVING']:
												self.soundplay('STEP_METAL',0)
											#REGULAR SOUND
											elif t[0]['TYPE'] != 'WALL':
												self.soundplay('STEP_' + t[0]['TYPE'],0)'''
											if i['SPEED'] > 0: i['STEP'] = np.floor(12/i['SPEED'])
										#SWIMMING
										if t[0]['TYPE'] == 'WATER':
											if i['SWIM'] == None: i['SWIM'] = 0.0
										else: i['SWIM'] = None
								#DRIVING
								elif i['DRIVING'] != None and t[0]['TYPE'] != 'WALL' and t[0]['TYPE'].startswith('JUMP') == False and i['JUMP'] == 0:
									if i['STEP'] == 0 and res.MAP != 'rodoviary':
										self.soundplay('STEP_MOTOR',0)
										if i['SPEED'] > 0: i['STEP'] = np.floor(12/i['SPEED'])
					y[2] = obj.rect.y
				
				#PORTALS
				if y[0] == 'portal' and self.colide(obj['RECT'],cm): self.portal(obj); y[2] = y[1]['RECT'].y
				
				#PARTICLES
				if y[0] == 'particle': self.particle(y[1]); y[2] = 0
				
				#ITEMS
				elif y[0] == 'item':
					if pygame.Rect.colliderect(y[1]['RECT'],cm):
						y[1]['FLOAT'] = int(np.sin(y[1]['ACC']) * y[1]['ACCLIMIT'])
						y[1]['ACC'] += y[1]['ACCSPD']
						self.surfaces[1].blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y + y[1]['FLOAT']))
					y[2] = y[1]['RECT'].y

				#SIGNS
				elif y[0] == 'sign':
					if self.colide(y[1]['RECT'],cm) and self.turn != -6:
						if res.MAP != 'rodoviary':
							sz = res.FONTS['DEFAULT'].size(dtb.SIGNS[y[1]['TEXT']])
							pygame.draw.rect(self.surfaces[0], (250, 250, 250), pygame.Rect(y[1]['RECT'].x - self.cam.x, y[1]['RECT'].y - self.cam.y, np.floor(sz[0]/2) + 10, np.floor(sz[1]/2) + 10))
							self.surfaces[1].blit(res.FONTS['DEFAULT'].render(dtb.SIGNS[y[1]['TEXT']], True, (0,0,0)), ((5 + y[1]['RECT'].x - self.cam.x) * res.GSCALE,(5 + y[1]['RECT'].y - self.cam.y) * res.GSCALE))
						else: self.surfaces[1].blit(res.FONTS['DEFAULT'].render(y[1]['TEXT'], True, (250,250,250)), ((y[1]['RECT'].x - self.cam.x - np.floor(self.cam.x/5)) * res.GSCALE,(y[1]['RECT'].y - self.cam.y - np.floor(self.cam.y/5)) * res.GSCALE))
					y[2] = y[1]['RECT'].y

				#MOVE
				elif obj == 'move':
					if self.colide(y[1]['RECT'],cm):
						self.surfaces[0].blit(y[1]['IMAGE'],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - self.map.tileheight))
						if self.rectdebug: pygame.draw.rect(self.surfaces[0], (0,0,255), pygame.Rect(y[1]['RECT'].x - self.cam.x, y[1]['RECT'].y - self.cam.y, y[1]['RECT'].width, y[1]['RECT'].height),3)
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
				elif obj == 'toll':
					if self.colide(y[1]['RECT'],cm):
						srf = pygame.Surface((44,44), pygame.SRCALPHA)
						trs = pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'toll.png'),y[1]['ANGLE'] + 90)
						#i['CENTER'] = trs.get_rect(center = i['CENTER'].center)
						srf.blit(trs,(0,0))
						self.surfaces[0].blit(srf,(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y))
						if y[1]['TIME'] > 0: y[1]['TIME'] -= 1
						if self.colide(self.player[0]['RECT'],y[1]['RECT']):
							if y[1]['TIME'] == 0:
								mny = self.guis['INVENTORY'].gui.find(None,'credit_card','value')
								if mny != None and mny[1] >= 10:
									res.MIXER[0].play(res.SOUND['BUY'])
									mny[1] -= 10
									y[1]['TIME'] = 180
									self.notification.append({'TEXT': 'Pedágio -$ 10', 'COLOR': (255, 255, 255), 'HALIGN': 'left','X': 0})
								elif self.facing(self.player[0],y[1]['RECT']) == 2:
									self.player[0]['SPEED'] = 0
					y[2] = y[1]['RECT'].y
				#RADARS
				elif obj == 'radar':
					if self.colide(y[1]['RECT'],cm):
						if self.colide(self.player[0]['RECT'],y[1]['RECT']):
							for j in self.objects:
								if j[0] == 5 and j[1]['TEXT'] == 'radar' + str(0):
									j[1]['TEXT'] = self.player[0]['SPEED']
							if self.player[0]['SPEED'] > y[1]['LIMIT']:
								res.MIXER[0].play(res.SOUND['BUY'])
								mny = self.guis['INVENTORY'].gui.find(None,'credit_card','value')
								if mny != None: mny[1] -= 10
					y[2] = y[1]['RECT'].y
				#TENTS
				elif obj == 'tent':
					if self.colide(y[1]['RECT'],cm):
						self.surfaces[0].blit(y[1]['SPRITE'],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - 20))
						for p in self.player:
							if self.colide(p['RECT'],y[1]['RECT']):
								 self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (y[1]['RECT'].x - self.cam.x + int(y[1]['RECT'].width/2) - 5,y[1]['RECT'].y - self.cam.y - y[1]['RECT'].height * 2))
								 if self.pressed[4][0]: p['SLEEP'] = not p['SLEEP']
					y[2] = y[1]['RECT'].y
				#PETS
				elif obj == 'pet' and self.colide(y[1]['RECT'],cm): self.pet(y[1]); y[2] = y[1]['RECT'].y
				#TILES
				elif obj == 11:
					self.surfaces[0].blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y)); y[2] = y[1]['RECT'].y
				#CLICK
				elif obj == 'click':
					y[1]['GIF'] += 0.1
					if np.floor(y[1]['GIF']) >= len(y[1]['IMAGE']):
						y[1]['GIF'] = 0
					self.surfaces[0].blit(y[1]['IMAGE'][np.floor(y[1]['GIF'])],(y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y - 20))
					if self.colide(self.player[0]['RECT'],y[1]['RECT']): y[1]['DESTROY'] = True
					y[2] = y[1]['RECT'].y
			self.objects += rqstlst

			#BUILD ITEMS
			if self.build != '':
				srf = pygame.image.load(res.SPRITES_PATH + '' + self.build + '.png')
				srf.set_alpha(100)
				self.surfaces[0].blit(srf,((np.floor((self.player[0]['RECT'].x + 15)/30) * 30) - self.cam.x,(np.floor((self.player[0]['RECT'].y + 15)/30) * 30) - self.cam.y - 20))
			#NODES DEBUG
			if self.rectdebug:
				for i in self.nodes: pygame.draw.rect(self.surfaces[0], (250,250,10),pygame.Rect(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y, i['RECT'].width, i['RECT'].height))
			#OVER TILES & CLOUDS
			if self.map: pass
			#DAYTIME & WEATHER
			if res.TIME[0] >= 18: tim = 100
			elif res.TIME[0] >= 6: tim = 0
			else: tim = 100
			srf = pygame.Surface((self.display.width,self.display.height))
			srf.set_alpha(tim)
			srf.fill((0, 58, 160))
			#LIGHTS
			for y in self.objects:
				if obj == 'light':
					if self.colide(y[1]['RECT'], self.cam):
						srf.blit(y[1]['IMAGE'], (y[1]['RECT'].x - self.cam.x,y[1]['RECT'].y - self.cam.y),None,pygame.BLEND_RGBA_SUB)
			if self.map and self.map.interior == 0: self.surfaces[0].blit(srf, (0,0))
			#RAIN
			if self.map and self.map.interior == 0 and res.WEATHER == 1 and res.MAP != 'rodoviary':
				if len(self.particles) < 100:
					for i in range(5):
						img = pygame.Surface((2,2),pygame.SRCALPHA)
						pygame.draw.circle(img,(0, 148, 255),(1,1),2)
						img.set_alpha(120)
						self.particles.append({'IMAGE': img,'TYPE': 'raindrop', 'X': round(np.random.randint(0,self.cam.width + int(self.cam.width/4))), 'Y': -int(self.cam.height/2),
							'RADIUS': 2, 'DIRECTION': 90, 'SPEED': 15, 'TIME': round(np.random.randint(10,60)), 'GIF': 0})

			#DRIVING BARS
			for p in self.player:
				if p['DRIVING'] != None:
					pygame.draw.rect(self.surfaces[0], (10,10,10), pygame.Rect(20,20,100,20))
					if res.GAS >= 1: pygame.draw.rect(self.surfaces[0], (255,155,66), pygame.Rect(20,20,int(100/(self.vehicles[p['DRIVING']]['CAPACITY']/round(res.GAS))),20))
					pygame.draw.rect(self.surfaces[0], (10,10,10), pygame.Rect(20,42,100,20))
					if p['SPEED'] > 0: pygame.draw.rect(self.surfaces[0], (0,255,0), pygame.Rect(20,42,int(100/(20/p['SPEED'])),20))
					res.HINTEXT = 'VEHICLE_CONTROLS'
			#PORTALGO
			if self.portalgo != {}:
				if self.rectdebug: pygame.draw.rect(self.surfaces[0], (255,0,0), pygame.Rect(self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y, self.portalgo[0]['RECT'].width, self.portalgo[0]['RECT'].height))
				if self.portalgo[0]['RECT'].width == 24: self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_01.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				if self.portalgo[0]['RECT'].width == 48: self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'door_11.png'), (self.portalgo[0]['RECT'].x, self.portalgo[0]['RECT'].y))
				self.portalgo[1]['RECT'].x = self.portalgo[0]['RECT'].x + self.cam.x
				self.portalgo[1]['RECT'].y = self.portalgo[0]['RECT'].y + self.cam.y + 20
				self.doll(self.portalgo[1],True)
				for i in self.objects:
					if i[0] == 4 and self.portalgo[0]['MATCH'] != None and i[1]['MATCH'] == self.portalgo[0]['MATCH']:
						self.cam.x += int((i[1]['RECT'].x  - self.cam.x - self.display.width/2)/15)
						self.cam.y += int((i[1]['RECT'].y  - self.cam.y - self.display.height/2)/15)
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
					res.CHARACTERS[i]['VITALITY'] -= 1
					if res.CHARACTERS[i]['HEALTH'] == 17:
						chc = round(np.random.randint(0,100))
						if chc > 70: res.CHARACTERS[i]['HEALTH'] = 0
				if self.player[u]['SHK'] > 0: self.player[u]['SHK'] = -self.player[u]['SHK']
				elif self.player[u]['SHK'] < 0: self.player[u]['SHK'] = -self.player[u]['SHK'] - 1
			if res.CHARACTERS[i]['VITALITY'] <= 0: dth += 1
			elif res.CHARACTERS[i]['HEALTH'] in [8,13,14,15]: dth += 1
			u += 1
		#GAME OVER
		if dth == len(res.PARTY[res.FORMATION]) and self.turn != -5: self.guis['LEVEL'].draw()
		#BATTLE
		if False:#self.battle:
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
				if self.fig[self.turn]['HEALTH'] == 12: self.surfaces[0].fill((0,0,0))
				if self.fig[self.turn]['VITALITY'] <= 0: self.turn += 1
				elif self.fig[self.turn]['HEALTH'] in [8,13,14,15]: self.turn += 1
				if self.turn >= len(self.fig):
					if res.BTYPE == 1: self.fight()
					else: self.turn = 0
		
		#HUD
		self.surfaces[1].blit(tools.draw.bar((int(res.INVENTORY[res.PARTY[res.FORMATION][0]][4][1][1]),5),(20,40),(10,10,10),(200,200,10),'stack',5),(20,40))
		self.surfaces[1].blit(self.guis['INVENTORY'].gui.bar(0,4,(1,3),'horizontal',background=(0,0,0,0)),(50,40))
		self.surfaces[1].blit(tools.draw.bar((res.CHARACTERS[res.PARTY[res.FORMATION][0]]['ENERGY'],99),(self.window.height - int(self.window.height/10),40),(10,10,10),(10,200,10),'levels'),(150,40))
		
		#COUNTERS
		for i in range(len(self.counters)):
			self.counters[i].update(res.CHARACTERS[0]['SCORE'])
			self.surfaces[1].blit(self.counters[i].draw(),(10,10 + (i * 40)))

		#BLACKBARS
		if self.blackbars[0].height > 0:
			for i in self.blackbars: pygame.draw.rect(self.surfaces[1],(0,0,0),i)
			if self.guis['FILES'].show:
				self.surfaces[1].blit(res.FONTS['DEFAULT'].render(res.GNAME + ' v' + res.VERSION,True,(200,200,200)),(self.blackbars[0].x + 10,self.blackbars[0].y + 10))
				self.surfaces[1].blit(res.FONTS['DEFAULT'].render(res.AUTHOR + ' (' + res.YEAR + ')',True,(200,200,200)),(self.blackbars[1].x + 10,self.blackbars[1].y + 10))
		if res.PAUSE < 2 and self.blackbars[0].height > 0: self.blackbars[0].y -= 2; self.blackbars[0].height -= 2; self.blackbars[1].y += 2; self.blackbars[1].height -= 2
		if res.PAUSE > 1 and self.blackbars[0].height < 60: self.blackbars[0].y += 2; self.blackbars[0].height += 2; self.blackbars[1].y -= 2; self.blackbars[1].height += 2

		#STATUS
		if self.sttsy > 0:
			upsts = pygame.Surface((self.display.width,100))
			if res.GSCALE < 3: dwyy = 38
			else: dwyy = 18
			#ENEMIES COUNT
			if self.battle and self.winbar <= 100 and self.turn != -4:
				ce = 0
				if len(self.mrc) == 0:
					for i in self.foe:
						if i['VITALITY'] > 0: ce += 1
					self.surfaces[0].blit(res.FONTS['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (self.display.width - 100, int(self.winbar/2) - 15))
				else:
					for i in self.foe:
						if i['VITALITY'] > 0: ce += 1
					self.surfaces[0].blit(res.FONTS['MININFO'].render(str(ce) + '/' + str(len(self.foe)), True, (255,255,255)), (self.display.width - 100, 15))
					ce = 0
					for i in self.mrc:
						if i['VITALITY'] > 0: ce += 1
					self.surfaces[0].blit(res.FONTS['MININFO'].render(str(ce) + '/' + str(len(self.mrc)), True, (255,255,255)), (self.display.width - 100, 50))
			#DICES
			for i in self.dices: self.pseudo3d()
			'''y = 0
			for i in self.dices:
				if i[0] != -1:
					pygame.draw.rect(self.surfaces[0],res.COLOR,pygame.Rect(int(self.display.width/2) - (30 * len(self.dices)) + (y * 80),int(self.display.height/2) - 30,60,60))
					self.surfaces[0].blit(res.FONTS['MININFO'].render(str(i[0]),True,(10,10,10)),(int(self.display.width/2) - (30 * len(self.dices)) + (y * 80) + 15,int(self.display.height/2) - 15))
				y += 1'''
			#GRADIENT
			'''for i in range(len(self.grd)):
				self.surfaces[1].blit(self.grd[i],(0,i))
				self.surfaces[1].blit(self.grd[i],(0,self.window.height - i))'''
		
		#ACTQUEUE
		for i in self.actqueue:
			if i['RECT'] == self.player[0]['RECT']: pos = (self.player[0]['RECT'].x - int(self.player[0]['RECT'].width/2) - self.cam.x,self.player[0]['RECT'].y - 40 - self.cam.y)
			else: pos = (i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y)
			pygame.draw.rect(self.surfaces[0],(10,10,10),pygame.Rect(pos[0],pos[1],50,10))
			if i['BAR'] > 0: pygame.draw.rect(self.surfaces[0],(10,200,10),pygame.Rect(pos[0],pos[1],np.floor(50/(100/i['BAR'])),10))
		
		#GUI WINDOWS
		for i in self.guis:
			if i == 'POPUPS':
				for p in self.guis[i]:
					if self.guis[i][p].show: self.surfaces[1].blit(self.guis[i][p].draw(), (self.guis[i][p].rect.x,self.guis[i][p].rect.y))
			elif i != 'BKG' and self.guis[i].show: self.surfaces[1].blit(self.guis[i].draw(), (self.guis[i].rect.x,self.guis[i].rect.y))

		#DIALOGS
		if self.dlg: self.surfaces[1].blit(self.dlg.draw(),(0,0))
		#EASTER EGG
		if self.cityname == 'TWNN': self.surfaces[0].blit(pygame.image.load(res.SPRITES_PATH + 'TWNN.png').convert_alpha(), (35,0))
		
		#NOTIFICATIONS
		self.notification = [i for i in self.notification if i['TEXT'] != None]
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
			szw = np.floor(res.FONTS['DEFAULT'].size(txt)[0]/2) + 30 + isz
			szh = np.floor(res.FONTS['DEFAULT'].size(txt)[1]/2) + 30
			#MOVING
			if i['HALIGN'] == 'left':
				yy = 0
				i['X'] += 20
				if i['X'] < 0: xx = i['X']
				else: xx = 0
			if i['HALIGN'] == 'right':
				yy = 1
				i['X'] -= 20
				if i['X'] > self.display.width - szw: xx = i['X']
				else: xx = self.display.width - szw
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
				if i['COLOR'] != (0,0,0): pygame.draw.rect(self.surfaces[0], (0,0,0), pygame.Rect(xx - 3,y[yy] + 27,szw,szh))
				else: pygame.draw.rect(self.surfaces[0], (255,255,255), pygame.Rect(xx - 3,y[yy] + 27,szw,szh))
				pygame.draw.rect(self.surfaces[0], i['COLOR'], pygame.Rect(xx,y[yy] + 30,szw - 6,szh - 6))
				if 'IMAGE' in i: self.surfaces[0].blit(i['IMAGE'], (10 + xx, y[yy] + 40)); addx += i['IMAGE'].get_width() + 10
				if 'BAR' in i:
					pygame.draw.rect(self.surfaces[0], (10,10,10), pygame.Rect(10 + xx + addx,y[yy] + 40,100,20))
					pygame.draw.rect(self.surfaces[0], (200,200,10), pygame.Rect(10 + xx + addx,y[yy] + 40,int(100/(i['BAR'][0]/i['BAR'][1])),20))
					pygame.draw.rect(self.surfaces[0], (10,200,10), pygame.Rect(10 + xx + addx,y[yy] + 40,int(100/(i['BAR'][0]/i['BAR'][2])),20))
				self.surfaces[1].blit(res.FONTS['DEFAULT'].render(txt, True, (0, 0, 0)), ((10 + xx + addx) * res.GSCALE, (y[yy] + 45) * res.GSCALE))
				y[yy] += szh + 10
			if i['X'] in [1000,-1000]:
				i['TEXT'] = None
		#TRANSICTION
		if self.trsction: self.surfaces[1].blit(self.trsction,(0,0))
		#HINTEXT
		if res.HINT and res.HINTEXT:
			txt = dtb.HINTS[res.HINTEXT].format(*('<' + pygame.key.name(i).upper() + '>' for i in res.CONTROLS[0]))
			sz = res.FONTS['DEFAULT'].size(txt)
			self.surfaces[1].blit(res.FONTS['DEFAULT'].render(txt,True,(200,200,200)), (self.window.width - sz[0] - 10, self.window.height - sz[1] - 10))
		
		#TOUCH BUTTONS
		if len(self.buttons) > 0 and self.battle == False:
			if self.player[0]['SPEED'] > 0: prs = str(self.player[0]['DIRECTION'])
			else: prs = '0'
			tchpad = pygame.image.load(res.SPRITES_PATH + 'tchpad_' + prs + '.png')
			tchpad.fill(res.COLOR,None,pygame.BLEND_RGBA_MULT)
			self.surfaces[1].blit(tchpad,(20,self.window.height - 264))
			for bt in [(4,(self.window.width - 190,self.window.height - 100)),(5,(self.window.width - 100,self.window.height - 100)),
				(6,(self.window.width - 190,40)),(7,(self.window.width - 100,40))]:
				abl = False
				if self.guis['INVENTORY'].gui.type == 0: abl = True
				elif bt[0] in [6,7]: abl = True
				if abl:
					if bt[0] == 5:
						if self.player[0]['SPEEDLOCK']: fr = '1'
						else: fr = str(int(self.pressed[bt[0]][0]))
					else: fr = str(int(self.pressed[bt[0]][0]))
					img = pygame.image.load(res.SPRITES_PATH + 'tch_' + fr + '.png')
					img.fill(res.COLOR,None,pygame.BLEND_RGBA_MULT)
					self.surfaces[1].blit(img,bt[1])
		
		#DISDEBUG
		if self.disdbg:
			prs = ''
			mix = 0
			osinfo = platform.uname()
			for i in range(len(self.pressed)): prs += str(self.pressed[i][0]) + ','
			for i in range(len(self.channels)):
				if self.channels[i][1]: mix += 1
			dinfo = ['DEVICE WIDTH: ' + str(self.window.width) + ' | DEVICE HEIGHT: ' + str(self.window.height) + ' | ',
			'GAME WIDTH: ' + str(self.display.width) + ' | GAME HEIGHT: ' + str(self.display.height) + ' | FPS: ' + str(int(self.glock.get_time())) + ' | ',
			'CAMERA X: ' + str(self.cam.x) + ' | CAMERA Y: ' + str(self.cam.y) + ' | ',
			'SYSTEM: ' + osinfo.system + ' | NODE: ' + osinfo.node + ' | RELEASE: ' + osinfo.release + ' | VERSION: ' + osinfo.version + ' | ',
			'MACHINE: ' + osinfo.machine,
			'PRESSED: [' + prs[0:-1] + '] + | MIXER: ' + str(mix) + ' | ',
			'TIME: ' + str(res.TIME[0]) + ':' + str(res.TIME[1]) + ':' + str(res.TIME[2]) + ' | DATE: ' + str(res.DATE[0]) + '/' + str(res.DATE[1]) + '/' + str(res.DATE[2]) + ' | ',
			'INVENTORY: ' + str(self.guis['INVENTORY'].gui.type) + ' | PAUSE: ' + str(self.title.mnu)]
			y = 0
			for txt in tools.text.wrap(dinfo,res.FONTS['DISDBG'],int(self.window.width * 0.75)):
				self.surfaces[1].blit(res.FONTS['DISDBG'].render(txt, True, (200,200,200)), (10, 10 + (y * 30)))
				y += 1
		
		#CAMERA
		dlgcam = True
		camfollow = True
		camspd = int(res.CAMACC * res.GSCALE)
		recam = [self.cam.x,self.cam.y]
		if len(self.player) == 0: pcam = [int(self.display.width/2),int(self.display.height/2)]
		elif dlgcam:#self.dlg['CAMERA'] == 0:
			pcam = [0,0]
			for i in self.player:
				if i['POSTURE'] == 2: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y - 200
				else: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y
			pcam = [int(pcam[0]/len(self.player)),int(pcam[1]/len(self.player))]
		else: pcam = [self.dlg['CAMERA'].x,self.dlg['CAMERA'].y]

		if self.map:
			cmgrd = [[0,(self.map.width * self.map.tilewidth) - self.display.width],[0,(self.map.height * self.map.tileheight) - self.display.height]]
			lst = [[self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight],[self.display.width,self.display.height]]
			camscroll = [self.map.hscroll,self.map.vscroll]
		else:
			cmgrd = [[0,300],[0,200]]
			lst = [[300,200],[300,200]]
			camscroll = [0,0]

		for i in range(2):
			if lst[0][i] > lst[1][i]:
				if camfollow:
					if self.portalgo == {}: self.campos[i] = pcam[i]
					#SCROLL CAMERA
					if camscroll[i] != 0: recam[i] += camscroll[i]
					#REGULAR CAMERA
					elif self.camgrid == 1: recam[i] += int((self.campos[i] - recam[i] - (lst[1][i]/2))/camspd)
					#STATIC CAMERA
					else:
						if self.camgrid == 'screen': gg = lst[1][i]
						else: gg = self.camgrid * self.map.tilewidth
						recam[i] = np.floor(self.campos[i]/gg) * gg
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
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['FLAW'] == 'myopia': chk = not chk
		if chk == False:
			srf = pygame.transform.scale(self.surfaces[0], (self.display.width * res.GSCALE, self.display.height * res.GSCALE))
			srf.set_alpha(100)
			self.screen.blit(srf, (self.display.x - 20, self.display.y))
			self.screen.blit(srf, (self.display.x + 10, self.display.y))
			srf = self.surfaces[1]
			srf.set_alpha(100)
			self.screen.blit(srf, (self.display.x - 20, self.display.y))
			self.screen.blit(srf, (self.display.x + 10, self.display.y))
		else:
			if self.display.x > self.display.width * 0.25:
				self.screen.blit(pygame.transform.scale(self.surfaces[0], (self.display.width * res.GSCALE, self.display.height * res.GSCALE)), (self.display.x - int(self.display.width * res.GSCALE * 1.25), self.display.y))
				self.screen.blit(self.surfaces[1], (self.display.x - int(self.display.width * res.GSCALE * 1.25), self.display.y))
			if self.display.y > self.display.height * 0.25:
				self.screen.blit(pygame.transform.scale(self.surfaces[0], (self.display.width * res.GSCALE, self.display.height * res.GSCALE)), (self.display.x, self.display.y - int(self.display.height * res.GSCALE * 1.25)))
				self.screen.blit(self.surfaces[1], (self.display.x, self.display.y - int(self.display.height * res.GSCALE * 1.25)))
			self.screen.blit(pygame.transform.scale(self.surfaces[0], (self.display.width * res.GSCALE, self.display.height * res.GSCALE)), (self.display.x, self.display.y))
			self.screen.blit(self.surfaces[1], (self.display.x, self.display.y))
		#MOUSE
		if res.MOUSE == 1: self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'),(self.click.x,self.click.y))

	def loading(self):
		self.events()
		self.screen.fill((0,0,0),pygame.Rect(self.window.width - 80, self.window.height - 80,30,30))
		if self.loadingif != None:
			self.loadingif += 0.01
			if str(self.loadingif)[2] == '0': upd = True
			else: upd = False
			if self.loadingif >= 8.0: self.loadingif = 0.0
		if upd:
			self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'loading_' + str(np.floor(self.loadingif)) + '.png'), (self.window.width - 80, self.window.height - 80))
			pygame.display.update(pygame.Rect(self.window.width - 80,self.window.height - 80,30,30))

	def crash(self):
		from traceback import extract_tb
		self.screen.fill((0,0,0))
		et, ev, eb = sys.exc_info()
		err = str(et.__name__) + ': ' + str(ev) + ''
		tlist = [dtb.ERROR['file'] + ' "' + str(i[0]) + '", ' + dtb.ERROR['line'] + ' ' + str(i[1]) + ' ' + dtb.ERROR['in'] + ' ' + str(i[2]) + ': ' + str(i[3]) for i in extract_tb(eb)]

		fnt = pygame.font.SysFont('Calibri', 26)
		self.screen.blit(fnt.render(dtb.ERROR['crash'],True,(10,250,10)),(10,20))
		fnt = pygame.font.SysFont('Calibri', 22)
		self.screen.blit(fnt.render(err,True,(10,250,10)),(10,60))
		for i in range(len(tlist)): self.screen.blit(fnt.render(str(tlist[i]),True,(10,250,10)),(10,100 + (i * 20)))
		self.screen.blit(fnt.render(dtb.ERROR['press'],True,(10,250,10)),(10,140 + (i * 20)))
		pygame.display.flip()

		self.log += '\n ' + dtb.ERROR['crash'] + '\n' + err
		print('\n' + dtb.ERROR['crash'])
		print(err)
		for i in tlist: print('	' + i)
			
		lp = True
		while lp:
			for event in pygame.event.get():
				#EXIT
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					exit()
				#RESIZE
				if event.type == pygame.VIDEORESIZE:
					self.window.height = event.h
					sh = int(event.h/4)
					self.window.width = 6 * sh
					self.screen = pygame.display.set_mode((self.window.width, self.window.height), pygame.RESIZABLE)
				#SKIP
				do = False
				if event.type == pygame.KEYDOWN: do = True
				if event.type == pygame.MOUSEBUTTONDOWN: do = True
				if do:
					#self.loadmap()
					lp = False
					print(dtb.ERROR['restart'])

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
							res.MIXER[1].play(res.SOUND['HEAL'])
							hl = dtb.ITEMS[it[0]][5]
							hg = dtb.ITEMS[it[0]][6]
							for ex in it[2::2]:
								if ex != '_': hl += dtb.ITEMS[ex][5]
							if it in res.CHARACTERS[self.guis['INVENTORY'].gui.opt[2]]['FAVFOOD']:
								hl += int(hl/2)
								hg += int(hg/2)
							hpb = ch['VITALITY']
							ch['VITALITY'] += hl
							ch['HUNGER'] += hg
							if res.DISITEMS[it[0]] == 0:
								res.DISITEMS[it[0]] = 1
							if ch['VITALITY'] > dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]:
								ch['VITALITY'] = dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]
						else:
							res.MIXER[1].play(res.SOUND['INCONSCIOUS'])
							ch['HEALTH'] = 10
						if self.guis['INVENTORY'].gui.allowtrash and len(dtb.ITEMS[it[0]]) > 8 and dtb.ITEMS[it[0]][8] != None:
							it = ['trash_' + dtb.ITEMS[it[0]][8],'0000']
						elif self.guis['INVENTORY'].gui.allowtrash and it[0].endswith('_wasted') and dtb.ITEMS[it[0]][7] != None:
							it = ['trash_' + dtb.ITEMS[it[0]][7],'0000']
						else:
							it = ['_','0000']
						bbr = [dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']],ch['VITALITY'],hpb]
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
						res.MIXER[1].play(res.SOUND['CALLING'],-1)
						if self.rad.onoff: pygame.mixer.music.pause()
						self.cal.nb = i[0][3:]
						self.waitlst.append(['cutcal',self.waitime + 1200])
					#CUTTING CALL
					elif i[0].startswith('cutcal'):
						if self.cal.nb != '':
							res.MIXER[1].stop()
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
						res.MIXER[1].stop()
						pygame.mixer.music.load(res.MUSIC_PATH + i[2] + '.mp3')
						pygame.mixer.music.play()
						self.rad.msc = -1
					#TIME WARNING
					elif i[0].startswith('advice'):
						if self.dlg['FADE'] > 0:
							self.dialog(dtb.DIALOGS['ADVICE'])
			#RADIONEWS AND RADIOEE
			if self.guis['RADIO'].gui.onoff: pass
			'''for i in dtb.RADIONEWS:
				if i[1][0] == res.TIME[0] and i[1][1] == res.TIME[1]:
					if i[0] == None: ply = True
					elif i[0][0] == res.DATE[0] and i[1][1] == res.DATE[1]: ply = True
					else: ply = False
					if ply and self.rad.msc != -2:
						self.rad.nwsw = 1
						self.rad.nwsind = i[0][2]
						pygame.mixer.music.stop()
						res.MIXER[1].play(res.SOUND['RADIONEWS'])
						self.waitlst.append(['radionews',self.waitime + 20,i[0]])
			for i in dtb.RADIOEE:
				if int(i[2][0:2]) == res.TIME[0] and int(i[2][2:4]) == res.TIME[1]:
					if i[1] == None: ply = True
					elif int(i[1][0:2]) == res.DATE[0] and int(i[1][2:4]) == res.DATE[1]: ply = True
					else: ply = False
					if ply and self.rad.msc != -2:
						self.rad.msc = -2
						pygame.mixer.music.stop()
						res.MIXER[1].play(res.SOUND['NOISE'],-1)
						self.waitlst.append(['radioee',self.waitime + 60,i[0]])'''
			#ITEMS DURATION
			"""u = 0
			for b in res.INVENTORY:
				for j in b:
					for i in list(filter(lambda x: x[0] != '_', j)):
						self.guis['INVENTORY'].gui.duration(i,u)
				u += 1"""
			#WASH
			"""for i in res.WASH:
				if i[2] != None and self.notification['X'] == 0:
					if res.TIME[0] >= int(i[2][0:2]):
						if res.TIME[1] >= int(i[2][2:4]):
							res.MIXER[0].play(res.SOUND['NOTIFICATION'])
							self.notification['TEXT'] = dtb.NOTINFO['WASH']
							self.notification['COLOR'] = (165, 255, 0)
							res.TASKS.append([(dtb.NOTINFO['WASH'],None,None), 0])
							i[2] = None"""
			self.waitime += 1
			
			#BATTERY
			battery = '1000'
			'''battery = res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1]
			if battery != 'infinite' and self.dev != None:
				battery = int(battery)
				if battery < 0:
					if self.guis[3].gui.onoff:
						self.guis[3].gui.onoff = False
						res.MIXER[1].stop()
						pygame.mixer.music.stop()
					battery = 0
				self.dev.battery = battery'''
			sleep = False
			#for p in self.player:
			#	if sleep == False: sleep = p['SLEEP']
			
			if 'TIME' in dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]] and dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]]['TIME'][0] < 0: vv = -1
			else: vv = 1
			if sleep: vv *= 5
			#chk = tools.time.datetime_update(vv)

			chk = [0,0,0,0,0,0,0]
			#res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1] = str(battery)
			if res.TIME == [0,0,0]:
				for i in res.PARTY[res.FORMATION]: res.CHARACTERS[i]['VITALITY'] = 0
			if chk[0]:
				for p in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[p]['VITALITY'] < dtb.CLASSES[res.CHARACTERS[p]['CLASS']]['RESISTANCE'][res.CHARACTERS[p]['LEVEL']]: res.CHARACTERS[p]['VITALITY'] += 1
					if res.CHARACTERS[p]['SLEEP'] < 10000: res.CHARACTERS[p]['SLEEP'] += 50
			if chk[1]:
				pass
				#BASIC NECESITIES
				"""for p in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[p]['HUNGER'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 6
					else: res.CHARACTERS[p]['HUNGER'] -= 1
					if res.CHARACTERS[p]['THIRST'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 7
					else: res.CHARACTERS[p]['THIRST'] -= 1
					if res.CHARACTERS[p]['SLEEP'] == 0: pass #res.CHARACTERS[p]['HEALTH'] = 8
					else: res.CHARACTERS[p]['SLEEP'] -= 10"""
			if chk[2] and sleep:
				for u in res.PARTY[res.FORMATION]:
					if res.CHARACTERS[u]['HEALTH'] in (4,5,9,10,11):
						res.CHARACTERS[u]['HEALTH'] = 0
			if chk[3]: res.TEMPERATURE = dtb.CITIES[self.map.city][1][res.DATE[1] - 1]
		self.events()
		self.draw()

		for i in res.MIXER:
			if pygame.display.get_active(): i.set_volume(res.SFX)
			elif res.MUTE: i.set_volume(0)

		'''if int(self.glock.get_fps()) > 0:
			jp = np.floor(res.FPS/int(self.glock.time()))
		else: jp = 1
		if res.FPS >= jp: pass'''
		#UPDATE
		try: pygame.display.flip()
		except: self.screen = pygame.display.set_mode((self.window.width, self.window.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
		#FPS
		self.glock.tick(res.FPS)
		tg = self.glock.get_rawtime()
		res.GAMETIME += tg

		#DEVICE INFORMATION
		#if res.DEBUG: print(f'CPU: {psutil.cpu_percent(tg)} | RAM: {psutil.virtual_memory()[2]}')

Initialize()
#REGULAR PLAY
if len(sys.argv) == 1:
	g = Game()
	while g.running:
		try: g.run()
		except: g.crash()
	f = open('log.txt','w')
	f.write(g.log)
	f.close()

#TERMINAL TESTING
elif len(sys.argv) > 1:
	hlp ='\tavatar - test avatar (index)\n\tchar (index) (x position) (y position) - test NPC\n\tdialog (index) - test dialog\n\t' + \
			'mpopen (file) - open map in GUI\n\tmprogue (file) - open map in terminal\n'
	if sys.argv[1] == 'avatar':
		if len(sys.argv) > 2:
			t = Avatar(sys.argv[2],testing=True)
			while True: t.test()
		else: print('\nFAILED: please, input avatar index')
	elif sys.argv[1] in ['char','character']:
		t = Character(sys.argv[2],(sys.argv[3],sys.argv[4]),testing=True)
		while True: t.test()
	elif sys.argv[1] == 'dialog': Dialog(sys.argv[2],testing=True)
	elif sys.argv[1] in ['mpopen','mprogue']:
		if len(sys.argv) > 2:
			t = MapHandler(sys.argv[2],testing=True)
			if sys.argv[1] == 'mpopen':
				while True: t.run()
			if sys.argv[1] == 'mprogue':
				t.roguemap()
		else: print('\nFAILED: please, input a xml map file')
	else: print(hlp)
else: print('missing arguments')
pygame.quit()
exit()