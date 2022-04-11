import ctypes
import pathlib
import numpy as np

def follow(rct1,rct2):
	offstx = [rct1.x + int(rct1.width/2),rct2.x + int(rct2.width/2)]
	offsty = [rct1.y + int(rct1.height/2),rct2.y + int(rct2.height/2)]
	if offsty[0] > offsty[1]:
		if offstx[0] < offstx[1]: return 8
		elif offstx[0] > offstx[1]: return 6
		else: return 7
	elif offsty[0] < offsty[1]: 
		if offstx[0] < offstx[1]: return 2
		elif offstx[0] > offstx[1]: return 4
		else: return 3
	elif offstx[0] < offstx[1]:
		if offsty[0] > offsty[1]: return 8
		elif offsty[0] < offsty[1]: return 2
		else: return 1
	elif offstx[0] > offstx[1]:
		if offsty[0] > offsty[1]: return 6
		elif offsty[0] < offsty[1]: return 4
		else: return 5

def align(input,value):
	xx = np.floor(input.x/value[0]) * value[0]
	yy = np.floor(input.y/value[1]) * value[1]
	return (xx,yy)

def pathfinding(rct,tgt,map): pass