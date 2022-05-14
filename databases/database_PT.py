# -*- coding: utf-8 -*-
NAMES = ('Sidney','Barreto','Jane','Oliveira','Renan','Pinheiro','Diego','Donovan','Bianca','Pacheco','Lúcia','Figueiredo',
'Maicon','Neves','Iago','Dantas','Vinícius','Tavares','João','Pedro Lima','Sofia','Torres','Paulo','Sousa','Pietra','Mendonça','Hermes','Fonseca','Dalibor','Marković','Ryan','Figueiredo')

CINFO = [
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
''
]

PRONOUNS = {'he': 'Ele','she': 'Ela','they': 'Ele/Ela'}

CITIES = (('Itatiaia',(25,25,24,22,20,18,17,19,20,22,23,24)),
('Volta Redonda',(24,24,23,21,19,18,17,19,20,21,22,23)),
('Passa Quatro',(22,22,21,19,16,15,14,16,18,20,20,21)),
('Taubaté',(23,23,22,20,18,16,16,17,19,20,21,22)),
('Campos do Jordão',(17,16,15,13,11,10,10,12,14,15,15,15)),
('São Lourenço'),
('Varginha',(23,23,22,20,18,16,17,18,20,21,22,22)),
('Juiz de Fora',(23,23,21,20,18,17,17,18,20,21,21,21)),
('Seropédica',(27,26,25,24,22,21,21,22,22,23,25,25)),
('Petrópolis',(21,22,21,19,17,16,15,16,17,18,19,20)),
('Nova Iguaçu',(27,27,26,24,22,21,20,21,22,23,24,25)),
('Lagoa Santa',(24,24,23,21,19,18,20,21,22,23,23,22)),
('Rio de Janeiro',(26,25,25,24,22,21,21,21,22,22,24,24)),
('Resende',(25,25,24,22,20,19,18,19,21,22,23,23)))

CLASSES = {
'mercenary': {'STRENGHT': [5,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [4,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [3,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [3,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [2,22,22,25,25,26,28,30,30,32,33,35]},

'hunter': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'nomad': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'alchemist': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'hermit': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'medium': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'scientist': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'bard': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'thief': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},

'watchman': {'STRENGHT': [10,1,1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,5],
'RESISTANCE': [20,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
'AGILITY': [0,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,1,1,1,1.25,1.25,1.5,1.5,1.5,1.5,1.75],
'KNOWLEDGE': [0,1,2,2,2,2.25,2.25,2.25,2.25,2.25,2.5,2.5,2.5,2.5,2.5,2.75,2.75,2.75,2.75,2.75,3],
'CHARISMA': [20,22,22,25,25,26,28,30,30,32,33,35]},
}

NEXTLEVEL = (100,150,200,300,300,350,450,500,600)
PROFNAMES = {'STRENGHT': 'força','AGILITY': 'agilidade','RESISTANCE': 'resistência','KNOWLEDGE': 'sabedoria','CHARISMA': 'carisma'}
MONTHS = ('janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro')
ZODIAC = ('aquário','peixes','áries','touro','gêmeos','câncer','leão','virgem','libra','escorpião','sagitário','capricórnio')
MEASURINGS = {'hour': ('h',0.0187),'minutes': ('m',60),'distance': ('m',1),'volume': ('l',1),'weight': ('g',1),'temperature': ('ºC',1)}
#('inches',39.37008),

CNAMES = {
'mercenary': ['mercenário',['novato','intermediário','profissional']],
'hunter': ['caçador',['calouro','amador','regular','veterano','expert']],
'nomad': ['nômade',['iniciante','experiente','frequente','longa data']],
'alchemist': ['alquimista',['aprendiz','iniciado','estudante','discípulo','mestre']],
'hermit': ['eremita',['iniciado','experiente','ancião']],
'medium': ['médium',['em descoberta','em caminhada']],
'scientist': ['cientista',['graduada','bacharel','mestrada','doutorada','phd']],
'bard': ['bardo',['iniciante','de longa data']],
'thief': ['ladino',['novato','pequeno','bom','de respeito','veterano']],
'watchman': ['polical',['cabo','capitão','comandante','sargento','delegado']],

'gunslinger': 'pistoleiro','shooter': 'atirador','warrior': 'guerreiro','barbarian': 'bárbaro',
'mystic': 'místico','researcher': 'pesquisador','collector': 'colecionador','sportsman': 'esportista','sportswoman': 'esportista',
'traveler': 'viajante','merchant': 'comerciante','explorer': 'explorador','pilgrim': 'peregrino',
'sorcerer': 'feiticeiro','chemical': 'químico','blacksmith': 'ferreiro',
'priest': 'sacerdote','mentor': 'mentor','shaman': 'xamã','hermit': 'ermitão',
'telepath': 'telepata','host': 'hospedeiro','necromancer': 'necromante','soothsayer': 'adivinho',
'healer': 'curandeiro','mechanic': 'mecânico','interpreter': 'intérprete',
'singer': 'cantor','dancer': 'dançarino','charmer': 'encantador','mimic': 'mímico',
'spy': 'espião','assassin': 'assassino','smartass': 'espertalhão','acrobat': 'acrobata',
'detective': 'detetive','shooter': 'atirador','squire': 'escudeiro','forensic': 'forense'
}

CHAPTERS = [
['Depois do começo', 'prólogo',[25,12,2007,1,1],[0,32,0],('hauntedhouse_0',200,300)],
['Duplo Andantes', 'capítulo I',[25,1,2007,1,1],[11,10,0],('UFF_0',0,0)],
['Sangue Verde', 'capítulo II',[23,1,2007,1,1],[17,5,0],('archsite_0',0,0)],
['Não se meta com a gangue', 'capítulo III',[12,3,2007,1,1],[18,15,0],('pub_0',0,0)],
['Caminhões Canavieiros', 'capítulo IV',[13,1,2007,1,1],[9,22,0],('canefield_0',0,0)],
['Peste Negra', 'capítulo V',[6,4,2007,1,1],[14,2,0],('iagoshouse_0',0,0)],
['Vida Loka', 'capítulo VI',[12,2,2007,1,1],[18,32,0],('1urban_0',400,400)],
['Pelo Benefício do Mr. Kite!', 'capítulo VII',[25,1,2007,1,1],[10,47,0],('archsite_0',0,0)],
['Dr. Estanho', 'capítulo VIII',[17,8,2007,1,1],[13,36,0],('urban_0',0,0)],
['Milícia x Meliante', 'capítulo IX',[2,4,2007,1,1],[16,11,0],('urban_0',0,0)],
['Não Identificado', 'capítulo X',[18,9,2007,1,1],[12,0,0],('hotel_0',0,0)],
['Químicas Quimeras', 'capítulo XI',[14,9,2007,1,1],[13,44,0],('lab_0',0,0)],
['Quem tem medo de assombração?', 'capítulo XII',[17,10,2007,1,1],[18,30,0],('restaurant_0',0,0)],
['MP-XIII', 'epílogo',[25,12,2007,1,1],[0,3,0],('hauntedhouse_0',0,0)]
]

'''
ATTACKS
0 - faz nada
1 - atacar
7 - chamar anomalia
8 - roubar
9 - fugir
10 - charge

CONDITIONS
0 - normal
1 - de costas (perde um turno)
2 - repelente (anomalias não o atacam)
3 - fedor (não consegue batalhar)
4 - resfriado (comida cura menos e perde HP no frio)
5 - febre (perde HP no calor)
6 - fome (perde HP por não comer)
7 - sede (perde HP por não beber)
8 - sono (fica fora da batalha)
9 - náusea (erra facilmente)
10 - enjoo (não pode comer)
11 - fraqueza (ataques mais fracos)
12 - cegueira (não pode enxergar a batalha)
13 - preso (perde o turno)
14 - paralisia (perde o turno e não sai sozinho)
15 - inconsciente (não necessariamente sem HP)
16 - parasita (suga o HP)
17 - queimadura (perde HP, mas some)
18 - veneno aracnídeo (perde HP)
19 - veneno antiofídico (perde HP)
20 - veneno escorpiônico (perde HP)
21 - hemorragia (perde HP e não tem cura)
22 - regeneração (aumenta o HP a cada turno)
23 - invisibilidade (inimigos não te atacam)
24 - velocidade (ganha um turno extra)
'''

FTYPES = {0.0:'não incluso',1.0:'humanóide',1.1:'parte corporal',1.2:'metahumano',2.0:'quimera',2.1:'animal',3.0:'planta',4.0:'assombração',4.1:'psíquico',4.2:'espírito',4.3:'elemental',5.0:'inorgânico',5.1:'robótico',6.0:'extraterrestre'}
FHABITATS = {'jungle':'floresta','seaside':'litoral','sierra':'serra','cerrado':'cerrado','pantanal':'pantanal','manguezal':'manguezal','cave':'subterrâneo','urban':'urbano'}
FCONDITIONS = ('normal','costas','repelente','fedor','resfriado','febre','fome','sede','sono','náusea','enjôo','fraqueza','cegueira','preso','paralisia','inconsciente','parasita','queimadura',
	'veneno aracnídeo','veneno antiofídico','veneno escorpiônico','hemorragia','regeneração','invisibilidade','velocidade')
FWEAKNESSES = {'gold':'ouro','silver':'prata','copper':'cobre','tin':'estanho','lead':'chumbo','iron':'ferro','mercury':'mercúrio','fire':'fogo','water':'água','earth':'terra','air':'ar','explosive':'explosivos','corrosive':'corrosivos'}

#HABILITIES: [[name,description,damage,type,probability,attackimation],...]

FREAKS = {
'4.1.1': {'NAME': 'Gatacado','INFO': 'É um felino sobrenatural que flutua como um fantasma. Pequeno e ágil, porém bem frágil.',
'OA': 4,'HEIGHT': '0,80','HABITAT': 'jungle','STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 1,'VITALITY': 8,
'PATH': ((0,300),(500,0),(0,-300)),'DODGE': 'walk','AVATAR': {'head','eye','body'},'EYES': (9,-15),
'HABILITIES': [['Morder','O felino morde o oponente.',-5,1,40,1],['Arranhar','O felino usa suas garras para atacar o oponente.',-3,10,40,10],
['Ronronar','O felino ronrona, mostrando seu desprezo pela situação.',0,9,10,1],['Miar','O felino mia para o além, chamando outros felinos.',('4.1.0'),7,10,1]],
'FOOD': 'ingredient_mice','WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': 'reactor1','SONG': 'HEY_SAM','SCREAM': 1},
   
'lizardshrimp': {'NAME': 'Camaraleão','INFO': 'É um réptil que se fundiu com um camarão, não se sabe se é um alimento apetitoso.',
'HEIGHT': '0,23','HABITAT': 'jungle','TYPE': 'reptile',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Camuflar','O réptil se camufla no ambiente, aumentando sua AGILIDADE.',2,3],
['Língua','O réptil usa sua língua como chicote para atacar o oponente.',-3,1],
['Estalo','O réptil se estala, criando um campo de força elétrico.',-13,1]],
'WEAKNESS': 'EARTH','BLOOD': 10,'ITEM': ('food_camarão',50),'SONG': 'GREENBLOOD','SCREAM': 2},
   
'2.1.1': {'NAME': 'Pombo Pavão','INFO': 'Um pombo urbano com uma mutação que o fez desenvolver penas de pavão com olhos reais nas suas pontas.',
'OA': 2,'HEIGHT': '0,25','HABITAT': 'urban','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'horizontal','DODGE': 'walk',
'HABILITIES': [['Defecar','A ave defeca no oponente, infectando-o.',5,6,20,1],
['Hipnose','A ave hipnotiza o oponente com os olhos das penas de pavão, diminuindo sua AGILIDADE.',-2,3,20],
['Bicar','A ave bica o oponente.',-4,1,50,1],
['Gritar','A ave grita, com a possibilidade de outra anomalia entrar na batalha.',('madladcat','peacockpigeon'),7,10,1]],
'WEAKNESS': 'IRON','BLOOD': 20,'ITEM': ('food_peanut_candy',30),'SONG': 'URBAN_PLAGUE','SCREAM': 3},

'sickletoucan': {'NAME': 'Tucano Foice','INFO': 'Um estranho pássaro com um bico em formato de foice.',
'HEIGHT': '0,53','HABITAT': 'jungle','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stealth','DODGE': 'fly',
'HABILITIES': [['Ceifar','A ave utiliza o seu bico de foice para atacar seu oponente.',-20,1],
['Perfurar','A ave utiliza seu bico para furar seu oponente.',-15,1],
['Voar','A ave voa em volta do oponente, tonteando-o e deixando com NÁUSEA.',9,6]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': None,'SONG': 'FROM_RUSSIA_WITH_LOVE','SCREAM': 4},

'bunchofeyes': {'NAME': 'Cacho de Olhos','INFO': 'Vários olhos diferentes agrupados que possuem poderes hipnóticos. PS: NÃO É GUARANÁ, NÃO FAÇA SUCO.',
'HEIGHT': '0,30','HABITAT': 'jungle','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES':[['Encarar','Os olhos começam a encarar o oponente, amedrontando-o e fazendo seu ATAQUE abaixar.',-1,2,20,1],
['Atirar','Um dos olhos se lança no oponente.',-3,1,40,1],
['Plantar','Um olho se planta no chão com a possibilidade de germinar um novo cacho.',('bunchofeyes'),7,20,1],
['Explodir','Todos os olhos se soltam num ataque fulminante.',-7,1,20,1]],
'WEAKNESS': 'FIRE','BLOOD': 10,'ITEM': ('ingredient_eye',20),'SONG': 'GREENBLOOD','SCREAM': 5},

'bodybuilderfrog': {'NAME': 'Perereca Mil Grau','INFO': 'Um anfíbio que saiu da metamorfose antes da hora e ao mesmo tempo que manteve a cauda, desenvolveu braços fortes.',
'HEIGHT': '0,70','HABITAT': 'jungle','TYPE': 'aquatic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'jump',
'HABILITIES':[['Língua',['O anfíbio usa sua língua','para chicotear o oponente.'],-5,1],
['Porrada',['O anfíbio usa seus','braços musculosos para','bater no oponente.'],-8,1],
['Veneno',['O anfíbio libera toxinas','nas bolsas das suas','costas para infectar','o oponente.'],1,4],
['Salto',['O anfíbio pula pelo',' ambiente e aumenta','sua AGILIDADE.'],2,3]],
'WEAKNESS': 'EARTH','BLOOD': 10,'ITEM': None,'SONG': 'GREENBLOOD','SCREAM': 6},

'gospelant': {'NAME': 'Formiga Gospel','INFO': 'Um pequeno inseto insignificante cuja crença no divino demonstra uma anormalidade entre os artrópodes.',
'HEIGHT': '0,1','HABITAT': 'jungle','TYPE': 'arthropod',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Rezar',['O inseto pede','ao seu advesário para','que não o ataque.'],0,0,25,1],
['Perdoar',['O inseto perdoa','seu oponente por','atacá-lo.'],0,0,25,1],
['Meteoro divino',['O inseto invoca um','grande meteoro para','aniquilar seu oponente.'],-30,10,5,1],
['Louvar',['De alguma maneira, o','inseto canta hinos','deixando seu oponente','com SONO.'],8,6,45,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'FAITH_SHOW','SCREAM': 7},

#SEASIDE
'armedcrab': {'NAME': 'Carangueijo Armado','INFO': 'Um carangueijo que aprendeu a utilizar uma arma branca.',
'HEIGHT': '0,18','HABITAT': 'seaside','TYPE': 'arthropod',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [['Facada',['O crustáceo utiliza','sua arma branca para','perfurar seu oponente.'],-15,1],
['Pinçar',['O crustáceo utiliza','suas garras para','atacar seu oponente.'],-15,1]],
'WEAKNESS': 'COPPER','BLOOD': 10,'ITEM': None},

'hipocampus': {'NAME': 'Hipocampo','INFO': 'Um Hipocampo com o formato de um hipocampo.',
'HEIGHT': '2,30','HABITAT': 'seaside','TYPE': 'aquatic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'jump',
'HABILITIES': [['Aminésia',['O elemento utiliza','seus poderes psíquicos','para deixar seu','oponente com CEGUEIRA.'],12,6],
['Ciclone',['O elemento cavalga','na água para produzir','um tornado marinho.'],-30,1],
['Coice',['O elemento usa sua','cauda como chicote para','atacar seu oponente.'],-10,1],
['Cabeçada',['O elemento vai na','direção de seu oponente','para atacá-lo.'],-10,1]],
'WEAKNESS': 'TIN','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},

#CERRADO
'cattle': {'NAME': 'Gado','INFO': 'Um boi com chifres incrivelmente enormes, lendas folclóricas contam que elas são originárias de traições.',
'HEIGHT': '1,70','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Chifrar',['O bovino utiliza seus','enormes chifres para','atacar seu oponente'],-5,1,100,1],
['Berrante',['O bovino utiliza seus','próprios chifres para','chamar outros gados.'],['cattle','cow'],7]],
'WEAKNESS': 'GOLD','BLOOD': 10,'ITEM': None,'SONG': 'CATTLE_KING','SCREAM': 8},

'cow': {'NAME': 'Vaca','INFO': 'Um mamífero bovino fêmea que por muitas vezes é comparada a pessoas indevidas.',
'HEIGHT': '1,70','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Chifrar',['O bovino utiliza seus','enormes chifres para','atacar seu oponente'],-5,1,100,1],
['Leite',['O bovino utiliza suas','mamas para espirrar','leite no opontente.'],-10,1]],
'WEAKNESS': 'GOLD','BLOOD': 10,'ITEM': None,'SONG': 'CATTLE_KING','SCREAM': 8},

'lilanteater': {'NAME': 'Tamanduá Cotoco','INFO': 'Apesar do tamanho, pode ser bastante violento e perigoso.',
'HEIGHT': '0,80','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Arranhar',['O mamífero utiliza','suas garras para arranhar','seu oponente.'],-10,1,100,1],
['Língua',['O mamífero utiliza sua','enorme língua para chicotear','seu oponente.'],-15,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 9},

'pennanteater': {'NAME': 'Tamanduá Bandeirante','INFO': 'Grande e imponente como um urso, carrega pelo cerrado a bandeira da floresta.',
'HEIGHT': '1,20','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Arranhar',['O mamífero utiliza','suas garras para arranhar','seu oponente.'],-10,1,100,1],
['Língua',['O mamífero utiliza sua','enorme língua para chicotear','seu oponente.'],-15,1]],
'WEAKNESS': 'TIN','BLOOD': 10,'ITEM': None,'SONG': 'FROM_RUSSIA_WITH_LOVE','SCREAM': 9},

'militanteater': {'NAME': 'Tamanduá Militante','INFO': 'Carrega a bandeira da militância socialista por onde anda.',
'HEIGHT': '1,20','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Arranhar',['O mamífero utiliza','suas garras para arranhar','seu oponente.'],-10,1,100,1],
['Língua',['O mamífero utiliza sua','enorme língua para chicotear','seu oponente.'],-15,1]],
'WEAKNESS': 'EARTH','BLOOD': 10,'ITEM': None,'SONG': 'FROM_RUSSIA_WITH_LOVE','SCREAM': 9},

'termitribe': {'NAME': 'Cupinzal','INFO': 'Uma aldeia de cupins bem desenvolvida e organizada em sociedade.',
'HEIGHT': '1,40','HABITAT': 'cerrado','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'FIRE','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 7},

'termimpire': {'NAME': 'Cupimpério','INFO': 'Um império inteletual com uma forma de governo democrática para os cupins considerados cidadãos.',
'HEIGHT': '1,40','HABITAT': 'cerrado','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'AIR','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 7},

'termitropolis': {'NAME': 'Cupintrópole','INFO': 'Uma cidade bem estruturada nos moldes da civilização moderna...com cupins.',
'HEIGHT': '1,40','HABITAT': 'cerrado','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Canhões',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 7},

'tutuarmadillo': {'NAME': 'Tatu de Tutu','INFO': 'Um Tatu Bola com estilo e talento para o balê.',
'HEIGHT': '0,70','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'spin',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': ['clth_tutu',20],'SONG': 'HEY_SAM','SCREAM': 10},

'prettywolf': {'NAME': 'Loba Chique','INFO': 'A rainha do cerrado, corre com seus pelos cor de fogo e salto alto.',
'HEIGHT': '1,50','HABITAT': 'cerrado','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 11},

#PANTANAL
'prettyfish': {'NAME': 'Peixe Galã','INFO': 'Um peixe que abre a boca acima dos limites de sua mandíbula e da biologia, pelo menos ele é admirável.',
'HEIGHT': '1,20','HABITAT': 'swamp','TYPE': 'aquatic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'swim',
'HABILITIES': [['Aumentar',['O peixe aumenta o tamanho da sua face e volta ao normal, assustando o oponente e abaixando seu ATAQUE'],-2,2],
['Saltar',['O peixe salta na água e chicoteia o oponente com sua cauda'],-7,1],
['Morder',['O peixe morde o oponente com seus dentes limpos e branquinhos.'],-9,1],
['Brilhar',['O peixe reflete a luz do sol cegando o oponente.'],2,4]],
'WEAKNESS': 'EARTH','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 10},

'hammerbird': {'NAME': 'Pássaro Martelo','INFO': 'Companheiro do Tucano Foice, usa seu inusitado bico para martelar frutos e grãos.',
'HEIGHT': '0,50','HABITAT': 'pantanal','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [],
'WEAKNESS': 'EARTH','BLOOD': 10,'ITEM': ('ingredient_hammer_beak',20),'SONG': 'FROM_RUSSIA_WITH_LOVE','SCREAM': 11},

'flamencoflamingo': {'NAME': 'Flamingo Flamenguista','INFO': 'Uma ave com a peculiaridade de ter a anomalia FLAMENGO.',
'HEIGHT': '1,20','HABITAT': 'pantanal','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stealth','DODGE': 'fly',
'HABILITIES': [['Bolada',['A ave chuta uma bola na face do oponente.'],-13,1,50,1],
['Dibre',['Lamentamos o erro de ortografia, a ave dribla o oponente fazendo sua AGILIDADE aumentar.'],3,2,20,1],
['Rasteira',['A ave ataca o oponente se jogando no chão e derrubando-o.'],-10,1,27,1],
['Gabigol',['A ave recruta o profissional jogador de futebol GABIGOL, ganhando a batalha imediatamente.'],-50,1,3,1]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': ('clth_flamengo_shirt',10),'SONG': 'ONCE_YOU_BECOME_FOREVER_YOU_ARE','SCREAM': 12},

#MANGUEZAL
'spidermangue': {'NAME': 'Mangue Aranha','INFO': 'Uma árvore peculiar que possui pernas no lugar de raízes.',
'HEIGHT': '2,30','HABITAT': 'manguezal','TYPE': 'plant',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'STRENGHT': 2,'PATH': 'follow','DODGE': 'stay','HABILITIES': [],'WEAKNESS': 'FIRE','BLOOD': 10,'ITEM': None},
  
'crabman': {'NAME': 'Homem Carangueijo','INFO': 'Um carangueijo gigante que lembra uma música do Chico Science.',
'HEIGHT': '2,30','HABITAT': 'manguezal','TYPE': 'arthropod',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'STRENGHT': 2,'PATH': 'follow','DODGE': 'circle','HABILITIES': [],'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': ['ingredient_crab_claw',30],'SONG' :'CHICOLOGY'},

'communismbird': {'NAME': 'Carcará Comunista','INFO': 'O cruzamento de duas espécies de pássaros resultou em uma ave de rapina majestosa.',
'HEIGHT': '1,30','HABITAT': 'manguezal','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'circle',
'HABILITIES': [],
'WEAKNESS': 'GOLD','BLOOD': 10,'ITEM': None,'SONG': 'FROM_RUSSIA_WITH_LOVE'},

#CAVE
'bat': {'NAME': 'Morcego','INFO': 'Uma árvore peculiar que possui pernas no lugar de raízes.',
'HEIGHT': '2,30','HABITAT': 'cave','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [],
'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': None,'SONG': 'GREENBLOOD','SCREAM': 13},

'phlegm': {'NAME': 'Catarro','INFO': 'Uma estranha substância viva pegajosa e muito nojenta.',
'HEIGHT': '2,30','HABITAT': 'cave','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'hide',
'HABILITIES': [],
'WEAKNESS': 'MERCURY','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},

#AQUATIC
'cattlefish': {'NAME': 'Peixe Gado','INFO': 'Um búfalo que nadou tanto que ganhou uma cauda de sereia. Seria um tipo de Hipocampo?',
'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'aquatic',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'STRENGHT': 2,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'GOLD','BLOOD': 10,'ITEM': None,'SONG': 'CATTLE_KING','SCREAM': 8},

'belledoplhine': {'NAME': 'Belle Dolphine','INFO': 'Fruto de uma relação entre uma E-Girl e o Boto.','HEIGHT': '2,10','HABITAT': 'jungle','TYPE': 'aquatic',
'AGILITY': 7,'HP': 42,'RESISTANCE': 1,'STRENGHT': 2,'PATH': 'follow','DODGE': 'circle','HABILITIES': [['Ahegao',['O mamífero tenta sensualizar o oponente simulando um ato sexual, mas faz o efeito contrário abaixando seu ATAQUE'],-3,2],
['Água de banho',['O mamífero oferece água de banho para o oponente, este o ingere e obtém HERPES.'],2,4],
['Nadar',['O mamífero nada no ambiente para recuperar sua VITALIDADE.'],10,1],
['Canto submarino',['O mamífero entoa uma canção para chamar uma anomalia para a batalha.'],1,5]],'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': None},

#URBAN
'emohipster': {'NAME': 'Emo Hipster','INFO': 'A DDA ainda não sabe se esse ser é uma anomalia ou apenas um cara estranho que chegou e parece não achar lugar no corpo que Deus encarnou.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Cantar',['O esquisito começa a cantar uma música dos los hermanos com uma guitarra.'],1,4],
['Guitarrada',['O esquisito usa sua guitarra para atacar o oponente.'],-10,1],
['Óculos sem lente',['O esquisito põe óculos sem lente para confundir o oponente, abaixando sua AGILIDADE.'],-1,3],
['Franja',['O esquisito balança sua franja, aumentando seu ATAQUE.'],2,2]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'EMOS_HERMANOS','SCREAM': 14},

'wesleylesbian': {'NAME': 'Wesley Sapatão','INFO': 'A DDA ainda não sabe se esse ser é uma anomalia ou apenas um cara estranho que chegou e parece não achar lugar no corpo que Deus encarnou.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'EMOS_HERMANOS','SCREAM': 15},

'giantear': {'NAME': 'Orelhão','INFO': 'Um fungo que realmente existe, e quis trabalhar pra telefônica.',
'HEIGHT': '2,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Soar',['O elemento vibra seus tímpanos,','abaixando a RESISTÊNCIA do oponente.'],-5,4],
['Fichas',['O elemento arremessa fichas','do seu cofrinho.'],-10,1],
['Trote',['O elemento te passa um trote,','enganando o oponente e abaixando','sua FORÇA'],1,6],
['Ligação',['O elemento faz uma ligação,','chamando outra anomalia.'],2,6]],
'WEAKNESS': 'GOLD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 16},
 
'greenchicken': {'NAME': 'Galinha Verde','INFO': 'Uma ave com a terrível anomalia INTEGRALISMO.',
'HEIGHT': '0,60','HABITAT': 'urban','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'COPPER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 17},

'blindchicken': {'NAME': 'Galo Cego','INFO': 'Uma ave com deficiência visual, mas bom humor e problemas com bebida.',
'HEIGHT': '0,60','HABITAT': 'urban','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [],
'WEAKNESS': 'COPPER','BLOOD': 10,'ITEM': ('melee_walking_stick',20),'SONG': 'HEY_SAM','SCREAM': 17},
 
'yellowdocs': {'NAME': 'Médicos de amarelo','INFO': 'Embora seu papel seja de ajudar a população, onde eles aparecem há morte.',
'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'guard',
'HABILITIES': [],
'WEAKNESS': 'TIN','BLOOD': 0,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 18},
 
'zombie': {'NAME': 'Zumbis','INFO': 'Não são de fato mortos-vivos, mas sua terrível saúde lembra um.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 19},
 
'humanfeet': {'NAME': 'Pé de moleque','INFO': 'É um doce de amendoim delicioso muito comum em festas juninas...não pera. É um membro que se separou do corpo humano e agora consegue viver por conta própria, não confundir com mãozinha da Família Adams.',
'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'jump',
'HABILITIES': [['Pisar',['O membro pisa no oponente com toda sua força.'],-10,1,50,1],['Chutar',['O membro chuta o oponente, mesmo perdendo seu equilíbrio.'],-12,1,30,1],
['Cura',['O membro se cura utilizando uma técnica que não entendemos devido ás limitações de seu corpo.'],10,1,10,1],['Agachar',['O membro concentra a energia dos seus pés e aumenta seu ATAQUE.'],5,2,10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': ['food_pedemoleque'],'SONG': 'HEY_SAM','SCREAM': 20},
 
'captaincatfish': {'NAME': 'Cabeça de Bagre!!','INFO': 'Um homem com cabeça de bagre e com péssima compreensão de ritmo.',
'HEIGHT': '1,90','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [],
'WEAKNESS': 'MERCURY','BLOOD': 10,'ITEM': None,'SONG': 'CATFISH_HEAD','SCREAM': 21},
  
'primateman': {'NAME': 'Homem Primata','INFO': 'Um humano que sabe dançar muito bem.',
'HEIGHT': '2,00','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DINOSAUR_HEAD','SCREAM': 22},
  
'drynwetman': {'NAME': 'Homem Seco e Molhado','INFO': 'Um homem que possui a anomalia de estar seco e molhado ao mesmo tempo.',
'HEIGHT': '1,80','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'LATINO_LIFE','SCREAM': 14},

#SEWERS
'crodile': {'NAME': 'Jaré','INFO': 'Um réptil que, graças á uma sílaba a menos em seu nome, perdeu dois de seus membros. Não muito ágil, mas causa muito dano.',
'HEIGHT': '1,90','HABITAT': 'swamp','TYPE': 'reptile',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'walk',
'HABILITIES': [['Morder',['O réptil morde seu oponente'],-6,1],['Esperar',['O réptil aumenta seu ATAQUE.'],1,2],
['Bote',['O réptil ataca com uma mordida em avanço.'],-5,1],
['Esconder',['O réptil se esconde no ambiente, aumentando sua AGILIDADE.'],1,3]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 23},

'fatherat': {'NAME': 'Rato padre','INFO': 'Um ratinho santo e divino.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [['Morder','O roedor morde o oponente.',-5,1,100,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DORIME','SCREAM': 24},

'bishoprat': {'NAME': 'Rato bispo','INFO': 'Um ratinho santo e divino.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DORIME','SCREAM': 24},

'cardinalrat': {'NAME': 'Rato cardeal','INFO': 'Um ratinho santo e divino.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DORIME','SCREAM': 24},

#ALIEN
'hermite': {'NAME': 'Hermita','INFO': 'Este ser extraterrestre com pele gelatinosa se parece mais com um bichinho de pelúcia.',
'HEIGHT': '0,25','HABITAT': 'cave','TYPE': 'alien',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'horizontal','DODGE': 'walk',
'HABILITIES': [['Nada',['O alienígena não reage.'],0,0,100,1]],
'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'HERMITES','SCREAM': 25},
  
#MISCELANEOUS
'squaresponge': {'NAME': 'Esponja Quadrada','INFO': 'Ele vai acabar com sua raça.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'jump',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': ['food_egg',50],'SONG': 'EGG_RAP','SCREAM': 26},

'eggrapper1': {'NAME': 'MC Ovinho','INFO': 'Ele vai acabar com sua raça.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'jump',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': ['food_egg',50],'SONG': 'EGG_RAP','SCREAM': 26},

'eggrapper2': {'NAME': 'Ovinho Caipira','INFO': 'Ele vai acabar com sua raça.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'jump',
'HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],
'WEAKNESS': 'IRON','BLOOD': 10,'ITEM': ['food_egg',50],'SONG': 'EGG_RAP','SCREAM': 26},

'bigeye': {'NAME': 'Zoiudo','INFO': 'Tira os zóio, tira os zóio, vê se me erra.',
'HEIGHT': '3,00','HABITAT': 'urban','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'circle',
'HABILITIES': [['Olhar mortal','O elemento infere dano psicológico no oponente.',-5,1,100,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 5},

'cigaruto': {'NAME': 'Xaruto','INFO': 'Estranhamente lembra um personagem de um anime que não é tão bom quanto Evangelion.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'teleport',
'HABILITIES': [['Fumaça ninja',['O elemento solta uma fumaça com mais de 100.000 substâncias tóxicas incluindo nicotina e enxofre, envenenando o oponente.'],-3,1],
['Chama ninja',['O elemento sopra uma labareda ardente, incendiando o oponente.'],-2,1],
['Xaringan',['O elemento usa uma espécime de energia oculta para aumentar seu ATAQUE.'],-3,1],
['Vaporizar',['O elemento se transforma num cigarro eletrônico, relaxando e diminuindo sua AGILIDADE.'],-3,1]],
'WEAKNESS': 'LEAD','BLOOD': 100,'ITEM': None,'SONG': 'CIGARUTO','SCREAM': 27},
 
'elkeys': {'NAME': 'Chaves','INFO': 'Um molho de chaves que ninguém tem paciência.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [],
'WEAKNESS': 'COPPER','BLOOD': 10,'ITEM': None,'SONG': 'EL_KEYS','SCREAM': 28},

'mayanman': {'NAME': 'Tim Maia','INFO': 'Um mesoamericano com ótima afinação vocal.',
'HEIGHT': '1,80','HABITAT': 'jungle','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'MAYANMAN','SCREAM': 29},

'hotman': {'NAME': 'Cremado Cremoso','INFO': 'Um homem que sofreu uma combustão espontânea, mas continua vivo graças á mutação.',
'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [['Bater',['O indivíduo bate no oponente.'],-5,1],
['Cinzas',['O indivíduo joga cinzas no oponente, abaixando sua AGILIDADE.'],-3,3],
['Dançar',['O indivíduo começa a rebolar e mostrar seu charme.'],0,8],
['Infectar',['O indivíduo entra dentro do oponente através das cinzas, diminuindo seu ATAQUE.'],-3,2]],
'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': None,'SONG': 'CATFISH_HEAD','SCREAM': 31},
   
'spontaneouscombustion': {'NAME': 'Combustão Espontânea','INFO': 'Uma homem normal que teve o azar de ter essa anomalia, e agora vive como uma tocha humana.',
'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'dance',
'HABILITIES': [['Bater',['O indivíduo bate no oponente.'],-8,1],
['Labareda',['O indivíduo sopra uma labareda no','oponente, fazendo ele se queimar.'],3,4],
['Queimadura',['O indivíduo se ilumina tanto que','o oponente perde a visão.'],9,6],
['Bolas de Fogo',['O indivíduo arremessa bolas','de fogo que vão te atolar.'],-14,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'CATFISH_HEAD','SCREAM': 31},
     
'crucifiedbiscuit': {'NAME': 'Biscoito Crucificado','INFO': 'Esse ser humano não está em um estado muito bacana...É um biscoito de gengibre possuído preso num crucifixo, parece até coisa de algum filme B!',
'HEIGHT': '0,30','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Chantily',['O possuído jorra chantily venenoso no oponente.'],1,4],
['Gargalhar',['O possuído ri de uma maneira terrorífica, diminuindo o ATAQUE do oponente.'],-2,2],
['Bater',['O possuído usa seu crucifixo para atacar o oponente.'],-8,1],
['Perfurar',['O possuído perfura o corpo do oponente usando o crucifixo'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DORIME','SCREAM': 31},
  
'ppap': {'NAME': 'Caneta Azul', 'INFO': 'É um objeto possuído por um fantasma e agora tem o poder de atormentar as pessoas com uma música irritante.',
'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [['Rabiscar',['O elemento se move contra o oponente','e o rabisca o rosto.'],-8,1],
['Cantar',['O elemento atormenta o oponente','através de uma canção pertubadora.'],6,4],
['Explodir',['O elemento se estoura, espalhando','tinta na cara do oponente.'],-20,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'PPAP','SCREAM': 32},

'crush': {'NAME': 'Crush','INFO': 'Não conseguimos coletar muitos dados dessa anomalia, só sabemos que é a mais forte e nunca foi sequer derrotada.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 999,'AGILITY': 999,'RESISTANCE': 999,'VITALITY': 999,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Iludir',['A anomalia usa as palavras','como lanças e ataca o','coração do oponente.'],-99999,1]],
'BLOOD': 10,'ITEM': None,'SONG': 'MAYANMAN','SCREAM': 15},
 
'mecanicmonkey': {'NAME': 'Macaco','INFO': 'Um macaco mecânico portando um macaco.',
'HEIGHT': '1,80','HABITAT': 'jungle','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'jump',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': ('melee_spanner',10),'SONG': 'MONKEY_MAN','SCREAM': 33},

'roundsquare': {'NAME': 'Quadrado Redondo','INFO': 'Uma obra da geometria não-euclidiana que só poderia ser imaginada em teorias matemáticas.',
'HEIGHT': '2,00','HABITAT': 'urban','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'circle',
'HABILITIES': [['Morder','O felino morde o oponente.',-5,1,100,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'TUBULAR_BELLS','SCREAM': 32},

'hakunapotato': {'NAME': 'Hakuna Batata','INFO': 'Uma dupla inseparável de tubérculos.',
'HEIGHT': '0,30','HABITAT': 'jungle','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'jump',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 35},
 
'wingedcan': {'NAME': 'Lata Alada','INFO': 'Uma lata de energético que tenta ser irada e tem o único atributo que prometeu dar á quem o consumisse. É literalmente uma piada.',
'HEIGHT': '0,15','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'fly',
'HABILITIES': [['Voar',['Aumenta sua agilidade'],1,3],
['Energizar',['Aumenta seu dano de arremesso'],2,2],
['Ressaca',['A lata se auto destrói'],0,1],
['Arremessar',['A lata se joga no oponente, se machucando junto.'],-1,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 32},
 
'teresacristinabust': {'NAME': 'Busto de Teresa Cristina','INFO': 'Um busto muito pesado e cheio, de ódio no seu coração.',
'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [['Atacar',['O elemento se joga contra o oponente.'],-10,1],
['Esmagar',['O elemento cai em cima','da cabeça do oponente.'],-20,1],
['Voar',['O elemento voa ao derredor','do oponente'],0,8]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 32},
   
'tarsila': {'NAME': 'Tarsila','INFO': 'Um auto retrato da pintora Tarsila do Amaral, te encarando pronta pra acabar com sua raça. Óleo sobre tela.',
'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 33},

'groovyduck': {'NAME': 'Pato da Braba','INFO': 'Um patinho com óculos escuros, estilo e bom gosto musical.',
'HEIGHT': '0,60','HABITAT': 'urban','TYPE': 'flying',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'ONCE_YOU_BECOME_FOREVER_YOU_ARE','SCREAM': 35},
 
'racketfly': {'NAME': 'Mosca de Raquete','INFO': 'Certamente matar uma mosca é difícil, mas nunca imaginou que ela iria se vingar, né?',
'HEIGHT': '0,01','HABITAT': 'urban','TYPE': 'arthropod',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [['Atacar','A pintura se joga contra o oponente, machucando a si no processo.',-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': ['melee_racket',10],'SONG': 'TUBULAR_BELLS','SCREAM': 32},
 
'conicaltoilet': {'NAME': 'Vaso Cônico','INFO': 'Um vaso sanitário que infelizmente não cumpre seu papel higiênico.',
'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 32},
 
'edmoto': {'NAME': 'Ed Moto','INFO': 'Um famoso cantor que largou sua carreira artística para se tornar uma motocicleta, livre a andar pelas rodovias.',
'HEIGHT': '1,20','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 36},
 
'siamesecat': {'NAME': 'Gato Siamês','INFO': 'Gatos gêmeos siameses, eles sempre estão ao seu lado. Esse gato tem algo que não consigo explicar.',
'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'WATER','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 1},

'pisadeira': {'NAME': 'Pisadeira','INFO': 'Esta mulher descabelada e aterrorizante aparece nas camas de várias pessoas apenas para matá-los pisando em suas barrigas.',
'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'FIRE','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 15},
 
#CHEFES
'bluebulldog': {'NAME': 'Bulldogue Azul','INFO': 'Tudo o que sabemos sobre esta anomalia é que se trata de um canino de cor azulada.',
'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'boss',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 100,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 37},

'samaumaant': {'NAME': 'Formiga Samaúma','INFO': 'Este artrópode gigante tem a força proporcional á uma formiga comum, ou seja, pode carregar x vezes o seu próprio peso.',
'HEIGHT': '1,30','HABITAT': 'urban','TYPE': 'arthropod',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'circle',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 100,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 7},

'guaranawolf': {'NAME': 'Lobo Guaraná','INFO': 'Um lobo que escapou de seu habitat natural e andou tomando muito guaraná.',
'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 100,'ITEM': ('drink_guarana',100),'SONG': 'HEY_SAM','SCREAM': 9},

'araraucaria': {'NAME': 'Araraucária','INFO': 'Uma árvore animal que possui penas coloridas no lugar de folhas.',
'HEIGHT': '10,2','HABITAT': 'jungle','TYPE':'plant',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Algazarra',['Barulhos estranhos saem das folhas do vegetal, diminuindo o ATAQUE do oponente.'],-1,2],
['Fruta',['O vegetal deixa cair uma fruta de um dos galhos.'],-6,1],['Regeneração',['O vegetal drena recursos de suas raízes e recupera 10 HP.'],10,1]],
'WEAKNESS': 'LEAD','BLOOD': 100,'ITEM': None,'SONG': 'JUNGLE_JINGLE','SCREAM': 38},
 
'saltgolem': {'NAME': 'Golem do Sal','INFO': 'Nada se sabe sobre esta anomalia.',
'HEIGHT': '3,00','HABITAT': 'urban','TYPE': 'mystic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 39},

'papamouse': {'NAME': 'Rato Papa','INFO': 'O imponente e religioso líder da seita de ratinhos.',
'HEIGHT': '0,40','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'teleport',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 24},

'lucyintheskywithdiamonds': {'NAME': 'Lúcia no céu de diamantes','INFO': 'A policial se transformou em uma mulher com olhos de caleidoscópio.',
'HEIGHT': '1,80','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'circle',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': ('SHINE_ON_LUCY_IN_THE_SKY',4),'SCREAM': 15},

'mrkite': {'NAME': 'Mr.Kite','INFO': 'Um misterioso mágico e empresário que frequentava o Edifício Esmeralda.',
'HEIGHT': '1,50','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'teleport',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'MR_KITE','SCREAM': 14},

'possessedpietra': {'NAME': 'Pietra Possessa','INFO': 'Essa abominável aberração um dia foi o amor da vida de alguém.',
'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 15},

'caesarean': {'NAME': 'Cesariana','INFO': 'Um feto dentro de uma bolha numa cesariana com poderes psíquicos.',
'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Escudo','O feto reforça a resistência da bolha.',1,6],
['Cordão Umbilical','O feto drena a energia de sua hospedeira e recupera sua VITALIDADE.',10,1],
['Grito molecular','O feto grita em um nível estratosféricamente alto, agitando as moléculas de seus oponentes.',-15,1],
['Líquido Uterino','O feto arremesa o líquido uterino da bolha nos oponentes, confundindo-os e dando NÁUSEA.',2,4]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 5},

'drtin': {'NAME': 'Dr. Estanho','INFO': 'Este misterioso cientista é o responsável pelo surgimento das quimeras.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'boss',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'guard',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'DR_TIN','SCREAM': 15},

'mret': {'NAME': 'Tio Etê','INFO': 'Todos esperavam que ele fosse um sábio extraterrestre que ensinasse o segredo da vida, mas na verdade é apenas um cara enrolado em papel higiênico.',
'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'boss',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'THE_X_FILES_THEME','SCREAM': 15},

'ciborgchicken': {'NAME': 'Galo Ciborgue do SENAI','INFO': 'Rinha de galo foi uma coisa levada muito á sério por um engenheiro mecatrônico.',
'HEIGHT': '0,60','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 17},

'poltergeist': {'NAME': 'Poltergeist','INFO': 'Não é uma criatura, mas uma manifestação sobrenatural que pode ser mais perigosa do que qualquer monstro.',
'HEIGHT': '???','HABITAT': 'urban','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'none',
'HABILITIES': [],
'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': 'HERE_COMES_THE_DEATH','SCREAM': 40},

'dragon': {'NAME': 'Dragão','INFO': 'É um dragão. Um dragão de verdade.',
'HEIGHT': '+100,00','HABITAT': 'urban','TYPE': 'mystic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'fly',
'HABILITIES': [],
'WEAKNESS': None,'BLOOD': 10,'ITEM': None,'SONG': 'ALCHIMERA','SCREAM': 41},

#MERCENARIES
'thuga': {'NAME': 'Bandido A','TYPE': 'mercenary','STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]],'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'HEY_SAM'},

'vinicius': {'NAME': 'Vinícius','TYPE': 'mercenary','STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]],'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'HEY_SAM'},

'pietra': {'NAME': 'Pietra','HEIGHT': '1,70','TYPE': 'mercenary','STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'STRENGHT': 2,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Atirar','',-8,1,100,1]],'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'HEY_SAM'},

#OTHER
'target': {'NAME': 'Alvo','HABITAT': 'urban','TYPE': 'inorganic','STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'stay',
'HABILITIES': [['Fazer nada',[],0,6]],'WEAKNESS': 'LEAD','BLOOD': 0,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 14},

#SECRET
'ancap': {'NAME': 'Anarcocapitalismo','INFO': 'Vamos mesmo tirar sarro de uma ideologia política utópica? Sim, vamos.',
'HEIGHT': '0,00','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'stay','DODGE': 'spin',
'HABILITIES': [['Diálogo',['O elemento tenta lhe convencer.'],-5,1,100,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'FREAK_FRENZY','SCREAM': 30},

'steroids': {'NAME': 'Asteróides','INFO': 'Uma pedra espacial que faz crossfit e usa whey protein. O antidoping é sua maior fraqueza.',
'HEIGHT': '1,80','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 34},

'obamium': {'NAME': 'Obamium','INFO': 'Graças á muita pesquisa científica da FIOCRUZ, os brasileiros foram os primeiros em todo o mundo a sintetizar este precioso material.',
'HEIGHT': '0,50','HABITAT': 'urban','TYPE': 'psychic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'TUBULAR_BELLS','SCREAM': 32},

'fausthanos': {'NAME': 'Fausthanos','INFO': 'Este extraterrestre costumava ser um grande líder militar de um planeta distante, mas decidiu largar tudo para virar apresentador de programa de auditório.',
'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'humanoid',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'stay',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'SUPER_SUNDAY','SCREAM': 34},

'flatearth': {'NAME': 'Terra Plana','INFO': 'Algo tão estúpido que classificamos como uma anomalia científica.',
'HEIGHT': '0','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [['Atacar',['A pintura se joga contra o oponente, machucando a si no processo.'],-10,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 5},
 
'torpedosquid': {'NAME': 'Lula Torpedo','INFO': 'Um molusco que antige seus oponentes como um torpedo. Apesar de enorme, forte e resistente, se locomove muito devagar.','HEIGHT': '2,10','HABITAT': 'sea','TYPE': 'aquatic',
'AGILITY': 1,'HP': 50,'RESISTANCE': 1,'STRENGHT': 2,'PATH': 'follow','DODGE': 'hide','HABILITIES': [['Tentáculos','O molusco usa seus tentáculos para atacar seu oponente.',-5,1],
['Jato de tinta','O molusco atira um jato de tinta que impossibilita o oponente de atacar.',-5,3],
['Camuflagem',['O molusco se disfarça no ambiente, aumentando sua AGILIDADE.'],2,3],['Torpedo',['O molusco acerta o oponente com um ataque explosivo que acerta todos á volta, super efetivo.'],-15,1]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},

'abaporu': {'NAME': 'Abaporu','INFO': 'Uma pintura modernista que criou vida própria e por sinal é canibal.',
'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'walk',
'HABILITIES': [['Pisar','A pintura pisa no oponente esmagando-o.',-13,1],
['Fúria','A pintura grita furiosamente aumentando seu ATAQUE.',3,2],
['Proteger','A pintura reforça sua proteção de acrílico sobre a tela',1,6],
['Reforço','A pintura chama outra pintura para ajudar na batalha.',1,5]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},

'tsunamifreezer': {'NAME': 'Geladeira Tsunami','INFO': 'Essa grande invenção da humanidade tem a capacidade de reproduzir ondas sonoras em volumes extremamente altos.',
'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'inorganic',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [['Tsunami',['O elemento emite ondas','sonoras tão altas que','empurram o advesário.'],-30,1],
['Ritmo cruel',['O elemento reproduz um','ritmo tão agitado que','tonteia seu advesário,','deixando-o com NÁUSEA.'],5,5]],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'TSUNAMI_FREEZER'},

'polishcow': {'NAME': 'Vaca Polonesa','INFO': 'Um bovino que irá lhe ensinar uma importante lição sobre narcóticos em uma língua que você não conhece.',
'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'mammal',
'STRENGHT': 2,'AGILITY': 4,'RESISTANCE': 0,'VITALITY': 6,'PATH': 'follow','DODGE': 'spin',
'HABILITIES': [],
'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'POLISH_COW','SCREAM': 8},
}

ITEMENEMIES = {'drink_guarana': ('wingedcan',100),'key_bedroom': ('elkeys',100),'tool_pen': ('ppap',100),'cigar': ('cigaruto',0)}

ITEMS = {
#BAGS (name,description,price,volume,weight)
'bag1': {'NAME': 'bolsinha','DESCRIPTION': 'Guarde seus itens nele e leve para qualquer lugar. Volume: 5 - Peso: 5','PRICE': 1000,'VOLUME': 5,'WEIGHT': 5,'PROPERTIES': {}},
'bag2': {'NAME': 'bolsa','DESCRIPTION': 'Guarde seus itens nele e leve para qualquer lugar. Volume: 10 - Peso: 10','PRICE': 2500,'VOLUME': 10,'WEIGHT': 10,'PROPERTIES': {}},
'bag3': {'NAME': 'mala','DESCRIPTION': 'Guarde seus itens nele e leve para qualquer lugar. Volume: 20 - Peso: 15','PRICE': 5000,'VOLUME': 20,'WEIGHT': 15,'PROPERTIES': {}},
'bag4': {'NAME': 'mochila','DESCRIPTION': 'Guarde seus itens nele e leve para qualquer lugar. Volume: 30 - Peso: 20','PRICE': 7500,'VOLUME': 30,'WEIGHT': 20,'PROPERTIES': {}},
'bag5': {'NAME': 'mala de rodinhas','DESCRIPTION': 'Guarde seus itens nele e leve para qualquer lugar. Volume: 30 - Peso: 25','PRICE': 10000,'VOLUME': 30,'WEIGHT': 25,'PROPERTIES': {}},
'tube100': {'NAME': 'frasco de sulfúrio 100ml','DESCRIPTION': 'Feita especialmente para guardar sangue verde.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'SIZE': 100}},
'tube250': {'NAME': 'pote de sulfúrio 250ml','DESCRIPTION': 'Feita especialmente para guardar sangue verde.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'SIZE': 250}},
'tube500': {'NAME': 'garrafa de sulfúrio 500ml','DESCRIPTION': 'Feita especialmente para guardar sangue verde.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'SIZE': 500}},
'wallet': {'NAME': 'carteira','DESCRIPTION': 'Use para guardar seu dinheiro e coisas pequenos. JAMAIS PERCA ISSO!','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'lock': {'NAME': 'cadeado','DESCRIPTION': 'Use para proteger objetos.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith1': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith2': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith3': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith4': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith5': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith6': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'locksmith7': {'NAME': 'chaveiro','DESCRIPTION': 'Use para guardar até duas chaves.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'bottle1': {'NAME': 'garrafa vermelha','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle2': {'NAME': 'garrafa laranja','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle3': {'NAME': 'garrafa amarela','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle4': {'NAME': 'garrafa verde','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle5': {'NAME': 'garrafa ciano','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle6': {'NAME': 'garrafa azul','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
'bottle7': {'NAME': 'garrafa rosa','DESCRIPTION': 'Use para armazenar bebidas.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'SIZE': 3}},
   
#HEAD ACCESORIES (name,description,price,volume,weight)
'head_hairclip': {'NAME': 'xuxinha','DESCRIPTION': 'Pra amarrar o cabelo.','PRICE': 30,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},
'head_hat1': {'NAME': 'boné','DESCRIPTION': 'Pra proteger do sol e ficar estiloso.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_hat2': {'NAME': 'gorro','DESCRIPTION': 'Reza a lenda que todo mundo que usa vira um mendigo.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_hat3': {'NAME': 'chapéu de sol','DESCRIPTION': 'Ideal para a praia','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_hat4': {'NAME': 'chapéu de aviador','DESCRIPTION': 'De um falecido senhor...','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_glasses1': {'NAME': 'óculos de grau','DESCRIPTION': 'Apenas pra quem precisa, senão vocêganha cegueira.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_glasses2': {'NAME': 'óculos escuros','DESCRIPTION': 'Pra quem não tem colírio.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_glasses3': {'NAME': 'óculos redondos','DESCRIPTION': 'Qualquer um que usá-lo se transformaimediatamente no Harry Potter.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_glasses4': {'NAME': 'óculos retrô','DESCRIPTION': 'Apenas para quem é hype de verdade.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'head_glasses5': {'NAME': 'visor de laboratório','DESCRIPTION': 'Se não usar um ácido pode cair no seu olho.','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},

#CUSTOM CLOTHES (name,description,price,volume,weight,color)
'clth_shirt1': {'NAME': 'camisa preta','DESCRIPTION': 'O traje predileto dos solitários.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 0},
'clth_shirt2': {'NAME': 'camisa laranja','DESCRIPTION': 'Roupa casual.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 2},
'clth_shirt3': {'NAME': 'camisa vermelha','DESCRIPTION': 'Roupa casual.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 3},

'clth_regatta1': {'NAME': 'regata vermelha','DESCRIPTION': 'É excelente caso esteja fazendo calor.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 3},

'clth_stripeshirt01': {'NAME': 'camisa vermelha listrada','DESCRIPTION': 'Parece com o uniforme do flamengo.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 3},

'clth_jacket1': {'NAME': 'jaqueta preta','DESCRIPTION': 'Pra dar uma de Ramones.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '01'},
'clth_jacket2': {'NAME': 'avental','DESCRIPTION': 'Para pesquisadores.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},

'clth_flannel1': {'NAME': 'flanela verde','DESCRIPTION': 'Pareçe roupa de festa junina.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '02'},
'clth_flannel2': {'NAME': 'flanela vermelha','DESCRIPTION': 'Conhece o Iberê? então.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '03'},
'clth_flannel3': {'NAME': 'flanela laranja','DESCRIPTION': 'Parece o tipo de roupa que um menino do mato grosso usaria.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '03'},

'clth_sweatshirt1': {'NAME': 'moletom cinza','DESCRIPTION': 'Pra aqueles que não tem paciêciapra escolher roupa.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '04'},
'clth_sweatshirt2': {'NAME': 'moletom azul','DESCRIPTION': 'Pra aqueles que não tem paciêciapra escolher roupa.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '05'},
'clth_tutu00': {'NAME': 'tutu','DESCRIPTION': 'Uma bela saia para bailarinas.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '07'},

'clth_printedshirt1': {'NAME': 'camisa de ET','DESCRIPTION': 'A favorita dos ufólogos.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 3},
'clth_printedshirt2': {'NAME': 'camisa de banda','DESCRIPTION': 'Está escrito "Senta que lá vem história".','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': 3},

'clth_bikini1': {'NAME': 'biquíni vermelho','DESCRIPTION': 'Bom para ir á praia','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'clth_fantasy1': {'NAME': 'fantasia de anjo','DESCRIPTION': 'A fantasia mais usada no carnaval.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'clth_fantasy2': {'NAME': 'fantasia de diabo','DESCRIPTION': 'A segunda fantasia mais usada no carnaval.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'clth_fantasy3': {'NAME': 'fantasia de gatinho','DESCRIPTION': 'Talvez essa seja a fantasia mais usada.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'clth_fantasy4': {'NAME': 'roupa de passista','DESCRIPTION': 'Foi encontrada no edifício esmeralda.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},

'clth_uniform1': {'NAME': 'uniforme de faculdade','DESCRIPTION': 'Uniforme da Universidade Federal Fluminense.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'clth_uniform2': {'NAME': 'uniforme de zelador','DESCRIPTION': 'Quem usa essa roupa geralmente é bom de conversa.','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},

'undr_shorts1': {'NAME': 'shorts jeans','DESCRIPTION': 'Esse tipo de calça é a sensação do momento!','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'undr_shorts2': {'NAME': 'shorts fino','DESCRIPTION': 'Esse tipo de calça é a sensação do momento!','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},

'undr_pants1': {'NAME': 'calça jeans clara','DESCRIPTION': 'Esse tipo de calça é a sensação do momento!','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},
'undr_pants2': {'NAME': 'calça jeans escura','DESCRIPTION': 'Esse tipo de calça é a sensação do momento!','PRICE': 30,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': '06'},

#VESTS (name,description,price,volume,weight,armor,duration)
'vest1': {'NAME': 'colete amarelo','DESCRIPTION': 'Cuidado pra não pensarem queé um francês manifestante.','PRICE': 30,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 3,'DURATION': 15}},
'vest2': {'NAME': 'colete salva-vidas','DESCRIPTION': 'Mesmo sem água por perto, protege bastante.','PRICE': 60,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 3,'DURATION': 15}},
'vest3': {'NAME': 'colete I','DESCRIPTION': 'Reduz o dano do advesárioDEFESA: 5 DURAÇÃO: 25','PRICE': 120,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 5,'DURATION': 20}},
'vest4': {'NAME': 'colete IIA','DESCRIPTION': 'Reduz o dano do advesárioDEFESA: 8 DURAÇÃO: 25','PRICE': 240,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 8,'DURATION': 25}},
'vest5': {'NAME': 'colete II','DESCRIPTION': 'Reduz o dano do advesárioDEFESA: 10 DURAÇÃO: 30','PRICE': 360,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 10,'DURATION': 30}},
'vest6': {'NAME': 'colete IIIA','DESCRIPTION': 'Reduz o dano do advesárioDEFESA: 12 DURAÇÃO: 35','PRICE': 480,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 12,'DURATION': 35}},
'vest7': {'NAME': 'colete III','DESCRIPTION': 'Restrito apenas parapoliciais de elite.','PRICE': 600,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 16,'DURATION': 40}},
'vest8': {'NAME': 'colete IV','DESCRIPTION': 'Restrito apenas parapoliciais de elite.','PRICE': 720,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'ARMOR': 20,'DURATION': 45}},
 
#CHARMS (name,description,price,volume,weight,armor,duration)
'amulet1': {'NAME': 'cruz','DESCRIPTION': 'Conçede proteção e espanta espíritos.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {5,50}},
'amulet2': {'NAME': 'ankh','DESCRIPTION': 'Conçede proteção e espanta espíritos.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {10,50}},
'amulet3': {'NAME': 'hamsá','DESCRIPTION': 'Conçede força e proteção.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {15,50}},
'amulet4': {'NAME': 'pentáculo','DESCRIPTION': 'Conçede força, proteção e vitalidade.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {20,50}},
'amulet5': {'NAME': 'tríscele','DESCRIPTION': 'Conçede força, proteção e vitalidade','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {25,50}},
'amulet6': {'NAME': 'ouroboros','DESCRIPTION': 'Conçede força, proteção,vitalidade e resistência.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {25,50}},
'amulet7': {'NAME': 'muiraquitã','DESCRIPTION': 'Conçede aumento em todos os atributos.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {25,50}},
 
#AMMO (name,description,price,volume,weight,calibre,metal)
'ammo_stone': {'NAME': 'pedra','DESCRIPTION': 'Isso pode salvar sua vida um dia.','PRICE': 1,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': 0},
'ammo_tranquilizer': {'NAME': 'tranquilizante','DESCRIPTION': 'Munição para pistola que fazo inimigo adormecer.','PRICE': 100,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'arrow_gold': {'NAME': 'flechas de ouro','DESCRIPTION': 'Munição para arco e beste com ponta de ouro.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,1}},
'arrow_silver': {'NAME': 'flechas de prata','DESCRIPTION': 'Munição para arco e beste com ponta de prata.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,2}},
'arrow_copper': {'NAME': 'flechas de cobre','DESCRIPTION': 'Munição para arco e beste com ponta de cobre.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,3}},
'arrow_tin': {'NAME': 'flechas de estanho','DESCRIPTION': 'Munição para arco e beste com ponta de estanho.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,4}},
'arrow_lead': {'NAME': 'flechas de chumbo','DESCRIPTION': 'Munição para arco e beste com ponta de chumbo.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,5}},
'arrow_iron': {'NAME': 'flechas de ferro','DESCRIPTION': 'Munição para arco e beste com ponta de ferro.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,6}},
'arrow_mercury': {'NAME': 'flechas de mercúrio','DESCRIPTION': 'Munição para arco e beste com ponta de mercúrio.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {0,7}},
'ammo.12_gold': {'NAME': 'munição.12 de ouro','DESCRIPTION': 'Balas de ouro de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,1}},
'ammo.12_silver': {'NAME': 'munição.12 de prata','DESCRIPTION': 'Balas de prata de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,2}},
'ammo.12_copper': {'NAME': 'munição.12 de cobre','DESCRIPTION': 'Balas de cobre de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,3}},
'ammo.12_tin': {'NAME': 'munição.12 de estanho','DESCRIPTION': 'Balas de estanho de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,4}},
'ammo.12_lead': {'NAME': 'munição.12 de chumbo','DESCRIPTION': 'Balas de chumbo de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,5}},
'ammo.12_iron': {'NAME': 'munição.12 de ferro','DESCRIPTION': 'Balas de ferro de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,6}},
'ammo.12_mercury': {'NAME': 'munição.12 de mercúrio','DESCRIPTION': 'Balas de mercúrio de calibre 12.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,7}},
'ammo.16_gold': {'NAME': 'munição.16 de ouro','DESCRIPTION': 'Balas de ouro de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,1}},
'ammo.16_silver': {'NAME': 'munição.16 de prata','DESCRIPTION': 'Balas de prata de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,2}},
'ammo.16_copper': {'NAME': 'munição.16 de cobre','DESCRIPTION': 'Balas de cobre de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,3}},
'ammo.16_tin': {'NAME': 'munição.16 de estanho','DESCRIPTION': 'Balas de estanho de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,4}},
'ammo.16_lead': {'NAME': 'munição.16 de chumbo','DESCRIPTION': 'Balas de chumbo de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,5}},
'ammo.16_iron': {'NAME': 'munição.16 de ferro','DESCRIPTION': 'Balas de ferro de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,6}},
'ammo.16_mercury': {'NAME': 'munição.16 de mercúrio','DESCRIPTION': 'Balas de mercúrio de calibre 16.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {16,7}},
'ammo.22_gold': {'NAME': 'munição.22 de ouro','DESCRIPTION': 'Balas de ouro de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,1}},
'ammo.22_silver': {'NAME': 'munição.22 de prata','DESCRIPTION': 'Balas de prata de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,2}},
'ammo.22_copper': {'NAME': 'munição.22 de cobre','DESCRIPTION': 'Balas de cobre de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,3}},
'ammo.22_tin': {'NAME': 'munição.22 de estanho','DESCRIPTION': 'Balas de estanho de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,4}},
'ammo.22_lead': {'NAME': 'munição.22 de chumbo','DESCRIPTION': 'Balas de chumbo de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,5}},
'ammo.22_iron': {'NAME': 'munição.22 de ferro','DESCRIPTION': 'Balas de ferro de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,6}},
'ammo.22_mercury': {'NAME': 'munição.22 de mercúrio','DESCRIPTION': 'Balas de mercúrio de calibre 22.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {22,7}},
'ammo.32_gold': {'NAME': 'munição.32 de ouro','DESCRIPTION': 'Balas de ouro de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,1}},
'ammo.32_silver': {'NAME': 'munição.32 de prata','DESCRIPTION': 'Balas de prata de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,2}},
'ammo.32_copper': {'NAME': 'munição.32 de cobre','DESCRIPTION': 'Balas de cobre de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,3}},
'ammo.32_tin': {'NAME': 'munição.32 de estanho','DESCRIPTION': 'Balas de estanho de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,4}},
'ammo.32_lead': {'NAME': 'munição.32 de chumbo','DESCRIPTION': 'Balas de chumbo de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,5}},
'ammo.32_iron': {'NAME': 'munição.32 de ferro','DESCRIPTION': 'Balas de ouro de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,6}},
'ammo.32_mercury': {'NAME': 'munição.32 de mercúrio','DESCRIPTION': 'Balas de mercúrio de calibre 32.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {32,7}},
'ammo.38_gold': {'NAME': 'munição.38 de ouro','DESCRIPTION': 'Balas de ouro de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,1}},
'ammo.38_silver': {'NAME': 'munição.38 de prata','DESCRIPTION': 'Balas de prata de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,2}},
'ammo.38_copper': {'NAME': 'munição.38 de cobre','DESCRIPTION': 'Balas de cobre de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,3}},
'ammo.38_tin': {'NAME': 'munição.38 de estanho','DESCRIPTION': 'Balas de estanho de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,4}},
'ammo.38_lead': {'NAME': 'munição.38 de chumbo','DESCRIPTION': 'Balas de chumbo de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,5}},
'ammo.38_iron': {'NAME': 'munição.38 de ferro','DESCRIPTION': 'Balas de ferro de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,6}},
'ammo.38_mercury': {'NAME': 'munição.38 de mercúrio','DESCRIPTION': 'Balas de mercúrio de calibre 38.','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {38,7}},
'ammo.42': {'NAME': 'munição.42','DESCRIPTION': '','PRICE': 400,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 42},
'ammo.44': {'NAME': 'munição.44','DESCRIPTION': '','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 44},
'ammo.45': {'NAME': 'munição.45','DESCRIPTION': '','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 45},
'ammo.38mm': {'NAME': 'munição 0.38mm','DESCRIPTION': '','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 380},
'ammo.5.56mm': {'NAME': 'munição 5.56mm','DESCRIPTION': '','PRICE': 200,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 556},
'ammo_missile': {'NAME': 'míssel','DESCRIPTION': '','PRICE': 800,'VOLUME': 5,'WEIGHT': 4,'PROPERTIES': 1000},
 
#TOOLS (name,description,price,volume,weight,{damage,unlock})
'tool_crowbar': {'NAME': 'pé de cabra','DESCRIPTION': 'Use para abrir portas trancadas.','PRICE': 50,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 5, 'UNLOCK': 'metal','RECHARGE': 2,'CADENCY': 50}},
'tool_axe': {'NAME': 'machado','DESCRIPTION': 'Use para quebrar madeira.','PRICE': 50,'VOLUME': 4,'WEIGHT': 4,'PROPERTIES': {'DAMAGE': 5, 'UNLOCK': 'wood','RECHARGE': 2,'CADENCY': 50}},
'tool_hammer': {'NAME': 'martelo','DESCRIPTION': 'Conserta, prega e quebra objetos e cabeças.','PRICE': 30,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 3, 'UNLOCK': 'stone','RECHARGE': 2,'CADENCY': 50}},
'tool_sledgehammer': {'NAME': 'marreta','DESCRIPTION': 'Use para quebrar vidro.','PRICE': 50,'VOLUME': 4,'WEIGHT': 5,'PROPERTIES': {'DAMAGE': 5, 'UNLOCK': 'stone','RECHARGE': 2,'CADENCY': 50}},
'tool_dustpan': {'NAME': 'pá de lixo','DESCRIPTION': 'Cai bem para limpar a sujeira.','PRICE': 10,'VOLUME': 5,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 1,'RECHARGE': 2,'CADENCY': 50}},
'tool_shovel': {'NAME': 'pá','DESCRIPTION': 'Use para cavar o solo para encontrar itens e abrir passagens.','PRICE': 50,'VOLUME': 5,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 5, 'UNLOCK': 'grass','RECHARGE': 2,'CADENCY': 50}},
'tool_chainsaw': {'NAME': 'motoserra','DESCRIPTION': 'Use para cortar árvores grandese de quebra bancar o Jason.','PRICE': 50,'VOLUME': 6,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 5, 'UNLOCK': 'wood','RECHARGE': 2,'CADENCY': 50}},
'tool_lighter1': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter2': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter3': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter4': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter5': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter6': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_lighter7': {'NAME': 'isqueiro','DESCRIPTION': 'Use para acender bombase talvez cigarros, mas não se recomenda.','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_spoon': {'NAME': 'colher','DESCRIPTION': 'Você não come do prato com as mãos, correto?','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_fork': {'NAME': 'garfo','DESCRIPTION': 'Você não come do prato com as mãos, correto?','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_knife': {'NAME': 'faca','DESCRIPTION': 'Você não come do prato com as mãos, correto?','PRICE': 6,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_magnifying_glass': {'NAME': 'lupa','DESCRIPTION': 'Use para observar coisas pequenas.','PRICE': 2,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_handcuffs': {'NAME': 'algemas','DESCRIPTION': 'Use para capturar anomalias e levá-las para pesquisa.','PRICE': 50,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'tool_umbrella': {'NAME': 'guarda-chuva','DESCRIPTION': 'Não pegue resfriado meu filho!','PRICE': 800,'VOLUME': 5,'WEIGHT': 1,'PROPERTIES': {}},
'tool_umbrella_portable': {'NAME': 'guarda-chuva portátil','DESCRIPTION': 'Não pegue resfriado meu filho!Cabe na mochila!','PRICE': 800,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {}},
'tool_can_opener': {'NAME': 'abridor de lata','DESCRIPTION': 'Use para abrir garrafas de vidro e latas em conserva.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_syringe': {'NAME': 'seringa','DESCRIPTION': 'Use para tirar sangue e aplicar antibióticos. Sempre lave antes de usar!','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'tool_asthma_inhaler': {'NAME': 'bombinha','DESCRIPTION': 'Não se esqueça de usar quando sentirfalta de ar.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
   
#MELEE WEAPONS (name,description,price,volume,weight,{damage})
'melee_broom': {'NAME': 'vassoura','DESCRIPTION': 'Não foi feita para se armar, muito menospara caçar ou voar, mas funciona.','PRICE': 10,'VOLUME': 5,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 2,'RECHARGE': 2,'CADENCY': 50}},
'melee_walking_stick': {'NAME': 'bengala','DESCRIPTION': 'Pessoas mais velhas usam isso comoterceira perna, mas pode ser uma boa arma.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}},
'melee_boomerang': {'NAME': 'bumerangue','DESCRIPTION': 'Você sabia que isso era usado para quebrarpescoços de cangurus?','PRICE': 30,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}},
'melee_stick': {'NAME': 'galho','DESCRIPTION': 'No meio do mato, qualquer coisa podevirar uma arma.','PRICE': 1,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}},
'melee_frying_pan': {'NAME': 'frigideira','DESCRIPTION': 'Se não tiver o que usar, ela quebra um galhoe ainda frita um ovo legal.','PRICE': 30,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 4,'RECHARGE': 2,'CADENCY': 50}},
'melee_spanner': {'NAME': 'chave inglesa','DESCRIPTION': 'Pode ser usada para girar porcas, masvocê a usa para espancar.','PRICE': 10,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 5,'RECHARGE': 2,'CADENCY': 50}},
'melee_bottle': {'NAME': 'garrafa de vidro','DESCRIPTION': 'Depois de um drink moderadoé excelente para tacar na cabeça de um nazi.','PRICE': 10,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 6,'RECHARGE': 2,'CADENCY': 50}},
'melee_bar': {'NAME': 'barra de ferro','DESCRIPTION': 'Dá na telha pra descero cacete em alguém.','PRICE': 4,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 8,'RECHARGE': 2,'CADENCY': 50}},
'melee_scissors': {'NAME': 'tesoura','DESCRIPTION': 'Para cortar papel, plástico, panoe tecido muscular.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 2,'RECHARGE': 2,'CADENCY': 50}},
'melee_stiletto': {'NAME': 'estilete','DESCRIPTION': 'Útil para ataques corpo-a-corpo, pode ser tão letalquanto uma arma de fogo.','PRICE': 20,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 5,'RECHARGE': 2,'CADENCY': 50}},
'melee_knife': {'NAME': 'faca','DESCRIPTION': 'Útil para ataques corpo-a-corpo, pode ser tão letalquanto uma arma de fogo.','PRICE': 300,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 10,'RECHARGE': 2,'CADENCY': 50}},
'melee_scalpel': {'NAME': 'bisturi','DESCRIPTION': 'Altamente letal e perfurante, mas obviamenteele só é utilizado em prol da medicina, certo?.','PRICE': 800,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 20,'RECHARGE': 2,'CADENCY': 50}},
'melee_fishmonger': {'NAME': 'peixeira','DESCRIPTION': 'Útil para ataques corpo-a-corpo, pode ser tão letalquanto uma arma de fogo.','PRICE': 500,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 13,'RECHARGE': 2,'CADENCY': 50}},
'melee_cleaver': {'NAME': 'cutelo','DESCRIPTION': 'Foi feita para cortar ossos de carnes, masserve como uma boa arma também.','PRICE': 700,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 16,'RECHARGE': 2,'CADENCY': 50}},
'melee_katana': {'NAME': 'katana','DESCRIPTION': 'Útil para ataques corpo-a-corpo, pode ser tão letalquanto uma arma de fogo.','PRICE': 1000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 18,'RECHARGE': 2,'CADENCY': 50}},
'melee_whip': {'NAME': 'chicote','DESCRIPTION': 'Útil para ataques corpo-a-corpo, pode ser tão letalquanto uma arma de fogo.','PRICE': 500,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 14,'RECHARGE': 2,'CADENCY': 50}},
'melee_taser': {'NAME': 'taser','DESCRIPTION': 'Porque um verdadeiro meliantenão mata, causa dor.','PRICE': 1500,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 8,'RECHARGE': 2,'CADENCY': 50}},
'melee_cursedknife': {'NAME': 'faca amaldiçoada','DESCRIPTION': 'Uma faca com uma terrível maldiçãode transformar tudo o que corta em bolo.','PRICE': 300,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 10,'RECHARGE': 2,'CADENCY': 50}},

#WEAPONS (name,description,price,volume,weight,{damage,recharge,cadency,capacity,gauge})
'gun_bow': {'NAME': 'arco','DESCRIPTION': 'Uma arma de longa distância e velha moda.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 5, 'GAUGE': 0}},
'gun_crossbow': {'NAME': 'besta','DESCRIPTION': 'Uma arma de longa distância e velha moda.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 5, 'GAUGE': 0}},
'gun_revolver.12': {'NAME': 'revólver.12','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição decalibre 12.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 12}},
'gun_revolver.16': {'NAME': 'revólver.16','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição decalibre 16.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 16}},
'gun_revolver.22': {'NAME': 'revólver.22','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição decalibre 22.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 22}},
'gun_revolver.32': {'NAME': 'revólver.32','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição decalibre 32.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 32}},
'gun_revolver.38': {'NAME': 'revólver.38','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição decalibre 38.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}},
  
'gun_pistol': {'NAME': 'pistola','DESCRIPTION': 'Arma de fogo para ataques de média distância, ela usa munição de calibre 38.','PRICE': 2500,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 3, 'CAPACITY': 16}},
  
'gun_UZI.22': {'NAME': 'Uzi .22','DESCRIPTION': 'Arma de fogo para ataques de média distância.','PRICE': 4000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 4, 'RECHARGE': 1, 'CADENCY': 20, 'CAPACITY': 10, 'GAUGE': 22}},
'gun_UZI.45': {'NAME': 'Uzi .45','DESCRIPTION': 'Arma de fogo para ataques de média distância.','PRICE': 4000,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {'DAMAGE': 4, 'RECHARGE': 8, 'CADENCY': 1, 'CAPACITY': 16, 'GAUGE': 45}},
  
'gun_shotgun.12': {'NAME': 'espingarda .12','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição de calibre 12.','PRICE': 5000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 5, 'RECHARGE': 4, 'CADENCY': 4, 'CAPACITY': 6, 'GAUGE': 12}},
'gun_carbine': {'NAME': 'carabina','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 5000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 8, 'CAPACITY': 3, 'GAUGE': 16}},
  
'gun_sniper': {'NAME': 'sniper','DESCRIPTION': 'Arma de fogo para ataques de curta distância,ela usa munição de calibre 16.','PRICE': 6000,'VOLUME': 5,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}},
'gun_shotgun': {'NAME': 'escopeta','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 4000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}},
  
'gun_assault_riffle': {'NAME': 'fuzil de assalto','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 4000,'VOLUME': 5,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}},
'gun_rifle': {'NAME': 'fuzil','DESCRIPTION': 'Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 5000,'VOLUME': 5,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 16, 'GAUGE': 16}},
'gun_AK-47': {'NAME': 'AK-47','DESCRIPTION': 'Fuzil para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 5000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 20, 'GAUGE': 39.0}},
'gun_M16': {'NAME': 'M16','DESCRIPTION': 'Fuzil para ataques de curta distância, ela usa munição de calibre 16.','PRICE': 5000,'VOLUME': 4,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 6, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 30, 'GAUGE': 5.56}},
  
'gun_RPG-7': {'NAME': 'RPG-7','DESCRIPTION': 'Bazuca utilizada contra tanques.','PRICE': 12000,'VOLUME': 7,'WEIGHT': 5,'PROPERTIES': {'DAMAGE': 50, 'RECHARGE': 10, 'CADENCY': 0, 'CAPACITY': 1, 'GAUGE': 0}},
   
#GRENADES (name,description,price,volume,weight,{damage,type})
'grenade': {'NAME': 'granada','DESCRIPTION': 'Use numa batalha para causar dano á todos os inimigos na tela.','PRICE': 100,'VOLUME': 2,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 30,'TYPE': 1}},
'grenade_smoke': {'NAME': 'granada de fumaça','DESCRIPTION': 'Use numa batalha para que todos os inimigos percam AGILIDADE.','PRICE': 200,'VOLUME': 2,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 13,'TYPE': 2}},
'grenade_flash': {'NAME': 'granada de luz','DESCRIPTION': 'Use numa batalha para que todos os inimigos percam sua vez.','PRICE': 500,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': {'DAMAGE': 15,'TYPE': 3}},
'grenade_molotov_cocktail': {'NAME': 'coquetel molotov','DESCRIPTION': 'Use numa batalha para causar dano á todos os inimigose possivelmente queimá-los.','PRICE': 40,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {'DAMAGE': 12,'TYPE': 1}},

#BATTLE (name,description,price,volume,weight,{damage,type})
'pepper_spray': {'NAME': 'spray de pimenta','DESCRIPTION': 'Use numa batalha para atordoar um inimigo.','PRICE': 40,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {}},
'horn': {'NAME': 'buzina','DESCRIPTION': 'Use numa batalha para atordoar um inimigo.','PRICE': 40,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {}},
'extinguisher': {'NAME': 'extintor','DESCRIPTION': 'Use num caso de emergência.... até pra jogar num bulldogue.','PRICE': 40,'VOLUME': 4,'WEIGHT': 30,'PROPERTIES': {}},
'rope': {'NAME': 'corda','DESCRIPTION': 'Use em batalhas para prender seus oponentesou dentro de cavernas para descer e subir','PRICE': 70,'VOLUME': 4,'WEIGHT': 1,'PROPERTIES': {}},

#DRUGS (name,description,price,volume,weight,condition)
'drug_antibiotic': {'NAME': 'antibiótico','DESCRIPTION': 'Use para infeccionar feridas letais e impedir hemorragias, parando de consumir a barra de HP.','PRICE': 25,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_syrup': {'NAME': 'xarope','DESCRIPTION': 'Remédio utilizado para combater resfriados e alergias.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_tablets': {'NAME': 'comprimidos','DESCRIPTION': 'Remédios utilizados para combater náusea.','PRICE': 30,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'drug_pills': {'NAME': 'pílulas','DESCRIPTION': 'Remédios utilizados para combater dor muscular.','PRICE': 40,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'drug_paracetamol': {'NAME': 'paracetamol','DESCRIPTION': 'Medicamento para combater a febre.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_desloratadin': {'NAME': 'desloratadina','DESCRIPTION': 'Medicamento para combater a tontura.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_pseudoefedrin': {'NAME': 'pseudoefedrina','DESCRIPTION': 'Medicamento para combater o resfriado.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_ibuprofen': {'NAME': 'ibuprofeno','DESCRIPTION': 'Medicamento para combater o resfriado e a febre.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'drug_ciprofloxacin': {'NAME': 'ciprofloxacino','DESCRIPTION': 'Antibiótico útil contra conjutivite,resfriado e febre.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
   
'serum_antiscorpionic': {'NAME': 'soro antiescorpiônico','DESCRIPTION': 'Antídoto para combater veneno de escorpiões.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'serum_antivenom': {'NAME': 'soro antiofídico','DESCRIPTION': 'Antídoto para combater veneno de cobras.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'serum_antiarachnid': {'NAME': 'soro antiaracnídico','DESCRIPTION': 'Antídoto para combater veneno de aranhas.','PRICE': 40,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
 
'drug_adrenaline': {'NAME': 'adrenalina','DESCRIPTION': 'Remédio utilizado para reviver uma pessoa inconsciente.','PRICE': 60,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'cigar': {'NAME': 'maço de cigarro','DESCRIPTION': 'Use isso pra arregaçar seu sistema respiratório.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},

#CONDIMENTS (name,description,price,volume,weight,type,duration)
'condiment_ketchup': {'NAME': 'ketchup','DESCRIPTION': 'Condimento muito usado em salgados.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {0,'0100'}},
'condiment_mayonnaise': {'NAME': 'maionese','DESCRIPTION': 'Condimento muito usado em salgados.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {0,'0100'}},
'condiment_sugar': {'NAME': 'açúcar','DESCRIPTION': 'Condimento muito usado em doces.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {1,'0100'}},
'condiment_sweetener': {'NAME': 'adoçante','DESCRIPTION': 'Condimento muito usado em doces.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {1,'0100'}},
'condiment_salt': {'NAME': 'sal','DESCRIPTION': 'Condimento muito usado em refeições.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,'0100'}},
'condiment_pepper': {'NAME': 'pimenta','DESCRIPTION': 'Condimento muito usado em refeições.','PRICE': 5,'VOLUME': 1,'WEIGHT': 2,'PROPERTIES': {6,'0100'}},
'condiment_olive_oil': {'NAME': 'azeite','DESCRIPTION': 'Condimento muito usado em refeições.','PRICE': 5,'VOLUME': 1,'WEIGHT': 2,'PROPERTIES': {6,'0100'}},
'condiment_vinegar': {'NAME': 'vinagre','DESCRIPTION': 'Condimento muito usado em refeições.','PRICE': 5,'VOLUME': 1,'WEIGHT': 2,'PROPERTIES': {6,'0100'}},
'condiment_oregan': {'NAME': 'orégano','DESCRIPTION': 'Condimento muito usado em salgados.','PRICE': 5,'VOLUME': 1,'WEIGHT': 0,'PROPERTIES': {6,'0100'}},
'condiment_shoyu': {'NAME': 'shoyu','DESCRIPTION': 'Condimento muito usado em refeições.','PRICE': 5,'VOLUME': 1,'WEIGHT': 2,'PROPERTIES': {6,'0100'}},

#DRINK (name,description,price,volume,weight,health,thirst,duration,trash)
'drink_water': {'NAME': 'água','DESCRIPTION': 'O básico pra te manter de péno calor e no cansaço. BEBA ÁGUA!','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {10,10,'0100','plastic_bottle'}},
'drink_water_gas': {'NAME': 'água com gás','DESCRIPTION': 'Certas pessoas preferem beber águadesse jeito.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {10,10,'0100','plastic_bottle'}},
'drink_juice_orange': {'NAME': 'suco de laranja','DESCRIPTION': 'Saudável e nutritivo, o Jailson aprova.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {12,10,'0100','box'}},
'drink_juice_passion_fruit': {'NAME': 'suco de maracujá','DESCRIPTION': 'Saudável e nutritivo, acalma a alma e o espírito.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {12,10,'0100','box'}},
'drink_coffee': {'NAME': 'café','DESCRIPTION': 'Bebida que aumenta a sua energia.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {8,10,'0100','cup'}},
'drink_chocolate': {'NAME': 'chocolate quente','DESCRIPTION': 'Vai bem com biscoitos','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {6,10,'0100','cup'}},
'drink_milk': {'NAME': 'leite','DESCRIPTION': 'Vai bem no café.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {6,10,'0100','box'}},
'drink_coffeenmilk': {'NAME': 'café com leite','DESCRIPTION': 'Bebida preferida do criadordo jogo, foi muito útil.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {10,10,'0100','cup'}},
'drink_energy': {'NAME': 'energético','DESCRIPTION': 'Bebida que acelera o metabolismoe aumenta a energia.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {10,10,'0100','can'}},
'drink_cola': {'NAME': 'refri','DESCRIPTION': 'A bomba calórica que a gente gosta.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {5,10,'0100','can'}},
'drink_guarana': {'NAME': 'guaraná','DESCRIPTION': 'Um suquinho barato e muito açúcaradomas é bom, não confundir com cachos de olhos.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {5,10,'0100','can'}},
'drink_beer': {'NAME': 'cerveja','DESCRIPTION': 'Bebida alcóolica para aumentar a energiaPelo amor de deus COM MODERAÇÃO.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {8,10,'0100','bottle'}},
'drink_whiskey': {'NAME': 'uísque','DESCRIPTION': 'Bebida alcóolica para aumentar a energiaPelo amor de deus COM MODERAÇÃO.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {8,10,'0100','bottle'}},
'drink_yogurt': {'NAME': 'iogurte','DESCRIPTION': 'Delicioso e saudável.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {8,10,'0100','cup'}},

#WASTED DRINK (name,description,price,volume,weight,health,thirst,duration)
'drink_water_wasted': {'NAME': 'água quente','DESCRIPTION': 'O básico pra te manter de péno calor e no cansaço. BEBA ÁGUA!','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {10,10,'0100'}},
'drink_water_gas_wasted': {'NAME': 'água com gás quente','DESCRIPTION': 'Certas pessoas preferem beber águadesse jeito.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {10,10,'0100'}},
'drink_juice_orange_wasted': {'NAME': 'suco de laranja quente','DESCRIPTION': 'Saudável e nutritivo, o Jailson aprova.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {12,10,'0100'}},
'drink_juice_passion_fruit_wasted': {'NAME': 'suco de maracujá quente','DESCRIPTION': 'Saudável e nutritivo, acalma a alma e o espírito.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {12,10,'0100'}},
'drink_coffee_wasted': {'NAME': 'café frio','DESCRIPTION': 'Bebida que aumenta a sua energia.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {8,10,'0100'}},
'drink_chocolate_wasted': {'NAME': 'chocolate frio','DESCRIPTION': 'Vai bem com biscoitos','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {6,10,'0100'}},
'drink_milk_wasted': {'NAME': 'leite','DESCRIPTION': 'Vai bem no café.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {6,10,'0100'}},
'drink_coffeenmilk_wasted': {'NAME': 'café com leite frio','DESCRIPTION': 'Bebida preferida do criadordo jogo, foi muito útil.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {10,10,'0100'}},
'drink_energy_wasted': {'NAME': 'energético quente','DESCRIPTION': 'Bebida que acelera o metabolismoe aumenta a energia.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {10,10,'0100'}},
'drink_cola_wasted': {'NAME': 'refri sem gás','DESCRIPTION': 'A bomba calórica que a gente gosta.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {5,10,'0100'}},
'drink_guarana_wasted': {'NAME': 'guaraná sem gás','DESCRIPTION': 'Um suquinho barato e muito açúcaradomas é bom, não confundir com cachos de olhos.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {5,10,'0100'}},
'drink_beer_wasted': {'NAME': 'cerveja quente','DESCRIPTION': 'Bebida alcóolica para aumentar a energiaPelo amor de deus COM MODERAÇÃO.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {8,10,'0100'}},
'drink_whiskey_wasted': {'NAME': 'uísque quente','DESCRIPTION': 'Bebida alcóolica para aumentar a energiaPelo amor de deus COM MODERAÇÃO.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {8,10,'0100'}},
'drink_yogurt_wasted': {'NAME': 'iogurte estragado','DESCRIPTION': 'Delicioso e saudável.','PRICE': 8,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {8,10,'0100'}},
 
#FOOD (name,description,price,volume,weight,health,hunger,duration,trash)
'food_burger': {'NAME': 'hamburguer','DESCRIPTION': 'É bom quando está passeando e quertomar alguma coisa.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_hotdog': {'NAME': 'cachorro quente','DESCRIPTION': 'Hot dog sua bunda.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_popcorn': {'NAME': 'pipoca','DESCRIPTION': 'Você falou em pipoca?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_popcorn_candy': {'NAME': 'pipoca doce','DESCRIPTION': 'Você falou em pipoca?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_churros': {'NAME': 'churros','DESCRIPTION': 'Churros, olha o churros.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_ice_cream_chocolate': {'NAME': 'sorvete de chocolate','DESCRIPTION': 'É bom quando está passeando e quertomar alguma coisa.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_ice_cream_vanilla': {'NAME': 'sorvete de baunilha','DESCRIPTION': 'É bom quando está passeando e quertomar alguma coisa.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_ice_cream_mixed': {'NAME': 'sorvete misto','DESCRIPTION': 'É bom quando está passeando e quertomar alguma coisa.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_orange': {'NAME': 'laranja','DESCRIPTION': 'Fruta fácil de se acharnum pomar.','PRICE': 3,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,10,'0100',None}},
'food_fish': {'NAME': 'pirarucu','DESCRIPTION': 'Peixe de água doce.','PRICE': 3,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,10,'0100',None}},
'food_bread': {'NAME': 'pão','DESCRIPTION': 'O alimento matinal de cada dia.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_pedemoleque': {'NAME': 'pé de moleque','DESCRIPTION': 'Doce de amendoim, fácil de encontrar em padarias.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,10,'0100','packing'}},
'food_peanut_candy': {'NAME': 'paçoca','DESCRIPTION': 'Doce de amendoim, fácil de encontrar em padarias.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,10,'0100','packing'}},
'food_coconut_candy': {'NAME': 'cocada','DESCRIPTION': 'Doce de côco, fácil de encontrar em padadias.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {2,10,'0100','packing'}},
'food_coxinha': {'NAME': 'coxinha','DESCRIPTION': 'Salgado feito com massa frita e recheada com frango, fácil deencontrar em lanchonetes.','PRICE': 5,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {8,10,'0100',None}},
'food_pastry': {'NAME': 'pastel','DESCRIPTION': 'Salgado feito com massa frita e recheado com queijo.','PRICE': 3,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {5,10,'0100',None}},
'food_puff_pastry': {'NAME': 'pastel folheado','DESCRIPTION': 'Salgado feito com várias camadas de massa e queijo.','PRICE': 6,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {12,10,'0100',None}},
'food_brigadeiro': {'NAME': 'brigadeiro','DESCRIPTION': 'Doce de chocolate.','PRICE': 2,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {3,10,'0100',None}},
'food_cheese_bread': {'NAME': 'pão de queijo','DESCRIPTION': 'Salgado feito com massa de queijo.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {7,10,'0100',None}},
'food_pudding': {'NAME': 'pudim','DESCRIPTION': 'Doce feito com leite condensado.','PRICE': 10,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {15,10,'0300',None}},
'food_cake_corn': {'NAME': 'bolo de fubá','DESCRIPTION': 'Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.','PRICE': 12,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {18,10,'0500',None}},
'food_cake_carrot': {'NAME': 'bolo de cenoura','DESCRIPTION': 'Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.','PRICE': 12,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {18,10,'0500',None}},
'food_cake_chocolate': {'NAME': 'bolo de chocolate','DESCRIPTION': 'Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.','PRICE': 12,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {18,10,'0500',None}},
'food_packed_lunch': {'NAME': 'marmita','DESCRIPTION': 'Tem muitas coisas diferentes dentro, além de ser bem nutritivo!','PRICE': 15,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_egg': {'NAME': 'ovo','DESCRIPTION': 'Ele te deixa forte pra enfrentar qualquer perigo.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300',None}},
'food_lamen_chicken': {'NAME': 'miojo de galinha','DESCRIPTION': 'O macarrão instantâneodo cara que mora sozinho.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','packing'}},
'food_lamen_meat': {'NAME': 'miojo de carne','DESCRIPTION': 'O macarrão instantâneodo cara que mora sozinho.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','packing'}},
'food_cookie_chocolate': {'NAME': 'bolacha de chocolate','DESCRIPTION': 'Biscoito recheado semprefoi chamado assim.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','cookie_packing'}},
'food_cookie_strawberry': {'NAME': 'bolacha de morango','DESCRIPTION': 'Biscoito recheado semprefoi chamado assim.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','cookie_packing'}},
'food_snack_onion': {'NAME': 'salgadinho de cebola','DESCRIPTION': '50% do saco é de puro vento.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','snack_packing'}},
'food_snack_cheese': {'NAME': 'salgadinho de queijo','DESCRIPTION': '50% do saco é de puro vento.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','snack_packing'}},
'food_snack_creammycheese': {'NAME': 'salgadinho de requeijão','DESCRIPTION': '50% do saco é de puro vento.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','snack_packing'}},
'food_pizza_mussarella': {'NAME': 'pizza de mussarela','DESCRIPTION': 'Quem não gosta de pizza?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','pizza'}},
'food_pizza_shaggy': {'NAME': 'pizza de calabresa','DESCRIPTION': 'Quem não gosta de pizza?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','pizza'}},
'food_pizza_chicken': {'NAME': 'pizza de frango','DESCRIPTION': 'Quem não gosta de pizza?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','pizza'}},
'food_pizza_4cheese': {'NAME': 'pizza de 4 queijos','DESCRIPTION': 'Quem não gosta de pizza?','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10,'0300','pizza'}},
'food_soup': {'NAME': 'sopa','DESCRIPTION': 'Nutritivo e quentinho, pode ser feiti dequalquer coisa.','PRICE': 10,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {40,15,'0300',None}},
'food_soup_monkey': {'NAME': 'sopa de macaco','DESCRIPTION': 'Sopa de macaco.','PRICE': 10,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {40,15,'0300',None}},

#WASTED FOOD (name,description,price,volume,weight,health)
'food_coxinha_wasted': {'NAME': 'coxinha fria','DESCRIPTION': 'Não é mais tão gostosa quanto antes,mas é comestível.','PRICE': 2,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {4,10}},
'food_peanut_candy_wasted': {'NAME': 'paçoca esfarelada','DESCRIPTION': 'O que antes era um doce maravilhosoagora são apenas migalhas...','PRICE': 2,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {1,10}},
'food_egg_wasted': {'NAME': 'ovo podre','DESCRIPTION': 'ALGUÉM DESTRUIU O MEU OVO','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {30,10}},
'food_pizza_chicken_wasted': {'NAME': 'pizza de frango fria','DESCRIPTION': 'Tá gelada e sem gosto.','PRICE': 15,'VOLUME': 2,'WEIGHT': 2,'PROPERTIES': {10,3,'pizza'}},

#INGREDIENTS (name,description,price,volume,weight)
'ingredient_ectoplasm': {'NAME': 'ectoplasma','DESCRIPTION': 'Uma estranha gosma branca, comum eminvocações de espíritos.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_eyefeather': {'NAME': 'pena ocular','DESCRIPTION': 'Uma pena de pavão com umolho laranja na ponta.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_sickle_beak': {'NAME': 'bico de foice','DESCRIPTION': 'Um bico com formato defoice, pode ser usado como arma.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_hammer_beak': {'NAME': 'bico de martelo','DESCRIPTION': 'Um bico com formato demartelo, pode ser usado como arma.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_eye': {'NAME': 'olho','DESCRIPTION': 'Um glóbulo ocular.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_crab_claw': {'NAME': 'garra de caranguejo','DESCRIPTION': 'Um garra de caranguejo pontuda e afiada.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'ingredient_ox_horn': {'NAME': 'Chifre de boi','DESCRIPTION': 'Um material resistente e duro como osso.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},

#UTENSILS (name,description,price,volume,weight)
'utn_cup': {'NAME': 'prato','DESCRIPTION': 'Objeto arremessável.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'utn_plate': {'NAME': 'prato','DESCRIPTION': 'Objeto arremessável.','PRICE': 1,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
 
#TRASH (name,description,price,volume,weight)
'trash_packing': {'NAME': 'embalagem','DESCRIPTION': 'Um papel que não serve pra absolutamente nadaa menos que seja uma esponja amarela.','PRICE': 8,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'trash_cookie_packing': {'NAME': 'embalagem de biscoito','DESCRIPTION': 'Um papel que não serve pra absolutamente nadaa menos que seja uma esponja amarela.','PRICE': 8,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'trash_snack_packing': {'NAME': 'embalagem de salgadinho','DESCRIPTION': 'Um papel que não serve pra absolutamente nadaa menos que seja uma esponja amarela.','PRICE': 8,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'trash_bottle': {'NAME': 'garrafa de vidro','DESCRIPTION': 'Um item meio perigoso de se levar nas suas costas,sabe-se lá o que pode fazer com isso','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'trash_plastic_bottle': {'NAME': 'garrafa plástica','DESCRIPTION': 'Se você não jogar no lixo, nãofaz idéia do dano que vai fazer.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'trash_can': {'NAME': 'latinha','DESCRIPTION': 'Um latinha que poderia ser usadapara brincar de bola.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'trash_pizza': {'NAME': 'caixa de pizza','DESCRIPTION': 'Uma caixa que um dia tinha uma coisamuito gostosa dentro.','PRICE': 8,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'trash_box': {'NAME': 'caixa','DESCRIPTION': 'Ás vezes é o que você mais precisapra um trabalho escolar.','PRICE': 8,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'trash_cup': {'NAME': 'copo descartável','DESCRIPTION': 'Quem nunca ficou cortando as tirascomo uma água viva.','PRICE': 8,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
   
#KEY ITEMS (name,description,price,volume,weight)
'key': {'NAME': 'chave','DESCRIPTION': 'Use para abrir portas pelo labirinto!.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_bedroom': {'NAME': 'chave do quarto','DESCRIPTION': 'Se perder vai ficar sem caminha.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_chest': {'NAME': 'chave de baú','DESCRIPTION': 'Use para abrir um compartimento.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_vehicle': {'NAME': 'chave do veículo','DESCRIPTION': 'É o que põe o motor pra funcionar.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_park': {'NAME': 'chave do parque','DESCRIPTION': 'Ela serve pra entrar no parque nacionalonde você achou é outra história.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_lab': {'NAME': 'chave do laboratório','DESCRIPTION': 'Que honra ter as chaves do laboratório Fiocruz!','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_office': {'NAME': 'chave do escritório','DESCRIPTION': 'Um homem simpático que deuele quer mesmo é ver o circo pegar fogo.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'key_cave': {'NAME': 'signo de mercúrio','DESCRIPTION': 'Uma placa de ferro com a inscriçãode mercúrio... estranho','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'dungeon_key': {'NAME': 'chave','DESCRIPTION': 'Use dentro de instalações para abrir caminhos.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
   
#DOCUMENTS (name,description,price,volume,weight)
'id_card0': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'id_card1': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 1},
'id_card2': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'id_card3': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},
'id_card4': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 4},
'id_card5': {'NAME': 'identidade','DESCRIPTION': 'Mostra suas informações básicas e prova sua autoridade acimados civis.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 5},
'newspaper': {'NAME': 'jornal semanal','DESCRIPTION': 'Para receber as notícias da semana.','PRICE': 5,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},

#DEVICES (name,description,price,volume,weight,GUI)
'phone': {'NAME': 'celular','DESCRIPTION': 'Mais importante que o cartão só o celular, pode ser usado para fazerchamadas e receber emails, mas lembre-se de recarregar.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'phone_lantern': {'NAME': 'celular com lanterna','DESCRIPTION': 'Além de tudo o que um celular faz,você pode usá-lo para enxergar no escuro.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'PDA': {'NAME': 'PDA','DESCRIPTION': 'Com este dispositivo, você pode fazer coisasalém do celular, como acessar a internet.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 1},
'charger': {'NAME': 'carregador','DESCRIPTION': 'Use para carregar seu celular.','PRICE': 40,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'portable_charger': {'NAME': 'carregador portátil','DESCRIPTION': 'Use para carregar seu celular.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'headphone_cheap': {'NAME': 'fone de ouvido barato','DESCRIPTION': 'Ao obter um, você consegue escutar o rádio do celular, mas atenção! ele quebra nos momentos mais inesperados.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'headphone_expensive': {'NAME': 'fone de ouvido caro','DESCRIPTION': 'Ao obter um, você consegue escutar o rádio do celular. Bem mais resistente que fones de ouvido baratos.','PRICE': 60,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'simcard1': {'NAME': 'cartão SIM IO','DESCRIPTION': 'Insira dentro de um celular parafazer chamadas e acessar a internet.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'simcard2': {'NAME': 'cartão SIM MIMO','DESCRIPTION': 'Insira dentro de um celular parafazer chamadas e acessar a internet.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'simcard3': {'NAME': 'cartão SIM SIM','DESCRIPTION': 'Insira dentro de um celular parafazer chamadas e acessar a internet.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'simcard4': {'NAME': 'cartão SIM FALO','DESCRIPTION': 'Insira dentro de um celular parafazer chamadas e acessar a internet.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'sdcard': {'NAME': 'cartão SD','DESCRIPTION': 'Para guardar músicas salvas.','PRICE': 60,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'GPS': {'NAME': 'GPS','DESCRIPTION': 'Este dispositivo super tecnológico serve paraapontar sua localização e mostrar o mapa da região.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'camera': {'NAME': 'camera digital','DESCRIPTION': 'Serve para tirar fotos e guardar de recordação.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'mp3': {'NAME': 'tocador mp3','DESCRIPTION': 'Útil para escutar rádio e música.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'brickgame': {'NAME': 'brick game','DESCRIPTION': 'Não faz mal se descontrair com 99 jogos.','PRICE': 20,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'flashlight': {'NAME': 'lanterna','DESCRIPTION': 'Use para enxergar no escuro.','PRICE': 60,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'nightvision': {'NAME': 'visão noturna','DESCRIPTION': 'Use para enxergar no escuro.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'binoculars': {'NAME': 'binóculos','DESCRIPTION': 'Use para enxergar mais além.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'sonar': {'NAME': 'sonar','DESCRIPTION': 'Use para detectar a presença de anomalias.','PRICE': 500,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {}},
'batteries': {'NAME': 'pilhas','DESCRIPTION': 'A fonte de energia de vários aparelhos eletrônicos.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},

#GAMING (name,description,price,volume,weight,GUI)
'playingcards': {'NAME': 'cartas de baralho','DESCRIPTION': 'Use para jogar vários jogos de baralho.','PRICE': 10,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'dominoes': {'NAME': 'dominó','DESCRIPTION': 'Pode usar tanto pra montar castelinhos e trilhasquanto pra jogar com os amigos.','PRICE': 10,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 0},
'chess_board': {'NAME': 'tabuleiro de xadrez','DESCRIPTION': 'Use para jogar o jogo das pessoas de estratégia.','PRICE': 50,'VOLUME': 3,'WEIGHT': 2,'PROPERTIES': 0},
'ouija_board': {'NAME': 'tabuleiro ouija','DESCRIPTION': 'Um instrumento sério de contatação espiritualque virou brinquedo graças ao capitalismo.','PRICE': 50,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': 0},

#INSTRUMENTS (name,description,price,volume,weight,{type})
'instrument_acousticguitar': {'NAME': 'violão acústico','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 300,'VOLUME': 7,'WEIGHT': 3,'PROPERTIES': {'TYPE': 0}},
'instrument_electricguitar': {'NAME': 'guitarra elétrica','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 300,'VOLUME': 7,'WEIGHT': 4,'PROPERTIES': {'TYPE': 1}},
'instrument_bassguitar': {'NAME': 'baixo','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 300,'VOLUME': 7,'WEIGHT': 4,'PROPERTIES': {'TYPE': 2}},
'instrument_flute': {'NAME': 'flauta','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {'TYPE': 3}},
'instrument_ocarina': {'NAME': 'ocarina','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'TYPE': 4}},
'instrument_harmonica': {'NAME': 'gaita','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'TYPE': 5}},
'instrument_tambourine': {'NAME': 'tamborim','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'TYPE': 6}},
'instrument_bongo': {'NAME': 'bongô','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'TYPE': 7}},
'instrument_maracas': {'NAME': 'maracas','DESCRIPTION': 'Um belo instrumento musical.','PRICE': 50,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {'TYPE': 8}},

#PILLS (name,description,price,volume,weight,type)
'pill_strenght': {'NAME': 'suplemento de força','DESCRIPTION': 'Aumenta a FORÇA permanentemente em +10.','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
'pill_agility': {'NAME': 'suplemento de agilidade','DESCRIPTION': 'Aumenta a AGILIDADE permanentemente em +10.','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 1},
'pill_resistance': {'NAME': 'suplemento de resistência','DESCRIPTION': 'Aumenta a RESISTÊNCIA permanentemente em +10.','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'pill_knowledge': {'NAME': 'suplemento de sabedoria','DESCRIPTION': 'Aumenta a SABEDORIApermanentemente em +10.','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},
'pill_charisma': {'NAME': 'suplemento de carisma','DESCRIPTION': 'Aumenta o CARISMA em +10','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 4},
'pill_mistery': {'NAME': 'suplemento misterioso','DESCRIPTION': 'Aumenta um atributo aleatório','PRICE': 500,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 5},

#REPELLENTS (name,description,price,volume,weight,duration)
'repellent1': {'NAME': 'repelente básico','DESCRIPTION': 'Evita anomalias de aparecer por 10 minutos.','PRICE': 50,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 600},
'repellent2': {'NAME': 'super repelente','DESCRIPTION': 'Evita anomalias de aparecer por 30 minutos.','PRICE': 100,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1800},
'repellent3': {'NAME': 'ultra repelente','DESCRIPTION': 'Evita anomalias de aparecer por 60 minutos.','PRICE': 250,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 3600},

#ACESSORIES (name,description,price,volume,weight,type)
'aim1': {'NAME': 'mira 1','DESCRIPTION': 'Customiza a mira de sua arma.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 1},
'aim2': {'NAME': 'mira 2','DESCRIPTION': 'Customiza a mira de sua arma.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'aim3': {'NAME': 'mira 3','DESCRIPTION': 'Customiza a mira de sua arma.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},
'aim4': {'NAME': 'mira 4','DESCRIPTION': 'Customiza a mira de sua arma.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 4},
'aim5': {'NAME': 'mira 5','DESCRIPTION': 'Customiza a mira de sua arma.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 5},
 
'acc_silencer': {'NAME': 'silenciador','DESCRIPTION': 'Aumenta o ATAQUE de uma pistola.','PRICE': 200,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 1},
'acc_cartridge': {'NAME': 'cartucho extra','DESCRIPTION': 'Aumenta a capacidade da arma.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 2},
'acc_gun_butt': {'NAME': 'coronha','DESCRIPTION': 'Aumenta a AGILIDADE da arma.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},
'acc_bandolier': {'NAME': 'bandoleira','DESCRIPTION': 'Adiciona um espaço extra no inventário.','PRICE': 100,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 3},

#CRAFTING (name,description,price,volume,weight)
'craft_spring_small': ['mola pequena','',0,1,1],
'craft_fuel': ['combustível','',0,1,1],
'craft_cloth': ['pano','',0,1,1],
'craft_powder': ['pólvora','',0,1,1],

#CAMPING (name,description,price,volume,weight,amount,sleep)
'air_pump': {'NAME': 'bomba de ar','DESCRIPTION': 'Para encher um colchão inflável.','PRICE': 30,'VOLUME': 3,'WEIGHT': 1,'PROPERTIES': {}},
'bed_single': {'NAME': 'colchão inflável de solteiro','DESCRIPTION': 'Caso precise passar a noite na mata.','PRICE': 50,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {1,2}},
'bed_couple': {'NAME': 'colchão inflável de casal','DESCRIPTION': 'Caso precise passar a noite na mata.','PRICE': 70,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {2,2}},
'tent_small': {'NAME': 'barraca pequena','DESCRIPTION': 'Caso precise passar a noite na mata.','PRICE': 100,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {1,3}},
'tent_medium': {'NAME': 'barraca média','DESCRIPTION': 'Caso precise passar a noite na mata.','PRICE': 100,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {2,3}},
'tent_big': {'NAME': 'barraca grande','DESCRIPTION': 'Caso precise passar a noite na mata.','PRICE': 100,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': {3,3}},

#TRAPS (name,description,price,volume,weight,size)
'cage_small': {'NAME': 'gaiola pequena','DESCRIPTION': 'Para capturar anomalias de pequeno porte.','PRICE': 50,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 1},
'cage_big': {'NAME': 'gaiola grande','DESCRIPTION': 'Para capturar anomalias de grande porte.','PRICE': 80,'VOLUME': 2,'WEIGHT': 1,'PROPERTIES': 2},

#MONEY (name,description,price,volume,weight)
'USD': ['dólar americano',['Surgiu em 1992 com o governo de Itamar Franco.'],1.0,0,0],
'BRL': ['real brasileiro',['Surgiu em 1992 com o governo de Itamar Franco.'],2.0,0,0],
'EUR': ['euro',['Surgiu em 1992 com o governo de Itamar Franco.'],0.85,0,0],
'creditcard1': {'NAME': 'cartão BB','DESCRIPTION': 'Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'creditcard2': {'NAME': 'cartão Uati','DESCRIPTION': 'Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'creditcard3': {'NAME': 'cartão Faixa','DESCRIPTION': 'Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},
'creditcard4': {'NAME': 'cartão Cabresto','DESCRIPTION': 'Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': {}},

#TREASURES (name,description,price,volume,weight,type)
'treasure_vase': {'NAME': 'vaso marajoara','DESCRIPTION': 'Um antigo vaso indígena feita da cerâmica do marajó.','PRICE': 2000,'VOLUME': 3,'WEIGHT': 3,'PROPERTIES': 0},
 
'jewel_emerald': {'NAME': 'esmeralda','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_diamond': {'NAME': 'diamante','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_ruby': {'NAME': 'rubi','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_amethyst': {'NAME': 'ametista','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_sapphire': {'NAME': 'safira','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_opal': {'NAME': 'opala','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_gold': {'NAME': 'ouro','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'jewel_quartz': {'NAME': 'quartzo','DESCRIPTION': 'Essa jóia deve custar uma fortuna!','PRICE': 2000,'VOLUME': 1,'WEIGHT': 3,'PROPERTIES': 0},
'mysterious': {'NAME': '???','DESCRIPTION': 'Você não faz idéia do que é isso.','PRICE': 0,'VOLUME': 1,'WEIGHT': 1,'PROPERTIES': 0},
}

GLUTEN_FOOD =  ['food_bread']

LACTOSE_FOOD = ['food_brigadeiro','food_cake_corn','food_cake_carrot','food_cake_chocolate',
'food_cookie_chocolate','food_cookie_strawberry','food_pizza_mussarella','food_pizza_shaggy','food_pizza_chicken','food_pizza_4cheese',
'drink_milk','drink_coffeenmilk','drink_chocolate','drink_yogurt']

CRAFTING = [
['drink_milk','drink_coffee','drink_coffeenmilk'],
['trash_bottle','craft_cloth','grenade_molotov_cocktail']
]

EXAMINE = ['sellcard','credit_card1','credit_card2','credit_card3','credit_card4','id_card0','id_card1','id_card2','id_card3','id_card4','id_card5']

TRICKS = {
'1.0': {'NAME': 'Instinto','DESCRIPTION': 'O usuário percebe uma presença estranha.','BONUS': [5,0,0,0,0]},
'1.1': {'NAME': 'Fúria','DESCRIPTION': 'Um ataque fulminante.','BONUS': [5,0,0,0,0]},
'2.0': {'NAME': 'Impulso','DESCRIPTION': 'Aumento de velocidade','BONUS': [5,0,0,0,0]},
'3.0': {'NAME': 'Terremoto','DESCRIPTION': 'O chão treme.','BONUS': [5,0,0,0,0]},
'4.0': {'NAME': 'Furacão','DESCRIPTION': 'Os oponentes giram.','BONUS': [5,0,0,0,0]},
'5.0': {'NAME': 'Atração','DESCRIPTION': 'Itens próximos chegam mais perto de você.','BONUS': [5,0,0,0,0]},
'6.0': {'NAME': 'Adivinhação','DESCRIPTION': 'O usuário prevê os movimentos do oponente.','BONUS': [5,0,0,0,0]},
'7.0': {'NAME': 'Indomado','DESCRIPTION': 'Invencível temporariamente.','BONUS': [5,0,0,0,0]},
}

VEHICLES = {
#BICYCLES
'bike_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'bike_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1},
#MOTOCYCLES
'moto_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'moto_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1},
#CARS
'car_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'car_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1},
#BUS
'bus_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'bus_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1},
#TRUCKS
'truck_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'truck_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1},
}
 
NUMBERS = [['Sidney','89074454'],['Jane','91124257'],['Renan','90435671'],['Diego','26148930'],['Bianca','76564008'],['Lúcia','90271802'],
['Maicon','23778988'],['Iago','77904623'],['Sofia','23578103'],['Vinícius','60428331'],['Pietra','40028922'],['Paulo','87690021'],['João Grande','56230401'],
['Pizza Delivery','53478809'],['Correios','09236521'],['Mercador','69696969']]
 
EMAILS = [
['prfrj@cmail.com','Caso de anomalia',['Boas novas','','Uma anomalia foi encontrada nos','arredores do Parque Nacional do Itatiaia,','É necessário a eliminação do','indivíduo assim que o possível','','Encontrem seus próprios meios','para adentrar o local.']],
 
['prfrj@cmail.com','Caso de anomalia',['Boas novas','','Uma anomalia foi encontrada nos','arredores da cidade de Resende,','É necessário a eliminação do','indivíduo assim que o possível','','Encontrem seus próprios meios','para adentrar o local.']],


#['cangaceirostv@cmail.com','Proposta de entrevista',
#['Boas novas, ' + res.CHARACTERS[0]['NAME'] + ' ' + res.CHARACTERS[0]['LASTNAME'] + '.', ' ', 'Com a repercussão dos casos de', 'anomalias do Departamento de', 'Detenção de Anomalias de',
#'Itatiaia, sugerimos uma', 'entrevista com você e dois', 'participantes para o', 'Jornal da Noite.', ' ', 'A entrevista será ás 5:30 PM', 'e será gravado nos estúdios', 'da Cangaceiros TV, na',
#'Av. Getúlio Vargas.', ' ', 'Aguardamos sua resposta', 'no local.']],
 
['mendoncapietra7@cmail.com','Oiee',
['Só tô te testando menino']],
]

RANDNEWS = [[
('Polícia Federal',[
	('prende',[('homem',[('suspeito de',['assédio sexual','assassinato','sequestro']),'foragido']),'mulher']),
	('apreende',['maconha','carga roubada','celulares roubados','produtos falsificados']),
	('captura',['bandido','criminoso']),('encontra',[('corpo de',['criança desaparecida','mulher esquartejada']),'pessoa desaparecida'])]),
('Homem',[('é acusado',['de assassinato','por ex','de homicídio','por matar']),('é visto',[('roubando',['carros','celulares','roupas','empadas']),('assaltando',['caixa eletrônico','banco','mercado local','supermercado','loja'])])]),
('Enchente atinge',[('região serrana',['do Rio de Janeiro','de Minas Gerais','de São Paulo']),('cidade do interior',['do Rio de Janeiro','de Minas Gerais','de São Paulo'])]),
('Preço',[('dos',[
	('combustíveis',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),
	('alimentos',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),
	('imóveis',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),
	('colchões',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])]),
	('do',[
		('arroz',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),
		('gás',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])]),
	('da',[
		('conta de luz',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),
		('conta de água',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])])])
],
['no Acre','em Angra dos Reis','em Petrópolis','no Rio de Janeiro','em Belo Horizonte','em Lagoinha','em Taubaté','em Pindamonhangaba','em Guarulhos','em Juiz de Fora']
]

RADIONEWS = [
[(25,12),(0,40),'Uma casa foi destruída no interior de Petrópolis. As autoridades ainda não descobriram as causas do incidente.']
]

TASKINDEX = {
#HIKO LABYRINTH
'LVL_00_0': [{'TEXT': 'Pinte os pisos de vermelho.','TIME': [-5,0,0],'OBJECTIVE': 'color'},
{'TEXT': 'Pinte os pisos de laranja.','TIME': '-0500','OBJECTIVE': 'color'}],
'LVL_05_0': [('Pinte os pisos de verde..',None,'-0500')],
'LVL_08_1': [('Alcançe 5000 pontos..',None,'-0500')],

#CAMPAIGN MISSIONS
'CH01': [('Falar com a ',(23,5),'2512','1000'),
('Procure algo pra beber','0000','0000')],
'CH10': [('Faça as compras no mercadinho','0000','0000',['1urban_0',30,30,1]),
('Vá para o edifício esmeralda','0000','0000'),
('Vá para uma delegacia','0000','0000')],
'CH20': [('Vá para sua casa','0000','0000'),
('Viaje até o sítio arqueológico','0000','0000')],
'CH40': [('Siga as viaturas','0000','0000'),
('Procure um lugar para ficar','0000','0000')],
'CH81': [('Chame uma ambulância','0000','0000')],

#SIDE QUESTS
'SQ001': [('Dar dominó',None,None)],

#TOWER DEFENSE WAVES
'TDW': [('Primeira onda','0000','0000'),('Segunda onda','0000','0000')],
}
 
DTALKS = {'good morning': 'Bom dia','good afternoon': 'Boa tarde','good evening': 'Boa noite','good night': 'Boa noite',
'he1': 'Senhor','she1': 'Senhora'}

SIGNS = {
'INN': 'pousada', 'PUB': 'bar', 'HOTEL': 'hotel', 'DRUGSTORE': 'drogaria', 'BAKERY': 'padaria', 'BAZAAR': 'bazar', 'MARKET': 'mercado', 'BANK': 'banco',
'GAS': 'posto','HOSPITAL': 'hospital','POLICE': 'delegacia', 'SHOP': 'loja', 'BATHROOM': 'banheiro'
}

AVATAR = {
'humanoid_head': ['redondo','quadrado','pontudo'],
'humanoid_hair': ['careca','raspado','calvo','afro','cacheado curto','cacheado médio','cacheado longo','cacheado preso',
	'crespo curto','crespo médio','crespo longo','crespo preso',
	'liso curto','liso médio','liso longo','liso preso','dread curto','dread médio','dread longo','dread preso',
	'trança curta','trança média','trança longa','trança presa'],
'humanoid_eyes': ['redondo','puxado'],
'humanoid_eyebrows': ['fino','médio','grosso','rena','monocelha','corte'],
'humanoid_nose': ['fino','pontudo','longo','redondo','pequeno'],
'humanoid_facialhair': ['bigode fino','bigode pequeno','barba rala','barba cheia','barba longa','barbicha','cavanhaque'],
'humanoid_torso': ['sem seios','seios pequenos','seios grandes'],
'humanoid_marks': ['sinal','cicatriz','sardas','vitiligo','queimadura','ferida'],
'humanoid_tatoos': ['runas','fogo','água','terra','ar'],
'humanoid_facepaint': ['listras','olhos','setas'],
'humanoid_mask': ['jason','vampiro'],
'humanoid_hat': ['boné','gorro curto','gorro longo','chapéu de sol','sombreiro','chapéu de palha','boina','chapéu de aviador'],
'humanoid_glasses': ['óculos de grau redondo','óculos de grau quadrado','óculos escuros redondos','óculos escuros quadrados',
	'óculos 3D','visor de proteção'],
'humanoid_Lear': ['brinco pequeno','argola','piercing','alargador','fone'],
'humanoid_Rear': [],
'humanoid_neck': ['corrente','terço','memento','bandana'],
'humanoid_piercings': ['esfera','barra'],
'humanoid_Lhand': ['luva de pedreiro','luva de goleiro','luva de ciclista','luva sem dedos','luva de médico'],
'humanoid_Rhand': [],
'humanoid_Lpulse': ['relógio analógico','relógio digital','pulseira'],
'humanoid_Rpulse': [],
'humanoid_uppercloth': ['flanela','moletom','jaqueta','terno','avental','macacão'],
'humanoid_shirt': [],
'humanoid_pants': [],
'humanoid_dress': ['saia','mini saia','tutu','vestido'],
'humanoid_socks': [],
'humanoid_feet': ['descalço','chinelo','chinelo chique','sapato esportivo','sapato social','bota','pantufa']
}

HINTS = {
'MENUS': '{6} inventário {7} celular','NPC_DIALOG': '{4} conversar','NAMING': 'digite os nomes no teclado {6} prosseguir',
'VEHICLE_USE': '{4} montar','VEHICLE_CONTROLS': '{5} esquerda {3} direita {5} acelerar {1} freiar {0} desmontar',
'INVENTORY_ITEMS': '{4} usar {5} segurar','INVENTORY_HOLD': '{4} juntar {5} colocar','INVENTORY_ACCESORIES': '{5} tirar',
'BATTLE_TACTICS': '{4} escolher tática','BATTLE_DIALOG': '{4} dialogar','BATTLE_GUARD': '{4} defender','BATTLE_RUN': '{4} fugir','BATTLE_SHOT': '{4} atacar',
'APPS': '{4} selecionar','GPS': '{4} aumentar {5} diminuir','CONTACTS': '{4} selecionar','EMAIL': '{0}{1} selecionar {4} ler',
'NEWS': '{0}{1} selecionar {4} ler','RADIO': '{2}{3} mudar estação {4} tocar','CAMERA': '{4} salvar jogo','BESTIARY': '{4} selecionar',
'TASKS': '{0}{1} selecionar','STATUS': '{2}{3} olhar personagens','TACTICS': '{4} administrar tática','ACHIEVEMENTS': '{0}{1} selecionar',
'RANKING': None,'MANUAL': '{0}{1} selecionar {4} ler','SETTINGS': '{4} selecionar','ABOUT': '{4} acessar link',
'CALLING': '{4} atender','PHOTO': '{4} fotografar'
}
     
TTSTEXT = {'.': 'ponto',',': 'vírgula',':': 'dois pontos',';': 'ponto e vírgula',' ': 'espaço','!': 'exclamação','?': 'interrogação',
'"': 'aspas duplas',"'": 'aspas','(': 'abre parênteses',')': 'fecha parenteses','[': 'abre colchetes',']': 'fecha colchetes','{': 'abre chaves','}': 'fecha chaves',
'<': 'menor que','>': 'maior que','CAPS1': 'minúscula','CAPS2': 'maíscula','CAPS3': 'caps lock','CONFIRM': 'confirm','DELETE': 'deletar','PAGE': 'página'}

MENU = {'new_file': 'nova sessão','load_file': 'iniciar sessão','save_file': 'salvar sessão','delete_file': 'excluir sessão','resume': 'continuar','exit': 'sair',
'Inventory': 'inventário','volume': 'volume','weight': 'peso','discover': 'Use o item para obter informações.','drop': 'Escolha os itens que deseja descartar.',
'Storage': 'depositar','Products': 'produtos','Basket': 'carrinho','Wash': 'lavar','Mercator': 'Mercador','Trash': 'lixeira',
'armor': 'proteção','duration': 'duração','damage': 'dano','recharge': 'recarga','cadency': 'cadência','capacity': 'capacidade',
'gauge': 'calibre','vitality': 'vitalidade','hunger': 'fome','thirst': 'sede','storage': 'depositar',
'success': 'sucesso','fail': 'falha','touche': 'touché','strike': 'strike','ko': 'nocaute','one_more': 'oitra vez','miss': 'errou...',
'victory': 'vitória','perfect': 'perfeito','lost': 'derrota','continue': 'continuar?','level_up': 'foi promovido para',
'GPS': 'mapa','Contacts': 'contatos','Email': 'emails','Newspaper': 'notícias','Radio': 'música','Camera': 'galeria','Bestiary': 'bestiário','Calendar': 'calendário',
'Tasks': 'tarefas','Status': 'ficha','Tactics': 'táticas','Achievements': 'conquistas','Ranking': 'placar','Help': 'ajuda','Settings': 'ajustes','About': 'sobre',
'no_signal': 'sem sinal','no_credit': 'sem saldo','no_freaks': 'nenhuma anomalia registrada','empty': 'nada por aqui','calling': 'chamando',
'to_do': 'fazer','done': 'feitas','all': 'todas','unread': 'novas','read': 'lidas','groups': 'grupos','history': 'histórico',
'name': 'nome','birth': 'data de nascimento','hometown': 'naturalidade','rg': 'registrado','cpf': 'cpf',
'gameplay': 'geral','sound': 'áudio','controls': 'controles',
'lang': 'idioma','border': 'borda','hints': 'dicas','tutorials': 'tutoriais','cursor': 'cursor','dislexic': 'dislexia',
'sfx': 'som','music': 'música','tts': 'narrador','cc': 'áudio descrição','speed': 'velocidade','censorship': 'censura',
'bt_choose': 'escolba o botão','vibrate': 'vibrar',
'conf': 'confirmar','info': 'info','yes': 'sim','no': 'não','ok': 'ok','cancel': 'cancelar',
'Phone': 'celular','PC': 'computador','PDA': 'pda','Image': 'imagem','AudioPlayer': 'áudio','GifPlayer': 'gif','TextReader': 'arquivo',
'not_email': 'Novo Email','not_contact': 'Novo contato adicionado!','not_wash': 'Sua roupa foi lavada!',
'left_to_go': '{}{} para chegar em'}

HOLIDAYS = [(1,1,'Feliz ano novo!'),(3,8,'Feliz dia da mulher!'),(3,15,'É aniversário do autor!'),(4,7,'Feliz páscoa!'),(4,22,'Feliz dia da terra!'),(10,31,'Feliz Halloween!'),(12,25,'Feliz natal!')]

RADIOEE = [['MNOM','0609','0000'],['DJNEL','0402','0020'],
['MC1','1702','0300'],['MC2','1806','0300'],['MC3','2012','0300'],['MC4','2512','0736'],
['SGPP','2605','0000'],['FT','0707','0000'],
['RV1','2512','0609'],['RV2','1308','0830']]

ABOUT = ['Source code por Matt Kai','Feito em Python','Twitter','GitHub','GNU General Public License']
  
DISCLAIMER = ['Esta é uma obra de ficção,','e quaisquer semelhanças com','acontecimentos reais são','mera coincidência.','',
'Uma certa porcentagem da','população sofre de condições','como eplepsia e convulsões,','por isso sempre consulte','seu médico antes de jogar']

BUILDING = ['Preparando uma nova executável da aplicação.\nPor favor, aguarde...','Aplicação .exe compilada com sucesso em ','Instalador .msi compilado com sucesso em ']

MAPTOOLS = {'select': ['seleção','seleciona tiles a partir de uma área retangular.'],
'transform': ['transformar','move tiles dentro de uma área retangular.'],
'pencil': ['lápis','pinta o mapa com a tile selecionada.'],'erase': ['borracha','apaga tiles.'],
'pick': ['conta gotas','use para obter a tile selecionada.'],'fill': ['preencher','pinta tiles.'],'rect': ['retângulo','apaga tiles.'],
'copy': ['copiar','copia tiles da seleção.'],'cut': ['recortar','copia tiles da seleção e em seguida as remove.'],'paste': ['colar','cola tiles de uma seleção.'],
'undo': ['desfazer','volta um passo no histórico.'],'redo': ['refazer','avança um passo no histórico.'],
'load': ['carregar','carrega um mapa.'],'save': ['salvar','salva um mapa.'],
'zoomin': ['ampliar','aumenta o zoom.'],'zoomout': ['reduzir','diminui o zoom.']}

ERROR = {'crash': 'Oops! Alguma coisa deu errado... =(','press': 'Aperte qualquer botão para fechar','file': 'Arquivo','line': 'linha','in': 'em','restart': 'Reiniciando...',
	'img_noload': 'ATENÇÃO! imagem não foi carregada.','tileset_save': 'Não foi possível salvar a tileset: está sendo utilizada.','dialog_key': 'ATENÇÃO: Não foi possível carregar o diálogo. Chave inexistente: ',
	'sound_exists': 'ATENÇÃO! Este arquivo ou outro com um nome semelhante já foi carregado: "{}" | Considere renomear os arquivos para evitar problemas.'
	}

MINIGAMES = {
'Pinball': 'Pinball','Tetris': 'Tetris','Minesweeper': 'Campo Minado','Pong': 'Pong','Differences': '7 Erros','Jigsaw': 'Quebra-cabeça','Maze': 'Labirinto','Pool': 'Sinuca','MusicTiles': 'Guitarrero',
'Footrace': 'Corrida','Hops': 'Pula corda',
'Snake': 'Snake','HittheMole': 'Acerte a toupeira','FallingItems': 'Chuva de itens','Jumping': 'Pulando','FlappyBird': 'Flappy Bird','Breakout': 'Breakout','BubbleBubble': 'Bubble Bubble','CannonBattle': 'Canhões','ColorMatch': 'Combinações',
'Twothousandforthyeight': '2048','Memory': 'Jogo da Memória','Simon': 'Simon','FindtheCup': 'Jogo dos Copos','ImageMatch': 'Combine a imagem','Cassino': 'Caça-níquel','Roulette': 'Roleta',
'Chess': 'Xadrez','Checkers': 'Damas','Trilha': 'Trilha','Blackgammon': 'Gamão','Ludo': 'Ludo','Reversi': 'Reversi','SnakesNLadders': 'Cobras e Escadas','NumberPuzzle': 'Quebra-cabeça de números',
'Solitaire': 'Paciência','SpiderSolitaire': 'Paciência Spider','Freecell': 'Freecell','Mahjong': 'Mahjong','PegSolitaire': 'Resta 1',
'Dominoes': 'Dominó','Truco': 'Truco','Sueca': 'Sueca','Cacheta': 'Cacheta','Pife': 'Pife','Buraco': 'Buraco','Poker': 'Poker','Copas': 'Copas','Espadas': 'Espadas','Maumau': 'Maumau',
'Matchingwords': 'Palavras Cruzadas','TicTacToe': 'Jogo da Velha','LinesNBoxes': 'Timbiriche','Nonogram': 'Nonograma','HuntingWords': 'Caça Palavras','Sudoku': 'Sudoku','Hangman': 'Jogo da Forca',
'Yatzy': 'Yatzy','Stop': 'Adedonha','Piano': 'Piano'
}

ACHIEVEMENTS = [
['Zerado','Ganhar todos os troféus',0,''],

['Zerado','Complete o capítulo "Depois do Começo"',0,''],
['Zerado','Complete o capítulo "Duplo Andantes"',0,''],
['Zerado','Complete o capítulo "Sangue Verde"',0,''],
['Zerado','Complete o capítulo "Não se meta com a gangue"',0,''],
['Zerado','Complete o capítulo "Caminhões Canavieiros"',0,''],
['Zerado','Complete o capítulo "Peste Negra"',0,''],
['Zerado','Complete o capítulo "Pelo benefício de Mr.Kite!"',0,''],
['Zerado','Complete o capítulo "Vida Loka"',0,''],
['Zerado','Complete o capítulo "Milícia x Meliante"',0,''],
['Zerado','Complete o capítulo "Dr.Estanho"',0,''],
['Zerado','Complete o capítulo "Não Identificado"',0,''],
['Zerado','Complete o capítulo "Químicas Quimeras"',0,''],
['Zerado','Complete o capítulo "Quem tem medo de assombração?"',0,''],
['Zerado','Complete o capítulo "MP-XIII"',0,''],

['Piloto','Vencer 10 corridas',0,''],
['Fúria da Estrada','Vencer 50 corridas',0,''],
['Corredor da Noite','Vencer 100 corridas',0,''],
   
['Exterminador','Expurgue 100 anomalias',0,''],
['Terror dos imundos','Expurgue 500 anomalias',0,''],
['Purificador','Expurgue 1000 anomalias',0,''],
   
['Espadachim','Compre todas as armas brancas',0,''],
['Arsenal Pesado','Compre todas as armas de fogo',0,''],
['Por Precaução','Compre todos os coletes',0,''],
['Os 6 Lendários','Eleve o nível de todos ao 100',0,''],
   
['Sociável','Registre todos os contatos',0,''],
['O Caçador de Mitos','Registre todas as anomalias no Bestiário',0,''],
['Temos um Xeroque Holmes','Complete o esqueleto de todas as anomalias',0,''],
   
['Não que eu me orgulhe disso','Roube um caixa',0,''],
['Zé Droguinha','Roube um veículo',0,''],
['Vergonha da Profission','Mate um cidadão',0,''],
['Traíra','Fuja da polícia',0,''],
   
['Eu Sou a Lenda','Derrote uma anomalia maior apenas usando armas brancas',0,''],
['Meros Insetos','Vença 5 batalhas consecutivas sem tomar dano',0,''],
['Salmos 91:7','Vença um exército sem tomar dano',0,''],
['Fugir é sabedoria','Fuja de uma batalha 20 vezes',0,''],
['Podre de Rico','Consiga 1.000.000.000 em dinheiro vivo',0,'']
]

MESSAGES = [
['Não feche o jogo se','o ícone de carregamento','aparecer no canto da tela'],
['Esta é uma obra de ficção,','e quaisquer semelhanças com','acontecimentos reais podem','ter alterações artísticas.'],
['Uma certa porcentagem da','população sofre de condições','como eplepsia e convulsões,','por isso sempre consulte','seu médico antes de jogar'],
['Conecte-se na Steam ou','No Google Play para salvar','seus dados'],
['Algum youtuber está','jogando isso aqui?']
]

TSECRETS = ['É verdade, certo, e muito verdadeiro.',
'54 68 65 20 42 69 72 64 20 6f 66 20 48 65 72 6d 65 73 20 69 73 20 6d 79 20 6e 61 6d 65 2c 20 65 61 74 69 6e 67 20 6d 79 20 77 69 6e 67 73 20 74 6f 20 6d 61 6b 65 20 6d 65 20 74 61 6d 65 2e',
'Você tem louça para lavar?',
'54 68 65 20 53 65 72 70 65 6e 74 20 6f 66 20 41 72 61 62 69 61 20 69 73 20 6d 79 20 6e 61 6d 65 2c 20 74 68 65 20 77 68 69 63 68 20 69 73 20 6c 65 61 64 65 72 20 6f 66 20 61 6c 6c 20 74 68 69 73 20 67 61 6d 65 2e',
'4c 61 72 6b 27 73 20 54 6f 6e 67 75 65 73 20 69 6e 20 41 73 70 69 63',
'49 20 77 61 6e 74 20 74 6f 20 62 65 6c 69 65 76 65',
'Hoc non pereo habebo fortior me',
'01010110 01101111 01100011 11101010 00100000 01100100 01100101 01110011 01100011 01101111 01100010 01110010 01101001 01110101 00100000 01110101 01101101 00100000 01100101 01101110 01101001 01100111 01101101 01100001 00100001',
'ipse se nihil scire id unum sciat',
'A vingança nunca é plena, mata a alma e a envenena',
'01001110 01101111 01110011 01110011 01100001 00100000 01100101 01110011 01110000 01100101 01110010 01100001 01101110 11100111 01100001 00100000 01100101 01110011 01110100 11100001 00100000 01101110 01101111 00100000 01101110 \
	01101111 01110011 01110011 01101111 00100000 01110011 01100001 01101100 01110110 01100001 01100100 01101111 01110010 00100000 01001011 01100001 00100111 01101100 01100101 01100010',
'Hello World!',
'insira uma mensagem aqui',
'Veritas lux mea',
'Soy juan carlos bodoque, y esta fue mi nota verde'
]

STARTINFO = 'Licenciado pela GNU General Public License.'