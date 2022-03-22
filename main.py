# -*- coding: utf-8 -*-
import pygame
import xml.sax
import plyer
import random
import datetime
import platform
import math
import sys
import os

from plugins import *
import resources as res
import minigames as mng
import GUI

if res.FILES != []: dtb = __import__('database_' + res.FILES[0][4])
else: dtb = __import__('database_' + res.MAINLANG)

class Initialize:
	def __init__(self):
		osinfo = platform.uname()
		print(res.GNAME.upper() + ' v.' + res.VERSION + ' - ' + res.AUTHOR + ' ' + res.YEAR)
		print(osinfo.system + ' ' + osinfo.machine + ' ' + osinfo.node + ' ' + osinfo.release + ' ' + osinfo.version)
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption(res.GNAME)
		pygame.display.set_icon(pygame.image.load('icon.ico'))
		pygame.mouse.set_visible(False)
		self.glock = pygame.time.Clock()
		if osinfo.system == 'Windows':
			self.windoww = 800
			self.windowh = 600
			res.MOUSE = 1
			res.GSCALE = 2
		else:
			sz = pygame.display.Info()
			self.windoww = sz.current_w
			self.windowh = sz.current_h
			res.MOUSE = 2
			res.GSCALE = 2
		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
		img = pygame.image.load('Icon.png')
		self.screen.blit(img,(int(self.windoww/2) - int(img.get_width()/2),int(self.windowh/2) - int(img.get_height()/2)))
		pygame.display.update()
		if res.TTS: plyer.tts.speak('')
		if res.VIBRATE: plyer.vibrator.vibrate(0.01)
		self.srf = pygame.Surface((600,400),pygame.SRCALPHA)
		self.fnt = {'DEFAULT': pygame.font.Font(res.FONTS_PATH + res.FONT, 22)}
		pygame.mixer.music.set_volume(res.MSC)
		self.alpha = 0
		self.wait = 0
		self.mnu = 0
		self.lspd = 0
		
		self.bump = pygame.image.load(res.BACKG_PATH + 'bump_' + str(random.randint(0,res.RANGE_BUMP)) + '.png')
		
		self.holiday = datetime.datetime.now()
		
		self.sscroll = self.windoww + 20
		self.stext = dtb.TSECRETS[random.randint(0,len(dtb.TSECRETS) - 1)]
		self.stime = random.randint(600,1000)
		self.gmtim = []
		
		self.load = 0
		self.msg = 0
		self.tim = 1.0
		self.gif = 0
		self.stars = []
		
		self.fload = res.RANGE_RADIO + len(os.listdir(res.SFX_PATH[:-1])) + 3 + (13 * 2)
		
		#self.grd = [self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0)),
		#self.guitools.gradient((self.windoww,200),(0,0,0,200),(0,0,0,0))]
		
		if res.GAMETIME > 0: self.msc.play(pygame.mixer.Sound(res.MUSIC_PATH + 'alchimera.mp3'))
		res.spr()
		res.battlesprites()
		res.animals()
		for j in os.listdir(res.SFX_PATH[:-1]):
			res.sfx(j)
			self.run()
		print('Boot time: ' + str(float(self.lspd/1000)) + 's')
	
	def intro(self):
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
		
	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				self.fnt = {'DEFAULT': pygame.font.SysFont('Calibri', math.floor(self.windoww/200) * 2)}
		
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
			
class ModeSeven:
	def __init__(self,sz,til):
		self.window = pygame.display.set_mode((600,600))
		self.input = pygame.Surface(sz)
		self.output = pygame.Surface(sz)
		self.grid = (int(sz[0]/til),int(sz[1]/til))
		self.angle = 0.25 #1/(90/x)
		self.ball = 0
		self.til = til
	
	def draw(self,srf):
		self.output.fill((0,0,0))
		
		brd = self.angle * (self.output.get_height() * self.angle)
		for i in range(self.grid[0]):
			prp = int((i * self.til)/4) + int(self.output.get_width() * self.angle)
			pygame.draw.line(self.output,(200,200,200),(i * self.til,self.output.get_height()),(prp,int(self.output.get_height() * self.angle)),1)
		for i in range(self.grid[1]):
			yy = self.output.get_height() - int((i * (self.til/((i + 1)/self.grid[1]))) * self.angle)
			prp = int((i * self.til)/4) + int(self.output.get_width() * self.angle)
			pygame.draw.line(self.output,(200,200,200),(0,yy),(prp,yy),1)
		pygame.draw.polygon(self.output,(100,100,100),((0,self.output.get_height()),(brd,self.output.get_height() * self.angle),(self.output.get_width() - brd,self.output.get_height() * self.angle),(self.output.get_width(),self.output.get_height())),5)
		pos = (int(math.sin(self.ball) * 20) + 100,int(math.cos(self.ball) * 20) + 100)
		pygame.draw.circle(self.output,(200,10,10),pos,5)
		
		return self.output
		
	def test(self):
		for event in pygame.event.get(): pass
		self.window.fill((100,100,100))
		self.input.fill((0,0,0))
		for i in range(self.grid[0]): pygame.draw.line(self.input,(200,200,200),(i * self.til,0),(i * self.til,self.input.get_height()))
		for i in range(self.grid[1]): pygame.draw.line(self.input,(200,200,200),(0,i * self.til),(self.input.get_width(),i * self.til))
		
		self.ball += 0.1
		pos = (int(math.sin(self.ball) * 20) + 100,int(math.cos(self.ball) * 20) + 100)
		pygame.draw.circle(self.input,(200,10,10),pos,5)
		self.draw(self.input)
		
		sz = (self.output.get_width() * res.GSCALE,self.output.get_height() * res.GSCALE)
		self.window.blit(pygame.transform.scale(self.output,sz),(0,0))
		self.window.blit(pygame.transform.scale(self.input,sz),(0,sz[1]))
		pygame.display.flip()
		pygame.time.Clock().tick(60)

'''
m = ModeSeven((200,200),20)
while True: m.test()'''
		

class Avatar:
	def __init__(self):
		self.window = pygame.display.set_mode((600, 600))
		self.surface = pygame.Surface((400, 600))
		self.brd = pygame.Surface((200,150))
		for x in range(math.ceil(self.brd.get_width()/10)):
			for y in range(math.ceil(self.brd.get_height()/10)):
				self.brd.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		self.scr = [pygame.Surface((200,150)), pygame.Surface((400,300), pygame.SRCALPHA)]
		self.fnt = {'MEDIUM': pygame.font.SysFont('Calibri', 40), 'SMALL': pygame.font.SysFont('Calibri', 20)}
		self.inv = GUI.Inventory((0,0),0)
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.player = {'RECT': pygame.Rect(res.PX,res.PY,20,20),'SPEED': 0,'ACC': 0,'SPEEDLOCK': False,'JUMP': 0,'GRAVITY': -5,'STEP': 10,
			'SWIM': None,'HEAT': res.TEMPERATURE,'HEAD': 'D','SPRITE': 'STANDD','SCORE': 0,'DRIVING': None,'SLEEP': False,'POSTURE': 1,
			'HAIR': res.CHARACTERS[0]['HAIR'],'SKIN': res.CHARACTERS[0]['SKIN'],
			'ACCESORIES': self.inv.find(0,['head'],'position'),'COSTUME': self.inv.find(0,['clth'],'position'),
			'GIF': 0.0,'BLINK': 100,'INVFRM': 0,'DMGTIM': 100,'SHK': 0,'DIRECTION': 3,'PAUSE': 0,
			'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','PLAYING': False,'NODES': [],'HOLD': None}
		self.donesprites = {}
		res.spr()

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
						if True: #self.dlg['CAMERA'] == i['RECT']:
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
				if visible:
					img = doll.copy()
					#if self.turn == -6: img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
					#self.display[0].blit(img,(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y - i['RECT'].height - i['JUMP']))
		return doll
		
	def inside_events(self,pressed):
		if pressed[2][0]: self.page = 0; self.sfx.play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page = 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def menu(self):
		scr = pygame.Surface((400,300))

		scr.fill((0,0,0))
			
		return self.scr

	def test(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		self.surface.fill((100,100,100))
		#self.surface.blit(self.overworld_draw(),(self.rect.x - 50,self.rect.y))
		self.surface.blit(self.people(self.player,False),(20,20))
		sz = (self.surface.get_width() * res.GSCALE * 4,self.surface.get_height() * res.GSCALE * 4)
		self.window.blit(pygame.transform.scale(self.surface,sz),(0,0))
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

a = Avatar()
while True: a.test()

class NPC:
	def __init__(self,index,pos):
		self.item = None
		for i in dtb.FREAKS[index].items():
			self.__dict__[i[0].lower()] = i[1]
		self.window = pygame.display.set_mode((600, 600))
		self.surface = pygame.Surface((400, 600))
		self.id = 0
		self.file = index
		self.sprite = pygame.image.load(res.FREAKS_PATH + (self.file) + '_mini.png').convert()
		self.rect = pygame.Rect(pos[0],pos[1],self.sprite.get_width(),self.sprite.get_height())
		self.eyes = [0,0]
		self.emote = 'regular'
		self.hdpos = [0,0]
		self.acc = 0
		self.mask = pygame.Rect(pos[0],pos[1],40,40)
		self.btrng = [20,200]
		self.direction = 1
		self.fighting = False
		self.hp = self.vitality
		self.condition = []
		self.time = 20
		self.fade = 10
		self.away = 0
		self.effect = 0.0
		self.speed = 0
		self.btimes = [0,0,0,0]
		self.jump = 0
		#if self.map.properties['HABITAT'] == self.habitat:
		if self.jump == 6:
			self.strenght = int(self.strenght * 1.25)
			self.agility = int(self.agility * 1.25)
			self.resistance = int(self.resistance * 1.25)
			self.hp = int(self.hp * 1.25)
		self.cursor = pygame.Rect(0,0,0,0)
		
	def overworld_draw(self):
		rectdebug = True
		if rectdebug: pygame.draw.rect(self.surface, (255,0,0), self.rect)
		img = pygame.image.load(res.FREAKS_PATH + (self.file) + '_mini.png')
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
		self.surface.blit(shd, (sxx, self.rect.y))
		for b in res.BESTIARY:
			if b['N'] == self.file and b['SEEN'] == 0 and i['TYPE'] != 'mercenary':
				img.fill((10,10,10),None,pygame.BLEND_RGBA_MULT)
		self.sprite = img
		if self.path == 'notice': self.surface.blit(pygame.image.load(res.SPRITES_PATH + 'notice.png'), (self.rect.x, self.rect.y - 30))
		return self.sprite
		
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
					self.ch_sfx.play(res.SOUND['NOTICED'])
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
				self.direction = self.guitools(self.rect,self.player[0]['RECT'])
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
			#MOVING
			if self.path != 'stay':
				if self.direction == 1: self.rect.x += self.agility - 1
				if self.direction == 2: self.rect.x += self.agility - 1; self.rect.y += self.agility - 1
				if self.direction == 3: self.rect.y += self.agility - 1
				if self.direction == 4: self.rect.x -= self.agility - 1; self.rect.y += self.agility - 1
				if self.direction == 5: self.rect.x -= self.agility - 1
				if self.direction == 6: self.rect.x -= self.agility - 1; self.rect.y -= self.agility - 1
				if self.direction == 7: self.rect.y -= self.agility - 1
				if self.direction == 8: self.rect.x += self.agility - 1; self.rect.y -= self.agility - 1
				self.time -= 1
				
	def interact(self):
		mp = pygame.mouse.get_pos()
		self.cursor = pygame.Rect(int(mp[0]/res.GSCALE),int(mp[1]/res.GSCALE),2,2)
		if pygame.Rect.colliderect(self.cursor,self.mask): self.emote = 'hurt'
	
	def colide(self):
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
								#self.turn = -6
								self.turn = -2
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
						i['MASK'].x = int(math.cos(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzw/2) - 50
						i['MASK'].y = int(math.sin(i['SPEED'] + (i['N'] * 2)) * 50) + int(self.displayzh/2) - 50
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
					self.hdpos[1] = int(math.sin(self.acc) * 3)
					self.acc += 0.1
					self.surface.blit(pygame.image.load(res.FREAKS_PATH + (self.file) + '_body.png').convert_alpha(), (int(self.mask.x + dtb.FREAKS[self.file]['SKELETON']['body'][0]), int(self.mask.y + dtb.FREAKS[self.file]['SKELETON']['body'][1])))
					for x in range(len(dtb.FREAKS[self.file]['SKELETON']['eye'])):
						img = pygame.image.load(res.FREAKS_PATH + (self.file) + '_eye.png').convert()
						offst = (int(img.get_width()/2),int(img.get_height()/2))
						xx = int(self.mask.x + dtb.FREAKS[self.file]['SKELETON']['eye'][x][0] - offst[0])
						yy = int(self.mask.y + dtb.FREAKS[self.file]['SKELETON']['eye'][x][1] - offst[1])
						if self.cursor.x > xx - 5 and self.cursor.x < xx + 5: self.eyes[0] = self.cursor.x - xx
						if self.cursor.y > yy - 5 and self.cursor.y < yy + 5: self.eyes[0] = self.cursor.y - yy
						self.surface.blit(img, (xx + self.eyes[0] + self.hdpos[0],yy + self.eyes[1] + self.hdpos[1]))
					self.surface.blit(pygame.image.load(res.FREAKS_PATH + (self.file) + '_head_' + self.emote + '.png').convert_alpha(), (int(self.mask.x + self.hdpos[0]), int(self.mask.y + self.hdpos[1])))
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
					self.surface.blit(res.SPRITES['EFFECT_' + str(i['HEALTH'])][math.floor(self.effect)], (self.mask.x + 5, self.mask.y - 10))
					self.effect += 0.5
					#self.effect >= len(res.SPRITES['EFFECT_' + str(i['HEALTH'])]): self.effect = 0.0
			else: self.mask.x -= self.agility
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
		
	def test(self):
		for event in pygame.event.get(): self.interact()
		self.surface.fill((100,100,100))
		self.overworld_move()
		self.inbattle_draw()
		#self.surface.blit(self.overworld_draw(),(self.rect.x - 50,self.rect.y))
		sz = (self.surface.get_width() * res.GSCALE,self.surface.get_height() * res.GSCALE)
		self.window.blit(pygame.transform.scale(self.surface,sz),(0,0))
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

'''
e = NPC('4.1.1',(50,50))
while True: e.test()
'''

class MapHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.window = pygame.display.set_mode((400,300))
		self.surfaces = [None for i in range(5)]
		self.layers = [[] for i in range(5)]
		self.tileset = []
		self.srflvl = 0
		self.current = None
		self.content = ''

		self.interior = 0
		self.hscroll = 0
		self.vscroll = 0
		self.city = 0
		self.edit = False
		
		self.npcs = [{'RECT': pygame.Rect(x * 30,60,25,25), 'DIRECTION': 1} for x in range(3)]
		self.cars = [{'RECT': pygame.Rect(x * 30,90,25,25), 'DIRECTION': 1} for x in range(3)]
		self.sidewalk = []
		self.streets = []
		self.crossing = []
		self.traflight = 0
   
	def startElement(self, tag, attributes):
		tag = tag.lower()
		lst = ['floor','walls','ceil']
		if tag == 'map':
			for i in [i[0] for i in attributes.items() if i[0] not in ['version','tiledversion','orientation','renderorder']]:
				setattr(self, i, int(attributes[i]))
			self.surfaces = [pygame.Surface((int(attributes['width']) * int(attributes['tilewidth']),int(attributes['height']) * int(attributes['tileheight'])),pygame.SRCALPHA) for i in range(5)]
		if tag == 'property': setattr(self, attributes['name'], attributes['value'])
		if tag == 'tileset': pass
		if tag in lst: self.srflvl = lst.index(tag)
		if tag == 'layer':
			dct = {i[0]: i[1] for i in attributes.items()}
			dct['data'] = []
			dct['surface'] = pygame.Surface((int(attributes['width']) * self.tilewidth,int(attributes['height']) * self.tileheight),pygame.SRCALPHA)
			self.layers[self.srflvl].append(dct)
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
			parser = xml.sax.make_parser()
			parser.setFeature(xml.sax.handler.feature_namespaces, 0)
			tls = {}
			gid = 0
			for t in os.listdir(res.TILESETS_PATH):
				tset = TileHandler(self.tileset,gid)
				parser.setContentHandler(tset)
				parser.parse(res.TILESETS_PATH + t)
				tls = {**tls,**tset.tiles}
				gid += tset.lenght
			for i in range(5):
				for ldx in range(len(self.layers[i])):
					#DRAW LAYERS
					for y in range(int(self.layers[i][ldx]['height'])):
						for x in range(int(self.layers[i][ldx]['width'])):
							t = self.layers[i][ldx]['data'][x + (y * int(self.layers[i][ldx]['height']))]
							if t > 0: self.layers[i][ldx]['surface'].blit(tls[t]['IMG'],(x * self.tilewidth,y * self.tileheight))
					#DRAW SURFACES
					for l in self.layers[i]:
						if 'offsetx' in l.keys(): cor = (int(l['offsetx']) * self.tilewidth,int(l['offsety']) * self.tileheight)
						else: cor = (0,0)
						self.surfaces[i].blit(l['surface'],cor)
				'''if tls[self.layers[i][pos]]['TYPE'] == 'sidewalk': self.sidewalk.append(cor)
				if tls[self.layers[i][pos]]['TYPE'] == 'street': self.streets.append(cor)
				if tls[self.layers[i][pos]]['TYPE'] == 'crossing': self.crossing.append(cor)'''
		self.current = None
		self.content = ''

	def save(self, mp=None):
		contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
		'<map version="1.2" orientation="orthogonal" renderorder="left-up" compressionlevel="0" width="{}" height="{}" '.format(self.width,self.height)
		contents += 'tilewidth="{}" tileheight="{}" infinite="0" nextlayerid="14" nextobjectid="77">\n'.format(self.tilewidth,self.tileheight)
		if len(self.mapdata['PROPERTIES']) > 0:
			contents += '	<properties>\n'
			for p in self.mapdata['PROPERTIES'].items():
				contents += '		<property name="{}" type="{}" value="{}"/>\n'.format(p[0],type(p[1]).__name__,p[1])
			contents += '	</properties>\n'
		'''
		gid = 1
		for i in tilset:
			tst = pytmx.load_pygame(res.TILESETS_PATH + i)
			gid += tst.tilecount
			contents += '	<tileset firstgid="{}" source="../{}"/>\n'.format(gid,res.TILESETS_PATH + i)'''
		id = 1
		tid = 0
		oid = 1
		for i in self.tileset:
			contents += '	<layer id="{}" name="TILE LAYER {}" width="{}" height="{}">\n'.format(id,tid + 1,self.width,self.height)
			contents += '		<data encoding="csv">\n'
			dd = ''
			for d in i: dd += self.guitools.digitstring(d,3) + ','
			for d in range(self.map['width']):
				contents += '			' + str(dd[d * (self.width) * 4:(d + 1) * (self.height) * 4]) + '\n'
			contents = contents[0:-2] + '\n		</data>\n	</layer>\n'
			tid += 1

		for i in self.layers:
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
		
	def draw(self):
		pass
		'''
		#REGULAR GROUND
		self.surfaces[0].blit(self.tilmap[0][math.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
		if len(self.tilmap[1]) > 0: self.display[0].blit(self.tilmap[1][math.floor(self.tilemation)],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
		#MIRROR SURFACES
		for i in self.tilrect[5]:
			self.display[0].blit(i[0],(i[1].x - self.cam.x, i[1].y - self.cam.y))
			if self.rectdebug: pygame.draw.rect(self.display[0],(0,0,255),pygame.Rect(i[1].x - self.cam.x,i[1].y - self.cam.y,i[1].width,i[1].height),3)
		'''

	def test(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		self.window.fill((100,100,100))
		for i in self.surfaces: self.window.blit(i,(0,0))
		self.traflight += 1
		if self.traflight > 240: self.traflight = 0
		for i in self.sidewalk: pygame.draw.rect(self.window,(100,100,200),pygame.Rect(i[0],i[1],30,30),2)
		for i in self.streets: pygame.draw.rect(self.window,(200,100,100),pygame.Rect(i[0],i[1],30,30),2)
		for i in self.crossing:
			if self.traflight < 120: pygame.draw.rect(self.window,(200,100,100),pygame.Rect(i[0],i[1],30,30),2)
			else: pygame.draw.rect(self.window,(100,100,200),pygame.Rect(i[0],i[1],30,30),2)
		lst = [self.npcs,self.cars]
		for l in range(len(lst)):
			for i in range(len(lst[l])):
				rct = lst[l][i]['RECT']
				cl = [(100,100,200),(200,100,100)]
				pygame.draw.ellipse(self.window,cl[l],rct)

				if lst[l][i]['DIRECTION'] == 1: chk = [1,0]
				if lst[l][i]['DIRECTION'] == 2: chk = [1,1]
				if lst[l][i]['DIRECTION'] == 3: chk = [0,1]
				if lst[l][i]['DIRECTION'] == 4: chk = [-1,1]
				if lst[l][i]['DIRECTION'] == 5: chk = [-1,0]
				if lst[l][i]['DIRECTION'] == 6: chk = [-1,-1]
				if lst[l][i]['DIRECTION'] == 7: chk = [0,-1]
				if lst[l][i]['DIRECTION'] == 8: chk = [1,-1]
				chk = []
				for c in [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]:
					chk.append([rct.x + (c[0] * 30),rct.y + (c[1] * 30)])

				if l == 0: ls = self.streets; eq = 'self.traflight < 120'
				else: ls = self.sidewalk; eq = 'self.traflight >= 120'
				ntil = [cor for x in ls for cor in range(len(chk)) if x[0] == int(chk[cor][0]/self.map['tilewidth']) * self.map['tilewidth'] and x[1] == int(chk[cor][1]/self.map['tileheight']) * self.map['tileheight']]
				if eval(eq): ntil += [x for x in self.crossing for cor in chk if x[0] == int(cor[0]/self.map['tilewidth']) * self.map['tilewidth'] and x[1] == int(cor[1]/self.map['tileheight']) * self.map['tileheight']]
				dirs = [x for x in [1,3,5,7] if x not in ntil]
				if len(dirs) == 0: lst[l][i]['DIRECTION'] = 0
				elif lst[l][i]['DIRECTION'] not in dirs: lst[l][i]['DIRECTION'] = dirs[random.randint(0,len(dirs) - 1)]

				spd = 1
				if lst[l][i]['DIRECTION'] == 1: rct.x += spd
				if lst[l][i]['DIRECTION'] == 2: rct.x += spd; rct.y += spd
				if lst[l][i]['DIRECTION'] == 3: rct.y += spd
				if lst[l][i]['DIRECTION'] == 4: rct.x -= spd; rct.y += spd
				if lst[l][i]['DIRECTION'] == 5: rct.x -= spd
				if lst[l][i]['DIRECTION'] == 6: rct.x -= spd; rct.y -= spd
				if lst[l][i]['DIRECTION'] == 7: rct.y -= spd
				if lst[l][i]['DIRECTION'] == 8: rct.x += spd; rct.y -= spd
				
		pygame.display.flip()
		pygame.time.Clock().tick(res.FPS)

class TileHandler(xml.sax.ContentHandler):
	def __init__(self,lst,first):
		self.ind = ''
		self.img = None
		self.tileset = lst
		self.tiles = {}
		self.tilprp = {} #for old tiled tileset versions
		self.tilani = []
		self.first = first
		self.gid = 0
		self.cor = [0,0]

		self.rows = None
		self.columns = None
   
	def startElement(self, tag, attributes):
		if tag == 'tileset':
			for i in [i[0] for i in attributes.items() if i[0] not in ['version','tiledversion','name']]:
				setattr(self, i, int(attributes[i]))
			if self.rows == None: self.rows = int(self.tilecount/self.columns)
			self.lenght = self.rows * self.columns
		if tag in ['img','image']:
			self.img = pygame.image.load(res.TILESETS_PATH + attributes['source'])
			self.width = self.img.get_width(); self.height = self.img.get_height()
		if tag == 'tile':
			self.cor[0] += 1
			if self.cor[0] >= self.columns:
				self.cor[0] = 0
				self.cor[1] += 1
			if int(attributes['id']) + self.first in self.tileset:
				lid = int(attributes['id'])
				self.gid = int(attributes['id']) + self.first
				rct = (self.cor[0] * self.tilewidth,self.cor[1] * self.tileheight,self.tilewidth,self.tileheight)
				self.tiles[self.gid] = {'IMG': self.img.subsurface(rct).copy(),'RECT': (0,0,0,0)}
				for x in attributes.items(): self.tiles[self.gid][x[0].upper()] = x[1]
		if tag == 'properties': self.tilprp = {}
		if tag == 'property': self.tilprp[attributes['name']] = attributes['value']
		if tag == 'animation': self.tilani = []
		if tag == 'frame':
			if 'tileid' in attributes.keys(): self.tilani.append(attributes['tileid'])
			else: self.tilani.append(attributes['tile'])
		self.ind = tag

	def endElement(self, tag):
		if tag == 'tile' and self.gid > 0:
			for i in self.tilprp.items(): self.tiles[self.gid][i[0]] = i[1]
			if self.tilani: self.tiles[self.gid]['ANIMATION'] = self.tilani
		self.ind = ''

	def characters(self, content): pass
	
	def save(self, f=None):
		contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
		'<tileset version="1.2" name="{}" tilewidth="{}" tileheight="{}" rows="{}" columns="{}">\n'.format(self.properties['tilewidth'],self.properties['tileheight'],self.properties['rows'],self.properties['columns'])
		contents += '	<img source="{}" width="{}" height="{}"/>\n'.format(self.mapdata['WIDTH'],self.mapdata['HEIGHT'])
		id = 1
		for i in tilset:
			gid += tst.tilecount
			contents += '	<tile id="{}" mask="{}" type="{}">\n'.format(id,(0,0,30,30),0)
			id += 1
		contents += '</tilset>'
		
		if f: ff = self.name
		else: ff = f
		file = open(res.MAPS_PATH + ff + '.xml','w')
		file.write(contents)
		file.close()

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
map = MapHandler()
parser.setContentHandler(map)
parser.parse(res.MAPS_PATH + 'savetest.tmx')
while True: map.test()

class Map:
	def __init__(self):
		pass
			
	def loadmap(self, mp=None):
		import pytmx
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
											tilimg[gid].append(self.map.get_tile_image_by_gid(frm.gid).convert_alpha())
										image = tilimg[gid][a]
									else:
										image = tilimg[gid]
								else:
									if t['frames'] != []:
										image = self.map.get_tile_image_by_gid(t['frames'][a].gid).convert_alpha()
										tilimg[gid] = []
										tilimg[gid].append(image)
									else:
										image = self.map.get_tile_image_by_gid(gid).convert_alpha()
										tilimg[gid] = image
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
								#HIDE TILES
								else:
									if t['TYPE'].startswith('HIDE'): self.tilrect[4].append([t['TYPE'],pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,int(self.map.tilewidth),int(self.map.tileheight))])
							#FOR GRID
							elif i in [0,1]:
								self.tilrect[i].append(None)
								if i == 0: self.tilrect[3].append(None)
		
		print(tilimg)
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
					eny = Enemy(wh,(0,0))
					eny.id = i
					rct = None
					while rct == None: rct = self.tilrect[0][round(random.randint(0, len(self.tilrect[0])))]
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
			
class Game:
	def __init__(self):
		#GAME SETTINGS
		sz = pygame.display.Info()
		self.running = True
		self.windoww = sz.current_w
		self.windowh = sz.current_h
		self.displayzw = int(self.windoww/res.GSCALE)
		self.displayzh = int(self.windowh/res.GSCALE)
		self.displayx = 0
		self.displayy = 0
		self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = [pygame.Surface((self.displayzw, self.displayzh)), pygame.Surface((self.windoww, self.windowh), pygame.SRCALPHA)]
		self.glock = pygame.time.Clock()
		self.fnt = {'DEFAULT': pygame.font.Font(res.FONTS_PATH + res.FONT, 10 * res.GSCALE), 'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 30),
			'MININFO': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 25), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 15),
			'CONTROLKEYS': pygame.font.Font(res.FONTS_PATH + 'controlkeys.ttf', 15),'ANGER': pygame.font.Font(res.FONTS_PATH + res.FONT, 15 * res.GSCALE),
			'DISDBG': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', int(7.5 * res.GSCALE)),'SCORETXT': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 12)}
		self.cam = pygame.Rect(0,0,self.displayzw,self.displayzh)
		self.camgrid = 1
		self.campos = [0,0]
		self.tilemation = 0
		self.rectdebug = False
		self.disdbg = False
		self.classrun = 1
		self.hpctrl = []
		self.waitime = 0
		self.waitlst = [['advice',432000],['rain',3600]]
		self.blankimg = pygame.Surface((self.windoww,self.windowh))
		self.blankimg.fill(res.COLOR)
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
		#self.cal = GUI.Contacts()
		self.inv = GUI.Inventory((self.displayzw,self.displayzh),0)
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
		self.phone = 0
		self.phofa = 0
		self.trsction = None
		self.guis = []
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
		self.objects = []
		self.log = ''
		res.MAP = 'savetest'
		res.PX = 0
		res.PY = 0
		#PLAYERS
		x = 0
		for i in res.PARTY[res.FORMATION]:
			self.player.append({'RECT': pygame.Rect(res.PX,res.PY,20,20),'SPEED': 0,'ACC': 0,'SPEEDLOCK': False,'JUMP': 0,'GRAVITY': -5,'STEP': 10,
			'SWIM': None,'HEAT': res.TEMPERATURE,'HEAD': 'D','SPRITE': 'STANDD','SCORE': 0,'DRIVING': None,'SLEEP': False,'POSTURE': 1,
			'HAIR': res.CHARACTERS[i]['HAIR'],'SKIN': res.CHARACTERS[i]['SKIN'],
			'ACCESORIES': self.inv.find(i,['head'],'position'),'COSTUME': self.inv.find(i,['clth'],'position'),
			'GIF': 0.0,'BLINK': 100,'INVFRM': 0,'DMGTIM': 100,'SHK': 0,'DIRECTION': 3,'PAUSE': 0,
			'FOLLOW': None,'FOLLEND': 0,'FOLLMOV': '','PLAYING': False,'NODES': [],'HOLD': None})
			self.objects.append(['player',x,self.player[x]['RECT'].y])
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
		self.map = None
		#START MENU
		self.files = GUI.Files((self.displayzw,self.displayzh))
		self.bckgs = GUI.Backgrounds()
		for i in self.guitools.transiction((self.displayzw,self.displayzh),1,-100,'fade'): self.trsction = i; self.run()

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
			parser = xml.sax.make_parser()
			parser.setFeature(xml.sax.handler.feature_namespaces, 0)
			self.map = MapHandler()
			parser.setContentHandler(self.map)
			parser.parse(res.MAPS_PATH + 'savetest.tmx')
			self.tilmap = [[i,i] for i in self.map.surfaces]
			
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
			if i['MOVE'] == 'follow': i['DIRECTION'] = self.guitools(i['RECT'],self.player[0]['RECT'])
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
			i['DIRECTION'] = self.guitools.follow(i['RECT'],i['FOLLOW'])
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
	
	def events(self):
		for event in pygame.event.get():
			self.pressed, self.click = self.guitools.get_pressed(event)
			#EXIT
			if event.type == pygame.QUIT: self.running = False
			#RESIZE
			if event.type == pygame.VIDEORESIZE:
				self.windoww = event.w
				self.windowh = event.h
				self.displayzw = int(self.windoww/res.GSCALE)
				self.displayzh = int(self.windowh/res.GSCALE)
				self.inv = GUI.Inventory((self.displayzw,self.displayzh),0)
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
						rct = pygame.Rect(int(math.floor(((self.click.x/res.GSCALE) + self.cam.x)/self.map.tilewidth) * self.map.tilewidth),
						int(math.floor(((self.click.y/res.GSCALE) + self.cam.y)/self.map.tileheight) * self.map.tileheight),10,10)
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
			
			#DEVICE OPTIONS
			if mnuchk[3] and self.pressed[mnuchk[3]][0] and self.dev != None and self.inv.find(res.PARTY[res.FORMATION][0],'phone') != None and self.inv.type == 0:
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
			if self.minigame != None: self.minigame.events(event)
			for i in self.guis:
				if i.show: i.inside_events(self.pressed,self.click)
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
		self.pressed, self.click = self.guitools.get_pressed(None)
		#BATTLE AIM MOVE
		if self.battle and self.mnu == 2 and res.MOUSE < 2:
			for tp in range(len(self.player)):
				if self.pressed[0][tp] and self.aim.x > 10: self.aim.x -= 1
				if self.pressed[1][tp] and self.aim.x < self.displayzw - 10: self.aim.x += 1
				if self.pressed[2][tp] and self.aim.y > self.winbar: self.aim.y -= 1
				if self.pressed[3][tp] and self.aim.y < self.displayzh - self.winbar: self.aim.y += 1
		#PHONE HOLDING OPTIONS
		if self.phone > 0 and self.dev != None: self.dev.outside_events(self.pressed)
		#READING SCROLL
		if self.read != None: self.read.outside_events(self.pressed)
		for i in self.guis:
			if i.show: i.outside_events(pressed)
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
		#PAINT TILES
		do = False
		if self.pressed[4][0]: do = True
		if pygame.mouse.get_pressed()[0]: do = True
		if self.editing and do and self.paint != '' and self.battle == False and self.phone == 0 and self.player[0]['PAUSE'] == 0:
			if self.inv.type == 0 and self.map.edit:
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
					i['DIRECTION'] = self.guitools.follow(i['RECT'],i['FOLLOW'])
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
			'''dx = 0; dy = 0
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
				#		if obj[0] == 'move': cld = self.colide(i['RECT'],obj[1]['RECT'])'''
			cld = True
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
					self.notification.append({'TEXT': dtb.MENU['not_email'], 'COLOR': (255, 221, 0), 'HALIGN': 'left','X': 0})
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
					self.notification.append({'TEXT': dtb.MENU['not_contact'], 'COLOR': (165, 255, 0), 'HALIGN': 'left','X': 0})
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
				
	def audioedit(self,snd,function,value):
		import numpy
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
			self.bbg['IMAGE'] = pygame.image.load(res.BACKG_PATH + 'bt_' + self.map.habitat + '.png')
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
			if self.turn != -6: self.transiction(True,int(self.windoww/100),type='zoom')
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
			if self.turn != -6: self.transiction(False,int(self.windoww/res.GSCALE),type="zoom")
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
							self.hitisplay(10, i['MASK'], dtb.MENU['critical'], (200, 0, 0))
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
					self.hitisplay(5, self.aim, dtb.MENU['miss'], (200, 200, 200))
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
				self.hitisplay(0, self.aim, dtb.MENU['one_more'], (10, 50, 255))
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
	
	def draw(self):
		for i in self.display: i.fill((0,0,0,0))
		if self.battle and self.turn < 0: self.hpctrl = []
		elif self.dlg['FADE'] > 0: self.hpctrl = []
		else: self.hpctrl = dtb.HINTS['MENUS']
		#TILEMATION
		if self.player[0]['PAUSE'] < 2: self.tilemation += 0.1
		if self.tilemation >= 2.0: self.tilemation = 0.0
		#BLINDNESS
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] == 12: self.display[0].fill((0,0,0))
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
		elif self.map and self.turn != -6:
			self.map.draw()
			'''#SKY
			if len(self.tilmap) > 2:
				tt = (res.TIME[0] * 60) + res.TIME[1]
				img = self.tilmap[3][0]
				self.display[0].blit(img, (0, -int(tt * ((img.get_height() - (img.get_height()/self.displayzh))/1440))))
				if len(self.tilrect) > 5:
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
				px += 3'''
			#MAP FLOOR
			self.display[0].blit(self.map.surfaces[0],(0,0),(self.cam.x,self.cam.y,self.displayzw,self.displayzh))
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
		else: self.display[0].fill((250,10,250))
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
			if self.enemies[i].hp <= 0: del self.enemies[i]; break
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
									pygame.draw.rect(self.display[0], res.COLOR, pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								else: pygame.draw.rect(self.display[0], (255,10,10), pygame.Rect(i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40,16,13))
								self.display[0].blit(pygame.image.load(res.SPRITES_PATH + 'hl_' + str(res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HEALTH']) + '.png'), (i['RECT'].x - self.cam.x + 10 + i['SHK'],i['RECT'].y - self.cam.y - 40))
							if self.map.hscroll != 0 and i['RECT'].x < self.cam.x - self.map.tilewidth: res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] = 0
							if self.map.vscroll != 0 and i['RECT'].y < self.cam.y - self.map.tileheight: res.CHARACTERS[res.PARTY[res.FORMATION][p]]['HP'] = 0
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
													elif t[0]['TYPE'] == 'XXXCOLOR':
														if t[0]['SCALE'] == 30 and t[0]['COLOR'] > 0:
															self.dmg.append({'INFO': pygame.Surface((43,40), pygame.SRCALPHA, 32), 'TYPE': 2,
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
						if i.id == y[1] and self.colide(i.rect,cm): self.display[0].blit(i.sprite,(i.rect.x,i.rect.y)); y[2] = i.rect.y
				#NPCS
				elif y[0] == 'npc':
					for i in self.npcs:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.npc(i); y[2] = i['RECT'].y
				#VEHICLES
				elif y[0] == 'vehicle':
					for i in self.vehicles:
						if i['N'] == y[1] and self.colide(i['RECT'],cm): self.vehicle(i); y[2] = i['RECT'].y
				#PORTALS
				elif y[0] == 'portal' and self.colide(y[1]['RECT'],cm): self.portal(y[1]); y[2] = y[1]['RECT'].y
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
			if self.map:
				if res.MAP != 'rodoviary':
					if self.turn != -6 and res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] != 12:
						if len(self.tilmap) > 1: self.display[0].blit(self.tilmap[2][math.floor(self.tilemation)],(0,0),(self.cam.x, self.cam.y,self.displayzw,self.displayzh))
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
			if self.map and self.map.interior == 0: self.display[0].blit(srf, (0,0))
			#RAIN
			if self.map and self.map.interior == 0 and res.WEATHER == 1 and res.MAP != 'rodoviary':
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
			if self.map and len(self.tilrect) > 3:
				if self.tilhide == False and self.tilalpha > 0: self.tilalpha -= 20
				if self.tilhide and self.tilalpha < 255: self.tilalpha += 20
				if self.tilalpha < 0: self.tilalpha = 0
				if self.tilalpha > 255: self.tilalpha = 255
				al = 255 - self.tilalpha
				for i in self.tilrect[4]:
					srf = pygame.Surface((i[1].width,i[1].height))
					if i[0].endswith('ON') and al > 0: srf.set_alpha(al); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
					if i[0].endswith('OFF') and self.tilalpha > 0: srf.set_alpha(self.tilalpha); srf.fill((0,0,0)); self.display[0].blit(srf, (i[1].x - self.cam.x,i[1].y - self.cam.y))
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
			if self.trsction: self.display[1].blit(self.trsction,(0,0))
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
			for i in self.guitools.transiction((800,600),1,-100,'fade'): self.trsction = i; self.run()
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
					pygame.draw.rect(upsts, res.COLOR, pygame.Rect(p * 120,0,120,100))
					upsts.blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, (0,0,0)), (10 + p * 120, 10))
				else: 
					upsts.blit(self.fnt['MININFO'].render(res.CHARACTERS[ctr]['NAME'].lower(), True, res.COLOR), (10 + p * 120, 10))
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
						pygame.draw.rect(self.display[0], res.COLOR, pygame.Rect(0,self.displayzh - wbrh,int(self.displayzw/(100/self.btime)),5))
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
						pygame.draw.rect(self.display[0],res.COLOR,pygame.Rect(int(self.displayzw/2) - (30 * len(self.dices)) + (y * 80),int(self.displayzh/2) - 30,60,60))
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
					if self.hpl < 0: self.display[0].blit(self.fnt['MININFO'].render(dtb.MENU['victory'], True, (255,255,255)), (pd + 30 + self.mnu, pd - 30))
					else: self.display[0].blit(self.fnt['MININFO'].render(dtb.MENU['perfect'], True, (255,255,255)), (pd + 30 + self.mnu, pd - 30))
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
						self.display[1].blit(self.fnt['DEFAULT'].render(dtb.MENU['level_up'] + str(dtb.CNAMES[ch['CLASS']][ch['LEVEL'] - 1]) + ' !', True, (255,255,255)), ((800 + self.mnu) * res.GSCALE, 70 * res.GSCALE))
				#LOST SCREEN
				elif self.turn == -5:
					self.display[0].blit(self.fnt['MININFO'].render(dtb.MENU['lost'], True, (255,255,255)), (200 + self.mnu, 70))
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
							if i['TYPE'] == 1: fnt = 'MININFO'
							else: fnt = 'SCORETXT'
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
		'''if self.inv.fade < self.windoww + 400:
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
			self.display[0].blit(srf,(self.player[0]['RECT'].x - self.cam.x - int(srf.get_width()/2),self.player[0]['RECT'].y - self.cam.y - int(srf.get_width()/2)))'''
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
							pygame.draw.rect(self.display[0], res.COLOR, pygame.Rect(20,(yyax + 25) + self.dlg['Y'] - yy,5 + txtsz,5))
							pygame.draw.polygon(self.display[0], res.COLOR, ((25,(yyax + 25) + self.dlg['Y'] - yy),(45,(yyax + 25) + self.dlg['Y'] - yy),(25,(yyax + 35) + self.dlg['Y'] - yy)))
							pygame.draw.polygon(self.display[0], (0, 0, 0), ((25,(yyax + 21) + self.dlg['Y'] - yy),(45,(yyax + 21) + self.dlg['Y'] - yy),(25,(yyax + 31) + self.dlg['Y'] - yy)))
						else:
							if self.lopt == opt:
								col1 = res.COLOR
								col2 = (10,10,10)
							else:
								col1 = (10,10,10)
								col2 = res.COLOR
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
		'''sz = 10 * res.GSCALE
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
				x += 1'''
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
		#GUI WINDOWS
		for i in self.guis: self.display[1].blit(i.draw(), (i.rect.x,i.rect.y))
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
			tchpad.fill(res.COLOR,None,pygame.BLEND_RGBA_MULT)
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
					img.fill(res.COLOR,None,pygame.BLEND_RGBA_MULT)
					self.display[1].blit(img,bt[1])
		#DISDEBUG
		if self.disdbg:
			prs = ''
			mix = 0
			osinfo = platform.uname()
			for i in range(len(self.pressed)): prs += str(self.pressed[i][0]) + ','
			for i in range(len(self.channels)):
				if self.channels[i][1]: mix += 1
			dinfo = ['DEVICE WIDTH: ' + str(self.windoww) + ' | DEVICE HEIGHT: ' + str(self.windowh) + ' | ',
			'GAME WIDTH: ' + str(self.displayzw) + ' | GAME HEIGHT: ' + str(self.displayzh) + ' | FPS: ' + str(int(self.glock.get_time())) + ' | ',
			'CAMERA X: ' + str(self.cam.x) + ' | CAMERA Y: ' + str(self.cam.y) + ' | ',
			'SYSTEM: ' + osinfo.system + ' | NODE: ' + osinfo.node + ' | RELEASE: ' + osinfo.release + ' | VERSION: ' + osinfo.version + ' | ',
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
		if len(self.player) == 0: pcam = [int(self.displayzw/2),int(self.displayzh/2)]
		elif self.dlg['CAMERA'] == 0:
			pcam = [0,0]
			for i in self.player:
				if i['POSTURE'] == 2: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y - 200
				else: pcam[0] += i['RECT'].x; pcam[1] += i['RECT'].y
			pcam = [int(pcam[0]/len(self.player)),int(pcam[1]/len(self.player))]
		else: pcam = [self.dlg['CAMERA'].x,self.dlg['CAMERA'].y]

		if self.map:
			cmgrd = [[0,(self.map.width * self.map.tilewidth) - self.displayzw],[0,(self.map.height * self.map.tileheight) - self.displayzh]]
			lst = [[self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight],[self.displayzw,self.displayzh]]
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
		if res.CHARACTERS[res.PARTY[res.FORMATION][0]]['FLAW'] == 'myopia': chk = not chk
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
		if res.MOUSE == 1: self.screen.blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'),(self.click.x,self.click.y))

	def loading(self):
		for event in pygame.event.get():
			#EXIT
			if event.type == pygame.QUIT:
				self.classrun = 0
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
		from traceback import extract_tb
		#self.screen.fill((0,0,0))
		et, ev, eb = sys.exc_info()
		err = str(et.__name__) + ': ' + str(ev) + ''
		tlist = [dtb.ERROR[2] + ' "' + str(i[0]) + '", ' + dtb.ERROR[3] + ' ' + str(i[1]) + ' ' + dtb.ERROR[4] + ' ' + str(i[2]) + ': ' + str(i[3]) for i in extract_tb(eb)]

		fnt = pygame.font.SysFont('Calibri', 26)
		self.screen.blit(fnt.render(dtb.ERROR[0],True,(10,250,10)),(10,20))
		fnt = pygame.font.SysFont('Calibri', 22)
		self.screen.blit(fnt.render(err,True,(10,250,10)),(10,60))
		for i in range(len(tlist)): self.screen.blit(fnt.render(str(tlist[i]),True,(10,250,10)),(10,100 + (i * 20)))
		self.screen.blit(fnt.render(dtb.ERROR[1],True,(10,250,10)),(10,140 + (i * 20)))
		pygame.display.flip()

		self.log += '\n ' + dtb.ERROR[0] + '\n' + err
		print('\n' + dtb.ERROR[0])
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
					self.windowh = event.h
					sh = int(event.h/4)
					self.windoww = 6 * sh
					self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE)
				#SKIP
				do = False
				if event.type == pygame.KEYDOWN: do = True
				if event.type == pygame.MOUSEBUTTONDOWN: do = True
				if do:
					#self.loadmap()
					lp = False
					print(dtb.ERROR[5])

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
			if 'TIME' in dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]] and dtb.TASKINDEX[res.TASKS[0][0]][res.TASKS[0][1]]['TIME'][0] < 0: pom = -1
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
			if res.TIME[0] >= 24: res.DATE[0] += 1; res.DATE[3] += 1; res.TIME[0] = 0; res.TEMPERATURE = dtb.CITIES[self.map.city][1][res.DATE[1] - 1]
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
		res.FPS += 1
		if res.FPS >= jp:
			#UPDATE
			try: pygame.display.flip()
			except: self.screen = pygame.display.set_mode((self.windoww, self.windowh), pygame.RESIZABLE | pygame.DOUBLEBUF)
			#FPS
			res.FPS = int()
			if res.FPS > 0:
				self.glock.tick(res.FPS)
			res.FPS = 0 
			res.GAMETIME += self.glock.get_rawtime()

Initialize()
g = Game()
while g.running:
	try: g.run()
	except: g.crash()

f = open('log.txt','w')
f.write(g.log)
f.close()
pygame.quit()
exit()