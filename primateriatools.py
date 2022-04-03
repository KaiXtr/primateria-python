import ctypes
import pathlib

if __name__ == "__main__":
	primateriatools = pathlib.Path().absolute() / "SDL.cxx"
	c_lib = ctypes.CDLL(primateriatools)
	
	sdlstart = c_lib.main()