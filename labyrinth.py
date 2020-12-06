import pygame
import pytmx
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import sys

pygame.init()
pygame.display.set_caption('Labyrinth')
pygame.display.set_icon(pygame.image.load('icon.ico'))
pygame.mouse.set_visible(False)

class Main:
	def __init__(self):
		self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.OPENGL)
		self.glock = pygame.time.Clock()
		self.FPS = 60

		self.cubes = []
		self.position = [10,10,10]
		self.rotate = [0,0,0,0]
		self.edg = [
			[0,1],[0,2],[0,4],
			[3,1],[3,2],[3,7],
			[5,1],[5,4],[5,7],
			[6,4],[6,2],[6,7],
		]
		self.faces = [
			(0,1,3,2),
			(4,5,7,6),
			(0,1,5,4),
			(2,3,7,6),
			(2,0,4,6),
			(1,3,7,5)
		]
		self.colors = (
			[[0,1,1],
			[0,1,1],
			[1,1,1],
			[1,1,1],
			[0,0,1],
			[0,0,1]],

			[[1,0,0],
			[1,0,0],
			[0,1,0],
			[0,1,0],
			[1,0,1],
			[1,0,1]],
		)
		self.rendermap()

	def rendermap(self):
		self.map = pytmx.load_pygame('Maps/3Dtest.tmx')
		self.cubes = []
		cb = 0
		rects = []
		for y in range(0, self.map.height):
			for x in range(0, self.map.width):
				t = self.map.get_tile_properties(x, y, 0)
				if t != None:
					#image = self.map.get_tile_image_by_gid(gid)/2
					#image.convert()
					t = t['TYPE'].upper()

					if t == 'GRASS': z = 0
					if t == 'WALL': z = 2
					'''if len(rects) > 1:
						if rects[cb - 1][0] == ((x * 2) - 2) and rects[cb -1][4] == z: rects[cb - 1][2] += 2
						else: rects.append([x * 2,y * 2,2,2,z])
					else: rects.append([x * 2,y * 2,2,2,z])'''
					rects.append([x * 2,y * 2,2,2,z])
			cb += 1
		for r in rects:
			vertex = []
			for vz in (r[4],r[4] + 2):
				for vy in (r[1],r[1] + r[3]):
					for vx in (r[0],r[0] + r[2]):
						vertex.append([vx,vz,vy])
			self.cubes.append(vertex)

	def run(self):
		gluPerspective(45,(3/2),0.1,50.0)
		glTranslatef(0.0,0.0,-5)
		glRotatef(0,0,0,0)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					exit()
				self.rotation = [0,0,0]
				self.position = [0,0,0]
				self.pressed = pygame.key.get_pressed()
				if self.pressed[pygame.K_w]: self.rotate[0] = 1
				if self.pressed[pygame.K_s]: self.rotate[0] = -1
				if self.pressed[pygame.K_a]: self.rotate[1] = 1
				if self.pressed[pygame.K_d]: self.rotate[1] = -1
				if self.pressed[pygame.K_UP]: self.position[2] = 0.1
				if self.pressed[pygame.K_DOWN]: self.position[2] = -0.1
				if self.pressed[pygame.K_LEFT]: self.position[0] = 0.1
				if self.pressed[pygame.K_RIGHT]: self.position[0] = -0.1
				if self.pressed[pygame.K_g]: self.position[1] = -0.1
				if self.pressed[pygame.K_h]: self.position[1] = 0.1

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glTranslatef(self.position[0],self.position[1],self.position[2])
			glRotatef(self.rotate[0],self.rotate[1],self.rotate[2],self.rotate[3])

			glBegin(GL_QUADS)
			for c in self.cubes:
				if c[0][1] == 0: t = 0
				elif c[0][1] == 2: t = 1
				x = 0
				for f in self.faces:
					for v in f:
						glColor3fv(self.colors[t][x])
						glVertex3fv(c[v])
					x += 1
			glEnd()
			'''
			glBegin(GL_LINES)
			for c in self.cubes:
				for e in self.edg:
					for v in e:
						glVertex3fv(c[v])
			glEnd()'''
			pygame.display.flip()
			#self.glock.tick(self.FPS)
m = Main()
m.run()