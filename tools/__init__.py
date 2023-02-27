import ctypes
import pathlib
import sys
import os

'''t = ctypes.CDLL("teste.so")
t.connect()
print(t.hello())'''

for i in ['data','draw','event','image','mixer','physics','text','time']:
	if os.path.basename(os.getcwd()) == 'tools': exec(f'import {i}')
	else: exec(f'import tools.{i}')

if __name__ == "__main__": pass
	#tools = pathlib.Path().absolute() / "SDL.cxx"
	#c_lib = ctypes.CDLL(tools)
	#sdlstart = c_lib.main()