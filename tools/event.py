import pygame
import sys
import os

sys.path.insert(0,os.path.realpath('../'))
res = __import__('resources')

def get_pressed(event):
	pressed = [[0 for p in range(4)] for i in range(len(res.CONTROLS[0]))]
	click = pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],2,2)
	#KEYBOARD
	if res.MOUSE < 2:
		if event:
			if event.type == pygame.KEYDOWN:
				pressed = [[event.key == res.CONTROLS[p][i] for p in range(4)] for i in range(len(res.ACTION))]
		else: pressed = [[pygame.key.get_pressed()[res.CONTROLS[p][i]] for p in range(4)] for i in range(len(res.ACTION))]
	#MOUSE
	if res.MOUSE:
		do = False
		if event:
			if event.type == pygame.MOUSEBUTTONDOWN: do = True
		else: do = True
		if do:
			gt = pygame.mouse.get_pressed()
			if gt[0]: pressed[4][0] = gt[0]
			if gt[2]: pressed[5][0] = gt[2]
			if gt[1]: pressed[8][0] = gt[1]
		if event and event.type == pygame.MOUSEWHEEL:
			if event.y > 0: pressed[0][0] = abs(event.y)
			if event.y < 0: pressed[1][0] = abs(event.y)
	#JOYSTICK
	pygame.joystick.init()
	connect = pygame.joystick.get_count()
	if connect > 1:
		res.MOUSE = 3
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
		print(joystick.get_numbuttons())
		#for i in range(6 + joystick.get_numbuttons()): pressed.append([0])
		for b in range(4):
			if pressed[res.JOYSTICK[b]][0] == 0:
				pressed[res.JOYSTICK[b]][0] = int(joystick.get_axis(b))
		for b in range(joystick.get_numbuttons()):
			if JOYSTICK[b + 4] == None and pressed[b + 4][0] == 0: pressed[b + 4][0] = 0
			elif pressed[JOYSTICK[b + 4]][0] == 0: pressed[res.JOYSTICK[b + 4]][0] = joystick.get_button(b)
		for b in range(2):
			if JOYSTICK[b + 4 + joystick.get_numbuttons()] == None: pressed[b + 4 + joystick.get_numbuttons()][0] = 0
			elif pressed[JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] == 0:
				pressed[JOYSTICK[b + 4 + joystick.get_numbuttons()]][0] = int(joystick.get_axis(b + 4))
		for i in pressed:
			while len(i) < 3: i.append(0)
	#TOUCHPAD
	buttons = []
	if len(buttons) > 0:
		res.MOUSE = 2
		if event != None:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if res.VIBRATE: plyer.vibrator.vibrate(0.1)
				chk = 1
			else: chk = 0
		else: chk = pygame.mouse.get_pressed()[0]
		for i in range(len(buttons)):
			if pygame.rect.colliderect(click,buttons[i]):
				if chk: pressed[i] = [1,0,0,0]
				elif pressed[i][0] == 0: pressed[i] = [0,0,0,0]
			elif pressed[i][0] == 0: pressed[i] = [0,0,0,0]
	#SHOW DEBUG
	#print(['PLAYER ' + str(p + 1) + ': ' + str([int(pressed[i][p]) for i in range(len(res.ACTION))]) for p in range(4)])
	return pressed, click

def wait():
	waiting = True
	'''pressed = self.get_pressed(None)
	for i in pressed:
		for j in i:
			if j: waiting = False'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); exit()
		if event.type == pygame.MOUSEBUTTONDOWN: waiting = False
		if event.type == pygame.KEYDOWN: waiting = False
	return waiting