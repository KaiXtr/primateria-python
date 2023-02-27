import pygame
import numpy as np
import PIL
import sys
import os

def reverse(file):
	img = pygame.image.load(file)
	srf = pygame.Surface((img.get_width(),img.get_height()),pygame.SRCALPHA)
	srf.fill((255,255,255,255))
	srf.blit(img,(0,0),None,pygame.BLEND_RGB_SUB)
	return srf

def rgb_channel(file,value):
	lst = [i + '-' + j for i in ['rgb','rbg','grb','gbr','brg','bgr'] \
		for j in ['regular','grayscale','red','green','blue','red-green','red-blue','green-blue']]
	for i in range(len(lst)):
		if value == lst[i]: value = i

	channels = []
	chn = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
	for c in [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]:
		add = [0 for i in range(12)]
		for cc in range(len(c)): add[c[cc] + (4 * cc)] = 1
		channels.append(tuple(add))

		add = [0 for i in range(12)]
		for cc in range(len(c)): add[4 * cc] = 1
		channels.append(tuple(add))

		for i in chn:
			add = [0 for i in range(12)]
			for cc in range(len(c)): add[c[cc] + (4 * cc)] = i[cc]
			channels.append(tuple(add))

	srf = PIL.Image.open(file)
	srf = srf.convert(srf.mode,channels[value])
	return pygame.image.fromstring(srf.tobytes(),srf.size,srf.mode).convert_alpha()

def glitch(file):
	img = PIL.Image.open(file)
	srf = pygame.Surface(img.size,pygame.SRCALPHA)
	mm = 0
	mrg = [(0,15),(15,0),(15,15)]
	for i in [(1,0,0),(0,1,0),(0,0,1)]:	
		add = [0 for x in range(12)]
		add[0] = i[0]; add[4] = i[1]; add[8] = i[2]
		chn = img.copy().convert(img.mode,tuple(add))
		chn = pygame.image.fromstring(chn.tobytes(),chn.size,chn.mode)
		if mm: srf.blit(chn,mrg[mm],None,pygame.BLEND_RGBA_ADD)
		else: srf.blit(chn,mrg[mm])
		mm += 1

	return srf