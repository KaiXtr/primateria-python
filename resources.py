from PIL import Image
import sqlite3
import pygame
import os

GNAME = 'Setesalém: Mutation Purge'
AUTHOR = 'Matt Kai'
DESCRIPTION = 'Setesalém: Mutation Purge (2021)'
VERSION = 'BETA 0.1'
YEAR = '2021'
MAINLANG = 'PT'
DEBUG = True
GSCALE = 2 #game ratio ÷ window ratio
FPS = 30

BACKG_PATH = 'backgrounds/'
SPRITES_PATH = 'sprites/'
CHARS_PATH = 'sprites/characters/'
TEMP_PATH = 'sprites/templates/'
ITEMS_PATH = 'sprites/items/it_'
FREAKS_PATH = 'sprites/freaks/frk_'
SFX_PATH = 'sfx/'
MUSIC_PATH = 'music/'
MAPS_PATH = 'maps/'
TILES_PATH = 'tiles/'
TILESETS_PATH = 'tiles/files/'
FONTS_PATH = 'fonts/'

#None/camera/move/walk/look/squat/shoot/jump/run/bomb/equip
CLICK = ['move',None]
ACTION = ['walk','walk','walk','walk','equip','run','inventory','pause']

SPRITES = {}
SOUND = {}
RADIO = {
0: ['Astronomy Domine','Pow .R Toc .H','Take Up Thy Stethoscope And Walk','Bike'],
1: ['Adeus Maria Fulô','A Day in the Life','Ouro de Tolo','mr_kite'],
2: ['Dreamcast','Infinite Login','my_pain','cattle_king'],
3: ['Polythene Pam','Save Me','from_russia_with_love'],
4: ['Duplo Andantes','hey_sam','urban_plague','wacky_ways'],
5: ['Sombra ou Dúvida','Elogio á Intuição do Cinismo','Give it Away'],
6: ['Discipline','Elephant Talk','she_left_me','mayanman']
}

PALETTES = [
#SKIN COLOR
[(63,37,0),(153,92,58),(206,138,78),(226,157,97),(234,161,100),(234,154,107),(235,185,139),(247,202,163),(255,215,168),(255,231,204)],
#HAIR COLOR
[(76,39,17),(114,65,32),(165,95,48),(255,191,0),(119,7,0),(255,255,255),(63,255,0),(84,39,0),(255,144,0)],
#SHIRT COLOR
[(200,10,10),(200,100,10),(200,200,10),(10,200,10),(10,200,100),(10,10,200),(200,10,200)]
]
RANGE_BUMP = 27
RANGE_HAIR = 8
RANGE_FACE = 6
RANGE_COSTUME = 2
RANGE_SKIN = len(PALETTES[0])
RANGE_RADIO = 7
RANGE_BORDER = 7
RANGE_CURSOR = 6

FILES = []
ID = 0
LANG = 'PT'
GAMETIME = 0
CHAPTER = 0
MAP = None
PX = 0
PY = 0
SIGNAL = 1
TIME = [0,0,0] #hour-minute-second
DATE = [0,0,0,1,1] #day-month-year-week-moon
TEMPERATURE = 25
WEATHER = 0
CHAPTER = 0
SCENE = 0

SFX = 1.0
MSC = 1.0
CONTROLS = [[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,
pygame.K_g,pygame.K_h,pygame.K_RETURN,pygame.K_BACKSPACE],
[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,
pygame.K_KP0,pygame.K_KP_ENTER,pygame.K_KP_MULTIPLY,pygame.K_KP_MINUS]]
JOYSTICK = [0,1,2,3,4,5,6,7,None,None,None,8,None,6,7,0,1,2,3,0,1,None,None]
MOUSE = 2 #keyboard only/keyboard and mouse/touchpad/joystick
VIBRATE = False
DTYPE = 1
SPEED = 2
COLOR = [255,10,10]
CAMACC = 10
BORDER = 0
FONT = 'BohemianTypewriter.ttf'
CENSORSHIP = True
HINT = True
HELP = True
CURSOR = 0
TMNU = False
TTS = False
CC = False
DISLEXIC = False
BTYPE = 2 #1=turns,2=dynamic,3=action

PARTY = [[0,4,3]]
FORMATION = 0
CALLHIST = []
CONTACTS = []
INBOX = []
TASKS = []
TACTICAL = []
BESTIARY = []
INVENTORY = []
STORAGE = []
PRODUCTS = []
for i in range(25): PRODUCTS.append(['_',1])
BASKET = []
for i in range(25): BASKET.append(['_','0000'])
WASH = []
RANK = []

GAS = 100.0
SHORTCUT = [1,0,1]

TASKPIN = False
MINIMAP = False

CHARACTERS = [
{'NAME': 'Sidney','LASTNAME': 'Barreto','PRONOUN': 'he','ID': '0064','BLOOD': 'A+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'mercenary','SUBCLASS': 'gunslinger',
'HAIR': [0,1,0],'SKIN': 5,
'FAVFOOD': ['food_coxinha','drink_whisky'],
'FEAR': 'psychic','FLAW': 'alcoholic'},
  
{'NAME': 'Jane', 'LASTNAME': 'Oliveira','PRONOUN': 'she','ID': '0094','BLOOD': 'O-','CIVIL': 'casada','SIGN': 1,'CLASS': 'medium','SUBCLASS': 'necromancer',
'HAIR': [0,2,0],'SKIN': 4,
'FAVFOOD': ['food_chesse_bread','food_coffee'],
'FEAR': 'reptile','FLAW': 'myopia'},
  
{'NAME': 'Renan', 'LASTNAME': 'Pinheiro','PRONOUN': 'he','ID': '0100','BLOOD': 'A-','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'thief','SUBCLASS': 'smartass',
'HAIR': [0,3,7],'SKIN': 6,
'FAVFOOD': ['food_cola','food_cake_carrot'],
'FEAR': 'mammal','FLAW': 'asthma'},
 
{'NAME': 'Diego', 'LASTNAME': 'Donovan','PRONOUN': 'he','ID': '0024','BLOOD': 'A-','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'hunter','SUBCLASS': 'researcher',
'HAIR': [0,4,1],'SKIN': 8,
'FAVFOOD': ['food_burguer','food_cola'],
'FEAR': 'plant','FLAW': 'lactose intolerant'},
  
{'NAME': 'Bianca', 'LASTNAME': 'Pacheco','PRONOUN': 'she','ID': '0120','BLOOD': 'O+','CIVIL': 'casada','SIGN': 1,'CLASS': 'scientist','SUBCLASS': 'healer',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,
'HAIR': [0,5,0],'SKIN': 9,
'FAVFOOD': ['food_sushi','food_juice_orange'],
'FEAR': 'spirit','FLAW': 'celiac'},
 
{'NAME': 'Lúcia', 'LASTNAME': 'Figueiredo','PRONOUN': 'she','ID': '0013','BLOOD': 'O+','CIVIL': 'viúva','SIGN': 1,'CLASS': 'watchman','SUBCLASS': 'detective',
'HAIR': [0,6,0],'SKIN': 1,
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'inorganic','FLAW': 'cigarette addict'},

{'NAME': 'Maicon', 'LASTNAME': 'Neves','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'hunter','SUBCLASS': 'warrior',
'HAIR': [0,1,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'BONUS': [0,0,0,0,0],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Iago', 'LASTNAME': 'Dantas','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'comprometido','SIGN': 1,'CLASS': 'nomad','SUBCLASS': 'traveler',
'HAIR': [0,14,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Vinicíus', 'LASTNAME': 'Tavares','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'mercenary','SUBCLASS': 'barbarian',
'HAIR': [0,3,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'João', 'LASTNAME': 'Pedro Lima','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'watchman','SUBCLASS': 'forensic',
'HAIR': [0,3,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Sofia', 'LASTNAME': 'Torres','PRONOUN': 'she','ID': '0013','BLOOD': 'O+','CIVIL': 'casada','SIGN': 1,'CLASS': 'scientist','SUBCLASS': 'healer',
'HAIR': [0,12,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Paulo', 'LASTNAME': 'Sousa','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'casado','SIGN': 1,'CLASS': 'watchman','SUBCLASS': 'shooter',
'HAIR': [0,0,6],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Pietra', 'LASTNAME': 'Amaral','PRONOUN': 'she','ID': '0013','BLOOD': 'O+','CIVIL': 'comprometida','SIGN': 1,'CLASS': 'thief','SUBCLASS': 'assassin',
'HAIR': [0,8,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Hermes', 'LASTNAME': 'Fonseca','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'viúvo','SIGN': 1,'CLASS': 'alchemist','SUBCLASS': 'sorcerer',
'HAIR': [0,13,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Dalibor', 'LASTNAME': 'Marković','PRONOUN': 'he','ID': '0013','BLOOD': 'O+','CIVIL': 'viúvo','SIGN': 1,'CLASS': 'watchman','SUBCLASS': 'detective',
'HAIR': [0,13,0],'SKIN': '0',
'FAVFOOD': ['food_juice_orange','food_fish'],
'FEAR': 'psychic','FLAW': 'alcoholic'}
]

for i in range(len(CHARACTERS)):
	CHARACTERS[i]['BONUS'] = [0,0,0,0,0]
	CHARACTERS[i]['HUNGER'] = 1000
	CHARACTERS[i]['THIRST'] = 1000
	CHARACTERS[i]['SLEEP'] = 1000
	for j in ['LEVEL','BLESS','HP','XP','HEALTH','MORALITY','INSPIRATION','INTIMIDATION','PERSUASION','ANIMALS','SPIRITS','STAMINA','ATLETISM',
	'ACROBATICS','FURTIVITY','PERCEPTION','MEDICINE','IMUNITY','INFANTRY','INVESTIGATION','CRAFTING','CULINARY','DEATHS']:
		CHARACTERS[i][j] = 0

RELATIONS = []
for i in range(15):
	RELATIONS.append([])
	for j in range(15):
		if i > j:
			RELATIONS[i].append(RELATIONS[j][i])
		elif i == j:
			RELATIONS[i].append(0)
		else:
			RELATIONS[i].append(0)
RELATIONS[0][3] = 70
RELATIONS[0][5] = 10
RELATIONS[0][6] = 30
RELATIONS[0][11] = 10
RELATIONS[0][12] = 60
RELATIONS[1][7] = 80
RELATIONS[2][8] = 50
RELATIONS[2][12] = 70
RELATIONS[3][0] = 80
RELATIONS[3][9] = 70
RELATIONS[4][10] = 70
RELATIONS[5][11] = 50

DLGSAV = {}
DISITEMS = {}

MARKER = [['1urban_0',300,300,1],['1urban_0',200,300,0]]

def recent_data(m,opt=0):
	global FILES, ID, CHAPTER, GAMETIME, LANG, PARTY
	tbl = sqlite3.connect('userdata.db')
	com = tbl.cursor()

	#LOAD FILES
	if m == 0:
		com.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recent'")
		rs = com.fetchone()
		if rs != None:
			FILES = [[],[],[],[],[]]
			com.execute("SELECT id from recent")
			for i in com.fetchall(): FILES[0].append(i[0])
			com.execute("SELECT chp from recent")
			for i in com.fetchall(): FILES[1].append(i[0])
			com.execute("SELECT gt from recent")
			for i in com.fetchall(): FILES[2].append(i[0])
			com.execute("SELECT lang from recent")
			for i in com.fetchall(): FILES[3].append(i[0])
			com.execute("SELECT party from recent")
			for i in com.fetchall(): FILES[4].append(i[0])
		else:
			com.execute("CREATE TABLE recent (id integer,chp integer,gt integer,lang text,party text)")
			com.execute("INSERT INTO recent VALUES (0,0,0,'PT','0')")
			tbl.commit()
			FILES = [[0],[0],[0],['PT'],['0']]
	#UPDATE FILE
	elif m == 1:
		prt = ''
		for i in PARTY[FORMATION]:
			prt += str(i)
		com.execute("UPDATE recent SET chp = {}, gt = {}, lang = '{}', party = '{}' WHERE id = {}".format(CHAPTER,GAMETIME,LANG,prt,opt))
		tbl.commit()
	#NEW FILE
	elif m == 2:
		ID = opt
		CHAPTER = 0
		GAMETIME = 0
		LANG = 'PT'
		FILES[0].append(ID)
		FILES[1].append(CHAPTER)
		FILES[2].append(GAMETIME)
		FILES[3].append(LANG)
		FILES[3].append('0')
		com.execute("INSERT INTO recent VALUES (" + str(ID) + "," + str(CHAPTER) + "," + str(GAMETIME) + ",'" + LANG + "','0')")
		tbl.commit()
	#ADD FILE
	elif m == 3:
		ID = opt
		prt = ''
		for i in PARTY[FORMATION]:
			prt += str(i)
		FILES[0].append(ID)
		FILES[1].append(CHAPTER)
		FILES[2].append(GAMETIME)
		FILES[3].append(LANG)
		FILES[4].append(prt)
		com.execute("INSERT INTO recent VALUES (" + str(ID) + "," + str(CHAPTER) + "," + str(GAMETIME) + ",'" + LANG + "','" + prt + "')")
		tbl.commit()
	com.close()
	tbl.close()

def new_data(add=False):
	global ID, LANG, SFX, MSC, CONTROLS, SPEED, COLOR, INVENTORY, STORAGE, WASH, RANK, WEATHER, BORDER, CHARACTERS, TASKPIN, MINIMAP, SCENE, CENSORSHIP, HINT, HELP,\
	FORMATION, MAP, PX, PY, TIME, DATE, CHAPTER, GAS, GAMETIME, PARTY, CONTACTS, CALLHIST, INBOX, TASKS, TACTICAL, BESTIARY, ACHIEVEMENTS, DISITEMS, RELATIONS
 
	tbl = sqlite3.connect('userdata.db')
	com = tbl.cursor()
	
	if add == False:
		LANG = 'PT'
		SFX = 1.5
		MSC = 0.0
		CONTROLS = [[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,
		pygame.K_g,pygame.K_h,pygame.K_RETURN,pygame.K_RETURN,pygame.K_BACKSPACE],
		[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,
		pygame.K_KP0,pygame.K_KP_ENTER,pygame.K_KP_PLUS,pygame.K_KP_MULTIPLY,pygame.K_KP_MINUS]]
		MOUSE = 2
		CURSOR = 0
		SPEED = 2
		COLOR = [242,30,30]
		BORDER = 0
		FONT = 'BohemianTypewriter.ttf'
		CENSORSHIP = True
		HINT = True
		HELP = True
		DISLEXIC = False
		BTYPE = 2
		
		TIME = [0,32,0]
		DATE = [25,12,2007,1,1]
		WEATHER = 0
		CHAPTER = 6
		SCENE = 0
		GAMETIME = 0
		FORMATION = 0
		MAP = dtb.CHAPTERS[CHAPTER][5][0]
		PX = dtb.CHAPTERS[CHAPTER][5][1]
		PY = dtb.CHAPTERS[CHAPTER][5][2]
		MAP = 'labyrinth_1'
		PX = 90
		PY = 90
		
		GAS = 100.0
		SHORTCUT = [1,1,4]
		 
		for i in range(6):
			'''CHARACTERS[i]['NAME'] = ''
			CHARACTERS[i]['LASTNAME'] = '''
			CHARACTERS[i]['LEVEL'] = 0
			CHARACTERS[i]['XP'] = 90
			CHARACTERS[i]['BONUS'] = [3,3,3,3,3]
			CHARACTERS[i]['DEATHS'] = 0
	 
		PARTY = [[1,2,0]]
		CONTACTS = [['Maicon','923778988'],['Mercador','969696969'],['Pizza Delivery','953478809']]
		CALLHIST = []
		INBOX = []
		TASKS = [['LVL_00_0',0]]
		TACTICAL = [[1,1,1,1]]
		for i in dtb.ITEMS.items():
			if i[0].startswith('food'):
				DISITEMS[i[0]] = 0
			if i[0].startswith('drug'):
				DISITEMS[i[0]] = 0
		BESTIARY = []
		for i in dtb.FREAKS.items(): BESTIARY.append({'N': i[0],'ID': 'xxxx','DATE': '000000','SEEN': 0})
		for i in dtb.ACHIEVEMENTS:
			i[2] = 0
			i[3] = ''

		INVENTORY = []
		for u in range(6):
			INVENTORY.append([])
			for y in range(5):
				INVENTORY[u].append([])
				for x in range(5):
					INVENTORY[u][y].append(['_','0000'])
		INVENTORY[1] = [
		[['amulet1','0000'],['phone','3600','sim_card','0003'],['tube100','0050'],['wallet','0100','creditcard1','0100','id_card1','0000'],['food_pizza_chicken','9999']],
		[['vest1','7'],['til_grass','infinite'],['til_color','infinite'],['til_metalbars','infinite'],['food_pizza_4cheese','0000']],
		[['head_glasses1','0000'],['guit_load','0'],['guit_save','0000'],['guit_undo','0000'],['guit_redo','0000']],
		[['head_hairclip','0000'],['guit_pencil','0000'],['guit_erase','0000'],['guit_dropper','0000'],['_','0000']],
		[['bag1','0000'],['bomb_regular','3'],['pow_triplebubble','3'],['cigar','0000'],['_','0000']]
		]
	 
		STORAGE = [['jewel_ruby','0000'],['drink_whiskey','1503']]
		for i in range(23): STORAGE.append(['_','0000'])
		WASH = [] #[('clth_shirt00','0000','0000')]
		RANK = []
	
	#CREATE TABLES
	com.execute("CREATE TABLE IF NOT EXISTS settings (id integer,lang text,sfx integer,msc integer,ctrl integer,mouse integer,cursor integer,speed integer,color1 integer,color2 integer,color3 integer,border integer,\
			font text,censor integer,hint integer,help integer,btype integer,dislexic integer)")
	com.execute("CREATE TABLE IF NOT EXISTS controls (id integer,player integer,key integer,value integer)")
	com.execute("CREATE TABLE IF NOT EXISTS paths (id integer,backg text,sprites text,chars text,temp text,items text,freaks text,sfx text,music text,maps text,tiles text,fonts text)")
	com.execute("CREATE TABLE IF NOT EXISTS data (id integer,gt integer,fr integer,map text,x integer,y integer,time text,date text,weather integer,chapter integer,scene integer,\
			gas integer,shortcut text)")
	com.execute("CREATE TABLE IF NOT EXISTS characters (id integer,n integer,name text,lastname text,level integer,hp integer,xp integer,health integer,morality integer,hc integer,ht integer,fh integer,\
	hunger integer,thirst integer,sleep integer,b1 integer,b2 integer,b3 integer,b4 integer,b5 integer,inspiration integer,intimidation integer,persuasion integer,animals integer,spirits integer,\
	stamina integer,atletism integer,acrobatics integer,furtivity integer,perception integer,medicine integer,imunity integer,\
	infantry integer,investigation integer,crafting integer,culinary integer,deaths integer)")
	com.execute("CREATE TABLE IF NOT EXISTS chapters (id integer,n integer,progress integer)")
	com.execute("CREATE TABLE IF NOT EXISTS dlgsav (id integer,who text,vl integer)")
	com.execute("CREATE TABLE IF NOT EXISTS disitems (id integer,it text,vl integer)")
	com.execute("CREATE TABLE IF NOT EXISTS relations (id integer,w1 integer,w2 integer,vl integer)")
	com.execute("CREATE TABLE IF NOT EXISTS party (id integer,n integer,p1 integer,p2 integer,p3 integer)")
	com.execute("CREATE TABLE IF NOT EXISTS contacts (id integer,n integer)")
	com.execute("CREATE TABLE IF NOT EXISTS callhist (id integer,n integer,w integer)")
	com.execute("CREATE TABLE IF NOT EXISTS inbox (id integer,n integer,red integer)")
	com.execute("CREATE TABLE IF NOT EXISTS tasks (id integer,tsk text,don integer)")
	com.execute("CREATE TABLE IF NOT EXISTS tactical (id integer,n integer,pl1 integer,pl2 integer,pl3 integer,pl4 integer)")
	com.execute("CREATE TABLE IF NOT EXISTS bestiary (id integer,name text,nb text,date text,seen int)")
	com.execute("CREATE TABLE IF NOT EXISTS achievements (id integer,nb integer,got integer,date text)")
	com.execute("CREATE TABLE IF NOT EXISTS inventory (id integer,item text,position text,properties text)")
	com.execute("CREATE TABLE IF NOT EXISTS storage (id integer,it text,ip text)")
	com.execute("CREATE TABLE IF NOT EXISTS wash (id integer,it text,nb text,date text)")
	com.execute("CREATE TABLE IF NOT EXISTS rank (id integer,chp integer,level integer,score integer,time integer,paint integer,enemies integer,deaths integer)")
	  
    #FILE ALREADY EXISTS
	for i in ['recent','settings','data','characters','party','contacts',
	'callhist','inbox','tasks','tactical','bestiary','achievements','inventory',
	'storage','wash','rank']:
		com.execute("DELETE FROM " + i + " WHERE id=" + str(ID))
	
	#INSERT NEW VALUES
	com.execute("INSERT INTO settings VALUES ({},'PT',0.8,0.6,0,0,2,2,242,30,30,0,'BohemianTypewriter.ttf',1,1,1,2,0)".format(ID))
	for i in range(len(CONTROLS)):
		for l in range(len(CONTROLS[i])): com.execute("INSERT INTO controls VALUES ({},{},{},{})".format(ID,i,l,CONTROLS[i][l]))
	com.execute("INSERT INTO paths VALUES (0,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(BACKG_PATH,SPRITES_PATH,CHARS_PATH,TEMP_PATH,ITEMS_PATH,FREAKS_PATH,SFX_PATH,MUSIC_PATH,MAPS_PATH,TILES_PATH,FONTS_PATH))
	com.execute("INSERT INTO data VALUES ({},0,0,'hauntedhouse_0',0,0,'0030','2512200711',0,0,0,10,'001')".format(ID))
	for i in range(len(CHARACTERS)): com.execute("INSERT INTO characters VALUES({},{},'','',0,0,0,0,0,100,100,10000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)".format(ID,i))
	for i in range(len(dtb.CHAPTERS)): com.execute("INSERT INTO chapters VALUES ({},{},0)".format(ID,i))
	for i in DLGSAV:
		com.execute("INSERT INTO dlgsav VALUES({},'{}',0)".format(ID,i))
	for i in DISITEMS:
		com.execute("INSERT INTO disitems VALUES({},'{}',0)".format(ID,i))
	com.execute("INSERT INTO party VALUES({},0,1,2,0)".format(ID))
	for i in range(15):
		for j in range(15):
			com.execute("INSERT INTO relations VALUES({},'{}','{}',0)".format(ID,str(i),str(j)))
	for i in dtb.FREAKS.items(): com.execute("INSERT INTO bestiary VALUES({},'{}','xxxxxx','000000',0)".format(ID,i[0]))
	for u in range(6):
		for x in range(5):
			for y in range(5):
				com.execute("INSERT INTO inventory VALUES({},'_','{}{}{}0','0000')".format(ID,u,x,y))
	for i in range(25): com.execute("INSERT INTO storage VALUES({},'_','0000')".format(ID))
	for i in range(len(dtb.CHAPTERS)):
		for l in range(8): com.execute("INSERT INTO rank VALUES ({},{},{},0,0,0,0,0)".format(ID,i,l))
	
	tbl.commit()
	com.close()
	tbl.close()

def load_data():
	global ID, LANG, SFX, MSC, CONTROLS, MOUSE, CURSOR, SPEED, COLOR, FONT, WEATHER, BORDER, TASKPIN, MINIMAP, SCENE, CENSORSHIP, HINT, HELP, BTYPE, DISLEXIC,\
	FORMATION, MAP, PX, PY, TIME, DATE, CHAPTER, GAS, GAMETIME, PARTY, CONTACTS, CALLHIST, INBOX, TASKS, TACTICAL, BESTIARY, INVENTORY, STORAGE, WASH, DISITEMS, RELATIONS
	  
	tbl = sqlite3.connect('userdata.db')
	com = tbl.cursor()
	
	com.execute("SELECT lang,sfx,msc,ctrl,cursor,mouse,speed,color1,color2,color3,border,font,censor,hint,help,btype,dislexic FROM settings WHERE id=" + str(ID))
	vl = com.fetchall()[0]
	print(vl)
	LANG = vl[0]
	SFX = vl[1]
	MSC = vl[2]
	ctrl = vl[3]
	MOUSE = vl[4]
	CURSOR = vl[5]
	SPEED = vl[6]
	COLOR = [vl[7],vl[8],vl[9]]
	BORDER = vl[10]
	FONT = vl[11]
	CENSORSHIP = bool(vl[12])
	HINT = bool(vl[13])
	HELP = bool(vl[14])
	BTYPE = vl[15]
	DISLEXIC = bool(vl[16])
	
	CONTROLS = []
	for p in range(2):
		com.execute("SELECT value FROM controls WHERE id={} AND p={} ORDER BY key".format(ctrl,p))
		CONTROLS.append(com.fetchall()[0])
	
	com.execute("SELECT gt,fr,map,x,y,time,date,weather,chapter,scene,gas,shortcut FROM data WHERE id=" + str(ID))
	vl = com.fetchall()[0]
	GAMETIME = vl[0]
	FORMATION = vl[1]
	MAP = vl[2]
	PX = vl[3]
	PY = vl[4]
	TIME = [int(vl[5][0:2]),int(vl[5][2:4]),0]
	DATE = [int(vl[6][0:2]),int(vl[6][2:4]),int(vl[6][4:8]),int(vl[6][8]),int(vl[6][9])]
	WEATHER = vl[7]
	CHAPTER = vl[8]
	SCENE = vl[9]
	GAS = vl[10]
	SHORTCUT = [int(vl[11][0]),int(vl[11][1]),(vl[11][2])]
	
	com.execute("SELECT * FROM characters WHERE id=" + str(ID))
	res = com.fetchall()
	for i in range(len(CHARACTERS)):
		ix = 2
		for ch in ['NAME','LASTNAME','LEVEL','HP','XP','HEALTH','MORALITY','HAIR','HUNGER','THIRST','SLEEP','BONUS','INSPIRATION','INTIMIDATION','PERSUASION','ANIMALS','SPIRITS','STAMINA','ATLETISM','ACROBATICS','FURTIVITY','PERCEPTION','MEDICINE','IMUNITY','INFANTRY','INVESTIGATION','CRAFTING','CULINARY','DEATHS']:
			if ch == 'HAIR': CHARACTERS[i][ch] = [res[i][ix],res[i][ix + 1],res[i][ix + 2]]; ix += 3
			elif ch == 'BONUS': CHARACTERS[i][ch] = [res[i][ix],res[i][ix + 1],res[i][ix + 2],res[i][ix + 3],res[i][ix + 4]]; ix += 5
			else: CHARACTERS[i][ch] = res[i][ix]; ix += 1
	com.execute("SELECT * FROM dlgsav WHERE id=" + str(ID))
	res = com.fetchall()
	for i in res: DLGSAV[i[0]] = i[1]
	com.execute("SELECT * FROM disitems WHERE id=" + str(ID))
	res = com.fetchall()
	for i in res: DISITEMS[i[0]] = i[1]
	com.execute("SELECT * FROM relations WHERE id=" + str(ID))
	res = com.fetchall()
	for i in res: RELATIONS[i[0]][i[1]] = i[2]
	com.execute("SELECT * FROM party WHERE id=" + str(ID) + " ORDER BY n")
	res = com.fetchall()
	PARTY = []
	for i in res: PARTY.append([i[2],i[3],i[4]])
	com.execute("SELECT * FROM contacts WHERE id=" + str(ID))
	res = com.fetchall()
	CONTACTS = []
	for i in res: CONTACTS.append(NUMBERS[i[0]].copy())
	CONTACTS = [['Maicon','923778988'],['Mercador','969696969'],['Pizza Delivery','953478809']]
	com.execute("SELECT * FROM callhist WHERE id=" + str(ID))
	res = com.fetchall()
	CALLHIST = []
	for i in res: CALLHIST.append([i[0],i[1]])
	com.execute("SELECT * FROM inbox WHERE id=" + str(ID))
	res = com.fetchall()
	INBOX = []
	for i in res:
		mail = EMAILS[i[0]].copy()
		mail.append(i[1])
		INBOX.append(mail)
	com.execute("SELECT * FROM tasks WHERE id=" + str(ID))
	res = com.fetchall()
	TASKS = []
	for i in res: TASKS.append([i[0],i[1]])
	com.execute("SELECT * FROM tactical WHERE id=" + str(ID))
	res = com.fetchall()
	TACTICAL = []
	for i in res: TACTICAL.append([i[2],i[3],i[4],i[5]])
	com.execute("SELECT * FROM bestiary WHERE id=" + str(ID))
	res = com.fetchall()
	BESTIARY = []
	for i in res:
		BESTIARY.append({'N': i[1],'ID': i[2],'DATE': i[3],'SEEN': i[4]})
	com.execute("SELECT * FROM achievements WHERE id="+ str(ID))
	res = com.fetchall()
	for i in res:
		dtb.ACHIEVEMENTS[i[1]][2] = i[2]
		dtb.ACHIEVEMENTS[i[1]][3] = i[3]
	if res == []:
		for i in dtb.ACHIEVEMENTS:
			i[2] = 0
			i[3] = ''
	com.execute("SELECT * FROM inventory WHERE id="+ str(ID))
	res = com.fetchall()
	INVENTORY = []
	for u in range(6):
		INVENTORY.append([])
		for y in range(5):
			INVENTORY[u].append([])
			for x in range(5):
				for i in res:
					if int(i[2][0]) == u and int(i[2][1]) == y and int(i[2][2]) == x:
						if len(INVENTORY[u][y]) <= x:
							INVENTORY[u][y].append([])
						INVENTORY[u][y][x].append(i[1])
						INVENTORY[u][y][x].append(i[3])
	com.execute("SELECT * FROM storage WHERE id="+ str(ID))
	res = com.fetchall()
	STORAGE = []
	for i in res:
		STORAGE.append([i[1],i[2]])
	com.execute("SELECT * FROM wash WHERE id="+ str(ID))
	res = com.fetchall()
	WASH = []
	for i in res:
		WASH.append([i[1],i[2],i[3]])
	com.execute("SELECT * FROM rank WHERE id="+ str(ID))
	res = com.fetchall()
	RANK = []
	for i in res:
		RANK.append([])
	com.close()
	tbl.close()

def save_data(t):
	global ID, MAP, PX, PY, TIME, DATE, WEATHER, CHAPTER, GAS, GAMETIME, FORMATION, CHARACTERS, TASKPIN, MINIMAP, DLGSAV, SCENE, BESTIARY
 
	tbl = sqlite3.connect('userdata.db')
	com = tbl.cursor()
	
	#REGULAR SAVING
	if t == 0:
		if TIME[0] < 10: hr = '0' + str(TIME[0])
		else: hr = str(TIME[0])
		if TIME[1] < 10: mn = '0' + str(TIME[1])
		else: mn = str(TIME[1])
		ts = hr + mn
		
		if DATE[0] < 10: dd = '0' + str(DATE[0])
		else: dd = str(DATE[0])
		if DATE[1] < 10: mm = '0' + str(DATE[1])
		else: mm = str(DATE[1])
		if DATE[2] < 10: yy = '0' + str(DATE[2])
		else: yy = str(DATE[2])
		dt = dd + mm + yy + str(DATE[3]) + str(DATE[4])
		st = str(SHORTCUT[0]) + str(SHORTCUT[1]) + str(SHORTCUT[2])
		#SAVE GLOBAL GAME DATA
		com.execute("UPDATE data SET gt = {},fr = {},map = '{}',x = {},y = {},time = '{}',date = '{}',weather = {},chapter = {},scene = {},gas = {},\
			shortcut = {} WHERE id = {}".format(GAMETIME,FORMATION,MAP,PX,PY,ts,dt,WEATHER,CHAPTER,SCENE,GAS,st,ID))
		#SAVE CHARACTERS DATA
		p = 0
		for i in CHARACTERS:
			com.execute("UPDATE characters SET name = '{}',lastname = '{}',level = {},hp = {},xp = {},health = {},morality = {},hc = {},ht = {},fh = {},hunger = {},thirst = {},sleep = {},b1 = {},b2 = {},b3 = {},b4 = {},b5 = {},\
				inspiration = {},intimidation = {},persuasion = {},animals = {},spirits = {},stamina = {},atletism = {},acrobatics = {},furtivity = {},perception = {},\
				medicine = {},imunity = {},infantry = {},investigation = {},crafting = {},culinary = {},deaths = {} WHERE n = {} AND id = {}".format(i['NAME'],i['LASTNAME'],i['LEVEL'],
					i['HP'],i['XP'],i['HEALTH'],i['MORALITY'],i['HAIR'][0],i['HAIR'][1],i['HAIR'][2],i['HUNGER'],i['THIRST'],i['SLEEP'],i['BONUS'][0],i['BONUS'][1],i['BONUS'][2],i['BONUS'][3],i['BONUS'][4],i['INSPIRATION'],i['INTIMIDATION'],i['PERSUASION'],
					i['SPIRITS'],i['ANIMALS'],0,i['ATLETISM'],i['ACROBATICS'],i['FURTIVITY'],i['PERCEPTION'],i['MEDICINE'],i['IMUNITY'],
					i['INFANTRY'],i['INVESTIGATION'],i['CRAFTING'],i['CULINARY'],i['DEATHS'],p,ID))
			p += 1
		#SAVE DIALOGS DATA
		for i in DLGSAV:
			com.execute("UPDATE dlgsav SET vl = {} WHERE who = '{}' AND id={}".format(DLGSAV[i],i,ID))
		#SAVE DISCOVERED ITEMS DATA
		for i in DISITEMS:
			com.execute("UPDATE disitems SET vl = {} WHERE it = '{}' AND id = {}".format(DISITEMS[i],i,ID))
		#SAVE RELATIONS DATA
		for i in range(len(RELATIONS)):
			for j in range(len(RELATIONS[i])):
				com.execute("UPDATE relations SET vl = {} WHERE w1 = '{}' and w2 = '{}' AND id = {}".format(RELATIONS[i][j],i,j,ID))
		#SAVE PARTY DATA
		com.execute("DELETE FROM party WHERE id = " + str(ID))
		p = 0
		for i in PARTY:
			com.execute("INSERT INTO party VALUES({},{},'{}','{}','{}')".format(ID,p,i[0],i[1],i[2]))
			p += 1
		#SAVE TACTICAL DATA
		for i in range(len(TACTICAL)):
			try: com.execute("UPDATE tactical SET p1 = {},p2 = {},p3 = {},p4 = {} WHERE n = {} AND id = {}".format(TACTICAL[i][0],TACTICAL[i][1],TACTICAL[i][2],TACTICAL[i][3],i,ID))
			except: com.execute("INSERT INTO tactical VALUES({},{},{},{},{},{})".format(ID,i,TACTICAL[i][0],TACTICAL[i][1],TACTICAL[i][2],TACTICAL[i][3]))
		#SAVE BESTIARY DATA
		for i in BESTIARY:
			com.execute("UPDATE bestiary SET id = '{}',date = '{}',seen = {} WHERE name = '{}' AND id = {}".format(i['ID'],i['DATE'],i['SEEN'],i['N'],ID))
		#SAVE INVENTORY DATA
		for u in range(len(INVENTORY)):
			for y in range(5):
				for x in range(5):
					for i in range(int(len(INVENTORY[u][y][x])/2)):
						com.execute("DELETE FROM inventory WHERE id = {} AND position = '{}'".format(ID,str(u) + str(y) + str(x) + str(i)))
						com.execute("INSERT INTO inventory VALUES({},'{}','{}','{}')".format(ID,INVENTORY[u][y][x][i * 2],str(u) + str(y) + str(x) + str(i),INVENTORY[u][y][x][(i * 2) + 1]))
		#SAVE STORAGE DATA
		com.execute("DELETE FROM storage WHERE id = " + str(ID))
		for i in STORAGE:
			com.execute("INSERT INTO storage VALUES({},'{}','{}')".format(ID,i[0],i[1]))
		#SAVE WASH DATA
		com.execute("DELETE FROM wash WHERE id = " + str(ID))
		for i in WASH:
			com.execute("INSERT INTO wash VALUES({},'{}','{}','{}')".format(ID,i[0],i[1],i[2]))
		#SAVE RANK DATA
		for i in range(len(RANK)):
			for j in range(len(RANK[i])):
				for p in RANK[i][j]:
					com.execute("UPDATE rank SET score = {},time = {},paint = {},enemies = {},deaths = {} WHERE id = {} AND chp = {} AND level = {}".format(p[0],p[1],p[2],p[3],p[4],ID,i,j))
	#SETTINGS SAVE
	if t == 1:
		com.execute("UPDATE settings SET lang = '{}',sfx = {},msc = {},ctrl = {},mouse = {},cursor = {},speed = {},color1 = {},color2 = {},color3 = {},border = {},\
		font = '{}',censor = {},hint = {},help = {},btype = {},dislexic = {} WHERE id = {}".format(LANG,SFX,MSC,0,MOUSE,CURSOR,SPEED,COLOR[0],COLOR[1],COLOR[2],BORDER,
		FONT,int(CENSORSHIP),int(HINT),int(HELP),BTYPE,DISLEXIC,ID))
	#CONTROLS SAVE
	if t == 2:
		for p in range(3):
			com.execute("UPDATE controls SET up = '{}',down = '{}',left = '{}',right = '{}',act = '{}',run = '{}',pause = '{}',inventory = '{}',device = '{}' WHERE id = {} AND p = {}".format(
			CONTROLS[p][0],CONTROLS[p][1],CONTROLS[p][2],CONTROLS[p][3],CONTROLS[p][4],CONTROLS[p][5],CONTROLS[p][6],CONTROLS[p][7],CONTROLS[p][8],ID,p))
	#ACHIEVEMENTS SAVE
	if t == 3:
		com.execute("UPDATE achievements SET got = {},date = '{}' WHERE nb = {} AND id = {}".format(ACHIEVEMENTS[i][2],ACHIEVEMENTS[i][3],i,ID))
		
	tbl.commit()
	com.close()
	tbl.close()

def delete_data():
	global ID
	tbl = sqlite3.connect('userdata.db')
	com = tbl.cursor()
	
	del FILES[0][ID]
	del FILES[1][ID]
	del FILES[2][ID]
	del FILES[3][ID]
	
	for i in ['recent','settings','data','characters','party','contacts',
	'callhist','inbox','tasks','tactical','bestiary','achievements','inventory',
	'storage','wash','rank']:
		com.execute("DELETE FROM " + i + " WHERE id=" + str(ID))
	
	tbl.commit()
	com.close()
	tbl.close()

def spr():
	global SPRITES
	
	dirs = ['U','LU','L','LD','D','RD','R','RU']
	movs = [('STAND',[0,1,2,3]),('TIREDSTAND',[0,0,1,1]),('SEAT',[0]),('DRIVE',[0]),
	('JUMP',[0,1]),('WALK',[0,1,2,1,0,3,4,3]),('RUN',[0,1,2,1,0,3,4,3])]
	
	SPRITES['PHONE'] = [pygame.image.load(TEMP_PATH + 'body_phone.png')]
	SPRITES['CALL'] = [pygame.image.load(TEMP_PATH + 'body_call.png')]
	SPRITES['REST'] = [pygame.image.load(TEMP_PATH + 'body_rest.png')]
	
	for m in movs:
		for d in dirs:
			trg = True
			if m[0] == 'JUMP' and d not in ['U','D']: trg = False
			if trg == True:
				SPRITES[m[0] + d] = []
				for f in m[1]:
					if m[1] == [0]: fn = ''
					else: fn = '_' + str(f)
					if d == 'LU': spr = pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'HU' + fn + '.png')
					elif d == 'L': spr = pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'H' + fn + '.png')
					elif d == 'LD': spr = pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'HD' + fn + '.png')
					elif d == 'RU': spr = pygame.transform.flip(pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'HU' + fn + '.png'),True,False)
					elif d == 'R': spr = pygame.transform.flip(pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'H' + fn + '.png'),True,False)
					elif d == 'RD': spr = pygame.transform.flip(pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + 'HD' + fn + '.png'),True,False)
					else: spr = pygame.image.load(TEMP_PATH + 'body_' + m[0].lower() + d + fn + '.png')
					SPRITES[m[0] + d].append(spr)
	
def animals():
	global SPRITES
	
	SPRITES['PIGEON_WALKL'] = []
	SPRITES['PIGEON_WALKR'] = []
	SPRITES['PIGEON_FLYL'] = []
	SPRITES['PIGEON_FLYR'] = []
	for i in (0,1):
		SPRITES['PIGEON_WALKL'].append(pygame.transform.flip(pygame.image.load(SPRITES_PATH + 'ani_pigeon_walk_' + str(i) + '.png'),True,False))
		SPRITES['PIGEON_WALKR'].append(pygame.image.load(SPRITES_PATH + 'ani_pigeon_walk_' + str(i) + '.png'))
	for i in (0,1):
		SPRITES['PIGEON_FLYL'].append(pygame.transform.flip(pygame.image.load(SPRITES_PATH + 'ani_pigeon_fly_' + str(i) + '.png'),True,False))
		SPRITES['PIGEON_FLYR'].append(pygame.image.load(SPRITES_PATH + 'ani_pigeon_fly_' + str(i) + '.png'))
	for a in [0]:
		SPRITES['DOG' + str(a) + '_STANDL'] = []
		SPRITES['DOG' + str(a) + '_STANDR'] = []
		SPRITES['DOG' + str(a) + '_SITL'] = []
		SPRITES['DOG' + str(a) + '_SITR'] = []
		SPRITES['DOG' + str(a) + '_WALKL'] = []
		SPRITES['DOG' + str(a) + '_WALKR'] = []
		for i in (0,1):
			SPRITES['DOG' + str(a) + '_STANDL'].append(pygame.transform.flip(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_stand_' + str(i) + '.png'),True,False))
			SPRITES['DOG' + str(a) + '_STANDR'].append(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_stand_' + str(i) + '.png'))
		for i in (0,1):
			SPRITES['DOG' + str(a) + '_SITL'].append(pygame.transform.flip(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_sit_' + str(i) + '.png'),True,False))
			SPRITES['DOG' + str(a) + '_SITR'].append(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_sit_' + str(i) + '.png'))
		for i in (0,1,2,3,4,3,2,1):
			SPRITES['DOG' + str(a) + '_WALKL'].append(pygame.transform.flip(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_walk_' + str(i) + '.png'),True,False))
			SPRITES['DOG' + str(a) + '_WALKR'].append(pygame.image.load(SPRITES_PATH + 'ani_dog' + str(a) + '_walk_' + str(i) + '.png'))

def battlesprites():
	global SPRITES
	
	for a in (1,2,3,9,10):
		SPRITES['ATTACKIMATION_' + str(a)] = []
		i = 0
		while True:
			try:
				SPRITES['ATTACKIMATION_' + str(a)].append(pygame.image.load(SPRITES_PATH + 'attackimation_' + str(a) + '_' + str(i) + '.png'))
				i += 1
			except: break
	for e in (6,8,9):
		SPRITES['EFFECT_' + str(e)] = []
		i = 0
		while True:
			try:
				SPRITES['EFFECT_' + str(e)].append(pygame.image.load(SPRITES_PATH + 'eff_' + str(e) + '_' + str(i) + '.png'))
				i += 1
			except: break

def sfx(j):
	global SOUND
	if j.endswith('.wav'): SOUND[j[:-4].upper()] = pygame.mixer.Sound(SFX_PATH + j)

recent_data(0)
if FILES[3] != []:
	if FILES[3][0] == 'PT': import database_PT as dtb
	if FILES[3][0] == 'EN': import database_EN as dtb
	ID = FILES[0][0]
	CHAPTER = FILES[1][0]
	GAMETIME = FILES[2][0]
	LANG = FILES[3][0]
else: import database_PT as dtb