# -*- coding: utf-8 -*-
import random
import pygame
import math
import sys
import resources
import os

if resources.FILES[3] != []:
	if resources.FILES[3][0] == 'PT': import database_PT as database
	if resources.FILES[3][0] == 'EN': import database_EN as database
else: import database_PT as database

class Debug:
	def __init__(self):
		self.scr = pygame.Surface((1200,50))
		self.fnt = pygame.font.Font('Fonts/monotype.ttf', 15)
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
				self.dlg = database.DIALOGS[self.cmd[10:].upper()][int(self.cmd[7:9])]
			elif self.cmd.startswith('dialogs'):
				database.load_dialogs()
			elif self.cmd.startswith('battle'):
				if len(self.cmd) > 7: self.dlg = [[13,self.cmd[7:]]]
				else: self.dlg = [[13,'madladcat']]
			elif self.cmd.startswith('item'):
				if len(self.cmd) > 5:
					database.ITEMS[self.cmd[5:]]
					self.dlg = [[1,self.cmd[5:],0,0]]
			elif self.cmd.startswith('level'):
				for i in resources.PARTY[resources.FORMATION]: resources.CHARACTERS[i]['LEVEL'] = int(self.cmd[6:])
			elif self.cmd.startswith('hp'):
				resources.CHARACTERS[int(self.cmd[3])]['HP'] = int(self.cmd[5])
			elif self.cmd.startswith('hair'):
				resources.CHARACTERS[int(self.cmd[5])]['HAIR'] = self.cmd[7:]
			elif self.cmd.startswith('costume'):
				resources.CHARACTERS[int(self.cmd[8])]['COSTUME'] = self.cmd[10:]
			elif self.cmd.startswith('map'):
				resources.MAP = int(self.cmd[4:])
			elif self.cmd.startswith('chapter'):
				resources.CHAPTER = int(self.cmd[8:])
			elif self.cmd.startswith('money'):
				src = None
				for i in resources.PARTY[resources.FORMATION]:
					src = self.inv.find(i,'credit_card')
					if src == None:
						src = self.inv.find(i,'wallet')
						if src != None:
							src[1] = int(self.cmd[6:])
							break
					else:
						src[1] = int(self.cmd[6:])
						break
			elif self.cmd.startswith('atm'):
				resources.ATM = int(self.cmd[4:])
			elif self.cmd.startswith('credit'):
				resources.CREDIT = int(self.cmd[7:])
			elif self.cmd.startswith('battery'):
				resources.BATTERY = int(self.cmd[8:])
			elif self.cmd.startswith('time'):
				resources.TIME = [int(self.cmd[5:7]),int(self.cmd[7:9]),int(self.cmd[9:11])]
			elif self.cmd.startswith('date'):
				resources.DATE = [int(self.cmd[5:7]),int(self.cmd[7:9]),int(self.cmd[9:11]),int(self.cmd[11:13])]
			elif self.cmd.startswith('weather'):
				resources.WEATHER = int(self.cmd[8:])
			elif self.cmd.startswith('party'):
				resources.PARTY[resources.FORMATION] = [int(self.cmd[6]),int(self.cmd[7]),int(self.cmd[8])]
				resources.party_make(0)
			elif self.cmd.startswith('health'):
				resources.CHARACTERS[resources.PARTY[resources.FORMATION][0]]['HEALTH'] = int(self.cmd[7:])
			elif self.cmd == 'rect': self.dlg = 'rectdebug'
			else: self.sfx.play(resources.SOUND['ERROR'])
		except: self.sfx.play(resources.SOUND['ERROR'])
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
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'ALT': pygame.font.Font('Fonts/PrestigeEliteStd.otf', 10)}
		self.ch_sfx = pygame.mixer.Channel(1)
		self.ch_ton = pygame.mixer.Channel(2)
		self.wdw = pygame.Surface((200, 200))
		pygame.draw.rect(self.wdw, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,0,200,200))
		for x in range(20):
			for y in range(20):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))
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
								if len(self.name[self.ind]) > 0: self.lopt = 1; self.ch_ton.play(resources.SOUND['MENU_GO'])
								else: self.ch_sfx.play(resources.SOUND['ERROR'])
							else:
								if len(self.lame[self.ind]) > 0: self.lopt = 0; self.ind += 1; self.ch_ton.play(resources.SOUND['TEXT_ENTER'])
								else: self.ch_sfx.play(resources.SOUND['ERROR'])
						elif event.key == pygame.K_BACKSPACE:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							if self.lopt == 0:
								if len(self.name[self.ind]) > 0: self.name[self.ind] = self.name[self.ind][:-1]
								elif self.ind > 0: self.ind -= 1; self.lopt = 0
							if self.lopt == 1:
								if len(self.lame[self.ind]) > 0: self.lame[self.ind] = self.lame[self.ind][:-1]
								else: self.lopt = 0
						else:
							self.ch_sfx.play(resources.SOUND['TEXT_INPUT'])
							if self.lopt == 0 and len(self.name[self.ind]) < 10: self.name[self.ind] += event.unicode
							if self.lopt == 1 and len(self.lame[self.ind]) < 10: self.lame[self.ind] += event.unicode
				else:
					self.pressed = pygame.key.get_pressed()
					if self.pressed[resources.LEFT[0]]: self.lopt = 0; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT[0]]: self.lopt = 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.ACT[0]]:
						if self.lopt == 0:
							self.ch_sfx.play(resources.SOUND['FILE_NEW'])
							for i in range(len(self.name)):
								resources.CHARACTERS[i]['NAME'] = self.name[i]
								resources.CHARACTERS[i]['LASTNAME'] = self.lame[i]
							resources.save_data()
							resources.save_sett()
							resources.party_make(0)
							self.show = False
						if self.lopt == 1:
							self.ch_sfx.play(resources.SOUND['MENU_BACK'])
							self.ind = 0
							self.lopt = 0

	def run(self):
		for i in self.scr: i.fill((0,0,0))

		self.blink += 0.1
		if math.floor(self.blink) == 0: self.bt = ''
		elif math.floor(self.blink) == 1: self.bt = '.'
		else: self.blink = 0.0

		if self.ninput == False:
			resources.CHARACTERS[0]['NAME'] = database.NAMES[0]
			resources.CHARACTERS[0]['LASTNAME'] = database.NAMES[1]
			resources.CHARACTERS[1]['NAME'] = database.NAMES[2]
			resources.CHARACTERS[1]['LASTNAME'] = database.NAMES[3]
			resources.CHARACTERS[2]['NAME'] = database.NAMES[4]
			resources.CHARACTERS[2]['LASTNAME'] = database.NAMES[5]
			resources.CHARACTERS[3]['NAME'] = database.NAMES[6]
			resources.CHARACTERS[3]['LASTNAME'] = database.NAMES[7]
			resources.CHARACTERS[4]['NAME'] = database.NAMES[8]
			resources.CHARACTERS[4]['LASTNAME'] = database.NAMES[9]
			resources.CHARACTERS[5]['NAME'] = database.NAMES[10]
			resources.CHARACTERS[5]['LASTNAME'] = database.NAMES[11]
			if self.ind < 6:
				if self.lopt == 0:
					if self.tim != 0: self.tim -= 1
					else:
						if len(self.name[self.ind]) != len(resources.CHARACTERS[self.ind]['NAME']):
							self.name[self.ind] += resources.CHARACTERS[self.ind]['NAME'][self.did]
							self.ch_sfx.play(pygame.mixer.Sound('SFX/text_input.wav'))
							self.tim = 3
							self.did += 1
						else: self.ch_ton.play(pygame.mixer.Sound('SFX/menu_go.wav')); self.lopt = 1; self.tim = 3; self.did = 0
				if self.lopt == 1:
					if self.tim != 0: self.tim -= 1
					else:
						if len(self.lame[self.ind]) != len(resources.CHARACTERS[self.ind]['LASTNAME']):
							self.lame[self.ind] += resources.CHARACTERS[self.ind]['LASTNAME'][self.did]
							self.ch_sfx.play(pygame.mixer.Sound('SFX/text_input.wav'))
							self.tim = 3
							self.did += 1
						else: self.ch_ton.play(pygame.mixer.Sound('SFX/text_enter.wav')); self.ind += 1; self.lopt = 0; self.tim = 3; self.did = 0
			else:
				self.ch_sfx.play(pygame.mixer.Sound('SFX/file_new.wav'))
				for i in range(len(self.name)):
					resources.CHARACTERS[i]['NAME'] = self.name[i]
					resources.CHARACTERS[i]['LASTNAME'] = self.lame[i]
				resources.save_data()
				resources.save_sett()
				resources.party_make(0)
				resources.recent_data(1,resources.ID)
				self.show = False
		
		if self.ind < 6:
			l1 = 0
			l2 = 0
			for l in database.MENU[80]:
				if l in ['m','w','M','Q','T','U','V','W','Y','?']: l1 += 8
				elif l in ['f','r']: l1 += 6
				elif l in ['J']: l1 += 5
				elif l in ['l']: l1 += 4
				elif l in ['i','I','!','.',',']: l1 += 2
				else: l1 += 7
			for l in database.MENU[81]:
				if l in ['m','w','M','Q','T','U','V','W','Y','?']: l2 += 8
				elif l in ['f','r']: l2 += 6
				elif l in ['J']: l2 += 5
				elif l in ['l']: l2 += 4
				elif l in ['i','I','!','.',',']: l2 += 2
				else: l2 += 7
			if self.lopt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[80] + ': ' + self.name[self.ind] + self.bt, True, (255, 255, 0)), (120 - l1, 60))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[80] + ': ' + self.name[self.ind], True, (255, 255, 255)), (120 - l1, 60))
			if self.lopt == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[81] + ': '+ self.lame[self.ind] + self.bt, True, (255, 255, 0)), (120 - l2, 100))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[81] + ': '+ self.lame[self.ind], True, (255, 255, 255)), (120 - l2, 100))
		else:
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[82], True, (255, 255, 255)), (100, 20))
			y = 0
			for i in range(len(self.name)):
				self.scr[1].blit(self.fnt['CALIBRI'].render(self.name[i] + ' ' + self.lame[i], True, (255, 255, 255)), (20, (30 + (20 * y)) * 2))
				y += 1

			if self.lopt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[83], True, (255, 255, 0)), (100, 320))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[83], True, (255, 255, 255)), (100, 320))
			if self.lopt == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[84], True, (255, 255, 0)), (200, 320))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[84], True, (255, 255, 255)), (200, 320))

		self.wdw.blit(self.scr[0],(10,10))
		return [self.wdw,self.scr[1]]

class Inventory:
	def __init__(self):
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 25), 'ALT': pygame.font.Font('Fonts/PrestigeEliteStd.otf', 10)}
		self.wdw = pygame.Surface((400, 300), pygame.SRCALPHA)
		self.wdw.fill((resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]))
		for x in range(40):
			for y in range(30):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))

		self.itbor = pygame.Surface((100, 40))
		self.itbor.fill((resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]))
		for x in range(10):
			for y in range(4):
				self.itbor.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (1 + (x * 10),1 + (y * 10)))
		self.mnbor = pygame.Surface((60, 40))
		self.mnbor.fill((resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]))
		for x in range(6):
			for y in range(4):
				self.mnbor.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (1 + (x * 10),1 + (y * 10)))

		self.scr = [pygame.Surface((380,220)), pygame.Surface((760,600), pygame.SRCALPHA)]
		self.itmov = ''
		self.scroll = 50
		self.strgscroll = 50
		self.shake = 0
		self.arrow = 0
		self.arrdir = False

	def find(self, where, item):
		fnd = None
		if where != None:
			for y in resources.INVENTORY[where]:
				for x in y:
					if x[0] == item and fnd == None: fnd = x
		else:
			for i in resources.INVENTORY:
				for y in i:
					for x in y:
						if x[0] == item and fnd == None: fnd = x
		return fnd

	def add(self, where, item, prp='0000'):
		i = 0
		j = 0
		trigg = False
		for y in resources.INVENTORY[where]:
			if j != 4:
				for x in y:
					if i != 0 and x[0] == '_' and trigg == False:
						vi = prp
						if item.startswith('food'):
							dd = resources.DATE[0] + int(database.ITEMS[item][6][0:2])
							mm = resources.DATE[1] + int(database.ITEMS[item][6][2:4])
							if dd > 30: dd -= 30; mm += 1
							if mm > 12: dd += 1; mm -= 12
							if dd < 10: dd = '0' + str(dd)
							if mm < 10: mm = '0' + str(mm)
							vi = str(dd) + str(mm)
						resources.INVENTORY[where][j][i] = [item,vi,'_','_']
						trigg = True
					i += 1
			j += 1
			i = 0

	def space(self, where, ex=0, opt=None, lopt=None):
		if opt != None:
			if self.itmov[0] != 0:
				vlm = database.ITEMS[self.itmov[0]][3]
				wei = database.ITEMS[self.itmov[0]][4]
			else:
				vlm = database.ITEMS[self.itmov[ex]][3]
				wei = database.ITEMS[self.itmov[ex]][4]
		else:
			vlm = 0
			wei = 0
		trigg = True
		for y in resources.INVENTORY[where][:-1]:
			for x in y[1:]:
				if x[0] != '_':
					vlm += database.ITEMS[x[0]][3]
					wei += database.ITEMS[x[0]][4]
		if resources.INVENTORY[where][4][0][0] != '_':
			if vlm >= database.ITEMS[resources.INVENTORY[where][4][0][0]][3]: trigg = False
			if wei >= database.ITEMS[resources.INVENTORY[where][4][0][0]][4]: trigg = False
		if lopt == 4: trigg = True
		elif opt == 0: trigg = True
		if resources.INVENTORY[where][4][0][0] == '_': trigg = True
		return trigg

	def show(self, opt, lopt, mn, ex, tp):
		for i in self.scr: i.fill((0,0,0,0))
		x = 10
		y = 45
		optx = 0
		opty = 0
		mnc = 0
		dscr = '_'
		vlm = 0
		wei = 0

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
		for n in resources.PARTY[resources.FORMATION]:
			self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[n]['NAME'], True, (255, 255, 255)), ((10 + (200 * mnc) - self.scroll) * 2, 25))
			for j in range(len(resources.INVENTORY[n])):
				if opty == 4: y += 5
				for i in resources.INVENTORY[n][j]:
					if optx == 1: x += 5

					trigg = False
					if optx == 0 or opty == 4: trigg = True
					elif resources.INVENTORY[mnc][4][0][0] != '_': trigg = True

					if trigg == True:
						if opt == optx and lopt == opty and mn == mnc:
							if tp == 0: pygame.draw.rect(self.scr[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x + (200 * mnc) - self.scroll,y,30,30))
							if tp == 1: pygame.draw.rect(self.scr[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x,y + (210 * mnc) - self.scroll,30,30))
							dscr = resources.INVENTORY[resources.PARTY[resources.FORMATION][mn]][lopt][opt]
						else:
							if tp == 0: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x + (200 * mnc) - self.scroll,y,30,30))
							if tp == 1: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x,y + (210 * mnc) - self.scroll,30,30))
						if i[0] != '_':
							if tp == 0: self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + i[0] + '.png'), (x + (200 * mnc) - self.scroll, y))
							if tp == 1: self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + i[0] + '.png'), (x, y + (210 * mnc) - self.scroll))
							if optx > 0 and opty < 4:
								vlm += database.ITEMS[i[0]][3]
								wei += database.ITEMS[i[0]][4]
					x += 32
					optx += 1
				x = 10
				y += 32
				optx = 0
				opty += 1

			#VOLUME AND WEIGHT
			if tp == 0:
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[78] + ':', True, (255, 255, 255)), ((65 + 200 * mnc - self.scroll) * 2, 15))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120 + (200 * mnc) - self.scroll,10,50,10))
				if vlm > 0 and resources.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120 + (200 * mnc) - self.scroll,10,int(50/(database.ITEMS[resources.INVENTORY[mnc][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[79] + ':', True, (255, 255, 255)), ((65 + (200 * mnc) - self.scroll) * 2, 45))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120 + (200 * mnc) - self.scroll,25,50,10))
				if wei > 0 and resources.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120 + (200 * mnc) - self.scroll,25,int(50/(database.ITEMS[resources.INVENTORY[mnc][4][0][0]][4]/wei)),10))
			if tp == 1:
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[78] + ':', True, (255, 255, 255)), (65, (10 + (210 * mnc) - self.scroll) * 2))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120,12 + (210 * mnc) - self.scroll,50,10))
				if vlm > 0 and resources.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120,12 + (210 * mnc) - self.scroll,int(50/(database.ITEMS[resources.INVENTORY[mnc][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[79] + ':', True, (255, 255, 255)), (65, (25 + (210 * mnc) - self.scroll) * 2))
				pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(120,27 + (210 * mnc) - self.scroll,50,10))
				if wei > 0 and resources.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(120,27 + (210 * mnc) - self.scroll,int(50/(database.ITEMS[resources.INVENTORY[mnc][4][0][0]][4]/wei)),10))

			x = 10
			y = 45
			vlm = 0
			wei = 0
			optx = 0
			opty = 0
			mnc += 1

		if lopt > 5:
			if self.strgscroll < (lopt * 32):
				self.strgscroll += 8
			if self.strgscroll > (lopt * 32):
				self.strgscroll -= 8
		else:
			if self.strgscroll > 0:
				self.strgscroll -= 40
		if self.strgscroll < 0: self.strgscroll = 0

		#DEPOSIT ITEMS
		if tp == 1:
			x = 210
			y = 45
			optx = 5
			opty = 0

			self.scr[1].blit(self.fnt['CALIBRI'].render('Depositar', True, (255, 255, 255)), (420, (10 - self.strgscroll) * 2))
			for j in resources.STORAGE:
				if optx == 10:
					x = 210
					y += 32
					optx = 5
					opty += 1

				if opt == optx and lopt == opty:
					pygame.draw.rect(self.scr[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x, y - self.strgscroll,30,30))
					dscr = j
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x, y - self.strgscroll,30,30))
				if j[0] != '_':
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + j[0] + '.png'), (x, y - self.strgscroll))
				x += 32
				optx += 1

		#HOLDING ITEM
		if self.itmov != '':
			ox = (opt * 32) 
			lox = (lopt * 32)
			if opt > 0: ox += 5
			if lopt == 4: lox += 5
			if opt > 4: ox += 34

			#ITEM MOVE
			if self.itmov[0] != 0:
				if tp == 0:
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_shade.png'), (14 + (mn * 200) + ox - self.scroll,62 + lox))
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[0] + '.png'), (10 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
				if tp == 1:
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_shade.png'), (14 + ox,62 + (mn * 210) + lox - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[0] + '.png'), (10 + ox + self.shake,35 + (mn * 210) + lox - self.scroll))
			#SUB-ITEMS
			else:
				srf = pygame.Surface((70,40))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.scr[0].blit(srf, (25 + (mn * 200) + ox - self.scroll,40 + lox))
				self.scr[0].blit(self.itbor, (20 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
				'''if self.money == True:
					self.scr[0].blit(self.mnbor, (-35 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
					pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(-30 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,50,30))
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(resources.MONEY), True, (255, 255, 255)), ((-25 + (mn * 200) + ox - self.scroll + self.shake) * 2,(45 + lox) * 2))'''
				if ex == 1:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = [self.itmov[ex],resources.INVENTORY[resources.PARTY[resources.FORMATION][mn]][lopt][opt][1][0:4]]
				else: pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 2:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = [self.itmov[ex],resources.INVENTORY[resources.PARTY[resources.FORMATION][mn]][lopt][opt][1][4:8]]
				else: pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 3:
					pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					dscr = ['_','0000']
				else: pygame.draw.rect(self.scr[0], (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if self.itmov[1] != '_': self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[1] + '.png'), (25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				if self.itmov[2] != '_': self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[2] + '.png'), (55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				self.scr[0].blit(pygame.image.load('Sprites/e_run.png'), (85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
		
		#ARROWS
		if self.arrdir == False:
			self.arrow += 1
			if self.arrow == 8: self.arrdir = True
		elif self.arrdir == True:
			self.arrow -= 1
			if self.arrow == 0: self.arrdir = False
		if tp == 0:
			if mn > 0: self.scr[0].blit(pygame.transform.rotate(pygame.image.load('Sprites/arw.png'),270), (0 + self.arrow,110))
			if mn < len(resources.PARTY[resources.FORMATION]) - 1: self.scr[0].blit(pygame.transform.rotate(pygame.image.load('Sprites/arw.png'),90), (368 - self.arrow,110))
		if tp == 1:
			if mn > 0: self.scr[0].blit(pygame.transform.flip(pygame.image.load('Sprites/arw.png'),False,True), (80,0 + self.arrow))
			if mn < len(resources.PARTY[resources.FORMATION]) - 1: self.scr[0].blit(pygame.image.load('Sprites/arw.png'), (80,208 - self.arrow))

		self.wdw.blit(self.scr[0], (10,10))

		#ITEM DESCRIPTION
		pygame.draw.rect(self.wdw, (0, 0, 0), pygame.Rect(10,240,380,50))
		if dscr[0] != '_':
			y = 0
			txt = database.ITEMS[dscr[0]][1].copy()
			if dscr[0].startswith('gun'):
				if len(txt) == 1: txt.append('ammo: ' + str(dscr[1]) + '/' + str(database.ITEMS[dscr[0]][5]['CAPACITY']))
				elif len(txt) == 2: txt[1] += ' - ammo: ' + str(dscr[1]) + '/' + str(database.ITEMS[dscr[0]][5]['CAPACITY'])
			if dscr[0].startswith('wallet'):
				if len(txt) == 1: txt.append('$' + str(dscr[1][0:6]))
				elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1][0:6])
			if dscr[0].startswith('credit_card'):
				if len(txt) == 1: txt.append('$' + str(dscr[1]))
				elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1])
			if dscr[0].startswith('bottle'):
				if len(txt) == 1: txt.append(str(dscr[1]) + 'ml/' + str(database.ITEMS[dscr[0]][5]) + 'ml')
				elif len(txt) == 2: txt[1] += ' - ' + str(dscr[1]) + 'ml/' + str(database.ITEMS[dscr[0]][5]) + 'ml'
			for t in txt:
				self.scr[1].blit(self.fnt['CALIBRI'].render(t, True, (255, 255, 255)), (20, 480 + y))
				y += 30

		if self.shake > 0: self.shake = -self.shake
		elif self.shake < 0: self.shake = -self.shake - 1

		return [self.wdw,self.scr[1]]

class Shop:
	def __init__(self):
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font('Fonts/monotype.ttf', 10),
			'TITLE': pygame.font.Font('Fonts/pixel-font.ttf', 25), 'DATETIME': pygame.font.Font('Fonts/datetype.ttf', 8)}
		self.wdw = pygame.Surface((400, 250))
		pygame.draw.rect(self.wdw, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,0,400,250))
		for x in range(40):
			for y in range(25):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))
		self.scr = [pygame.Surface((380,230)),pygame.Surface((760,460), pygame.SRCALPHA)]
		self.inv = Inventory()
		
	def products(self, opt, lopt, lst):
		for i in self.scr: i.fill((0,0,0,0))
		mny = 0
		for i in resources.PARTY[resources.FORMATION]:
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
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (0, 0, 0)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt['CALIBRI'].render(str(opt) + 'x', True, (0, 0, 0)), (360, 30 + (y * 12)))
			else:
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt['CALIBRI'].render(str(opt) + 'x', True, (255, 255, 255)), (360, 30 + (y * 12)))
			y += 1

		if lopt != len(lst):
			l = 0
			for j in database.ITEMS[lst[lopt]][1]:
				self.scr[0].blit(self.fnt['CALIBRI'].render(j, True, (255, 255, 255)), (20,200 + (l * 10)))
				l += 1

		if lopt == y:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,33 + (y * 12),370,12))
			self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[1], True, (0, 0, 0)), (20, 30 + (y * 12)))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[1], True, (255, 255, 255)), (20, 30 + (y * 12)))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def buy(self, opt, lopt, lst):
		for i in self.scr: i.fill((0,0,0,0))
		mny = 0
		for i in resources.PARTY[resources.FORMATION]:
			src = self.inv.find(i,'credit_card')
			if src == None:
				src = self.inv.find(i,'wallet')
				if src != None:
					mny = int(src[1][0:6])
					break
			else:
				mny = int(src[1])
				break
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
				self.scr[0].blit(self.fnt['CALIBRI'].render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, 25 + (y * 15)))
				cost += database.ITEMS[i][2]
				y += 1

		self.scr[0].blit(self.fnt['CALIBRI'].render('valor: ' + str(mny), True, (255, 255, 255)), (305, 165))
		self.scr[0].blit(self.fnt['CALIBRI'].render('total: ' + str(cost), True, (255, 255, 255)), (305, 185))
		if mny - cost > 0: pcol = (0,255,0)
		else: pcol = (255,0,0)
		self.scr[0].blit(self.fnt['CALIBRI'].render('troco: ' + str(mny - cost), True, pcol), (305, 205))
		self.scr[0].blit(self.fnt['CALIBRI'].render('atendente: ', True, (255, 255, 255)), (10, 230))
		self.scr[0].blit(self.fnt['CALIBRI'].render('hora: ' + str(resources.TIME[0]) + ': ' + str(resources.TIME[1]), True, (255, 255, 255)), (200, 230))
		self.scr[0].blit(self.fnt['CALIBRI'].render('data: ' + str(resources.DATE[0]) + '/ ' + str(resources.DATE[1]), True, (255, 255, 255)), (300, 230))

		if lopt == 0:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,204,300,12))
			self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[0], True, (0,0,0)), (10, 201))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[0], True, (255, 255, 255)), (10, 201))

		if lopt == 1:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,216,300,12)); tcol = (0,0,0)
			self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[7], True, (0, 0, 0)), (10, 213))
		else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.SHOP[7], True, (255, 255, 255)), (10, 213))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def mercator(self, opt, lopt, lst, prm):
		for i in self.scr: i.fill((0,0,0,0))
		mny = 0
		for i in resources.PARTY[resources.FORMATION]:
			src = self.inv.find(i,'credit_card')
			if src == None:
				src = self.inv.find(i,'wallet')
				if src != None:
					mny = int(src[1][0:6])
					break
			else:
				mny = int(src[1])
				break
		#OPTIONS
		self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(mny), True, (255, 255, 255)), (20, 20))
		if opt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(database.SHOP[8], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20, 60))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.SHOP[8], True, (255,255,255)), (20, 60))
		x = 1
		for i in resources.PARTY[resources.FORMATION]:
			if opt == x: self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[i]['NAME'], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (40 + (x * 120), 60))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[i]['NAME'], True, (255,255,255)), (40 + (x * 120), 60))
			x += 1
		y = 0
		for i in lst:
			#MERCATOR PRODUCTS
			if opt == 0:
				if prm > 0:
					prc = database.ITEMS[i][2] - int(database.ITEMS[i][2]/prm)
				else: prc = database.ITEMS[i][2]
				if lopt == y:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(prc) + ' - ' + database.ITEMS[i][0], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20, (50 + (y * 15)) * 2))
				else:
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(prc) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))
				if prm > 0:
					pygame.draw.rect(self.scr[0], (255, 170, 0), pygame.Rect(350,50 + (y * 15),30,20))
					self.scr[1].blit(self.fnt['DATETIME'].render(str(prm) + '%', True, (255, 255, 255)), (350, (50 + (y * 15)) * 2))
				y += 1
			#SELLING PARTY ITEMS
			else:
				itm = resources.INVENTORY[resources.PARTY[resources.FORMATION][opt - 1]][i[0]][i[1]][0]
				if lopt == y:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(int(database.ITEMS[itm][2]/2)) + ' - ' + database.ITEMS[itm][0], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20, (50 + (y * 15)) * 2))
				else:
					self.scr[1].blit(self.fnt['CALIBRI'].render('$' + str(int(database.ITEMS[itm][2]/2)) + ' - ' + database.ITEMS[itm][0], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))
				y += 1
		#ITEMS DESCRIPTIONS
		if lopt != len(lst):
			l = 0
			if opt == 0:
				for j in database.ITEMS[lst[lopt]][1]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(j, True, (255, 255, 255)), (20,(190 + (l * 15)) * 2))
					l += 1
			else:
				for t in database.ITEMS[resources.INVENTORY[resources.PARTY[resources.FORMATION][opt - 1]][lst[lopt][0]][lst[lopt][1]][0]][1]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(t, True, (255, 255, 255)), (20,(190 + (l * 15)) * 2))
					l += 1
		#EXIT SHOP
		if lopt == y:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,50 + (y * 15),380,15))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.SHOP[1], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20, (50 + (y * 15)) * 2))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.SHOP[1], True, (255, 255, 255)), (20, (50 + (y * 15)) * 2))

		self.wdw.blit(self.scr[0], (10,10))
		return [self.wdw, self.scr[1]]

	def bank(self, opt, lopt, mn, ext):
		self.scr[0].fill((234,234,234))
		mny = 0
		for i in resources.PARTY[resources.FORMATION]:
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
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[5], True, (0,0,0)), (10, 120))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,120,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[5], True, (0, 0, 0)), (10, 120))

			if lopt == 1:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[6], True, (0, 0, 0)), (10, 160))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[6], True, (0, 0, 0)), (10, 160))

			if lopt == 2:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[7], True, (0, 0, 0)), (10, 200))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.fnt['TITLE'].render(database.SHOP[7], True, (0, 0, 0)), (10, 200))

		else:
			pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(80,80,200,110))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,90,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,120,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,150,130,27))
			pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(120 + opt * 6,135,5,2))

			self.scr[0].blit(self.fnt['TITLE'].render(str(resources.ATM), True, (0,0,0)), (120, 90))
			self.scr[0].blit(self.fnt['TITLE'].render(str(ext[0]) + str(ext[1]) + str(ext[2]) + str(ext[3]) + str(ext[4]) + str(ext[5]), True, (0,0,0)), (120, 120))
			self.scr[0].blit(self.fnt['TITLE'].render(str(mny), True, (0,0,0)), (120, 150))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

class Phone:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font('Fonts/monotype.ttf', 10),
			'TITLE': pygame.font.Font('Fonts/pixel-font.ttf', 40), 'DATETIME': pygame.font.Font('Fonts/Sicret_PERSONAL-Regular.ttf', 32)}
		self.pbg = resources.PARTY[resources.FORMATION][0]
		self.scroll = 0
		self.mp = None

	def bar(self, sg):
		self.bsc = [pygame.Surface((self.scr[0].get_width(),18)),pygame.Surface((self.scr[1].get_width(),36), pygame.SRCALPHA)]
		for i in self.bsc: i.fill((10,10,10,0))
		dvd3 = math.floor(self.scr[0].get_width()/3)

		day = ['','','']
		if resources.DATE[0] < 10: day[0] = '0' + str(resources.DATE[0])
		else: day[0] = str(resources.DATE[0])
		if resources.DATE[1] < 10: day[1] = '0' + str(resources.DATE[1])
		else: day[1] = str(resources.DATE[1])
		if resources.DATE[2] < 10: day[2] = '0' + str(resources.DATE[2])
		else: day[2] = str(resources.DATE[2])
		self.bsc[1].blit(self.fnt['DATETIME'].render(day[0] + '/' + day[1] + '/' + day[2], True, (255, 255, 255)), (3, 4))

		hour = ['','']
		if resources.TIME[0] < 10: hour[0] = '0' + str(resources.TIME[0])
		else: hour[0] = str(resources.TIME[0])
		if resources.TIME[1] < 10: hour[1] = '0' + str(resources.TIME[1])
		else: hour[1] = str(resources.TIME[1])
		self.bsc[1].blit(self.fnt['DATETIME'].render(hour[0] + ':' + hour[1], True, (255, 255, 255)), ((dvd3 + 30) * 2, 4))

		self.bsc[0].blit(pygame.image.load('Sprites/signal_' + str(sg) + '.png'), ((dvd3 * 3) - 47, 6))
		self.bsc[0].blit(pygame.image.load('Sprites/battery.png'), ((dvd3 * 3) - 30, 2))
		if resources.BATTERY > 100.0: pygame.draw.rect(self.bsc[0], (255, 255, 255), pygame.Rect((dvd3 * 3) - 7 - int(18/(360/resources.BATTERY)),5,int(18/(360/resources.BATTERY)),7))
		elif resources.BATTERY > 1.0: pygame.draw.rect(self.bsc[0], (255, 10, 10), pygame.Rect((dvd3 * 3) - 7 - int(18/(360/resources.BATTERY)),5,int(18/(360/resources.BATTERY)),7))

		return self.bsc

	def apps(self, opt, lopt):
		for i in self.scr: i.fill((10,10,10,0))

		if lopt > 2:
			if self.scroll < (lopt - 2) * 60:
				self.scroll += 10
		elif lopt > 0 and lopt < 3:
			if self.scroll > (lopt - 1) * 60:
				self.scroll -= 10
		elif lopt == 0 and self.scroll > 0:
			self.scroll -= 10

		self.scr[0].blit(pygame.image.load('Backgrounds/phone_' + str(self.pbg) + '.png'), (0, 0))

		dvd3 = math.floor(self.scr[0].get_width()/3)
		pdd = 10
		if opt == 0 and lopt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_maps.png'), (50, 50)), (pdd - 3, 2 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_maps.png'), (pdd, 5 - self.scroll))
		if opt == 1 and lopt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_call.png'), (50, 50)), (pdd - 3 + dvd3, 2 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_call.png'), (pdd + dvd3, 5 - self.scroll))
		if opt == 2 and lopt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_mail.png'), (50, 50)), (pdd - 3 + (dvd3 * 2), 2 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_mail.png'), (pdd + (dvd3 * 2), 5 - self.scroll))
		if opt == 0 and lopt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_news.png'), (50, 50)), (pdd - 3, 62 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_news.png'), (pdd, 65 - self.scroll))
		if opt == 1 and lopt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_radi.png'), (50, 50)), (pdd - 3 + dvd3, 62 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_radi.png'), (pdd + dvd3, 65 - self.scroll))
		if opt == 2 and lopt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_camr.png'), (50, 50)), (pdd - 3 + (dvd3 * 2), 62 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_camr.png'), (pdd + (dvd3 * 2), 65 - self.scroll))
		if opt == 0 and lopt == 2: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_best.png'), (50, 50)), (pdd - 3, 122 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_best.png'), (pdd, 125 - self.scroll))
		if opt == 1 and lopt == 2: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_task.png'), (50, 50)), (pdd - 3 + dvd3, 122 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_task.png'), (pdd + dvd3, 125 - self.scroll))
		if opt == 2 and lopt == 2: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_stts.png'), (50, 50)), (pdd - 3 + (dvd3 * 2), 122 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_stts.png'), (pdd + (dvd3 * 2), 125 - self.scroll))
		if opt == 0 and lopt == 3: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_tact.png'), (50, 50)), (pdd - 3, 182 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_tact.png'), (pdd, 185 - self.scroll))
		if opt == 1 and lopt == 3: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_achi.png'), (50, 50)), (pdd - 3 + dvd3, 182 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_achi.png'), (pdd + dvd3, 185 - self.scroll))
		if opt == 2 and lopt == 3: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_rank.png'), (50, 50)), (pdd - 3 + (dvd3 * 2), 182 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_rank.png'), (pdd + (dvd3 * 2), 185 - self.scroll))
		if opt == 0 and lopt == 4: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_help.png'), (50, 50)), (pdd - 3, 242 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_help.png'), (pdd, 245 - self.scroll))
		if opt == 1 and lopt == 4: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_sett.png'), (50, 50)), (pdd - 3 + dvd3, 242 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_sett.png'), (pdd + dvd3, 245 - self.scroll))
		if opt == 2 and lopt == 4: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/ph_info.png'), (50, 50)), (pdd - 3 + (dvd3 * 2), 242 - self.scroll))
		else: self.scr[0].blit(pygame.image.load('Sprites/ph_info.png'), (pdd + (dvd3 * 2), 245 - self.scroll))

		return self.scr

	def map(self, mn, rm, tl, pl, en, sig, x, y, zoom, sg):
		sz = self.scr[0].get_width() #button width
		if mn == False: scr = [pygame.Surface((sz,232)),pygame.Surface((sz * 2,464),pygame.SRCALPHA)]
		if mn == True: scr = [pygame.Surface((100,100)),pygame.Surface((200,200),pygame.SRCALPHA)]
		for i in scr: i.fill((0,0,0,0))
		if sg > 0:
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

			mpx = x - int(zoom/2)
			mpy = y - int(zoom/2)
			scr[0].blit(pygame.transform.scale(self.mp, (zoom,zoom)), (mpx,mpy))

			xx = (pl['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
			yy = (pl['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
			scr[0].blit(pygame.image.load('Sprites/mp_player.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in resources.MARKER:
				xx = (i[1] - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i[2] - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				#if i[0] == rm:
				scr[0].blit(pygame.image.load('Sprites/mp_pin.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in sig:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				scr[0].blit(pygame.image.load('Sprites/mp_' + i['ICON'] + '.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in en:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				if i['HP'] > 0 and i['RECT'].x > 0 and i['RECT'].y > 0:
					scr[0].blit(pygame.image.load('Sprites/mp_anomaly.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
		else: scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (25, 200))

		if mn == False:
			pygame.draw.rect(scr[1], (140, 255, 253), pygame.Rect(0,0,sz * 2,80))
			scr[1].blit(self.fnt['TITLE'].render(database.MENU[0], True, (0, 0, 0)), (5, 4))

		return scr

	def contacts(self, flt, opt, mnu):
		sz = self.scr[0].get_width() #button width
		if flt == 0: em = resources.PARTY
		if flt == 1: em = resources.CONTACTS
		if flt == 2: em = resources.CALLHIST
		if opt > 2:
			if self.scroll < (opt - 2) * 51:
				self.scroll += 5.1
		elif opt > 0 and opt < len(em) - 1:
			if self.scroll > (opt - 1) * 51:
				self.scroll -= 5.1
		elif opt == 0:
			if self.scroll > 0:
				self.scroll -= 5.1
		for i in self.scr: i.fill((10,10,10,0))
		y = 0
		for i in em:
			if opt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,sz,50))

			if flt > 0: self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, (76 + y - self.scroll) * 2))
			else:
				if opt == y/51:
					if mnu == 1: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 52,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load('Sprites/tc_9.png'), (sz - 50, 76 + y - self.scroll))
					if mnu == 2: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 30,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load('Sprites/tc_8.png'), (sz - 28, 76 + y - self.scroll))
					if mnu == 3: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(8,74 + y - self.scroll,24,24))
					if mnu == 4: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(30,74 + y - self.scroll,24,24))
					if mnu == 5: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(52,74 + y - self.scroll,24,24))
				x = 0
				for p in i:
					self.scr[0].blit(pygame.image.load('Sprites/who_' + str(p) + '.png'), (10 + x, 76 + y - self.scroll))
					x += 22
			if flt == 0: self.scr[1].blit(self.fnt['CALIBRI'].render('grupo ' + str(int((y + 51)/51)), True, (0, 0, 0)), (20, (96 + y - self.scroll) * 2))
			if flt == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, (92 + y - self.scroll) * 2))
			if flt == 2: self.scr[0].blit(pygame.image.load('Sprites/who_' + str(i[1]).lower() + '.png'), (160, 43 + y - self.scroll))
			y += 51
		if flt == 0:
			if opt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[31], True, (0, 0, 0)), (170, (83 + y - self.scroll) * 2))
		if y == 0 and flt == 1:
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[16], True, (255, 255, 255)), (100, 280))
		dvd3 = math.floor(sz/3)
		if flt == 0:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[23], True, (0, 0, 0)), (16, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(0,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[23], True, (255, 255, 255)), (16, 94))
		if flt == 1:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[24], True, (0, 0, 0)), ((dvd3 * 2) + 20, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(dvd3,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[24], True, (255, 255, 255)), ((dvd3 * 2) + 20, 94))
		if flt == 2:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[25], True, (0, 0, 0)), ((dvd3 * 4) + 20, 94))
		else:
			pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(dvd3 * 2,40,dvd3,25))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[25], True, (255, 255, 255)), ((dvd3 * 4) + 20, 94))
		pygame.draw.rect(self.scr[1], (15, 255, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[1], True, (0, 0, 0)), (10, 10))

		return self.scr

	def email(self, flt, opt, mnu, sg):
		sz = self.scr[0].get_width() #button width
		self.e_read = []
		self.e_unread = []
		for i in resources.INBOX:
			if i[3] == 1:
				self.e_read.append(i)
			if i[3] == 0:
				self.e_unread.append(i)
				
		if flt == 0: em = self.e_unread
		if flt == 1: em = self.e_read
		if flt == 2: em = resources.INBOX

		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0:
			if mnu == 0:
				self.scroll = 0
				if opt > 2: self.scroll += (opt - 2) * 51

				y = 0
				for i in em:
					if opt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,sz,50))
					else: pygame.draw.rect(self.scr[0], (255, 221, 0), pygame.Rect(0,66 + y,sz,50))
					self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, (0, 0, 0)), (20, 152 + y - self.scroll))
					self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, 172 + y - self.scroll))
					y += 51
				if y == 0:
					self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[19], True, (255, 255, 255)), (510, 280))

				dvd3 = math.floor(sz/3)
				if flt == 0:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[26], True, (0, 0, 0)), (24, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[26], True, (255, 255, 255)), (24, 94))
				if flt == 1:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[27], True, (0, 0, 0)), ((dvd3 * 2) + 30, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[27], True, (255, 255, 255)), ((dvd3 * 2) + 30, 94))
				if flt == 2:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
					self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[28], True, (0, 0, 0)), ((dvd3 * 4) + 24, 94))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[28], True, (255, 255, 255)), ((dvd3 * 4) + 24, 94))

			elif mnu > 0:
				self.scroll = (mnu - 1) * 3
				pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
				self.scr[1].blit(self.fnt['CALIBRI'].render(em[opt][1], True, (0, 0, 0)), (30, 110 - self.scroll))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[34] + em[opt][0], True, (0, 0, 0)), (30, 170 - self.scroll))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[35] + (resources.CHARACTERS[resources.PARTY[0][0]]['NAME'] + resources.CHARACTERS[resources.PARTY[0][0]]['LASTNAME']).lower() + '@cmail.com', True, (0, 0, 0)), (30, 200 - self.scroll))
				y = 0
				for l in em[opt][2]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (15, 130 + y - self.scroll))
					y += 15
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (100, 200))

		pygame.draw.rect(self.scr[1], (255, 221, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[2], True, (0, 0, 0)), (10, 10))

		return self.scr

	def news(self, opt, mnu, sg):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0:
			if mnu == 0:
				self.scroll = 0
				if opt > 2: self.scroll += (opt - 2) * 51
				y = 0
				opty = 0
				hei = 0
				for i in database.NEWS[resources.DATE[0] - 1]:
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
				for l in database.NEWS[resources.DATE[0] - 1][opt][0]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (20, (50 + y - self.scroll) * 2))
					y += 15
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.NEWS[resources.DATE[0] - 1][opt][1], True, (0, 0, 0)), (20, (55 + y - self.scroll) * 2))
				for l in database.NEWS[resources.DATE[0] - 1][opt][2]:
					self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (20, (100 + y - self.scroll) * 2))
					y += 15
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (219, 49, 37), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[3], True, (0, 0, 0)), (10, 10))

		return self.scr

	def radio(self, fm, msc):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))
		if resources.RADIO[str(math.floor(fm/20))] != []:
			pygame.draw.rect(self.scr[0], (255, 0, 135), pygame.Rect(0,66,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(resources.RADIO[str(math.floor(fm/20))][msc][:-4], True, (0, 0, 0)), (20, 152))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[20], True, (255, 255, 255)), (140, 280))

		pygame.draw.rect(self.scr[0], (10, 10, 10), pygame.Rect(0,40,sz,26))
		f = 0
		sp = math.floor(sz/9)
		for i in range(9):
			pygame.draw.line(self.scr[0], (255, 255, 255), (0 + f,50),(0 + f,65),1)
			pygame.draw.line(self.scr[0], (255, 255, 255), (round(sp/2) + f,55),(round(sp/2) + f,65),1)
			f += sp
		pygame.draw.rect(self.scr[0], (255, 0, 0), pygame.Rect(0 + fm,50,4,16))
		self.scr[1].blit(self.fnt['CALIBRI'].render(str(fm/10), True, (255, 255, 255)), (140, 40))

		pygame.draw.rect(self.scr[1], (255, 0, 135), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[4], True, (0, 0, 0)), (10, 10))

		return self.scr

	def camera(self, opt, sg):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((10,10,10,0))

		if sg > 0:
			y = 0
			for i in range(len(resources.FILES[1])):
				if opt != y: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + (y * 51),sz,50))
				else: pygame.draw.rect(self.scr[0], (255, 255, 10), pygame.Rect(0,41 + (y * 51),sz,50))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.CHAPTERS[resources.FILES[1][i]][0], True, (0, 0, 0)), (20, (51 + (y * 51)) * 2))
				ss = math.floor(resources.FILES[2][i]/1000)
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
				for p in resources.FILES[4][i][::-1]:
					self.scr[0].blit(pygame.image.load('Sprites/who_' + str(p) + '.png'), (sz - 30 - x, 65 + (y * 51)))
					x += 22
				y += 1

			if opt != y: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + (y * 51),sz,50))
			else: pygame.draw.rect(self.scr[0], (255, 255, 10), pygame.Rect(0,41 + (y * 51),sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[61], True, (0, 0, 0)), (20, (61 + (y * 51)) * 2))

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[5], True, (0, 0, 0)), (10, 10))

		return self.scr

	def bestiary(self, opt, lopt, mnu, sg):
		sz = self.scr[0].get_width() #button width
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0:
			if len(resources.BESTIARY) > 0:
				if mnu == 0:
					y = 0
					for i in resources.BESTIARY:
						if i['SEEN'] > 0:
							if lopt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
							else: pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(0,41 + y - self.scroll,sz,50))
							self.scr[1].blit(self.fnt['CALIBRI'].render(database.FREAKS[i['N']]['NAME'], True, (0, 0, 0)), (10, 51 + y - self.scroll))
							y += 51

				if mnu == 1:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,170,200))
					pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(5,243,83,3))
					self.scr[1].blit(self.fnt['CALIBRI'].render(database.FREAKS[resources.BESTIARY[opt]['N']]['NAME'], True, (0, 0, 0)), (10, 55))
					self.scr[0].blit(pygame.image.load('Sprites/' + resources.BESTIARY[opt]['N'] + '_stand.png'), (60, 70))
					self.scr[1].blit(self.fnt['CALIBRI'].render('ID: ' + resources.BESTIARY[opt]['ID'], True, (0, 0, 0)), (20, 160))
					self.scr[1].blit(self.fnt['CALIBRI'].render('RG: ' + resources.BESTIARY[opt]['DATE'], True, (0, 0, 0)), (60, 160))
					self.scr[1].blit(self.fnt['CALIBRI'].render('HG: ' + database.FREAKS[resources.BESTIARY[opt]['N']]['HEIGHT'], True, (0, 0, 0)), (110, 160))

					j = 0
					for l in database.FREAKS[resources.BESTIARY[opt]['N']]['INFO']:
						self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (10, sz + j))
						j += 15

				if mnu == 2:
					pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,200))
					pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(92,243,83,3))
					pygame.draw.rect(self.scr[0], (0, 0, 0), pygame.Rect(10,50,160,77))

					y = 0
					for i in database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES']:
						if lopt != y/19: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(11,51 + y,158,18))
						else: pygame.draw.rect(self.scr[0], (134, 0, 211), pygame.Rect(11,51 + y,158,18))
						self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, 53 + y))
						y += 19

					j = 0
					for l in database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][1]:
						self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (10, 140 + j))
						j += 15

					if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 1: dmg = database.MENU[37] + str(database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 2: dmg = database.MENU[38] + str(database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 3: dmg = database.MENU[39] + str(database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 4: dmg = database.MENU[40] + str(database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 5: dmg = database.MENU[41] + str(database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2])
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 6:
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 4: dmg = database.MENU[42]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 5: dmg = database.MENU[43]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 6: dmg = database.MENU[44]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 7: dmg = database.MENU[45]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 8: dmg = database.MENU[46]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 9: dmg = database.MENU[47]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 10: dmg = database.MENU[48]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 11: dmg = database.MENU[49]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] in (12,13,14): dmg = database.MENU[50]
						if database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][2] == 15: dmg = database.MENU[51]
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 7: dmg = database.MENU[52]
					elif database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][3] == 8: dmg = database.MENU[53]
					else: dmg = ''

					self.scr[1].blit(self.fnt['CALIBRI'].render(dmg, True, (0, 0, 0)), (20, 210))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[21], True, (255, 255, 255)), (10, 140))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (134, 0, 211), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[6], True, (0, 0, 0)), (10, 10))

		return self.scr

	def task(self, flt, opt, mnu):
		sz = self.scr[0].get_width() #button width
		self.t_unmark = []
		self.t_mark = []
		for i in resources.TASKS:
			if i[1] == 1:
				self.t_mark.append(i)
			if i[1] == 0:
				self.t_unmark.append(i)

		if flt == 0: em = self.t_unmark
		if flt == 1: em = self.t_mark
		if flt == 2: em = resources.TASKS

		if opt > 2:
			if self.scroll < (opt - 2) * 31:
				self.scroll += 6.2
		elif opt > 0 and opt < len(em) - 1:
			if self.scroll > (opt - 1) * 31:
				self.scroll -= 6.2
		elif opt == 0 and self.scroll > 0:
			self.scroll -= 6.2
			
		for i in self.scr: i.fill((10,10,10,0))
		y = 0
		for i in em:
			if opt != y/31: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.sz,30))
			else: pygame.draw.rect(self.scr[0], (255, 123, 0), pygame.Rect(0,66 + y - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, 146 + y - self.scroll))
			y += 31
		if y == 0:
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[22], True, (255, 255, 255)), (80, 280))

		dvd3 = math.floor(sz/3)
		if flt == 0:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[29], True, (0, 0, 0)), (24, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[29], True, (255, 255, 255)), (24, 94))
		if flt == 1:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[30], True, (0, 0, 0)), ((dvd3 * 2) + 30, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[30], True, (255, 255, 255)), ((dvd3 * 2) + 30, 94))
		if flt == 2:
			pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[28], True, (0, 0, 0)), ((dvd3 * 4) + 24, 94))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[28], True, (255, 255, 255)), ((dvd3 * 4) + 24, 94))

		pygame.draw.rect(self.scr[1], (255, 123, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[7], True, (0, 0, 0)), (10, 10))

		return self.scr

	def status(self, opt):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if opt > 2: self.scroll += (opt - 2) * 60

		for i in self.scr: i.fill((10,10,10,0))

		x = 0
		dvd3 = math.floor(sz/3)
		for i in resources.PARTY[resources.FORMATION]:
			if opt == x/dvd3:
				pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0 + x - self.scroll,45,dvd3,20))
				self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[i]['NAME'], True, (0, 0, 0)), ((16 + x - self.scroll) * 2, 95))
			else: self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[i]['NAME'], True, (255, 255, 255)), ((16 + x - self.scroll) * 2, 95))
			x += dvd3

		self.scr[0].blit(pygame.image.load('Sprites/who_' + str(resources.PARTY[resources.FORMATION][opt]) + '.png'), (10, 74))
		self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['NAME'] + ' ' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LASTNAME'], True, (255, 255, 255)), (70, 152))
		self.scr[1].blit(self.fnt['CALIBRI'].render(str(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ID']), True, (255, 255, 255)), (20, 192))
		self.scr[0].blit(pygame.image.load('Sprites/gn_' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['GENDER'] + '.png'), (70, 96))
		self.scr[1].blit(self.fnt['CALIBRI'].render(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['BLOOD'], True, (255, 255, 255)), (100, 192))

		self.scr[1].blit(self.fnt['CALIBRI'].render('level ' + str(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']), True, (255, 255, 255)), (20, 230))
		self.scr[1].blit(self.fnt['CALIBRI'].render('hp:', True, (255, 255, 255)), (20, 260))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,135,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['HP'] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,135,int(100/(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['VITALITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']]/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['HP'])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('xp:', True, (255, 255, 255)), (20, 290))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,150,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['XP'] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,150,int(100/(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['MAXXP']/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['XP'])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('st:', True, (255, 255, 255)), (20, 320))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,165,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['STRENGHT'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,165,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['STRENGHT'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('at:', True, (255, 255, 255)), (20, 350))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,180,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ATTACK'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,180,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ATTACK'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('ag:', True, (255, 255, 255)), (20, 380))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,195,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['AGILITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,195,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['AGILITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[1].blit(self.fnt['CALIBRI'].render('rs:', True, (255, 255, 255)), (20, 410))
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(40,210,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['RESISTANCE'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr[0], (0, 255, 0), pygame.Rect(40,210,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['RESISTANCE'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))

		pygame.draw.rect(self.scr[1], (255, 0, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[8], True, (0, 0, 0)), (10, 10))

		return self.scr

	def tactics(self, opt, lopt, mnu, sg):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if lopt > 2: self.scroll += (lopt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0:
			y = 0
			for i in resources.TACTICAL:
				if i != [] and len(i) == 4:
					if lopt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
					else: pygame.draw.rect(self.scr[0], (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,sz,50))

					if mnu > 0 and lopt == y/51:
						if mnu < 5:
							pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(8 + (mnu - 1) * 22,49 + y - self.scroll,24,24))
							if i[mnu - 1] == 1: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[54], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 2: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[55], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 3: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[56], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 4: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[57], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 5: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[58], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 6: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[59], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
							if i[mnu - 1] == 7: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[60], True, (0, 0, 0)), (20, (75 + y - self.scroll) * 2))
						else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(sz - 42,49 + y - self.scroll,24,24))
						self.scr[0].blit(pygame.image.load('Sprites/tc_8.png'), (sz - 40, 51 + y - self.scroll))

					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[0]) + '.png'), (10, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[1]) + '.png'), (32, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[2]) + '.png'), (54, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[3]) + '.png'), (76, 51 + y - self.scroll))
				y += 51

			if lopt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
			else: pygame.draw.rect(self.scr[0], (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,sz,50))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[36], True, (0, 0, 0)), (100, (60 + y - self.scroll) * 2))

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (33, 75, 127), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[9], True, (0, 0, 0)), (10, 10))

		return self.scr

	def achievements(self, opt, sg):
		self.scroll = 0
		sz = self.scr[0].get_width() #button width
		if opt > 2: self.scroll += (opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0:
			y = 0
			for i in database.ACHIEVEMENTS:
				if opt != y/51: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,50))
				else: pygame.draw.rect(self.scr[0], (255, 191, 0), pygame.Rect(0,41 + y - self.scroll,sz,50))

				if i[2] == True: tcol = (0,0,0)
				else: tcol = (80,80,80)
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, tcol), (20, (51 + y - self.scroll) * 2))
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[1], True, tcol), (20, (65 + y - self.scroll) * 2))
				y += 51

		else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (255, 191, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[10], True, (0, 0, 0)), (10, 10))

		return self.scr

	def ranking(self, opt, sg):
		sz = self.scr[0].get_width() #button width
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		for i in self.scr: i.fill((10,10,10,0))
		if sg > 0: pass
		else: self.scr[1].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr[1], (55, 255, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[11], True, (0, 0, 0)), (10, 10))
		pygame.draw.rect(self.scr[0], (10, 10, 10), pygame.Rect(0,40,sz,210))

		return self.scr

	def help(self, opt, mnu):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[0].get_width() #button width
		if mnu == 0:
			self.scroll = 0
			if opt > 2: self.scroll += (opt - 2) * 31
			y = 0
			for i in database.MANUAL:
				if opt != y/31: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr[0], (137, 50, 0), pygame.Rect(0,41 + y - self.scroll,sz,30))
				self.scr[1].blit(self.fnt['CALIBRI'].render(i[0], True, (0, 0, 0)), (20, (51 + y - self.scroll) * 2))
				y += 31

		if mnu > 0:
			self.scroll = (mnu - 1) * 3
			pygame.draw.rect(self.scr[0],(255, 255, 255), pygame.Rect(5,45,222,200))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MANUAL[opt][0], True, (0, 0, 0)), (140, 110 - self.scroll))
			y = 0
			for l in database.MANUAL[opt][1]:
				self.scr[1].blit(self.fnt['CALIBRI'].render(l, True, (0, 0, 0)), (30, 160 + y - self.scroll))
				y += 30

		pygame.draw.rect(self.scr[1], (137, 50, 0), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[12], True, (0, 0, 0)), (10, 10))

		return self.scr

	def settings(self, opt, mnu, trg):
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
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp
		#GAMEPLAY MENU
		if mnu == 1:
			inpts = (62,72,73,74,75,87,96,97,98)
			if opt == 0:
				if self.scroll > 0:
					self.scroll -= 10
			elif opt == 5 or opt == 6:
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
						pygame.draw.rect(self.scr[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,y - self.scroll,sz,hz))
					else:
						pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				#SCROLL BAR
				if i >= 2 and i < 5:
					pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
					pygame.draw.rect(self.scr[0], (110,110,110), pygame.Rect(bs + int(bw/(242/resources.COLOR[i - 2])) - 10,y + bh - self.scroll,10,10))
				#BORDER OPTIONS
				if i == 5:
					for b in range(math.floor(sz/10) - 4):
						for c in range(3): self.scr[0].blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (60 + b * 10, 196 + (c * 10) - self.scroll))
				#SWITCH
				if i == 6:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if resources.CENSORSHIP == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y + 10 - self.scroll,40,10))
					if resources.CENSORSHIP == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y + 10 - self.scroll,40,10))
				if i == 7:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if resources.HINT == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y - self.scroll,40,10))
					if resources.HINT == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y - self.scroll,40,10))
				if i == 8:
					pygame.draw.rect(self.scr[0], (230,230,230), pygame.Rect(75,y + 10 - self.scroll,80,10))
					if resources.HELP == False: pygame.draw.rect(self.scr[0], (255,61,61), pygame.Rect(115,y - self.scroll,40,10))
					if resources.HELP == True: pygame.draw.rect(self.scr[0], (140,255,124), pygame.Rect(75,y - self.scroll,40,10))
				#TEXT
				if i == 0:
					txt = resources.LANG
				elif i == 1:	
					if resources.SPEED == 5: txt = database.MENU[91]
					if resources.SPEED == 4: txt = database.MENU[92]
					if resources.SPEED == 3: txt = database.MENU[93]
					if resources.SPEED == 2: txt = database.MENU[94]
					if resources.SPEED == 1: txt = database.MENU[95]
				else: txt = ''
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[inpts[i]] + ': ' + txt, True, (0,0,0)), (10, (y + ty - 2 - self.scroll) * 2))
				y += hz + sp
		#AUDIO MENU
		if mnu == 2:
			self.scroll = 0
			inpts = (resources.SFX,resources.MSC)
			for i in range(2):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
				pygame.draw.rect(self.scr[0], (110, 110, 110), pygame.Rect(bs + (inpts[i] * (bw - 10)),y + ty - self.scroll,20,bh))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[63 + i], True, (0,0,0)), (10, (y + ty - 2 - self.scroll)* 2))
				y += hz + sp
		#CONTROLS MENU
		if mnu == 3:
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

			ctrls = (resources.UP,resources.DOWN,resources.LEFT,resources.RIGHT,resources.ACT,resources.RUN,resources.PHONE,resources.BAG)
			for i in range(7):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				if trg == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				elif opt == i: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp

		pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[13], True, (0, 0, 0)), (10, 10))

		return self.scr

	def info(self, opt):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[0].get_width() #button width
		pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,45,sz - 10,195))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[0], True, (0, 0, 0)), (80, 110))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[1], True, (0, 0, 0)), (30, 160))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[2], True, (0, 0, 0)), (30, 190))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[3], True, (0, 0, 0)), (30, 220))

		if opt == 0: pygame.draw.rect(self.scr[0], (193, 193, 193), pygame.Rect(5,139,sz - 10,20))
		else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,139,sz - 10,20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[4], True, (0, 0, 0)), (20, 286))
		if opt == 1: pygame.draw.rect(self.scr[0], (193, 193, 193), pygame.Rect(5,160,sz - 10,20))
		else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(5,160,sz - 10,20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[5], True, (0, 0, 0)), (20, 328))

		self.scr[1].blit(self.fnt['CALIBRI'].render(database.ABOUT[6], True, (0, 0, 0)), (40, 400))

		pygame.draw.rect(self.scr[1], (193, 193, 193), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(database.MENU[14], True, (0, 0, 0)), (10, 10))

		return self.scr

	def call(self, opt, nb):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[1].get_width() #button width
		num = 0
		for i in database.NUMBERS:
			if i[1] == nb: break
			num += 1
		self.scr[0].blit(pygame.image.load('Backgrounds/call_' + nb + '.png'), (0, 90))
		pygame.draw.rect(self.scr[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,0,sz,90))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.NUMBERS[num][0], True, (255, 255, 255)), (100, 20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(nb, True, (255, 255, 255)), (100, 40))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[32] + str(resources.CREDIT), True, (255, 255, 255)), (100, 80))
		self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[33], True, (255, 255, 255)), (100, 120))

		if opt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_ys.png'), (40, 40)), (25, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_ys.png'), (30, 190))
		if opt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_no.png'), (40, 40)), (sz - 55, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_no.png'), (sz - 50, 190))

		return self.scr
