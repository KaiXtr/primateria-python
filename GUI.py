# -*- coding: utf-8 -*-
import resources as res
import random
import pygame
import math
import sys
import os

if res.FILES[3] != []:
	if res.FILES[3][0] == 'PT': import database_PT as dtb
	if res.FILES[3][0] == 'EN': import database_EN as dtb
else: import database_PT as dtb

class Debug:
	def __init__(self):
		self.scr = pygame.Surface((1200,50))
		self.fnt = pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 15)
		self.sfx = pygame.mixer.Channel(1)
		self.classrun = True
		self.cmd = ''
		self.goto = ''
		self.dlg = []

	def command(self):
		try:
			if self.cmd.startswith('mute'):
				pygame.mixer.stop()
				pygame.mixer.music.stop()
			elif self.cmd.startswith('sleep'):
				self.dlg = 'sleep'
			elif self.cmd.startswith('pacify'):
				self.dlg = 'pacify'
			elif self.cmd.startswith('storage'):
				self.dlg = 'storage'
			elif self.cmd.startswith('goto'):
				self.goto = self.cmd[5:]
			elif self.cmd.startswith('dialog'):
				self.dlg = dtb.DIALOGS[self.cmd[10:].upper()][int(self.cmd[7:9])]
			elif self.cmd.startswith('dialogs'):
				dtb.load_dialogs()
			elif self.cmd.startswith('battle'):
				if len(self.cmd) > 7: self.dlg = [[13,self.cmd[7:]]]
				else: self.dlg = [[13,'madladcat']]
			elif self.cmd.startswith('item'):
				if len(self.cmd) > 5:
					dtb.ITEMS[self.cmd[5:]]
					self.dlg = [[1,self.cmd[5:],0,0,'9999']]
			elif self.cmd.startswith('level'):
				for i in res.PARTY[res.FORMATION]: res.CHARACTERS[i]['LEVEL'] = int(self.cmd[6:])
			elif self.cmd.startswith('hp'):
				res.CHARACTERS[int(self.cmd[3])]['HP'] = int(self.cmd[5])
			elif self.cmd.startswith('hair'):
				res.CHARACTERS[int(self.cmd[5])]['HAIR'] = self.cmd[7:]
			elif self.cmd.startswith('costume'):
				res.CHARACTERS[int(self.cmd[8])]['COSTUME'] = self.cmd[10:]
			elif self.cmd.startswith('map'):
				res.MAP = int(self.cmd[4:])
			elif self.cmd.startswith('chapter'):
				res.CHAPTER = int(self.cmd[8:])
			elif self.cmd.startswith('money'):
				src = None
				for i in res.PARTY[res.FORMATION]:
					src = self.inv.find(i,'credit_card')
					if src == None:
						src = self.inv.find(i,'wallet')
						if src != None:
							src[1] = int(self.cmd[6:])
							break
					else:
						src[1] = int(self.cmd[6:])
						break
			elif self.cmd.startswith('time'):
				res.TIME = [int(self.cmd[5:7]),int(self.cmd[7:9]),int(self.cmd[9:11])]
			elif self.cmd.startswith('date'):
				res.DATE = [int(self.cmd[5:7]),int(self.cmd[7:9]),int(self.cmd[9:11]),int(self.cmd[11:13]),0]
			elif self.cmd.startswith('weather'):
				res.WEATHER = int(self.cmd[8:])
			elif self.cmd.startswith('party'):
				res.PARTY[res.FORMATION] = [int(self.cmd[6]),int(self.cmd[7]),int(self.cmd[8])]
				res.party_make(0)
			elif self.cmd.startswith('health'):
				res.CHARACTERS[res.PARTY[res.FORMATION][0]]['HEALTH'] = int(self.cmd[7:])
			elif self.cmd == 'rect': self.dlg = 'rectdebug'
			else: self.sfx.play(res.SOUND['ERROR'])
		except: self.sfx.play(res.SOUND['ERROR'])
		self.cmd = ''

	def draw(self):
		self.scr.fill((0,0,0))
		self.scr.blit(self.fnt.render(self.cmd,True,(250,250,250)),(10,10))
		return self.scr

	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.classrun = False
				elif event.key == pygame.K_BACKSPACE:
					self.cmd = self.cmd[:-1]
				else: self.cmd += event.unicode

class Naming:
	def __init__(self):
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 10)}
		self.sfx = pygame.mixer.Channel(1)
		self.ton = pygame.mixer.Channel(2)
		self.wdw = pygame.Surface((200, 200))
		pygame.draw.rect(self.wdw, (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,0,200,200))
		for x in range(20):
			for y in range(20):
				self.wdw.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		self.show = False
		self.scr = [pygame.Surface((180,180)),pygame.Surface((360,360), pygame.SRCALPHA)]
		self.blink = 0.0
		self.bt = ''
		self.name = ['','','','','','']
		self.lame = ['','','','','','']
		self.ninput = True
		self.ind = 0
		self.lopt = 0
		self.did = 0
		self.tim = 3

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.ninput == True:
				if self.ind < 6:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							if self.lopt == 0:
								if len(self.name[self.ind]) > 0: self.lopt = 1; self.ton.play(res.SOUND['MENU_GO'])
								else: self.sfx.play(res.SOUND['ERROR'])
							else:
								if len(self.lame[self.ind]) > 0: self.lopt = 0; self.ind += 1; self.ton.play(res.SOUND['TEXT_ENTER'])
								else: self.sfx.play(res.SOUND['ERROR'])
						elif event.key == pygame.K_BACKSPACE:
							self.sfx.play(res.SOUND['MENU_BACK'])
							if self.lopt == 0:
								if len(self.name[self.ind]) > 0: self.name[self.ind] = self.name[self.ind][:-1]
								elif self.ind > 0: self.ind -= 1; self.lopt = 0
							if self.lopt == 1:
								if len(self.lame[self.ind]) > 0: self.lame[self.ind] = self.lame[self.ind][:-1]
								else: self.lopt = 0
						else:
							self.sfx.play(res.SOUND['TEXT_INPUT'])
							if self.lopt == 0 and len(self.name[self.ind]) < 10: self.name[self.ind] += event.unicode
							if self.lopt == 1 and len(self.lame[self.ind]) < 10: self.lame[self.ind] += event.unicode
				else:
					pressed = pygame.key.get_pressed()
					if pressed[res.LEFT[0]]: self.lopt = 0; self.sfx.play(res.SOUND['MENU_HOR'])
					if pressed[res.RIGHT[0]]: self.lopt = 1; self.sfx.play(res.SOUND['MENU_HOR'])
					if pressed[res.ACT[0]]:
						if self.lopt == 0:
							self.sfx.play(res.SOUND['FILE_NEW'])
							for i in range(len(self.name)):
								res.CHARACTERS[i]['NAME'] = self.name[i]
								res.CHARACTERS[i]['LASTNAME'] = self.lame[i]
							res.save_data()
							res.save_sett()
							res.party_make(0)
							self.show = False
						if self.lopt == 1:
							self.sfx.play(res.SOUND['MENU_BACK'])
							self.ind = 0
							self.lopt = 0

	def run(self):
		for i in self.scr: i.fill((0,0,0))

		self.blink += 0.1
		if math.floor(self.blink) == 0: self.bt = ''
		elif math.floor(self.blink) == 1: self.bt = '.'
		else: self.blink = 0.0

		if self.ninput == False:
			res.CHARACTERS[0]['NAME'] = dtb.NAMES[0]
			res.CHARACTERS[0]['LASTNAME'] = dtb.NAMES[1]
			res.CHARACTERS[1]['NAME'] = dtb.NAMES[2]
			res.CHARACTERS[1]['LASTNAME'] = dtb.NAMES[3]
			res.CHARACTERS[2]['NAME'] = dtb.NAMES[4]
			res.CHARACTERS[2]['LASTNAME'] = dtb.NAMES[5]
			res.CHARACTERS[3]['NAME'] = dtb.NAMES[6]
			res.CHARACTERS[3]['LASTNAME'] = dtb.NAMES[7]
			res.CHARACTERS[4]['NAME'] = dtb.NAMES[8]
			res.CHARACTERS[4]['LASTNAME'] = dtb.NAMES[9]
			res.CHARACTERS[5]['NAME'] = dtb.NAMES[10]
			res.CHARACTERS[5]['LASTNAME'] = dtb.NAMES[11]
			if self.ind < 6:
				if self.lopt == 0:
					if self.tim != 0: self.tim -= 1
					else:
						if len(self.name[self.ind]) != len(res.CHARACTERS[self.ind]['NAME']):
							self.name[self.ind] += res.CHARACTERS[self.ind]['NAME'][self.did]
							self.sfx.play(pygame.mixer.Sound(res.SFX_PATH + 'text_input.wav'))
							self.tim = 3
							self.did += 1
						else: self.ton.play(res.SOUND['MENU_GO']); self.lopt = 1; self.tim = 3; self.did = 0
				if self.lopt == 1:
					if self.tim != 0: self.tim -= 1
					else:
						if len(self.lame[self.ind]) != len(res.CHARACTERS[self.ind]['LASTNAME']):
							self.lame[self.ind] += res.CHARACTERS[self.ind]['LASTNAME'][self.did]
							self.sfx.play(res.SOUND['TEXT_INPUT'])
							self.tim = 3
							self.did += 1
						else: self.ch_ton.play(res.SOUND['TEXT_ENTER']); self.ind += 1; self.lopt = 0; self.tim = 3; self.did = 0
			else:
				self.sfx.play(res.SOUND['FILE_NEW'])
				for i in range(len(self.name)):
					res.CHARACTERS[i]['NAME'] = self.name[i]
					res.CHARACTERS[i]['LASTNAME'] = self.lame[i]
				res.save_data()
				res.save_sett()
				res.party_make(0)
				res.recent_data(1,res.ID)
				self.show = False
		
		if self.ind < 6:
			l1 = self.fnt['CALIBRI'].size(dtb.MENU[80])[0]
			l2 = self.fnt['CALIBRI'].size(dtb.MENU[80])[1]
			if self.lopt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[80] + ': ' + self.name[self.ind] + self.bt, True, (255, 255, 0)), (120 - l1, 60))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[80] + ': ' + self.name[self.ind], True, (255, 255, 255)), (120 - l1, 60))
			if self.lopt == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[81] + ': '+ self.lame[self.ind] + self.bt, True, (255, 255, 0)), (120 - l2, 100))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[81] + ': '+ self.lame[self.ind], True, (255, 255, 255)), (120 - l2, 100))
		else:
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[82], True, (255, 255, 255)), (100, 20))
			y = 0
			for i in range(len(self.name)):
				self.scr[1].blit(self.fnt['CALIBRI'].render(self.name[i] + ' ' + self.lame[i], True, (255, 255, 255)), (20, (30 + (20 * y)) * 2))
				y += 1

			if self.lopt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[83], True, (255, 255, 0)), (100, 320))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[83], True, (255, 255, 255)), (100, 320))
			if self.lopt == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[84], True, (255, 255, 0)), (200, 320))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[84], True, (255, 255, 255)), (200, 320))

		self.wdw.blit(self.scr[0],(10,10))
		return [self.wdw,self.scr[1]]

class Inventory:
	def __init__(self,srf):
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 25), 'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 10)}
		if srf != False:
			#self.wdw = pygame.Surface((srf[0] - int(srf[0]/3), srf[1] - int(srf[1]/4)), pygame.SRCALPHA)
			self.wdw = pygame.Surface((srf[0] - int(srf[0]/3), 300), pygame.SRCALPHA)
			self.wdw.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(math.ceil(self.wdw.get_width()/10)):
				for y in range(math.ceil(self.wdw.get_height()/10)):
					self.wdw.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
			
			self.itbor = pygame.Surface((100, 40))
			self.itbor.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(10):
				for y in range(4):
					self.itbor.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (1 + (x * 10),1 + (y * 10)))
			self.mnbor = pygame.Surface((60, 40))
			self.mnbor.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(6):
				for y in range(4):
					self.mnbor.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (1 + (x * 10),1 + (y * 10)))
			self.scr = [pygame.Surface((self.wdw.get_width() - 20,self.wdw.get_height() - 80)),pygame.Surface(((self.wdw.get_width() - 20) * 2,(self.wdw.get_height() - 20) * 2), pygame.SRCALPHA)]
			self.dsrf = pygame.Surface((self.scr[0].get_width(),50))
		self.itmov = ''
		self.st = [1,0,0]
		self.scroll = 50
		self.strgscroll = 50
		self.shake = 0
		self.arrow = 0
		self.arrdir = False
		self.optrects = []
		x = 10
		y = 45
		for u in range(len(res.PARTY[res.FORMATION])):
			self.optrects.append([])
			for j in range(5):
				self.optrects[u].append([])
				if j == 4: y += 5
				for i in range(5):
					if i == 1: x += 5
					self.optrects[u][j].append((pygame.Rect(x + (200 * u),y,30,30),pygame.Rect(x,y + (210 * u),30,30)))
					x += 32
				x = 10
				y += 32
			x = 10
			y = 45
			
	def money(self,m):
			pass
			
	def get_property(self,g1,g2):
		prp = 0
		for i in res.PARTY[res.FORMATION]:
			src = self.inv.find(i,g1)
			if src == None:
				src = self.inv.find(i,g2)
				if src != None:
					prp = int(src[1][0:6])
					break
			else:
				prp = int(src[1])
				break
				
		return prp

	def find(self, where, item):
		fnd = None
		for i in range(len(res.INVENTORY)):
			able = True
			if where != None:
				if i == where: able = True
				else: able = False
			else: able = True
			if able == True:
				for y in res.INVENTORY[i]:
					for x in y:
						if fnd == None:
							if x[0] == item: fnd = x
							elif x[2] == item: fnd = [x[2],x[3]]
							elif x[4] == item: fnd = [x[4],x[5]]
		return fnd

	def add(self, where, item, prp='0000'):
		i = 0
		j = 0
		trigg = False
		for y in res.INVENTORY[where]:
			if j != 4:
				for x in y:
					if i != 0 and x[0] == '_' and trigg == False:
						vi = prp
						if item.startswith('food'):
							dd = res.DATE[0] + int(dtb.ITEMS[item][7][0:2])
							mm = res.DATE[1] + int(dtb.ITEMS[item][7][2:4])
							if dd > 30: dd -= 30; mm += 1
							if mm > 12: dd += 1; mm -= 12
							if dd < 10: dd = '0' + str(dd)
							if mm < 10: mm = '0' + str(mm)
							vi = str(dd) + str(mm)
						res.INVENTORY[where][j][i] = [item,vi,'_','_']
						trigg = True
					i += 1
			j += 1
			i = 0

	def space(self, where, ex=0, opt=None, lopt=None):
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
			if vlm >= dtb.ITEMS[res.INVENTORY[where][4][0][0]][3]: trigg = False
			if wei >= dtb.ITEMS[res.INVENTORY[where][4][0][0]][4]: trigg = False
		if lopt == 4: trigg = True
		elif opt == 0: trigg = True
		if res.INVENTORY[where][4][0][0] == '_': trigg = True
		return trigg

	def show(self, opt, lopt, mn, ex, tp):
		for i in self.scr: i.fill((0,0,0,0))
		self.dsrf.fill((0,0,0))
		optx = 0
		opty = 0
		mnc = 0
		dscr = '_'
		vlm = 0
		wei = 0
		#SCROLL
		if tp == 0:
			if self.scroll < (mn * 200):
				self.scroll += 40
			if self.scroll > (mn * 200):
				self.scroll -= 40
		if tp == 1:
			if self.scroll < (mn * 210):
				self.scroll += 42
			if self.scroll > (mn * 210):
				self.scroll -= 42
		if self.scroll < 0: self.scroll = 0
		#INVENTORY FOR EACH ONE IN THE PARTY
		for n in res.PARTY[res.FORMATION]:
			self.scr[1].blit(self.fnt['CALIBRI'].render(res.CHARACTERS[n]['NAME'], True, (255, 255, 255)), ((10 + (200 * mnc) - self.scroll) * 2, 15))
			self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(n) + '.png'), (10 + (200 * mnc) - self.scroll, 20))
			for j in range(len(res.INVENTORY[n])):
				for i in range(len(res.INVENTORY[n][j])):
					#CHECK BAG
					trigg = False
					if optx == 0 or opty == 4: trigg = True
					elif res.INVENTORY[n][4][0][0] != '_': trigg = True
					#DRAW RECTS
					if opt == optx and lopt == opty and mn == mnc:
						cl = (res.COLOR[0],res.COLOR[1],res.COLOR[2])
						dscr = res.INVENTORY[res.PARTY[res.FORMATION][mn]][lopt][opt]
					else: cl = (255,255,255)
					rct = self.optrects[n][j][i][tp].copy()
					if tp == 0: rct.x = self.optrects[mnc][j][i][tp].x - self.scroll
					if tp == 1: rct.y = self.optrects[mnc][j][i][tp].y - self.scroll
					if trigg == True:
						pygame.draw.rect(self.scr[0],cl,rct)
					elif opt == optx and lopt == opty and mn == mnc:
						pygame.draw.rect(self.scr[0],cl,rct)
					#DRAW SPRITES
					if trigg == True:
						if res.INVENTORY[n][j][i][0] != '_':
							self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + res.INVENTORY[n][j][i][0] + '.png'), (rct.x,rct.y))
							if self.st == [optx,opty,mnc]:
								self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + 'st.png'), (rct.x,rct.y))
							if optx > 0 and opty < 4:
								vlm += dtb.ITEMS[res.INVENTORY[n][j][i][0]][3]
								wei += dtb.ITEMS[res.INVENTORY[n][j][i][0]][4]
					optx += 1
				optx = 0
				opty += 1
			#VOLUME AND WEIGHT
			if tp == 0:
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[78] + ':', True, (255, 255, 255)), ((65 + 200 * mnc - self.scroll) * 2, 15))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120 + (200 * mnc) - self.scroll,10,50,10))
				if vlm > 0 and res.INVENTORY[n][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120 + (200 * mnc) - self.scroll,10,int(50/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[79] + ':', True, (255, 255, 255)), ((65 + (200 * mnc) - self.scroll) * 2, 45))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120 + (200 * mnc) - self.scroll,25,50,10))
				if wei > 0 and res.INVENTORY[n][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120 + (200 * mnc) - self.scroll,25,int(50/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][4]/wei)),10))
			if tp == 1:
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[78] + ':', True, (255, 255, 255)), (65, (10 + (210 * mnc) - self.scroll) * 2))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120,12 + (210 * mnc) - self.scroll,50,10))
				if vlm > 0 and res.INVENTORY[n][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120,12 + (210 * mnc) - self.scroll,int(50/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[79] + ':', True, (255, 255, 255)), (65, (25 + (210 * mnc) - self.scroll) * 2))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120,27 + (210 * mnc) - self.scroll,50,10))
				if wei > 0 and res.INVENTORY[n][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120,27 + (210 * mnc) - self.scroll,int(50/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][4]/wei)),10))
			vlm = 0
			wei = 0
			optx = 0
			opty = 0
			mnc += 1
		#STORAGE SCROLL
		if lopt > 5:
			if self.strgscroll < (lopt * 32):
				self.strgscroll += 8
			if self.strgscroll > (lopt * 32):
				self.strgscroll -= 8
		else:
			if self.strgscroll > 0:
				self.strgscroll -= 40
		if self.strgscroll < 0: self.strgscroll = 0
		#STORAGE ITEMS
		if tp == 1:
			x = 210
			y = 45
			optx = 5
			opty = 0

			self.scr[1].blit(self.fnt['CALIBRI'].render('Depositar', True, (255, 255, 255)), (420, (10 - self.strgscroll) * 2))
			for j in res.STORAGE:
				if optx == 10:
					x = 210
					y += 32
					optx = 5
					opty += 1

				if opt == optx and lopt == opty:
					pygame.draw.rect(self.scr[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(x, y - self.strgscroll,30,30))
					dscr = j
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x, y - self.strgscroll,30,30))
				if j[0] != '_':
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + j[0] + '.png'), (x, y - self.strgscroll))
				x += 32
				optx += 1
		#HOLDING ITEM
		if self.itmov != '' and self.itmov[0] != '_':
			ox = (opt * 32) 
			lox = (lopt * 32)
			if opt > 0: ox += 5
			if lopt == 4: lox += 5
			if opt > 4: ox += 34
			#ITEM MOVE
			if self.itmov[0] != 0:
				if tp == 0:
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + 'shade.png'), (14 + (mn * 200) + ox - self.scroll,62 + lox))
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + self.itmov[0] + '.png'), (10 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
				if tp == 1:
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + 'shade.png'), (14 + ox,62 + (mn * 210) + lox - self.scroll))
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + self.itmov[0] + '.png'), (10 + ox + self.shake,35 + (mn * 210) + lox - self.scroll))
			#SUB-ITEMS
			else:
				srf = pygame.Surface((70,40))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.scr[0].blit(srf, (25 + (mn * 200) + ox - self.scroll,40 + lox))
				self.scr[0].blit(self.itbor, (20 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
				if ex == 1:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = [self.itmov[ex],res.INVENTORY[res.PARTY[res.FORMATION][mn]][lopt][opt][1][0:4]]
				else: pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 2:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = [self.itmov[ex],res.INVENTORY[res.PARTY[res.FORMATION][mn]][lopt][opt][1][4:8]]
				else: pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 3:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = ['_','0000']
				else: pygame.draw.rect(self.scr[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if self.itmov[1] != '_': self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + self.itmov[1] + '.png'), (25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				if self.itmov[2] != '_': self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + self.itmov[2] + '.png'), (55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_run.png'), (85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
		#ARROWS
		if self.arrdir == False:
			self.arrow += 1
			if self.arrow == 8: self.arrdir = True
		elif self.arrdir == True:
			self.arrow -= 1
			if self.arrow == 0: self.arrdir = False
		if tp == 0:
			if mn > 0: self.scr[0].blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),270), (0 + self.arrow,110))
			if mn < len(res.PARTY[res.FORMATION]) - 1: self.scr[0].blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),90), ((self.scr[0].get_width() - 12) - self.arrow,110))
		if tp == 1:
			if mn > 0: self.scr[0].blit(pygame.transform.flip(pygame.image.load(res.SPRITES_PATH + 'arw.png'),False,True), (80,0 + self.arrow))
			if mn < len(res.PARTY[res.FORMATION]) - 1: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (80,208 - self.arrow))

		self.wdw.blit(self.scr[0], (10,10))
		#ITEM DESCRIPTION
		if self.itmov != '':
			dtp = 1
			for i in ('bag','vest','amulet','tool','melee','gun','grenade'):
				if self.itmov[0].startswith(i):
					dtp = 3
					if dscr[0].startswith(i):
						dtp = 4
			if self.itmov[0] in res.DISITEMS:
				if res.DISITEMS[self.itmov[0]] == 0:
					dtp = 2
			if dtp == 1 and dscr[0] == '_': dtp = 0
		elif dscr[0] != '_': dtp = 1
		else: dtp = 0
		if dtp > 0:
			#ITEM DESCRIPTION
			if dtp == 1:
				txt = dtb.ITEMS[dscr[0]][1].copy()
				if dscr[0].startswith('gun'):
					if len(txt) == 1: txt.append('ammo: ' + str(dscr[1]) + '/' + str(dtb.ITEMS[dscr[0]][5]['CAPACITY']))
					elif len(txt) == 2: txt[1] += ' - ammo: ' + str(dscr[1]) + '/' + str(dtb.ITEMS[dscr[0]][5]['CAPACITY'])
				if dscr[0].startswith('wallet'):
					if len(txt) == 1: txt.append('$' + str(dscr[1][0:6]))
					elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1][0:6])
				if dscr[0].startswith('credit_card'):
					if len(txt) == 1: txt.append('$' + str(dscr[1]))
					elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1])
				if dscr[0].startswith('bottle'):
					if len(txt) == 1: txt.append(str(dscr[1]) + 'ml/' + str(dtb.ITEMS[dscr[0]][5]) + 'ml')
					elif len(txt) == 2: txt[1] += ' - ' + str(dscr[1]) + 'ml/' + str(dtb.ITEMS[dscr[0]][5]) + 'ml'
				y = 0
				for t in txt:
					if res.DISLEXIC == True:
						out = ''
						for tl in t:
							out += tl + ' '
					else: out = t
					self.scr[1].blit(self.fnt['CALIBRI'].render(out, True, (255, 255, 255)), (20, ((self.wdw.get_height() - 60) * 2) + y))
					y += 30
			#NOT DISCOVERED
			elif dtp == 2:
				self.scr[1].blit(self.fnt['CALIBRI'].render('use o item para obter mais informações', True, (255, 255, 255)), (20, (self.wdw.get_height() - 50) * 2))
			#ITEM STATS
			elif dtp > 2:
				xbr = 0
				ybr = 0
				#ARMOR
				if self.itmov[0].startswith('vest') or self.itmov[0].startswith('amulet'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['ARMOR'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]) - math.floor(50/dtb.ITEMS[self.itmov[0]][5])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#DURATION
				if self.itmov[0].startswith('vest') or self.itmov[0].startswith('amulet'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['DURATION'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][6]),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][6]) - math.floor(50/dtb.ITEMS[self.itmov[0]][6])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][6]) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#DAMAGE
				if self.itmov[0].startswith('tool') or self.itmov[0].startswith('melee') or self.itmov[0].startswith('gun') or self.itmov[0].startswith('grenade'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['DAMAGE'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]['DAMAGE']),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]['DAMAGE']) - math.floor(50/dtb.ITEMS[self.itmov[0]][5]['DAMAGE'])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]['DAMAGE']) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#RECHARGE
				if self.itmov[0].startswith('gun'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['RECHARGE'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]['RECHARGE']),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]['RECHARGE']) - math.floor(50/dtb.ITEMS[self.itmov[0]][5]['RECHARGE'])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]['RECHARGE']) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#CADENCY
				if self.itmov[0].startswith('gun'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['CADENCY'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CADENCY']),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]['CADENCY']) - math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CADENCY'])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CADENCY']) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#CAPACITY
				if self.itmov[0].startswith('gun'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['CAPACITY'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CAPACITY']),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]['CAPACITY']) - math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CAPACITY'])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]['CAPACITY']) + sx,10 + (ybr * 20),abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#VITALITY
				if self.itmov[0].startswith('food') or self.itmov[0].startswith('drink'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['VITALITY'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][5]),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][5]) - math.floor(50/dtb.ITEMS[self.itmov[0]][5])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][5]),10 + (ybr * 20) + sx,abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#HUNGER
				if self.itmov[0].startswith('food'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['HUNGER'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][6]),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][6]) - math.floor(50/dtb.ITEMS[self.itmov[0]][6])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][6]),10 + (ybr * 20) + sx,abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
				#THIRST
				if self.itmov[0].startswith('drink'):
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ITINFO['THIRST'], True, (255, 255, 255)), ((10 + (xbr * 200)) * 2, (self.wdw.get_height() - 60 + (ybr * 20)) * 2))
					pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),50,10))
					pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(100 + (xbr * 200),10 + (ybr * 20),math.floor(50/dtb.ITEMS[self.itmov[0]][6]),10))
					if dtp == 4:
						df = math.floor(50/dtb.ITEMS[dscr[0]][6]) - math.floor(50/dtb.ITEMS[self.itmov[0]][6])
						if df != 0:
							if df < 0: col = (200,10,10); sx = -df
							if df > 0: col = (10,200,10); sx = 0
							pygame.draw.rect(self.dsrf,col,pygame.Rect(100 + (xbr * 200) + math.floor(50/dtb.ITEMS[self.itmov[0]][6]) + df,10 + (ybr * 20) + sx,abs(df),10))
					ybr += 1
					if ybr == 2:
						xbr += 1
						ybr = 0
		#ITEM SHAKE
		if self.shake > 0: self.shake = -self.shake
		elif self.shake < 0: self.shake = -self.shake - 1
		
		self.wdw.blit(self.dsrf,(10,self.wdw.get_height() - 60))

		return [self.wdw,self.scr[1]]

class Shop:
	def __init__(self):
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 25), 'DATETIME': pygame.font.Font(res.FONTS_PATH + 'datetype.ttf', 8)}
		self.wdw = pygame.Surface((400, 250))
		pygame.draw.rect(self.wdw, (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(0,0,400,250))
		for x in range(40):
			for y in range(25):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		self.scr = [pygame.Surface((380,230)),pygame.Surface((760,460), pygame.SRCALPHA)]
		self.inv = Inventory(False)
		
	def products(self, opt, lopt, lst):
		for i in self.scr: i.fill((0,0,0,0))
		mny = 0
		for i in res.PARTY[res.FORMATION]:
			src = self.inv.find(i,'credit_card')
			if src == None:
				src = self.inv.find(i,'wallet')
				if src != None:
					mny = int(src[1][0:6])
					break
			else:
				mny = int(src[1])
				break
		self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(mny), True, (255, 255, 255)), (20, 10))

		y = 0
		for i in lst:
			if lopt == y:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,33 + (y * 12),370,12))
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(dtb.ITEMS[i][2]) + ' - ' + dtb.ITEMS[i][0], True, (0, 0, 0)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt['CALIBRI'].render(str(opt) + 'x', True, (0, 0, 0)), (360, 30 + (y * 12)))
			else:
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(dtb.ITEMS[i][2]) + ' - ' + dtb.ITEMS[i][0], True, (255, 255, 255)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt['CALIBRI'].render(str(opt) + 'x', True, (255, 255, 255)), (360, 30 + (y * 12)))
			y += 1

		if lopt != len(lst):
			l = 0
			for j in dtb.ITEMS[lst[lopt]][1]:
				self.scr[0].blit(self.fnt['CALIBRI'].render(j, True, (255, 255, 255)), (20,200 + (l * 10)))
				l += 1

		if lopt == y:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,33 + (y * 12),370,12))
			self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[1], True, (0, 0, 0)), (20, 30 + (y * 12)))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[1], True, (255, 255, 255)), (20, 30 + (y * 12)))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def buy(self, opt, lopt, lst):
		for i in self.scr: i.fill((0,0,0,0))
		mny = self.inv.get_property('credit_card','wallet')
		pygame.draw.line(self.scr, (255, 255, 255), (5,15),(395,15),2)
		pygame.draw.line(self.scr, (255, 255, 255), (300,15),(300,230),2)
		pygame.draw.line(self.scr, (255, 255, 255), (300,160),(395,160),2)
		pygame.draw.line(self.scr, (255, 255, 255), (300,180),(395,180),2)
		pygame.draw.line(self.scr, (255, 255, 255), (5,200),(395,200),2)
		pygame.draw.line(self.scr, (255, 255, 255), (5,230),(395,230),2)

		y = 0
		cost = 0
		if len(lst) > 0:
			for i in lst:
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(dtb.ITEMS[i][2]) + ' - ' + dtb.ITEMS[i][0], True, (255, 255, 255)), (20, 25 + (y * 15)))
				cost += dtb.ITEMS[i][2]
				y += 1

		self.scr[0].blit(self.fnt['CALIBRI'].render('valor: ' + str(mny), True, (255, 255, 255)), (305, 165))
		self.scr[0].blit(self.fnt['CALIBRI'].render('total: ' + str(cost), True, (255, 255, 255)), (305, 185))
		if mny - cost > 0: pcol = (0,255,0)
		else: pcol = (255,0,0)
		self.scr[0].blit(self.fnt['CALIBRI'].render('troco: ' + str(mny - cost), True, pcol), (305, 205))
		self.scr[0].blit(self.fnt['CALIBRI'].render('atendente: ', True, (255, 255, 255)), (10, 230))
		self.scr[0].blit(self.fnt['CALIBRI'].render('hora: ' + str(res.TIME[0]) + ': ' + str(res.TIME[1]), True, (255, 255, 255)), (200, 230))
		self.scr[0].blit(self.fnt['CALIBRI'].render('data: ' + str(res.DATE[0]) + '/ ' + str(res.DATE[1]), True, (255, 255, 255)), (300, 230))

		if lopt == 0:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,204,300,12))
			self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[0], True, (0,0,0)), (10, 201))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[0], True, (255, 255, 255)), (10, 201))

		if lopt == 1:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,216,300,12)); tcol = (0,0,0)
			self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[7], True, (0, 0, 0)), (10, 213))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.SHOP[7], True, (255, 255, 255)), (10, 213))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def mercator(self, opt, lopt, lst, prm):
		for i in self.scr: i.fill((0,0,0,0))
		mny = self.inv.get_property('credit_card','wallet')
		#OPTIONS
		self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(mny), True, (255, 255, 255)), (20, 20))
		if opt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.SHOP[8], True, (res.COLOR[0], res.COLOR[1], res.COLOR[2])), (20, 60))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.SHOP[8], True, (255,255,255)), (20, 60))
		x = 1
		for i in res.PARTY[res.FORMATION]:
			if opt == x: self.scr[1].blit(self.fnt['CALIBRI'].render(res.CHARACTERS[i]['NAME'], True, (res.COLOR[0], res.COLOR[1], res.COLOR[2])), (40 + (x * 120), 60))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(res.CHARACTERS[i]['NAME'], True, (255,255,255)), (40 + (x * 120), 60))
			x += 1
		y = 0
		for i in lst:
			#MERCATOR PRODUCTS
			if opt == 0:
				if prm > 0:
					prc = dtb.ITEMS[i][2] - int(dtb.ITEMS[i][2]/prm)
				else: prc = dtb.ITEMS[i][2]
				if lopt == y:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(prc) + ' - ' + dtb.ITEMS[i][0], True, (res.COLOR[0], res.COLOR[1], res.COLOR[2])), (20, (50 + (y * 15)) * 2))
				else:
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(prc) + ' - ' + dtb.ITEMS[i][0], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))
				if prm > 0:
					pygame.draw.rect(self.scr[0], (255, 170, 0), pygame.Rect(350,50 + (y * 15),30,20))
					self.scr[1].blit(self.fnt['DATETIME'].render(str(prm) + '%', True, (255, 255, 255)), (350, (50 + (y * 15)) * 2))
				y += 1
			#SELLING PARTY ITEMS
			else:
				itm = res.INVENTORY[res.PARTY[res.FORMATION][opt - 1]][i[0]][i[1]][0]
				if lopt == y:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(int(dtb.ITEMS[itm][2]/2)) + ' - ' + dtb.ITEMS[itm][0], True, (res.COLOR[0], res.COLOR[1], res.COLOR[2])), (20, (50 + (y * 15)) * 2))
				else:
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(int(dtb.ITEMS[itm][2]/2)) + ' - ' + dtb.ITEMS[itm][0], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))
				y += 1
		#ITEMS DESCRIPTIONS
		if lopt != len(lst):
			l = 0
			if opt == 0:
				for j in dtb.ITEMS[lst[lopt]][1]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(j, True, (255, 255, 255)), (20,(190 + (l * 15)) * 2))
					l += 1
			else:
				for t in dtb.ITEMS[res.INVENTORY[res.PARTY[res.FORMATION][opt - 1]][lst[lopt][0]][lst[lopt][1]][0]][1]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(t, True, (255, 255, 255)), (20,(190 + (l * 15)) * 2))
					l += 1
		#EXIT SHOP
		if lopt == y:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.SHOP[1], True, (res.COLOR[0], res.COLOR[1], res.COLOR[2])), (20, (50 + (y * 15)) * 2))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.SHOP[1], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))

		self.wdw.blit(self.scr[0], (10,10))
		return [self.wdw, self.scr[1]]

	def bank(self, opt, lopt, mn, ext):
		self.scr[0].fill((234,234,234))
		mny = 0
		for i in res.PARTY[res.FORMATION]:
			src = self.inv.find(i,'credit_card')
			if src == None:
				src = self.inv.find(i,'wallet')
				if src != None:
					mny += int(src[1][0:6])
			else:
				mny += int(src[1])
		if mn == 3:
			if lopt == 0:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,120,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[5], True, (0,0,0)), (10, 120))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,120,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[5], True, (0, 0, 0)), (10, 120))

			if lopt == 1:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[6], True, (0, 0, 0)), (10, 160))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[6], True, (0, 0, 0)), (10, 160))

			if lopt == 2:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[7], True, (0, 0, 0)), (10, 200))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(dtb.SHOP[7], True, (0, 0, 0)), (10, 200))

		else:
			pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(80,80,200,110))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,90,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,120,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,150,130,27))
			pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(120 + opt * 6,135,5,2))

			self.scr[0].blit(self.fnt['TITLE'].render(str(res.ATM), True, (0,0,0)), (120, 90))
			self.scr[0].blit(self.fnt['TITLE'].render(str(ext[0]) + str(ext[1]) + str(ext[2]) + str(ext[3]) + str(ext[4]) + str(ext[5]), True, (0,0,0)), (120, 120))
			self.scr[0].blit(self.fnt['TITLE'].render(str(mny), True, (0,0,0)), (120, 150))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

class PhoneBar:
	def __init__(self):
		self.scr = [pygame.Surface((232,18)),pygame.Surface((464,36), pygame.SRCALPHA)]
		self.fnt = {'DATETIME': pygame.font.Font(res.FONTS_PATH + 'Sicret_PERSONAL-Regular.ttf', 32)}
		self.credit = 0
		self.inv = Inventory(False)
		self.battery = self.inv.find(res.PARTY[res.FORMATION][0],'phone')
		if self.battery != None:
			if self.battery[2] == 'sim_card': self.credit = int(self.battery[3])
			elif self.battery[4] == 'sim_card': self.credit = int(self.battery[5])
			self.battery = int(self.battery[1])
		else: self.battery = 0
	
	def draw(self):
		for i in self.scr: i.fill((10,10,10,0))
		dvd3 = math.floor(self.scr[0].get_width()/3)

		day = ['','','']
		if res.DATE[0] < 10: day[0] = '0' + str(res.DATE[0])
		else: day[0] = str(res.DATE[0])
		if res.DATE[1] < 10: day[1] = '0' + str(res.DATE[1])
		else: day[1] = str(res.DATE[1])
		if res.DATE[2] < 10: day[2] = '0' + str(res.DATE[2])
		else: day[2] = str(res.DATE[2])
		self.scr[1].blit(self.fnt['DATETIME'].render(day[0] + '/' + day[1] + '/' + day[2], True, (255, 255, 255)), (3, 4))

		hour = ['','']
		if res.TIME[0] < 10: hour[0] = '0' + str(res.TIME[0])
		else: hour[0] = str(res.TIME[0])
		if res.TIME[1] < 10: hour[1] = '0' + str(res.TIME[1])
		else: hour[1] = str(res.TIME[1])
		self.scr[1].blit(self.fnt['DATETIME'].render(hour[0] + ':' + hour[1], True, (255, 255, 255)), ((dvd3 + 30) * 2, 4))

		self.scr[0].blit(pygame.image.load('Sprites/signal_' + str(res.SIGNAL) + '.png'), ((dvd3 * 3) - 47, 6))
		self.scr[0].blit(pygame.image.load('Sprites/battery.png'), ((dvd3 * 3) - 30, 2))
		if self.battery > 200: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect((dvd3 * 3) - 7 - int(18/(3600/self.battery)),5,int(18/(3600/self.battery)),7))
		elif self.battery > 0: pygame.draw.rect(self.scr[0], (255, 10, 10), pygame.Rect((dvd3 * 3) - 7 - int(18/(3600/self.battery)),5,int(18/(3600/self.battery)),7))

		return self.scr

class Apps:
	def __init__(self,t):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.nb = None
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.opt = [0,0]
		self.optrects = []
		if t == 0: rng = 3
		if t == 1: rng = 4
		i = 0
		for y in range(3):
			for x in range(rng):
				self.optrects.append([i,x,y])
				i += 1
		self.app = None
		self.type = t
		self.hpctrl = 'PHONE_APPS'
		
	def inside_events(self,pressed):
		if self.app == None:
			if pressed[0][0]: self.opt[1] -=1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt[1] +=1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[2][0]: self.opt[0] -=1; self.sfx.play(res.SOUND['MENU_HOR'])
			if pressed[3][0]: self.opt[0] +=1; self.sfx.play(res.SOUND['MENU_HOR'])
			
			if self.opt[0] < 0: self.opt[0] = 2
			if self.opt[0] > 2: self.opt[0] = 0
			if self.opt[1] < 0: self.opt[1] = self.type + 3
			if self.opt[1] > self.type + 3: self.opt[1] = 0

			if pressed[4][0]:
				self.sfx.play(res.SOUND['MENU_GO'])
				if self.type == 0:
					if self.opt == [0,0]: self.app = Contacts(); self.hpctrl = 'PHONE_CONTACTS'
					if self.opt == [1,0]: self.app = Stats(); self.hpctrl = 'PHONE_STATS'
					if self.opt == [2,0]: self.app = Tactics(); self.hpctrl = 'PHONE_TACTICS'
					if self.opt == [0,1]: self.app = Tasks(); self.hpctrl = 'PHONE_TASKS'
					if self.opt == [1,1]: self.app = Achievements(); self.hpctrl = 'PHONE_ACHIEVEMENTS'
					if self.opt == [2,1]: self.app = Ranking(); self.hpctrl = 'PHONE_RANK'
					if self.opt == [0,2]: self.app = Help(); self.hpctrl = 'PHONE_MANUAL'
					if self.opt == [1,2]: self.app = About(); self.hpctrl = 'PHONE_ABOUT'
					if self.opt == [2,2]: self.app = Settings(); self.hpctrl = 'PHONE_SETTINGS'
				if self.type == 1:
					if self.opt == [0,0]: self.app = Contacts(); self.hpctrl = 'PHONE_CONTACTS'
					if self.opt == [1,0]: self.app = Email(); self.hpctrl = 'PHONE_EMAIL'
					if self.opt == [2,0]: self.app = Radio(); self.hpctrl = 'PHONE_RADIO'
					if self.opt == [0,1]: self.app = Camera(); self.hpctrl = 'PHONE_CAMERA'
					if self.opt == [1,1]: self.app = Tasks(); self.hpctrl = 'PHONE_TASKS'
					if self.opt == [2,1]: self.app = Stats(); self.hpctrl = 'PHONE_STATS'
					if self.opt == [0,2]: self.app = Tactics(); self.hpctrl = 'PHONE_TACTICS'
					if self.opt == [1,2]: self.app = Achievements(); self.hpctrl = 'PHONE_ACHIEVEMENTS'
					if self.opt == [2,2]: self.app = Ranking(); self.hpctrl = 'PHONE_RANK'
					if self.opt == [0,3]: self.app = Help(); self.hpctrl = 'PHONE_MANUAL'
					if self.opt == [1,3]: self.app = About(); self.hpctrl = 'PHONE_ABOUT'
					if self.opt == [2,3]: self.app = Settings(); self.hpctrl = 'PHONE_SETTINGS'
		else:
			self.app.inside_events(pressed)
			self.ingame = self.app.ingame
			if self.opt == [0,0]: self.nb = self.app.nb
			if pressed[5][0]:
				if res.CHAPTER != 0 or res.SCENE != 0:
					self.sfx.play(res.SOUND['MENU_BACK'])
					self.app = None
						
	def outside_events(self,pressed):
		if self.app != None: self.app.outside_events(pressed)
	
	def draw(self):
		if self.app == None:
			for i in self.scr: i.fill((10,10,10,0))
	
			if self.opt[1] > 2:
				if self.scroll < (self.opt[1] - 2) * 60:
					self.scroll += 10
			elif self.opt[1] > 0 and self.opt[1] < 3:
				if self.scroll > (self.opt[1] - 1) * 60:
					self.scroll -= 10
			elif self.opt[1] == 0 and self.scroll > 0:
				self.scroll -= 10
	
			self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'phone_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))
			if self.type == 0:
				imgs = ['call','stts','tact','task','achi','rank','help','info','sett']
			if self.type == 1:
				imgs = ['call','mail','radi','camr','task','stts','tact','achi','rank','help','info','sett']
			if self.type == 2:
				imgs = ['maps','call','mail','news','radi','camr','best','task','stts','tact','achi','rank','help','sett','info']
			dvd3 = math.floor(self.scr[0].get_width()/3)
			pdd = 10
			for i in self.optrects:
				img = pygame.image.load(res.SPRITES_PATH + 'ph_' + imgs[i[0]] + '.png')
				if self.opt[0] == i[1] and self.opt[1] == i[2]: self.scr[0].blit(pygame.transform.scale(img, (50, 50)), (pdd - 3 + (dvd3 * i[1]), 2 + (60 * i[2]) - self.scroll))
				else: self.scr[0].blit(img, (pdd + (dvd3 * i[1]), 5 + (60 * i[2]) - self.scroll))
	
			return self.scr
		else: return self.app.draw()

class GPS:
	def __init__(self, mn, rm, tl, pl, en, sig):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.scroll = 0
		self.mp = None
		self.optrects = []
		self.xy = [80,80]
		self.zoom = 200
		self.hpctrl = 'PHONE_MAP'
		
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
		
	def inside_events(self,pressed):
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
	
	def draw(self):
		sz = self.scr[0].get_width() #button width
		if self.mn == False: scr = [pygame.Surface((sz,232)),pygame.Surface((sz * 2,464),pygame.SRCALPHA)]
		if self.mn == True: scr = [pygame.Surface((100,100)),pygame.Surface((200,200),pygame.SRCALPHA)]
		for i in scr: i.fill((0,0,0,0))
		if res.SIGNAL > 0:
			mpx = self.xy[0] - int(self.zoom/2)
			mpy = self.xy[1] - int(self.zoom/2)
			scr[0].blit(pygame.transform.scale(self.mp, (self.zoom,self.zoom)), (mpx,mpy))

			xx = (self.pl['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
			yy = (self.pl['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
			scr[0].blit(pygame.image.load('Sprites/mp_player.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in res.MARKER:
				xx = (i[1] - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
				yy = (i[2] - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				#if i[0] == rm:
				scr[0].blit(pygame.image.load('Sprites/mp_pin' + str(i[3]) + '.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in self.sig:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				scr[0].blit(pygame.image.load('Sprites/mp_' + i['ICON'] + '.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
			for i in self.en:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(self.rm.width * self.rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(self.rm.height * self.rm.tileheight)
				if i['HP'] > 0 and i['RECT'].x > 0 and i['RECT'].y > 0:
					scr[0].blit(pygame.image.load('Sprites/mp_anomaly.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
		else: scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (25, 200))

		if self.mn == False:
			pygame.draw.rect(scr[1], (140, 255, 253), pygame.Rect(0,0,sz * 2,80))
			scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[0], True, (0, 0, 0)), (5, 4))

		return scr

class Contacts:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.ton = pygame.mixer.Channel(1)
		self.ton.set_volume(res.SFX)
		self.ingame = 0
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.nb = None
		self.credit = 0
		self.inv = Inventory(False)
		self.battery = self.inv.find(res.PARTY[res.FORMATION][0],'phone')
		if self.battery != None:
			if self.battery[2] == 'sim_card': self.credit = int(self.battery[3])
			elif self.battery[4] == 'sim_card': self.credit = int(self.battery[5])
			self.battery = int(self.battery[1])
		else: self.battery = 0
		self.mnu = 0
		self.exvar = 0
		
	def inside_events(self,pressed):
		#SELECT OPTIONS
		if pressed[2][0]:
			self.sfx.play(res.SOUND['MENU_HOR'])
			if self.mnu == 0: self.opt[0] -= 1; self.opt[1] = 0
			elif self.mnu < 3: self.mnu = 1
			else:
				self.mnu -= 1
				if self.mnu < 3: self.mnu = 5

		if pressed[3][0]:
			self.sfx.play(res.SOUND['MENU_HOR'])
			if self.mnu == 0: self.opt[0] += 1; self.opt[1] = 0
			elif self.mnu < 3: self.mnu = 2
			else:
				self.mnu += 1
				if self.mnu > 5: self.mnu = 3

		if pressed[0][0]:
			self.sfx.play(res.SOUND['MENU_VER'])
			if self.mnu < 3: self.opt[1] -= 1
			else:
				self.exvar -= 1
				if self.exvar < 0: self.exvar = 5
				res.PARTY[self.opt[1]][self.mnu - 3] = self.exvar

		if pressed[1][0]:
			self.sfx.play(res.SOUND['MENU_VER'])
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
				self.sfx.play(res.SOUND['MENU_GO'])
				if self.opt[1] < len(res.PARTY):
					if self.mnu == 0:
						self.mnu = 1
					elif self.mnu == 1:
						res.FORMATION = self.opt[1]
						for i in res.PARTY[res.FORMATION]:
							res.CHARACTERS[i]['HP'] = dtb.CLASSES[res.CHARACTERS[i]['CLASS']]['RESISTANCE'][res.CHARACTERS[i]['LEVEL']]
						self.ton.play(res.SOUND['PARTY_CHANGE'])
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
					pygame.time.wait(round(random.randint(10,200)))
					if self.credit > 0:
						credit = self.inv.find(res.PARTY[res.FORMATION][0],'phone')
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
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
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
		for i in self.scr: i.fill((10,10,10,0))
		y = 0
		for i in em:
			if self.opt[1] != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,sz,50))

			if self.opt[0] > 0: self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, (76 + y - self.scroll) * 2))
			else:
				if self.opt[1] == y/51:
					if self.mnu == 1: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 52,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_9.png'), (sz - 50, 76 + y - self.scroll))
					if self.mnu == 2: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 30,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_8.png'), (sz - 28, 76 + y - self.scroll))
					if self.mnu == 3: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(8,74 + y - self.scroll,24,24))
					if self.mnu == 4: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(30,74 + y - self.scroll,24,24))
					if self.mnu == 5: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(52,74 + y - self.scroll,24,24))
				x = 0
				for p in i:
					self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (10 + x, 76 + y - self.scroll))
					x += 22
			if self.opt[0] == 0: self.scr[1].blit(self.fnt['CALIBRI'].render('grupo ' + str(int((y + 51)/51)), True, (0, 0, 0)), (20, (96 + y - self.scroll) * 2))
			if self.opt[0] == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, (92 + y - self.scroll) * 2))
			if self.opt[0] == 2: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(i[1]).lower() + '.png'), (160, 43 + y - self.scroll))
			y += 51
		if self.opt[0] == 0:
			if self.opt[1] != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[31], True, (0, 0, 0)), (170, (83 + y - self.scroll) * 2))
		if y == 0 and self.opt[0] == 1:
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[16], True, (255, 255, 255)), (100, 280))
		dvd3 = math.floor(sz/3)
		if self.opt[0] == 0:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[23], True, (0, 0, 0)), (16, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(0,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[23], True, (255, 255, 255)), (16, 94))
		if self.opt[0] == 1:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[24], True, (0, 0, 0)), ((dvd3 * 2) + 20, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(dvd3,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[24], True, (255, 255, 255)), ((dvd3 * 2) + 20, 94))
		if self.opt[0] == 2:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[25], True, (0, 0, 0)), ((dvd3 * 4) + 20, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(dvd3 * 2,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[25], True, (255, 255, 255)), ((dvd3 * 4) + 20, 94))
		pygame.draw.rect(self.scr[1], (15, 255, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[1], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Email:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed):
		if res.SIGNAL > 0:
			if self.mnu == 0:
				if pressed[0][0]: self.opt[1] -= 1; self.sfx.play(res.SOUND['MENU_VER'])
				if pressed[1][0]: self.opt[1] += 1; self.sfx.play(res.SOUND['MENU_VER'])
				if pressed[2][0]: self.opt[0] -= 1; self.opt[1] = 0; self.c
				sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: self.opt[0] += 1; self.opt[1] = 0; self.sfx.play(res.SOUND['MENU_HOR'])

			if pressed[4][0] and res.SIGNAL > 0:
				if self.mnu == 0: self.mnu = 1; self.sfx.play(res.SOUND['MENU_GO'])
				elif self.mnu > 0:
					self.sfx.play(res.SOUND['MENU_BACK'])
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
		sz = self.scr[0].get_width() #button width
		self.e_read = []
		self.e_unread = []
		for i in res.INBOX:
			if i[3] == 1:
				self.e_read.append(i)
			if i[3] == 0:
				self.e_unread.append(i)
				
		if self.opt[0] == 0: em = self.e_unread
		if self.opt[0] == 1: em = self.e_read
		if self.opt[0] == 2: em = res.INBOX

		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0:
			if self.mnu == 0:
				self.scroll = 0
				if self.opt[1] > 2: self.scroll += (self.opt[1] - 2) * 51

				y = 0
				for i in em:
					if self.opt[1] != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
					else: pygame.draw.rect(self.scr[0], (255, 221, 0), pygame.Rect(0,66 + y,sz,50))
					self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, 152 + y - self.scroll))
					self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, 172 + y - self.scroll))
					y += 51
				if y == 0:
					self.scr[0].blit(self.fnt['CALIBRI'].render(dtb.MENU[19], True, (255, 255, 255)), (510, 280))

				dvd3 = math.floor(sz/3)
				if self.opt[0] == 0:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[26], True, (0, 0, 0)), (24, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[26], True, (255, 255, 255)), (24, 94))
				if self.opt[0] == 1:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[27], True, (0, 0, 0)), ((dvd3 * 2) + 30, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[27], True, (255, 255, 255)), ((dvd3 * 2) + 30, 94))
				if self.opt[0] == 2:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[28], True, (0, 0, 0)), ((dvd3 * 4) + 24, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[28], True, (255, 255, 255)), ((dvd3 * 4) + 24, 94))

			elif self.mnu > 0:
				self.scroll = (self.mnu - 1) * 3
				pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
				self.scr[1].blit(self.fnt['CALIBRI'].render(em[self.opt[1]][1], True, (0, 0, 0)), (30, 110 - self.scroll))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[34] + em[opt][0], True, (0, 0, 0)), (30, 170 - self.scroll))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[35] + (res.CHARACTERS[res.PARTY[0][0]]['NAME'] + res.CHARACTERS[res.PARTY[0][0]]['LASTNAME']).lower() + '@cmail.com', True, (0, 0, 0)), (30, 200 - self.scroll))
				y = 0
				for l in em[self.opt[1]][2]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (15, 130 + y - self.scroll))
					y += 15
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (100, 200))

		pygame.draw.rect(self.scr[1], (255, 221, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[2], True, (0, 0, 0)), (10, 10))

		return self.scr

class Newspaper:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'TITLE': pygame.font.SysFont('Times New Roman', 32),'MEDIUM': pygame.font.SysFont('Calibri', 30), 'SMALL': pygame.font.SysFont('Calibri', 20)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.page = 0
		self.rdnws = []
		for i in range(5):
			nw = ''
			prb = random.randint(0,len(dtb.RANDNEWS[0]) - 1)
			nw += dtb.RANDNEWS[0][prb][0]
			fnd = dtb.RANDNEWS[0][prb][1]
			while True:
				add = random.randint(0,len(fnd) - 1)
				if isinstance(fnd[add],str):
					nw += ' ' + fnd[add]
					break
				else:
					nw += ' ' + fnd[add][0]
					fnd = fnd[add][1]
			if prb in [0,1]:
				pprb = random.randint(0,100)
				if pprb > 50:
					pl = random.randint(0,len(dtb.RANDNEWS[1]) - 1)
					nw += ' ' + dtb.RANDNEWS[1][pl]
			nw += '.'
			self.rdnws.append(nw)
		
	def inside_events(self,pressed):
		if pressed[2][0]: self.page -= 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page += 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((200,200,200,0))
		
		pygame.draw.rect(self.scr[0],(50,50,200),pygame.Rect(5,5,sz - 10,40))
		self.scr[1].blit(self.fnt['TITLE'].render('O LOBO', True, (200,200,200)), (40, 25))
		self.scr[1].blit(self.fnt['SMALL'].render(str(res.DATE[0]) + '/' + str(res.DATE[1]) + ' - 1ª edição', True, (10,10,10)), (30, 50))
		for y in range(5):
			if y == 0: self.scr[1].blit(self.fnt['MEDIUM'].render(self.rdnws[y], True, (10,10,10)), (25, 70))
			else: self.scr[1].blit(self.fnt['SMALL'].render(self.rdnws[y], True, (10,10,10)), (25, 100 + (y * 20)))

		return self.scr
	
class News:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.page = 0
		
	def inside_events(self,pressed):
		if res.SIGNAL > 0:
			if self.mnu == 0:
				if pressed[0][0]: self.lopt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
				if pressed[1][0]: self.lopt += 1; self.sfx.play(res.SOUND['MENU_VER'])

			if pressed[4][0]:
				self.sfx.play(res.SOUND['MENU_GO'])
				if self.mnu == 0: self.mnu = 1
				elif self.mnu > 0: self.mnu = 0

			if self.lopt < 0: self.lopt = 3
			if self.lopt > 3: self.lopt = 0
	
	def outside_events(self,pressed):
		if self.mnu > 0:
			if pressed[0][0]: self.mnu -= 2
			if pressed[1][0]: self.mnu += 2

			if self.mnu < 1: self.mnu = 1
			if self.mnu > 1000: self.mnu = 1000
	
	def draw(self):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0:
			if mnu == 0:
				self.scroll = 0
				if opt > 2: self.scroll += (opt - 2) * 51
				y = 0
				opty = 0
				hei = 0
				for i in dtb.NEWS[res.DATE[0] - 1]:
					if isinstance(i[0],list):
						for l in i[0]: hei += 20
						hei += 20
						if opt != opty: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50 + y + hei))
						else: pygame.draw.rect(self.scr[0], (219, 49, 37), pygame.Rect(0,41 + y,sz,50 + y + hei))

						yi = 0
						for l in i[0]:
							self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (20, (46 + y - self.scroll + yi) * 2))
							yi += 15

						self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, (52 + y - self.scroll + yi) * 2))
					elif i[0] == 1:
						pygame.draw.rect(self.scr[0], (219, 49, 37), pygame.Rect(0,41 + (y * hei),sz,50 + (y * hei)))
						self.scr[1].blit(self.fnt['CALIBRI'].render(i[1][0], True, (0, 0, 0)), (20, (46 + (y * hei) - self.scroll) * 2))
						self.scr[1].blit(self.fnt['CALIBRI'].render(i[1][1], True, (0, 0, 0)), (20, (56 + (y * hei) - self.scroll) * 2))
					y += hei
					opty += 1
					hei = 0

			elif mnu > 0:
				self.scroll = (mnu - 1) * 3
				pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
				y = 0
				for l in dtb.NEWS[res.DATE[0] - 1][opt][0]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (20, (50 + y - self.scroll) * 2))
					y += 15
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.NEWS[res.DATE[0] - 1][opt][1], True, (0, 0, 0)), (20, (55 + y - self.scroll) * 2))
				for l in dtb.NEWS[res.DATE[0] - 1][opt][2]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (20, (100 + y - self.scroll) * 2))
					y += 15
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (219, 49, 37), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[3], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Radio:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.noi = pygame.mixer.Channel(1)
		self.noi.set_volume(res.SFX)
		self.optrects = []
		self.hpctrl = 'PHONE_RADIO'
		self.onoff = False
		self.load = ''
		self.msc = 0
		self.fm = 0
		self.vm = 0
		self.song = res.SONGS_PATH + str(math.floor(self.fm/20)) + '/' + res.RADIO[str(math.floor(self.fm/20))][self.msc]
		
	def inside_events(self,pressed):
		if res.SIGNAL > 0:
			if pressed[4][0]:
				self.onoff = not self.onoff
				if self.onoff == False:
					self.sfx.play(res.SOUND['MENU_BACK'])
					self.noi.stop()
					pygame.mixer.music.stop()
				else:
					self.sfx.play(res.SOUND['MENU_GO'])
					self.noi.play(res.SOUND['NOISE'],-1)
					self.song = res.SONGS_PATH + str(math.floor(self.fm/20)) + '/' + res.RADIO[str(math.floor(self.fm/20))][self.msc]
					pygame.mixer.music.load(self.song)
					pygame.mixer.music.play()
			if pressed[7][0]:
				self.noi.stop()
						
	def outside_events(self,pressed):
		if pressed[2][0]: self.fm -= 1; self.vm -= 0.05
		if pressed[3][0]: self.fm += 1; self.vm += 0.05

		if self.fm < 0: self.fm = 180
		if self.fm > 180: self.fm = 0
		if self.vm < 0.0: self.vm = 1.0
		if self.vm > 1.0: self.vm = 0.0

		pygame.mixer.music.set_volume(self.vm)
		self.noi.set_volume(1 - self.vm)
		if self.vm == 0.0 and self.onoff == True:
			if res.RADIO[str(math.floor(self.fm/20))] != []:
				self.song = res.SONGS_PATH + str(math.floor(self.fm/20)) + '/' + res.RADIO[str(math.floor(self.fm/20))][self.msc]
				pygame.mixer.music.load(self.song)
				pygame.mixer.music.play()

	def draw(self):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))
		if res.RADIO[str(math.floor(self.fm/20))] != []:
			pygame.draw.rect(self.scr[0], (255, 0, 135), pygame.Rect(0,66,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(res.RADIO[str(math.floor(self.fm/20))][self.msc][:-4], True, (0, 0, 0)), (20, 152))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[20], True, (255, 255, 255)), (140, 280))

		pygame.draw.rect(self.scr[0], (10, 10, 10), pygame.Rect(0,40,sz,26))
		f = 0
		sp = math.floor(sz/9)
		for i in range(9):
			pygame.draw.line(self.scr[0], (255, 255, 255), (0 + f,50),(0 + f,65),1)
			pygame.draw.line(self.scr[0], (255, 255, 255), (round(sp/2) + f,55),(round(sp/2) + f,65),1)
			f += sp
		pygame.draw.rect(self.scr[0], (255, 0, 0), pygame.Rect(0 + self.fm,50,4,16))
		self.scr[1].blit(self.fnt['CALIBRI'].render(str(self.fm/10), True, (255, 255, 255)), (140, 40))

		pygame.draw.rect(self.scr[1], (255, 0, 135), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[4], True, (0, 0, 0)), (10, 10))

		return self.scr

class Camera:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = 0
		self.hpctrl = 'PHONE_CAMERA'
		res.recent_data(0)
	
	def inside_events(self,pressed):
		if res.SIGNAL > 0:
			if pressed[0][0]: self.opt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt += 1; self.sfx.play(res.SOUND['MENU_VER'])

			if self.opt < 0: self.opt = 2
			if self.opt > 2: self.opt = 0

			if pressed[4][0] and res.SIGNAL > 0:
				self.sfx.play(res.SOUND['FILE_SAVE'])
				res.ID = self.opt
				res.CHAPTER = 13
				self.ingame = 6
				#SAVE FILE
				if self.opt < len(res.FILES[0]):
					res.save_data()
					res.recent_data(1,self.opt)
				#NEW FILE
				else:
					res.recent_data(3,self.opt)
					res.new_data(True)
					res.save_data()
				res.recent_data(0)
	
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))

		if res.SIGNAL > 0:
			y = 0
			for i in range(len(res.FILES[0])):
				if self.opt != y: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + (y * 51),sz,50))
				else: pygame.draw.rect(self.scr[0], (255, 255, 10), pygame.Rect(0,41 + (y * 51),sz,50))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.CHAPTERS[res.FILES[1][i]][0], True, (0, 0, 0)), (20, (51 + (y * 51)) * 2))
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
				self.scr[1].blit(self.fnt['CALIBRI'].render(hh + ' : ' + mm + ' : ' + ss, True, (0, 0, 0)), (20, (65 + (y * 51)) * 2))
				x = 0
				for p in res.FILES[4][i][::-1]:
					self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (sz - 30 - x, 65 + (y * 51)))
					x += 22
				y += 1

			if self.opt != y: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + (y * 51),sz,50))
			else: pygame.draw.rect(self.scr[0], (255, 255, 10), pygame.Rect(0,41 + (y * 51),sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[61], True, (0, 0, 0)), (20, (61 + (y * 51)) * 2))

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[5], True, (0, 0, 0)), (10, 10))

		return self.scr

class Bestiary:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed):
		if res.SIGNAL > 0:
			if pressed[0][0]: self.lopt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.lopt += 1; self.sfx.play(res.SOUND['MENU_VER'])

			if pressed[4][0]:
				if self.mnu == 0: self.mnu = 1; self.sfx.play(res.SOUND['MENU_GO'])
				elif self.mnu > 0: self.mnu = 0; self.sfx.play(res.SOUND['MENU_BACK'])

			slst = 0
			for i in res.BESTIARY:
				if i['SEEN'] > 0: slst += 1

			if self.mnu == 0:
				if self.lopt < 0: self.lopt = slst
				if self.lopt > slst: self.lopt = 0

			if self.mnu > 0:
				if pressed[2][0]: self.mnu = 1; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: self.mnu = 2; self.sfx.play(res.SOUND['MENU_HOR'])

				if self.lopt < 0: self.lopt = 3
				if self.lopt > 3: self.lopt = 0
	
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0:
			frks = False
			for i in res.BESTIARY:
				if i['SEEN'] > 1: frks = True; break
			if frks == True:
				#FREAKS LIST
				if mnu == 0:
					y = 0
					for i in res.BESTIARY:
						if i['SEEN'] > 1:
							if lopt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
							else: pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(0,41 + y - self.scroll,sz,50))
							self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.FREAKS[i['N']]['NAME'], True, (0, 0, 0)), (20, (51 + y - self.scroll) * 2))
							self.scr[1].blit(self.fnt['CALIBRI'].render(i['ID'], True, (0, 0, 0)), (20, (71 + y - self.scroll) * 2))
							y += 51
				#FREAK INFORMATION
				if mnu == 1:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
					pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(5,243,83,3))
					self.scr[0].blit(pygame.image.load('Sprites/Freaks/frk_' + res.BESTIARY[opt]['N'] + '_stand.png'), (40, 70))
					self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.FREAKS[res.BESTIARY[opt]['N']]['NAME'], True, (0, 0, 0)), (210, 120))
					self.scr[1].blit(self.fnt['CALIBRI'].render('ID: ' + res.BESTIARY[opt]['ID'], True, (0, 0, 0)), (210, 160))
					self.scr[1].blit(self.fnt['CALIBRI'].render('RG: ' + res.BESTIARY[opt]['DATE'], True, (0, 0, 0)), (210, 200))
					self.scr[1].blit(self.fnt['CALIBRI'].render('HG: ' + dtb.FREAKS[res.BESTIARY[opt]['N']]['HEIGHT'], True, (0, 0, 0)), (210, 240))
					self.scr[1].blit(self.fnt['CALIBRI'].render('TP: ' + dtb.FTYPES[dtb.FREAKS[res.BESTIARY[opt]['N']]['TYPE']], True, (0, 0, 0)), (210, 280))
					self.scr[1].blit(self.fnt['CALIBRI'].render('HT: ' + dtb.FHABITATS[dtb.FREAKS[res.BESTIARY[opt]['N']]['HABITAT']], True, (0, 0, 0)), (210, 320))
					#DESCRIPTION
					j = 0
					for l in dtb.FREAKS[res.BESTIARY[opt]['N']]['INFO']:
						self.scr[1].blit(self.fnt['DESCRIPTION'].render(l, True, (0, 0, 0)), (40, 360 + j))
						j += 30
				#FREAK HABILITIES INFORMATION
				if mnu == 2:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
					pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(92,243,83,3))
					pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(10,50,160,77))

					y = 0
					for i in dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES']:
						if lopt != y/19: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(11,51 + y,158,18))
						else: pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(11,51 + y,158,18))
						self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (40, (53 + y) * 2))
						y += 19

					j = 0
					for l in dtb.FREAKS[res.BESTIARY[opt]['N']]['HABILITIES'][lopt][1]:
						self.scr[1].blit(self.fnt['DESCRIPTION'].render(l, True, (0, 0, 0)), (40, 360 + j))
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

					self.scr[1].blit(self.fnt['CALIBRI'].render(dmg, True, (0, 0, 0)), (20, 210))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[21], True, (255, 255, 255)), (40, 140))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (134, 0, 211), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[6], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Tasks:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed):
		if pressed[0][0]: self.opt[1] -= 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[2][0]: self.opt[0] -= 1; self.sfx.play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt[0] += 1; self.sfx.play(res.SOUND['MENU_HOR'])

		if self.opt[0] < 0: self.opt[0] = 2
		if self.opt[0] > 2: self.opt[0] = 0
		if self.opt[1] < 0: self.opt[1] = len(res.TASKS) - 1
		if self.opt[1] > len(res.TASKS) - 1: self.opt[1] = 0
					
	def outside_events(self,pressed):
		pass

	def draw(self):
		sz = self.scr[0].get_width() #button width
		self.t_unmark = []
		self.t_mark = []
		for i in res.TASKS:
			if i[1] == 1:
				self.t_mark.append(i)
			if i[1] == 0:
				self.t_unmark.append(i)

		if self.opt[0] == 0: em = self.t_unmark
		if self.opt[0] == 1: em = self.t_mark
		if self.opt[0] == 2: em = res.TASKS

		if self.opt[1] > 2:
			if self.scroll < (self.opt[1] - 2) * 31:
				self.scroll += 6.2
		elif self.opt[1] > 0 and self.opt[1] < len(em) - 1:
			if self.scroll > (self.opt[1] - 1) * 31:
				self.scroll -= 6.2
		elif self.opt[1] == 0 and self.scroll > 0:
			self.scroll -= 6.2
			
		for i in self.scr: i.fill((10,10,10,0))
		y = 0
		for i in em:
			if self.opt[1] != y/31: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.sz,30))
			else: pygame.draw.rect(self.scr[0], (255, 123, 0), pygame.Rect(0,66 + y - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, 146 + y - self.scroll))
			y += 31
		if y == 0:
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[22], True, (255, 255, 255)), (80, 280))

		dvd3 = math.floor(sz/3)
		if self.opt[0] == 0:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[29], True, (0, 0, 0)), (24, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[29], True, (255, 255, 255)), (24, 94))
		if self.opt[0] == 1:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[30], True, (0, 0, 0)), ((dvd3 * 2) + 30, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[30], True, (255, 255, 255)), ((dvd3 * 2) + 30, 94))
		if self.opt[0] == 2:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[28], True, (0, 0, 0)), ((dvd3 * 4) + 24, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[28], True, (255, 255, 255)), ((dvd3 * 4) + 24, 94))

		pygame.draw.rect(self.scr[1], (255, 123, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[7], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Stats:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = 0
	
	def inside_events(self,pressed):
		if pressed[2][0]: self.opt -= 1; self.sfx.play(res.SOUND['MENU_HOR'])
		if pressed[3][0]: self.opt += 1; self.sfx.play(res.SOUND['MENU_HOR'])

		if self.opt < 0: self.opt = len(res.PARTY[res.FORMATION]) - 1
		if self.opt > len(res.PARTY[res.FORMATION]) - 1: self.opt = 0
					
	def outside_events(self,pressed):
		pass

	def draw(self):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if self.opt > 2: self.scroll += (self.opt - 2) * 60

		for i in self.scr: i.fill((10,10,10,0))

		x = 0
		dvd3 = math.floor(sz/3)
		for i in res.PARTY[res.FORMATION]:
			if self.opt == x/dvd3:
				pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0 + x - self.scroll,45,dvd3,20))
				self.scr[1].blit(self.fnt['CALIBRI'].render(res.CHARACTERS[i]['NAME'], True, (0, 0, 0)), ((16 + x - self.scroll) * 2, 95))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(res.CHARACTERS[i]['NAME'], True, (255, 255, 255)), ((16 + x - self.scroll) * 2, 95))
			x += dvd3

		ch = res.CHARACTERS[res.PARTY[res.FORMATION][self.opt]]
		self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(res.PARTY[res.FORMATION][self.opt]) + '.png'), (10, 74))
		self.scr[1].blit(self.fnt['CALIBRI'].render(ch['NAME'] + ' ' + res.CHARACTERS[res.PARTY[res.FORMATION][self.opt]]['LASTNAME'], True, (255, 255, 255)), (70, 152))
		self.scr[1].blit(self.fnt['CALIBRI'].render(str(ch['ID']), True, (255, 255, 255)), (20, 192))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.PRONOUNS[ch['PRONOUN']], True, (255, 255, 255)), (140, 192))
		self.scr[1].blit(self.fnt['CALIBRI'].render(ch['BLOOD'], True, (255, 255, 255)), (100, 192))

		self.scr[1].blit(self.fnt['CALIBRI'].render('level ' + str(ch['LEVEL']), True, (255, 255, 255)), (20, 230))
		self.scr[1].blit(self.fnt['CALIBRI'].render('hp:', True, (255, 255, 255)), (20, 260))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,135,100,10))
		if ch['HP'] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,135,int(100/(dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']]/ch['HP'])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('xp:', True, (255, 255, 255)), (20, 290))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,150,100,10))
		if ch['XP'] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,150,int(100/(dtb.NEXTLEVEL[ch['LEVEL']]/ch['XP'])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('st:', True, (255, 255, 255)), (20, 320))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,165,100,10))
		if dtb.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,165,int(100/(100/dtb.CLASSES[ch['CLASS']]['STRENGHT'][ch['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('at:', True, (255, 255, 255)), (20, 350))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,180,100,10))
		if dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,180,int(100/(100/dtb.CLASSES[ch['CLASS']]['RESISTANCE'][ch['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('ag:', True, (255, 255, 255)), (20, 380))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,195,100,10))
		if dtb.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,195,int(100/(100/dtb.CLASSES[ch['CLASS']]['AGILITY'][ch['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('rs:', True, (255, 255, 255)), (20, 410))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,210,100,10))
		if dtb.CLASSES[ch['CLASS']]['KNOWLEDGE'][ch['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,210,int(100/(100/dtb.CLASSES[ch['CLASS']]['KNOWLEDGE'][ch['LEVEL']])),10))

		pygame.draw.rect(self.scr[1], (255, 0, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[8], True, (0, 0, 0)), (10, 10))

		return self.scr

class Tactics:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed):
		#CHOOSING TACTICS
		if self.mnu == 0:
			if pressed[4][0]:
				self.sfx.play(res.SOUND['MENU_GO'])
				if self.opt[1] == len(res.TACTICAL):
					res.TACTICAL.append([0,0,0,0])
				self.mnu = 1
				self.opt[0] = res.TACTICAL[self.opt[1]][self.mnu - 1]

			if pressed[0][0]: self.opt[1] -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt[1] += 1; self.sfx.play(res.SOUND['MENU_VER'])

			if self.opt[1] < 0: self.opt[1] = len(res.TACTICAL)
			if self.opt[1] > len(res.TACTICAL): self.opt[1] = 0
		#MANAGING TACTICS
		elif self.mnu > 0:
			if pressed[4][0]:
				self.sfx.play(res.SOUND['MENU_BACK'])
				if self.mnu < 5:
					self.mnu = 0
				else:
					del res.TACTICAL[self.opt[1]]
					self.mnu = 0

			if pressed[0][0]: self.opt[0] -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt[0] += 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[2][0]: self.mnu -= 1; self.sfx.play(res.SOUND['MENU_HOR'])
			if pressed[3][0]: self.mnu += 1; self.sfx.play(res.SOUND['MENU_HOR'])

			if self.mnu > 0:
				if self.mnu < 1: self.mnu = 5
				if self.mnu > 5: self.mnu = 1
				if self.opt[0] < 0: self.opt[0] = 7
				if self.opt[0] > 7: self.opt[0] = 0
				
				if pressed[2][0] or pressed[3][0]:
					if self.mnu < 5 and len(res.TACTICAL) > 0: self.opt = res.TACTICAL[self.opt[1]][self.mnu - 1]
				else:
					if self.mnu < 5 and len(res.TACTICAL) > 0: res.TACTICAL[self.opt[1]][self.mnu - 1] = self.opt[0]
								
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if opt[1] > 2: self.scroll += (opt[1] - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0:
			y = 0
			for i in res.TACTICAL:
				if i != [] and len(i) == 4:
					if opt[1] != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
					else: pygame.draw.rect(self.scr[0], (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,sz,50))

					if self.mnu > 0 and opt[1] == y/51:
						if self.mnu < 5:
							pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(8 + (mnu - 1) * 22,49 + y - self.scroll,24,24))
							if i[self.mnu - 1] == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[54], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 2: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[55], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 3: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[56], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 4: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[57], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 5: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[58], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 6: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[59], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[self.mnu - 1] == 7: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[60], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
						else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 42,49 + y - self.scroll,24,24))
						self.scr[0].blit(pygame.image.load('Sprites/tc_8.png'), (sz - 40, 51 + y - self.scroll))
					for b in range(4):
						self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[b]) + '.png'), (10 + (22 * b), 51 + y - self.scroll))
				y += 51

			if self.opt[1] != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[36], True, (0, 0, 0)), (100, (60 + y - self.scroll) * 2))

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (33, 75, 127), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[9], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Achievements:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = 0
		
	def inside_events(self,pressed):
		if pressed[0][0]: self.opt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt += 1; self.sfx.play(res.SOUND['MENU_VER'])

		if self.opt < 0: self.opt = len(dtb.ACHIEVEMENTS) - 1
		if self.opt > len(dtb.ACHIEVEMENTS) - 1: self.opt = 0
					
	def outside_events(self,pressed):
		pass

	def draw(self):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if self.opt > 2: self.scroll += (self.opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0:
			y = 0
			for i in dtb.ACHIEVEMENTS:
				if self.opt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
				else: pygame.draw.rect(self.scr[0], (255, 191, 0), pygame.Rect(0,41 + y - self.scroll,sz,50))

				if i[2] == True: tcol = (0,0,0)
				else: tcol = (80,80,80)
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, tcol), (20, (51 + y - self.scroll) * 2))
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, tcol), (20, (65 + y - self.scroll) * 2))
				y += 51

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (255, 191, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[10], True, (0, 0, 0)), (10, 10))

		return self.scr

class Ranking:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scroll = 0
		
	def inside_events(self,pressed):
		pass
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if res.SIGNAL > 0: pass
		else: self.scr[1].blit(self.fnt.render(dtb.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr[1], (55, 255, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[11], True, (0, 0, 0)), (10, 10))
		pygame.draw.rect(self.scr[0], (10, 10, 10), pygame.Rect(0,40,sz,210))

		return self.scr

class Help:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = 0
		self.mnu = 0
		
	def inside_events(self,pressed):
		if self.mnu == 0:
			if pressed[0][0]: self.opt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt += 1; self.sfx.play(res.SOUND['MENU_VER'])

		if pressed[4][0]:
			if self.mnu == 0: self.mnu = 1; self.sfx.play(res.SOUND['MENU_GO'])
			elif self.mnu > 0: self.mnu = 0; self.sfx.play(res.SOUND['MENU_BACK'])

		if self.opt < 0: self.lopt = len(dtb.MANUAL) - 1
		if self.opt > len(dtb.MANUAL) - 1: self.opt = 0
					
	def outside_events(self,pressed):
		if self.mnu > 0:
			if pressed[0][0]: self.mnu -=1
			if pressed[1][0]: self.mnu +=1
					
			if self.mnu < 1: self.mnu = 1
			if self.mnu > 1000: self.mnu = 1000
	
	def draw(self):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[0].get_width() #button width
		if self.mnu == 0:
			self.scroll = 0
			if self.opt > 2: self.scroll += (self.opt - 2) * 31
			y = 0
			for i in dtb.MANUAL:
				if self.opt != y/31: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr[0], (137, 50, 0), pygame.Rect(0,41 + y - self.scroll,sz,30))
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, (51 + y - self.scroll) * 2))
				y += 31

		if self.mnu > 0:
			self.scroll = (self.mnu - 1) * 3
			pygame.draw.rect(self.scr[0],(255, 255, 255), pygame.Rect(5,45,222,200))
			self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MANUAL[self.opt][0], True, (0, 0, 0)), (140, 110 - self.scroll))
			y = 0
			for l in dtb.MANUAL[self.opt][1]:
				self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (30, 160 + y - self.scroll))
				y += 30

		pygame.draw.rect(self.scr[1], (137, 50, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[12], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class Settings:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed):
		if pressed[0][0]: self.lopt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.lopt += 1; self.sfx.play(res.SOUND['MENU_VER'])

		if self.mnu == 0:
			if self.lopt < 0: self.lopt = 3
			if self.lopt > 3: self.lopt = 0
		if self.mnu == 1:
			if self.lopt < 0: self.lopt = 7
			if self.lopt > 7: self.lopt = 0
		if self.mnu == 2:
			if self.lopt < 0: self.lopt = 1
			if self.lopt > 1: self.lopt = 0
		if self.mnu == 3:
			if self.lopt < 0: self.lopt = 7
			if self.lopt > 7: self.lopt = 0
		#MAIN SETTINGS
		if self.mnu == 0:
			if pressed[4][0]:
				if self.lopt == 3:
					self.phn = GUI.Phone()
					self.inv = GUI.Inventory(False)
					self.shpmnu = GUI.Shop()
					res.save_sett()
					self.sfx.play(res.SOUND['MENU_GO'])
					self.opt = 1
					self.lopt = 4
					self.phone = 1
					if res.CHAPTER == 0 and res.SCENE == 0:
						self.ch_ton.play(res.SOUND['CALLING'],-1)
						self.ch_rng.play(res.SOUND['RINGTONE_' + str(self.phn.pbg)],-1)
						self.phone = 17
						self.nb = '977904623'
				else:
					self.mnu = self.lopt + 1
					self.opt = 0
					self.lopt = 0
		#GAMEPLAY SETTINGS
		elif self.mnu == 1:
			if self.lopt == 0:
				if pressed[2][0]:
					res.LANG = 'EN'; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]:
					res.LANG = 'PT'; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.lopt == 1:
				if pressed[2][0]: res.SPEED += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SPEED -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

				if res.SPEED < 1: res.SPEED = 5
				if res.SPEED > 5: res.SPEED = 1
			if self.lopt == 5:
				if pressed[2][0]: res.BORDER -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.BORDER += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

				if res.BORDER < 0: res.BORDER = res.RANGE_BORDER
				if res.BORDER > res.RANGE_BORDER: res.BORDER = 0
			if self.lopt == 6:
				if pressed[2][0]: res.CENSORSHIP = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CENSORSHIP = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.lopt == 7:
				if pressed[2][0]: res.HINT = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HINT = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.lopt == 8:
				if pressed[2][0]: res.HELP = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HELP = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
		#CONTROLS MENU
		elif self.mnu == 3:
			if pressed[4][0]:
				self.mnu = self.lopt + 4
				self.opt = 0
				self.lopt = 0
		#MOUSE SETTINGS
		elif self.mnu == 4:
			if self.lopt == 1:
				if pressed[2][0]: res.CURSOR -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CURSOR += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

				if res.CURSOR < 0: res.CURSOR = res.RANGE_CURSOR
				if res.CURSOR > res.RANGE_CURSOR: res.CURSOR = 0
			if pressed[4][0]:
				self.mnu = self.lopt + 4
				self.opt = 0
				self.lopt = 0
		#1P SETTINGS
		elif self.mnu == 5:
			#UP KEY
			if self.lopt == 0:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.PHONE[0],res.BAG[0],res.RUN[0]):
							dtb.UP = event.key; self.opt = 0
			#DOWN KEY
			if self.lopt == 1:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.UP[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.PHONE[0],res.BAG[0],res.RUN[0]):
							dtb.DOWN = event.key; self.opt = 0
			#LEFT KEY
			if self.lopt == 2:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.UP[0],res.RIGHT[0],res.ACT[0],res.PHONE[0],res.BAG[0],res.RUN[0]):
							dtb.LEFT = event.key; self.opt = 0
			#RIGHT KEY
			if self.lopt == 3:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.UP[0],res.ACT[0],res.PHONE[0],res.BAG[0],res.RUN[0]):
							dtb.RIGHT = event.key; self.opt = 0
			#ACT KEY
			if self.lopt == 4:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.UP[0],res.PHONE[0],res.BAG[0],res.RUN[0]):
							dtb.ACT = event.key; self.opt = 0
			#RUN KEY
			if self.lopt == 5:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.UP[0],res.PHONE[0],res.BAG[0],res.ACT[0]):
							dtb.RUN = event.key; self.opt = 0
			#PHONE KEY
			if self.lopt == 6:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.UP[0],res.BAG[0],res.RUN[0]):
							dtb.PHONE = event.key; self.opt = 0
			#INVENTORY KEY
			if self.lopt == 7:
				if pressed[4][0]:
					if self.opt == 0: self.opt = 1
				else:
					if self.opt == 1:
						if event.key not in (res.DOWN[0],res.LEFT[0],res.RIGHT[0],res.ACT[0],res.PHONE[0],res.UP[0],res.RUN[0]):
							dtb.BAG = event.key; self.opt = 0
		#GO BACK
		if pressed[5][0]:
			if self.mnu > 0:
				self.sfx.play(res.SOUND['MENU_BACK'])
				self.mnu = 0
							
	def outside_events(self,pressed):
		#COLORS SETTINGS
		if self.mnu == 1:
			if self.lopt == 2:
				if pressed[2][0]: res.COLOR[0] -= 5; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[0] += 5; self.sfx.play(res.SOUND['MENU_HOR'])

				if res.COLOR[0] < 30: res.COLOR[0] = 242
				if res.COLOR[0] > 242: res.COLOR[0] = 30
			if self.lopt == 3:
				if pressed[2][0]: res.COLOR[1] -= 5; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[1] += 5; self.sfx.play(res.SOUND['MENU_HOR'])

				if res.COLOR[1] < 30: res.COLOR[1] = 242
				if res.COLOR[1] > 242: res.COLOR[1] = 30
			if self.lopt == 4:
				if pressed[2][0]: res.COLOR[2] -= 5; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.COLOR[2] += 5; self.sfx.play(res.SOUND['MENU_HOR'])

				if res.COLOR[2] < 30: res.COLOR[2] = 242
				if res.COLOR[2] > 242: res.COLOR[2] = 30
		#AUDIO SETTINGS
		if self.mnu == 2:
			if self.lopt == 0:
				if pressed[2][0]: res.SFX -= 0.1; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SFX += 0.1;  self.sfx.play(res.SOUND['MENU_HOR'])

				self.sfx.set_volume(res.SFX)
				self.ch_ton.set_volume(res.SFX)
				self.ch_stp.set_volume(res.SFX)
				self.ch_dlg.set_volume(res.SFX)

				if res.SFX < 0.0: res.SFX = 0.0
				if res.SFX > 1.0: res.SFX = 1.0
			if self.lopt == 1:
				if pressed[2][0]: res.MSC -= 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.MSC += 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])

				self.ch_msc.set_volume(res.MSC)
				self.ch_rad.set_volume(res.MSC)
				self.ch_rng.set_volume(res.MSC)

				if res.MSC < 0.0: res.MSC = 0.0
				if res.MSC > 1.0: res.MSC = 1.0

	def draw(self, opt, mnu, trg):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[0].get_width() #button width
		hz = 30 #button height
		sp = 1 #scroll speed
		bw = 110 #bar width
		bh = 10 #bar height
		bs = 60 #bar x
		y = 41
		ty = 10

		#SETTINGS MENU
		if mnu == 0:
			self.scroll = 0
			inpts = (88,89,90,76)
			for i in range(4):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp
		#GAMEPLAY MENU
		if mnu == 1:
			inpts = (62,72,73,74,75,87,96,97,98)
			if opt == 0:
				if self.scroll > 0:
					self.scroll -= 10
			elif opt == 5:
				if self.scroll < 60:
					self.scroll += 10
			elif opt == 6:
				if self.scroll < 60:
					self.scroll += 10
			elif opt == 2:
				if self.scroll > 0:
					self.scroll -= 10
			elif opt == 8:
				if self.scroll < 60:
					self.scroll += 10
			for i in range(9):
				#RECT AND SELECT
				if opt == i:
					if i >= 2 and i < 6:
						pygame.draw.rect(self.scr[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(0,y - self.scroll,sz,hz))
					else:
						pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				#SCROLL BAR
				if i >= 2 and i < 5:
					pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
					pygame.draw.rect(self.scr[0], (110,110,110), pygame.Rect(bs + int(bw/(242/res.COLOR[i - 2])) - 10,y + bh - self.scroll,10,10))
				#BORDER OPTIONS
				if i == 5:
					for b in range(math.floor(sz/10) - 4):
						for c in range(3): self.scr[0].blit(pygame.image.load('Sprites/border_' + str(res.BORDER) + '.png'), (60 + b * 10, 196 + (c * 10) - self.scroll))
				#SWITCH
				if i == 6:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if res.CENSORSHIP == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y + 10 - self.scroll,40,10))
					if res.CENSORSHIP == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y + 10 - self.scroll,40,10))
				if i == 7:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if res.HINT == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y - self.scroll,40,10))
					if res.HINT == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y - self.scroll,40,10))
				if i == 8:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if res.HELP == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y - self.scroll,40,10))
					if res.HELP == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y - self.scroll,40,10))
				#TEXT
				if i == 0:
					txt = res.LANG
				elif i == 1:	
					if res.SPEED == 5: txt = dtb.MENU[91]
					if res.SPEED == 4: txt = dtb.MENU[92]
					if res.SPEED == 3: txt = dtb.MENU[93]
					if res.SPEED == 2: txt = dtb.MENU[94]
					if res.SPEED == 1: txt = dtb.MENU[95]
				else: txt = ''
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]] + ': ' + txt, True, (0,0,0)), (10, (y + ty - 2 - self.scroll) * 2))
				y += hz + sp
		#AUDIO MENU
		if mnu == 2:
			self.scroll = 0
			inpts = (res.SFX,res.MSC)
			for i in range(2):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
				pygame.draw.rect(self.scr[0], (110, 110, 110), pygame.Rect(bs + (inpts[i] * (bw - 10)),y + ty - self.scroll,20,bh))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[63 + i], True, (0,0,0)), (10, (y + ty - 2 - self.scroll)* 2))
				y += hz + sp
		#CONTROLS MENU
		if mnu == 3:
			self.scroll = 0
			inpts = (99,100,101,102)
			for i in range(4):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp
		#MOUSE MENU
		if mnu == 4:
			self.scroll = 0
			inpts = (103,104,105)
			for i in range(3):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				#CURSOR OPTIONS
				if i == 1: self.scr[0].blit(pygame.image.load('Sprites/cursor_' + str(res.CURSOR) + '.png'), (100, 5 + y - self.scroll))
				y += hz + sp
		#1P CONTROLS
		if mnu == 5:
			if opt == 0:
				if self.scroll > 0:
					self.scroll -= 10
			elif opt == 5:
				if self.scroll < 60:
					self.scroll += 10
			elif opt == 2:
				if self.scroll > 0:
					self.scroll -= 10
			elif opt == 7:
				if self.scroll < 60:
					self.scroll += 10

			ctrls = (res.UP,res.DOWN,res.LEFT,res.RIGHT,res.ACT,res.RUN,res.PHONE,res.BAG)
			for i in range(7):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				if trg == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				elif opt == i: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[77], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp

		pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[13], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class About:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.optrects = []
		self.opt = 0
		
	def inside_events(self,pressed):
		if pressed[0][0] and self.opt == 1: self.opt = 0; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[1][0] and self.opt == 0: self.opt = 1; self.sfx.play(res.SOUND['MENU_VER'])

		if pressed[4][0]:
			self.sfx.play(res.SOUND['MENU_GO'])
			if self.opt == 0:
				webbrowser.get('windows-default').open('twitter.com/kaixtr')
			if self.opt == 1:
				webbrowser.get('windows-default').open('github.com/kaixtr')
							
	def outside_events(self,pressed):
		pass

	def draw(self):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[0].get_width() #button width
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,195))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[0], True, (0, 0, 0)), (80, 110))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[1], True, (0, 0, 0)), (30, 160))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[2], True, (0, 0, 0)), (30, 190))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[3], True, (0, 0, 0)), (30, 220))

		if self.opt == 0: pygame.draw.rect(self.scr[0], (193, 193, 193), pygame.Rect(5,139,sz - 10,20))
		else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,139,sz - 10,20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[4], True, (0, 0, 0)), (20, 286))
		if self.opt == 1: pygame.draw.rect(self.scr[0], (193, 193, 193), pygame.Rect(5,160,sz - 10,20))
		else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,160,sz - 10,20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[5], True, (0, 0, 0)), (20, 328))

		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.ABOUT[6], True, (0, 0, 0)), (40, 400))

		pygame.draw.rect(self.scr[1], (193, 193, 193), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[14], True, (0, 0, 0)), (10, 10))

		return self.scr

class Call:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.optrects = []
		self.opt = 0
		self.credit = 0
		self.inv = Inventory(False)
		self.battery = self.inv.find(res.PARTY[res.FORMATION][0],'phone')
		if self.battery != None:
			if self.battery[2] == 'sim_card': self.credit = int(self.battery[3])
			elif self.battery[4] == 'sim_card': self.credit = int(self.battery[5])
			self.battery = int(self.battery[1])
		else: self.battery = 0
		
	def inside_events(self,pressed):
		if pressed[2][0] and self.opt == 1: self.opt = 0; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[3][0] and self.opt == 0: self.opt = 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[4][0]:
			self.ch_ton.stop()
			self.ch_rng.stop()
			if self.opt == 0:
				self.ingame = 4
			elif self.opt == 1:
				self.sfx.play(res.SOUND['MENU_BACK'])
				self.phone = 1
			if self.radonoff == True: pygame.mixer.music.unpause()
			if res.CHAPTER == 0 and res.SCENE == 0:
				self.ingame = 5
	
	def outside_events(self,pressed):
		pass
	
	def draw(self, nb):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[1].get_width() #button width
		num = 0
		for i in dtb.NUMBERS:
			if i[1] == nb: break
			num += 1
		self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'call_' + nb + '.png'), (0, 90))
		pygame.draw.rect(self.scr[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(0,0,sz,90))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.NUMBERS[num][0], True, (255, 255, 255)), (100, 20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(nb, True, (255, 255, 255)), (100, 40))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[32] + str(self.credit), True, (255, 255, 255)), (100, 80))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[33], True, (255, 255, 255)), (100, 120))

		if self.opt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_ys.png'), (40, 40)), (25, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_ys.png'), (30, 190))
		if self.opt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_no.png'), (40, 40)), (sz - 55, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_no.png'), (sz - 50, 190))

		return self.scr

class Photo:
	def __init__(self,bg,foes,xpos):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40), 'DATETIME': pygame.font.Font(res.FONTS_PATH + 'Sicret_PERSONAL-Regular.ttf', 32)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.bg = bg
		self.foes = foes
		self.xpos = xpos
		self.hpctrl = 'PHONE_PHOTO'
		
	def inside_events(self,pressed):
		if pressed[4][0]:
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
				self.sfx.play(res.SOUND['CAMERA'])
				self.ingame = 7
				self.mnu = 1
							
	def outside_events(self,pressed):
		pass
	
	def draw(self):
		sz = self.scr[0].get_width() #button width
		self.scroll = 0
		for i in self.scr: i.fill((0,0,0,0))

		self.scr[0].blit(self.bg, (-self.xpos, -88))
		for i in self.foes:
			self.scr[0].blit(i['SPRITE'], (-self.xpos + i['MASK'].x, -88 + i['MASK'].y))

		return self.scr
