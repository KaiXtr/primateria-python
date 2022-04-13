import pygame
import numpy as np

def sound_wave(wave, f=1000, length=1, fs=44100):
	if wave == 'sine': x = np.sin(2 * np.pi * f * np.arange(length * fs) / fs)
	if wave == 'square': x = [i for i in [[1,-1][i%2] for i in range(int(f/2))] for ff in range(int((length * fs)/int(f/2)))]
	if wave == 'saw': x = [ff for i in range(int(f/2)) for ff in range(-int((length * fs)/(f/2)),int((length * fs)/(f/2)))]
	if wave == 'som_interessante_e_estranho': x = [i - int((i/f) * f) for i in range(int(length * fs))]
	if wave == 'noise': x = np.random.uniform(-1,1,length * fs)

	x = np.int16(x/np.max(np.abs(x)) * 5000)
	return pygame.sndarray.make_sound(np.tile(x,(2,1)).T.copy(order='c'))

def noise(): return sound_wave('noise')

def audio_velocity(snd,value):
	x = pygame.sndarray.array(snd)
	if int(value): x = x[::int(value)]
	if value%1: x = np.array([i for i in x for v in range(int(1/value))])
	return pygame.sndarray.make_sound(x.copy(order='c'))

def audio_display(snd,offset=0,zoomt=0.1,zooma=0.01):
	snd = pygame.sndarray.array(snd)
	srf = pygame.Surface((300,300))
	srf.fill((0,0,0))

	for i in range(len(snd)):
		cor = ((i * zoomt) - offset,(snd[i][0] * zooma) + 150)
		if i > 0: pygame.draw.aaline(srf,(10,200,10),prv,cor)
		prv = cor
	return srf