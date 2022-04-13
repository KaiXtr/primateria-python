import pygame
import sys
import os

sys.path.insert(0,os.path.realpath('../'))
res = __import__('resources')

def digitstring(number,digits):
	value = ''
	for i in range(digits):
		if len(str(number)) == i:
			add = ''
			for d in range(digits - i):
				add += '0'
			value = add + str(number)
	if value == '': return str(number)
	else: return value

def font_size(font,size):
	return pygame.freetype.Font(res.FONTS_PATH + 'BohemianTypewriter.ttf', size * res.GSCALE)
	
def stripacc(txt):
	lst = [('a','äåæªáãàâ'),('c','ćçč'),('e','ëėēèéêę'),('i','íìîįïī'),('n','ñń'),('o','ºōœøöòôóõ'),
	('u','ūùúüû')]
	txt = txt.lower()
	nw = ''
	for i in range(len(txt)):
		nn = True
		for x in lst:
			if txt[i] in [y for y in x[1]]:
				nw += x[0]
				nn = False
		if nn: nw += txt[i]
	return nw

def dislexic(txt):
	DISLEXIC = False
	if DISLEXIC == True:
		out = ''
		for t in txt: out += t + ' '
	else: out = txt
	return out

def wrap(text,font,width):
	txt = []
	t = ''
	for y in text:
		'''if isinstance(y,int):
			if t != '': t += ' '
			t += res.CHARACTERS[y]['NAME']'''
		if y == '':
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