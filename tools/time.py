import sys
import os

sys.path.insert(0,os.path.realpath('../'))
res = __import__('resources')

def datetime_update(value=1):
	lst = [0,0,0,0,0,0,0]
	for i in range(int(value/60) + 1):
		#SECONDS
		res.TIME[2] += value - (i * 60); lst[0] = 1
		#MINUTES
		if res.TIME[2] < 0: res.TIME[1] -= 1; res.TIME[2] = 59
		if res.TIME[2] >= 60: res.TIME[1] += 1; res.TIME[2] = 0; lst[1] = 1
		#HOURS
		if res.TIME[1] < 0: res.TIME[0] -= 1; res.TIME[1] = 59
		if res.TIME[1] >= 60: res.TIME[0] += 1; res.TIME[1] = 0; lst[2] = 1
		#DAYS
		if res.TIME[0] >= 24: res.DATE[0] += 1; res.DATE[3] += 1; res.DATE[4] += 1; res.TIME[0] = 0; lst[3] = 1
		#WEAKS
		if res.DATE[3] > 7: res.DATE[3] = 1; res.DATE[4] += 1; lst[4] = 1
		#MOONS
		if res.DATE[4] > 8: res.DATE[4] = 0
		#MONTHS
		if res.DATE[1] in [1,3,5,7,8,10,12] and res.DATE[0] > 31: res.DATE[1] += 1; res.DATE[0] = 1; lst[5] = 1
		elif res.DATE[1] in [4,6,9,11] and res.DATE[0] > 30: res.DATE[1] += 1; res.DATE[0] = 1; lst[5] = 1
		elif res.DATE[1] == 2 and res.DATE[0] > 28: res.DATE[1] += 1; res.DATE[0] = 1; lst[5] = 1
		#YEARS
		if res.DATE[1] > 12: res.DATE[2] += 1; res.DATE[1] = 1; lst[6] = 1

	return lst