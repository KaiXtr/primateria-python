import pygame
import numpy as np

class Main:
  def __init__(self):
    pygame.init()
    self.display = pygame.display.set_mode((600, 600))
    self.clock = pygame.time.Clock()
    
    self.map = (self.display.get_width() * 5,self.display.get_height() * 5)
    self.player = [300,300]
    self.cam = [0,0]
    self.items = []
    for i in range(100): self.items.append([np.random.randint(0,self.map[0]),np.random.randint(0,self.map[1])])
  	
  def run(self):
    mp = pygame.mouse.get_pos()
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		pygame.quit()
    		exit()
    for i in range(2): 
      self.player[i] += int((mp[i] - self.player[i])/20)
      self.cam[i] += int((mp[i] - self.player[i])/20)
    
    self.display.fill((100,100,100))
    
    c = False
    sz = 40
    for y in range(int(self.map[1]/sz)):
      for x in range(int(self.map[0]/sz)):
        if c: col = (10,10,10)
        else: col = (200,200,10)
        pygame.draw.rect(self.display,col,pygame.Rect((x * sz) - self.cam[0],(y * sz) - self.cam[1],sz,sz))
        c = not c
    pygame.draw.circle(self.display,(200,10,10),(self.player[0] - self.cam[0],self.player[1] - self.cam[1]),20)
    self.items = [i for i in self.items if not pygame.Rect.colliderect(pygame.Rect(self.player[0],self.player[1],40,40),pygame.Rect(i[0],i[1],10,10))]
    for i in self.items: pygame.draw.circle(self.display,(10,200,10),(i[0] - self.cam[0],i[1] - self.cam[1]),10)
    
    pygame.display.flip()
    self.clock.tick(30)
		
g = Main()
while True: g.run()
