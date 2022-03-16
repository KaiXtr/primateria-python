# -*- coding: utf-8 -*-
import pygame
import resources as res
import os

NAMES = ('Sidney','Barreto','Jane','Oliveira','Renan','Pinheiro','Diego','Donovan','Bianca','Pacheco','Lúcia','Figueiredo',
'Maicon','Neves','Iago','Dantas','Vinícius','Tavares','João','Pedro Lima','Sofia','Torres','Paulo','Sousa','Pietra','Mendonça','Hermes','Fonseca','Ryan','Figueiredo','Dalibor','Marković')

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
MEASURINGS = {'distance': ('m',1),'volume': ('l',1),'weight': ('g',1),'temperature': ('ºC',1)}
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
['Depois do começo', 'prólogo', ['Medo é desconhecer','Não entender e não compreender','É uma parede que nos impede','Que nossa mente atravesse','As comportas do saber','','O que não se sabe é bizarro','Estranho e extraordinário','Com o instinto natural de sobreviver','Todos podemos perceber','Que pode até ser um pouco hilário','','Sem contexto não há razão','Só há uma imensa ilusão','De que detém todo o poder','Que a verdade pode compreender','Quando quem mente é você','','Imaginação é uma dádiva','A força criadora e divina dada','Pelas mãos suadas de Prometeu','Que entregou a magia aos súditos seus','E aboliu a separação que agora juntava','','Através do símbolo do caduceus','Eu pude perceber quem é Deus','E quem é o divino mensageiro','O messias, o Hermes, o hospedeiro','Que habita os pensamentos meus','','A quintessência só é alcançada','Na alquimia da Serpente da Arábia','E quando sua alma for tratada','Como limpando a sujeira da água','Não terás mais medo de nada','','Pois alcançastes a iluminação','Que tirou a impureza da visão','E agora um novo mundo','Se abre para você','Como um grande portão','','Essa nova dimensão','Vai além da nossa imaginação','Uma realidade possível','Em outro espaço, em outro tempo','Em outras regras, outros momentos','','Você está prestes a adentrar','Um lugar onde pode imaginar além','Um lugar que muitos chamam','De Setesalém'],
[25,12,2007,1,1],[0,32,0],('hauntedhouse_0',200,300)],
 
['Duplo Andantes', 'capítulo I', [1,': Eu começo?','',-1,': Sim. Por favor.','',1,': Bom...','Antes de me envolver com a caça de anomalias, eu estudava psicologia na UFF de Volta Redonda. Na verdade, eu ainda estudo, mas a rotina de caçadora dificulta um pouco.','',-1,': Entendo.','',1,': Eu e meu marido passávamos muito perrengue e procurávamos bicos o tempo inteiro. Eu trabalhava como faxineira no Edifício Esmeralda.','',-1,': No Edifício Esmeralda?','',1,': Sim.','',-1,': Continue.','',1,': Quando eu vi aquelas coisas estranhas pela primeira vez no prédio, eu já tinha visto várias coisas estranhas antes. Eu achava que estava ficando louca.','Numa dessas vezes Iago me buscou na faculdade...'],[25,1,2007,1,1],[11,10,0],('UFF_0',0,0)],
 
['Sangue Verde', 'capítulo II', [-1,': Intrigante.','Já vi que vou ter muito trabalho...','Todos esses acontecimentos ocorreram','entre os meses de Janeiro e Abril,','certo?','',1,': Certo.','',-1,': Ok.','A partir de então vocês dois saíram muito?','',1,': Pode se dizer que sim.','',-1,': E os acontecimentos no Edifício e sua posterior entrada como mercenária foram eventos após o assalto á FIOCRUZ, certo?','',1,': Sim.','',-1,': Preciso de detalhes sobre esse ocorrido.','Por favor,',4,'.','',4,': Claro.','Bom, antes disso, preciso mencionar um fato que pode ser muito importante para a investigação.','Antes de eu receber as amostras, eu fui chamada por cientistas para ir até Lagoa Santa...'],[23,1,2007,1,1],[17,5,0],('archsite_0',0,0)],
 
['Não se meta com a gangue', 'capítulo III', [-1,': Lamento muito o que houve com você,',4,'.','',4,': Obrigado...','',-1,': Você também não entendia com o que estava mexendo, certo?','',4,
': Não no momento. Com as pesquisas eu consegui extrair informações importantes das amostras, mas nada que realmente fosse uma descoberta.','',-1,': Se permitir, quero que minha equipe forense colete as amostras.','',4,': Vamos precisar conversar antes, podemos acertar isso depois?','',-1,': Claro.','Você.','',0,': Olá.','',-1,': Voltando á questão da',1,'...vocês se encontraram na delegacia para fazer um teste de aptidão...é isso?','',0,': Sim, isso mesmo.','',-1,': Me explique melhor.','',0,': Eu já sou mercenário faz um bom tempo. E nunca tivemos uma boa reputação na população. Graças aos surtos que houveram uns tempos atrás, precisamos tomar providências e a PRF foi a primeira a tomar uma atitude.','',-1,': Conheço dessa história...','',0,': Mas no meio, muitos criminosos e gente ruim foi entrando de qualquer jeito para ganhar um dinheiro matando e usando armas. Estava manchando muito a reputação dos mercenários.','E também estava dando muitos gastos, óbvio.','Então decidiram fazer um teste para permitir apenas os melhores dos melhores.','E eu fui lá, é claro.'],
[12,3,2007,1,1],[18,15,0],('pub_0',0,0)],
 
['Caminhões Canavieiros', 'capítulo IV', [-1,': Você não soube quem matou Vinícius?','',0,': Não, foi um acaso muito estranho para mim.','',-1,': Entendido.','Bom,',5,'?','',5,': Ao seu dispor.','',-1,': Você ficou bastante ansiosa para compartilhar sua investigação comigo.','',5,': É uma honra poder trabalhar com o senhor!','',-1,': Muito obrigado.','Mas lembre-se que você ainda é minha testemunha.','',5,': Sim, Senhor Dalibor.','',-1,': Continuando...','Numa dessas investigações, você foi atrás de um idoso do interior que podia estar escondendo "informações importantes"?','',5,': Sim, eu soube desse tal de Hermes graças á investigações anteriores. Eu fui junto com minha equipe até a fazenda desse homem...'],[13,1,2007,1,1],[9,22,0],('canefield_0',0,0)],
 
['Peste Negra', 'capítulo V', [-1,': E você não se lembra de mais nada?','',5,': Lembro. Mas prefiro não contar...','',-1,': Entendo... Eu lamento pelo que você passou,',5,'.','Bom... Preciso falar com você de novo.','',1,': Quem? Eu?','',-1,': Como ela tinha dito anteriormente, ela pediu para que',0,'investigasse uma tal casa assombrada. Sabendo do envolvimento entre vocês dois, posso presumir que ele também te chamou.','',1,': Pior que sim...(risos)','Era apenas para ser uma ida rápida na casa. Só que acabei descobrindo muito mais. Sobre mim ainda.','',-1,': Descobriu o quê?','',1,': Eu encontrei as respostas que procurava no começo do ano...'],[6,4,2007,1,1],[14,2,0],('iagoshouse_0',0,0)],

['Vida Loka', 'capítulo VI', [-1,': Impressionante...','',1,': Pois é...','',-1,': Uma médium...','Você estuda psicologia, certo?','',1,': Sim.','',-1,': Isto não cria dúvidas na sua cabeça?','',1,': Muitas! Muitas mesmo! Na verdade, até hoje não sei como tenho esse dom.','',-1,': Peculiar.','Ok, acho que já terminei com você.','',1,': Sem mais perguntas?','',-1,': Mais nenhuma. Agora que ele está aqui, quero ouvir a versão dele sobre o assalto á FIOCRUZ.','',0,': ...',1,': ...',3,': ...',4,': ...',5,': ...para defesa?','',-1,': Não.','Apenas preciso escutá-lo. Sei que ele tem informações valiosas.','',5,': Desculpa, Senhor Dalibor, mas creio que pode obter essas informações comigo!','',-1,': Agradeço a ajuda, mas quero escutar todos os lados da história.',2,', pode me dizer como organizou o assalto, o que pretendia e o que levou á sua liberdade, após quase matar',1,'?','',2,': Posso sim, senhor...'],[12,2,2007,1,1],[18,32,0],('1urban_0',400,400)],
 
['Pelo Benefício do Mr. Kite!', 'capítulo VII', [-1,': E você foi procurar ajuda depois que todos desapareceram?','',2,': Era o mais lógico a se fazer.','',-1,': De fato.','Essa história está me interessando muito.','',3,': Quero só ver a reação dele!','',-1,': Calma.','',3,': Mano, você vai se amarrar!','',-1,': Ok, tudo bem.','Mas antes eu preciso de detalhes antes de você se reunir novamente com',0,'.','',3,': Beleza! Presta atenção! Se liga, eu e meu amigo, João Grande, estávamos buscando evidências de alienígenas aqui na- É muito esquisito falar isso?','',-1,': De maneira alguma.','',3,': Obrigado. Bom, como tava dizendo... A parada dos géoglifos nos interessou. Então fomos atrás de provas...'],[25,1,2007,1,1],[10,47,0],('archsite_0',0,0)],
 
['Dr. Estanho', 'capítulo VIII', [-1,': No fim, vocês conseguiram prender o sujeito?','',3,': Claro né! A gente chutou a bunda daqu-','',5,': Minha equipe foi acionada e agora ele está na prisão aguardando julgamento','',-1,': Entendi...','(risos)','',3,': Que foi?','',-1,': Nada...ai, ai...','Eu conhecia esse maluco.','',3,': Você também conhecia Mr.Kite?!','',-1,': Todo mundo conhecia ele (risos) mas agora ele tá no fundo do poço. (risos) É isso que ele virou, foi? (risos)','Ok...voltando para você.','',2,': Sim?','',-1,': Investigou um hospital junto com',4,'?','',2,': Sim, a doença misteriosa que todos estão falando começou a se agravar muito rápido. Começou a se espalhar entre as pessoas perto de mim.','Uma dessas pessoas foi justamente Pietra...'],[17,8,2007,1,1],[13,36,0],('urban_0',0,0)],

['Milícia x Meliante', 'capítulo IX', [-1,': Engraçado, também conheci o Dr.Estanho.','',4,': Sério?','',-1,': Sim. Acho que nós nos daríamos bem juntos...','',5,': Seria um prazer, Senhor Dalibor.','',-1,': Isso explica muitas coisas... O paradeiro dele foi um total mistério para mim.','Bom, também terminei com você,',2,'.','',': Foi um prazer ajudar.','',1,': quê? (risos)','',2,': Algum problema?','',1,': Desculpa, nada não. (risos)','',-1,': Já que está tão empolgada comigo, por que não compartilha conosco suas investigações,',5,'?','',5,': Mas é claro!','Foram muitas coisas ao mesmo tempo, o que quer que eu conte primeiro?','',-1,': O assassinato de Vinicíus.','',5,': ...','não prefere outra coisa?','',-1,': Não. Por favor, pode começar.','',5,': ...tudo bem...'],[2,4,2007,1,1],[16,11,0],('urban_0',0,0)],
 
['Não Identificado', 'capítulo X', [-1,': Bom, isso é o bastante.','Já terminei com você também.','',2,': Por que não prende ela também, senhor?','',5,': Eu estava defendendo um amigo!','',2,': Por que esse seu amigo não sabe enfrentar ninguém sozinho, né?','',0,': Não fala nada que eu sou veterano!','',2,': Balela! Pra cima de mim!','',5,': Diz isso para seu amiguinho!','',2,': NÃO FALA ASSIM DELE!','',0,': VOCÊ NEM LIGA PRA ELE!','',5,': VOCÊ MANDOU ELE PRA MORRER!','',2,': NÃO ERA PRA ELE MORRER!','',1,': Matar quem não precisa é o que faz de melhor, né?','',2,': Você não tinha nada a ver com nada!','',4,': Gente, calma...','',0,': Ele assaltou seu laboratório!','',4,': Isso foi faz muito tempo, já. Deixa isso pra lá.','',5,': Essas coisas ninguém perdoa fácil, não! Se quiser você pode conversar com a',1,'.','',1,': O que tem eu?','',5,': Não é psicóloga?','',4,': Tá me chamando de doente?','',2,': Boa! Tô gostando de ver!','',1,': Você fica quieto também!','',-1,': Já chega! Por favor! Parecem um bando de crianças!','',0,': ...',1,': ...',2,': ...',3,': ...',4,': ...',5,': ...ele começou.','',-1,': Quer saber? Esqueçe o que tinha dito. Desse jeito não vamos poder trabalhar juntos.','',5,': Mas Senhor Dalibor...','',-1,': Vamos logo terminar isso...','Aqui,',3,', pelo menos não tá brigando.','Você foi investigar mais sobre os alienígenas?','',3,': Sim.','Após longos meses conseguimos evidências concretas. Fomos mais longe até que',5,'.','',5,': Como?','',-1,': Quero escutá-lo.'],[18,9,2007,1,1],[12,0,0],('hotel_0',0,0)],
 
['Químicas Quimeras', 'capítulo XI', [-1,': Hermitas?','',3,': Pois é! E o melhor é que isso também solucionou o mistério da praga que assolou a região serrana.','',-1,': Percebi. No fim, uma simples busca por provas de alienígenas ofereceu um bem real para a população. Parabéns,',3,'.','',': Não foi nada, obrigado.','',-1,': Se bem me lembro,',0,'se separou de vocês para ir junto com Dra.',4,'.','',4,': Sim, ele veio depois que eu já havia obtido algumas informações.','',-1,': Sobre uma rinha de anomalias?','',4,': Sim. Absurdo, né? Eu descobri me infiltrando entre os participantes. A maioria eram ex-mercenários que não passaram no teste no começo do ano.'],[14,9,2007,1,1],[13,44,0],('lab_0',0,0)],
 
['Quem tem medo de assombração?', 'capítulo XII', [-1,': Olha...','Devo admitir que antes eu estava bravo com vocês, mas o que vocês fizeram por essa região é impressionante, mesmo. Quem diria que o acaso iria unir pessoas tão diferentes para resolver mistérios?','',0,': Verdade...','',1,': Concordo...','',-1,': Consegui cobrir quase todos os eventos desse ano. Em Julho não fizeram nada?','',0,': Eu fiquei caçando, normal.','',3,': Eu visitei minha família.','',1,': Botei minhas matérias em dia e viajei para Angra com meu marido.','',4,': Também viajei, fiz um cursinho de férias e participei de pesquisas.','',5,': Visitei a família e levei meu filho para passear.','',-1,': E você,',2,'?','',2,': Eu não tenho férias.','',-1,': Entendi...','E nesses últimos meses, muitos mistérios?','',0,': Até então, nada. Pelo menos nada muito impressionante.','A gente já tinha dado conta da maioria dos casos. A região estava tranquila de novo.','','Tranquila até demais...'],[17,10,2007,1,1],[18,30,0],('restaurant_0',0,0)],
 
['MP-XIII', 'epílogo', ['[ПОВЕРИТЕЛНО]','','Отчитане на събитията от 25 декември 2007 г. в 12:30 ч. На -22.55105007942486, -43.18521939938314.','','Момичето не присъстваше. Дом разрушен. Има нужда от прикриване.','','Информацията беше събрана от наемника, медиума, мошеника, ловеца, мошеника, учения и полицията. Записите от разговорите се съхраняват на 12 DVD, чифт DVD за всеки респондент.','','Предложението за членство на Албанската агенция е отхвърлено. Запазени спомени. Те се нуждаят от защита от албанската агенция.','','Змеят се появи след интервюто. Несигурна дължина, височина на главата е приблизително 50 метра. Можете лесно да погълнете цял син кит.','УЖАСНО ИМПОНТЕНТ.'],[25,12,2007,1,1],[0,3,0],('hauntedhouse_0',0,0)]
]

'''
ATTACKS
0 - faz nada
1 - atacar
2 - abaixar ATAQUE
3 - abaixar AGILIDADE
4 - abaixar FORÇA
5 - abaixar RESISTÊNCIA
6 - condição
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
FCONDITIONS = ('normal','costas','repelente','fedor','resfriado','febre','fome','sede','sono','náusea','enjôo','fraqueza','cegueira','preso','paralisia','inconsciente','parasita','queimadura','veneno aracnídeo','veneno antiofídico','veneno escorpiônico','hemorragia','regeneração','invisibilidade','velocidade')
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
'AGILITY': 7,'HP': 42,'RESISTANCE': 1,'STRENGHT': 2,'PATH': 'follow','DODGE': 'circle','HABILITIES': [['Ahegao',['O mamífero tenta sensualizar o oponente simulando um ato sexual, mas faz o efeito contrário abaixando seu ATAQUE'],-3,2],['Água de banho',['O mamífero oferece água de banho para o oponente, este o ingere e obtém HERPES.'],2,4],
['Nadar',['O mamífero nada no ambiente para recuperar sua VITALIDADE.'],10,1],['Canto submarino',['O mamífero entoa uma canção para chamar uma anomalia para a batalha.'],1,5]],'WEAKNESS': 'SILVER','BLOOD': 10,'ITEM': None},

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
'AGILITY': 1,'HP': 50,'RESISTANCE': 1,'STRENGHT': 2,'PATH': 'follow','DODGE': 'hide','HABILITIES': [['Tentáculos','O molusco usa seus tentáculos para atacar seu oponente.',-5,1],['Jato de tinta','O molusco atira um jato de tinta que impossibilita o oponente de atacar.',-5,3],
['Camuflagem',['O molusco se disfarça no ambiente, aumentando sua AGILIDADE.'],2,3],['Torpedo',['O molusco acerta o oponente com um ataque explosivo que acerta todos á volta, super efetivo.'],-15,1]],'WEAKNESS': 'LEAD','BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},

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

#LABYRINTH
'spike': {'NAME': 'Spike','INFO': 'Alienígena da raça red spinam. Possui vários chifres na cabeça, lembrando espinhos. Ele não é perigoso, mas não se engane: ele pode ir na sua direção e lhe dar uma cabeçada!',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'blaze': {'NAME': 'Blaze','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Queimar','',0]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'slime': {'NAME': 'Slime','INFO': 'Alienígena da raça viridi gunk. Possui seis tentáculos e um chifre na cabeça e anda soltando gosma.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Gosma','',1]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'rock': {'NAME': 'Rock','INFO': 'Alienígena da raça constans caerulea. Possui duas garras gigantes e dois pés minúsculos. É muito forte e aguenta três tiros, porém ele é muito dorminhoco e bobão, pois ele não se movimenta no cenário enquanto ele não repara sua presença.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'laser': {'NAME': 'Laser','INFO': 'Alienígena da raça percussit aureos. Possui duas antenas, duas patas grandes, dois pés e um único olho que possui a habilidade de soltar raios de plasma. Ele tem uma personalidade fria e séria.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Atirar','',2]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'bounce': {'NAME': 'Bounce','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Pular','',3]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'float': {'NAME': 'Float','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Bombas','',4]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'glue': {'NAME': 'Glue','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'turn': {'NAME': 'Turn','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Virar','',5]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'stone': {'NAME': 'Stone','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Transformar','',6]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'hide': {'NAME': 'Hide','INFO': 'Alienígena da raça ignem aurantiaco. Possui dois chifres, duas patas e duas garras. Curiosamente, ele tem os olhos separados. Ele tem esse nome pois pode queimar itens com fogo cósmico.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Esconder','',7]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'diskman': {'NAME': 'Diskman','INFO': 'Ao derrotar todos os invasores do cenário você ganha 1000 de bônus e um Diskman irá aparecer para colocar mais inimigos do exército de Black Head.Todos eles são filhos, sobrinhos, primos, tios, avôs, sogros e amigos dele.',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Levar','',8]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},

'blackhead': {'NAME': 'Black Head','INFO': 'Também conhecido como cabeça de fogo, alienígena de raça desconhecida. É da altura de uma casa de 2 andares e é negro com um rosto de uma caveira assustadora. Possui as habilidades de todos os seus capangas e quer invadir planetas pelo universo para escravizar alguns alienígenas e vendê-los para o mercado negro',
'HEIGHT': '1,20','HABITAT': None,'TYPE': None,
'STRENGHT': 2,'AGILITY': 5,'RESISTANCE': 0,'VITALITY': 1,'PATH': 'maze1','DODGE': None,
'HABILITIES': [['Atirar','',2],['Explodir','',9]],
'FOOD': None,'WEAKNESS': None,'BLOOD': 0,'ITEM': None,'SONG': None,'SCREAM': None},
}

ITEMENEMIES = {'drink_guarana': ('wingedcan',100),'key_bedroom': ('elkeys',100),'tool_pen': ('ppap',100),'cigar': ('cigaruto',100)}

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

#BOMBS (name,description,price,volume,weight,type)
'bomb_regular': ['bomba',['Destroem blocos que atrapalham seu caminho, mas cuidado para não ser atingido também! Novas bombas surgem na MBEM.'],0,0,0,0],
'bomb_slime': ['bomba de meleca',['Ao explodir, deixam meleca grudenta no chão, o que faz seu advesário andar mais devagar.'],0,0,0,1],
'bomb_bolt': ['bomba trovejante',['Quando explode, solta 4 rajadas em 4 direções que destroem tudo em seu caminho.'],0,0,0,2],
'bomb_grenade': ['granada',['Ao invés de deixar em um canto, você arremessa a bomba!'],0,0,0,3],
'bomb_tactical': ['bomba tática',['Só é ativada quando você dá o sinal.'],0,0,0,4],

#POWER UPS (name,description,price,volume,weight,type)
'letter': ['letra',['Use para fazer seu personagem crescer!'],0,0,0,0],
'pow_bubble': ['bolha',['Use para mandar seus inimigos para fora do labirinto!'],0,0,0,0],
'pow_doublebubble': ['bolha dupla',['Se um já é bom, dois é melhor.'],0,0,0,1],
'pow_triplebubble': ['bolha tripla',['Dois é bom, três é demais.'],0,0,0,2],
'pow_bounce': ['bolha saltitante',['Quica nas paredes do labirinto.'],0,0,0,3],
'pow_plasma': ['bolha de plasma',['Ao atingir seu advesário, todos os pisos pintados por ele voltam á cor branca.'],0,0,0,4],
'pow_phantom': ['bolha fantasmagórica',['Ela atravessa as paredes do labirinto.'],0,0,0,5],
'pow_follow': ['bolha perseguidora',['Persegue o inimigo mais próximo.'],0,0,0,6],
'pow_speed': ['bota de velocidade',['Faz você andar mais rápido.'],0,0,0,7],
'pow_slow': ['bota de lentidão',['Faz você andar mais devagar.'],0,0,0,8],
'pow_invert': ['inversor',['Inverte os controles dos jogadores.'],0,0,0,9],
'pow_bolt': ['relâmpago',['Solta um raio congelante no seu advesário, que fica 10 segundos sem se mexer.'],0,0,0,10],

#TILES (name,description,price,volume,weight,gid)
'til_grass': ['grama',['graminha vedinha'],0,0,0,348],
'til_color': ['piso colorido',['graminha vedinha'],0,0,0,397],
'til_metalbars': ['barras de ferro',['graminha vedinha'],0,0,0,410],

#GUITOOLS (name,description,price,volume,weight,function)
'guit_pencil': ['lápis',['pinta o mapa.'],0,0,0,1],
'guit_erase': ['borracha',['apaga tiles.'],0,0,0,0],
'guit_dropper': ['conta gotas',['use para obter a tile selecionada.'],0,0,0,2],
'guit_bucket': ['balde',['pinta tiles.'],0,0,0,3],
'guit_select': ['seleção',['seleciona tiles.'],0,0,0,4],
'guit_transform': ['transformar',['move tiles.'],0,0,0,5],
'guit_copy': ['copiar',['copia tiles.'],0,0,0,8],
'guit_scissors': ['tesoura',['recorta tiles.'],0,0,0,6],
'guit_glue': ['cola',['cola tiles.'],0,0,0,7],
'guit_rect': ['retângulo',['apaga tiles.'],0,0,0,8],
'guit_undo': ['desfazer',['volta no histórico.'],0,0,0,8],
'guit_redo': ['refazer',['avança no histórico.'],0,0,0,8],
'guit_load': ['carregar',['carrega um mapa.'],0,0,0,8],
'guit_save': ['salvar',['salva um mapa.'],0,0,0,8],
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
 
['cangaceirostv@cmail.com','Proposta de entrevista',
['Boas novas, ' + res.CHARACTERS[0]['NAME'] + ' ' + res.CHARACTERS[0]['LASTNAME'] + '.', ' ', 'Com a repercussão dos casos de', 'anomalias do Departamento de', 'Detenção de Anomalias de',
'Itatiaia, sugerimos uma', 'entrevista com você e dois', 'participantes para o', 'Jornal da Noite.', ' ', 'A entrevista será ás 5:30 PM', 'e será gravado nos estúdios', 'da Cangaceiros TV, na',
'Av. Getúlio Vargas.', ' ', 'Aguardamos sua resposta', 'no local.']],
 
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
('Polícia Federal',[('prende',[('homem',[('suspeito de',['assédio sexual','assassinato','sequestro']),'foragido']),'mulher']),('apreende',['maconha','carga roubada','celulares roubados','produtos falsificados']),('captura',['bandido','criminoso']),('encontra',[('corpo de',['criança desaparecida','mulher esquartejada']),'pessoa desaparecida'])]),
('Homem',[('é acusado',['de assassinato','por ex','de homicídio','por matar']),('é visto',[('roubando',['carros','celulares','roupas','empadas']),('assaltando',['caixa eletrônico','banco','mercado local','supermercado','loja'])])]),
('Enchente atinge',[('região serrana',['do Rio de Janeiro','de Minas Gerais','de São Paulo']),('cidade do interior',['do Rio de Janeiro','de Minas Gerais','de São Paulo'])]),
('Preço',[('dos',[('combustíveis',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),('alimentos',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),('imóveis',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),('colchões',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])]),('do',[('arroz',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),('gás',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])]),('da',[('conta de luz',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])]),('conta de água',[('aumenta',['5%','10%','15%','20%','25%']),('diminui',['5%','10%','15%','20%','25%']),('tende a',['aumentar, segundo especialistas','diminuir, segundo especialistas'])])])])
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

'''
DIALOG PROTOCOLS IN INT
0 - change speaker
1 - wait for input
2 - dialog name
3 - chapter beginning
4 - exit chapter
5 - chapter ending

DIALOG PROTOCOLS IN TUPLE
0 - dialog settings (voice/type/font,value)
1 - get item/money (item/quantity,price,dlgsav,properties)
2 - morality (quantity,check,[if text],[else text])
3 - insert text (dtalks index/party member/time)
4 - call (contact index)
5 - new email (email index)
6 - task (task index/item,text incomplete,text complete)
7 - new contact (contact index)
8 - achievement (achievement index)
9 - relationship ((from,to),check,[if ttext],[else text])
10 - dialog choices ([text]...)
11 - walk in dialog (quantity)
12 - gui class (gui class)
13 - battle (enemies,(repeat))
14 - probabiliy ([probability,text],...)
15 - play sfx/music (sound/song)
16 - if character in party (party index, text)
17 - waitlist (name,time,{type,who,index})
18 - change party
19 - set datetime (time,date)
20 - attribute change (quantity,proficiency)
21 - dlgsav (dialog key, dialog index)
22 - name party (answer)
23 - insert dialog (dialog key,dialog index)
24 - move character (npc index,(x,y),direction,sprite key)
25 - character emotion (npc index,sprite key)
26 - camera (npc index)
27 - wait (time)
28 - tutorial (tutorial key)
29 - go to place (map name,x,y)
30 - add character ((x,y),npc index,npc who)
31 - censorship (original, censored)
'''
 
DTALKS = {'good morning': 'Bom dia','good afternoon': 'Boa tarde','good evening': 'Boa noite','good night': 'Boa noite','he1': 'Senhor','she1': 'Senhora'}

DIALOGS = {
#ADVICES
'TEST': [['Queria jogar cartas...',1,(6,'playingcards',['Você tem algumas?',1],['Que conveniente! Você tem cartas!',1,'Que acha de jogar?',(10,['Por que não?',(12,'minigames.TicTacToe()')],['Não, obrigado'])]),(3,'CC','<ele anda pelo quarto.>'),'O que vai acontecer em outro dia?',1,(19,[14,35,0],[15,3,2007,1,1])]],

'PRODUCTS': [[(12,'products',[('food_peanut_candy',),('locksmith1',),('cage_big',0,0.75)])],[(12,'products',[])]],

'INVSHIRT': [['Não é uma boa idéia tirar a camisa aqui.',1,'Se eu tivesse ao menos um provador...',1]],
'INVPANTS': [['Não é uma boa idéia tirar as calças aqui.',1,'Se eu tivesse ao menos um provador...',1]],

#TUTORIALS
'TUTINV': [['Antes disso,','você sabe mexer nas suas coisas?',1,0,'Como assim?',1,0,'Você sabe...','suas coisas!',1,'Sua mochila','Seu inventário.',
(10,['Sei sim (pular tutorial)','Ah, que bom!',1,(23,'',0)],['Mais ou menos (tutorial pra experientes)','Já mexeu com','esse tipo de coisa','antes, né?',1,
'O jeito que mexo é','um pouco diferente.',1,(23,'TUTINV1',1)],['Não... (tutorial pra iniciantes)','Nunca mexeu com','inventário antes?',1,'Não se preocupe!',
'Vou te ensinar direitinho!',1,(23,'TUTINV',2)])],
['Como já deve saber,','Você deve acessar seu inventário',(3,(6,0)),'para mexer em seus itens.',1,'Aqui estão todas as suas...','Uísque?',1,0,'Voltei a beber.',1,0,
'Entendi...',1,'Enfim,',1,'É muito importante','mexer no seu inventário.',1,'Mas você não pode guardar','tudo o que você quiser!',1,'Cada item tem','um volume e um peso,',
'assim como a mochila que','estiver usando.',1,'Por isso você precisa','ver o que você precisa','mesmo levar.',1,'Claro que tem coisas que','realmente não precisa','levar.',1,
'Como por exemplo essa','garrafa vazia que','tá ocupando espaço!',1,'Sempre que terminar de usar','seus itens você precisa','jogar o lixo fora!',1,'Alguns itens não deixam lixo,',
'mas a maioria deixa.','Vê se joga o lixo','no lugar certo, tá?',1,'Os 4 quadradinhos em pé','são as coisas que está vestindo.',1,'Só vai estar vestindo as roupas','se estiverem nesse espaço.',1,
'A mesma coisa acontece com','os 4 quadradinhos deitados.',1,'É onde ficam seus equipamentos','e armas para batalha.',1,'O quadradinho no canto é','sua mochila.',1,'Você vai encontrar mochilas',
'que carregam mais itens,','e você pode trocar por aqui.',1,'Por último,','você pode usar seus itens','apertando',(3,(4,0)),1,'Você também pode mover','seus itens apertando',(3,(5,0)),1,
'desse jeito você pode','equipar itens, juntar itens,','e até dar para outras pessoas.',1,'Também é desse jeito','que você recarrega armas','coloca tempero nas comidas','e confecciona objetos.',1,
'basta colocar um item','em cima de outro item.',1,'Nem sempre vai dar certo,','mas só vai saber se tentar!',1,'O inventário é bem legal','para se mexer.',1,'Por isso não tenha','medo de ficar brincando com ele.',1,(23,'',0)],
['Você deve acessar seu inventário',(3,(6,0)),'para mexer em seus itens.',1,'Aqui estão todas as suas...','Uísque?',1,0,'Voltei a beber.',1,0,'Entendi...',1,'Enfim,','Todas as coisas e objetos','que pegar vão ficar','guardados aqui.',1,
'comida, bebida, remédios,','roupas, armas, aparelhos,','munição, chaves e até lixo!',1,'É muito importante','mexer no seu inventário.',1,'Mas você não pode guardar','tudo o que você quiser!',1,
'Cada item tem','um volume e um peso,','assim como a mochila que','estiver usando.','Não vai caber tudo na sua mochila.',1,'Por isso você precisa','ver o que você precisa','mesmo levar.',1,'Claro que tem coisas que','realmente não precisa','levar.',1,'Como por exemplo essa','garrafa vazia que','tá ocupando espaço!',1,'Sempre que terminar de usar','seus itens você precisa','jogar o lixo fora!',1,'Alguns itens não deixam lixo,','mas a maioria deixa.','Vê se joga o lixo','no lugar certo, tá?',1,'Você deve ter visto','que alguns quadrados','estão afastados, né?',1,'Os 4 quadradinhos em pé','são as coisas que está vestindo.',1,'Como disse, você pode guardar roupas','mas só vai estar vestindo elas','se estiver nesse espaço.',1,'Roupas aumentam sua defesa','além de te deixar mais estiloso!',1,'A mesma coisa acontece com','os 5 quadradinhos deitados.',1,'É onde ficam seus equipamentos','e armas para batalha.',1,'O quadradinho no canto é','sua mochila.',1,'Lembra que falei que','mochilas tem volume e peso?',1,'Você vai encontrar mochilas','que carregam mais itens,','e você pode trocar por aqui.',1,'Por último,','você pode usar seus itens','apertando',(3,(4,0)),1,'É por aqui que você pode','comer, beber, essas coisas.',1,'Você também pode mover','seus itens apertando',(3,(5,0)),1,'desse jeito você pode','equipar itens, juntar itens,','e até dar para outras pessoas.',1,'Também é útil para dar uma','organizada!',1,'Também é desse jeito','que você recarrega armas','coloca tempero nas comidas','e confecciona objetos.',1,'basta colocar um item','em cima de outro item.',1,'Nem sempre vai dar certo,','mas só vai saber se tentar!',1,'O inventário é bem legal','para se mexer.',1,'Por isso não tenha','medo de ficar brincando com ele.',1,'Ele não vai te morder.',1,(23,'',0)]],

'TUTGB': [[0,'Mas como vocês ganham dinheiro?',1,0,'Isso é interessante.',1,'Nós caçadores de anomalias','ganhamos dinheiro com contratos.','Recebemos uma ligação','e uma pessoa paga a gente','para fazer um serviço.',1,'Seja um monstro que está','atrapalhando um fazendeiro,','ou uma aberração que','matou vários civis.',1,0,'Meu Deus...',0,'...mas o mais daora','é quando vamos numa','casa assombrada ou','algo do tipo!','É bem legal!',1,0,'Entendi...',1,'Mas na maioria das vezes...',1,'Ganhamos dinheiro expurgando mesmo.',1,0,'Expurgando?',1,0,'Exterminando anomalias.',1,'Essas que ficam zanzando','por aí, sabe?',1,0,'São muitas?',1,0,'Deve pensar que não são tantas','mas é porque elas preferem','a natureza.',1,'Houve um tempo que elas','atormentavam as cidades,','todas elas.',1,'Mas graças á PRF a gente','conseguiu controlar as anomalias.',1,0,'Mas por que a Polícia Rodoviária?',1,0,'É uma longa história.',1,'Voltando ao assunto,','A gente ganha uma graninha','com isso daqui.',1,0,'O que é isso?',1,0,'Nós chamamos de Sangue Verde','mas não sabemos o que é','de verdade.',1,'Apenas que todas as anomalias','tem essa coisa dentro deles.',1,'A gente vende o sangue verde','em frasquinhos.',1,'Sempre que expurgamos','alguma anomalia,','pegamos um pouco do','sangue verde nela.',1,'Não conseguimos pegar muito','porque a maioria seca rapidinho.',1,'Além disso a gente derrama','muito enfrentando elas.',1,0,'Vocês ganham dinheiro','vendendo sangue?!',1,0,'Daora né?',1,0,'Quem diabos iria comprar','sangue de monstros?',1,'Na moral?','Sei também não.',1,'Mas eu ganho grana','então isso é o que importa.',1,'A gente leva os frascos','para um posto de polícia','e eles nos pagam.',1,0,'Que nojo.','Já estou me arrependendo.',1,0,'Deixa de graça!','Você vai amar!',1]],

#FURNITURE
'MIRROR': [[(16,0,['Que peste feia é essa?',1,'ah.','Sou eu.',1]),(16,1,['Estou bonita...?',1]),(16,2,['Bigodin finin','Cabelin na régua',1]),(16,3,['Dá pra sair',1]),(16,4,['Sempre arrasando',1]),(16,5,['Tô bem arrumada',1])]],
'SIDNEY WARDROBE': [['Qual roupa vou vestir agora?',(10,['Casaco xadrez','Ok'],['Blusa preta de banda','Sempre gostei do HUG'],['Blusa social','Essa tá boa'])]],
'BROKEN CLOCK': [['Isso tá quebrado faz tempo.',1]],
'SIDNETRA PORTRAIT': [[(16,0,['Essa foto me traz muitas lembranças...',1,'...lembranças ruins.',1]),(16,1,['...',1,'Eles se davam bem...',1])]],
'JANAGO PORTRAIT': [[(16,0,['Legal.',1]),(16,1,['Essa foto foi em Búzios.',1,'Foi o dia em que nós','começamos a morar juntos.',1,'A gente comeu muito camarão naquele dia.',1])]],
'JANE BED': [['Ah não...',1,'a cama tá bagunçada de novo',1,'...',1,'...abracadabra, cama arrumada!',1]],
'PICTURE': [['É uma pintura bonita.',1,'não tô entendendo nada,','só sei que é bonita.',1]],
'DIRTY SINK': [['A pia está cheia de louça suja...',1]],
'DIRTY COOKER': [['Tem arroz frio e uma frigideira engordurada no fogão.',1]],
'EMPTY FRIDGE': [['Água,sachês de ketchup e ovos...',1,'Considero isso uma geladeira vazia.',1],['Tá na de fazer as compras do mês.',1]],
'JANE FRIDGE': [['A visão do paraíso.',1],['O Iago comprou um monte de sorvete.',1,'Esse idiota me conhece.',1]],
'TRASH': [[(12,'TRASH')]],

'BALANCE': [[(16,0,['PESO: 65kg']),(16,1,['PESO: 72kg']),(16,2,['PESO: 67kg']),(16,3,['PESO: 58kg']),(16,4,['PESO: 54kg']),(16,5,['PESO: 63kg']),1]],
'DEATH COUNTS': [['Você já parou no hospital ',(3,'deaths',' vezes.',1,(16,'DEATHS',[['Mas isso nem é nada.','O que você está passando','é só o começo.'],['Já está normal','ver você por aqui.'],['Devia fazer amizade com','as enfermeiras.','É o paciente número 1','delas.'],['Coitado...','Você quer morar aqui, né?'],['Mano...','Tá tudo bem?','Você tá vindo muitas','e muitas vezes aqui!',1,'Com certeza você tá','todo rachado!'],['Estou impressionado.',1,'Nunca vi ninguém parar no hospital','mais de 50 vezes na vida.']])),1]],

#DEVICES
'OLD PC': [['Esse pc ainda usa Windows XP.',1,(21,'OLD PC',1)],['O Orkut tá aberto.',1,(21,'OLD PC',2)],['Estavam usando o MSN.',1,(21,'OLD PC',0)]],
'MODERN PC': [['No canto da tela diz "Não é genuíno".',1]],
'PC GAMER': [['O teclado LED brilhando me deixa','ma',1,'lu',1,'co.',1]],
'OLD TV': [['O Maicon precisa trocar logo essa TV.',1]],
'MAICON PS2': [['O Maicon tava jogando Bully.',1,(21,'MAICON PS2',1)],['Droga!',1,'Esse CD do GTA San Andreas','veio com um jogo','nada a ver!',(21,'MAICON PS2',2)],['Se não funcionar','A gente bota de ponta-cabeça.',1,'Nunca falha.',1,(21,'MAICON PS2',0)]],
'PLUG': [['Eu posso encaixar um carregador aqui.',1],['O celular carregou.','Foi rápido!',1]],

'ATM': [[(12,'ATM')]],

'TV1': [[(15,'TVSHOW1',0),'Aí carinha que mora','logo ali!',1,'Passa um dólar!',1,(21,'TV1',1)],
[(15,'TVSHOW2',0),'E aí Til Phil!',1,(21,'TV1',2)],
[(15,'TVSHOW3',0),'QUEM É VELHA COROCA?',1,'Foi o Seu Madruga','que disse, Dona Florinda!',1,'AH É?',1,(15,'LAUGHS',0),(27,100),'E da próxima vez','Vá falar mal da sua avó!',1,'Ninguém tem paciência comigo...',1,'"Ninguém tem paciência comigo!"',1,'Só não te dou outra','Porque minha mãe','se chamava coroca...',1,(21,'TV1',0)]],

#CHESTS
'EMPTY CHEST': ['Não tem nada aqui...',1],
'HHBEDROOMCHEST': [[(1,'key_bedroom',0,'HHBEDROOMCHEST','0001')]],
'SIDNEY NIGHTSTAND': [[(1,'food_peanut_candy',0,'SIDNEY NIGHTSTAND')],[0,'Não deveria mexer nas','coisas dos outros',1]],
'HH FRIDGE': [[(1,'drink_beer',0,'HH FRIDGE')],[0,'Não deveria mexer nas','coisas dos outros',1]],
'TRASH CAN': [[(1,'melee_bottle',0,'TRASH CAN')]],
 
#PAPERS & SIGNS
'TAROT POSTER': ['BÚZIOS E CARTAS','Trago seu amor aos seus pés!','978543322',1],
'MISSING POSTER': ['PROCURA-SE','Talita Manhães','Se você a viu, favor,','ligue para: 992120342',1],

#FORTUNE TELLER
'FORTUNE TELLER': [['Seja bem vindo!','Está a procura de respostas?','Não consegue encontrar seu rumo?','Gostaria de conhecer seu destino?',(10,['Não, obrigado','Se mudar de idéia,','vou estar aqui para ajudar.',1],
['Sim','Excelente.','Sente-se, por favor.',1,'A verdade está nas cartas','interpretando elas com atenção','podemos encontrar as respostas','que nós procuramos.',1,(23,'FORTUNE TELLER','scene')])],
['Lhe aconselho a se','preparar para o que vir.',1,'Sempre esteja um passo adiante!',1,'Até mais!',1],
['Oh meu Deus!','Impressionante...',1,'Nunca vi algo assim antes!',1,'Você irá enfrentar','grandes ameaças',1,'Seres sem vida irão','te atormentar',1,'Irá se perder','no local que mais conhece',1,'E passará por dificuldades','em seus relacionamentos.',1,(23,'FORTUNE TELLER',1)],
['Vejamos...',1,'Você enfrentará tribulações','nos seus momentos de','maior discontração.',1,'Tentarão lhe tomar o que','é de mais valioso para você.',1,'Você precisa estar','sempre atenta','e vigilante.',1,(23,'FORTUNE TELLER',1)],
['Que interessante.',1,'Seus caminhos irão','se cruzar com o de','uma aprendiz.',1,'Laços firmes e duradouros','irão surgir dessa relação.',1,'Mas seus caminhos também','irão se cruzar com os','de um vingativo.',1,'Alguém se arrependerá de cometer','um grave erro que custará','sua paz e longevidade.',1],
[]],

#ENEMIES
'BATTLEDIALOG': [(10,['Motivar',(20,2,2)],['Ameaçar',(20,2,-2)],['Negociar',(23,None)])],
'IRRATIONAL': ['A anomalia não entende nada do que você tá falando',1],
'MADLADCAT': ['Miau miau','miau miau miau','miau.',1,(10,['Sábias palavras.','miau.',1],['Magnífico.',0,(31,'Não ajudou em porra nenhuma.','Não me ajudou em nada.'),1])],
'TARGET': ['Parece bobo, eu sei','Mas é bom já pegar o jeito da coisa.','Ás vezes você pode negociar com o oponente','E assim poupar sua vida.','Também pode obter informações','Importantes dele',
'Ou mesmo convencê-lo a parar de lutar'],
'EMOHIPSTER': [(10,['O que você escuta?','conhece aquela banda?','HUG','muito boa',(10,['eu também gosto de HUG!','sério?!','ai meu deus! que legal!'],['já ouvi falar','é muito boa cara','você tem que escutar'])],['se manda daqui ô barbudo!','como é que é?','o que você tem contra barba?',(10,['Nada oxe','é bom mesmo'],['Isso não é barba','mas...eu cuido tanto dela...'])])],
'HOTMAN': [(10,['Cê tá bem mano?','Claro que não né?? Estou queimando feito palha nessa desgraça!'],['Vaza ou meto chumbo','Eu não tenho medo de você'],['A gente não quer nada contigo',
'Mas eu quero','Preciso de sangue!!'])],
'EDMOTO': [(10,['ED MOTA??','Não!','Meu nome não é mais Ed Mota!',1,'De agora em diante...',1,'Meu nome será...',1,'ED MOTO!',1],[])],

#MERCENARIES
'VINICIUS': [(10,['Eu não quero brigar contigo','Eu também não quero','Mas é preciso'],['Você pode ficar com a recompensa','Você está blefando?',(10,['Vai pegar?','É claro que vou!','...assim que acabar com você!'],['Esqueçe','Agora estou mais invocado!'])])],

#SHOP
'POPCORN KART': [[(3,'time',','),(3,1,'!'),(10,['Quanto é uma pipoca?','A pipoca salgada é 5$','e a pipoca doce é 6$.',1,(11,-6)],['Gostaria de comprar uma pipoca salgada.','Aqui está!',1,(1,'food_popcorn',5),0,'Muito obrigado.',1],['Gostaria de comprar uma pipoca doce.','Aqui está!',1,(1,'food_popcorn_candy',5),0,'Muito obrigado.',1],['Estou só olhando.'])]],
'CHURROS KART': [[(3,'time','!'),(10,['Quanto é um churros?','Um churros é 5$.',1,(11,-5)],['Gostaria de comprar um churros.','Aqui está!',1,(1,'food_churros',5),0,'Muito obrigado.',1],['Estou só olhando.'])]],
 
#DELIVERY
'DEPOSIT': [['Olá!','Me chamou?',1,(12,'storage')],['Se precisar de qualquer coisa,','é só chamar!',1,(24,'n',('px300','py0'),0)]],
'PIZZA DELIVERY MUSSARELLA': [['Aqui está.',1,(1,'food_pizza_mussarella',20),(24,'n',('px300','py0'),0)]],
'PIZZA DELIVERY SHAGGY': [['Aqui está.',1,(1,'food_pizza_shaggy',20),(24,'n',('px300','py0'),0)]],
'PIZZA DELIVERY CHICKEN': [['Aqui está.',1,(1,'food_pizza_chicken',20),(24,'n',('px300','py0'),0)]],
'PIZZA DELIVERY 4CHEESE': [['Aqui está.',1,(1,'food_pizza_4cheese',20),(24,'n',('px300','py0'),0)]],
'REWARD':[['Ei! Você não tem sangue nenhum!','Volte quando tiver pego alguma coisa!',1],['Só isso?','Vou dar sua recompensa, mas poderia ter se esforçado mais',1],['Você conseguiu bastante sangue','Aqui está sua recompensa',1],['Uau! isso é muito sangue!','Aqui está sua recompensa pelo seu trabalho duro!',1],['Não tem carteira?','Nem cartão?',1,'E como é que vou te','pagar?',1]],
'MERCATOR': [['Olá cliente!','Interessado em alguns produtos?',1,(12,'mercator',[('locksmith1',),('tent_big',1,0.5)])],['Foi mal cara, mas sem grana, sem acordo.',1],['Espera um pouco cara!','Você tá sem espaço!',1,'Não quer dar para outra pessoa?',1]],
'CASHIER INGRID': [['Os produtos estão nas pratileiras','é só você ir pegar e trazer aqui',1,0,'O quê? você quer que eu vá buscar pra você?!',1],['Você não tem dinheiro?',1,'Sério?',1],['Você tá cheio de coisas...','Não sei se posso deixar levar tudo isso.',1]],
'CASHIER SANDRA': [['Vai pedir alguma coisa?',1],['Você tá sem dinheiro.',1],['Você tá sem espaço',1]],
'CASHIER YASMIN': [['Eu tenho que dormir...','compra logo o que tu quer...',1],['Como é que você leva coisas','que não pode comprar??',1],['Fala sério',1,'Por favor leve só o que puder levar',1]],

'DRITHR SANDRA': [['Licença, aqui é o Drive Thru',1],['Você tá sem dinheiro.',1],['Você tá sem espaço',1]],
 
'FARMACEUTIC': [['Não sabe que remédios comprar?',(10,['Não...','O que você quer tratar?',(10,['Resfriados e alergias','Se você estiver sentindo algum resfriado,','gripe, tontura ou fraqueza, um\
 simples','xarope já basta'],['Infecções e hemorragias','Esses são problemas fortes, mas não muito graves','Para infecções, use o antibiótico correspondente ao tipo de','contaminação.',0,'Se tiver\
  hemorragias, primeiro cicatrize a ferida','e depois ponha um band-aid para','evitar mais saída de sangue'],['Contaminação e Mal-estar','Caso se sinta alguma coisa parecida, pode ser','sinal de envenenamento ou\
   intoxicação, existem','várias pílulas para diversos tipos de tóxicos']),'Mais alguma pergunta?',(11,-7)],['Tô de boa','Tudo bem','Se tiver alguma dúvida é só perguntar','Fique á vontade'])]],
 
'HOTEL ATTENDANT': [[(3,'time','!'),'O que deseja?',(10,['Uma noite apenas','O custo é de 20 por pessoa',(10,['Ok','Aqui, seu quarto é o N° 902',(1,'chave',20)],['Deixa pra lá','Volte a hora que quiser'])],
['Estou apenas olhando','Sinta-se á vontade'])]],

#STRANGERS
'STNPC': ['Oi...eu te conheço?','Você não deveria estar falando com estranhos','Agora não! Eu tô com pressa!','Afe, mercenários...','Não quero falar com você','Licença'],
'STDOOR': ['Não conheço você','Quem é você?','O que você quer?','Vai embora!'],
'STHOTEL DOOR': ['Esse é meu quarto','Aqui não é seu quarto, está perdido?'],

#CITY ONE
'BUS WAITER': [['Esse ônibus demora mesmo',1,'Pego ele todo dia pra','descer a serra até a capital',1,(0,2,'ANGER'),'São só 4h de viagem!',1,3]],
'SQUARE OLD MAN': [['Eu adoro alimentar os pombinhos',1,'ainda mais aqueles que','tem um monte de penas','lindas no rabo',1,(10,['como assim?','elas chegam a hipnotizar...',
'eu fico olhando e perco','a noção do tempo.',1],['legal','são adoráveis',1])]],
'HOMELESS MAN': [['Pode me dar um trocado','por favor?',1,(10,['...','é sempre assim...',1,(2,-5)],['Tudo bem',(1,-1),(2,5),'Deus te abençoe!',1])]],
'STREET SWEEPER': [['Hey mano',1,'Posso te falar uma coisa?',1,(10,['É claro','Se estiver com lixo nos','bolsos ou na mochila...',1,'por favor...',1,'...jogue na lixeira',1,
'Não custa nada',1,'Tem uma em cada esquina da cidade',1,'Fechou?',1],['Agora não...','Tá bom então...',1,'não é como se fosse','te dar uma informação','importante que fosse',
'mudar sua vida e seu','jeito de agir',1,'bola pra frente',1])]],
'YOUNG MOM': [['Meu filho adora brincar','nesse monte de areia',1,'Também gosto porque','o sinal da praça é','muito bom',1,(10,['o quão bom?','quê?',1,(10,['o quão bom?','ah...',
'dá pra ver as notícias','e mexer na internet',1,'não é muita coisa porque','meu celular é de tecla',1,'mal posso esperar ter','um daqueles celulares novos','que você pode tocar',
'na tela',1],['esquece','ah tá',1])],['não é pra tanto','é o que você pensa',1,'pelo menos é melhor','do que em outras cidades',1],['mas é só aqui?','meio que sim',1,'o sinal só é bom',
'mesmo na praça',1,'mas dá pra usar o sinal','em outros lugares também',1])]],
'FUNNY KID': [['Iaaaaaaá!',1,0,'que fofo',1]],
'INFORMED MAN': [['Eu sempre vejo as','notícias na televisão',1,'mas quando a internet está','boa eu vejo no celular','também',1,(10,['deveria ver mais jornais','vai por mim, hoje em',
'dia é mais que necessário',1,'ainda mais com essa onda','de crimes por causa dos mercenários',1,'eles avisam quando tá tendo','caça na região',1],['não gosto muito de notícias',
'mas por que?',1,(10,['É muita violência','eu também acho',1,'mas é a vida',1,'se não se informar, pode','perder muita coisa importante',1],['Não tenho tempo pra isso','Ler um artigo não',
'faz mal cara',1,'não demora muito, é bom','parar a correria do dia','pra ler alguma coisa',1],['É tudo mentira','eu concordo',1,'mas sei lá','quem não mente hoje?','eu faço assim, leio a matéria',
'mas com uma certa desconfiança',1,'eu preciso me informar,','mas se eu sair acreditando','em tudo que vejo,','aí eu posso acabar','espalhando mentiras',1])])]],
 
 #HOSPITAL
'OLD MAN': [['É bom você sempre','tirar dúvidas com o','entendido do assunto.',1,'Minha filha comprou um','antibiótico e pensou que','era pra beber.',1,'Agora ela tá no hospital...',1,'Essa menina...',1]],
'INJURIED DAUGHTER': [['É bem vergonhoso dizer o motivo',1,'Mas estou internada porque','bebi antibiótico',1,'Devia ter escutado meu pai...',1]],
'PRETTY MOM': [['Minha filha tá me','pertubando pra levar alguns','doces pra ela.',1,'É assim toda hora,','ela vai parar já já.',1]],
'PRESSING CHILD': [['Mãe!','Tem tantos doces aqui!',1,'Eu quero!','Eu quero!','EU QUERO!',1]],
 
'DOCTOR': [['Você sofreu várias fraturas no corpo.',1,'A conta dos cuidados foi de','$100 por pessoa.',1]],
'WORRIED NURSE': [['Você deveria se cuidar mais.','É muito comum te ver por aqui.',1]],
'HINT NURSE': [['Tome cuidado com sua vida!',1,'Não digo por causa da saúde, mas pelo dinheiro.',1,'Se não tiver dinheiro da próxima vez, pode','entrar em prejuízo.',1]],
'PATIENT': [['Eu quero ir pra casa logo!','A comida daqui é horrível!',1]],
'IMPATIENT PATIENT': [['Eu tô na fila desde anteontem','Parece até que nunca anda!',1]],
 
'BANK GUARD': [['Ponha qualquer objeto de metal que tiver','na caixa ao lado.',1]],
'UNLUCKY MAN': [['Não é possível','uma coisa dessas!',1,'O caixa acabou de entrar','em manutenção!',1,'ERA MINHA VEZ!',1]],
'OLD WOMAN': [['Como que faz pra','tirar a telesena aqui?',1]],
'SUSPICIOUS MAN': [['Estão falando que tem uma anomalia','solta na rodovia.',1,'Sendo honesto, eu não acredito','que existam anomalias.',1]],

#PROLOGUE DIALOG
'HHINTRO': [[(27,100),0,'Quem está aí?',1,2,(29,'hauntedhouse_0',0,0)]],

'DALIBOR': [['VEM AQUI TODO MUNDO!!',1,0,'Que foi isso?!!',1,2,0,(26,4),(24,None,(184,370),8),(24,1,(180,350),2,'stand'),(24,2,(230,380),6,'stand'),(24,3,(200,330),2,'stand'),(24,4,(230,350),4,'stand'),(27,70),(25,4,'L'),
'Estão todos os mercenários aqui?',1,(25,4,'LD'),0,'Não, tem um lá fora e outro','não chegou ainda.',1,(25,4,'DD'),0,'Ah pronto.',1,'não tenho idade pra essas coisas...',1,(25,4,'D'),
'seguinte...',1,'vamos fazer assim então.',1,(25,4,'LD'),'você.',1,0,'quem, eu?',1,0,'Sim! você!','Pode falar o nome e sobrenome','de vocês seis?',1,(10,['Não ( nomes padrões )','Não sabe?',1,(25,4,'LU'),'Era só o que me faltava...',1,(25,4,'L'),
'então a mulher do seu lado','vai me dizer.',1,'Beleza?',1,(22,False)],['Sim ( nomear personagens )','Ok,','Tenha o tempo que quiser.',1,(22,True)]),'Muito bom,','Quando todos chegarem','nós vamos dar início ao','interrogatório.',1,
(24,4,(330,300),3,'seat'),(27,20),(26,1),(27,20),(25,1,'D'),'Esquisito.',1,'Eu imaginava que um interrogatório','fosse bem mais...',1,'...pesado.','digamos assim.',1,0,'Verdade...',1,(25,1,'DD'),0,(27,30),(21,'DALIBOR',1),(23,'HHBIANCA',1)],
['Chame todo mundo pra','começar as gravações,','por favor.',1],
['Estão todos aqui',1,'vamos começar?',1,(10,['Espera um pouco','Venha quando','estiver pronta.',1],['Podemos','Excelente.',1,'Atenção!','Põe essa máquina','pra rodar!',1,3])]],

'AGENT 1': [['Tá procurando alguém?',1,(10,['Não','Tudo bem',1,'Se estiver precisando','de ajuda, é só','falar',1],['Sim','Eu vi um homem subindo','as escadas',1,'Deve estar lá','em cima',1])]],

'AGENT 2': [['Vocês entraram em encrenca',1,'Tem noção do que seus','preciosos olhos testemunharam?',1,(10,['Do que tá falando?','Não se faça de besta!',1,'Espero que tenha','muita coisa pra',
'contar para o','Senhor Dalibor!',1],['Nem imagino','Você não tem noção',1,'Nunca antes se','viu um evento','dessa magnitude',1,'Por isso mesmo','nós precisamos que','vocês contem tudo','pra gente',1],
['Eu tô com pressa','Que isso',1,'Se acalma',1,'Bebe um copo','de água',1,'Você vai ter','bastante tempo','quando falar com','o Senhor Dalibor',1])]],

'HHSIDNEY': [[0,'Oi, ',(3,0,'.'),1,(27,100),(3,0,'?'),1,0,'Oi ',(3,4,'.'),1,0,'O que tá fazendo?',1,0,'Nada não...',1,'Só apreciando a vista...',1,0,'Ah sim...',1,(24,None,(None,None),8),(27,100),
0,'A noite não é linda?',1,'É a minha parte favorita do dia.',1,'Ficar vendo as estrelas...',1,'As pessoas não tem mais','tempo para essas coisas','hoje em dia.',1,(10,['Verdade','Tem muita coisa que as','pessoas perdem por causa','do tempo delas.',1,
'as pessoas deveriam aproveitar','mais as coisas a sua volta.',1,(27,100)],
['Estava falando com ela?',(27,200),'Não é surpresa nenhuma...',1,'...né?',1]),'O que veio fazer aqui?',1,(10,['Queria saber como estava.','Ah..',1,'Valeu...',1],['Lá dentro tá chato.','Pior...',1]),(30,(320,520),'051011','HHLUCY'),
'Olha lá.','É a ',(3,5,'.'),1,(6,'CH01',False),(21,'HHSIDNEY',1),(21,'HHJANE',1),(21,'HHLUCY',1),(28,'NOTIFICATION'),(18,[0,0,'HHJANE'])],
['Eu já vou.',1,'Espera só um pouquinho.',1],
['...',1,'A lua está mesmo linda',1,(27,300),'Tem algo de estranho nessa lua','Não é possível',1]],

'HHJANE': [['Por favor vê onde',1,'O ',(3,0,' foi.'),1],
[(24,None,(None,None),2),(30,(150,220),'011014','HHJANE'),(15,'DOOR_KICK',0),(27,60),0,'Você sabe bater a porta?',1,0,'Desculpa aí.','Achei que tinha ninguém',1,(21,'HHJANE',2),(18,[1,9]),(28,'SIGNALI')],
['Melhor você entrar',1,'Estão te esperando',1,'Ainda mais o ',(3,3)]],

'HHRENAN': [[0,'Onde será que está esse miserável?',1,(29,'highway040',1160,360),0,(31,'Puta que pariu','Que merda'),'espero não estar atrasado!',1,(21,'HHRENAN',1),(18,[2,None])],
['Finalmente',1,(24,None,(390,160),6),(26,2),0,'Eu demorei muito?',1,0,'Tá todo mundo lá dentro','esperando você.',1,0,'Putz...',1,'Tive que resolver uma parada','antes de vir pra cá.',1,'Mas pra quê me chamaram?',1,0,'Detetives',1,0,
'Quê??',0,'Detetives vieram pra cá',0,'Como assim??',0,'Calma aí!',0,'Véi estamos muito ferrados!',0,'O Paulo tá de boa',1,0,'Como assim?',1,0,'Pô como ninguém ia saber','o que aconteceu depois daquilo?',1,0,
'Sei lá!','Mas o que vieram fazer aqui?',1,0,'Nem eu sei direito...','Mas eles são da PM',1,'Vão entrevistar a gente',1,0,'Beleza...',1,0,'Entra lá dentro que','Só falta você.',1,(21,'HHRENAN',2),(21,'HHDIEGO',1)],
[(6,'drink_beer',['Eu espero você.',1],['Aí sim meu rapaz!',1,'Mano, sabe onde a ',(3,5,' tá?'),1,(10,['Não faço idéia','Putz.','Preciso resolver um negócio com ela.'],['Estava no banheiro','Ah...','Valeu']),'Já volto já.',(21,'HHRENAN',3),(18,[2,9])])],
['Você tá carregando muita tralha!',1,'Aproveita para jogar fora','esse lixo na sua mochila',1]],

'HHDIEGO': [[(10,['Oi ',(3,3),'E aí',1],['Sabe onde está o ',(3,0,'?'),'Velho,','acho que ele tá lá fora.','atrás da casa.',1,
(10,['Obrigada.','Valeu',1],['Ah tá','Deve estar falando','com aquela garota','de novo.',1,0,'Já imaginava.',1])])],
[(3,2,'!'),'Finalmente!',1,(10,['O que aconteceu?','Nem queira saber','A gente encontrou um espírito','aqui nessa casa',1,0,'Não brinca',1,0,'Tô te falando.',
'Queria ver tua reação.',1,0,'Aí, mal aí por não ter vindo','Se não estivesse ocupado eu','ajudava vocês',1,0,'Que nada cara, tranquilo',1],['Já vai começar a entrevista?','A gente ia começar',
'Mas o ',(3,0,' tá falando'),'no celular',1,0,'Não é a...',0,'Sim, ela mesma.',1,0,'Putz...',1,0]),'Aí vou buscar alguma','coisa pra gente',1,0,'Beleza',1,(18,[3,7,'HHRENAN'])],
[]],

'HHBIANCA': [['O que foi?',1,0,'Era Iago.','Perguntou se eu tava bem.',0,1,'Ah tá.',1,'Pelo menos ele se preocupa','com você.',1,0,(25,None,'DD'),'Sim.',0,1,(27,100),'Percebeu onde a gente.','conseguiu chegar?',
1,0,(25,None,'LD'),'Como assim?',0,1,'Ás vezes nós não','nos damos conta...',1,'...mas agora a pouco eu','era pesquisadora,',1,'e agora além de tudo a gente','sai pra caçar monstros.',1,'não é esquisito?',1,
(10,['Não são monstros','Você entendeu o que eu','quis dizer!',1],['Muito esquisito','Não é?',1]),'Isso parece até coisa de filme.',1,'Mas isso não é errado?',1,(10,['Acho que não','Mas por que?',1,0,
'A gente não está salvando','as pessoas?',1,'Eu acho que isso é o','que importa.',0,1],['Eu não ligo','Sei não...',1,'Não gosto dessa coisa de matar','bichinhos.',1,0,(24,None,(None,None),5),(25,None,'L'),'Mas não são bichos, garota!',0,1]),
'Eu sei',1,'Mas mesmo assim...',1,0,'Ei',0,1,'O quê?',1,(10,['Não se culpe por isso',0,'No começo parece que','você está fazendo a coisa','mais cruel do mundo,',1,'se já deve ser difícil',
'pra quem trabalha na polícia,','imagine pra gente!',1,'Nós apenas estamos fazendo','o que é melhor pra todos.',0,1],['Eu já me acostumei',0,'Não ligue para o que os','outros dizem.',1,
'Eles não são a gente','pra dizer alguma coisa!',1,'Se estivessem no nosso lugar','fariam o mesmo.',0,1]),'Sim, mas...',1,'...',1,'...precisa ser matando...?',1,(21,'HHBIANCA',1),(23,'DALIBOR',0)],
[0,'Viu o ',(3,0,'?'),1,(25,1,'D'),0,'Não, não vi...',1,0,'Vê onde ele está, por favor?',1,0,'Tudo bem.',1,(18,[4,1,'HHJANE']),(28,'WALK')],
['Ei, você viu','se ele já voltou?',1,(10,['Eu ia perguntar isso','É, ele não aparece',1,(10,['Pode procurar ele?','Claro'],['Não vi ele','Ele tá demorando','muito...',1]),'Eu já volto',1,(18,[4,1,'HHLUCY'])])],
[(3,3,'!'),'Quem mandou você entrar aqui??!!',1]],

'HHLUCY': [['O ',(3,2,' tá demorando muito.'),1,'Acho que vamos ter que','começar sem ele.',1],
['E aí ',(3,0,'.'),'Daqui a pouco vão começar a entrevista',(10,['O ',(3,2,' chegou?'),'Ainda não...','Mas já deve estar chegando.',1,
'O Dalibor está pensando em','começar logo sem ele.',1,0,'Quem é Dalibor?',1,0,'O detetive.',1],
['Espera eu terminar','Muito ocupado você hein...',1]),'Então tá.','Quando acabar aí vem pra sala.',1,(21,'HHLUCY',2),(21,1),(18,[5,2,'HHSIDNEY'])]],

'HHBASEMENT': [['O que é isso?',1,(15,'TREASURE',0),(27,100),(1,'mysterious',0,'HHBASEMENT'),'Que esquisito.','Preciso mostrar pra ',(3,4,' depois.'),1,'Espera',1,'Ah não...',1,(13,['missingno3'])]],

'HHMERCHANT': [['Hey!',1,'Psiu!',1,(27,20),'Aqui!',0,'Que susto mano!',0,(10,['Que tá fazendo aí?','Eu tô no armário',1,(15,'LAUGHS',0),(27,120)],['Isso é hora cara?','Preciso arrumar meu trampo',
'Não tá fácil pra ninguém']),0,'Você não devia estar aqui.',1,'Tá rolando mó treta aqui','por causa de uma assombração.',1,0,'Nem pensar.',0,'Papo reto','É o que me disseram.',1,0,'Olha',
'Eu posso até não acreditar,','Mas sejam dias de luta ou','dias de glória eu vou','continuar meus negócios.',1,'Não quer descolar nada não?',1,0,'Agora não véi',0,'Sabe que te considero muito né?','Você é meu mano né não?',0,
'Sim mas-',0,'Ajuda o parça aqui pô','Vai me deixar na mão?',0,'AGORA NÃO DESGRAÇA!',1,0,(3,2,'?'),(24,None,(None,None),3),(30,(260,200),'051011','HHLUCY'),0,'Ah, oi',(3,5),'Tava te procurando',1,0,'Mesmo?',1,
'Todo mundo tá procurando você!',1,0,'Sério?',1,0,'Sim! o que tá fazendo aí?',1,0,'Tava só-',0,'Vai logo pra sala!',(21,'HHRENAN',3),(18,[5,10,'HHRENAN'])]],

'HHCLIFFS': [[(28,'CLIFFS')]],

#DUPLO ANDANTES
'CH1BLUEBULLDOG': [[(31,'CARALHO!!','MERDA!!'),1,0,'O QUE FOI ISSO!?',0,'EU NÃO SEI!',1,(27,200),'A gente deveria dar uma olhada?',1,(10,['Você vai sozinho!','Tá bom, tá bom,',0,'Fica aí que eu já volto.',1],
['Melhor a gente olhar','Ok...','...mas vamos devagar.']),(27,500),0,'ai meu deus.',1,'AI',1,'MEU','DEUS',1,0,'Fica calma ',(3,1,'.'),'Tá tudo bem...',0,
'COMO ASSIM TUDO BEM!?','A GENTE ATROPELOU UM BULLDOGUE ' + NAMES[0] + '!!',(31,'PUTA QUE PARIU!','MISERICÓRDIA!!'),1,(27,20),'A gente não pode deixar isso aqui!',1,'Que que a gente faz?!',1],
[(27,300),'Me desculpe bem.',1,'Não havia nada que','possamos fazer.',1,(27,300),0,'Iago...',1,'O que é isso?',1,(27,200),0,'Mais um...',1,'Bul...','...dogue?',1,0,'Não...','É....','Não pode ser....',1,(27,200),
'CORRE IAGO!!',0,'COMO É?',0,(31,'CORRE BUCETA','NÃO PARA'),'ELE TÁ VINDO!!',0,'ISSO É LOUCURA!',0,'AAAAAHHH!!!',0,'AHHHHHH!!!',(13,['bluebulldog'])],
[(27,100),0,'O que foi...','Esqueçe isso.',1,(27,300),'Vamos chegar em casa',1,'E fingir que nada disso aconteceu.',1,'Se tiver acontecido mesmo.','Talvez eu tenha bebido demais.',1,0,'Você tá dirigindo.',1,0,'Nunca se sabe.',1]],
'CH1JANE': [['Amor.',1,0,'Que foi.',1,0,'Tô indo fazer compras.',1,0,'Tá bom','Vai com Deus.',1,(27,200),'Traz um salgadinho pra gente',1,0,'Tudo bem.',1]],
'CH1IAGO': [[0,'O que você tá vendo?',1,0,'O jornal','não tá vendo?',1,0,'Mas o que está assistindo','no jornal?',1,0,'Eu que pergunto...',1,'O que é isso?',1,(23,'CH1FIOCRUZ',0)],
['Deus me livre.',1,'Estão assaltando até','as universidades.',1,'Onde esse país vai parar?',1,0,'Não é?',1]],
'CH1FIOCRUZ': [[(15,'TVNEWS',0),(27,200),'Nessa tarde de quarta-feira,','um grupo de assaltantes mercenários','acabou de invadir a Fundação Oswaldo Cruz','em Manguinhos, no centro da cidade','de Rio de Janeiro.',1,'A polícia militar já se encontra','no local e estão negociando','com os criminosos á respeito dos','cientistas e pesquisadores, que estão','sendo mantidos como reféns.',1,'A PM ainda desconhece','o motivo do assalto, visto que os','criminosos não possuem dinheiro e','não levaram os pertences dos reféns.',1,'A operação delicada continua','desde as 9h da manhã e até agora','nenhum refém foi liberto pelos bandidos.',1,(23,'CH1IAGO',1)]],
'CH1MRKITE': [['Obrigado pelo café.',1,0,'De nada senhor.',1,0,(27,100),'Sabe, é disso que eu gosto','desse local.',1,'O serviço, os funcionários...',1,'Dá para ver que os chefes sabem','mandar nessa gente!',1,0,'Pois é.',1,0,'Mas então,','sobre o que estava falando antes,','eu pessoalmente acho que','esses bicho aí podem','lucrar muito, sabe?',1,'Mas esse povo sabe','Eles não conseguem enxergar','o tanto de lucro que eles','poderiam estar ganhando!',1,'Pode ver que o povo','lá da cidade, lá de, de...',0,'...Varginha?',0,'Lá em Varginha,','o pessoal tá aproveitando!',1,'As pessoas dizem que eles','estão se aproveitando,','tão ganhando dinheiro de tudo,','isso aquilo, mas poxa!',1,'Né não?',1,'A gente que é empresário precisa','buscar novas oportunidades!',1,0,'É verdade.',1,0,'E esses bichos abrem','portas para novas oportunidades!',1,'Tanto para a gente que','bota as coisas pra funcionar',1,'quanto para os clientes que','vão conseguir um novo tipo','de entretenimento!',1,0,'Mas deixa eu te falar, senhor,','as pessoas ainda não confiam nisso não!',1,'Todos esses anos','As pessoas já se aproveitavam',0,'Não sim...',0,'desses casos estranhos sabe',0,'Claro, claro',0,'e o povo não quer mais','ser enganado!',1,0,'Mas aí que tá!','Tá começando á vir á tona','tudo isso daí!',1,'Tá muito mais fácil para','as pessoas acreditarem nas aberrações','agora que tá tendo muito','mais aparição!',1,'E quem que não vai querer','olhar uma de perto','agora que tem gente poderosa','envolvida nisso?',1,'Agora que todo mundo','se sente um pouco mais seguro','para se entreter com esses mistério?',1,0,'É né...',1,0,(27,100),'Que tá fazendo aqui?',(10,['Nada não','Estava escutando a gente, não é?','É feio ficar escutando','as conversa dos outros, hein?',1,(27,100),'Tinha que ser mulher,','fofqueiras...',1],['...','É uma conversa particular!','Vai varrer outro quarto!',1,(27,100),'Com empregada a gente','faz assim!','A gente manda e elas','fazem!',1]),'Enfim...','Eu quero trazer uma revolução','no mundo do entretenimento.',1]],
    
#SANGUE VERDE
'CH2PIETRA': [[0,'Olá?',1,(27,100),'Eu tô apertada sabe?',1,0,'j-já vou sair!',1,0,'Eu espero...',(27,100),'Finalmente...',1,0,'...',1,0,'...você tá bem?',1,0,'não.',1,(27,20),'ah...desculpa...',1,0,'Você não tem culpa de nada','Por que você tá chorando?',1,0,
'Nada demais','sério não precisa se preocupar',1,0,'...tá bom então...',1,0,'Só um desgraçado que não liga','pra ninguém e só se importa','com ele mesmo!','Nunca tem tempo pra nada!',1,'E ainda cobra de mim!',1,0,'...é um cara?',1,0,
'A gente não se vê faz meses,',1,'só conseguimos se falar por telefone.',1,'Ele sempre diz que vai','voltar algum dia mas nunca vem!',1,'Bom...pelo menos ele se importa...',1,'...',1,0,'...não?',1,0,'Ele finge que se importa,','fica fazendo falsas promessas','e me fazendo de otária!',1,0,
'É seu namorado?',1,0,'Não...','Quer dizer...','Não mais...','Ele era...','É complicado...',1,'Você acha que deveria esquecer?',1,0,'Honestamente...',0,'...',1,0,'Sim, você deveria',1,0,'Mas eu ainda gosto dele!',1,0,
'Problema seu','Você tem que parar de','se prender á pessoas que','não te fazem feliz,','a vida é assim',1,0,'Nossa que duro',1,0,'Que nem sua cara bateu no muro',1,0,'Afe, para!',1,0,'Tá bom, mas é sério,',1,'vai fazer bem pra você.',1,'Uma hora isso passa',1,0,
'...entendi',1,0,'ok?',1,0,'ok',1,0,'Então tira essa lágrima do rosto','e vai se divertir.',1,'Se quiser posso ir contigo,','tá sozinha?',1,0,'Não, mas pode vir',1,0,'Ah, obrigada!',1,0,'Você DEVE vir',1,0,'Eu sei menina, relaxa!','Como se chama?',1,0,
'A menina que veio te caçar.',1,0,'Que isso garota pera aí...',1,(26,1),(24,None,(None,None),5),(27,300),0,'...Te caçei',1,0,'Ah fala sério!',1,0,'Obrigada por me escutar,','Mas preciso ir direto para','o que interessa',1,0,'Caramba, eu achei que tinha','criado um laço de amizade aqui!',1,0,
'Olha','Não tem nada a ver comigo,','me pediram para fazer isso,','tá bom?',1,0,'Fala logo o que você quer!',1,0,'Preciso das suas amostras.',1,0,'Elas estão no laboratório.',1,0,'Eu sei que estão no laboratório.','Você vai me levar até a sala onde','estão guardados e entragar para mim',1,0,
'Eu não faria isso!',1,0,'Olha','Eu não sou burra e','sei que se eu atirar','aqui dentro vão me prender,','mas eu posso muito bem te','fazer ir para meu carro com','a pistola nas suas costas!',1,0,'Você não faria isso.',1,0,'Não mesmo',1,'Mas adivinha?',1,'Eu tenho que fazer!',1,0,
'Ei pera!',1,(27,100),'Tá vindo alguém!',0,'Rápido se escon-',(13,['pietra'])]],

#NÃO SE META COM A GANGUE
'CH3PROLOGUE': [['Hey?','...','Está me ouvindo?','hm?','Você entendeu o que eu disse?','Pra ser sincera, não','...','Estava pensando, com a cabeça em outro lugar...','...sobre o quê você estava pensando?','...eu...eu fiz\
 coisas...','...','...eu fiz coisas que...tantas coisas...que não...pensei direito','...','...eu me arrependo tanto, nada disso deveria ter acontecido, foi tudo por causa de uma briga, e eu trouxe essa desgraça\
 pra minha vida...eu achei que poderia ajudar nós dois, achei que eu seria aquela que iria nos tirar do buraco...','...','...mas no final eu só afundei ainda mais....','é natural pensar coisas assim, mas tente sempre\
 se lembrar que o que você fez você não fez por mal, você estava querendo ajudar, achar uma solução','...sim...','isso não te anima?','nem um pouco...porque eu atrapalhei ao invés de ajudar...não fui inteligente','é\
 difícil','muito...mesmo...','...','você está fazendo atitutes inteligentes agora, está procurando ajuda, reconhecendo seu erro, se afastando daquilo que te traz problema','...sim...','você precisa\
 continuar assim','...','ei','?','me prometa de que você nunca mais vai voltar a pegar em uma arma, certo?','certo! certo!','nem que um monstro apareça no mato ou um bandido invada sua casa, nunca, NUNCA MAIS, encoste\
 em nenhum arma!','...','está me ouvindo?','sim','ótimo...','...','já está na hora de ir','não pode ficar mais um pouco?','desculpa, mas pode continuar amanhã, eu também tenho sanidade mental','claro, \
desculpa...',[2,'990435671',True]]],
    
'CH3MAICON': [['Então...',1,'Como tá o trampo?',1,0,'Que trampo?',1,0,'Você sabe,','o de mercenário',1,(27,60),'Tá muito puxado?',1,0,'...bastante.',1,0,'Acho que já ouviu','alguns comentários sobre eles.',1,0,'Sim...',1,'Até demais, mas nem ligo.',1,0,
'Como não?',1,0,'Mano, foi graças á essa vida','que tô onde tô agora.',1,'Não vou deixar que alguns comentários','mudem minha cabeça.',1,'Eu gosto do que faço',1,0,'Sim, mas seria melhor você arranjar','alguma outra coisa né?',1,0,'Isso até eu quero né?',1,0,'Então por que você',' não sai dessa?',1,0,'Porque não dá cara!','Não vão contratar alguém','com ficha suja',1,0,'Ah, é mesmo...',1,0,'Além do mais eu já','me garanto onde eu tô,','se eu trocar de emprego ','posso ser demitido de novo',1,0,'Já passou perrengue demais, não é?',1,0,'Sim',1,0,'...sei não.','Ainda acho melhor você fazer','alguma outra coisa.',1,'Esse negócio de matar e','arriscar a própria vida...',1,0,'Que vida?',(27,300),0,'Ficou parecendo aqueles','adolescentes sadboys.',1,0,'É eu sei...',1,
'Eu já tô indo',1,0,'Deixa que eu pago essa',1,0,'Sério?',1,0,'Sim','É por minha conta',1,0,'Você é demais cara',(6,None,False)]],

'CH3JANE': [[0,'Teria sido melhor','ficar lá no bar',1,(27,300),0,'BORA LOGO!',1,'NÃO TENHO O DIA TODO!',1,'Que saco...',1,'Que demora',1,'Pra você ver né,','Até pra isso tem','toda essa baboseira',1,0,'Hã?','Ah, sim, sim, sim...',1,0,'Era pra ser um negócio rapidinho...','tranquilo, de boa, mas não!','Eu sou obrigada a ficar','aqui esperando!',1,0,'Eu já tô até acostumado',1,0,'Ai não ia me acostumar nunquinha,','deus me livre',1,0,'É que já é coisa da rotina,','todo ano tem isso.',1,0,
'É?',1,0,'Ahã...','só que agora saiu mais cedo,','geralmente é só lá pra setembro',1,0,'Você é mercenário?',1,0,'Sou.',1,0,'Ah...','Pra saber dessas coisas...',1,0,'Por que?','Você não é?',1,0,'Não, mas daqui a pouco','já tô virando uma!',1,0,'Mas aqui não é onde','renova a carteira?',1,0,'Não, disseram que o registro','é aqui também',1,0,'onde?',1,0,'no último guinchê',1,0,'Ah sim, agora eu vi',1,0,'Vem cá, e como é essa coisa','toda de mercenário, matar pessoas...',1,0,'A gente não mata pessoas',1,0,'Ah sim, desculpa...',1,0,'Não, tudo bem, é normal',1,0,'Então o que vocês fazem exatamente?',1,0,'Olha, a primeira coisa que','você deve saber se quiser','virar mercenária, é que certas','coisas são totalmente confidenciais',1,0,
'Uh! sério?',1,0,'Sim, sigiloso',1,0,'Tipo homens de preto né?',1,0,'Não é pra tanto,','Mas é tipo',1,0,'Mas eu achava que era só','matar e ganhar dinheiro!',1,0,'ihhhh...',1,'Vai sonhando, é um bicho chato',1,0,'Sério?',1,0,'Quer dizer, tirando toda a diversão,','ainda é um trabalho, tem que','estar sempre disposto, te chamam na','hora que querem, é cansativo,','tem os chefes, a gente recebe pouco...',0,'QUÊ?',0,'fala baixo!',0,'desculpa',1,(27,120),'...recebe pouco?',1,0,'depende do quanto você caça.',1,0,'Ah...então se eu','caço bastante...',0,'ganha bastante, isso aí',1,0,'Mas o que vocês caçam exatamente?',1,0,'segredo',1,0,'Ah! deixa disso!','Fala logo!',1,0,'Se quiser saber mesmo,','Vai ter que esperar até lá dentro',1,0,'tá bom então...',1,'Ô agente G',1,'Beleza James Bond',1,0,'tá já chega',1,0,'ei já tá na sua vez',1,0,'ah sim',1],
['Então esse é seu nome?',1,0,'Sim...',(3,0,0),1,0,
'Prazer, ',(3,1,1),1,0,'Prazer',1,0,'Então...o que tem que fazer agora?',1,0,'Bom, agora você pode','pegar sua primeira arma ali.',1,'E se quiser já pode treinar','Um pouco de tiro',1,0,'Você vem comigo?',1,0,
'Não...eu já tenho que ir',0,'Ah por favor!','Eu não entendo das coisas aqui!',1,'please!',1,(10,['Tá bom','YASS',0,'Não se empolga, tá.',1,0,'Então tá,','Onde que pega o brinquedinho?',1,0,'Me segue',(11,1)],['Agora não','Tudo bem então...',1,'A gente se vê por aí',1,0,'Eu tô aqui todo dia',1,0,'Beleza!',1,(27,180),'Ah! eu só posso vir','aqui nos sábados!',1,0,'Beleza!',1,0,'Tchau!',1,(27,210),0,'Essa garota tá querendo alguma coisa comigo...',(11,3)])],
['É aqui que faz o treinamento?',1,0,'exatamente',1,0,'Ok...',1,(27,60),'me ensina a atirar?',1,0,'Tudo bem',1,(9,2),'Primeiro põe esses óculos aí',1,0,'esses?',1,0,'sim, agora mira','Não põe muito perto','senão machuca o olho',1,0,'Já sei disso',1,0,'e...aperta o gatilho',1,(13,['target'])],
['Nossa!',1,'Mandou muito!',1,0,'Eu sou demais!',1,0,'Não sério,','Você já atirou antes?',1,0,'Um pouquinho',1,0,'Um pouquinho?!',1,0,'Tá, eu sei atirar',1,0,'Se você já sabia atirar,','por que pediu minha ajuda?',1,0,
'Ai,ai...','Faz muito tempo já,',1, 'Começei quando...',(5,0),0,'Pera aí rapidinho',1,0,'O que foi?',1,0,'Chegou email',1,(27,200),'Desculpa ',(3,1,', eu tenho que ir!'),1,0,'De novo?',1,0,
'É um caso pra resolver',1,0,'Agora?',1,0,'É o que eu te falei antes',1,0,'Posso ir com você?',1,0,'Vai devagar querida,','Eu tô em outro nível',1,0,'Por que não posso ir?',1,0,'Muita coisa ainda, muita coisa,','Te explico depois',1,0,'Pera aí! Mizera...']],

'CH3VINICIUS': [[(15,'battle_incoming',1),'O que tá fazendo aqui?',1,0,'Quem pergunta sou eu!','O que VOCÊ tá fazendo aqui?',1,0,'Com certeza não é deixar você','roubar minha recompensa',1,0,'E quem disse que ela é sua?',1,0,'Garoto,melhor sair do meio,','ou vai dar muito mal','pra nós dois',1,0,'que assim seja então!',1,(13,['madladcat','vinicius'])],
['Lembra de mim, filho da mãe?',1,0,'você!',1,0,'Essa é pra aprender a não mexer comigo!',(9,2),'???','O que você estava fazendo?',(10,[],[])]],

#CAMINHÕES CANAVIEIROS
'CH4PAUL': [['Vocês já estão chegando','no local?',1,0,'Não se preocupe.',1,'Nós estamos a caminho.',1]],

#PESTE NEGRA
'CH5RENAN': [[(15,'battle_incoming',1),'Você mexeu com a','turma errada, cara!',1,'Tá na hora de','aprender uma lição!',1,(13,['pietra'])]],

#VIDA LOKA
'CH6VINICIUS': [[0,'FIOCRUZ?',1,0,'Pois é.',1,0,'Por que a gente assaltaria','um lugar desses?',1,0,'Ele falou que lá dentro','tem uma coisa muito importante.',1,'Ao que parece são','amostras de sangue.',1,(27,20),0,
'...ele quer fraldar um teste de DNA?',0,'Eu lá vou saber cara!',1,'Mas parece que ele vai',' pagar bastante pra gente fazer isso.',1,'E a gente também tem algumas','informações pra nos ajudar.',1,
'Vocês estão sabendo da festa','que vai ter lá na Cinelândia, certo?',1,0,'ahã.',0,'então,','lá vai estar uma pesquisadora','que é a quem manda nas amostras.',1,'É só a gente ir atrás dela!',1,0,'Ah, vai ser moleza!']],
'CH6BIANCA': [['O QUE VOCÊS QUEREM?!',1,'Bora logo, ',(3,2,'!'),'Atrás dela!',1,(27,30),0,'Hã?',1,(27,20),'Sai da frente!',1,0,(3,2,'!'),'É uma emboscada!',1,'Não!','Eles estão malucos!',1],
[0,'Ela tá escapando!',1],['Quem foi que deu','Açúcar mascavo pra eles?',1]],

#PELO BENEFÍCIO DE MR. KITE!
'CH7MRKITE': [['Crianças malcriadas!',1,'Desse jeito o show','não vai ter graça!',1,0,'Quem está aí?',1,'Quem é você?',1,0,'Quem sou ou como me chamo','não é da sua conta!',1,
'Vocês estragaram o espetáculo!','Mas o show deve continuar!',1,0,'Já entendemos','Você é o cara dos shows',1,0,'Como você aprende rápido!',1,'Gostaria de aprender','alguns truques?',1,0,
'Dá um tempo cara.','Você não é vilão de','Scooby Doo!',1,0,'Pode até ser verdade','Mas no fim eu sempre','tenho uma carta na manga!',1,0,'Ele tá muito empenhado','nos trocadilhos.',1,0,'Gostou?','Eu decorei tudinho.',1,0,
'Achei massa!',1,0,'Muito obrigado.',1,'Como estava dizendo...',1,'O SHOW DEVE CONTINUAR!',1]],

#DR. ESTANHO
'CH8PIETRA': [['Isso tudo é muito estranho, cara.',1,'Semana passada o cleitinho disse','que não podia ir pro rolé','porque estava numa ressaca braba.',1,'Alguns dias depois a','Larissa fala que','tá sentindo uma cólica terrível.',1,
'E ontem o Breno estava','espirrando tanto que','desmaiou!',1,'O que é que está havendo?!',(10,['Deve ser coincidência','Ou deve ser muito azar, né?','Foi todo mundo','de uma vez só!',1],['Eu não sei','Eu também não...','admito que estou com','um pouco de medo.',1,'E se eu for','a próxima?',1,
(10,['Deus me livre, Pietra','Eu só to falando',1,'Pode ser que aconteça','comigo e eu não sei','o que fazer!',1],['Para de falar besteira!','Calma aí!','Tá bom!',1,'É que todo mundo','tá ficando desse jeito.'])]),(27,100),'Poucas idéias...',1,'Tudo isso tem que','ter alguma ligação!',1,0,'Estão espalhando por aí','que deve ser alguma doença.',1,'Tipo uma dengue,','só que muito pior.',1,0,'Meu Deus',(27,20),'É sério?',1,0,'Sim.','Deve ser por causa','desses pombos mortos','no meio das ruas!',1,0,
'Verdade.',(27,30),'Agora que você falou...','Eu não tenho mais','visto pombos vivos.','Só mortos.',1,(27,100),'Mas era trabalho','da prefeitura',(27,20),'cuidar disso daí!',(27,50),'Fica um fedor horrível','também!',(27,100),
(10,['Amor, você está bem?','Tô bem','Só tô com a','garganta seca.',1,(27,200),0,'Você tá tossindo','pra caramba!',1,0,'Eu vou',(27,20),'melhorar!',(27,30),'Tenho que',(27,200),'Tenho que ir pra',(27,300),0,(31,'Puta que pariu!','Meu Deus!'),'Vou chamar uma','Ambulância!',1],['Quer beber uma água?','bem queria','você tem aí com você?',1])]],

#MILÍCIA X MELIANTE

#NÃO IDENTIFICADO
'CH10HERMES': [[0,'Olá?',1,(27,60),'Alguém em casa?',1,(27,100),0,'Olá!',1,'Em que posso ajudá-los?',1,0,'Boa tarde senhor,','Essa fazenda é sua?',1,0,'Oh sim, é minha desde','que meu avô começou a capinar,','quando tudo isso ainda era mato!',1,0,'...mas só tem mato aqui senhor',1,0,
'Pois é.',1,'Faz um bom tempo que','não tem ninguém para','cuidar da minha fazendinha.',1,'Só resta eu e minha maloca...',1,0,'Mas esses animais também são seus?',1,0,'Ah não.','Apareceram aí!',1,'Não são criatuinhas de Deus?',1,
'Nossa ',(3,1,', tem um Boi Dourado ali!'),1,0,(3,3,'!'),'Se concentra!',1,'Então...nós somos...',1,0,'...detetives?',1,(27,120),'...sim! sim, detetive ',(3,3),'E minha colega, detetive ',(3,1,'.'),1,
'Muito prazer, me chamo Hermes.',1,'Eu já imaginava que fossem,','pois não tem uma semana','que alguém bate na minha porta!',1,0,'É mesmo?',1,0,'Sim! vocês não sabem?',1,0,'Não, viemos de outra cidade',1,0,'Ah...',1,'Vieram de onde?',1,0,'Vargi...',1,0,'Itatiaia!',0,'Pera, quê?',0,
'Não é que ele',0,'A gente acabou de vir de Itatiaia, mas estamos indo pra Varginha',1,0,'É, isso mesmo',1,0,'Interessante...',1,'É porque Policiais vieram','aqui perguntando um monte de baboseira...',1,'Umas presepada que','não sei nem o nome!',1,0,'Geóglifos?',1,0,
'Sim',1,'E acho que você gostariam','de saber algo a respeito, não é?',1,0,'Sim, o depoimento dos moradores','próximos é muito importante!',1,0,'Bom, eu não sei nada desses','Zoológicos coisa nenhuma.',1,'Mas por alguma razão','todos vem me perguntar',1,0,'É porque, Sr. Hermes,','os Geóglifos estão na sua fazenda',1,0,'Pois é, mas é justamente porque','ela está a tanto tempo parada','que não me informo','dessas coisas, entende?',1,'Talvez alguma pessoa tenha','invadido meus campos e fez','esses desenhos no mato!',1,0,'Hermes...',0,'Olha ',(3,1,', acho que já'),'conseguimos informações o','suficiente do Sr. Hermes.',1,'E aliás, acho que','um vândalo qualquer seria','mais suspeito do que','qualquer aposentado de','meia-idade',1,'Eu trabalho',1,'Ah, sério?',1,'Sim, eu vendo artesanato',1,'Boas vendas, Hermes',1,'Muito obrigado...',1,(3,3,'.'),(3,3,'!'),'Muito obrigado pela','ajuda de vocês!',1,'O prazer é todo nosso!',1,(27,120),0,'Por que fez isso?',1,0,'Muita gente já falou com ele.',1,'Se fizermos perguntas demais','ele pode fazer alguma coisa!',1,0,'O quê? destruir provas?',1,0,'Exatamente isso',1,0,'Por que ele faria isso?',1,0,'É o que estamos','tentando descobrir!',1]],

'CH10JANE': [['Ainda não entendo como','foi tão simpático com','aquele velho...',1,'Por que?','Você acha ele mau?',1,0,'Não...mas eu desconfio dele.',1,'Não deveria falar','desse jeito com ele',1,0,'Então o que você sugere?',1,0,'Seja mais duro?!',1,0,'Não dá pra gente','conseguir nada das','pessoas sendo duro com elas',1,0,'Os policiais conseguem',1,0,
'Ele é um cara muito suspeito,','isso a gente já sabe,','mas como ninguém conseguiu','tirar provas dele,','quer dizer que ele é','muito bom em guardar segredo',1,0,'Eu não sei...',1,'acho que a gente','devia sequestrar ele',0,
'Claro que não!',0,'Nossa calma!','Eu só tava falando...',1,(27,60),'Então o que a','gente vai fazer?',1,0,'Vamos continuar investigando',1,0,'Ah sim,','Claro que sim...',1,0,'O problema de leigos','como você é que eles','tentam começar de cima...',1,(24,None,(None,None),3),(27,60),0,'Como é que é?',1,0,'É a verdade',1,0,
'Olha me escuta aqui ',(3,3,'!'),'Você não sabe quem','eu sou e de onde eu vim!',1,'Então é bom você ficar','calado que aí você ganha','mais e não caga pela boca!',1,0,'Ok...',1]],

#QUÍMICAS QUIMERAS
'CH11SIDNEY': [[0,'Aí está você.',1,0,'Pois é...',1,'A gente já vai embora.','Precisamos capturar anomalias','para competir.',1,0,'Hã? Como é?',1,0,'Foi o único jeito.',1,0,'Achava que era','contra essas coisas!',1,0,'Agora as coisas são','um pouco diferentes',1,'Ou são 3 galos de combate','ou é toda a fauna da','mata atlântica.',1,'De quebra a gente','pode ganhar uma grana!',1,0,'Ah sim...',1,'Tem isso aí...',1,0,
'Falando nisso, onde','estão meus 300 reais?',1,0,'Então...',1,(27,60),0,(3,0,'.'),1,'Cadê meus 300 reais?',1,0,'Olha só tenta','entender a situação.',1,'Eu queria ajudar a gente','apostando dinheiro nas','anomalias de combate.',1,'Eu tava indo bem,','bem pra caramba.',1,'Só que...',0,'Só que o quê?!',1,0,'Bom...',1,'Como tava ganhando muito','eu fui logo com tudo.',1,
'Então apostei todo o','dinheiro que a gente tinha.',1,(27,300),0,'Oi?',1,'A gente ia ganhar o dobro!',0,'CARA QUAL É TEU PROBLEMA!!',0,'VOCÊ FARIA O MESMO!!','EU TAVA ENRIQUECENDO A GENTE!!',0,'Eu não acredito nisso','Era o bolsa família da minha mãe',0,'Tá e o que você quer','que eu faça?',0,
(31,'QUERO QUE VÁ SE FUDER ',(3,0,'!'),'QUERO QUE VÁ SE FERRAR ',(3,0,'!')),0,(31,'VAI TOMAR NO CU TAMBÉM','VÁ TE CATAR TAMBÉM'),(27,180),0,'Eu preciso desse dinheiro...',1,'Você nem tem noção...',1,0,'Ok...eu tô te devendo essa.',1,'Eu vou te ajudar a','capturar algumas pestes.',1,0,
'Eu ia te chamar','de qualquer jeito!',1,0,'Tá bom!','Se acalma!',1,0,(31,'Puta que pariu...','Misericórdia...'),'Vamos embora logo...',1]],

#QUEM ACREDITA EM ASSOMBRAÇÃO?
'POLTERGEIST': [[(10,['Você está aqui?',(27,120),'Mexeu!','Como isso é possível?',0,'Silêncio!'],['Charlie Charlie'])]],

#MP-XIII
'CH13PIETRA': [['VOCÊ É INSUPORTÁVEL!',1,'O QUE FOI QUE EU FIZ?!',1,'EU VOU TE MATAR!!',1,0,'Pietra!','Aguenta firme!',1,(23,2,'!'),'Mete bala logo!','Só não me acerta!',1,'Você tem demência mulher?',1,'Não pedi sua ajuda também!',1,(27,100),'Amor! Me ajuda!!',1,'Me espera!',1]],
'CH13SIDNEY': [[0,'O que é que eu','estou olhando?',1,0,'Parece um dragão, cara.',1,0,'Não pode ser.',1,'A gente tá chapando, né?',1,0,'Se fosse isso a gente','estaríamos chapados','desde ano passado.',1,0,'Como assim velho...',1,0,'Ok...',1,'Ele só tá voando, né?',1,'Pelo menos ele não tá...',(27,100),'...merda.',1,0,'Ele tá destruindo','a cidade?',1,0,'É o que você','tá vendo, né?',1,0,'Não quero acreditar','nos meus olhos.',1,0,'E o que a gente','deveria fazer agora?',1,(27,100),'Vou lá saber.','Dá não.','Vamo simbora.','Puxar o carro e já era.',1,0,'Vocês não estão','nem aí pra isso?',1,(27,100),'Desculpe',(3,1),'É que realmente','não temos mais','o que fazer!',1,0,'Eu vou rezar',0,'Eu também','Boa',1,0,'Olha gente...','Eu sei que parece','uma tarefa difícil.',1,'Mas não podemos deixar','que o tamanho dos nossos','problemas sejam maiores','do que nossa força de','vencê-los!',1,'Os gigantes da vida estão','apenas nas aparências!',1,'Com força e união nós',0,'Tá bom já entendi','psiquiatra da facul!',1,'Vamos se armar e ir','para o centro!',1,'Estou pensando em usar','os prédios para atirar','mas seria muito arriscado.',1,'Precisamos achar a','fraqueza dele primeiro!',1,'De repente seria',0,'Subam!',1,0,'Eu tava falan',0,'Não enrolem seus molengas!','Tem um dragão na cidade!','Subam logo!',0,'Vamos logo gente',0,'Eu tô com medo mas tô empolgado!',0,'Sei nem mais o que','tô sentindo!','Só deixo rolar!',1]],

#CONTACTS CALL
'89074454': [['Sidney']],
    
'91124257': [['Oi! Sou eu, a Jane']],
  
'90435671': [[[(3,1,'!'),'Precisamos de você aqui AGORA!','Eu sei que você saiu e coisa e tal, mas a gente PRECISA DE VOCÊ!','Estamos na Av. Jobim, venha logo!',[4, 'Urgência na Av. Jobim']],
['Caramba ',(3,1,', será que você'),'não entende a gravidade da situação??','Só você pode deter essa anomalia!']]],
    
'26148930': [['E aí mano? Beleza?','Então, aquela parada da transferência deu certo, adivinha?','Amanhã á noite eu tô indo pra Nova Friburgo!',0,'Tá tendo umas paradas estranhas lá, e me mandaram examinar','Vamos aproveitar pra gente se ver, beleza?']],
  
'76564008': [['Agora não, ',(3,0,'!'),'Eu tô trabalhando!','Me ligue depois, estou fazendo coisa importante aqui!']],
  
'40028922': [['Oh, olá! como vai, ',(3,0,'?'),'Tenho andado ocupada esses dias, muita coisa pra fazer...','Não dá pra falar com você agora, desculpa','Me ligue mais tarde, ok?'],
['oie']],
    
'90271802': [['Garoto, o chefe quer te ver o mais cedo possível na delegacia',1,'Espero que não tenha feito merda...',1,'Bláblabla','blablabla','blablabalbala','blablablaba',1,0,'entendeu?',1]],
    
'87690021': [['Paulo']],
  
'53478809': [[(3,'time',', em que posso ajudar?'),(10,
	['uma pizza de frango','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY CHICKEN'})],
	['uma pizza de 4 queijos','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY 4CHEESE'})],
	['uma pizza de calabresa','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY SHAGGY'})],
	['uma pizza de mussarela','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY MUSSARELLA'})],
	['foi um engano','Ah, entendo.','Tenha um bom dia.',1])],
['Alô? É Você?','Espere um instante, já estou','aí a qualquer momento.',1]],
  
'09236521': [[', correios']],
  
'23778988': [['Alô?',1,(16,0,[(3,0,'!'),'a quanto tempo cara!',1]),'Precisando de ajuda em','carregar algumas coisas?',1,'Não tem problema, o pai tá aí','pra resolver já já!',1,
(17,'deliver',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'DEPOSIT'})],
['Oi?','Ah sim, daqui a pouco','já chégo aí.',1]],
  
'69696969': [['Olá cliente, em que posso ajudar?','você está a procura de meus serviços?',(10,
	['Sim','chegarei em instantes',1,(17,'delivery',600,{'TYPE': 0, 'INDEX': '001003', 'WHO': 'MERCATOR'})],
	['Não','Ah, tudo bem','Mas qualquer coisa eu tô por aí','beleza?',1])],
['Alô? É tu?','Pera aí doido eu','já tô chegando.',1]],
  
'77904623': [['Hey!','Você está bem?','Onde você tá?','O que tá acontecendo?','Você se machucou?',(10,['Eu tô bem','Mesmo?',1,'Ufa...',1],['Fique calmo','Não consigo me acalmar',1]),'Eu estava preocupado','com você',1,
'mas graças a','Deus você está bem',1,'Aquela mulher chamando','vocês aos prantos me','deixou assustado',1,'Você deve estar','cansada depois de','tudo o que passou',1,'Engraçado, não é?',1,'Você mal saiu','dessa coisa de mercenária',
'e já tá na ativa','novamente',1,'Mas assim...',1,'...',(10,['Pode falar','não...','é que...',1,'Não quero que a gente','se afaste de novo',1,'Não agora que tá','tudo dando muito certo',1,'Não precisa ser','que nem seu amigo','mercenário',1,
'ah é, esqueci','de te contar',1,'Eu fiquei sabendo','dele e tudo isso','sobre aquela garota',1,'bem problemático',1,'Não...',1,'Esquece eu só','falei besteira',1,'Só quero que','você não seja','ausente como eu','fui com você',1,'entende?',1,
(10,['Sim','Ainda bem que','entendeu',1],['Não','Esquece isso',1])],
['Eu já ligo de volta','Tudo bem','Você deve estar','muito ocupada agora',1])
,'A gente se fala mais','em casa, então',1,'te amo, ok?',1]],
  
'23578103': [['Sofia']],
  
'60428331': [['Vinícius']],
 
'78543322': [['Oi, em que posso ajudar?','Ah...eu já parei de fazer isso há muitos anos','Tchau']],

'40028922': [[(14,[99,'Que pena...','Não foi dessa vez!',1,'Tente novamente em','outra hora!',1],[1,'Alô?',1,0,'Alô!',1,0,'Quem fala?',1,0,(3,'self','.'),1,0,'Que legal!','Quantos anos você tem?',1,(10,['Tenho 12 anos.','Muito bom!',1,'Seguinte',(3,'self',', nós vamos','fazer uma brincadeira.',1)],['Eu tô nos meus 20.','Minha nossa!','Você não é muito velha','para assistir esse programa,',(3,'self','?'),1])])]],

'66666666': [['Você vai morrer em sete dias.',1]],

#EASTER EGGS
'MATRIX GUY': [['Você nunca se questionou','sobre nossa existência','dentro do universo?',1,(15,'THE_X_FILES',1),'e se nada disso for real?','e se tudo for apenas','uma enorme simulação?','é tudo ilusão','da nossa mente?','ou vivemos dentro','de uma matrix','como dizia Platão?',1,'E SE TUDO ISSO','FOR APENAS UM JOGO???',1,(27,100)]],
'TWNN CLOCK': [['Você tem a hora certa?',1,(15,'TWNN',0),(27,300,'TWNN'),0,'Não.',1]],
'KONAMI GUY': [['Hey, sabe o que acontece','se você apertar cima, cima,','baixo, baixo, esquerda,','direita, esquerda, direita,','B, A e START?',1,'Merda nenhuma!',1]],
'MATT KAI': [['EU AMO PINK FLOYD','EU AMO PINK FLOYD','EU AMO PINK FLOYD',1,0,'Esse é o criador do jogo?',1,0,'Ele mesmo',1,0,'Sem nexo',1,0,'Mó fita',1]],

#ADVICE
'ADVICE': ['Desculpe interromper','Mas é uma história muito longa','para se contar.',1,'Não vai querer continuar amanhã?','Nós gravamos tudo o que você falou',1,'E então?',(10,['Tudo bem','Ótimo','rapazes, guardem suas coisas',4],['Espere um pouco','Tá bom então...','vamos prosseguir',1])],
}

res.DLGSAV = {}
for i in DIALOGS.items(): res.DLGSAV[i[0]] = 0
		
for i in ITEMS.items():
	if i[0].startswith('food'): res.DISITEMS[i[0]] = 0
	if i[0].startswith('drug'): res.DISITEMS[i[0]] = 0

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
'Inventory': 'inventário','volume': 'volume','weight': 'peso','discover': 'Use o item para obter informações.',
'storage': 'depositar','products': 'produtos','basket': 'carrinho','wash': 'lavar','mercator': 'mercador','trash': 'lixeira',
'armor': 'proteção','duration': 'duração','damage': 'dano','recharge': 'recarga','cadency': 'cadência','capacity': 'capacidade',
'gauge': 'calibre','vitality': 'vitalidade','hunger': 'fome','thirst': 'sede','storage': 'depositar',
'success': 'sucesso','fail': 'falha','touche': 'touché','strike': 'strike','ko': 'nocaute','one_more': 'oitra vez','miss': 'errou...','victory': 'vitória','perfect': 'perfeito','lost': 'derrota','level_up': 'foi promovido para',
'GPS': 'mapa','Contacts': 'contatos','Email': 'emails','Newspaper': 'notícias','Radio': 'música','Camera': 'galeria','Bestiary': 'bestiário',
'Tasks': 'tarefas','Status': 'ficha','Tactics': 'táticas','Achievements': 'conquistas','Rank': 'placar','Help': 'ajuda','Settings': 'ajustes','About': 'sobre',
'no_signal': 'sem sinal','no_credit': 'sem saldo','no_freaks': 'nenhuma anomalia registrada','empty': 'nada por aqui','calling': 'chamando',
'to_do': 'fazer','done': 'feitas','all': 'todas','unread': 'novas','read': 'lidas','groups': 'grupos','history': 'histórico',
'name': 'nome','birth': 'data de nascimento','hometown': 'naturalidade','rg': 'registrado','cpf': 'cpf',
'gameplay': 'geral','sound': 'áudio','controls': 'controles',
'lang': 'idioma','border': 'borda','hints': 'dicas','tutorials': 'tutoriais','cursor': 'cursor','dislexic': 'dislexia',
'sfx': 'som','music': 'música','tts': 'narrador','cc': 'áudio descrição','speed': 'velocidade','censorship': 'censura',
'bt_choose': 'escolba o botão','vibrate': 'vibrar',
'conf': 'confirmar','info': 'info','yes': 'sim','no': 'não','ok': 'ok','cancel': 'cancelar',
'not_email': 'Novo Email','not_contact': 'Novo contato adicionado!','not_wash': 'Sua roupa foi lavada!'}


"""
MENU = [
'créditos: ','chamando...','DE: ','PARA: ','nova tática','VITALIDADE: ','FORÇA: ','ATAQUE: ','AGILIDADE: ','RESISTÊNCIA:',
'RESFRIADO','FEBRE','SEDE','NÁUSEA','PARALISIA','INCONSCIÊNCIA','PARASITA','QUEIMADURA','VENENO','HEMORRAGIA','REFORÇOS','ROUBAR',
'equipamento 1','equipamento 2','equipamento 3','equipamento 4','dialogar','defender','fugir','mover cima','mover baixo','mover esquerda','mover direita','ato','celular','inventário','velocidade,
Nome','Sobrenome','Tudo certo?','Sim','Não','Tem certeza?','correr','muito lento','lento','médio','rápido','muito rápido','jogador 1','jogador 2','jogador 3','habilitar','ícone','sensibilidade']
"""

HOLIDAYS = [(1,1,'Feliz ano novo!'),(3,8,'Feliz dia da mulher!'),(3,15,'É aniversário do autor!'),(4,7,'Feliz páscoa!'),(4,22,'Feliz dia da terra!'),(10,31,'Feliz Halloween!'),(12,25,'Feliz natal!')]

RADIOEE = [['MNOM','0609','0000'],['DJNEL','0402','0020'],
['MC1','1702','0300'],['MC2','1806','0300'],['MC3','2012','0300'],['MC4','2512','0736'],
['SGPP','2605','0000'],['FT','0707','0000'],
['RV1','2512','0609'],['RV2','1308','0830']]

ABOUT = [res.GNAME.upper(),res.AUTHOR + ' (2020)','Source code por Matt Kai','Feito em Python','Twitter','GitHub','GNU General Public License']
  
DISCLAIMER = ['Esta é uma obra de ficção,','e quaisquer semelhanças com','acontecimentos reais são','mera coincidência.','',
'Uma certa porcentagem da','população sofre de condições','como eplepsia e convulsões,','por isso sempre consulte','seu médico antes de jogar']

ERROR = ['Oops! Alguma coisa deu errado... =(','Aperte qualquer botão para fechar']

MINIGAMES = {
'Pinball': 'Pinball','Tetris': 'Tetris','Minesweeper': 'Campo Minado','Pong': 'Pong','Differences': '7 Erros','Jigsaw': 'Quebra-cabeça','Maze': 'Labirinto','Pool': 'Sinuca','MusicTiles': 'Guitarrero',
'Footrace': 'Corrida','Hops': 'Pula corda',
'Snake': 'Snake','HittheMole': 'Acerte a toupeira','FallingItems': 'Chuva de itens','Jumping': 'Pulando','FlappyBird': 'Flappy Bird','Breakout': 'Breakout','BubbleBubble': 'Bubble Bubble','CannonBattle': 'Canhões','ColorMatch': 'Combinações',
'Twothousandforthyeight': '2048','Memory': 'Jogo da Memória','Simon': 'Simon','FindtheCup': 'Jogo dos Copos','ImageMatch': 'Combine a imagem','Cassino': 'Caça-níquel','Roulette': 'Roleta',
'Chess': 'Xadrez','Checkers': 'Damas','Trilha': 'Trilha','Blackgammon': 'Gamão','Ludo': 'Ludo','Reversi': 'Reversi','SnakesNLadders': 'Cobras e Escadas','NumberPuzzle': 'Quebra-cabeça de números',
'Solitaire': 'Paciência','SpiderSolitaire': 'Paciência Spider','Freecell': 'Freecell','Mahjong': 'Mahjong','PegSolitaire': 'Resta 1',
'Dominoes': 'Dominó','Truco': 'Truco','Sueca': 'Sueca','Cacheta': 'Cacheta','Pife': 'Pife','Buraco': 'Buraco','Poker': 'Poker','Copas': 'Copas','Espadas': 'Espadas','Maumau': 'Maumau',
'Matchingwords': 'Palavras Cruzadas','TicTacToe': 'Jogo da Velha','LinesNBoxes': 'Timbiriche','Nonogram': 'Nonograma','HuntingWords': 'Caça Palavras','Sudoku': 'Sudoku','Hangman': 'Jogo da Forca',
'Yatzy': 'Yatzy','Stop': 'Adedonha'
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
'01001110 01101111 01110011 01110011 01100001 00100000 01100101 01110011 01110000 01100101 01110010 01100001 01101110 11100111 01100001 00100000 01100101 01110011 01110100 11100001 00100000 01101110 01101111 00100000 01101110 01101111 01110011 01110011 01101111 00100000 01110011 01100001 01101100 01110110 01100001 01100100 01101111 01110010 00100000 01001011 01100001 00100111 01101100 01100101 01100010 ',
'Hello World!',
'insira uma mensagem aqui',
'Veritas lux mea',
'Soy juan carlos bodoque, y esta fue mi nota verde'
]