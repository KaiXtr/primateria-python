#include <iostream>
#include "SDL.h"

int main(int argc, char* argv[]) {
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		std::cout << "Unable to initialize SDL: " << SDL_GetError();
		return 1;
	}

	SDL_Quit();

	return 0;
}