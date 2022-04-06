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
'cop': ['polical',['cabo','capitão','comandante','sargento','delegado']],

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
'PATH': 'horizontal','DODGE': 'walk','SKELETON': {'body': (12,39),'eye': [(13,26),(31,26)]},
'HABILITIES': [['Morder','O felino morde o oponente.',-5,1,40,1],['Arranhar','O felino usa suas garras para atacar o oponente.',-3,10,40,10],
['Ronronar','O felino ronrona, mostrando seu desprezo pela situação.',0,9,10,1],['Miar','O felino mia para o além, chamando outros felinos.',('4.1.0'),7,10,1]],
'FOOD': 'ingredient_mice','WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM','SCREAM': 1},
   
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
'bag1': ['bolsinha',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 5 - Peso: 5'],1000,5,5],
'bag2': ['bolsa',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 10 - Peso: 10'],2500,10,10],
'bag3': ['mala',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 20 - Peso: 15'],5000,20,15],
'bag4': ['mochila',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 30 - Peso: 20'],7500,30,20],
'bag5': ['mala de rodinhas',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 30 - Peso: 25'],10000,30,25],
'tube100': ['frasco de sulfúrio 100ml',['Feita especialmente para guardar sangue verde.'],200,1,1,100],
'tube250': ['pote de sulfúrio 250ml',['Feita especialmente para guardar sangue verde.'],200,1,1,250],
'tube500': ['garrafa de sulfúrio 500ml',['Feita especialmente para guardar sangue verde.'],200,1,1,500],
'wallet': ['carteira',['Use para guardar seu dinheiro e coisas pequenos.','JAMAIS PERCA ISSO!'],50,1,1],
'lock': ['cadeado',['Use para proteger objetos.'],10,1,1],
'locksmith1': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith2': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith3': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith4': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith5': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith6': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'locksmith7': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1],
'bottle1': ['garrafa vermelha',['Use para armazenar bebidas.'],10,2,1],
'bottle2': ['garrafa laranja',['Use para armazenar bebidas.'],10,2,1],
'bottle3': ['garrafa amarela',['Use para armazenar bebidas.'],10,2,1],
'bottle4': ['garrafa verde',['Use para armazenar bebidas.'],10,2,1],
'bottle5': ['garrafa ciano',['Use para armazenar bebidas.'],10,2,1],
'bottle6': ['garrafa azul',['Use para armazenar bebidas.'],10,2,1],
'bottle7': ['garrafa rosa',['Use para armazenar bebidas.'],10,2,1],
   
#HEAD ACCESORIES (name,description,price,volume,weight)
'head_hairclip': ['xuxinha',['Pra amarrar o cabelo.'],30,1,1,3],
'head_hat1': ['boné',['Pra proteger do sol e ficar estiloso.'],30,2,1,1],
'head_hat2': ['gorro',['Reza a lenda que todo mundo que usa vira um mendigo.'],30,2,1,1],
'head_hat3': ['chapéu de sol',['Ideal para a praia'],30,2,1,1],
'head_hat4': ['chapéu de aviador',['De um falecido senhor...'],30,2,1,1],
'head_glasses1': ['óculos de grau',['Apenas pra quem precisa, senão você','ganha cegueira.'],30,2,1,1],
'head_glasses2': ['óculos escuros',['Pra quem não tem colírio.'],30,2,1,1],
'head_glasses3': ['óculos redondos',['Qualquer um que usá-lo se transforma','imediatamente no Harry Potter.'],30,2,1,1],
'head_glasses4': ['óculos retrô',['Apenas para quem é hype de verdade.'],30,2,1,1],
'head_glasses5': ['visor de laboratório',['Se não usar um ácido pode cair no seu olho.'],30,2,1,1],

#CUSTOM CLOTHES (name,description,price,volume,weight,color)
'clth_shirt1': ['camisa preta',['O traje predileto dos solitários.'],30,4,1,0],
'clth_shirt2': ['camisa laranja',['Roupa casual.'],30,4,1,2],
'clth_shirt3': ['camisa vermelha',['Roupa casual.'],30,4,1,3],

'clth_regatta1': ['regata vermelha',['É excelente caso esteja fazendo calor.'],30,4,1,3],

'clth_stripeshirt01': ['camisa vermelha listrada',['Parece com o uniforme do flamengo.'],30,4,1,3],

'clth_jacket1': ['jaqueta preta',['Pra dar uma de Ramones.'],30,4,1,'01'],
'clth_jacket2': ['avental',['Para pesquisadores.'],30,4,1,'06'],

'clth_flannel1': ['flanela verde',['Pareçe roupa de festa junina.'],30,4,1,'02'],
'clth_flannel2': ['flanela vermelha',['Conhece o Iberê? então.'],30,4,1,'03'],
'clth_flannel3': ['flanela laranja',['Parece o tipo de roupa que um menino do mato grosso usaria.'],30,4,1,'03'],

'clth_sweatshirt1': ['moletom cinza',['Pra aqueles que não tem paciêcia','pra escolher roupa.'],30,4,1,'04'],
'clth_sweatshirt2': ['moletom azul',['Pra aqueles que não tem paciêcia','pra escolher roupa.'],30,4,1,'05'],
'clth_tutu00': ['tutu',['Uma bela saia para bailarinas.'],30,4,1,2,'07'],

'clth_printedshirt1': ['camisa de ET',['A favorita dos ufólogos.'],30,4,1,3],
'clth_printedshirt2': ['camisa de banda',['Está escrito "Senta que lá vem história".'],30,4,1,3],

'clth_bikini1': ['biquíni vermelho',['Bom para ir á praia'],30,4,1,'06'],
'clth_fantasy1': ['fantasia de anjo',['A fantasia mais usada no carnaval.'],30,4,1,'06'],
'clth_fantasy2': ['fantasia de diabo',['A segunda fantasia mais usada no carnaval.'],30,4,1,'06'],
'clth_fantasy3': ['fantasia de gatinho',['Talvez essa seja a fantasia mais usada.'],30,4,1,'06'],
'clth_fantasy4': ['roupa de passista',['Foi encontrada no edifício esmeralda.'],30,4,1,'06'],

'clth_uniform1': ['uniforme de faculdade',['Uniforme da Universidade Federal Fluminense.'],30,4,1,'06'],
'clth_uniform2': ['uniforme de zelador',['Quem usa essa roupa geralmente é bom de conversa.'],30,4,1,'06'],

'undr_shorts1': ['shorts jeans',['Esse tipo de calça é a sensação do momento!'],30,4,1,'06'],
'undr_shorts2': ['shorts fino',['Esse tipo de calça é a sensação do momento!'],30,4,1,'06'],

'undr_pants1': ['calça jeans clara',['Esse tipo de calça é a sensação do momento!'],30,4,1,'06'],
'undr_pants2': ['calça jeans escura',['Esse tipo de calça é a sensação do momento!'],30,4,1,'06'],

#VESTS (name,description,price,volume,weight,armor,duration)
'vest1': ['colete amarelo',['Cuidado pra não pensarem que','é um francês manifestante.'],30,3,1,1,10],
'vest2': ['colete salva-vidas',['Mesmo sem água por perto, protege bastante.'],60,2,1,3,15],
'vest3': ['colete I',['Reduz o dano do advesário','DEFESA: 5 DURAÇÃO: 25'],120,3,1,5,20],
'vest4': ['colete IIA',['Reduz o dano do advesário','DEFESA: 8 DURAÇÃO: 25'],240,3,1,8,25],
'vest5': ['colete II',['Reduz o dano do advesário','DEFESA: 10 DURAÇÃO: 30'],360,3,1,10,30],
'vest6': ['colete IIIA',['Reduz o dano do advesário','DEFESA: 12 DURAÇÃO: 35'],480,3,1,12,35],
'vest7': ['colete III',['Restrito apenas para','policiais de elite.'],600,3,1,16,40],
'vest8': ['colete IV',['Restrito apenas para','policiais de elite.'],720,3,1,20,45],
 
#CHARMS (name,description,price,volume,weight,armor,duration)
'amulet1': ['cruz',['Conçede proteção e espanta espíritos.'],20,1,1,5,50],
'amulet2': ['ankh',['Conçede proteção e espanta espíritos.'],20,1,1,10,50],
'amulet3': ['hamsá',['Conçede força e proteção.'],20,1,1,15,50],
'amulet4': ['pentáculo',['Conçede força, proteção e vitalidade.'],20,1,1,20,50],
'amulet5': ['tríscele',['Conçede força, proteção e vitalidade'],20,1,1,25,50],
'amulet6': ['ouroboros',['Conçede força, proteção,','vitalidade e resistência.'],20,1,1,25,50],
'amulet7': ['muiraquitã',['Conçede aumento em todos os atributos.'],20,1,1,25,50],
 
#AMMO (name,description,price,volume,weight,calibre,metal)
'ammo_stone': ['pedra',['Isso pode salvar sua vida um dia.'],1,2,2,0],
'ammo_tranquilizer': ['tranquilizante',['Munição para pistola que faz','o inimigo adormecer.'],100,2,1,0],
'arrow_gold': ['flechas de ouro',['Munição para arco e beste com ponta de ouro.'],20,2,1,0,1],
'arrow_silver': ['flechas de prata',['Munição para arco e beste com ponta de prata.'],20,2,1,0,2],
'arrow_copper': ['flechas de cobre',['Munição para arco e beste com ponta de cobre.'],20,2,1,0,3],
'arrow_tin': ['flechas de estanho',['Munição para arco e beste com ponta de estanho.'],20,2,1,0,4],
'arrow_lead': ['flechas de chumbo',['Munição para arco e beste com ponta de chumbo.'],20,2,1,0,5],
'arrow_iron': ['flechas de ferro',['Munição para arco e beste com ponta de ferro.'],20,2,1,0,6],
'arrow_mercury': ['flechas de mercúrio',['Munição para arco e beste com ponta de mercúrio.'],20,2,1,0,7],
'ammo.12_gold': ['munição.12 de ouro',['Balas de ouro de calibre 12.'],200,2,1,12,1],
'ammo.12_silver': ['munição.12 de prata',['Balas de prata de calibre 12.'],200,2,1,12,2],
'ammo.12_copper': ['munição.12 de cobre',['Balas de cobre de calibre 12.'],200,2,1,12,3],
'ammo.12_tin': ['munição.12 de estanho',['Balas de estanho de calibre 12.'],200,2,1,12,4],
'ammo.12_lead': ['munição.12 de chumbo',['Balas de chumbo de calibre 12.'],200,2,1,12,5],
'ammo.12_iron': ['munição.12 de ferro',['Balas de ferro de calibre 12.'],200,2,1,12,6],
'ammo.12_mercury': ['munição.12 de mercúrio',['Balas de mercúrio de calibre 12.'],200,2,1,12,7],
'ammo.16_gold': ['munição.16 de ouro',['Balas de ouro de calibre 16.'],200,2,1,16,1],
'ammo.16_silver': ['munição.16 de prata',['Balas de prata de calibre 16.'],200,2,1,16,2],
'ammo.16_copper': ['munição.16 de cobre',['Balas de cobre de calibre 16.'],200,2,1,16,3],
'ammo.16_tin': ['munição.16 de estanho',['Balas de estanho de calibre 16.'],200,2,1,16,4],
'ammo.16_lead': ['munição.16 de chumbo',['Balas de chumbo de calibre 16.'],200,2,1,16,5],
'ammo.16_iron': ['munição.16 de ferro',['Balas de ferro de calibre 16.'],200,2,1,16,6],
'ammo.16_mercury': ['munição.16 de mercúrio',['Balas de mercúrio de calibre 16.'],200,2,1,16,7],
'ammo.22_gold': ['munição.22 de ouro',['Balas de ouro de calibre 22.'],200,2,1,22,1],
'ammo.22_silver': ['munição.22 de prata',['Balas de prata de calibre 22.'],200,2,1,22,2],
'ammo.22_copper': ['munição.22 de cobre',['Balas de cobre de calibre 22.'],200,2,1,22,3],
'ammo.22_tin': ['munição.22 de estanho',['Balas de estanho de calibre 22.'],200,2,1,22,4],
'ammo.22_lead': ['munição.22 de chumbo',['Balas de chumbo de calibre 22.'],200,2,1,22,5],
'ammo.22_iron': ['munição.22 de ferro',['Balas de ferro de calibre 22.'],200,2,1,22,6],
'ammo.22_mercury': ['munição.22 de mercúrio',['Balas de mercúrio de calibre 22.'],200,2,1,22,7],
'ammo.32_gold': ['munição.32 de ouro',['Balas de ouro de calibre 32.'],200,2,1,32,1],
'ammo.32_silver': ['munição.32 de prata',['Balas de prata de calibre 32.'],200,2,1,32,2],
'ammo.32_copper': ['munição.32 de cobre',['Balas de cobre de calibre 32.'],200,2,1,32,3],
'ammo.32_tin': ['munição.32 de estanho',['Balas de estanho de calibre 32.'],200,2,1,32,4],
'ammo.32_lead': ['munição.32 de chumbo',['Balas de chumbo de calibre 32.'],200,2,1,32,5],
'ammo.32_iron': ['munição.32 de ferro',['Balas de ouro de calibre 32.'],200,2,1,32,6],
'ammo.32_mercury': ['munição.32 de mercúrio',['Balas de mercúrio de calibre 32.'],200,2,1,32,7],
'ammo.38_gold': ['munição.38 de ouro',['Balas de ouro de calibre 38.'],200,2,1,38,1],
'ammo.38_silver': ['munição.38 de prata',['Balas de prata de calibre 38.'],200,2,1,38,2],
'ammo.38_copper': ['munição.38 de cobre',['Balas de cobre de calibre 38.'],200,2,1,38,3],
'ammo.38_tin': ['munição.38 de estanho',['Balas de estanho de calibre 38.'],200,2,1,38,4],
'ammo.38_lead': ['munição.38 de chumbo',['Balas de chumbo de calibre 38.'],200,2,1,38,5],
'ammo.38_iron': ['munição.38 de ferro',['Balas de ferro de calibre 38.'],200,2,1,38,6],
'ammo.38_mercury': ['munição.38 de mercúrio',['Balas de mercúrio de calibre 38.'],200,2,1,38,7],
'ammo.42': ['munição.42',[''],400,2,1,42],
'ammo.44': ['munição.44',[''],200,2,1,44],
'ammo.45': ['munição.45',[''],200,2,1,45],
'ammo.38mm': ['munição 0.38mm',[''],200,2,1,380],
'ammo.5.56mm': ['munição 5.56mm',[''],200,2,1,556],
'ammo_missile': ['míssel',[''],800,5,4,1000],
 
#TOOLS (name,description,price,volume,weight,{damage,unlock})
'tool_crowbar': ['pé de cabra',['Use para abrir portas trancadas.'],50,4,3,{'DAMAGE': 5, 'UNLOCK': 'metal','RECHARGE': 2,'CADENCY': 50}],
'tool_axe': ['machado',['Use para quebrar madeira.'],50,4,4,{'DAMAGE': 5, 'UNLOCK': 'wood','RECHARGE': 2,'CADENCY': 50}],
'tool_hammer': ['martelo',['Conserta, prega e quebra objetos e cabeças.'],30,3,3,{'DAMAGE': 3, 'UNLOCK': 'stone','RECHARGE': 2,'CADENCY': 50}],
'tool_sledgehammer': ['marreta',['Use para quebrar vidro.'],50,4,5,{'DAMAGE': 5, 'UNLOCK': 'stone','RECHARGE': 2,'CADENCY': 50}],
'tool_dustpan': ['pá de lixo',['Cai bem para limpar a sujeira.'],10,5,3,{'DAMAGE': 1,'RECHARGE': 2,'CADENCY': 50}],
'tool_shovel': ['pá',['Use para cavar o solo para encontrar itens e abrir passagens.'],50,5,3,{'DAMAGE': 5, 'UNLOCK': 'grass','RECHARGE': 2,'CADENCY': 50}],
'tool_chainsaw': ['motoserra',['Use para cortar árvores grandes','e de quebra bancar o Jason.'],50,6,3,{'DAMAGE': 5, 'UNLOCK': 'wood','RECHARGE': 2,'CADENCY': 50}],
'tool_lighter1': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter2': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter3': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter4': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter5': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter6': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_lighter7': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'tool_spoon': ['colher',['Você não come do prato com as mãos, correto?'],6,1,1],
'tool_fork': ['garfo',['Você não come do prato com as mãos, correto?'],6,1,1],
'tool_knife': ['faca',['Você não come do prato com as mãos, correto?'],6,1,1],
'tool_magnifying_glass': ['lupa',['Use para observar coisas pequenas.'],2,1,1],
'tool_handcuffs': ['algemas',['Use para capturar anomalias e levá-las para pesquisa.'],50,2,1],
'tool_umbrella': ['guarda-chuva',['Não pegue resfriado meu filho!'],800,5,1],
'tool_umbrella_portable': ['guarda-chuva portátil',['Não pegue resfriado meu filho!','Cabe na mochila!'],800,3,1],
'tool_can_opener': ['abridor de lata',['Use para abrir garrafas de vidro e latas em conserva.'],5,1,1],
'tool_syringe': ['seringa',['Use para tirar sangue e aplicar antibióticos.','Sempre lave antes de usar!'],10,1,1],
'tool_asthma_inhaler': ['bombinha',['Não se esqueça de usar quando sentir','falta de ar.'],10,1,1],
   
#MELEE WEAPONS (name,description,price,volume,weight,{damage})
'melee_broom': ['vassoura',['Não foi feita para se armar, muito menos','para caçar ou voar, mas funciona.'],10,5,2,{'DAMAGE': 2,'RECHARGE': 2,'CADENCY': 50}],
'melee_walking_stick': ['bengala',['Pessoas mais velhas usam isso como','terceira perna, mas pode ser uma boa arma.'],1,1,1,{'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}],
'melee_boomerang': ['bumerangue',['Você sabia que isso era usado para quebrar','pescoços de cangurus?'],30,2,1,{'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}],
'melee_stick': ['galho',['No meio do mato, qualquer coisa pode','virar uma arma.'],1,2,2,{'DAMAGE': 3,'RECHARGE': 2,'CADENCY': 50}],
'melee_frying_pan': ['frigideira',['Se não tiver o que usar, ela quebra um galho','e ainda frita um ovo legal.'],30,3,2,{'DAMAGE': 4,'RECHARGE': 2,'CADENCY': 50}],
'melee_spanner': ['chave inglesa',['Pode ser usada para girar porcas, mas','você a usa para espancar.'],10,3,3,{'DAMAGE': 5,'RECHARGE': 2,'CADENCY': 50}],
'melee_bottle': ['garrafa de vidro',['Depois de um drink moderado','é excelente para tacar na cabeça de um nazi.'],10,3,3,{'DAMAGE': 6,'RECHARGE': 2,'CADENCY': 50}],
'melee_bar': ['barra de ferro',['Dá na telha pra descer','o cacete em alguém.'],4,3,3,{'DAMAGE': 8,'RECHARGE': 2,'CADENCY': 50}],
'melee_scissors': ['tesoura',['Para cortar papel, plástico, pano','e tecido muscular.'],10,2,1,{'DAMAGE': 2,'RECHARGE': 2,'CADENCY': 50}],
'melee_stiletto': ['estilete',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],20,2,1,{'DAMAGE': 5,'RECHARGE': 2,'CADENCY': 50}],
'melee_knife': ['faca',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],300,2,1,{'DAMAGE': 10,'RECHARGE': 2,'CADENCY': 50}],
'melee_scalpel': ['bisturi',['Altamente letal e perfurante, mas obviamente','ele só é utilizado em prol da medicina, certo?.'],800,2,1,{'DAMAGE': 20,'RECHARGE': 2,'CADENCY': 50}],
'melee_fishmonger': ['peixeira',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],500,4,3,{'DAMAGE': 13,'RECHARGE': 2,'CADENCY': 50}],
'melee_cleaver': ['cutelo',['Foi feita para cortar ossos de carnes, mas','serve como uma boa arma também.'],700,3,2,{'DAMAGE': 16,'RECHARGE': 2,'CADENCY': 50}],
'melee_katana': ['katana',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],1000,4,3,{'DAMAGE': 18,'RECHARGE': 2,'CADENCY': 50}],
'melee_whip': ['chicote',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],500,3,3,{'DAMAGE': 14,'RECHARGE': 2,'CADENCY': 50}],
'melee_taser': ['taser',['Porque um verdadeiro meliante','não mata, causa dor.'],1500,1,3,{'DAMAGE': 8,'RECHARGE': 2,'CADENCY': 50}],
'melee_cursedknife': ['faca amaldiçoada',['Uma faca com uma terrível maldição','de transformar tudo o que corta em bolo.'],300,2,1,{'DAMAGE': 10,'RECHARGE': 2,'CADENCY': 50}],

#WEAPONS (name,description,price,volume,weight,{damage,recharge,cadency,capacity,gauge})
'gun_bow': ['arco',['Uma arma de longa distância e velha moda.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 5, 'GAUGE': 0}],
'gun_crossbow': ['besta',['Uma arma de longa distância e velha moda.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 5, 'GAUGE': 0}],
'gun_revolver.12': ['revólver.12',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 12.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 12}],
'gun_revolver.16': ['revólver.16',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 16.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 16}],
'gun_revolver.22': ['revólver.22',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 22.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 22}],
'gun_revolver.32': ['revólver.32',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 32.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 32}],
'gun_revolver.38': ['revólver.38',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 38.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}],
  
'gun_pistol': ['pistola',['Arma de fogo para ataques de média distância, ela usa munição de calibre 38.'],2500,3,2,{'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 3, 'CAPACITY': 16}],
  
'gun_UZI.22': ['Uzi .22',['Arma de fogo para ataques de média distância.'],4000,3,2,{'DAMAGE': 4, 'RECHARGE': 1, 'CADENCY': 20, 'CAPACITY': 10, 'GAUGE': 22}],
'gun_UZI.45': ['Uzi .45',['Arma de fogo para ataques de média distância.'],4000,3,2,{'DAMAGE': 4, 'RECHARGE': 8, 'CADENCY': 1, 'CAPACITY': 16, 'GAUGE': 45}],
  
'gun_shotgun.12': ['espingarda .12',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 12.'],5000,4,3,{'DAMAGE': 5, 'RECHARGE': 4, 'CADENCY': 4, 'CAPACITY': 6, 'GAUGE': 12}],
'gun_carbine': ['carabina',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 8, 'CAPACITY': 3, 'GAUGE': 16}],
  
'gun_sniper': ['sniper',['Arma de fogo para ataques de curta distância,','ela usa munição de calibre 16.'],6000,5,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}],
'gun_shotgun': ['escopeta',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],4000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}],
  
'gun_assault_riffle': ['fuzil de assalto',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],4000,5,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 3, 'GAUGE': 16}],
'gun_rifle': ['fuzil',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],5000,5,3,{'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 16, 'GAUGE': 16}],
'gun_AK-47': ['AK-47',['Fuzil para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 20, 'GAUGE': 39.0}],
'gun_M16': ['M16',['Fuzil para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 6, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 30, 'GAUGE': 5.56}],
  
'gun_RPG-7': ['RPG-7',['Bazuca utilizada contra tanques.'],12000,7,5,{'DAMAGE': 50, 'RECHARGE': 10, 'CADENCY': 0, 'CAPACITY': 1, 'GAUGE': 0}],
   
#GRENADES (name,description,price,volume,weight,{damage,type})
'grenade': ['granada',['Use numa batalha para causar dano á todos os inimigos na tela.'],100,2,3,{'DAMAGE': 30,'TYPE': 1}],
'grenade_smoke': ['granada de fumaça',['Use numa batalha para que todos os inimigos percam AGILIDADE.'],200,2,3,{'DAMAGE': 13,'TYPE': 2}],
'grenade_flash': ['granada de luz',['Use numa batalha para que todos os inimigos percam sua vez.'],500,3,3,{'DAMAGE': 15,'TYPE': 3}],
'grenade_molotov_cocktail': ['coquetel molotov',['Use numa batalha para causar dano á todos os inimigos','e possivelmente queimá-los.'],40,3,1,{'DAMAGE': 12,'TYPE': 1}],

#BATTLE (name,description,price,volume,weight,{damage,type})
'pepper_spray': ['spray de pimenta',['Use numa batalha para atordoar um inimigo.'],40,3,1],
'horn': ['buzina',['Use numa batalha para atordoar um inimigo.'],40,3,1],
'extinguisher': ['extintor',['Use num caso de emergência.','...até pra jogar num bulldogue.'],40,4,30],
'rope': ['corda',['Use em batalhas para prender seus oponentes','ou dentro de cavernas para descer e subir'],70,4,1],

#DRUGS (name,description,price,volume,weight,condition)
'drug_antibiotic': ['antibiótico',['Use para infeccionar feridas letais e impedir hemorragias, parando de consumir a barra de HP.'],25,2,1,0],
'drug_syrup': ['xarope',['Remédio utilizado para combater resfriados e alergias.'],10,2,1,0],
'drug_tablets': ['comprimidos',['Remédios utilizados para combater náusea.'],30,1,1,0],
'drug_pills': ['pílulas',['Remédios utilizados para combater dor muscular.'],40,1,1,0],
'drug_paracetamol': ['paracetamol',['Medicamento para combater a febre.'],40,2,1,0],
'drug_desloratadin': ['desloratadina',['Medicamento para combater a tontura.'],40,2,1,0],
'drug_pseudoefedrin': ['pseudoefedrina',['Medicamento para combater o resfriado.'],40,2,1,0],
'drug_ibuprofen': ['ibuprofeno',['Medicamento para combater o resfriado e a febre.'],40,2,1,0],
'drug_ciprofloxacin': ['ciprofloxacino',['Antibiótico útil contra conjutivite,','resfriado e febre.'],40,2,1,0],
   
'serum_antiscorpionic': ['soro antiescorpiônico',['Antídoto para combater veneno de escorpiões.'],40,2,1,0],
'serum_antivenom': ['soro antiofídico',['Antídoto para combater veneno de cobras.'],40,2,1,0],
'serum_antiarachnid': ['soro antiaracnídico',['Antídoto para combater veneno de aranhas.'],40,2,1,0],
 
'drug_adrenaline': ['adrenalina',['Remédio utilizado para reviver uma pessoa inconsciente.'],60,2,1,0],
'cigar': ['maço de cigarro',['Use isso pra arregaçar seu sistema respiratório.'],10,2,1,0],

#CONDIMENTS (name,description,price,volume,weight,type,duration)
'condiment_ketchup': ['ketchup',['Condimento muito usado em salgados.'],5,1,1,0,'0100'],
'condiment_mayonnaise': ['maionese',['Condimento muito usado em salgados.'],5,1,1,0,'0100'],
'condiment_sugar': ['açúcar',['Condimento muito usado em doces.'],5,1,1,1,'0100'],
'condiment_sweetener': ['adoçante',['Condimento muito usado em doces.'],5,1,1,1,'0100'],
'condiment_salt': ['sal',['Condimento muito usado em refeições.'],5,1,1,2,'0100'],
'condiment_pepper': ['pimenta',['Condimento muito usado em refeições.'],5,1,2,6,'0100'],
'condiment_olive_oil': ['azeite',['Condimento muito usado em refeições.'],5,1,2,6,'0100'],
'condiment_vinegar': ['vinagre',['Condimento muito usado em refeições.'],5,1,2,6,'0100'],
'condiment_oregan': ['orégano',['Condimento muito usado em salgados.'],5,1,0,6,'0100'],
'condiment_shoyu': ['shoyu',['Condimento muito usado em refeições.'],5,1,2,6,'0100'],

#DRINK (name,description,price,volume,weight,health,thirst,duration,trash)
'drink_water': ['água',['O básico pra te manter de pé','no calor e no cansaço. BEBA ÁGUA!'],8,2,1,10,10,'0100','plastic_bottle'],
'drink_water_gas': ['água com gás',['Certas pessoas preferem beber água','desse jeito.'],8,2,1,10,10,'0100','plastic_bottle'],
'drink_juice_orange': ['suco de laranja',['Saudável e nutritivo, o Jailson aprova.'],8,3,1,12,10,'0100','box'],
'drink_juice_passion_fruit': ['suco de maracujá',['Saudável e nutritivo, acalma a alma e o espírito.'],8,3,1,12,10,'0100','box'],
'drink_coffee': ['café',['Bebida que aumenta a sua energia.'],8,3,1,8,10,'0100','cup'],
'drink_chocolate': ['chocolate quente',['Vai bem com biscoitos'],8,3,1,6,10,'0100','cup'],
'drink_milk': ['leite',['Vai bem no café.'],8,3,1,6,10,'0100','box'],
'drink_coffeenmilk': ['café com leite',['Bebida preferida do criador','do jogo, foi muito útil.'],8,3,1,10,10,'0100','cup'],
'drink_energy': ['energético',['Bebida que acelera o metabolismo','e aumenta a energia.'],8,3,1,10,10,'0100','can'],
'drink_cola': ['refri',['A bomba calórica que a gente gosta.'],8,3,1,5,10,'0100','can'],
'drink_guarana': ['guaraná',['Um suquinho barato e muito açúcarado','mas é bom, não confundir com cachos de olhos.'],8,3,1,5,10,'0100','can'],
'drink_beer': ['cerveja',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,8,10,'0100','bottle'],
'drink_whiskey': ['uísque',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,8,10,'0100','bottle'],
'drink_yogurt': ['iogurte',['Delicioso e saudável.'],8,3,1,8,10,'0100','cup'],

#WASTED DRINK (name,description,price,volume,weight,health,thirst,duration)
'drink_water_wasted': ['água quente',['O básico pra te manter de pé','no calor e no cansaço. BEBA ÁGUA!'],8,2,1,10,10,'0100'],
'drink_water_gas_wasted': ['água com gás quente',['Certas pessoas preferem beber água','desse jeito.'],8,2,1,10,10,'0100'],
'drink_juice_orange_wasted': ['suco de laranja quente',['Saudável e nutritivo, o Jailson aprova.'],8,3,1,12,10,'0100'],
'drink_juice_passion_fruit_wasted': ['suco de maracujá quente',['Saudável e nutritivo, acalma a alma e o espírito.'],8,3,1,12,10,'0100'],
'drink_coffee_wasted': ['café frio',['Bebida que aumenta a sua energia.'],8,3,1,8,10,'0100'],
'drink_chocolate_wasted': ['chocolate frio',['Vai bem com biscoitos'],8,3,1,6,10,'0100'],
'drink_milk_wasted': ['leite',['Vai bem no café.'],8,3,1,6,10,'0100'],
'drink_coffeenmilk_wasted': ['café com leite frio',['Bebida preferida do criador','do jogo, foi muito útil.'],8,3,1,10,10,'0100'],
'drink_energy_wasted': ['energético quente',['Bebida que acelera o metabolismo','e aumenta a energia.'],8,3,1,10,10,'0100'],
'drink_cola_wasted': ['refri sem gás',['A bomba calórica que a gente gosta.'],8,3,1,5,10,'0100'],
'drink_guarana_wasted': ['guaraná sem gás',['Um suquinho barato e muito açúcarado','mas é bom, não confundir com cachos de olhos.'],8,3,1,5,10,'0100'],
'drink_beer_wasted': ['cerveja quente',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,8,10,'0100'],
'drink_whiskey_wasted': ['uísque quente',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,8,10,'0100'],
'drink_yogurt_wasted': ['iogurte estragado',['Delicioso e saudável.'],8,3,1,8,10,'0100'],
 
#FOOD (name,description,price,volume,weight,health,hunger,duration,trash)
'food_burger': ['hamburguer',['É bom quando está passeando e quer','tomar alguma coisa.'],15,2,2,30,10,'0300',None],
'food_hotdog': ['cachorro quente',['Hot dog sua bunda.'],15,2,2,30,10,'0300',None],
'food_popcorn': ['pipoca',['Você falou em pipoca?'],15,2,2,30,10,'0300',None],
'food_popcorn_candy': ['pipoca doce',['Você falou em pipoca?'],15,2,2,30,10,'0300',None],
'food_churros': ['churros',['Churros, olha o churros.'],15,2,2,30,10,'0300',None],
'food_ice_cream_chocolate': ['sorvete de chocolate',['É bom quando está passeando e quer','tomar alguma coisa.'],15,2,2,30,10,'0300',None],
'food_ice_cream_vanilla': ['sorvete de baunilha',['É bom quando está passeando e quer','tomar alguma coisa.'],15,2,2,30,10,'0300',None],
'food_ice_cream_mixed': ['sorvete misto',['É bom quando está passeando e quer','tomar alguma coisa.'],15,2,2,30,10,'0300',None],
'food_orange': ['laranja',['Fruta fácil de se achar','num pomar.'],3,1,1,2,10,'0100',None],
'food_fish': ['pirarucu',['Peixe de água doce.'],3,1,1,2,10,'0100',None],
'food_bread': ['pão',['O alimento matinal de cada dia.'],15,2,2,30,10,'0300',None],
'food_pedemoleque': ['pé de moleque',['Doce de amendoim, fácil de encontrar em padarias.'],1,1,1,2,10,'0100','packing'],
'food_peanut_candy': ['paçoca',['Doce de amendoim, fácil de encontrar em padarias.'],1,1,1,2,10,'0100','packing'],
'food_coconut_candy': ['cocada',['Doce de côco, fácil de encontrar em padadias.'],1,1,1,2,10,'0100','packing'],
'food_coxinha': ['coxinha',['Salgado feito com massa frita e recheada com frango, fácil de','encontrar em lanchonetes.'],5,2,1,8,10,'0100',None],
'food_pastry': ['pastel',['Salgado feito com massa frita e recheado com queijo.'],3,2,1,5,10,'0100',None],
'food_puff_pastry': ['pastel folheado',['Salgado feito com várias camadas de massa e queijo.'],6,2,1,12,10,'0100',None],
'food_brigadeiro': ['brigadeiro',['Doce de chocolate.'],2,1,1,3,10,'0100',None],
'food_cheese_bread': ['pão de queijo',['Salgado feito com massa de queijo.'],5,1,1,7,10,'0100',None],
'food_pudding': ['pudim',['Doce feito com leite condensado.'],10,3,1,15,10,'0300',None],
'food_cake_corn': ['bolo de fubá',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,10,'0500',None],
'food_cake_carrot': ['bolo de cenoura',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,10,'0500',None],
'food_cake_chocolate': ['bolo de chocolate',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,10,'0500',None],
'food_packed_lunch': ['marmita',['Tem muitas coisas diferentes dentro, além de ser bem nutritivo!'],15,3,2,30,10,'0300',None],
'food_egg': ['ovo',['Ele te deixa forte pra enfrentar qualquer perigo.'],15,2,2,30,10,'0300',None],
'food_lamen_chicken': ['miojo de galinha',['O macarrão instantâneo','do cara que mora sozinho.'],15,2,2,30,10,'0300','packing'],
'food_lamen_meat': ['miojo de carne',['O macarrão instantâneo','do cara que mora sozinho.'],15,2,2,30,10,'0300','packing'],
'food_cookie_chocolate': ['bolacha de chocolate',['Biscoito recheado sempre','foi chamado assim.'],15,2,2,30,10,'0300','cookie_packing'],
'food_cookie_strawberry': ['bolacha de morango',['Biscoito recheado sempre','foi chamado assim.'],15,2,2,30,10,'0300','cookie_packing'],
'food_snack_onion': ['salgadinho de cebola',['50% do saco é de puro vento.'],15,2,2,30,10,'0300','snack_packing'],
'food_snack_cheese': ['salgadinho de queijo',['50% do saco é de puro vento.'],15,2,2,30,10,'0300','snack_packing'],
'food_snack_creammycheese': ['salgadinho de requeijão',['50% do saco é de puro vento.'],15,2,2,30,10,'0300','snack_packing'],
'food_pizza_mussarella': ['pizza de mussarela',['Quem não gosta de pizza?'],15,2,2,30,10,'0300','pizza'],
'food_pizza_shaggy': ['pizza de calabresa',['Quem não gosta de pizza?'],15,2,2,30,10,'0300','pizza'],
'food_pizza_chicken': ['pizza de frango',['Quem não gosta de pizza?'],15,2,2,30,10,'0300','pizza'],
'food_pizza_4cheese': ['pizza de 4 queijos',['Quem não gosta de pizza?'],15,2,2,30,10,'0300','pizza'],
'food_soup': ['sopa',['Nutritivo e quentinho, pode ser feiti de','qualquer coisa.'],10,2,2,40,15,'0300',None],
'food_soup_monkey': ['sopa de macaco',['Sopa de macaco.'],10,2,2,40,15,'0300',None],

#WASTED FOOD (name,description,price,volume,weight,health)
'food_coxinha_wasted': ['coxinha fria',['Não é mais tão gostosa quanto antes,','mas é comestível.'],2,1,1,4,10],
'food_peanut_candy_wasted': ['paçoca esfarelada',['O que antes era um doce maravilhoso','agora são apenas migalhas...'],2,1,1,1,10],
'food_egg_wasted': ['ovo podre',['ALGUÉM DESTRUIU O MEU OVO'],15,2,2,30,10],
'food_pizza_chicken_wasted': ['pizza de frango fria',['Tá gelada e sem gosto.'],15,2,2,10,3,'pizza'],

#INGREDIENTS (name,description,price,volume,weight)
'ingredient_ectoplasm': ['ectoplasma',['Uma estranha gosma branca, comum em','invocações de espíritos.'],1,1,1,2],
'ingredient_eyefeather': ['pena ocular',['Uma pena de pavão com um','olho laranja na ponta.'],1,1,1,2],
'ingredient_sickle_beak': ['bico de foice',['Um bico com formato de','foice, pode ser usado como arma.'],1,1,1,2],
'ingredient_hammer_beak': ['bico de martelo',['Um bico com formato de','martelo, pode ser usado como arma.'],1,1,1,2],
'ingredient_eye': ['olho',['Um glóbulo ocular.'],1,1,1,2],
'ingredient_crab_claw': ['garra de caranguejo',['Um garra de caranguejo pontuda e afiada.'],1,1,1,2],
'ingredient_ox_horn': ['Chifre de boi',['Um material resistente e duro como osso.'],1,1,1,2],

#UTENSILS (name,description,price,volume,weight)
'utn_cup': ['prato',['Objeto arremessável.'],1,1,1,2],
'utn_plate': ['prato',['Objeto arremessável.'],1,1,1,2],
 
#TRASH (name,description,price,volume,weight)
'trash_packing': ['embalagem',['Um papel que não serve pra absolutamente nada','a menos que seja uma esponja amarela.'],8,1,1],
'trash_cookie_packing': ['embalagem de biscoito',['Um papel que não serve pra absolutamente nada','a menos que seja uma esponja amarela.'],8,1,1],
'trash_snack_packing': ['embalagem de salgadinho',['Um papel que não serve pra absolutamente nada','a menos que seja uma esponja amarela.'],8,1,1],
'trash_bottle': ['garrafa de vidro',['Um item meio perigoso de se levar','nas suas costas,','sabe-se lá o que pode fazer com isso'],8,2,1],
'trash_plastic_bottle': ['garrafa plástica',['Se você não jogar no lixo, não','faz idéia do dano que vai fazer.'],8,2,1],
'trash_can': ['latinha',['Um latinha que poderia ser usada','para brincar de bola.'],8,2,1],
'trash_pizza': ['caixa de pizza',['Uma caixa que um dia tinha uma coisa','muito gostosa dentro.'],8,2,1],
'trash_box': ['caixa',['Ás vezes é o que você mais precisa','pra um trabalho escolar.'],8,1,1],
'trash_cup': ['copo descartável',['Quem nunca ficou cortando as tiras','como uma água viva.'],8,1,1],
   
#KEY ITEMS (name,description,price,volume,weight)
'key': ['chave',['Use para abrir portas pelo labirinto!.'],10,1,1],
'key_bedroom': ['chave do quarto',['Se perder vai ficar sem caminha.'],10,1,1],
'key_chest': ['chave de baú',['Use para abrir um compartimento.'],10,1,1],
'key_vehicle': ['chave do veículo',['É o que põe o motor pra funcionar.'],10,1,1],
'key_park': ['chave do parque',['Ela serve pra entrar no parque nacional','onde você achou é outra história.'],10,1,1],
'key_lab': ['chave do laboratório',['Que honra ter as chaves do laboratório Fiocruz!'],10,1,1],
'key_office': ['chave do escritório',['Um homem simpático que deu','ele quer mesmo é ver o circo pegar fogo.'],10,1,1],
'key_cave': ['signo de mercúrio',['Uma placa de ferro com a inscrição','de mercúrio... estranho'],10,1,1],
'dungeon_key': ['chave',['Use dentro de instalações para abrir caminhos.'],10,1,1],
   
#DOCUMENTS (name,description,price,volume,weight)
'id_card0': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,0],
'id_card1': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,1],
'id_card2': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,2],
'id_card3': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,3],
'id_card4': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,4],
'id_card5': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1,5],
'newspaper': ['jornal semanal',['Para receber as notícias da semana.'],5,1,1],

#DEVICES (name,description,price,volume,weight,GUI)
'phone': ['celular',['Mais importante que o cartão só o celular, pode ser usado para fazer','chamadas e receber emails, mas lembre-se de recarregar.'],100,1,1,0],
'phone_lantern': ['celular com lanterna',['Além de tudo o que um celular faz,','você pode usá-lo para enxergar no escuro.'],200,1,1,0],
'PDA': ['PDA',['Com este dispositivo, você pode fazer coisas','além do celular, como acessar a internet.'],200,1,1,1],
'charger': ['carregador',['Use para carregar seu celular.'],40,1,1],
'portable_charger': ['carregador portátil',['Use para carregar seu celular.'],100,1,1],
'headphone_cheap': ['fone de ouvido barato',['Ao obter um, você consegue escutar o rádio do celular, mas atenção! ele quebra nos momentos mais inesperados.'],20,1,1],
'headphone_expensive': ['fone de ouvido caro',['Ao obter um, você consegue escutar o rádio do celular.','Bem mais resistente que fones de ouvido baratos.'],60,1,1],
'simcard1': ['cartão SIM IO',['Insira dentro de um celular para','fazer chamadas e acessar a internet.'],10,1,1],
'simcard2': ['cartão SIM MIMO',['Insira dentro de um celular para','fazer chamadas e acessar a internet.'],10,1,1],
'simcard3': ['cartão SIM SIM',['Insira dentro de um celular para','fazer chamadas e acessar a internet.'],10,1,1],
'simcard4': ['cartão SIM FALO',['Insira dentro de um celular para','fazer chamadas e acessar a internet.'],10,1,1],
'sdcard': ['cartão SD',['Para guardar músicas salvas.'],60,1,1],
'GPS': ['GPS',['Este dispositivo super tecnológico serve para','apontar sua localização e mostrar o mapa da região.'],200,1,1],
'camera': ['camera digital',['Serve para tirar fotos e guardar de recordação.'],200,1,1],
'mp3': ['tocador mp3',['Útil para escutar rádio e música.'],200,1,1],
'brickgame': ['brick game',['Não faz mal se descontrair com 99 jogos.'],20,1,1],
'flashlight': ['lanterna',['Use para enxergar no escuro.'],60,1,1],
'nightvision': ['visão noturna',['Use para enxergar no escuro.'],200,1,1],
'binoculars': ['binóculos',['Use para enxergar mais além.'],100,1,1],
'sonar': ['sonar',['Use para detectar a presença de anomalias.'],500,2,1],
'batteries': ['pilhas',['A fonte de energia de vários aparelhos eletrônicos.'],10,1,1],

#GAMING (name,description,price,volume,weight,GUI)
'playingcards': ['cartas de baralho',['Use para jogar vários jogos de baralho.'],10,1,1,0],
'dominoes': ['dominó',['Pode usar tanto pra montar castelinhos e trilhas','quanto pra jogar com os amigos.'],10,2,1,0],
'chess_board': ['tabuleiro de xadrez',['Use para jogar o jogo das pessoas de estratégia.'],50,3,2,0],
'ouija_board': ['tabuleiro ouija',['Um instrumento sério de contatação espiritual','que virou brinquedo graças ao capitalismo.'],50,3,1,0],

#INSTRUMENTS (name,description,price,volume,weight,{type})
'instrument_acousticguitar': ['violão acústico',['Um belo instrumento musical.'],300,7,3,{'TYPE': 0}],
'instrument_electricguitar': ['guitarra elétrica',['Um belo instrumento musical.'],300,7,4,{'TYPE': 1}],
'instrument_bassguitar': ['baixo',['Um belo instrumento musical.'],300,7,4,{'TYPE': 2}],
'instrument_flute': ['flauta',['Um belo instrumento musical.'],50,2,1,{'TYPE': 3}],
'instrument_ocarina': ['ocarina',['Um belo instrumento musical.'],50,1,1,{'TYPE': 4}],
'instrument_harmonica': ['gaita',['Um belo instrumento musical.'],50,1,1,{'TYPE': 5}],
'instrument_tambourine': ['tamborim',['Um belo instrumento musical.'],50,1,1,{'TYPE': 6}],
'instrument_bongo': ['bongô',['Um belo instrumento musical.'],50,1,1,{'TYPE': 7}],
'instrument_maracas': ['maracas',['Um belo instrumento musical.'],50,1,1,{'TYPE': 8}],

#PILLS (name,description,price,volume,weight,type)
'pill_strenght': ['suplemento de força',['Aumenta a FORÇA permanentemente em +10.'],500,1,1,0],
'pill_agility': ['suplemento de agilidade',['Aumenta a AGILIDADE permanentemente em +10.'],500,1,1,1],
'pill_resistance': ['suplemento de resistência',['Aumenta a RESISTÊNCIA permanentemente em +10.'],500,1,1,2],
'pill_knowledge': ['suplemento de sabedoria',['Aumenta a SABEDORIApermanentemente em +10.'],500,1,1,3],
'pill_charisma': ['suplemento de carisma',['Aumenta o CARISMA em +10'],500,1,1,4],
'pill_mistery': ['suplemento misterioso',['Aumenta um atributo aleatório'],500,1,1,5],

#REPELLENTS (name,description,price,volume,weight,duration)
'repellent1': ['repelente básico',['Evita anomalias de aparecer por 10 minutos.'],50,2,1,600],
'repellent2': ['super repelente',['Evita anomalias de aparecer por 30 minutos.'],100,2,1,1800],
'repellent3': ['ultra repelente',['Evita anomalias de aparecer por 60 minutos.'],250,2,1,3600],

#ACESSORIES (name,description,price,volume,weight,type)
'aim1': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,1],
'aim2': ['mira 2',['Customiza a mira de sua arma.'],200,1,1,2],
'aim3': ['mira 3',['Customiza a mira de sua arma.'],200,1,1,3],
'aim4': ['mira 4',['Customiza a mira de sua arma.'],200,1,1,4],
'aim5': ['mira 5',['Customiza a mira de sua arma.'],200,1,1,5],
 
'acc_silencer': ['silenciador',['Aumenta o ATAQUE de uma pistola.'],200,1,1,1],
'acc_cartridge': ['cartucho extra',['Aumenta a capacidade da arma.'],100,1,1,2],
'acc_gun_butt': ['coronha',['Aumenta a AGILIDADE da arma.'],100,1,1,3],
'acc_bandolier': ['bandoleira',['Adiciona um espaço extra no inventário.'],100,1,1,3],

#CRAFTING (name,description,price,volume,weight)
'craft_spring_small': ['mola pequena','',0,1,1],
'craft_fuel': ['combustível','',0,1,1],
'craft_cloth': ['pano','',0,1,1],
'craft_powder': ['pólvora','',0,1,1],

#CAMPING (name,description,price,volume,weight,amount,sleep)
'air_pump': ['bomba de ar',['Para encher um colchão inflável.'],30,3,1],
'bed_single': ['colchão inflável de solteiro',['Caso precise passar a noite na mata.'],50,2,1,1,2],
'bed_couple': ['colchão inflável de casal',['Caso precise passar a noite na mata.'],70,2,1,2,2],
'tent_small': ['barraca pequena',['Caso precise passar a noite na mata.'],100,2,1,1,3],
'tent_medium': ['barraca média',['Caso precise passar a noite na mata.'],100,2,1,2,3],
'tent_big': ['barraca grande',['Caso precise passar a noite na mata.'],100,2,1,3,3],

#TRAPS (name,description,price,volume,weight,size)
'cage_small': ['gaiola pequena',['Para capturar anomalias de pequeno porte.'],50,2,1,1],
'cage_big': ['gaiola grande',['Para capturar anomalias de grande porte.'],80,2,1,2],

#MONEY (name,description,price,volume,weight)
'USD': ['dólar americano',['Surgiu em 1992 com o governo de Itamar Franco.'],1.0,0,0],
'BRL': ['real brasileiro',['Surgiu em 1992 com o governo de Itamar Franco.'],2.0,0,0],
'EUR': ['euro',['Surgiu em 1992 com o governo de Itamar Franco.'],0.85,0,0],
'creditcard1': ['cartão BB',['Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!'],0,1,1],
'creditcard2': ['cartão Uati',['Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!'],0,1,1],
'creditcard3': ['cartão Faixa',['Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!'],0,1,1],
'creditcard4': ['cartão Cabresto',['Um item muito necessário na vida de um jovem adulto, use nos caixas de banco, nem imagine em jogar fora!'],0,1,1],

#TREASURES (name,description,price,volume,weight,type)
'treasure_vase': ['vaso marajoara',['Um antigo vaso indígena feita da cerâmica do marajó.'],2000,3,3,0],
 
'jewel_emerald': ['esmeralda',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_diamond': ['diamante',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_ruby': ['rubi',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_amethyst': ['ametista',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_sapphire': ['safira',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_opal': ['opala',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_gold': ['ouro',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_quartz': ['quartzo',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'mysterious': ['???',['Você não faz idéia do que é isso.'],0,1,1,0],
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
 
NEWS = {
'01/01': [
[['Polícia Municipal abre a renovação da carteira'],'Tereza Rocha',['Em 4 de abril, a Polícia Municipal abriu a renovação da carteira para mercenários. A carteira de identificação de Mercenário é \
obrigatória não só por identificação, mas por questões de segurança, depois que a câmara dos deputados aprovou a reforma armamentista, qualquer cidadão com a identificação de mercenário é livre para portar \
e possuir uma arma de fogo.','',' Recentemente, houveram vários casos de assassinatos não registrados pela polícia, pela incapacidade da polícia de analisar todos os casos separadamente, mercenários tem sido \
recompensados para cuidar desses assassinatos misteriosos.','','Devido a isso os dados de homicídio por armas de fogo aumentaram consideravelmente no estado, isso se deve á facilidade de se obter uma arma e também de \
reduzir a pena de um criminoso para servir ao estado como mercenário. O criminólogo Mauro Fidélis fala sobre a situação.','','"O que a polícia do rio de janeiro fez foi um ato irresponsável e inpensável, pois \
graças á essa facilidade de se armar, vários criminosos podem se aproveitar e utilizá-las para fins maliciosos, e mesmo com tantos casos de homicídios não registrados, o que custava a polícia recrutar mais policiais ou \
fazer uma investigação profunda e mais elaborada á respeito?"','','Sabendo disso, tudo o que podemos esperar é que os mercenários façam bom uso de seu poder bélico.']]
],
 
'01/01': [
[['Parque Nacional do Itatiaia é invadido'],'Jéssica Ramone',['Na tarde do dia anterior, um','caso que deixou autoridades','em estado de alerta, foram','filmadas imagens de vândalos',
'invadindo o parque nacional.','','"não é o que se espera','dessa juventude, não é?", diz','Marcelo Marinho, fiscal do','IBAMA e principal supervisor','do parque','',
'O Parque Nacional do Itatiaia','é uma área de preservação','da fauna brasileira protegida','por lei, pois é onde se','encontra o que resta da','mata atlântica, que vem','sofrendo drásticas degradações',
'com o tempo.','','Mas o maior desafio do','parque não são os vândalos,','mas sim os mercenários,','vários invadem locais restritos','atrás das presas e do','dinheiro, colocando em risco',
'a fauna e a flora da','natureza. A PRF já','possui conhecimento de tais','atos ediondos.','','"É lamentável, a gente pensa','que confia mas eles','só mostram que estamos',
'se enganando", diz Paulo Sousa','','O IBAMA, instituição','responsável pelo monitoramento','do parque, emitiu uma nota','avisando que irão reforçar','a segurança no local,',
'policiais militares armados','e cães de guarda são','apenas um pouco do','que os mercenários podem','temer de agora em','diante.']]
],
 
'01/01': [
[['Relato de assombração em Itatiaia pode ser verdadeiro'],'Jéssica Ramone',['Ás 11:30 da noite passada,','moradores de Itatiaia relataram','um caso incomum entre vários','da polícia, \
foi registrado um','caso de uma assombração','(vulgo Poltergeist) na casa de','Maria Elisângela das Dores,','35 anos.','','"Não sabia o que fazer, eu nunca','imaginei que assombrações\
 ou','fantasmas realmente existissem,','sempre achei que eram apenas','contos de criança.", diz','Maria Elisângela.','','Apesar de inesperado e muito','estranho, o relato foi comprovado','\
por filmagens do Departamento','de Detenção de Anomalias de','Itatiaia, além dos danos','causados pela assombração na','casa e nos moradores da região.','','Aparentemente este não é o','\
único relato de moradores a','respeito de uma assombração,','foram registrados 5 relatos em','um único mês e 12 em 3 meses, mas','se as investigações persistirem','este pode ser o \
primeiro','relato confirmado de uma','assombração no país.']],
[['Engarrafamento na zona sul'],'Gisele Peres',['Muito trânsito']]
],

'01/01': [
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
]
}

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

TUTORIALS = {
'BEGIN': [1,' - para cima',0,2,' - para baixo',0,5,' - selecionar',0,6,' - voltar',['phone',17]],
'WALK': ['Pressione os botões',0,1,2,3,4,' para andar',['wait',100,'RUN']],
'RUN': ['Pressione ',6,' para',0,'correr'],
'CLIFFS': ['Você pode pular de precipícios,',0,'Mas não pode subir por eles.'],
'SWIM': ['Você pode nadar nas águas'],
'NOTIFICATION': ['Você recebeu uma notificação,',0,'sempre que receber uma',0,'verifique seu celular',['wait',100,'PHONEI']],
'PHONEI': ['Pegue seu celular',0,'apertando ',8,['phone',1,'PHONEII']],
'PHONEII': ['Aqui é seu menu principal,',0,'sempre que precisar de',0,'ferramentas importantes,',0,'abra seu celular',['wait',100,'TASKSI']],
'TASKSI': ['Selecione o ícone com',0,'um lápis',0,['image','ph_task'],['phone',9,'TASKSII']],
'TASKSII': ['Aqui ficam suas tarefas,',0,'seus objetivos dentro',0,'do jogo'],
'INVENTORY': ['Pressione ',7,' para abrir',0,'o inventário'],
'SIGNALI': ['Seu sinal de telefone está',0,'ruim, você precisa de sinal',0,'para utilizar certos aplicativos','no seu celular.',['wait',100,'SIGNALII']],
'SIGNALII': ['Vá para o lado de fora',0,'da casa para ter um',0,'sinal melhor!'],
'NEWSI': ['Seu sinal já está melhor,',0,'agora você pode ver as',0,'notícias no seu celular',['wait',100,'NEWSII']],
'NEWSII': ['Selecione o ícone com',0,'um globo',0,['image','ph_news'],['phone',5,'NEWSIII']],
'NEWSIII': ['Aqui você fica por dentro',0,'do que está acontecendo',0,'no mundo do jogo.'],
'DRIVING': [3,' - esquerda',0,4,' - direita',0,2,' - frear',0,1,' - sair do veículo'],
'FUEL': ['Você precisa abastecer',0,'Para continuar dirigindo,',0,'Senão você não pode',0,'mais dirigir.'],
'INVENTORYI': [3,' - esquerda',0,4,' - direita',0,2,' - frear',0,1,' - sair do veículo'],
'KEYS': ['Parece que essa porta precisa',0,'de uma chave',('Items/it_keybedroom'),0,'procure-a pela casa!'],
}

HINTS = {
'MENUS': [6,'inventário',7,'celular'],
'NPC_DIALOG': [4,'conversar'],
'VEHICLE_USE': [4,'montar'],
'VEHICLE_CONTROLS': [2,'esquerda',3,'direita',5,'acelerar',1,'freiar',0,'desmontar'],
'INVENTORY_ITEMS': [4,'usar',5,'segurar'],
'INVENTORY_HOLD': [4,'juntar',5,'colocar'],
'INVENTORY_ACCESORIES': [5,'tirar'],
'BATTLE_TACTICS': [4,'escolher tática'],
'BATTLE_DIALOG': [4,'dialogar'],
'BATTLE_GUARD': [4,'defender'],
'BATTLE_RUN': [4,'fugir'],
'BATTLE_SHOT': [4,'atacar'],
'PHONE_APPS': [4,'selecionar'],
'PHONE_MAP': [4,'aumentar',5,'diminuir'],
'PHONE_CONTACTS': [4,'selecionar'],
'PHONE_EMAIL': [0,1,'selecionar',4,'ler'],
'PHONE_NEWS': [0,1,'selecionar',4,'ler'],
'PHONE_RADIO': [2,3,'mudar estação',4,'tocar'],
'PHONE_CAMERA': [4,'salvar jogo'],
'PHONE_BESTIARY': [4,'selecionar'],
'PHONE_TASKS': [0,1,'selecionar'],
'PHONE_STATS': [2,3,'olhar personagens'],
'PHONE_TACTICS': [4,'administrar tática'],
'PHONE_ACHIEVEMENTS': [0,1,'selecionar'],
'PHONE_RANKING': [],
'PHONE_MANUAL': [0,1,'selecionar',4,'ler'],
'PHONE_SETTINGS': [4,'selecionar'],
'PHONE_ABOUT': [4,'acessar link'],
'PHONE_CALLING': [4,'atender'],
'PHONE_PHOTO': [4,'fotografar'],
'NAMING': ['digite os nomes no teclado',6,'prosseguir']
}
     
TTSTEXT = {'.': 'ponto',',': 'vírgula',':': 'dois pontos',';': 'ponto e vírgula',' ': 'espaço','!': 'exclamação','?': 'interrogação',
'"': 'aspas duplas',"'": 'aspas','(': 'abre parênteses',')': 'fecha parenteses','[': 'abre colchetes',']': 'fecha colchetes','{': 'abre chaves','}': 'fecha chaves',
'<': 'menor que','>': 'maior que','CAPS1': 'minúscula','CAPS2': 'maíscula','CAPS3': 'caps lock','CONFIRM': 'confirm','DELETE': 'deletar','PAGE': 'página'}

MENU = {'new_file': 'nova sessão','load_file': 'iniciar sessão','save_file': 'salvar sessão','delete_file': 'excluir sessão','resume': 'continuar','exit': 'sair',
'Inventory': 'inventário','volume': 'volume','weight': 'peso','discover': 'Use o item para obter informações.','drop': 'Escolha os itens que deseja descartar.',
'Storage': 'depositar','Products': 'produtos','Basket': 'carrinho','Wash': 'lavar','Mercator': 'Mercador','Trash': 'lixeira',
'armor': 'proteção','duration': 'duração','damage': 'dano','recharge': 'recarga','cadency': 'cadência','capacity': 'capacidade',
'gauge': 'calibre','vitality': 'vitalidade','hunger': 'fome','thirst': 'sede','storage': 'depositar',
'success': 'sucesso','fail': 'falha','touche': 'touché','strike': 'strike','ko': 'nocaute','one_more': 'oitra vez','miss': 'errou...','victory': 'vitória','perfect': 'perfeito','lost': 'derrota','level_up': 'foi promovido para',
'GPS': 'mapa','Contacts': 'contatos','Email': 'emails','Newspaper': 'notícias','Radio': 'música','Camera': 'galeria','Bestiary': 'bestiário','Calendar': 'calendário',
'Tasks': 'tarefas','Status': 'ficha','Tactics': 'táticas','Achievements': 'conquistas','Rank': 'placar','Help': 'ajuda','Settings': 'ajustes','About': 'sobre',
'no_signal': 'sem sinal','no_credit': 'sem saldo','no_freaks': 'nenhuma anomalia registrada','empty': 'nada por aqui','calling': 'chamando',
'to_do': 'fazer','done': 'feitas','all': 'todas','unread': 'novas','read': 'lidas','groups': 'grupos','history': 'histórico',
'name': 'nome','birth': 'data de nascimento','hometown': 'naturalidade','rg': 'registrado','cpf': 'cpf',
'gameplay': 'geral','sound': 'áudio','controls': 'controles',
'lang': 'idioma','border': 'borda','hints': 'dicas','tutorials': 'tutoriais','cursor': 'cursor','dislexic': 'dislexia',
'sfx': 'som','music': 'música','tts': 'narrador','cc': 'áudio descrição','speed': 'velocidade','censorship': 'censura',
'bt_choose': 'escolba o botão','vibrate': 'vibrar',
'conf': 'confirmar','info': 'info','yes': 'sim','no': 'não','ok': 'ok','cancel': 'cancelar',
'Phone': 'celular','PC': 'computador','PDA': 'pda',
'not_email': 'Novo Email','not_contact': 'Novo contato adicionado!','not_wash': 'Sua roupa foi lavada!'}

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