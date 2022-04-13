import espeak

espeak.init()
spk = espeak.Espake()
#espeak.set_voice('')
spk.say('Hello World!')
#spk.rate(300)

#while espeak.is_playing: pass