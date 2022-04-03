#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>

//Load Image
extern "C" SDL_Texture *loadImage(SDL_Renderer *render, const char *src)
{
	SDL_Surface *img = IMG_Load("SS1.jpg");
	if (img == NULL)
	{
		fprintf(stderr, "IMG_Load Error: %s\n", IMG_GetError());
		return NULL;
	}
	SDL_Texture *txt = SDL_CreateTextureFromSurface(render, img);
	SDL_FreeSurface(img);

	return txt;
}

//Load audio
extern "C" Mix_Music *loadMusic(const char *src)
{
	Mix_Music *msc = Mix_LoadMUS(src);
	if (msc == NULL)
	{
		fprintf(stderr, "Mix_LoadMUS Error: %s\n", Mix_GetError());
		return NULL;
	}
	return msc;
}

//Load font
extern "C" SDL_Texture *loadText(SDL_Renderer *render, const char *msg)
{
	if (TTF_Init() == -1)
	{
		fprintf(stderr, "TTF_Init Error: %s\n", TTF_GetError());
		return NULL;
	}
	TTF_Font *fnt = TTF_OpenFont("/system/fonts/Roboto-Regular.ttf", 256);
	if (fnt == NULL)
	{
		fprintf(stderr, "TTF_OpenFont Error: %s\n", TTF_GetError());
		return NULL;
	}
	SDL_Color color = {255, 255, 255};
	SDL_Surface *srf = TTF_RenderText_Solid(fnt, msg, color);
	SDL_Texture *txt = SDL_CreateTextureFromSurface(render, srf);
	SDL_FreeSurface(srf);
	if (txt == NULL)
	{
		fprintf(stderr, "SDL_CreateTextureFromSurface Error: %s\n", SDL_GetError());
		return NULL;
	}
	return txt;
}

//Main Class
int main(int argc, char **argv)
{
	//Initialize SDL
	SDL_Event event;
	bool quit = false;
	SDL_Init(SDL_INIT_EVERYTHING);

	//Surfaces
	SDL_Window *window = SDL_CreateWindow("Hello World", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 300, 300, 0);
	//SDL_Surface * srf = SDL_GetWindowSurface(window);
	//SDL_FillRect(srf,NULL,SDL_MapRGB(srf->format,0xEE,0xAA,0xFF));
	SDL_Renderer *render = SDL_CreateRenderer(window, -1, 0);

	//Mixer
	Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 4096);
	Mix_Music *msc = loadMusic("snd.mp3");
	Mix_PlayMusic(msc, 1);

	//Loop
	while (!quit)
	{
		//Events
		SDL_WaitEvent(&event);
		switch (event.type) {
			case SDL_QUIT:
				quit = true;
				break;
			case SDL_MOUSEBUTTONDOWN:
				printf("click");
		}

		//Draw
		SDL_RenderClear(render);

		int w, h;
		SDL_GetRendererOutputSize(render, &w, &h);
		SDL_Rect dest;
		dest.x = 0;
		dest.y = 0;
		dest.w = w;
		dest.h = w;

		SDL_Texture * lst[2];
		lst[0] = loadImage(render, "SS1.jpg");
		lst[1] = loadText(render, "Hello, world!");
		for (int i = 0; i < 2; i++)
		{
			SDL_RenderCopy(render, lst[i], NULL, &dest);
			SDL_DestroyTexture(lst[i]);
		}

		SDL_RenderPresent(render);
		SDL_UpdateWindowSurface(window);
		
		int ct;
		ct = SDL_GetTicks();
		printf("Ticks: %d\n",ct);
	}

	//Terminate SDL
	Mix_FreeMusic(msc);
	Mix_CloseAudio();
	SDL_DestroyRenderer(render);
	SDL_DestroyWindow(window);
	SDL_Quit();
	return 0;
}