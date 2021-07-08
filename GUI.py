# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3
import resources as res
import random
import pygame
import plyer
import math
import sys
import os

if res.FILES[3] != []:
	if res.FILES[3][0] == 'PT': import database_PT as dtb
	if res.FILES[3][0] == 'EN': import database_EN as dtb
else: import database_PT as dtb
import resources as res

class Guitools:
	def digitstring(self,number,digits):
		value = ''
		for i in range(digits):
			if len(str(number)) == i:
				add = ''
				for d in range(digits - i):
					add += '0'
				value = add + str(number)
		if value == '': return str(number)
		else: return value
		
	def align(self,input,value):
		xx = math.floor(input.x/value[0]) * value[0]
		yy = math.floor(input.y/value[1]) * value[1]
		return (xx,yy)
	
	def get_tiles(self):
		tlsz = (30,30)
		tilset = os.listdir(res.TILES_PATH)
		tilset.remove('files')
		tilset.sort()
		srf = pygame.Surface(tlsz)
		srf.fill((0,0,0))
		tls = [srf]
		for t in tilset:
			tst = pygame.image.load(res.TILES_PATH + t)
			for y in range(int(tst.get_height()/tlsz[1])):
				for x in range(int(tst.get_width()/tlsz[0])):
					rct = pygame.Rect(x * tlsz[0],y * tlsz[1],tlsz[0],tlsz[1])
					tls.append(tst.subsurface(rct).copy())
		return tls
	
	def wrap(self,text,font,width):
		txt = []
		t = ''
		for y in text:
			if isinstance(y,int):
				if t != '': t += ' '
				t += res.CHARACTERS[y]['NAME']
			elif y == '':
				txt.append(t)
				txt.append('')
				t = ''
			else:
				for w in y.split():
					if font.size(t + ' ' + w)[0] > width:
						txt.append(t)
						t = ' ' + w
					elif w in [':','.','?','!']: t += w
					else: t += ' ' + w
		txt.append(t)
		return txt

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
							res.save_data(0)
							res.save_data(1)
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
						else: self.ton.play(res.SOUND['TEXT_ENTER']); self.ind += 1; self.lopt = 0; self.tim = 3; self.did = 0
			else:
				self.sfx.play(res.SOUND['FILE_NEW'])
				for i in range(len(self.name)):
					res.CHARACTERS[i]['NAME'] = self.name[i]
					res.CHARACTERS[i]['LASTNAME'] = self.lame[i]
				res.save_data(0)
				res.save_data(1)
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
		self.pos = [0,0]
		self.fnt = {'DEFAULT': pygame.font.Font(res.FONTS_PATH + res.FONT, 12 * res.GSCALE),'PRICE': pygame.font.Font(res.FONTS_PATH + res.FONT, 6 * res.GSCALE),
		'ALT': pygame.font.Font(res.FONTS_PATH + 'PrestigeEliteStd.otf', 10)}
		self.guitools = Guitools()
		self.allowlimit = False
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		if srf != False:
			self.window = (srf[0],srf[1])
			ww = srf[0] * 0.9
			if ww < 300: ww = 300
			self.wdw = pygame.Surface((ww, 300), pygame.SRCALPHA)
			self.wdw.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(math.ceil(self.wdw.get_width()/10)):
				for y in range(math.ceil(self.wdw.get_height()/10)):
					self.wdw.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
			self.itbor = pygame.Surface((130, 40))
			self.itbor.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(13):
				for y in range(4):
					self.itbor.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10,y * 10))
			'''self.mnbor = pygame.Surface((60, 40))
			self.mnbor.fill((res.COLOR[0],res.COLOR[1],res.COLOR[2]))
			for x in range(6):
				for y in range(4):
					self.mnbor.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (1 + (x * 10),1 + (y * 10)))'''
			self.scr = [pygame.Surface((self.wdw.get_width() - 20,self.wdw.get_height() - 80)),pygame.Surface(((self.wdw.get_width() - 20) * res.GSCALE,(self.wdw.get_height() - 20) * res.GSCALE), pygame.SRCALPHA)]
			self.dsrf = pygame.Surface((self.scr[0].get_width(),50))
			self.fade = srf[0] + 400
		self.whl = pygame.Surface((60,60),pygame.SRCALPHA)
		self.srf = None
		self.rqst = True
		self.hld = 0
		self.spn = 0
		self.itmov = ''
		self.type = 0
		self.opt = [0,0,0,0]
		self.scroll = 0
		self.strgscroll = 50
		self.shake = 0
		self.arrow = 0
		self.arrdir = False
		self.optrects = []
		self.doneimages = {}
		self.exzoom = 0
		self.tilset = self.guitools.get_tiles()
		x = 10
		y = 45
		for u in range(len(res.PARTY[res.FORMATION])):
			self.optrects.append([])
			for j in range(5):
				self.optrects[u].append([])
				if j == 4: y += 5
				for i in range(5):
					if i == 1: x += 5
					self.optrects[u][j].append((pygame.Rect(x + (200 * u),y,30,30),pygame.Rect(x,y + (210 * u),30,30),
					pygame.Rect(x,y + (210 * u),30,30),pygame.Rect(x,y + (210 * u),30,30),pygame.Rect(x + (200 * u),y,30,30),
					pygame.Rect(x,y + (200 * u),30,30),pygame.Rect(x,y + (200 * u),30,30)))
					x += 32
				x = 10
				y += 32
			x = 10
			y = 45
			
	def dev(self,d=None):
		if d == None:
			it = res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][0]
		else: it = d
		if it == 'phone': dv = Apps(0)
		elif it == 'PDA': dv = Apps(1)
		elif it == 'mp3': dv = 'radio'
		else:
			try: dv = getattr(sys.modules[__name__], it)
			except: dv = None
		if dv != None:
			bt = int(res.INVENTORY[res.SHORTCUT[0]][res.SHORTCUT[1]][res.SHORTCUT[2]][1])
		else: bt = 0
		
		return [dv,bt]

	def find(self, where, item, act='item'):
		if isinstance(item,list): fnd = []
		else: fnd = None
		for i in range(len(res.INVENTORY)):
			able = True
			if where != None:
				if i == where: able = True
				else: able = False
			else: able = True
			if able == True:
				yy = 0
				for y in res.INVENTORY[i]:
					xx = 0
					for x in y:
						for it in range(len(x[::2])):
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
						res.INVENTORY[where][j][i] = [item,vi]
						trigg = True
					i += 1
			j += 1
			i = 0

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
				if int(i[1][0:2]) <= res.DATE[0]:
					i[0] += '_wasted'
		elif i[0].startswith('drink') and i[0].endswith('wasted') == False:
			if int(i[1][2:4]) <= res.DATE[1]:
				if int(i[1][0:2]) <= res.DATE[0]:
					i[0] += '_wasted'
		elif i[0].startswith('clth'):
			if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
			if int(i[1]) == 0: res.CHARACTERS[u]['HEALTH'] = 3
		elif i[0].startswith('grenade') and int(i[1]) > 0:
			if int(i[1]) > 0: i[1] = str(int(i[1]) - 1)
			if int(i[1]) == 0:
				self.sfx.play(res.SOUND['HIT'])
				res.CHARACTERS[u]['HP'] -= dtb.ITEMS[i[0]][5]['DAMAGE']
		elif i[0] == 'cigar' and float(i[1]) > 0:
			if float(i[1]) > 0: i[1] = str(float(i[1]) - 0.2)
		
	def itimg(self,it):
		img = None
		if it in self.doneimages: img = self.doneimages[it]
		elif it.startswith('til'):
			img = self.tilset[dtb.ITEMS[it][5]]
		elif it.startswith('clth') or it.startswith('tool_lighter') or it.startswith('bottle'):
			img = pygame.image.load(res.ITEMS_PATH + it[:-1] + '.png')
			img.fill(res.PALETTES[2][int(it[-1]) - 1],None,pygame.BLEND_RGBA_MULT)
		elif it.endswith('_wasted'):
			img = pygame.image.load(res.ITEMS_PATH + it.replace('_wasted','') + '.png')
			img.fill((50,50,50),None,pygame.BLEND_RGBA_MULT)
		elif it != '_':
			if it.startswith('bed'):
				img = pygame.image.load(res.ITEMS_PATH + 'bed.png')
				if it.endswith('single'):
					ad = pygame.image.load(res.ITEMS_PATH + 'wS.png')
				if it.endswith('couple'):
					ad = pygame.image.load(res.ITEMS_PATH + 'wC.png')
				img.blit(ad,(img.get_width() - ad.get_width() - 1, 1))
			else:
				nrml = False
				for i in ['cage','tent']:
					if it.startswith(i):
						img = pygame.image.load(res.ITEMS_PATH + i + '.png')
						if it.endswith('big'): ad = pygame.image.load(res.ITEMS_PATH + 'wB.png')
						if it.endswith('medium'): ad = pygame.image.load(res.ITEMS_PATH + 'wM.png')
						if it.endswith('small'): ad = pygame.image.load(res.ITEMS_PATH + 'wP.png')
						img.blit(ad,(img.get_width() - ad.get_width() - 1, 1))
						nrml = True
				if nrml == False: img = pygame.image.load(res.ITEMS_PATH + it + '.png')
		self.doneimages[it] = img
		return img
		
	def wheel(self):
		self.whl.fill((0,0,0,0))
		pygame.draw.circle(self.whl,(0,0,0),(30,30),30)
		self.spn += int((self.spn - (self.opt[0] * 2))/5)
		a = int(self.spn)
		for i in res.INVENTORY[res.PARTY[res.FORMATION][0]][4][1:]:
			xx = int(math.cos(a) * 5) + 30
			yy = int(math.sin(a) * 5) + 30
			if self.opt[0] == a - 1:
				pygame.draw.arc(self.whl,(res.COLOR[0],res.COLOR[1],res.COLOR[2]),pygame.Rect(0,0,60,60),a,a + 1)
			if i[0] != '_': self.whl.blit(self.itimg(i[0]),(xx,yy))
			a += 1
		return self.whl
		
	def bar(self,where,row,column,orientation):
		lst = []
		if isinstance(row,tuple):
			for x in res.INVENTORY[where][row[0]:row[1]]: lst.append(x[column])
		if isinstance(column,tuple):
			lst = res.INVENTORY[where][row][column[0]:column[1]]
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
		self.rqst = False
		for i in self.scr: i.fill((0,0,0,0))
		self.dsrf.fill((0,0,0))
		mnc = 0
		dscr = '_'
		#SCROLL
		if self.type == 1:
			if self.scroll < (self.opt[2] * 200):
				self.scroll += 40
			if self.scroll > (self.opt[2] * 200):
				self.scroll -= 40
		if self.type == 2:
			if self.scroll < (self.opt[2] * 210):
				self.scroll += 42
			if self.scroll > (self.opt[2] * 210):
				self.scroll -= 42
		if self.scroll < 0: self.scroll = 0
		#INVENTORY FOR EACH ONE IN THE PARTY
		if self.type != 6:
			for n in res.PARTY[res.FORMATION]:
				optx = 0
				opty = 0
				vlm = 0
				wei = 0
				for j in range(len(res.INVENTORY[n])):
					for i in range(len(res.INVENTORY[n][j])):
						#CHECK BAG
						trigg = False
						if optx == 0 or opty == 4: trigg = True
						elif res.INVENTORY[n][4][0][0] != '_': trigg = True
						#DRAW RECTS
						if self.opt[0] == optx and self.opt[1] == opty and self.opt[2] == mnc:
							cl = (res.COLOR[0],res.COLOR[1],res.COLOR[2])
							dscr = res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]]
						elif res.SHORTCUT[0] == n and res.SHORTCUT[1] == opty and res.SHORTCUT[2] == optx:
							cl = (255,255,167)
						elif res.INVENTORY[n][j][i][0].endswith('_wasted'):
							cl = (176,255,182)
						elif res.INVENTORY[n][j][i][0].startswith('clth_') and int(res.INVENTORY[n][j][i][1]) == 0:
							cl = (176,255,182)
						else: cl = (255,255,255)
						rct = self.optrects[n][j][i][self.type - 1].copy()
						if self.type in [1,5]: rct.x = self.optrects[mnc][j][i][self.type - 1].x - self.scroll
						else: rct.y = self.optrects[mnc][j][i][self.type - 1].y - self.scroll
						if trigg == True:
							pygame.draw.rect(self.scr[0],cl,rct)
						elif self.opt[0] == optx and self.opt[1] == opty and self.opt[2] == mnc:
							pygame.draw.rect(self.scr[0],cl,rct)
						#ITEM DURATION
						for dr in [['tube',(10,200,10),5],['bottle',(100,100,200),5],['vest',(153,153,153),6],['cigar',(153,153,153),500],
						['gun',(255,183,183),'CAPACITY'],['phone',(255,226,173),3600]]:
							if res.INVENTORY[n][j][i][0].startswith(dr[0]) and float(res.INVENTORY[n][j][i][1]) > 1.0:
								if self.opt[0] != optx or self.opt[1] != opty or self.opt[2] != mnc:
									if isinstance(dr[2],str): dv = dtb.ITEMS[res.INVENTORY[n][j][i][0]][5][dr[2]]
									elif dr[2] >= 500: dv = int(dr[2])
									else: dv = dtb.ITEMS[res.INVENTORY[n][j][i][0]][dr[2]]
									drct = rct.copy()
									drct.height = int(rct.height/(dv/float(res.INVENTORY[n][j][i][1])))
									drct.y += rct.height - drct.height
									pygame.draw.rect(self.scr[0],dr[1],drct)
						#DRAW SPRITES
						if trigg == True:
							if res.INVENTORY[n][j][i][0] != '_':
								img = self.itimg(res.INVENTORY[n][j][i][0])
								self.scr[0].blit(img, (rct.x,rct.y))
								if optx > 0 and opty < 4:
									vlm += dtb.ITEMS[res.INVENTORY[n][j][i][0]][3]
									wei += dtb.ITEMS[res.INVENTORY[n][j][i][0]][4]
						optx += 1
					optx = 0
					opty += 1
				#VOLUME AND WEIGHT
				lst = [['VOLUME',vlm],['WEIGHT',wei]]
				sz = self.fnt['DEFAULT'].size(res.CHARACTERS[n]['NAME'])[0]
				if self.type in [1,5]:
					pos = [[(93 + (210 * mnc) - self.scroll,10),(93 + (210 * mnc) - self.scroll,25),(15 + (210 * mnc) - self.scroll, 20)],
					[((55 + (210 * mnc) - self.scroll) * res.GSCALE, 15 * res.GSCALE),((55 + (210 * mnc) - self.scroll) * res.GSCALE, 30 * res.GSCALE),(((40 + (210 * mnc) - self.scroll) * res.GSCALE) - sz, 15 * res.GSCALE)]]
				else:
					pos = [[(93,10 + (210 * mnc) - self.scroll),(93,25 + (210 * mnc) - self.scroll),(15, 20 + (210 * mnc) - self.scroll)],
					[(55 * res.GSCALE, (15 + (210 * mnc) - self.scroll) * res.GSCALE),(55 * res.GSCALE, (30 + (210 * mnc) - self.scroll) * res.GSCALE),((40 * res.GSCALE) - sz, (15 + (210 * mnc) - self.scroll) * res.GSCALE)]]
				if self.allowlimit:
					for i in range(2):
						self.scr[1].blit(self.fnt['DEFAULT'].render(dtb.ITINFO[lst[i][0]], True, (255, 255, 255)), pos[1][i])
						pygame.draw.rect(self.scr[0], (100, 100, 100), pygame.Rect(pos[0][i][0],pos[0][i][1],80,10))
						if vlm > 0 and res.INVENTORY[n][4][0][0] != '_':
							pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(pos[0][i][0],pos[0][i][1],int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/lst[i][1])),10))
							if self.itmov != '' and self.itmov[0] != 0:
								pygame.draw.rect(self.scr[0], (200, 10, 10), pygame.Rect(pos[0][i][0] + int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/lst[i][1])),pos[0][i][1],int(80/(dtb.ITEMS[res.INVENTORY[n][4][0][0]][3]/dtb.ITEMS[self.itmov[0]][3])),10))
				self.scr[1].blit(self.fnt['DEFAULT'].render(res.CHARACTERS[n]['NAME'], True, (255, 255, 255)),pos[1][2])
				self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(n) + '.png'),pos[0][2])
				mnc += 1
		#OTHER SCROLL
		if self.opt[1] > 5:
			if self.strgscroll < (self.opt[1] * 32):
				self.strgscroll += 8
			if self.strgscroll > (self.opt[1] * 32):
				self.strgscroll -= 8
		else:
			if self.strgscroll > 0:
				self.strgscroll -= 40
		if self.strgscroll < 0: self.strgscroll = 0
		#OTHER INVENTORY
		if self.type > 1:
			if self.type == 6: r = 2; rw = 0
			else: r = 1; rw = 1
			for i in range(r):
				x = (200 * rw)
				y = 45
				optx = 5 * rw
				opty = 0
				itinf = [['STORAGE',res.STORAGE],['BASKET',res.BASKET],['WASH',res.WASH],None,[['PRODUCTS',res.PRODUCTS],['BASKET',res.BASKET]],['MERCATOR',res.PRODUCTS]]
				if self.type != 6: txt = dtb.ITINFO[itinf[self.type - 2][0]]; lst = itinf[self.type - 2][1]
				else: txt = dtb.ITINFO[itinf[self.type - 2][rw][0]]; lst = itinf[self.type - 2][rw][1]
				self.scr[1].blit(self.fnt['DEFAULT'].render(txt, True, (255, 255, 255)), ((x + 5) * res.GSCALE, (15 - self.strgscroll) * res.GSCALE))
				for j in lst:
					if optx == 5 * (rw + 1):
						x = (200 * rw)
						if self.type in [3,6,7]: y += 44
						else: y += 32
						optx = 5 * rw
						opty += 1
					if self.opt[0] == optx and self.opt[1] == opty:
						pygame.draw.rect(self.scr[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(x, y - self.strgscroll,30,30))
						dscr = j
					else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x, y - self.strgscroll,30,30))
					if self.type in [3,6,7]:
						pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(x, y - self.strgscroll + 32,30,10))
						self.scr[1].blit(self.fnt['PRICE'].render('$' + str(j[1]), True, (10,10,10)), ((x + 12) * res.GSCALE, (y + 43 - self.strgscroll) * res.GSCALE))
					if j[0] != '_': self.scr[0].blit(self.itimg(j[0]), (x, y - self.strgscroll))
					x += 32
					optx += 1
				rw += 1
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
				if self.type == 1:
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + 'shade.png'), (14 + (self.opt[2] * 200) + ox - self.scroll,62 + lox))
					self.scr[0].blit(img, (10 + (self.opt[2] * 200) + ox - self.scroll + self.shake,35 + lox))
				else:
					self.scr[0].blit(pygame.image.load(res.ITEMS_PATH + 'shade.png'), (14 + ox,62 + (self.opt[2] * 200) + lox - self.scroll))
					self.scr[0].blit(img, (10 + ox + self.shake,35 + (self.opt[2] * 200) + lox - self.scroll))
			#SUB-ITEMS
			else:
				srf = pygame.Surface((70,40))
				srf.set_alpha(100)
				srf.fill((0, 0, 0))
				self.scr[0].blit(srf, (25 + (self.opt[2] * 200) + ox - self.scroll,40 + lox),pygame.Rect(0,0,10 + (len(self.itmov) * 30),40))
				self.scr[0].blit(self.itbor, (20 + (self.opt[2] * 200) + ox - self.scroll + self.shake,35 + lox),pygame.Rect(0,0,10 + (len(self.itmov) * 30),40))
				for it in range(len(res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]][2::2]) + 1):
					if self.opt[3] == it + 1:
						pygame.draw.rect(self.scr[0], (res.COLOR[0],res.COLOR[1],res.COLOR[2]), pygame.Rect(25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
						if self.opt[3] != len(self.itmov): dscr = [self.itmov[self.opt[3]][0],res.INVENTORY[res.PARTY[res.FORMATION][self.opt[2]]][self.opt[1]][self.opt[0]][it * 2]]
					else: pygame.draw.rect(self.scr[0], (255,255,255), pygame.Rect(25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll + self.shake,40 + lox,30,30))
					if it + 1 == len(self.itmov):
						self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'e_run.png'), (25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll + self.shake,40 + lox))
					elif self.itmov[it + 1][0] != '_':
						img = self.itimg(self.itmov[it + 1][0])
						self.scr[0].blit(img, (25 + (30 * it) + (self.opt[2] * 200) + ox - self.scroll + self.shake,40 + lox))
		#ARROWS
		'''if self.arrdir == False:
			self.arrow += 1
			if self.arrow == 8: self.arrdir = True
		elif self.arrdir == True:
			self.arrow -= 1
			if self.arrow == 0: self.arrdir = False
		if self.type == 1:
			if self.opt[2] > 0: self.scr[0].blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),270), (0 + self.arrow,110))
			if self.opt[2] < len(res.PARTY[res.FORMATION]) - 1: self.scr[0].blit(pygame.transform.rotate(pygame.image.load(res.SPRITES_PATH + 'arw.png'),90), ((self.scr[0].get_width() - 12) - self.arrow,110))
		if self.type == 2:
			if self.opt[2] > 0: self.scr[0].blit(pygame.transform.flip(pygame.image.load(res.SPRITES_PATH + 'arw.png'),False,True), (80,0 + self.arrow))
			if self.opt[2] < len(res.PARTY[res.FORMATION]) - 1: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'arw.png'), (80,208 - self.arrow))'''

		self.wdw.blit(self.scr[0], (10,10))
		#ITEM DESCRIPTION
		if self.itmov != '' and self.opt[3] < len(self.itmov):
			dtp = 1
			if self.itmov[0] != 0:
				for i in ('bag','vest','amulet','melee','gun','grenade'):
					if self.itmov[0].startswith(i):
						dtp = 3
						if dscr[0].startswith(i):
							dtp = 4
			if self.opt[3] != len(self.itmov) and self.itmov[self.opt[3]][0] in res.DISITEMS:
				if res.DISITEMS[self.itmov[0][0]] == 0:
					dtp = 2
			if dtp == 1 and dscr[0] == '_': dtp = 0
		elif dscr[0] != '_': dtp = 1
		else: dtp = 0
		if dtp > 0:
			#ITEM DESCRIPTION
			if dtp == 1:
				txt = dtb.ITEMS[dscr[0]][1].copy()
				if self.type == 3 and self.opt[0] > 4:
					if len(txt) == 1: txt.append('$' + str(dtb.ITEMS[dscr[0]][2] * dscr[1]))
					elif len(txt) == 2: txt[1] += '$' + str(dtb.ITEMS[dscr[0]][2] * dscr[1])
				elif dscr[0].startswith('gun'):
					if len(txt) == 1: txt.append('ammo: ' + str(dscr[1]) + '/' + str(dtb.ITEMS[dscr[0]][5]['CAPACITY']))
					elif len(txt) == 2: txt[1] += ' - ammo: ' + str(dscr[1]) + '/' + str(dtb.ITEMS[dscr[0]][5]['CAPACITY'])
				if dscr[0].startswith('wallet'):
					if len(txt) == 1: txt.append('$' + str(dscr[1][0:6]))
					elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1][0:6])
				if dscr[0].startswith('credit_card'):
					if len(txt) == 1: txt.append('$' + str(dscr[1]))
					elif len(txt) == 2: txt[1] += ' - $' + str(dscr[1])
				if dscr[0].startswith('bottle') and len(dscr) > 2:
					if len(txt) == 1: txt.append(str(dscr[1]) + ': ' + str(dtb.ITEMS[dscr[2]][0]))
					elif len(txt) == 2: txt[1] += ' - ' + str(dscr[1]) + 'm: ' + str(dtb.ITEMS[dscr[2]][0])
				y = 0
				for t in txt:
					if res.DISLEXIC == True:
						out = ''
						for tl in t:
							out += tl + ' '
					else: out = t
					self.scr[1].blit(self.fnt['DEFAULT'].render(out, True, (255, 255, 255)), (80, self.scr[1].get_height() - 80 + y))
					y += 30
			#NOT DISCOVERED
			elif dtp == 2: self.scr[1].blit(self.fnt['DEFAULT'].render(dtb.ITINFO['DISCOVER'], True, (255, 255, 255)), (20, self.scr[1].get_height() - 50))
			#ITEM STATS
			elif dtp > 2 and self.itmov[0] != 0:
				xbr = 0
				ybr = 0
				for p in [
				[['vest','amulet'],'ARMOR',5],
				[['vest','amulet'],'DURATION',6],
				[['tool','melee','gun','grenade'],'DAMAGE',5,'DAMAGE'],
				[['gun'],'CAPACITY',5,'CAPACITY'],
				[['tool','melee','gun'],'RECHARGE',5,'RECHARGE'],
				[['tool','melee','gun'],'CADENCY',5,'CADENCY'],
				[['gun'],'GAUGE',5,'GAUGE'],
				[['food','drink'],'VITALITY',5],
				[['food'],'HUNGER',6],
				[['drink'],'THIRST',6],
				]:
					shw = False
					for n in p[0]:
						if self.itmov[0].startswith(n): shw = True
					if shw:
						if len(p) > 3: it = dtb.ITEMS[self.itmov[0]][p[2]][p[3]]
						else: it = dtb.ITEMS[self.itmov[0]][p[2]]
						self.scr[1].blit(self.fnt['DEFAULT'].render(dtb.ITINFO[p[1]], True, (255, 255, 255)), (80 + (xbr * 200), self.scr[1].get_height() - 80 + (ybr * 30)))
						pygame.draw.rect(self.dsrf,(100,100,100),pygame.Rect(80 + (xbr * 160),10 + (ybr * 20),50,10))
						pygame.draw.rect(self.dsrf,(255,255,255),pygame.Rect(80 + (xbr * 160),10 + (ybr * 20),math.floor(50/it),10))
						if dtp == 4:
							df = math.floor(50/dtb.ITEMS[self.itmov[0]][5]) - math.floor(50/dtb.ITEMS[dscr[0]][5])
							if df != 0:
								if df < 0: pygame.draw.rect(self.dsrf,(200,10,10),pygame.Rect(80 + (xbr * 160) + math.floor(50/it),10 + (ybr * 20),abs(df),10))
								if df > 0: pygame.draw.rect(self.dsrf,(10,200,10),pygame.Rect(80 + (xbr * 160) + math.floor(50/it) - abs(df),10 + (ybr * 20),abs(df),10))
						ybr += 1
						if ybr == 2:
							xbr += 1
							ybr = 0
		#ITEM SHAKE
		if self.shake > 0: self.shake = -self.shake
		elif self.shake < 0: self.shake = -self.shake - 1
		
		self.wdw.blit(self.dsrf,(10,self.wdw.get_height() - 60))
		self.srf = [self.wdw,self.scr[1]]
		
		#RESCALE
		scl1 = res.GSCALE
		scl2 = 1
		if res.GSCALE == 3: scl1 *= 0.75; scl2 = 0.75
		self.srf = [pygame.transform.scale(self.srf[0],(int(self.srf[0].get_rect().width * scl1),int(self.srf[0].get_rect().height * scl1))),pygame.transform.scale(self.srf[1],(int(self.srf[1].get_rect().width * scl2),int(self.srf[1].get_rect().height * scl2)))]

class Vkeyboard:
	def __init__(self,size,type='QWERTY'):
		sz = int((size[0] - (10 * 12))/10)
		sp = 10 + sz
		self.surface = pygame.Surface((size[0],sp * 5.5))
		self.font = pygame.font.SysFont("Arial", 44)
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.type = type
		self.size = size
		self.active = False
		self.caps = 1
		self.page = 0
		self.hold = 0
		self.opt = 0
		self.output = ''
		self.pos = 0
		
		if type == 'QWERTY':
			lst = '1234567890qwertyuiopasdfghjklzxcvbnm, .'
		elif type == 'DVORAK':
			lst = "1234567890',.pyfgcrlaoeuidhtnsjkxbmwvq z"
			
		acclst = [('a','äåæªáãàâ'),('c','ćçč'),('e','ëėēèéêę'),('o','ºōœøöòôóõ'),
		('u','ūùúüû')]
		
		letters = [[],[]]
		for i in lst:
			letters[0].append(str(i))
		for i in '~`|•√π÷×¶∆@#$_&-+()/*"'+"':;!?,.<>={}[]%©®":
			letters[1].append(i)
		for i in letters:
			i.insert(29,1)
			i.insert(37,0)
			i.insert(38,2)
			i.append(3)
		for i in range(len(letters[0])):
			for a in acclst:
				if letters[0][i] == a[0]:
					letters[0][i] = a[0] + a[1]
		self.buttons = [[],[]]
		for p in range(2):
			x = 0
			for i in range(5):
				rr = 10
				add = 0
				if type == 'QWERTY':
					if i in [2,3]: rr = 9
				for j in range(rr):
					if x >= len(letters[p]): break
					pp = 1
					if letters[p][x] == ' ': pp = 6
					if letters[p][x] == 0: pp = 1.5
					if letters[p][x] == 1: pp = 1.5
					if letters[p][x] == 2: pp = 1.5
					if letters[p][x] == 3: pp = 1.5
					self.buttons[p].append([pygame.Rect(add + 20 + (j * sp), 20 + (i * sp),sz * pp,sz),letters[p][x],3])
					if letters[p][x] == ' ': add += sz * 5
					if letters[p][x] == 1: add += sz * 0.5
					if letters[p][x] == 2: add += sz * 0.5
					x += 1
	
	def events(self,event):
		if self.pos == 0: self.output = ''
		if event.type == pygame.MOUSEBUTTONDOWN:
			mp = pygame.mouse.get_pos()
			mr = pygame.Rect(mp[0],mp[1] - self.size[1] + self.pos,2,2)
			for i in self.buttons[self.page]:
				if pygame.Rect.colliderect(mr,i[0]):
					if i[1] == 0:
						if res.TTS: plyer.tts.speak(dtb.TTSTEXT['DELETE'])
						else: self.sfx.play(res.SOUND['MENU_BACK'])
						self.output = self.output[0:-1]
					elif i[1] == 1:
						self.caps += 1
						if self.caps > 2: self.caps = 0
						if res.TTS: plyer.tts.speak(dtb.TTSTEXT['CAPS' + str(self.caps + 1)])
						else: self.sfx.play(res.SOUND['MENU_GO'])
						self.sfx.play(res.SOUND['MENU_GO'])
					elif i[1] == 2:
						self.page += 1
						if self.page > 1: self.page = 0
						if res.TTS: plyer.tts.speak(dtb.TTSTEXT['PAGE'] + ' ' + str(self.page + 1))
						else: self.sfx.play(res.SOUND['MENU_GO'])
					elif i[1] == 3:
						if res.TTS: plyer.tts.speak(dtb.TTSTEXT['CONFIRM'])
						else: self.sfx.play(res.SOUND['MENU_GO'])
						self.active = False
					else:
						if res.TTS:
							if i[1][self.opt] in dtb.TTSTEXT: vv = dtb.TTSTEXT[i[1][self.opt]]
							else: vv = i[1][self.opt]
							plyer.tts.speak(vv)
						else: self.sfx.play(res.SOUND['TEXT_INPUT'])
						if len(i[1]) > 1: self.hold += 1
						if self.caps == 0: self.output += i[1][self.opt]
						else:
							self.output += i[1][self.opt].upper()
							if self.caps == 1: self.caps = 0
					i[2] = 0
	
	def scroll(self):
		if self.active and self.pos < self.surface.get_height(): self.pos += 10
		if self.active == False and self.pos > 0: self.pos -= 10

	def draw(self):
		self.surface.fill((0,0,0))
		
		r = 0
		for i in self.buttons[self.page]:
			add = 0
			if self.type == 'QWERTY' and r > 19 and r < 29: add = 20
			pygame.draw.rect(self.surface,(res.COLOR[0],res.COLOR[1],res.COLOR[2]),pygame.Rect(add + i[0].x,i[0].y,i[0].width,i[0].height),i[2])
			if i[1] == 0: self.surface.blit(self.font.render('<X>',1,(res.COLOR[0],res.COLOR[1],res.COLOR[2])),(add + i[0].x + 8,i[0].y))
			elif i[1] == 1: self.surface.blit(self.font.render(str(self.caps) + '^',1,(res.COLOR[0],res.COLOR[1],res.COLOR[2])),(add + i[0].x + 8,i[0].y))
			elif i[1] == 2: self.surface.blit(self.font.render(str(self.page + 1) + '/2',1,(res.COLOR[0],res.COLOR[1],res.COLOR[2])),(add + i[0].x + 8,i[0].y))
			elif i[1] == 3: self.surface.blit(self.font.render('&',1,(res.COLOR[0],res.COLOR[1],res.COLOR[2])),(add + i[0].x + 8,i[0].y))
			else:
				if self.caps == 0: txt = i[1][0]
				else: txt = i[1][0].upper()
				self.surface.blit(self.font.render(txt,1,(res.COLOR[0],res.COLOR[1],res.COLOR[2])),(add + i[0].x + 8,i[0].y))
			i[2] = 3
			r += 1
		
		return self.surface

class Avatar:
	def __init__(self):
		self.brd = pygame.Surface((200,150))
		for x in range(math.ceil(self.brd.get_width()/10)):
			for y in range(math.ceil(self.brd.get_height()/10)):
				self.brd.blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (x * 10, y * 10))
		self.scr = [pygame.Surface((200,150)), pygame.Surface((400,300), pygame.SRCALPHA)]
		self.fnt = {'MEDIUM': pygame.font.SysFont('Calibri', 40), 'SMALL': pygame.font.SysFont('Calibri', 20)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		
	def inside_events(self,pressed):
		if pressed[2][0]: self.page = 0; self.sfx.play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page = 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def draw(self,doll,data):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((0,0,0,0))
		self.scr[0].fill((100,200,100))
		pygame.draw.rect(self.scr[0],(10,40,10),pygame.Rect(0,0,400,300),10)
		
		if self.page == 0:
			img = pygame.image.load(res.SPRITES_PATH + 'pht_' + str(self.who) + '.png')
			pygame.draw.rect(self.scr[0],(250,250,250),pygame.Rect(15,15,img.get_rect().width,img.get_rect().height))
			self.scr[0].blit(img, (15, 15))
		if self.page == 1:
			self.scr[1].blit(self.fnt['SMALL'].render('REGISTRO', True, (10,40,10)), (15, 15))
			
		return self.scr

class PhoneBar:
	def __init__(self,bt):
		self.scr = [pygame.Surface((180,18)),pygame.Surface((360,50), pygame.SRCALPHA)]
		self.fnt = {'DATETIME': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 32),'ALT': pygame.font.Font(res.FONTS_PATH + 'Sicret_PERSONAL-Regular.ttf', 32)}
		self.credit = 0
		self.battery = bt
	
	def draw(self):
		for i in self.scr: i.fill((10,10,10))
		dvd3 = math.floor(self.scr[0].get_width()/3)

		day = ['','','']
		if res.DATE[0] < 10: day[0] = '0' + str(res.DATE[0])
		else: day[0] = str(res.DATE[0])
		if res.DATE[1] < 10: day[1] = '0' + str(res.DATE[1])
		else: day[1] = str(res.DATE[1])
		if res.DATE[2] < 10: day[2] = '0' + str(res.DATE[2])
		else: day[2] = str(res.DATE[2])
		self.scr[1].blit(self.fnt['DATETIME'].render(day[0] + '/' + day[1] + '/' + day[2], True, (255, 255, 255)), (3, 1))

		hour = ['','']
		if res.TIME[0] < 10: hour[0] = '0' + str(res.TIME[0])
		else: hour[0] = str(res.TIME[0])
		if res.TIME[1] < 10: hour[1] = '0' + str(res.TIME[1])
		else: hour[1] = str(res.TIME[1])
		self.scr[1].blit(self.fnt['DATETIME'].render(hour[0] + ':' + hour[1], True, (255, 255, 255)), ((dvd3 + 30) * 2, 1))

		self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'signal_' + str(res.SIGNAL) + '.png'), ((dvd3 * 3) - 47, 6))
		self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'battery.png'), ((dvd3 * 3) - 30, 2))
		if self.battery > 200: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect((dvd3 * 3) - 7 - int(18/(3600/self.battery)),5,int(18/(3600/self.battery)),7))
		elif self.battery > 0: pygame.draw.rect(self.scr[0], (255, 10, 10), pygame.Rect((dvd3 * 3) - 7 - int(18/(3600/self.battery)),5,int(18/(3600/self.battery)),7))

		return self.scr

class Apps:
	def __init__(self,t):
		self.img = pygame.image.load(res.BACKG_PATH + 'phone.png')
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scrpos = (44,93)
		self.rqst = True
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
		
	def inside_events(self,pressed,mouse):
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
			self.app.inside_events(pressed,mouse)
			self.ingame = self.app.ingame
			if self.opt == [0,0]: self.nb = self.app.nb
			if pressed[5][0]:
				self.sfx.play(res.SOUND['MENU_BACK'])
				if res.CHAPTER == 0 and res.SCENE == 0:
					self.ingame = 5
				self.app = None
						
	def outside_events(self,pressed):
		if self.app != None: self.app.outside_events(pressed)
	
	def draw(self):
		self.rqst = False
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
	
			self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))
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
				
			bsrf = PhoneBar(self.battery).draw()
			self.scr[0].blit(bsrf[0], (0,0))
			self.scr[1].blit(bsrf[1], (0,0))
			
			return self.scr
		else: self.scr = self.app.draw()

class GPS:
	def __init__(self, mn, rm, tl, pl, en, sig):
		self.img = pygame.image.load(res.BACKG_PATH + 'GPS.png')
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scrpos = (60,49)
		self.rqst = True
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
				
	def draw(self):
		self.rqst = False
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
				if i['HP'] > 0 and i['RECT'].x > 0 and i['RECT'].y > 0:
					scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'mp_anomaly.png'), (mpx + ((self.zoom/self.mp.get_width()) * xx),mpy + ((self.zoom/self.mp.get_height()) * yy)))
		else: scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[15], True, (255, 255, 255)), (25, 200))

		if self.mn == False:
			pygame.draw.rect(scr[1], (140, 255, 253), pygame.Rect(0,0,sz * 2,80))
			scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[0], True, (0, 0, 0)), (5, 4))

		return scr

class Contacts:
	def __init__(self):
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.credit = self.inv.find(res.PARTY[res.FORMATION][0],'sim_card','value')
		if self.battery != None: self.battery = int(self.battery[1])
		else: self.battery = 0
		if self.credit != None: self.credit = self.credit[1]
		else: self.credit = 0
		self.mnu = 0
		self.exvar = 0
		
	def inside_events(self,pressed,mouse):
		#SELECT OPTIONS
		if self.nb != None:
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
		else:
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
	
	def call(self):
		for i in self.scr: i.fill((10,10,10,0))
		sz = self.scr[1].get_width() #button width
		num = 0
		for i in dtb.NUMBERS:
			if i[1] == self.nb: break
			num += 1
		self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'call_' + self.nb + '.png'), (0, 90))
		pygame.draw.rect(self.scr[0], (res.COLOR[0], res.COLOR[1], res.COLOR[2]), pygame.Rect(0,0,sz,90))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.NUMBERS[num][0], True, (255, 255, 255)), (100, 20))
		self.scr[1].blit(self.fnt['CALIBRI'].render(self.nb, True, (255, 255, 255)), (100, 40))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[32] + str(self.credit), True, (255, 255, 255)), (100, 80))
		self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[33], True, (255, 255, 255)), (100, 120))

		if self.opt == 0: self.scr[0].blit(pygame.transform.scale(pygame.image.load(res.SPRITES_PATH + 'cl_ys.png'), (40, 40)), (25, 185))
		else: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'cl_ys.png'), (30, 190))
		if self.opt == 1: self.scr[0].blit(pygame.transform.scale(pygame.image.load(res.SPRITES_PATH + 'cl_no.png'), (40, 40)), (sz - 55, 185))
		else: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'cl_no.png'), (sz - 50, 190))

		return self.scr
	
	def draw(self):
		if self.nb != None: self.call()
		else:
			sz = self.scr[0].get_width() #button width
			for i in self.scr: i.fill((0,0,0,0))
			self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))
			
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
				pygame.draw.rect(self.scr[0], col, pygame.Rect(0,66 + y - self.scroll,sz,50))
	
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		
	def inside_events(self,pressed,mouse):
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
		self.scr = [pygame.Surface((300,300)), pygame.Surface((600,600), pygame.SRCALPHA)]
		self.fnt = {'TITLE': pygame.font.SysFont('Times New Roman', 42),'MEDIUM': pygame.font.SysFont('Calibri', 30), 'SMALL': pygame.font.SysFont('Calibri', 20)}
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
		fsz = self.fnt['TITLE'].size('O LOBO')[0]
		self.scr[1].blit(self.fnt['TITLE'].render('O LOBO', True, (200,200,200)), (int(((sz * 2)/2) - (fsz/2)), 15))
		self.scr[1].blit(self.fnt['SMALL'].render(str(res.DATE[0]) + '/' + str(res.DATE[1]) + ' - 1ª edição', True, (10,10,10)), (30, 70))
		for y in range(5):
			if y == 0: self.scr[1].blit(self.fnt['MEDIUM'].render(self.rdnws[y], True, (10,10,10)), (25, 100))
			else: self.scr[1].blit(self.fnt['SMALL'].render(self.rdnws[y], True, (10,10,10)), (25, 150 + (y * 20)))

		return self.scr
		
class ID:
	def __init__(self,n):
		self.scr = [pygame.Surface((200,150)), pygame.Surface((400,300), pygame.SRCALPHA)]
		self.fnt = {'MEDIUM': pygame.font.SysFont('Calibri', 40), 'SMALL': pygame.font.SysFont('Calibri', 20)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.page = 0
		self.who = n
		
	def inside_events(self,pressed):
		if pressed[2][0]: self.page = 0; self.sfx.play(res.SOUND['PAGE_FLIP'])
		if pressed[3][0]: self.page = 1; self.sfx.play(res.SOUND['PAGE_FLIP'])
		
	def outside_events(self,pressed):
		pass
		
	def draw(self):
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((0,0,0,0))
		self.scr[0].fill((100,200,100))
		pygame.draw.rect(self.scr[0],(10,40,10),pygame.Rect(0,0,400,300),10)
		
		if self.page == 0:
			img = pygame.image.load(res.SPRITES_PATH + 'pht_' + str(self.who) + '.png')
			pygame.draw.rect(self.scr[0],(250,250,250),pygame.Rect(15,15,img.get_rect().width,img.get_rect().height))
			self.scr[0].blit(img, (15, 15))
		if self.page == 1:
			self.scr[1].blit(self.fnt['SMALL'].render('REGISTRO', True, (10,40,10)), (15, 15))
			self.scr[1].blit(self.fnt['MEDIUM'].render('XX.XXX.XXX-X', True, (10,10,10)), (70, 15))
			
			self.scr[1].blit(self.fnt['SMALL'].render('NOME', True, (10,40,10)), (15, 40))
			self.scr[1].blit(self.fnt['MEDIUM'].render(res.CHARACTERS[self.who]['NAME'] + ' ' + res.CHARACTERS[self.who]['LASTNAME'], True, (10,10,10)), (15, 55))
			
			self.scr[1].blit(self.fnt['SMALL'].render('NATURALIDADE', True, (10,40,10)), (15, 210))
			self.scr[1].blit(self.fnt['MEDIUM'].render(dtb.IDINFO[self.who][0], True, (10,10,10)), (15, 225))
			
			self.scr[1].blit(self.fnt['SMALL'].render('DATA DE NASCIMENTO', True, (10,40,10)), (300, 210))
			self.scr[1].blit(self.fnt['MEDIUM'].render(dtb.IDINFO[self.who][1], True, (10,10,10)), (300, 225))
			
			self.scr[1].blit(self.fnt['SMALL'].render('CPF', True, (10,40,10)), (15, 250))
			self.scr[1].blit(self.fnt['MEDIUM'].render('XXX.XXX.XXX-XX', True, (10,10,10)), (15, 265))

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
		self.img = pygame.image.load(res.BACKG_PATH + 'mp3.png')
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scrpos = (39,46)
		self.rqst = True
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
		self.song = res.MUSIC_PATH + res.RADIO[math.floor(self.fm/20)][self.msc]
		self.mscinfo = {'TITLE': 'no song','ARTIST': 'unknown','ALBUM': 'unknown'}
		self.button = pygame.Rect(0,66,self.scr[0].get_width(),50)
		self.scroll = 0
		self.nwsw = 0
		self.nwss = 0
		
	def inside_events(self,pressed,mouse):
		if res.SIGNAL > 0:
			do = False
			if pressed[4][0]: do = True
			elif pygame.Rect.colliderect(self.button,mouse): do = True
			if pressed[4][0]:
				self.onoff = not self.onoff
				if self.onoff == False:
					self.sfx.play(res.SOUND['MENU_BACK'])
					self.noi.stop()
					pygame.mixer.music.stop()
				else:
					self.sfx.play(res.SOUND['MENU_GO'])
					self.noi.play(res.SOUND['NOISE'],-1)
					self.song = res.MUSIC_PATH + res.RADIO[math.floor(self.fm/20)][self.msc] + '.mp3'
					audio = MP3(self.song)
					try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
					except: self.mscinfo = {'TITLE': res.RADIO[math.floor(self.fm/20)][self.msc] + '.mp3','ARTIST': 'unknown','ALBUM': 'unknown'}
					pygame.mixer.music.load(self.song)
					pygame.mixer.music.play()
			if pressed[7][0]:
				self.noi.stop()
						
	def outside_events(self,pressed):
		if pressed[2][0]: self.fm -= 1; self.vm -= 0.05
		if pressed[3][0]: self.fm += 1; self.vm += 0.05

		if self.fm < 0: self.fm = (res.RANGE_RADIO - 1) * 20
		if self.fm > (res.RANGE_RADIO - 1) * 20: self.fm = 0
		if self.vm < 0.0: self.vm = 1.0
		if self.vm > 1.0: self.vm = 0.0

		pygame.mixer.music.set_volume(self.vm)
		self.noi.set_volume(1 - self.vm)
		ind = math.floor(self.fm/(res.RANGE_RADIO * 2))
		if self.vm == 0.0 and self.onoff == True:
			if res.RADIO[ind] != []:
				self.song = res.MUSIC_PATH + res.RADIO[ind][self.msc] + '.mp3'
				audio = MP3(self.song)
				try: self.mscinfo = {'TITLE': audio['TIT2'].text[0],'ARTIST': audio['TPE1'].text[0],'ALBUM': audio['TALB'].text[0]}
				except: self.mscinfo = {'TITLE': res.RADIO[ind][self.msc] + '.mp3','ARTIST': 'unknown','ALBUM': 'unknown'}
				pygame.mixer.music.load(self.song)
				pygame.mixer.music.play()
				
	def display(self):
		ind = math.floor(self.fm/(res.RANGE_RADIO * 2))
		rdsrf = pygame.Surface((360 + self.nwsw,50))
		rdsrf.fill((255, 0, 135))
		if self.msc < 0:
			ttsz = math.floor(self.fnt['CALIBRI'].size('?????')[0]/2)
			rdsrf.blit(self.fnt['CALIBRI'].render('?????', True, (0, 0, 0)), (-self.scroll * 2, 5 * 2))
		else:
			if self.nwsw > 0: txt = dtb.RADIONEWS[self.nwind][2]
			else:
				txt = self.mscinfo['TITLE']
				if self.mscinfo['ARTIST'] != 'unknown':
					txt += ' – ' + self.mscinfo['ARTIST']
			if res.DISLEXIC == True:
				out = ''
				for t in txt: out += t + ' '
			else: out = txt
			ttsz = math.floor(self.fnt['CALIBRI'].size(out)[0]/2)
			rdsrf.blit(self.fnt['CALIBRI'].render(out, True, (0, 0, 0)), (-self.scroll * 2, 5 * 2))
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
		
		return rdsrf

	def draw(self):
		self.rqst = False
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((0,0,0,0))
		ind = math.floor(self.fm/(res.RANGE_RADIO * 2))
		if res.RADIO[ind] != []:
			txt = self.mscinfo['TITLE']
			if self.mscinfo['ARTIST'] != 'unknown':
				txt += ' – ' + self.mscinfo['ARTIST']
			pygame.draw.rect(self.scr[0], (255, 0, 135), self.button)
			self.scr[1].blit(self.fnt['CALIBRI'].render(txt, True, (0, 0, 0)), (20, 152))
		else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[20], True, (255, 255, 255)), (140, 280))

		self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))
		f = 0
		sp = math.floor(sz/res.RANGE_RADIO)
		for i in range(res.RANGE_RADIO - 1):
			pygame.draw.line(self.scr[0], (255, 255, 255), (0 + f,50),(0 + f,65),1)
			pygame.draw.line(self.scr[0], (255, 255, 255), (round(sp/2) + f,55),(round(sp/2) + f,65),1)
			f += sp
		pygame.draw.rect(self.scr[0], (255, 0, 0), pygame.Rect(0 + self.fm,50,4,16))
		self.scr[1].blit(self.fnt['CALIBRI'].render(str(self.fm/10), True, (255, 255, 255)), (140, 40))

		'''pygame.draw.rect(self.scr[1], (255, 0, 135), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[4], True, (0, 0, 0)), (10, 10))'''
		
		bsrf = PhoneBar(self.battery).draw()
		self.scr[0].blit(bsrf[0], (0,0))
		self.scr[1].blit(bsrf[1], (0,0))

		return self.scr

class Camera:
	def __init__(self):
		self.img = pygame.image.load(res.BACKG_PATH + 'camera.png')
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 30),
		'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.scrpos = (57,89)
		self.rqst = True
		self.ingame = 0
		self.battle = False
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = 0
		self.hpctrl = 'PHONE_CAMERA'
		res.recent_data(0)
		self.optrects = []
		for i in range(len(res.FILES[0]) + 1):
			self.optrects.append(pygame.Rect(0,41 + (i * 51),self.scr[0].get_width(),50))
	
	def inside_events(self,pressed,mouse):
		if res.SIGNAL > 0:
			if pressed[0][0]: self.opt -= 1; self.sfx.play(res.SOUND['MENU_VER'])
			if pressed[1][0]: self.opt += 1; self.sfx.play(res.SOUND['MENU_VER'])

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
					self.sfx.play(res.SOUND['FILE_SAVE'])
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
						self.sfx.play(res.SOUND['CAMERA'])
						self.ingame = 7
	
	def outside_events(self,pressed):
		pass
		
	def photo(self,bg,foes,xpos):
		self.rqst = False
		self.hpctrl = 'PHONE_PHOTO'
		for i in self.scr: i.fill((0,0,0,0))
		self.scr[0].blit(bg, (-xpos, -88))
		for i in foes:
			self.scr[0].blit(i['SPRITE'], (-xpos + i['MASK'].x, -88 + i['MASK'].y))

		return self.scr
		
	def draw(self):
		self.rqst = False
		self.hpctrl = 'PHONE_CAMERA'
		sz = self.scr[0].get_width() #button width
		for i in self.scr: i.fill((0,0,0,0))
		self.scr[0].blit(pygame.image.load(res.BACKG_PATH + 'phn_' + str(res.PARTY[res.FORMATION][0]) + '.png'), (0, 0))

		if res.SIGNAL > 0:
			y = 0
			for i in self.optrects:
				if self.opt != y: col = (255, 255, 255)
				else: col = (255, 255, 10)
				rct = pygame.Surface((i.width,i.height))
				rct.fill(col)
				rct.set_alpha(100)
				self.scr[0].blit(rct,(i.x,i.y))
				if y < len(res.FILES[0]):
					self.scr[1].blit(self.fnt['MONOTYPE'].render(dtb.CHAPTERS[res.FILES[1][y]][0], True, (0, 0, 0)), (20, (51 + (y * 51)) * 2))
					ss = math.floor(res.FILES[2][y]/1000)
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
					self.scr[1].blit(self.fnt['MONOTYPE'].render(hh + ' : ' + mm + ' : ' + ss, True, (0, 0, 0)), (20, (65 + (y * 51)) * 2))
					x = 0
					for p in res.FILES[4][y][::-1]:
						self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'who_' + str(p) + '.png'), (sz - 30 - x, 65 + (y * 51)))
						x += 22
				else: self.scr[1].blit(self.fnt['MONOTYPE'].render(dtb.MENU[61], True, (0, 0, 0)), (20, (61 + (y * 51)) * 2))
				y += 1
		else: self.scr[1].blit(self.fnt['MONOTYPE'].render(dtb.MENU[15], True, (255, 255, 255)), (50, 280))

		pygame.draw.rect(self.scr[1], (255, 255, 255), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[5], True, (0, 0, 0)), (10, 10))
		
		return self.scr

class Bestiary:
	def __init__(self):
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
					self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'Freaks/frk_' + res.BESTIARY[opt]['N'] + '_stand.png'), (40, 70))
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
						self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_8.png'), (sz - 40, 51 + y - self.scroll))
					for b in range(4):
						self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'tc_' + str(i[b]) + '.png'), (10 + (22 * b), 51 + y - self.scroll))
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
		self.fnt = {'CALIBRI': pygame.font.SysFont('Calibri', 30), 'MONOTYPE': pygame.font.Font(res.FONTS_PATH + 'monotype.ttf', 10), 'DESCRIPTION': pygame.font.SysFont('Calibri', 25),
			'TITLE': pygame.font.Font(res.FONTS_PATH + 'pixel-font.ttf', 40)}
		self.ingame = 0
		self.sfx = pygame.mixer.Channel(0)
		self.sfx.set_volume(res.SFX)
		self.scroll = 0
		self.optrects = []
		self.opt = [0,0]
		self.mnu = 0
		self.trg = 0
		self.buttons = []
		btlst = [3,8,2,3,10,2,10]
		for i in range(len(btlst)):
			self.buttons.append([])
			for b in range(btlst[i]):
				self.buttons[i].append(pygame.Rect(0,b * 35,self.scr[0].get_width(),30))
		
	def inside_events(self,pressed):
		if pressed[0][0]: self.opt[1] -= 1; self.sfx.play(res.SOUND['MENU_VER'])
		if pressed[1][0]: self.opt[1] += 1; self.sfx.play(res.SOUND['MENU_VER'])
		if self.opt[1] < 0: self.opt[1] = len(self.buttons[self.mnu])
		if self.opt[1] > len(self.buttons[self.mnu]): self.opt[1] = 0
		#MAIN SETTINGS
		if self.mnu == 0:
			if pressed[4][0]:
				if self.opt[1] == 3:
					res.save_data(1)
					self.sfx.play(res.SOUND['MENU_GO'])
					self.opt[0] = 1
					self.opt[1] = 4
					self.phone = 1
					if res.CHAPTER == 0 and res.SCENE == 0:
						self.ch_ton.play(res.SOUND['CALLING'],-1)
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
					res.LANG = 'EN'; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]:
					res.LANG = 'PT'; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 1:
				if pressed[2][0]: res.SPEED += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SPEED -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

				if res.SPEED < 1: res.SPEED = 5
				if res.SPEED > 5: res.SPEED = 1
			if self.opt[1] == 5:
				if pressed[2][0]: res.BORDER -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.BORDER += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

				if res.BORDER < 0: res.BORDER = res.RANGE_BORDER
				if res.BORDER > res.RANGE_BORDER: res.BORDER = 0
			if self.opt[1] == 6:
				if pressed[2][0]: res.CENSORSHIP = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CENSORSHIP = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 7:
				if pressed[2][0]: res.HINT = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HINT = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
			if self.opt[1] == 8:
				if pressed[2][0]: res.HELP = False; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.HELP = True; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
		#CONTROLS MENU
		elif self.mnu == 3:
			if pressed[4][0]:
				self.mnu = self.opt[1] + 4
				self.opt[0] = 0
				self.opt[1] = 0
		#MOUSE SETTINGS
		elif self.mnu == 4:
			if self.opt[1] == 1:
				if pressed[2][0]: res.CURSOR -= 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.CURSOR += 1; self.sfx.set_volume(res.SFX); self.sfx.play(res.SOUND['MENU_HOR'])

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
				self.sfx.play(res.SOUND['MENU_BACK'])
				self.mnu = 0
							
	def outside_events(self,pressed):
		#COLORS SETTINGS
		if self.mnu == 1:
			if self.opt[1] == 2:
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
			if self.opt[1] == 0:
				if pressed[2][0]: res.SFX -= 0.1; self.sfx.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.SFX += 0.1;  self.sfx.play(res.SOUND['MENU_HOR'])
				self.sfx.set_volume(res.SFX)
				if res.SFX < 0.0: res.SFX = 0.0
				if res.SFX > 1.0: res.SFX = 1.0
			if self.opt[1] == 1:
				if pressed[2][0]: res.MSC -= 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])
				if pressed[3][0]: res.MSC += 0.1; self.ch_msc.play(res.SOUND['MENU_HOR'])

				if res.MSC < 0.0: res.MSC = 0.0
				if res.MSC > 1.0: res.MSC = 1.0

	def draw(self):
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
		if self.mnu == 0:
			self.scroll = 0
			inpts = (88,89,90,76)
			for i in range(4):
				if self.opt[0] == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp
		#GAMEPLAY MENU
		if self.mnu == 1:
			inpts = (62,72,73,74,75,87,96,97,98)
			if self.opt[0] == 0:
				if self.scroll > 0:
					self.scroll -= 10
			elif self.opt[0] == 5:
				if self.scroll < 60:
					self.scroll += 10
			elif self.opt[0] == 6:
				if self.scroll < 60:
					self.scroll += 10
			elif self.opt[0] == 2:
				if self.scroll > 0:
					self.scroll -= 10
			elif self.opt[0] == 8:
				if self.scroll < 60:
					self.scroll += 10
			for i in range(9):
				#RECT AND SELECT
				if self.opt[0] == i:
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
						for c in range(3): self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'border_' + str(res.BORDER) + '.png'), (60 + b * 10, 196 + (c * 10) - self.scroll))
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
		if self.mnu == 2:
			self.scroll = 0
			inpts = (res.SFX,res.MSC)
			for i in range(2):
				if self.opt[0] == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				pygame.draw.rect(self.scr[0], (230, 210, 210), pygame.Rect(bs,y + ty - self.scroll,bw,bh))
				pygame.draw.rect(self.scr[0], (110, 110, 110), pygame.Rect(bs + (inpts[i] * (bw - 10)),y + ty - self.scroll,20,bh))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[63 + i], True, (0,0,0)), (10, (y + ty - 2 - self.scroll)* 2))
				y += hz + sp
		#CONTROLS MENU
		if self.mnu == 3:
			self.scroll = 0
			inpts = (99,100,101,102)
			for i in range(4):
				if self.opt[0] == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp
		#MOUSE MENU
		if self.mnu == 4:
			self.scroll = 0
			inpts = (103,104,105)
			for i in range(3):
				if self.opt[0] == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[inpts[i]], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				#CURSOR self.opt[0]IONS
				if i == 1: self.scr[0].blit(pygame.image.load(res.SPRITES_PATH + 'cursor_' + str(res.CURSOR) + '.png'), (100, 5 + y - self.scroll))
				y += hz + sp
		#1P CONTROLS
		if self.mnu == 5:
			if self.opt[0] == 0:
				if self.scroll > 0:
					self.scroll -= 10
			elif self.opt[0] == 5:
				if self.scroll < 60:
					self.scroll += 10
			elif self.opt[0] == 2:
				if self.scroll > 0:
					self.scroll -= 10
			elif self.opt[0] == 7:
				if self.scroll < 60:
					self.scroll += 10

			ctrls = (res.UP,res.DOWN,res.LEFT,res.RIGHT,res.ACT,res.RUN,res.PHONE,res.BAG)
			for i in range(7):
				if self.opt[0] == i: pygame.draw.rect(self.scr[0], (91, 91, 91), pygame.Rect(0,y - self.scroll,sz,hz))
				else: pygame.draw.rect(self.scr[0], (255, 255, 255), pygame.Rect(0,y - self.scroll,sz,hz))
				if self.trg: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				elif self.opt[0] == i: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[77], True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				else: self.scr[1].blit(self.fnt['CALIBRI'].render(dtb.MENU[65 + i] + ': ' + pygame.key.name(ctrls[i][0]), True, (0,0,0)), (10, (y + ty - self.scroll) * 2))
				y += hz + sp

		pygame.draw.rect(self.scr[1], (91, 91, 91), pygame.Rect(0,0,sz * 2,80))
		self.scr[1].blit(self.fnt['TITLE'].render(dtb.MENU[13], True, (0, 0, 0)), (10, 10))

		return self.scr
		
class About:
	def __init__(self):
		self.scr = [pygame.Surface((180,232)), pygame.Surface((360,464), pygame.SRCALPHA)]
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