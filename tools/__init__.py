import ctypes
import pathlib
import sys
import os

'''t = ctypes.CDLL("teste.so")
t.connect()
print(t.hello())'''

sys.path.insert(0,'tools')
data = __import__('data')
draw = __import__('draw')
event = __import__('event')
image = __import__('image')
mixer = __import__('mixer')
physics = __import__('physics')
text = __import__('text')
time = __import__('time')

'''for i in ('data','draw','event','mixer','physics','text'):
	eval("{} = __import__('./{}')".format(i,i))'''


if __name__ == "__main__": pass
	#tools = pathlib.Path().absolute() / "SDL.cxx"
	#c_lib = ctypes.CDLL(tools)
	#sdlstart = c_lib.main()