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
				resources.MONEY = int(self.cmd[6:])
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
				resources.PARTY[resources.FORMATION] = [int(self.cmd[6]),int(self.cmd[7]),int(self.cmd[8]),int(self.cmd[9])]
			elif self.cmd == 'health':
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
		self.fnt = pygame.font.Font('Fonts/monotype.ttf', 15)
		self.ch_sfx = pygame.mixer.Channel(1)
		self.ch_ton = pygame.mixer.Channel(2)
		self.wdw = pygame.Surface((200, 200))
		pygame.draw.rect(self.wdw, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,0,200,200))
		for x in range(20):
			for y in range(20):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))
		self.show = False
		self.scr = [pygame.Surface((180,180))]
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
					if self.pressed[resources.LEFT]: self.lopt = 0; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.RIGHT]: self.lopt = 1; self.ch_sfx.play(resources.SOUND['MENU_HOR'])
					if self.pressed[resources.ACT]:
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
		self.scr[0].fill((0,0,0))

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
				resources.new_data()
				for i in range(len(self.name)):
					resources.CHARACTERS[i]['NAME'] = self.name[i]
					resources.CHARACTERS[i]['LASTNAME'] = self.lame[i]
				resources.save_data()
				resources.save_sett()
				resources.party_make(0)
				resources.recent_data(2)
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
			if self.lopt == 0: self.scr[0].blit(self.fnt.render(database.MENU[80] + ': ' + self.name[self.ind] + self.bt, True, (255, 255, 0)), (80 - l1, 30))
			else: self.scr[0].blit(self.fnt.render(database.MENU[80] + ': ' + self.name[self.ind], True, (255, 255, 255)), (80 - l1, 30))
			if self.lopt == 1: self.scr[0].blit(self.fnt.render(database.MENU[81] + ': '+ self.lame[self.ind] + self.bt, True, (255, 255, 0)), (80 - l2, 50))
			else: self.scr[0].blit(self.fnt.render(database.MENU[81] + ': '+ self.lame[self.ind], True, (255, 255, 255)), (80 - l2, 50))
		else:
			self.scr[0].blit(self.fnt.render(database.MENU[82], True, (255, 255, 255)), (50, 10))
			y = 0
			for i in range(len(self.name)):
				self.scr[0].blit(self.fnt.render(self.name[i] + ' ' + self.lame[i], True, (255, 255, 255)), (10, 30 + (20 * y)))
				y += 1

			if self.lopt == 0: self.scr[0].blit(self.fnt.render(database.MENU[83], True, (255, 255, 0)), (50, 160))
			else: self.scr[0].blit(self.fnt.render(database.MENU[83], True, (255, 255, 255)), (50, 160))
			if self.lopt == 1: self.scr[0].blit(self.fnt.render(database.MENU[84], True, (255, 255, 0)), (100, 160))
			else: self.scr[0].blit(self.fnt.render(database.MENU[84], True, (255, 255, 255)), (100, 160))


		self.wdw.blit(self.scr,(10,10))
		return self.wdw

class Inventory:
	def __init__(self):
		self.fnt = pygame.font.Font('Fonts/PrestigeEliteStd.otf', 10)
		self.wdw = pygame.Surface((400, 300))
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

		self.scr = [pygame.Surface((380,220))]
		self.itmov = ''
		self.money = False
		self.scroll = 50
		self.strgscroll = 50
		self.shake = 0
		self.arrow = 0
		self.arrdir = False

	def find(self, where, item):
		fnd = None
		if where != None:
			for y in database.INVENTORY[where]:
				for x in y:
					if x[0] == item and fnd == None: fnd = x
		else:
			for i in database.INVENTORY:
				for y in i:
					for x in y:
						if x[0] == item and fnd == None: fnd = x

		return fnd

	def add(self, where, item, prp='0000'):
		i = 0
		j = 0
		trigg = False
		for y in database.INVENTORY[where]:
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
						database.INVENTORY[where][j][i] = [item,vi,'_','_']
						trigg = True
					i += 1
			j += 1
			i = 0

	def space(self, where, ex=0, opt=None, lopt=None):
		i = 0
		j = 0
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
		for y in database.INVENTORY[where]:
			if j != 4:
				for x in y:
					if x[0] != '_' and i!= 0:
						vlm += database.ITEMS[x[0]][3]
						wei += database.ITEMS[x[0]][4]
						if database.INVENTORY[where][4][0][0] != '_':
							if vlm > database.ITEMS[database.INVENTORY[where][4][0][0]][3]: trigg = False
							if wei > database.ITEMS[database.INVENTORY[where][4][0][0]][4]: trigg = False
					i += 1
			j += 1
			i = 0

		if lopt == 4: trigg = True
		elif opt == 0: trigg = True
		if database.INVENTORY[where][4][0][0] == '_': trigg = True
		return trigg

	def show(self, opt, lopt, mn, ex, tp):
		self.scr[0].fill((0,0,0))
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
			self.scr[1].blit(self.fnt.render(resources.CHARACTERS[n]['NAME'], True, (255, 255, 255)), (20 + (200 * mnc) - self.scroll, 20))
			for j in range(len(database.INVENTORY[n])):
				if opty == 4: y += 5
				for i in database.INVENTORY[n][j]:
					if optx == 1: x += 5

					trigg = False
					if optx == 0 or opty == 4: trigg = True
					elif database.INVENTORY[mnc][4][0][0] != '_': trigg = True

					if trigg == True:
						if opt == optx and lopt == opty and mn == mnc:
							if tp == 0: pygame.draw.rect(self.scr, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x + (200 * mnc) - self.scroll,y,30,30))
							if tp == 1: pygame.draw.rect(self.scr, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x,y + (210 * mnc) - self.scroll,30,30))
							dscr = database.INVENTORY[resources.PARTY[resources.FORMATION][mn]][lopt][opt][0]
						else:
							if tp == 0: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(x + (200 * mnc) - self.scroll,y,30,30))
							if tp == 1: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(x,y + (210 * mnc) - self.scroll,30,30))
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
				self.scr[1].blit(self.fnt.render(database.MENU[78] + ':', True, (255, 255, 255)), (75 + 200 * mnc - self.scroll, 10))
				pygame.draw.rect(self.scr, (100, 100, 100), pygame.Rect(115 + (200 * mnc) - self.scroll,12,50,10))
				if vlm > 0 and database.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(115 + (200 * mnc) - self.scroll,12,int(50/(database.ITEMS[database.INVENTORY[mnc][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt.render(database.MENU[79] + ':', True, (255, 255, 255)), (75 + (200 * mnc) - self.scroll, 25))
				pygame.draw.rect(self.scr, (100, 100, 100), pygame.Rect(115 + (200 * mnc) - self.scroll,27,50,10))
				if wei > 0 and database.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(115 + (200 * mnc) - self.scroll,27,int(50/(database.ITEMS[database.INVENTORY[mnc][4][0][0]][4]/wei)),10))
			if tp == 1:
				self.scr[1].blit(self.fnt.render(database.MENU[78] + ':', True, (255, 255, 255)), (75, 10 + (210 * mnc) - self.scroll))
				pygame.draw.rect(self.scr, (100, 100, 100), pygame.Rect(115,12 + (210 * mnc) - self.scroll,50,10))
				if vlm > 0 and database.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(115,12 + (210 * mnc) - self.scroll,int(50/(database.ITEMS[database.INVENTORY[mnc][4][0][0]][3]/vlm)),10))
				self.scr[1].blit(self.fnt.render(database.MENU[79] + ':', True, (255, 255, 255)), (75, 25 + (210 * mnc) - self.scroll))
				pygame.draw.rect(self.scr, (100, 100, 100), pygame.Rect(115,27 + (210 * mnc) - self.scroll,50,10))
				if wei > 0 and database.INVENTORY[mnc][4][0][0] != '_': pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(115,27 + (210 * mnc) - self.scroll,int(50/(database.ITEMS[database.INVENTORY[mnc][4][0][0]][4]/wei)),10))

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

			self.scr[1].blit(self.fnt.render('Depositar', True, (255, 255, 255)), (210, 10 - self.strgscroll))
			for j in database.STORAGE:
				if optx == 10:
					x = 210
					y += 32
					optx = 5
					opty += 1

				if opt == optx and lopt == opty:
					pygame.draw.rect(self.scr, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(x, y - self.strgscroll,30,30))
					dscr = j[0]
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(x, y - self.strgscroll,30,30))
				if j[0] != '_':
					self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + j[0] + '.png'), (x, y - self.strgscroll))
				x += 32
				optx += 1

		#DESCRIPTION
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
				if self.money == True:
					self.scr[0].blit(self.mnbor, (-35 + (mn * 200) + ox - self.scroll + self.shake,35 + lox))
					pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(-30 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,50,30))
					self.scr[1].blit(self.fnt.render('$' + str(resources.MONEY), True, (255, 255, 255)), (-25 + (mn * 200) + ox - self.scroll + self.shake,45 + lox))

				if ex == 1: pygame.draw.rect(self.scr, (255,255,255), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				else: pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 2: pygame.draw.rect(self.scr, (255,255,255), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				else: pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if ex == 3: pygame.draw.rect(self.scr, (255,255,255), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				else: pygame.draw.rect(self.scr, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
				if self.itmov[1] != '_': self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[1] + '.png'), (25 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				if self.itmov[2] != '_': self.scr[0].blit(pygame.image.load('Sprites/Items/it_' + self.itmov[2] + '.png'), (55 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				self.scr[0].blit(pygame.image.load('Sprites/e_run.png'), (85 + (mn * 200) + ox - self.scroll + self.shake,40 + lox))
				if ex < 3: dscr = self.itmov[ex]
				else: dscr = '_'
		
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

		self.wdw.blit(self.scr, (10,10))

		#ITEM DESCRIPTION
		pygame.draw.rect(self.wdw, (0, 0, 0), pygame.Rect(10,240,380,50))
		if dscr != '_':
			y = 0
			for t in database.ITEMS[dscr][1]:
				self.wdw.blit(self.fnt.render(t, True, (255, 255, 255)), (20, 250 + y))
				y += 15

		if self.shake > 0: self.shake = -self.shake
		elif self.shake < 0: self.shake = -self.shake - 1
		return self.wdw

class Shop:
	def __init__(self):
		self.fnt = pygame.font.Font('Fonts/monotype.ttf', 10)
		self.pxf = pygame.font.Font('Fonts/pixel-font.ttf', 20)
		self.dtt = pygame.font.Font('Fonts/datetype.ttf', 10)
		self.wdw = pygame.Surface((400, 250))
		pygame.draw.rect(self.wdw, (resources.COLOR[0],resources.COLOR[1],resources.COLOR[2]), pygame.Rect(0,0,400,250))
		for x in range(40):
			for y in range(25):
				self.wdw.blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (x * 10, y * 10))
		self.scr = [pygame.Surface((380,230))]
		
	def products(self, opt, lopt, lst):
		self.scr[0].fill((10,10,10))

		self.scr[0].blit(self.fnt.render('$' + str(resources.MONEY), True, (255, 255, 255)), (20, 10))

		y = 0
		for i in lst:
			if lopt == y:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,33 + (y * 12),370,12))
				self.scr[0].blit(self.fnt.render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (0, 0, 0)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt.render(str(opt) + 'x', True, (0, 0, 0)), (360, 30 + (y * 12)))
			else:
				self.scr[0].blit(self.fnt.render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, 30 + (y * 12)))
				self.scr[0].blit(self.fnt.render(str(opt) + 'x', True, (255, 255, 255)), (360, 30 + (y * 12)))
			y += 1

		if lopt != len(lst):
			l = 0
			for j in database.ITEMS[lst[lopt]][1]:
				self.scr[0].blit(self.fnt.render(j, True, (255, 255, 255)), (20,200 + (l * 10)))
				l += 1

		if lopt == y:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,33 + (y * 12),370,12))
			self.scr[0].blit(self.fnt.render(database.SHOP[1], True, (0, 0, 0)), (20, 30 + (y * 12)))
		else: self.scr[0].blit(self.fnt.render(database.SHOP[1], True, (255, 255, 255)), (20, 30 + (y * 12)))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def buy(self, opt, lopt, lst):
		self.scr[0].fill((10,10,10))

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
				self.scr[0].blit(self.fnt.render('$' + str(database.ITEMS[i][2]) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, 25 + (y * 15)))
				cost += database.ITEMS[i][2]
				y += 1

		self.scr[0].blit(self.fnt.render('valor: ' + str(resources.MONEY), True, (255, 255, 255)), (305, 165))
		self.scr[0].blit(self.fnt.render('total: ' + str(cost), True, (255, 255, 255)), (305, 185))
		if resources.MONEY - cost > 0: pcol = (0,255,0)
		else: pcol = (255,0,0)
		self.scr[0].blit(self.fnt.render('troco: ' + str(resources.MONEY - cost), True, pcol), (305, 205))
		self.scr[0].blit(self.fnt.render('atendente: ', True, (255, 255, 255)), (10, 230))
		self.scr[0].blit(self.fnt.render('hora: ' + str(resources.TIME[0]) + ': ' + str(resources.TIME[1]), True, (255, 255, 255)), (200, 230))
		self.scr[0].blit(self.fnt.render('data: ' + str(resources.DATE[0]) + '/ ' + str(resources.DATE[1]), True, (255, 255, 255)), (300, 230))

		if lopt == 0:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,204,300,12))
			self.scr[0].blit(self.fnt.render(database.SHOP[0], True, (0,0,0)), (10, 201))
		else: self.scr[0].blit(self.fnt.render(database.SHOP[0], True, (255, 255, 255)), (10, 201))

		if lopt == 1:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,216,300,12)); tcol = (0,0,0)
			self.scr[0].blit(self.fnt.render(database.SHOP[7], True, (0, 0, 0)), (10, 213))
		else: self.scr[0].blit(self.fnt.render(database.SHOP[7], True, (255, 255, 255)), (10, 213))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def mercator(self, opt, lopt, lst, prm):
		self.scr[0].fill((10,10,10))

		self.scr[0].blit(self.fnt.render('$' + str(resources.MONEY), True, (255, 255, 255)), (20, 10))

		if opt == 0: self.scr[0].blit(self.fnt.render(database.SHOP[8], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20, 30))
		else: self.scr[0].blit(self.fnt.render(database.SHOP[8], True, (255,255,255)), (20, 30))
		x = 1
		for i in resources.PARTY[resources.FORMATION]:
			if opt == x: self.scr[0].blit(self.fnt.render(resources.CHARACTERS[i]['NAME'], True, (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2])), (20 + (x * 60), 30))
			else: self.scr[0].blit(self.fnt.render(resources.CHARACTERS[i]['NAME'], True, (255,255,255)), (20 + (x * 60), 30))
			x += 1

		y = 0
		for i in lst:
			if opt == 0:
				if prm > 0:
					prc = database.ITEMS[i][2] - int(database.ITEMS[i][2]/prm)
				else: prc = database.ITEMS[i][2]
				if lopt == y:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,50 + (y * 15),370,15))
					self.scr[0].blit(self.fnt.render('$' + str(prc) + ' - ' + database.ITEMS[i][0], True, (0, 0, 0)), (20, 50 + (y * 15)))
				else:
					self.scr[0].blit(self.fnt.render('$' + str(prc) + ' - ' + database.ITEMS[i][0], True, (255, 255, 255)), (20, 50 + (y * 15)))
				if prm > 0:
					pygame.draw.rect(self.scr, (255, 170, 0), pygame.Rect(350,50 + (y * 15),30,20))
					self.scr[0].blit(self.dtt.render(str(prm) + '%', True, (255, 255, 255)), (350, 50 + (y * 15)))
				y += 1
			elif i[0] == resources.PARTY[resources.FORMATION][opt - 1]:
				if lopt == y:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,50 + (y * 15),370,15))
					self.scr[0].blit(self.fnt.render('$' + str(int(database.ITEMS[database.INVENTORY[i[0]][i[1]][i[2]][0]][2]/2)) + ' - ' + database.ITEMS[database.INVENTORY[i[0]][i[1]][i[2]][0]][0], True, (0, 0, 0)), (20, 50 + (y * 15)))
				else:
					self.scr[0].blit(self.fnt.render('$' + str(int(database.ITEMS[database.INVENTORY[i[0]][i[1]][i[2]][0]][2]/2)) + ' - ' + database.ITEMS[database.INVENTORY[i[0]][i[1]][i[2]][0]][0], True, (255, 255, 255)), (20, 50 + (y * 15)))
				y += 1

		if lopt != len(lst):
			l = 0
			if opt == 0:
				for j in database.ITEMS[lst[lopt]][1]:
					self.scr[0].blit(self.fnt.render(j, True, (255, 255, 255)), (20,200 + (l * 15)))
					l += 1
			else:
				for t in database.ITEMS[database.INVENTORY[lst[lopt][0]][lst[lopt][1]][lst[lopt][2]][0]][1]:
					self.scr[0].blit(self.fnt.render(t, True, (255, 255, 255)), (20,200 + (l * 15)))
					l += 1

		if lopt == y:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(15,50 + (y * 15),370,15))
			self.scr[0].blit(self.fnt.render(database.SHOP[1], True, (0, 0, 0)), (20, 50 + (y * 15)))
		else: self.scr[0].blit(self.fnt.render(database.SHOP[1], True, (255, 255, 255)), (20, 50 + (y * 15)))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

	def bank(self, opt, lopt, mn, ext):
		self.scr[0].fill((234,234,234))

		if mn == 3:
			if lopt == 0:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,120,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[5], True, (0,0,0)), (10, 120))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,120,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[5], True, (0, 0, 0)), (10, 120))

			if lopt == 1:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[6], True, (0, 0, 0)), (10, 160))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,160,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[6], True, (0, 0, 0)), (10, 160))

			if lopt == 2:
				pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[7], True, (0, 0, 0)), (10, 200))
			else:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,200,200,30))
				self.scr[0].blit(self.pxf.render(database.SHOP[7], True, (0, 0, 0)), (10, 200))

		else:
			pygame.draw.rect(self.scr, (94, 137, 255), pygame.Rect(80,80,200,110))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,90,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,120,130,27))
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(110,150,130,27))
			pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(120 + opt * 6,135,5,2))

			self.scr[0].blit(self.pxf.render(str(resources.ATM), True, (0,0,0)), (120, 90))
			self.scr[0].blit(self.pxf.render(str(ext[0]) + str(ext[1]) + str(ext[2]) + str(ext[3]) + str(ext[4]) + str(ext[5]), True, (0,0,0)), (120, 120))
			self.scr[0].blit(self.pxf.render(str(resources.MONEY), True, (0,0,0)), (120, 150))

		self.wdw.blit(self.scr, (10,10))
		return self.wdw

class Phone:
	def __init__(self):
		self.scr = [pygame.Surface((232,232)), pygame.Surface((464,464), pygame.SRCALPHA)]
		self.fnt = pygame.font.Font('Fonts/monotype.ttf', 10)
		self.ttl = pygame.font.Font('Fonts/pixel-font.ttf', 25)
		self.dtt = pygame.font.Font('Fonts/datetype.ttf', 8)
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30)}
		self.pbg = resources.PARTY[resources.FORMATION][0]
		self.scroll = 0
		self.mp = None

	def bar(self, sg):
		self.bsc = pygame.Surface((self.scr[0].get_width(),18))
		self.bsc.fill((10,10,10))
		dvd3 = math.floor(self.scr[0].get_width()/3)

		day = ['','','']
		if resources.DATE[0] < 10: day[0] = '0' + str(resources.DATE[0])
		else: day[0] = str(resources.DATE[0])
		if resources.DATE[1] < 10: day[1] = '0' + str(resources.DATE[1])
		else: day[1] = str(resources.DATE[1])
		if resources.DATE[2] < 10: day[2] = '0' + str(resources.DATE[2])
		else: day[2] = str(resources.DATE[2])
		self.bsc.blit(self.dtt.render(day[0] + '/' + day[1] + '/' + day[2], True, (255, 255, 255)), (3, 4))

		hour = ['','']
		if resources.TIME[0] < 10: hour[0] = '0' + str(resources.TIME[0])
		else: hour[0] = str(resources.TIME[0])
		if resources.TIME[1] < 10: hour[1] = '0' + str(resources.TIME[1])
		else: hour[1] = str(resources.TIME[1])
		self.bsc.blit(self.dtt.render(hour[0] + ':' + hour[1], True, (255, 255, 255)), (dvd3 + 30, 4))

		self.bsc.blit(pygame.image.load('Sprites/signal_' + str(sg) + '.png'), ((dvd3 * 3) - 47, 6))
		self.bsc.blit(pygame.image.load('Sprites/battery.png'), ((dvd3 * 3) - 30, 2))
		if resources.BATTERY > 100.0: pygame.draw.rect(self.bsc, (255, 255, 255), pygame.Rect((dvd3 * 3) - 7 - int(18/(360/resources.BATTERY)),5,int(18/(360/resources.BATTERY)),7))
		elif resources.BATTERY > 1.0: pygame.draw.rect(self.bsc, (255, 10, 10), pygame.Rect((dvd3 * 3) - 7 - int(18/(360/resources.BATTERY)),5,int(18/(360/resources.BATTERY)),7))

		return self.bsc

	def apps(self, opt, lopt):
		self.scr[0].fill((0,0,0))

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
		if mn == False: scr = pygame.Surface((self.scr.get_width(),232))
		if mn == True: scr = pygame.Surface((100,100))
		scr.fill((0,0,0))
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
			scr.blit(pygame.transform.scale(self.mp, (zoom,zoom)), (mpx,mpy))

			xx = (pl['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
			yy = (pl['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
			scr.blit(pygame.image.load('Sprites/mp_player.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in resources.MARKER:
				xx = (i[1] - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i[2] - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				#if i[0] == rm:
				scr.blit(pygame.image.load('Sprites/mp_pin.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in sig:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				scr.blit(pygame.image.load('Sprites/mp_' + i['ICON'] + '.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
			for i in en:
				xx = (i['RECT'].x - 15) * self.mp.get_width()/(rm.width * rm.tilewidth)
				yy = (i['RECT'].y - 15) * self.mp.get_height()/(rm.height * rm.tileheight)
				if i['HP'] > 0 and i['RECT'].x > 0 and i['RECT'].y > 0:
					scr.blit(pygame.image.load('Sprites/mp_anomaly.png'), (mpx + ((zoom/self.mp.get_width()) * xx),mpy + ((zoom/self.mp.get_height()) * yy)))
		else: scr.blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 200))

		if mn == False:
			pygame.draw.rect(scr, (140, 255, 253), pygame.Rect(0,0,self.scr.get_width(),40))
			scr.blit(self.ttl.render(database.MENU[0], True, (0, 0, 0)), (5, 4))

		return scr

	def contacts(self, flt, opt, mnu):
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

		self.scr.fill((10,10,10))
		y = 0
		for i in em:
			if opt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),50))
			else: pygame.draw.rect(self.scr, (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),50))

			if flt > 0: self.scr[0].blit(self.fnt.render(i[0], True, (0, 0, 0)), (10, 76 + y - self.scroll))
			else:
				if opt == y/51:
					if mnu == 1: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(118,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load('Sprites/tc_9.png'), (self.scr.get_width() - 44, 76 + y - self.scroll))
					if mnu == 2: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(140,74 + y - self.scroll,24,24))
					self.scr[0].blit(pygame.image.load('Sprites/tc_8.png'), (self.scr.get_width() - 22, 76 + y - self.scroll))
					if mnu == 3: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(8,74 + y - self.scroll,24,24))
					if mnu == 4: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,74 + y - self.scroll,24,24))
					if mnu == 5: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(52,74 + y - self.scroll,24,24))

				x = 0
				for p in i:
					self.scr[0].blit(pygame.image.load('Sprites/who_' + str(p) + '.png'), (10 + x, 76 + y - self.scroll))
					x += 22

			if flt == 0: self.scr[0].blit(self.fnt.render('grupo ' + str(int((y + 51)/51)), True, (0, 0, 0)), (10, 96 + y - self.scroll))
			if flt == 1: self.scr[0].blit(self.fnt.render(i[1], True, (0, 0, 0)), (10, 86 + y - self.scroll))
			if flt == 2: self.scr[0].blit(pygame.image.load('Sprites/who_' + str(i[1]).lower() + '.png'), (160, 86 + y - self.scroll))
			y += 51
		if flt == 0:
			if opt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),50))
			else: pygame.draw.rect(self.scr, (15, 255, 0), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),50))
			self.scr[0].blit(self.fnt.render(database.MENU[31], True, (0, 0, 0)), (10, 76 + y - self.scroll))
		if y == 0 and flt == 1:
			self.scr[0].blit(self.fnt.render(database.MENU[16], True, (255, 255, 255)), (50, 140))

		dvd3 = math.floor(self.scr.get_width()/3)
		if flt == 0:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[23], True, (0, 0, 0)), (8, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[23], True, (255, 255, 255)), (8, 47))
		if flt == 1:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[24], True, (0, 0, 0)), (dvd3 + 10, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[24], True, (255, 255, 255)), (dvd3 + 10, 47))
		if flt == 2:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[25], True, (0, 0, 0)), ((dvd3 * 2) + 10, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[25], True, (255, 255, 255)), ((dvd3 * 2) + 10, 47))

		pygame.draw.rect(self.scr, (15, 255, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[1], True, (0, 0, 0)), (5, 5))

		return self.scr

	def email(self, flt, opt, mnu, sg):
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

		self.scr.fill((10,10,10))
		if sg > 0:
			if mnu == 0:
				self.scroll = 0
				if opt > 2: self.scroll += (opt - 2) * 51

				y = 0
				for i in em:
					if opt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),50))
					else: pygame.draw.rect(self.scr, (255, 221, 0), pygame.Rect(0,66 + y,self.scr.get_width(),50))
					self.scr[0].blit(self.fnt.render(i[1], True, (0, 0, 0)), (10, 76 + y - self.scroll))
					self.scr[0].blit(self.fnt.render(i[0], True, (0, 0, 0)), (10, 86 + y - self.scroll))
					y += 51
				if y == 0:
					self.scr[0].blit(self.fnt.render(database.MENU[19], True, (255, 255, 255)), (255, 140))

				dvd3 = math.floor(self.scr.get_width()/3)
				if flt == 0:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,45,dvd3,20))
					self.scr[0].blit(self.fnt.render(database.MENU[26], True, (0, 0, 0)), (12, 47))
				else: self.scr[0].blit(self.fnt.render(database.MENU[26], True, (255, 255, 255)), (12, 47))
				if flt == 1:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
					self.scr[0].blit(self.fnt.render(database.MENU[27], True, (0, 0, 0)), (dvd3 + 15, 47))
				else: self.scr[0].blit(self.fnt.render(database.MENU[27], True, (255, 255, 255)), (dvd3 + 15, 47))
				if flt == 2:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
					self.scr[0].blit(self.fnt.render(database.MENU[28], True, (0, 0, 0)), ((dvd3 * 2) + 12, 47))
				else: self.scr[0].blit(self.fnt.render(database.MENU[28], True, (255, 255, 255)), ((dvd3 * 2) + 12, 47))

			elif mnu > 0:
				self.scroll = (mnu - 1) * 3
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,45,self.scr.get_width() - 10,200))
				self.scr[0].blit(self.fnt.render(em[opt][1], True, (0, 0, 0)), (15, 55 - self.scroll))
				self.scr[0].blit(self.fnt.render(database.MENU[34] + em[opt][0], True, (0, 0, 0)), (15, 85 - self.scroll))
				self.scr[0].blit(self.fnt.render(database.MENU[35] + (resources.CHARACTERS[resources.PARTY[0][0]]['NAME'] + resources.CHARACTERS[resources.PARTY[0][0]]['LASTNAME']).lower() + '@cmail.com', True, (0, 0, 0)), (15, 100 - self.scroll))
				y = 0
				for l in em[opt][2]:
					self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (15, 130 + y - self.scroll))
					y += 15
		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 200))

		pygame.draw.rect(self.scr, (255, 221, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[2], True, (0, 0, 0)), (5, 5))

		return self.scr

	def news(self, opt, mnu, sg):
		self.scr.fill((10,10,10))
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
						if opt != opty: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50 + y + hei))
						else: pygame.draw.rect(self.scr, (219, 49, 37), pygame.Rect(0,41 + y,self.scr.get_width(),50 + y + hei))

						yi = 0
						for l in i[0]:
							self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (10, 46 + y - self.scroll + yi))
							yi += 15

						self.scr[0].blit(self.fnt.render(i[1], True, (0, 0, 0)), (10, 52 + y - self.scroll + yi))
					elif i[0] == 1:
						pygame.draw.rect(self.scr, (219, 49, 37), pygame.Rect(0,41 + (y * hei),self.scr.get_width(),50 + (y * hei)))
						self.scr[0].blit(self.fnt.render(i[1][0], True, (0, 0, 0)), (10, 46 + (y * hei) - self.scroll))
						self.scr[0].blit(self.fnt.render(i[1][1], True, (0, 0, 0)), (10, 56 + (y * hei) - self.scroll))
					y += hei
					opty += 1
					hei = 0

			elif mnu > 0:
				self.scroll = (mnu - 1) * 3
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,45,self.scr.get_width() - 10,200))
				y = 0
				for l in database.NEWS[resources.DATE[0] - 1][opt][0]:
					self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (10, 50 + y - self.scroll))
					y += 15
				self.scr[0].blit(self.fnt.render(database.NEWS[resources.DATE[0] - 1][opt][1], True, (0, 0, 0)), (10, 55 + y - self.scroll))
				for l in database.NEWS[resources.DATE[0] - 1][opt][2]:
					self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (10, 100 + y - self.scroll))
					y += 15
		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr, (219, 49, 37), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[3], True, (0, 0, 0)), (5, 5))

		return self.scr

	def radio(self, fm, msc):
		self.scr.fill((10,10,10))
		if resources.RADIO[str(math.floor(fm/20))] != []:
			pygame.draw.rect(self.scr, (255, 0, 135), pygame.Rect(0,66,self.scr.get_width(),50))
			self.scr[0].blit(self.fnt.render(resources.RADIO[str(math.floor(fm/20))][msc][:-4], True, (0, 0, 0)), (10, 76))
		else: self.scr[0].blit(self.fnt.render(database.MENU[20], True, (255, 255, 255)), (70, 140))

		pygame.draw.rect(self.scr, (10, 10, 10), pygame.Rect(0,40,self.scr.get_width(),26))
		f = 0
		sp = math.floor(self.scr.get_width()/9)
		for i in range(9):
			pygame.draw.line(self.scr, (255, 255, 255), (0 + f,50),(0 + f,65),1)
			pygame.draw.line(self.scr, (255, 255, 255), (round(sp/2) + f,55),(round(sp/2) + f,65),1)
			f += sp
		pygame.draw.rect(self.scr, (255, 0, 0), pygame.Rect(0 + fm,50,4,16))
		self.scr[0].blit(self.fnt.render(str(fm/10), True, (255, 255, 255)), (70, 20))

		pygame.draw.rect(self.scr, (255, 0, 135), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[4], True, (0, 0, 0)), (5, 5))

		return self.scr

	def camera(self, opt, sg):
		self.scr.fill((10,10,10))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[5], True, (0, 0, 0)), (5, 5))

		if sg > 0:
			y = 0
			print(resources.FILES)
			for i in range(len(resources.FILES[1])):
				if opt != y: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + (y * 51),self.scr.get_width(),50))
				else: pygame.draw.rect(self.scr, (255, 255, 10), pygame.Rect(0,41 + (y * 51),self.scr.get_width(),50))
				self.scr[0].blit(self.fnt.render(database.CHAPTERS[resources.FILES[1][i]][0], True, (0, 0, 0)), (10, 51 + (y * 51)))
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
				self.scr[0].blit(self.fnt.render(hh + ' : ' + mm + ' : ' + ss, True, (0, 0, 0)), (10, 61 + (y * 51)))
				y += 1

			if opt != y: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + (y * 51),self.scr.get_width(),50))
			else: pygame.draw.rect(self.scr, (255, 255, 10), pygame.Rect(0,41 + (y * 51),self.scr.get_width(),50))
			self.scr[0].blit(self.fnt.render(database.MENU[61], True, (0, 0, 0)), (10, 51 + (y * 51)))

		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		return self.scr

	def bestiary(self, opt, lopt, mnu, sg):
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		self.scr.fill((10,10,10))
		if sg > 0:
			if len(resources.BESTIARY) > 0:
				if mnu == 0:
					y = 0
					for i in resources.BESTIARY:
						if i['SEEN'] > 0:
							if lopt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
							else: pygame.draw.rect(self.scr, (134, 0, 211), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
							self.scr[0].blit(self.fnt.render(database.FREAKS[i['N']]['NAME'], True, (0, 0, 0)), (10, 51 + y - self.scroll))
							y += 51

				if mnu == 1:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,45,170,200))
					pygame.draw.rect(self.scr, (134, 0, 211), pygame.Rect(5,243,83,3))
					self.scr[0].blit(self.fnt.render(database.FREAKS[resources.BESTIARY[opt]['N']]['NAME'], True, (0, 0, 0)), (10, 55))
					self.scr[0].blit(pygame.image.load('Sprites/' + resources.BESTIARY[opt]['N'] + '_stand.png'), (60, 70))
					self.scr[0].blit(self.fnt.render('ID: ' + resources.BESTIARY[opt]['ID'], True, (0, 0, 0)), (20, 160))
					self.scr[0].blit(self.fnt.render('RG: ' + resources.BESTIARY[opt]['DATE'], True, (0, 0, 0)), (60, 160))
					self.scr[0].blit(self.fnt.render('HG: ' + database.FREAKS[resources.BESTIARY[opt]['N']]['HEIGHT'], True, (0, 0, 0)), (110, 160))

					j = 0
					for l in database.FREAKS[resources.BESTIARY[opt]['N']]['INFO']:
						self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (10, self.scr.get_width() + j))
						j += 15

				if mnu == 2:
					pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,45,self.scr.get_width() - 10,200))
					pygame.draw.rect(self.scr, (134, 0, 211), pygame.Rect(92,243,83,3))
					pygame.draw.rect(self.scr, (0, 0, 0), pygame.Rect(10,50,160,77))

					y = 0
					for i in database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES']:
						if lopt != y/19: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(11,51 + y,158,18))
						else: pygame.draw.rect(self.scr, (134, 0, 211), pygame.Rect(11,51 + y,158,18))
						self.scr[0].blit(self.fnt.render(i[0], True, (0, 0, 0)), (20, 53 + y))
						y += 19

					j = 0
					for l in database.FREAKS[resources.BESTIARY[opt]['N']]['HABILITIES'][lopt][1]:
						self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (10, 140 + j))
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

					self.scr[0].blit(self.fnt.render(dmg, True, (0, 0, 0)), (20, 210))
			else: self.scr[0].blit(self.fnt.render(database.MENU[21], True, (255, 255, 255)), (10, 140))
		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr, (134, 0, 211), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[6], True, (0, 0, 0)), (5, 5))

		return self.scr

	def task(self, flt, opt, mnu):
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
			
		self.scr.fill((10,10,10))
		y = 0
		for i in em:
			if opt != y/31: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),30))
			else: pygame.draw.rect(self.scr, (255, 123, 0), pygame.Rect(0,66 + y - self.scroll,self.scr.get_width(),30))
			self.scr[0].blit(self.fnt.render(i[0], True, (0, 0, 0)), (10, 73 + y - self.scroll))
			y += 31
		if y == 0:
			self.scr[0].blit(self.fnt.render(database.MENU[22], True, (255, 255, 255)), (45, 140))

		dvd3 = math.floor(self.scr.get_width()/3)
		if flt == 0:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[29], True, (0, 0, 0)), (12, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[29], True, (255, 255, 255)), (12, 47))
		if flt == 1:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[30], True, (0, 0, 0)), (dvd3 + 15, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[30], True, (255, 255, 255)), (dvd3 + 15, 47))
		if flt == 2:
			pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(dvd3 * 2,45,dvd3,20))
			self.scr[0].blit(self.fnt.render(database.MENU[28], True, (0, 0, 0)), ((dvd3 * 2) + 12, 47))
		else: self.scr[0].blit(self.fnt.render(database.MENU[28], True, (255, 255, 255)), ((dvd3 * 2) + 12, 47))

		pygame.draw.rect(self.scr, (255, 123, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[7], True, (0, 0, 0)), (5, 5))

		return self.scr

	def status(self, opt):
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 60

		self.scr.fill((10,10,10))

		x = 0
		dvd4 = math.floor(self.scr.get_width()/4)
		for i in resources.PARTY[resources.FORMATION]:
			if opt == x/dvd4:
				pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0 + x - self.scroll,45,dvd4,20))
				self.scr[0].blit(self.fnt.render(resources.CHARACTERS[i]['NAME'], True, (0, 0, 0)), (8 + x - self.scroll, 47))
			else: self.scr[0].blit(self.fnt.render(resources.CHARACTERS[i]['NAME'], True, (255, 255, 255)), (8 + x - self.scroll, 47))
			x += dvd4

		self.scr[0].blit(pygame.image.load('Sprites/who_' + str(resources.PARTY[resources.FORMATION][opt]) + '.png'), (10, 74))
		self.scr[0].blit(self.fnt.render(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['NAME'] + ' ' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LASTNAME'], True, (255, 255, 255)), (35, 76))
		self.scr[0].blit(self.fnt.render(str(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ID']), True, (255, 255, 255)), (10, 96))
		self.scr[0].blit(pygame.image.load('Sprites/gn_' + resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['GENDER'] + '.png'), (70, 96))
		self.scr[0].blit(self.fnt.render(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['BLOOD'], True, (255, 255, 255)), (50, 96))

		self.scr[0].blit(self.fnt.render('level ' + str(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']), True, (255, 255, 255)), (10, 115))
		self.scr[0].blit(self.fnt.render('hp:', True, (255, 255, 255)), (10, 130))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,135,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['HP'] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,135,int(100/(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['VITALITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']]/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['HP'])),10))
		self.scr[0].blit(self.fnt.render('xp:', True, (255, 255, 255)), (10, 145))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,150,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['XP'] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,150,int(100/(resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['MAXXP']/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['XP'])),10))
		self.scr[0].blit(self.fnt.render('st:', True, (255, 255, 255)), (10, 160))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,165,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['STRENGHT'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,165,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['STRENGHT'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[0].blit(self.fnt.render('at:', True, (255, 255, 255)), (10, 175))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,180,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ATTACK'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,180,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['ATTACK'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[0].blit(self.fnt.render('ag:', True, (255, 255, 255)), (10, 190))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,195,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['AGILITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,195,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['AGILITY'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))
		self.scr[0].blit(self.fnt.render('rs:', True, (255, 255, 255)), (10, 205))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(30,210,100,10))
		if resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['RESISTANCE'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']] > 0:
			pygame.draw.rect(self.scr, (0, 255, 0), pygame.Rect(30,210,int(100/(100/resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['RESISTANCE'][resources.CHARACTERS[resources.PARTY[resources.FORMATION][opt]]['LEVEL']])),10))

		pygame.draw.rect(self.scr, (255, 0, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[8], True, (0, 0, 0)), (5, 5))

		return self.scr

	def tactics(self, opt, lopt, mnu, sg):
		self.scroll = 0
		if lopt > 2: self.scroll += (lopt - 2) * 51

		self.scr.fill((10,10,10))
		if sg > 0:
			y = 0
			for i in resources.TACTICAL:
				if i != [] and len(i) == 4:
					if lopt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
					else: pygame.draw.rect(self.scr, (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))

					if mnu > 0 and lopt == y/51:
						if mnu < 5:
							pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(8 + (mnu - 1) * 22,49 + y - self.scroll,24,24))
							if i[mnu - 1] == 1: self.scr[0].blit(self.fnt.render(database.MENU[54], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 2: self.scr[0].blit(self.fnt.render(database.MENU[55], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 3: self.scr[0].blit(self.fnt.render(database.MENU[56], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 4: self.scr[0].blit(self.fnt.render(database.MENU[57], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 5: self.scr[0].blit(self.fnt.render(database.MENU[58], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 6: self.scr[0].blit(self.fnt.render(database.MENU[59], True, (0, 0, 0)), (10, 70 + y - self.scroll))
							if i[mnu - 1] == 7: self.scr[0].blit(self.fnt.render(database.MENU[60], True, (0, 0, 0)), (10, 70 + y - self.scroll))
						else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(self.scr.get_width() - 42,49 + y - self.scroll,24,24))
						self.scr[0].blit(pygame.image.load('Sprites/tc_8.png'), (self.scr.get_width() - 40, 51 + y - self.scroll))

					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[0]) + '.png'), (10, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[1]) + '.png'), (32, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[2]) + '.png'), (54, 51 + y - self.scroll))
					self.scr[0].blit(pygame.image.load('Sprites/tc_' + str(i[3]) + '.png'), (76, 51 + y - self.scroll))
				y += 51

			if lopt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
			else: pygame.draw.rect(self.scr, (33, 75, 127), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
			self.scr[0].blit(self.fnt.render(database.MENU[36], True, (0, 0, 0)), (20, 50 + y - self.scroll))

		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr, (33, 75, 127), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[9], True, (0, 0, 0)), (5, 5))

		return self.scr

	def achievements(self, opt, sg):
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		self.scr.fill((10,10,10))
		if sg > 0:
			y = 0
			for i in database.ACHIEVEMENTS:
				if opt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
				else: pygame.draw.rect(self.scr, (255, 191, 0), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))

				if i[2] == True: tcol = (0,0,0)
				else: tcol = (80,80,80)
				self.scr[0].blit(self.fnt.render(i[0], True, tcol), (10, 51 + y - self.scroll))
				self.scr[0].blit(self.fnt.render(i[1], True, tcol), (10, 65 + y - self.scroll))
				y += 51

		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr, (255, 191, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[10], True, (0, 0, 0)), (5, 5))

		return self.scr

	def ranking(self, opt, sg):
		self.scroll = 0
		if opt > 2: self.scroll += (opt - 2) * 51

		self.scr.fill((10,10,10))
		if sg > 0: pass
		else: self.scr[0].blit(self.fnt.render(database.MENU[15], True, (255, 255, 255)), (25, 140))

		pygame.draw.rect(self.scr, (55, 255, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[11], True, (0, 0, 0)), (5, 5))
		pygame.draw.rect(self.scr, (10, 10, 10), pygame.Rect(0,40,self.scr.get_width(),210))

		return self.scr

	def help(self, opt, mnu):
		self.scr.fill((10,10,10))
		if mnu == 0:
			self.scroll = 0
			if opt > 2: self.scroll += (opt - 2) * 51
			y = 0
			for i in database.MANUAL:
				if opt != y/51: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
				else: pygame.draw.rect(self.scr, (137, 50, 0), pygame.Rect(0,41 + y - self.scroll,self.scr.get_width(),50))
				self.scr[0].blit(self.fnt.render(i[0], True, (0, 0, 0)), (10, 51 + y - self.scroll))
				y += 51

		if mnu > 0:
			self.scroll = (mnu - 1) * 3
			pygame.draw.rect(self.scr,(255, 255, 255), pygame.Rect(5,45,170,200))
			self.scr[0].blit(self.fnt.render(database.MANUAL[opt][0], True, (0, 0, 0)), (70, 55 - self.scroll))
			y = 0
			for l in database.MANUAL[opt][1]:
				self.scr[0].blit(self.fnt.render(l, True, (0, 0, 0)), (15, 80 + y - self.scroll))
				y += 15

		pygame.draw.rect(self.scr, (137, 50, 0), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[12], True, (0, 0, 0)), (5, 5))

		return self.scr

	def settings(self, opt, mnu, trg):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[1].get_width() #button width
		hz = 30 #button height
		sp = 1 #scroll speed
		bw = 110 #bar width
		bh = 10 #bar height
		bs = 60
		y = 41
		ty = 5

		if mnu == 0:
			self.scroll = 0
			inpts = (88,89,90,76)
			for i in range(4):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[inpts[i]], True, (0,0,0)), (10, ((y * 2) + (ty * 2)) - self.scroll))
				y += hz + sp

			'''if opt == 0: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,41 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,41 - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[88], True, (0,0,0)), (10, 49 - self.scroll))

			if opt == 1: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,72 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,72 - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[89], True, (0,0,0)), (10, 80 - self.scroll))

			if opt == 2: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,103 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,103 - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[90], True, (0,0,0)), (10, 111 - self.scroll))

			if opt == 3: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,134 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,134 - self.scroll,sz,30))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[76], True, (0,0,0)), (10, 142 - self.scroll))'''

		if mnu == 1:
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

			if opt == 0: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,41 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,41 - self.scroll,sz,hz))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[62] + ': ' + resources.LANG, True, (0,0,0)), (10, 51 - self.scroll))

			if opt == 1: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,72 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,72 - self.scroll,sz,hz))
			if resources.SPEED == 5: txt = database.MENU[91]
			if resources.SPEED == 4: txt = database.MENU[92]
			if resources.SPEED == 3: txt = database.MENU[93]
			if resources.SPEED == 2: txt = database.MENU[94]
			if resources.SPEED == 1: txt = database.MENU[95]
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[72] + ': ' + txt, True, (0,0,0)), (10, 82 - self.scroll))
			
			if opt == 2: pygame.draw.rect(self.scr[1], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,103 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,103 - self.scroll,sz,hz))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(60,113 - self.scroll,bw,bh))
			pygame.draw.rect(self.scr[1], (110,110,110), pygame.Rect(60 + int(100/(242/resources.COLOR[0])),113 - self.scroll,10,10))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[73] + ':', True, (0,0,0)), (10, 111 - self.scroll))

			if opt == 3: pygame.draw.rect(self.scr[1], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,134 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,134 - self.scroll,sz,hz))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(60,144 - self.scroll,bw,bh))
			pygame.draw.rect(self.scr[1], (110,110,110), pygame.Rect(60 + int(100/(242/resources.COLOR[1])),144 - self.scroll,10,10))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[74] + ':', True, (0,0,0)), (10, 142 - self.scroll))

			if opt == 4: pygame.draw.rect(self.scr[1], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,165 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,165 - self.scroll,sz,hz))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(60,175 - self.scroll,bw,bh))
			pygame.draw.rect(self.scr[1], (110,110,110), pygame.Rect(60 + int(100/(242/resources.COLOR[2])),175 - self.scroll,10,10))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[75] + ':', True, (0,0,0)), (10, 171 - self.scroll))

			if opt == 5: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,196 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,196 - self.scroll,sz,hz))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[87] + ': ', True, (0,0,0)), (10, 204 - self.scroll))
			pygame.draw.rect(self.scr[1], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(60,196 - self.scroll,sz - 40,hz))
			for i in range(math.floor(sz/10) - 4):
				for y in range(3): self.scr[0].blit(pygame.image.load('Sprites/border_' + str(resources.BORDER) + '.png'), (60 + i * 10, 196 + (y * 10) - self.scroll))

			if opt == 6: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,227 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,227 - self.scroll,sz,hz))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(75,237 - self.scroll,80,10))
			if resources.CENSORSHIP == False: pygame.draw.rect(self.scr[1], (255,61,61), pygame.Rect(115,237 - self.scroll,40,10))
			if resources.CENSORSHIP == True: pygame.draw.rect(self.scr[1], (140,255,124), pygame.Rect(75,237 - self.scroll,40,10))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[96] + ': ', True, (0,0,0)), (10, 233 - self.scroll))

			if opt == 7: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,258 - self.scroll,sz,hz))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,258 - self.scroll,sz,hz))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(75,268 - self.scroll,80,10))
			if resources.HINT == False: pygame.draw.rect(self.scr[1], (255,61,61), pygame.Rect(115,268 - self.scroll,40,10))
			if resources.HINT == True: pygame.draw.rect(self.scr[1], (140,255,124), pygame.Rect(75,268 - self.scroll,40,10))
			self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[97] + ': ', True, (0,0,0)), (10, 264 - self.scroll))

		if mnu == 2:
			self.scroll = 0
			inpts = (resources.SFX,resources.MSC)
			for i in range(2):
				if opt == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
				pygame.draw.rect(self.scr[0], (110, 110, 110), pygame.Rect(bs + (inpts[i] * (bw - int(bw/10))),y + ty - self.scroll,20,bh))
				self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[63 + i], True, (0,0,0)), (10, ((y * 2) + (ty * 2)) - 2 - self.scroll))
				y += hz + sp

			'''if opt == 0: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,41 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,41 - self.scroll,sz,30))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(60,51 - self.scroll,110,10))
			pygame.draw.rect(self.scr[1], (110, 110, 110), pygame.Rect(60 + (resources.SFX * 100),51 - self.scroll,10,10))
			self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[63], True, (0,0,0)), (10, 49 - self.scroll))

			if opt == 1: pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,72 - self.scroll,sz,30))
			else: pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,72 - self.scroll,sz,30))
			pygame.draw.rect(self.scr[1], (210, 210, 210), pygame.Rect(60,82 - self.scroll,110,10))
			pygame.draw.rect(self.scr[1], (110, 110, 110), pygame.Rect(60 + (resources.MSC * 100),82 - self.scroll,10,10))
			self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[64], True, (0,0,0)), (10, 80 - self.scroll))'''

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
				if trg == 0: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, ((y * 2) + (ty * 2)) - self.scroll))
				elif opt == i: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, ((y * 2) + (ty * 2)) - self.scroll))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(database.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, ((y * 2) + (ty * 2)) - self.scroll))
				y += hz + sp

				'''
				if opt == 0: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,41 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,41 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[65] + ': ' + pygame.key.name(resources.UP[0]), True, (0,0,0)), (10, 51 - self.scroll))
				elif opt == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 51 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[65] + ': ' + pygame.key.name(resources.UP[0]), True, (0,0,0)), (10, 51 - self.scroll))

				if opt == 1: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,72 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,72 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[66] + ': ' + pygame.key.name(resources.DOWN[0]), True, (0,0,0)), (10, 82 - self.scroll))
				elif opt == 1: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 82 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[66] + ': ' + pygame.key.name(resources.DOWN[0]), True, (0,0,0)), (10, 82 - self.scroll))

				if opt == 2: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,103 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,103 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[67] + ': ' + pygame.key.name(resources.LEFT[0]), True, (0,0,0)), (10, 113 - self.scroll))
				elif opt == 2: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 113 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[67] + ': ' + pygame.key.name(resources.LEFT[0]), True, (0,0,0)), (10, 113 - self.scroll))
				
				if opt == 3: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,134 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,134 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[68] + ': ' + pygame.key.name(resources.RIGHT[0]), True, (0,0,0)), (10, 144 - self.scroll))
				elif opt == 3: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 144 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[68] + ': ' + pygame.key.name(resources.RIGHT[0]), True, (0,0,0)), (10, 144 - self.scroll))
				
				if opt == 4: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,165 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,165 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[69] + ': ' + pygame.key.name(resources.ACT[0]), True, (0,0,0)), (10, 175 - self.scroll))
				elif opt == 4: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 175 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[69] + ': ' + pygame.key.name(resources.ACT[0]), True, (0,0,0)), (10, 175 - self.scroll))

				if opt == 5: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,196 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,196 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[86] + ': ' + pygame.key.name(resources.RUN[0]), True, (0,0,0)), (10, 206 - self.scroll))
				elif opt == 5: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 206 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[86] + ': ' + pygame.key.name(resources.RUN[0]), True, (0,0,0)), (10, 206 - self.scroll))
				
				if opt == 6: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,227 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,227 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[70] + ': ' + pygame.key.name(resources.PHONE[0]), True, (0,0,0)), (10, 237 - self.scroll))
				elif opt == 6: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 237 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[70] + ': ' + pygame.key.name(resources.PHONE[0]), True, (0,0,0)), (10, 237 - self.scroll))
				
				if opt == 7: pygame.draw.rect(self.scr, (91, 91, 91), pygame.Rect(0,258 - self.scroll,sz,30))
				else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(0,258 - self.scroll,sz,30))
				if trg == 0: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[71] + ': ' + pygame.key.name(resources.BAG[0]), True, (0,0,0)), (10, 268 - self.scroll))
				elif opt == 7: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[77], True, (0,0,0)), (10, 268 - self.scroll))
				else: self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[71] + ': ' + pygame.key.name(resources.BAG[0]), True, (0,0,0)), (10, 268 - self.scroll))'''

		pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,0,sz,40))
		self.scr[1].blit(self.ttl.render(database.MENU[13], True, (0, 0, 0)), (5, 5))

		return self.scr

	def info(self, opt):
		self.scr.fill((10,10,10))
		pygame.draw.rect(self.scr, (193, 193, 193), pygame.Rect(0,0,self.scr.get_width(),40))
		self.scr[0].blit(self.ttl.render(database.MENU[14], True, (0, 0, 0)), (5, 5))
		pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,45,self.scr.get_width() - 10,195))
		self.scr[0].blit(self.fnt.render(database.ABOUT[0], True, (0, 0, 0)), (40, 55))
		self.scr[0].blit(self.fnt.render(database.ABOUT[1], True, (0, 0, 0)), (15, 80))
		self.scr[0].blit(self.fnt.render(database.ABOUT[2], True, (0, 0, 0)), (15, 95))
		self.scr[0].blit(self.fnt.render(database.ABOUT[3], True, (0, 0, 0)), (15, 110))

		if opt == 0: pygame.draw.rect(self.scr, (193, 193, 193), pygame.Rect(5,139,self.scr.get_width() - 10,20))
		else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,139,self.scr.get_width() - 10,20))
		self.scr[0].blit(self.fnt.render(database.ABOUT[4], True, (0, 0, 0)), (10, 143))
		if opt == 1: pygame.draw.rect(self.scr, (193, 193, 193), pygame.Rect(5,160,self.scr.get_width() - 10,20))
		else: pygame.draw.rect(self.scr, (255, 255, 255), pygame.Rect(5,160,self.scr.get_width() - 10,20))
		self.scr[0].blit(self.fnt.render(database.ABOUT[5], True, (0, 0, 0)), (10, 164))

		self.scr[0].blit(self.fnt.render(database.ABOUT[6], True, (0, 0, 0)), (20, 200))

		return self.scr

	def call(self, opt, nb):
		num = 0
		for i in database.NUMBERS:
			if i[1] == nb: break
			num += 1
		self.scr[0].blit(pygame.image.load('Backgrounds/call_' + nb + '.png'), (0, 90))
		pygame.draw.rect(self.scr[0], (resources.COLOR[0], resources.COLOR[1], resources.COLOR[2]), pygame.Rect(0,0,self.scr[0].get_width(),90))
		self.scr[0].blit(self.fnt['CALIBRI'].render(database.NUMBERS[num][0], True, (255, 255, 255)), (50, 10))
		self.scr[0].blit(self.fnt['CALIBRI'].render(nb, True, (255, 255, 255)), (50, 20))
		self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[32] + str(resources.CREDIT), True, (255, 255, 255)), (50, 40))
		self.scr[0].blit(self.fnt['CALIBRI'].render(database.MENU[33], True, (255, 255, 255)), (50, 60))

		if opt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_ys.png'), (40, 40)), (25, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_ys.png'), (30, 190))
		if opt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load('Sprites/cl_no.png'), (40, 40)), (self.scr[0].get_width() - 55, 185))
		else: self.scr[0].blit(pygame.image.load('Sprites/cl_no.png'), (self.scr[0].get_width() - 50, 190))

		return self.scr
