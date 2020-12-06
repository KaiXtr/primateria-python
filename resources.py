from PIL import Image
import sqlite3
import pygame
import os

VERSION = '0.0.1'
DEBUG = True

SPRITES = {}
SOUND = {}
SONGS = {}
RADIO = {'0': [],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[]}
PALETTES = [
[(198,57,21),(250,250,250),(91,7,0),(153,33,33)]
]

RANGE_HAIR = 8
RANGE_FACE = 6
RANGE_COSTUME = 2
RANGE_SKIN = 10
RANGE_RADIO = 10
RANGE_BORDER = 7
RANGE_CURSOR = 6

FILES = []
ID = 0
LANG = 'PT'
GAMETIME = 0
CHAPTER = 0
MAP = 1
PX = 0
PY = 0
TIME = [0,0,0] #hour-minute-second
DATE = [0,0,0,1,1] #day-month-year-week-moon
WEATHER = 0
CHAPTER = 0
SCENE = 0

SFX = 1.0
MSC = 1.0
UP = [pygame.K_w,pygame.K_UP]
DOWN = [pygame.K_s,pygame.K_DOWN]
LEFT = [pygame.K_a,pygame.K_LEFT]
RIGHT = [pygame.K_d,pygame.K_RIGHT]
ACT = [pygame.K_g,pygame.K_KP0]
RUN = [pygame.K_h,pygame.K_KP_ENTER]
PHONE = [pygame.K_BACKSPACE,pygame.K_KP_MULTIPLY]
BAG = [pygame.K_RETURN,pygame.K_KP_MINUS]
MOUSE = True
SPEED = 2
COLOR = [255,10,10]
BORDER = 0
CENSORSHIP = True
HINT = True
HELP = True
CURSOR = 0

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

GAS = 100.0

TASKPIN = False
MINIMAP = False

CHARACTERS = [
{'NAME': 'Sidney','LASTNAME': 'Barreto','GENDER': 'male','ID': '0064','BLOOD': 'A+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,70,0,10,30,0,0,0,0,10,60,0],
'HAIR': '001', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '5', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_coxinha','drink_whisky'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},
  
{'NAME': 'Jane', 'LASTNAME': 'Oliveira','GENDER': 'female','ID': '0094','BLOOD': 'O-','CIVIL': 'casada','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,80,0,0,0,0,0,0],
'HAIR': '011', 'ACCESORIES': 'head_glasses', 'COSTUME': '01', 'SKIN': '4', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_chesse_bread','food_coffee'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'reptile','FLAW': 'myopia'},
  
{'NAME': 'Renan', 'LASTNAME': 'Pinheiro','GENDER': 'male','ID': '0100','BLOOD': 'A-','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'thief',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,0,50,0,0,0,70,0],
'HAIR': '021', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '6', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_cola','food_cake_carrot'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'mammal','FLAW': 'asthma'},
 
{'NAME': 'Diego', 'LASTNAME': 'Donovan','GENDER': 'male','ID': '0024','BLOOD': 'A-','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [80,0,0,0,0,0,0,0,0,70,0,0,0,0],
'HAIR': '031', 'ACCESORIES': 'head_glasses', 'COSTUME': '00', 'SKIN': '8', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_burguer','food_cola'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'plant','FLAW': 'lactose intolerant'},
  
{'NAME': 'Bianca', 'LASTNAME': 'Pacheco','GENDER': 'female','ID': '0120','BLOOD': 'O+','CIVIL': 'casada','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,0,0,0,70,0,0,0],
'HAIR': '041', 'ACCESORIES': 'head_glasses', 'COSTUME': '01', 'SKIN': '9', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_sushi','food_juice_orange'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'spirit','FLAW': 'myopia'},
 
{'NAME': 'Lúcia', 'LASTNAME': 'Figueiredo','GENDER': 'female','ID': '0013','BLOOD': 'O+','CIVIL': 'viúva','SIGN': 1,'CLASS': 'cop',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,0,0,0,0,50,0,0],
'HAIR': '051', 'ACCESORIES': None, 'COSTUME': '01', 'SKIN': '1', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'inorganic','FLAW': 'cigarette addict'},

{'NAME': 'Maicon', 'LASTNAME': 'Neves','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'hunter',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Iago', 'LASTNAME': 'Dantas','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'comprometido','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [40,0,0,0,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Vinicíus', 'LASTNAME': 'Tavares','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'thief',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,60,0,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'João', 'LASTNAME': 'Pedro Lima','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'solteiro','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,60,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Sofia', 'LASTNAME': 'Torres','GENDER': 'female','ID': '0013','BLOOD': 'O+','CIVIL': 'casada','SIGN': 1,'CLASS': 'mercenary',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,70,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Paulo', 'LASTNAME': 'Sousa','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'casado','SIGN': 1,'CLASS': 'cop',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,70,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None,'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Pietra', 'LASTNAME': 'Amaral','GENDER': 'female','ID': '0013','BLOOD': 'O+','CIVIL': 'comprometida','SIGN': 1,'CLASS': 'thief',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [80,0,80,0,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'},

{'NAME': 'Hermes', 'LASTNAME': 'Paracelso','GENDER': 'male','ID': '0013','BLOOD': 'O+','CIVIL': 'viúvo','SIGN': 1,'CLASS': 'alchemist',
'LEVEL': 0,'BLESS': 0,'HP': 0,'XP': 0,'HEALTH': 0,'MORALITY': 0,'RELATIONS': [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
'HAIR': '000', 'ACCESORIES': None, 'COSTUME': '00', 'SKIN': '0', 'HUNGER': 720, 'THIRST': 360, 'SLEEP': 10000,
'FAVFOOD': ['food_juice_orange','food_fish'],
'CARISM': 0,'INTIMIDATION': 0,'PERSUASION': 0,'ANIMALS': 0,'SPIRITS': 0,'STAMINA': 0,'ATLETISM': 0, 'ACROBATICS': 0,'FURTIVITY': 0,'PERCEPTION': 0,
'MEDICINE': 0,'IMUNITY': 0,'INFANTRY': 0,'INVESTIGATION': 0,'CRAFTING': 0,'COORDENATION': 0,'EXPLOSIVES': 0,'CULINARY': 0,
'FEAR': 'psychic','FLAW': 'alcoholic'}
]

DLGSAV = {}

MARKER = [['1urban_0',30,30],['1urban_0',200,300]]

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
        com.execute("UPDATE recent SET chp = :chp, gt = :gt, lang = :lang, party = :party WHERE id = :id",
            {'id': opt,'chp': CHAPTER,'gt': GAMETIME,'lang': LANG,'party': prt})
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
    global ID, LANG, SFX, MSC, UP, DOWN, LEFT, RIGHT, ACT, RUN, PHONE, BAG, SPEED, COLOR, INVENTORY, WEATHER, BORDER, CHARACTERS, TASKPIN, MINIMAP, SCENE, CENSORSHIP, HINT, HELP,\
    FORMATION, MAP, PX, PY, TIME, DATE, CHAPTER, GAS, GAMETIME, PARTY, CONTACTS, CALLHIST, INBOX, TASKS, TACTICAL, BESTIARY, ACHIEVEMENTS
 
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
    
    if add == False:
        LANG = 'PT'
        SFX = 0.8
        MSC = 0.6
        UP = [pygame.K_w,pygame.K_UP]
        DOWN = [pygame.K_s,pygame.K_DOWN]
        LEFT = [pygame.K_a,pygame.K_LEFT]
        RIGHT = [pygame.K_d,pygame.K_RIGHT]
        ACT = [pygame.K_g,pygame.K_KP0]
        RUN = [pygame.K_h,pygame.K_KP_ENTER]
        PHONE = [pygame.K_BACKSPACE,pygame.K_KP_MULTIPLY]
        BAG = [pygame.K_RETURN,pygame.K_KP_MINUS]
        SPEED = 2
        COLOR = [242,30,30]
        BORDER = 0
        CENSORSHIP = True
        HINT = True
        HELP = True
          
        MAP = 1
        PX = 184
        PY = 476
        TIME = [0,32,0]
        DATE = [25,12,2007,1,1]
        WEATHER = 1
        CHAPTER = 0
        SCENE = 0
        GAMETIME = 0
        FORMATION = 0
        
        GAS = 100.0
         
        for i in range(6):
            CHARACTERS[i]['NAME'] = ''
            CHARACTERS[i]['LASTNAME'] = ''
            CHARACTERS[i]['LEVEL'] = 0
     
        PARTY = [[1,2,0]]
        CONTACTS = [['Maicon','923778988'],['Mercador','969696969'],['Pizza Delivery','953478809']]
        CALLHIST = []
        INBOX = []
        TASKS = []
        TACTICAL = [[1,1,1,1]]
        BESTIARY = []
        for i in database.FREAKS.items(): BESTIARY.append({'N': i[0],'ID': 'xxxx','DATE': '000000','SEEN': 0})
        for i in database.ACHIEVEMENTS:
            i[2] = 0
            i[3] = ''

        INVENTORY = []
        for u in range(6):
            INVENTORY.append([])
            for y in range(5):
                INVENTORY[u].append([])
                for x in range(5):
                    INVENTORY[u][y].append(['_','0000','_','0000','_','0000'])

        INVENTORY[1] = [
        [['amulet1','0000','_','0000','_','0000'],['phone','3600','sim_card','0003','_','0000'],['bottle100','0000','_','0000','_','0000'],['credit_card','0100','_','0000','_','0000'],['_','0000','_','0000','_','0000']],
        [['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000']],
        [['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000']],
        [['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000']],
        [['bag1','0000','_','0000','_','0000'],['gun_UZI.22','0010','ammo.22_silver','0000','_','0000'],['melee_bar','0010','_','0000','_','0000'],['_','0000','_','0000','_','0000'],['_','0000','_','0000','_','0000']]
        ]
     
        STORAGE = [['jewel_ruby','0000','_','0000','_','0000'],['drink_whiskey','1503','_','0000','_','0000']]
        for i in range(23): STORAGE.append(['_','0000','_','0000','_','0000'])
      
    try:
        com.execute("CREATE TABLE settings (id integer,lang text,sfx integer,msc integer,up text,down text,left text,right text,act text,run text,phone text,inventory text,speed integer,color1 integer,color2 integer,color3 integer,border integer,\
            censor integer,hint integer,help integer)")
        com.execute("CREATE TABLE data (id integer,gt integer,fr integer,map integer,x integer,y integer,time text,date text,weather integer,chapter integer,scene integer,\
            gas integer,taskpin integer,minimap integer)")
    except: pass
      
    trg = False
    com.execute("SELECT id FROM settings")
    for i in com.fetchall():
        if i[0] == ID: trg = True
    if trg == True:
        com.execute("DELETE FROM settings WHERE id=" + str(ID))
        com.execute("DELETE FROM data WHERE id=" + str(ID))
     
    com.execute("INSERT INTO settings VALUES (" + str(ID) + ",'PT',0.8,0.6,'W','S','A','D','G','H','BACKSPACE','RETURN',2,255,255,255,0,1,1,1)")
    com.execute("INSERT INTO data VALUES (" + str(ID) + ",0,0,1,0,0,'0830','2512200711',0,0,0,10,0,0)")
      
    com.execute("DROP TABLE IF EXISTS characters" + str(ID))
    com.execute("CREATE TABLE characters" + str(ID) + " (n integer,name text,lastname text,level integer,hp integer,xp integer,health integer,morality integer,"+
        "hunger integer,thirst integer,sleep integer,carism integer,intimidation integer,persuasion integer,animals integer,spirits integer,"+
        "stamina integer,atletism integer,acrobatics integer,furtivity integer,perception integer,medicine integer,imunity integer,"+
        "infantry integer,investigation integer,crafting integer,coordenation integer,explosives integer,culinary integer)")
    for i in range(len(CHARACTERS)): com.execute("INSERT INTO characters" + str(ID) + " VALUES(" + str(i) + ",'','',0,0,0,0,0,100,100,10000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")
    tbl.commit()
      
    database.load_dialogs(True)
    com.execute("DROP TABLE IF EXISTS dlgsav" + str(ID))
    com.execute("CREATE TABLE dlgsav" + str(ID) + " (who text,vl integer)")
    for i in DLGSAV: com.execute("INSERT INTO dlgsav" + str(ID) + " VALUES('" + i + "',0)")

    com.execute("DROP TABLE IF EXISTS party" + str(ID))
    com.execute("CREATE TABLE party" + str(ID) + " (n integer,p1 integer,p2 integer,p3 integer)")
      
    com.execute("DROP TABLE IF EXISTS contacts" + str(ID))
    com.execute("CREATE TABLE contacts" + str(ID) + " (n integer)")
 
    com.execute("DROP TABLE IF EXISTS callhist" + str(ID))
    com.execute("CREATE TABLE callhist" + str(ID) + " (n integer,w integer)")
 
    com.execute("DROP TABLE IF EXISTS inbox" + str(ID))
    com.execute("CREATE TABLE inbox" + str(ID) + " (n integer,red integer)")
 
    com.execute("DROP TABLE IF EXISTS tasks" + str(ID))
    com.execute("CREATE TABLE tasks" + str(ID) + " (tsk text,don integer)")
 
    com.execute("DROP TABLE IF EXISTS tactical" + str(ID))
    com.execute("CREATE TABLE tactical" + str(ID) + " (n integer,pl1 integer,pl2 integer,pl3 integer,pl4 integer)")
      
    com.execute("DROP TABLE IF EXISTS bestiary" + str(ID))
    com.execute("CREATE TABLE bestiary" + str(ID) + " (name text,id text,date text,seen int)")
    for i in database.FREAKS.items(): com.execute("INSERT INTO bestiary" + str(ID) + " VALUES('" + i[0] + "','xxxxxx','000000',0)")
      
    com.execute("DROP TABLE IF EXISTS achievements" + str(ID))
    com.execute("CREATE TABLE achievements" + str(ID) + " (idx integer,got integer,date text)")
      
    com.execute("DROP TABLE IF EXISTS inventory" + str(ID))
    com.execute("CREATE TABLE inventory" + str(ID) + " (item text,position text,properties text,acc1 text,acp1 text,acc2 text,acp2 text)")
    for u in range(6):
        for x in range(5):
            for y in range(5):
                com.execute("INSERT INTO inventory" + str(ID) + " VALUES('_','" + str(u) + str(x) + str(y) + "','0000','_','0000','_','0000')")
    tbl.commit()
 
    com.execute("DROP TABLE IF EXISTS storage" + str(ID))
    com.execute("CREATE TABLE storage" + str(ID) + " (it text,ip text,ic1 text,ip1 text,ic2 text,ip2 text)")
    for i in range(25): com.execute("INSERT INTO storage" + str(ID) + " VALUES('_','0000','_','0000','_','0000')")
     
    com.close()
    tbl.close()

def load_data():
    global ID, LANG, SFX, MSC, UP, DOWN, LEFT, RIGHT, ACT, RUN, PHONE, BAG, SPEED, COLOR, WEATHER, BORDER, TASKPIN, MINIMAP, SCENE, CENSORSHIP, HINT, HELP,\
    FORMATION, MAP, PX, PY, TIME, DATE, CHAPTER, GAS, GAMETIME, PARTY, CONTACTS, CALLHIST, INBOX, TASKS, TACTICAL, BESTIARY, INVENTORY
      
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
     
    com.execute("SELECT id from settings")
    com.execute("SELECT lang FROM settings")
    LANG = com.fetchall()[ID][0]
    com.execute("SELECT sfx FROM settings")
    SFX = com.fetchall()[ID][0]
    com.execute("SELECT msc FROM settings")
    MSC = com.fetchall()[ID][0]
    '''com.execute("SELECT up FROM settings")
    UP[0] = int(com.fetchall()[ID][0])
    if UP[0] == 'W': UP[0] = pygame.K_w
    com.execute("SELECT down FROM settings")
    DOWN[0] = int(com.fetchall()[ID][0])
    if DOWN[0] == 'S': DOWN[0] = pygame.K_s
    com.execute("SELECT left FROM settings")
    LEFT[0] = int(com.fetchall()[ID][0])
    if LEFT[0] == 'A': LEFT[0] = pygame.K_a
    com.execute("SELECT right FROM settings")
    RIGHT[0] = int(com.fetchall()[ID][0])
    if RIGHT[0] == 'D': RIGHT[0] = pygame.K_d
    com.execute("SELECT act FROM settings")
    ACT[0] = int(com.fetchall()[ID][0])
    if ACT[0] == 'SPACE': ACT[0] = pygame.K_SPACE
    com.execute("SELECT run FROM settings")
    RUN[0] = int(com.fetchall()[ID][0])
    if RUN[0] == 'SPACE': RUN[0] = pygame.K_SPACE
    com.execute("SELECT phone FROM settings")
    PHONE[0] = int(com.fetchall()[ID][0])
    if PHONE[0] == 'BACKSPACE': PHONE[0] = pygame.K_BACKSPACE
    com.execute("SELECT inventory FROM settings")
    BAG[0] = int(com.fetchall()[ID][0])'''

    UP = [pygame.K_w,pygame.K_UP]
    DOWN = [pygame.K_s,pygame.K_DOWN]
    LEFT = [pygame.K_a,pygame.K_LEFT]
    RIGHT = [pygame.K_d,pygame.K_RIGHT]
    ACT = [pygame.K_g,pygame.K_LCTRL]
    RUN = [pygame.K_h,pygame.K_SPACE]
    PHONE = [pygame.K_BACKSPACE,pygame.K_BACKSPACE]
    BAG = [pygame.K_RETURN,pygame.K_RETURN]

    com.execute("SELECT speed FROM settings")
    SPEED = com.fetchall()[ID][0]
    com.execute("SELECT color1 FROM settings")
    COLOR[0] = com.fetchall()[ID][0]
    com.execute("SELECT color2 FROM settings")
    COLOR[1] = com.fetchall()[ID][0]
    com.execute("SELECT color3 FROM settings")
    COLOR[2] = com.fetchall()[ID][0]
    com.execute("SELECT border FROM settings")
    BORDER = com.fetchall()[ID][0]
    com.execute("SELECT censor FROM settings")
    CENSORSHIP = bool(com.fetchall()[ID][0])
    com.execute("SELECT hint FROM settings")
    HINT = bool(com.fetchall()[ID][0])
    com.execute("SELECT help FROM settings")
    HELP = bool(com.fetchall()[ID][0])
      
    com.execute("SELECT gt FROM data")
    GAMETIME = com.fetchall()[ID][0]
    com.execute("SELECT fr FROM data")
    FORMATION = com.fetchall()[ID][0]
    com.execute("SELECT map FROM data")
    MAP = com.fetchall()[ID][0]
    com.execute("SELECT x FROM data")
    PX = com.fetchall()[ID][0]
    com.execute("SELECT y FROM data")
    PY = com.fetchall()[ID][0]
    com.execute("SELECT time FROM data")
    res = com.fetchall()[ID][0]
    TIME = [int(res[0:2]),int(res[2:4]),0]
    com.execute("SELECT date FROM data")
    res = com.fetchall()[ID][0]
    DATE = [int(res[0:2]),int(res[2:4]),int(res[4:8]),int(res[8]),int(res[9])]
    com.execute("SELECT weather FROM data")
    WEATHER = com.fetchall()[ID][0]
    com.execute("SELECT chapter FROM data")
    CHAPTER = com.fetchall()[ID][0]
    com.execute("SELECT scene FROM data")
    SCENE = com.fetchall()[ID][0]
    com.execute("SELECT gas FROM data")
    GAS = com.fetchall()[ID][0]
    com.execute("SELECT taskpin FROM data")
    TASKPIN = bool(com.fetchall()[ID])
    com.execute("SELECT minimap FROM data")
    MINIMAP = bool(com.fetchall()[ID])
    
    com.execute("SELECT * FROM characters" + str(ID))
    res = com.fetchall()
    for i in range(len(CHARACTERS)):
        CHARACTERS[i]['NAME'] = res[i][1]
        CHARACTERS[i]['LASTNAME'] = res[i][2]
        CHARACTERS[i]['LEVEL'] = res[i][3]
        CHARACTERS[i]['HP'] = res[i][4]
        CHARACTERS[i]['XP'] = res[i][5]
        CHARACTERS[i]['HEALTH'] = res[i][6]
        CHARACTERS[i]['MORALITY'] = res[i][7]
        CHARACTERS[i]['HUNGER'] = res[i][8]
        CHARACTERS[i]['THIRST'] = res[i][9]
        CHARACTERS[i]['SLEEP'] = res[i][10]
        CHARACTERS[i]['CARISM'] = res[i][11]
        CHARACTERS[i]['INTIMIDATION'] = res[i][12]
        CHARACTERS[i]['PERSUASION'] = res[i][13]
        CHARACTERS[i]['ANIMALS'] = res[i][14]
        CHARACTERS[i]['SPIRITS'] = res[i][15]
        CHARACTERS[i]['STAMINA'] = res[i][16]
        CHARACTERS[i]['ATLETISM'] = res[i][17]
        CHARACTERS[i]['ACROBATICS'] = res[i][18]
        CHARACTERS[i]['FURTIVITY'] = res[i][19]
        CHARACTERS[i]['PERCEPTION'] = res[i][20]
        CHARACTERS[i]['MEDICINE'] = res[i][21]
        CHARACTERS[i]['IMUNITY'] = res[i][22]
        CHARACTERS[i]['INFANTRY'] = res[i][23]
        CHARACTERS[i]['INVESTIGATION'] = res[i][24]
        CHARACTERS[i]['CRAFTING'] = res[i][25]
        CHARACTERS[i]['COORDENATION'] = res[i][26]
        CHARACTERS[i]['EXPLOSIVES'] = res[i][27]
        CHARACTERS[i]['CULINARY'] = res[i][28]
    com.execute("SELECT * FROM dlgsav" + str(ID))
    res = com.fetchall()
    for i in res: DLGSAV[i[0]] = i[1]
    com.execute("SELECT * FROM party" + str(ID))
    res = com.fetchall()
    PARTY = []
    for i in res: PARTY.append([i[1],i[2],i[3]])
    com.execute("SELECT * FROM contacts" + str(ID))
    res = com.fetchall()
    CONTACTS = []
    for i in res: CONTACTS.append(NUMBERS[i[0]].copy())
    CONTACTS = [['Maicon','923778988'],['Mercador','969696969'],['Pizza Delivery','953478809']]
    com.execute("SELECT * FROM callhist" + str(ID))
    res = com.fetchall()
    CALLHIST = []
    for i in res: CALLHIST.append([i[0],i[1]])
    com.execute("SELECT * FROM inbox" + str(ID))
    res = com.fetchall()
    INBOX = []
    for i in res:
        mail = EMAILS[i[0]].copy()
        mail.append(i[1])
        INBOX.append(mail)
    com.execute("SELECT * FROM tasks" + str(ID))
    res = com.fetchall()
    TASKS = []
    for i in res: TASKS.append([i[0],i[1]])
    com.execute("SELECT * FROM tactical" + str(ID))
    res = com.fetchall()
    TACTICAL = []
    for i in res: TACTICAL.append([i[1],i[2],i[3],i[4]])
    com.execute("SELECT * FROM bestiary" + str(ID))
    res = com.fetchall()
    BESTIARY = []
    for i in res:
        BESTIARY.append({'N': i[0],'ID': i[1],'DATE': i[2],'SEEN': i[3]})
    com.execute("SELECT * FROM achievements"+ str(ID))
    res = com.fetchall()
    for i in res:
        database.ACHIEVEMENTS[i[0]][2] = i[1]
        database.ACHIEVEMENTS[i[0]][3] = i[2]
    if res == []:
        for i in database.ACHIEVEMENTS:
            i[2] = 0
            i[3] = ''
    com.execute("SELECT * FROM inventory"+ str(ID))
    res = com.fetchall()
    INVENTORY = []
    for u in range(6):
        INVENTORY.append([])
        for x in range(5):
            INVENTORY[u].append([])
            for y in range(5):
                for i in res:
                    if int(i[1][0]) == u and int(i[1][1]) == x and int(i[1][2]) == y:
                        INVENTORY[u][x].append([i[0],i[2],i[3],i[4],i[5],i[6]])
    com.execute("SELECT * FROM storage"+ str(ID))
    res = com.fetchall()
    STORAGE = []
    for i in res:
        STORAGE.append([i[0],i[1],i[2],i[3],i[4],i[5]])
    com.close()
    tbl.close()
    database.load_dialogs()

def save_data():
    global ID, MAP, PX, PY, TIME, DATE, WEATHER, CHAPTER, GAS, GAMETIME, FORMATION, CHARACTERS, TASKPIN, MINIMAP, DLGSAV, SCENE, BESTIARY
 
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
 
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
    #SAVE GLOBAL GAME DATA
    com.execute("""UPDATE data SET gt = {},fr = {},map = {},x = {},y = {},time = {},date = {},weather = {},chapter = {},scene = {},gas = {},\
        taskpin = {},minimap = {} WHERE id = {}""".format(GAMETIME,FORMATION,MAP,PX,PY,ts,dt,WEATHER,CHAPTER,SCENE,GAS,int(TASKPIN),int(MINIMAP),ID))
    tbl.commit()
    #SAVE CHARACTERS DATA
    p = 0
    for i in CHARACTERS:
        com.execute("""UPDATE characters{} SET name = '{}',lastname = '{}',level = {},hp = {},xp = {},health = {},morality = {},hunger = {},thirst = {},sleep = {},\
            carism = {},intimidation = {},persuasion = {},animals = {},spirits = {},stamina = {},atletism = {},acrobatics = {},furtivity = {},perception = {},\
            medicine = {},imunity = {},infantry = {},investigation = {},crafting = {},coordenation = {},explosives = {},culinary = {} WHERE n = {}""".format(ID,i['NAME'],i['LASTNAME'],i['LEVEL'],\
                i['HP'],i['XP'],i['HEALTH'],i['MORALITY'],i['HUNGER'],i['THIRST'],i['SLEEP'],i['CARISM'],i['INTIMIDATION'],i['PERSUASION'],\
                i['SPIRITS'],i['ANIMALS'],i['STAMINA'],i['ATLETISM'],i['ACROBATICS'],i['FURTIVITY'],i['PERCEPTION'],i['MEDICINE'],i['IMUNITY'],\
                i['INFANTRY'],i['INVESTIGATION'],i['CRAFTING'],i['COORDENATION'],i['EXPLOSIVES'],i['CULINARY'],p))
        tbl.commit()
        p += 1
    #SAVE DIALOGS DATA
    for i in DLGSAV:
        com.execute("""UPDATE dlgsav{} SET vl = {} WHERE who = '{}'""".format(ID,DLGSAV[i],i))
        tbl.commit()
    #SAVE TACTICAL DATA
    for i in range(len(TACTICAL)):
        try: com.execute("""UPDATE tactical{} SET p1 = {},p2 = {},p3 = {},p4 = {} WHERE n = {}""".format(ID,TACTICAL[i][0],TACTICAL[i][1],TACTICAL[i][2],TACTICAL[i][3],i))
        except: com.execute("INSERT INTO tactical" + str(ID) + " VALUES(:n,:p1,:p2,:p3,:p4)",{'n': i,'p1': TACTICAL[i][0],'p2': TACTICAL[i][1],'p3': TACTICAL[i][2],'p4': TACTICAL[i][3]})
        tbl.commit()
    #SAVB BESTIARY DATA
    for i in BESTIARY:
        com.execute("""UPDATE bestiary{} SET id = '{}',date = '{}',seen = {} WHERE name = '{}'""".format(ID,i['ID'],i['DATE'],i['SEEN'],i['N']))
        tbl.commit()
    #SAVE INVENTORY DATA
    for u in range(6):
        for x in range(5):
            for y in range(5):
                com.execute("UPDATE inventory{} SET item = '{}',properties = '{}',acc1 = '{}',acp1 = '{}',acc2 = '{}',acp2 = '{}' WHERE position = '{}'".format(ID,\
                    INVENTORY[u][x][y][0],INVENTORY[u][x][y][1],INVENTORY[u][x][y][2],INVENTORY[u][x][y][3],INVENTORY[u][x][y][4],INVENTORY[u][x][y][5],str(u) + str(x) + str(y)))
                tbl.commit()
    #SAVE STORAGE DATA
    com.execute("DROP TABLE IF EXISTS storage" + str(ID))
    com.execute("CREATE TABLE storage" + str(ID) + " (it text,ip text,ic1 text,ip1 text,ic2 text,ip2 text)")
    for i in STORAGE:
        com.execute("INSERT INTO storage" + str(ID) + " VALUES('" + i[0] + "','" + i[1] + "','" + i[2] + "','" + i[3] + "','" + i[4] + "','" + i[5] + "')")
        tbl.commit()
 
    com.close()
    tbl.close()

def save_sett():
    global ID, LANG, SFX, MSC, UP, DOWN, LEFT, RIGHT, ACT, RUN, PHONE, BAG, SPEED, COLOR, BORDER, CENSORSHIP, HINT, HELP
      
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
      
    com.execute("UPDATE settings SET lang = :lang,sfx = :sfx,msc = :msc,up = :up,down = :down,left = :left,right = :right,act = :act,run = :run,phone = :phone,inventory = :inventory,\
        speed = :speed,color1 = :color1,color2 = :color2,color3 = :color3,border = :border,censor = :censor,hint = :hint,help = :help WHERE id = :id",
        {'id': ID,'lang': LANG,'sfx': SFX,'msc': MSC,'up': UP[0],'down': DOWN[0],'left': LEFT[0],'right': RIGHT[0],'act': ACT[0],'run': RUN[0],'phone': PHONE[0],'inventory': BAG[0],
        'speed': SPEED,'color1': COLOR[0],'color2': COLOR[1],'color3': COLOR[2],'border': BORDER,'censor': int(CENSORSHIP),'hint': int(HINT),'help': int(HELP)})
    tbl.commit()
      
    com.close()
    tbl.close()

def party_make(p):
    global ID, PARTY
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
      
    trg = False
    com.execute("SELECT n FROM party" + str(ID))
    for i in com.fetchall():
        if i[0] == trg: trg = True

    if len(PARTY[p]) < 2: PARTY[p].append(0)
    if len(PARTY[p]) < 3: PARTY[p].append(0)
    if trg == False:
        com.execute("DELETE FROM party" + str(ID) + " WHERE n = " + str(p))
    com.execute("INSERT INTO party" + str(ID) + " VALUES(:n,:p1,:p2,:p3)",{'n': p,'p1': PARTY[p][0],'p2': PARTY[p][1],'p3': PARTY[p][2]})
    tbl.commit()
      
    com.close()
    tbl.close()

def call_save(c):
    global ID
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
 
    com.execute("INSERT INTO contacts" + str(ID) + " VALUES (:n)",{'n': c})
    tbl.commit()
 
    com.close()
    tbl.close()

def hist_save(n,w):
    global ID
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
 
    com.execute("INSERT INTO callhist" + str(ID) + " VALUES (:n,:w)",{'n': n,'w': w})
    tbl.commit()
 
    com.close()
    tbl.close()

def inbx_save(e,r):
    global ID
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
 
    com.execute("INSERT INTO inbox" + str(ID) + " VALUES (:n,:red)",{'n': e,'red': r})
    tbl.commit()
 
    com.close()
    tbl.close()

def task_save(t,d):
    global ID
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
 
    com.execute("INSERT INTO tasks" + str(ID) + " VALUES (:tsk,:don)",{'tsk': t,'don': d})
    tbl.commit()
 
    com.close()
    tbl.close()

def trophy(i):
    global ID, ACHIEVEMENTS
    tbl = sqlite3.connect('userdata.db')
    com = tbl.cursor()
      
    com.execute("INSERT INTO achievements" + str(ID) + " VALUES(:idx,:got,:date)",{'idx': i,'got': ACHIEVEMENTS[i][2],'date': ACHIEVEMENTS[i][3]})
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

    com.execute("DELETE FROM recent WHERE id=" + str(ID))
    com.execute("DELETE FROM settings WHERE id=" + str(ID))
    com.execute("DELETE FROM data WHERE id=" + str(ID))
    com.execute("DROP TABLE characters" + str(ID))
    com.execute("DROP TABLE party" + str(ID))
    com.execute("DROP TABLE contacts" + str(ID))
    com.execute("DROP TABLE callhist" + str(ID))
    com.execute("DROP TABLE inbox" + str(ID))
    com.execute("DROP TABLE tasks" + str(ID))
    com.execute("DROP TABLE tactical" + str(ID))
    com.execute("DROP TABLE bestiary" + str(ID))
    com.execute("DROP TABLE achievements" + str(ID))
    com.execute("DROP TABLE inventory" + str(ID))
    tbl.commit()
      
    com.close()
    tbl.close()

def color_sprite(typ,p,mov,c,h='',ind=''):
    if ind == '': pth = 'Sprites/NPCs/' + typ + '_' + str(p) + str(h) + str(c) + '_' + mov + '.png'
    else: pth = 'Sprites/NPCs/' + typ + '_' + str(p) + str(h) + str(c) + '_' + mov + '_' + str(ind) + '.png'

    if os.path.isfile(pth):
        srf = pygame.image.load(pth)
    else:
        if typ == 'head': ex = '0'
        else: ex = ''
        if ind == '': srf = pygame.image.load('Sprites/Characters/' + typ + '_' + str(p) + ex + '0_' + mov + '.png')
        else: srf = pygame.image.load('Sprites/Characters/' + typ + '_' + str(p) + ex + '0_' + mov + '_' + str(ind) + '.png')

        for y in range(srf.get_rect().height):
            for x in range(srf.get_rect().width):
                #SKIN I
                if srf.get_at((x,y)) == (0,100,255):
                    if c == 0: srf.set_at((x,y),(63,37,0))
                    if c == 1: srf.set_at((x,y),(153,92,58))
                    if c == 2: srf.set_at((x,y),(206,138,78))
                    if c == 3: srf.set_at((x,y),(226,157,97))
                    if c == 4: srf.set_at((x,y),(234,161,100))
                    if c == 5: srf.set_at((x,y),(234,154,107))
                    if c == 6: srf.set_at((x,y),(235,185,139))
                    if c == 7: srf.set_at((x,y),(247,202,163))
                    if c == 8: srf.set_at((x,y),(255,215,168))
                    if c == 9: srf.set_at((x,y),(255,231,204))
                #SKIN II
                if srf.get_at((x,y)) == (0,0,255):
                    if c == 0: srf.set_at((x,y),(40,17,4))
                    if c == 1: srf.set_at((x,y),(130,66,61))
                    if c == 2: srf.set_at((x,y),(181,106,79))
                    if c == 3: srf.set_at((x,y),(224,143,96))
                    if c == 4: srf.set_at((x,y),(216,128,108))
                    if c == 5: srf.set_at((x,y),(224,132,112))
                    if c == 6: srf.set_at((x,y),(236,157,138))
                    if c == 7: srf.set_at((x,y),(224,174,163))
                    if c == 8: srf.set_at((x,y),(234,194,171))
                    if c == 9: srf.set_at((x,y),(226,199,192))
                #HAIR I
                if srf.get_at((x,y)) == (51,51,51):
                    if h == 0: srf.set_at((x,y),(76,39,17))
                    if h == 1: srf.set_at((x,y),(114,65,32))
                    if h == 2: srf.set_at((x,y),(165,95,48))
                    if h == 3: srf.set_at((x,y),(255,191,0))
                    if h == 4: srf.set_at((x,y),(119,7,0))
                    if h == 5: srf.set_at((x,y),(255,255,255))
                    if h == 6: srf.set_at((x,y),(63,255,0))
                    if h == 7: srf.set_at((x,y),(84,39,0))
                    if h == 8: srf.set_at((x,y),(255,144,0))
                #HAIR II
                if srf.get_at((x,y)) == (33,33,33):
                    if h == 0: srf.set_at((x,y),(40,23,13))
                    if h == 1: srf.set_at((x,y),(86,51,48))
                    if h == 2: srf.set_at((x,y),(127,67,62))
                    if h == 3: srf.set_at((x,y),(216,98,30))
                    if h == 4: srf.set_at((x,y),(86,9,37))
                    if h == 5: srf.set_at((x,y),(198,198,198))
                    if h == 6: srf.set_at((x,y),(44,204,87))
                    if h == 7: srf.set_at((x,y),(63,11,6))
                    if h == 8: srf.set_at((x,y),(206,100,39))

                print([p,h,c])
                raw_str = pygame.image.tostring(srf, 'RGBA', False)
                image = Image.frombytes('RGBA', srf.get_size(), raw_str)
                image.save(pth)

    return srf

def heads(p,w,h):
    global SPRITES
    g = 0

    #HEADS
    if p < 10: pt = '0' + str(p)
    else: pt = str(p)

    SPRITES['BLANKU_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKDD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKLD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKL_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKLU_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKRD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKR_' + str(pt) + str(h) + str(w)] = []
    SPRITES['BLANKRU_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKU_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKLD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKL_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKLU_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKRD_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKR_' + str(pt) + str(h) + str(w)] = []
    SPRITES['TALKRU_' + str(pt) + str(h) + str(w)] = []

    SPRITES['BLANKU_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'U',w,h))
    for i in range(2): SPRITES['BLANKDD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'blankDD',w,h,i))
    for i in range(2): SPRITES['BLANKD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'blankD',w,h,i))
    for i in range(2): SPRITES['BLANKLD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'blankLD',w,h,i))
    for i in range(2): SPRITES['BLANKL_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'blankH',w,h,i))
    SPRITES['BLANKLU_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'HU',w,h))
    for i in range(2): SPRITES['BLANKRD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'blankRD',w,h,i))
    for i in range(2): SPRITES['BLANKR_' + str(pt) + str(h) + str(w)].append(pygame.transform.flip(color_sprite('head',pt,'blankH',w,h,i),True,False))
    SPRITES['BLANKRU_' + str(pt) + str(h) + str(w)].append(pygame.transform.flip(color_sprite('head',pt,'HU',w,h),True,False))
    SPRITES['TALKU_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'U',w,h))
    for i in range(2): SPRITES['TALKD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'talkD',w,h,i))
    for i in range(2): SPRITES['TALKLD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'talkLD',w,h,i))
    for i in range(2): SPRITES['TALKL_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'talkH',w,h,i))
    SPRITES['TALKLU_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'HU',w,h))
    for i in range(2): SPRITES['TALKRD_' + str(pt) + str(h) + str(w)].append(color_sprite('head',pt,'talkRD',w,h,i))
    for i in range(2): SPRITES['TALKR_' + str(pt) + str(h) + str(w)].append(pygame.transform.flip(color_sprite('head',pt,'talkH',w,h,i),True,False))
    SPRITES['TALKRU_' + str(pt) + str(h) + str(w)].append(pygame.transform.flip(color_sprite('head',pt,'HU',w,h),True,False))

def bodies(w,t):
    global SPRITES

    if t < 10: pt = '0' + str(t)
    else: pt = str(t)

    SPRITES['PHONE_' + str(pt) + str(w)] = [color_sprite('body',pt,'phone',w)]; SPRITES['CALL_' + str(pt) + str(w)] = [color_sprite('body',pt,'call',w)]
    SPRITES['STANDU_' + str(pt) + str(w)] = []; SPRITES['STANDLU_' + str(pt) + str(w)] = []; SPRITES['STANDL_' + str(pt) + str(w)] = []; SPRITES['STANDLD_' + str(pt) + str(w)] = []
    SPRITES['STANDD_' + str(pt) + str(w)] = []; SPRITES['STANDRD_' + str(pt) + str(w)] = []; SPRITES['STANDR_' + str(pt) + str(w)] = []; SPRITES['STANDRU_' + str(pt) + str(w)] = []
    SPRITES['TIREDSTANDU_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDLU_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDL_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDLD_' + str(pt) + str(w)] = []
    SPRITES['TIREDSTANDD_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDRD_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDR_' + str(pt) + str(w)] = []; SPRITES['TIREDSTANDRU_' + str(pt) + str(w)] = []
    SPRITES['SEATU_' + str(pt) + str(w)] = [color_sprite('body',pt,'seatU',w)]; SPRITES['SEATLU_' + str(pt) + str(w)] = [color_sprite('body',pt,'seatHU',w)]; SPRITES['SEATL_' + str(pt) + str(w)] = [color_sprite('body',pt,'seatH',w)]; SPRITES['SEATHD_' + str(pt) + str(w)] = [color_sprite('body',pt,'seatHD',w)]
    SPRITES['SEATD_' + str(pt) + str(w)] = [color_sprite('body',pt,'seatD',w)]; SPRITES['SEATRD_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'seatHD',w),True,False)]; SPRITES['SEATR_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'seatH',w),True,False)]; SPRITES['SEATRU_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'seatHU',w),True,False)]
    SPRITES['DRIVEU_' + str(pt) + str(w)] = [color_sprite('body',pt,'driveU',w)]; SPRITES['DRIVELU_' + str(pt) + str(w)] = [color_sprite('body',pt,'driveHU',w)]; SPRITES['DRIVEL_' + str(pt) + str(w)] = [color_sprite('body',pt,'driveH',w)]; SPRITES['DRIVELD_' + str(pt) + str(w)] = [color_sprite('body',pt,'driveHD',w)]
    SPRITES['DRIVED_' + str(pt) + str(w)] = [color_sprite('body',pt,'driveD',w)]; SPRITES['DRIVERD_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'driveHD',w),True,False)]; SPRITES['DRIVER_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'driveH',w),True,False)]; SPRITES['DRIVERU_' + str(pt) + str(w)] = [pygame.transform.flip(color_sprite('body',pt,'driveHU',w),True,False)]
    SPRITES['JUMPU_' + str(pt) + str(w)] = []; SPRITES['JUMPD_' + str(pt) + str(w)] = []
    SPRITES['WALKU_' + str(pt) + str(w)] = []; SPRITES['WALKLU_' + str(pt) + str(w)] = []; SPRITES['WALKL_' + str(pt) + str(w)] = []; SPRITES['WALKLD_' + str(pt) + str(w)] = []
    SPRITES['WALKD_' + str(pt) + str(w)] = []; SPRITES['WALKRD_' + str(pt) + str(w)] = []; SPRITES['WALKR_' + str(pt) + str(w)] = []; SPRITES['WALKRU_' + str(pt) + str(w)] = []
    SPRITES['RUNU_' + str(pt) + str(w)] = []; SPRITES['RUNLU_' + str(pt) + str(w)] = []; SPRITES['RUNL_' + str(pt) + str(w)] = []; SPRITES['RUNLD_' + str(pt) + str(w)] = []; SPRITES['RUND_' + str(pt) + str(w)] = []
    SPRITES['RUNRD_' + str(pt) + str(w)] = []; SPRITES['RUNR_' + str(pt) + str(w)] = []; SPRITES['RUNRU_' + str(pt) + str(w)] = []

    for i in range(4): SPRITES['STANDU_' + str(pt) + str(w)].append(color_sprite('body',pt,'standU',w,ind=i))
    for i in range(4): SPRITES['STANDLU_' + str(pt) + str(w)].append(color_sprite('body',pt,'standHU',w,ind=i))
    for i in range(4): SPRITES['STANDL_' + str(pt) + str(w)].append(color_sprite('body',pt,'standH',w,ind=i))
    for i in range(4): SPRITES['STANDLD_' + str(pt) + str(w)].append(color_sprite('body',pt,'standHD',w,ind=i))
    for i in range(4): SPRITES['STANDD_' + str(pt) + str(w)].append(color_sprite('body',pt,'standD',w,ind=i))
    for i in range(4): SPRITES['STANDRU_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standHU',w,ind=i),True,False))
    for i in range(4): SPRITES['STANDR_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standH',w,ind=i),True,False))
    for i in range(4): SPRITES['STANDRD_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standHD',w,ind=i),True,False))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDU_' + str(pt) + str(w)].append(color_sprite('body',pt,'tiredstandU',w,ind=i))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDLU_' + str(pt) + str(w)].append(color_sprite('body',pt,'tiredstandHU',w,ind=i))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDL_' + str(pt) + str(w)].append(color_sprite('body',pt,'tiredstandH',w,ind=i))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDLD_' + str(pt) + str(w)].append(color_sprite('body',pt,'tiredstandHD',w,ind=i))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDD_' + str(pt) + str(w)].append(color_sprite('body',pt,'tiredstandD',w,ind=i))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDRU_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standHU',w,ind=i),True,False))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDR_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standH',w,ind=i),True,False))
    for i in [0,0,1,1]: SPRITES['TIREDSTANDRD_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'standHD',w,ind=i),True,False))
    for i in range(2): SPRITES['JUMPU_' + str(pt) + str(w)].append(color_sprite('body',pt,'jumpU',w,ind=i))
    for i in range(2): SPRITES['JUMPD_' + str(pt) + str(w)].append(color_sprite('body',pt,'jumpD',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKU_' + str(pt) + str(w)].append(color_sprite('body',pt,'walkU',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKLU_' + str(pt) + str(w)].append(color_sprite('body',pt,'walkHU',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKL_' + str(pt) + str(w)].append(color_sprite('body',pt,'walkH',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKLD_' + str(pt) + str(w)].append(color_sprite('body',pt,'walkHD',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKD_' + str(pt) + str(w)].append(color_sprite('body',pt,'walkD',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKRU_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'walkHU',w,ind=i),True,False))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKR_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'walkH',w,ind=i),True,False))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['WALKRD_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'walkHD',w,ind=i),True,False))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNU_' + str(pt) + str(w)].append(color_sprite('body',pt,'runU',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNLU_' + str(pt) + str(w)].append(color_sprite('body',pt,'runHU',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNL_' + str(pt) + str(w)].append(color_sprite('body',pt,'runH',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNLD_' + str(pt) + str(w)].append(color_sprite('body',pt,'runHD',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUND_' + str(pt) + str(w)].append(color_sprite('body',pt,'runD',w,ind=i))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNRU_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'runHU',w,ind=i),True,False))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNR_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'runH',w,ind=i),True,False))
    for i in [0,1,2,1,0,3,4,3]: SPRITES['RUNRD_' + str(pt) + str(w)].append(pygame.transform.flip(color_sprite('body',pt,'runHD',w,ind=i),True,False))

def battlesprites():
    global SPRITES

    SPRITES['ATTACKIMATION_1'] = []
    SPRITES['ATTACKIMATION_10'] = []
    SPRITES['EFFECT_6'] = []
    SPRITES['EFFECT_7'] = []

    for i in range(3): SPRITES['ATTACKIMATION_1'].append(pygame.image.load('Sprites/attackimation_1_' + str(i) + '.png'))
    for i in range(3): SPRITES['ATTACKIMATION_10'].append(pygame.image.load('Sprites/attackimation_10_' + str(i) + '.png'))

    for i in range(22): SPRITES['EFFECT_6'].append(pygame.image.load('Sprites/eff_6_' + str(i) + '.png'))
    for i in range(11): SPRITES['EFFECT_7'].append(pygame.image.load('Sprites/eff_7_' + str(i) + '.png'))

def sfx(j):
    global SOUND

    pygame.mixer.init()
    SOUND[j[:-4].upper()] = pygame.mixer.Sound('SFX/' + j)

def music():
    global SONGS
    SONGS = {
    'FATE_OCCURRENCES': pygame.mixer.Sound('Music/fate_occurrences.ogg'),
    #'BEYOND_THE_CLOUDS': pygame.mixer.Sound('Music/beyond_the_clouds.wav'), #'SIERRA_STREETS': pygame.mixer.Sound('Music/sierra_streets.wav'),
    'HEY_SAM': pygame.mixer.Sound('Music/hey_sam.wav'), 'URBAN_PLAGUE': pygame.mixer.Sound('Music/urban_plague.wav'),
    'EGG_RAP': pygame.mixer.Sound('Music/egg_rap.wav'),
    'CIGARUTO': pygame.mixer.Sound('Music/cigaruto.wav'),
    'EMOS_HERMANOS': pygame.mixer.Sound('Music/emos_hermanos.wav'),
    'ONCE_YOU_BECOME_FOREVER_YOU_ARE': pygame.mixer.Sound('Music/once_you_become_forever_you_are.wav'),
    }

def radio(i):
    global RADIO
    for j in os.listdir('Songs/FM_'+str(i)):
        RADIO[str(i)].append(j)

recent_data(0)
if FILES[3] != []:
    if FILES[3][0] == 'PT': import database_PT as database
    if FILES[3][0] == 'EN': import database_EN as database
    ID = FILES[0][0]
    CHAPTER = FILES[1][0]
    GAMETIME = FILES[2][0]
    LANG = FILES[3][0]
else: import database_PT as database