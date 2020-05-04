# -*- coding: utf-8 -*-
import pygame
import resources as rs
import os

NAMES = ['Sidney','Barreto','Jane','Oliveira','Renan','Pinheiro','Diego','Donovan','Bianca','Pacheco','Lúcia','Figueiredo',
'Maicon','Neves','Iago','Dantas','Vinícius','Tavares','João','Pedro Lima','Sofia','Torres','Paulo','Sousa','Pietra','Amaral']

CITIES = ['Itatiaia','Volta Redonda','Passa Quarto','Taubaté','Campos do Jordão','São Lourenço','Varginha','Juiz de Fora','Seropédica','Petrópolis']

CHAPTERS = [
['Depois do começo', 'prólogo', ['Desde aquele dia, o mundo inteiro havia mudado,', 'Um fato concreto comprovava o que os antigos cientistas', 'e filósofos tentavam nos dizer há muito tempo,',
'pela primeira vez, ali na frente, uma entidade', 'sobrenatural mostrava sua face ao mundo.', '', 'Eles não conseguiriam guardar esse segredo por mais', 'de 100.000 anos, era inviável, ainda mais devido ao',
'surto dos seres que os chamam de anomalias.', '', 'Vários caçadores cumpriam a difícil tarefa de expurgar', 'a praga de anomalias assolando a serra da região', 'sudeste brasileira, esses eram os Mercenários.',
'Eles eram odiados pela população e marginalizados', 'pela sociedade, não tinham mais escolha na vida', 'a não ser arriscá-la. Foram heróis injustiçados e', 'vilões glorificados, tudo começou desde que',
'a polícia civil legalizou o porte de armas a quem', 'quisesse se tornar um Mercenário, embora nem mesmo', 'a própria população soubesse direito o que era isso,', 'Várias teorias da conspiração se espalharam, difamando',
'a incapacidade da polícia de segurar o aumento dos', 'casos de homicídio não registrados, muitos duvidam', 'que esses casos sejam reais, ou que as anomalias', 'realmente existam.', '',
'Tudo isso gira em torno de algo muito maior,', 'mas por agora, eu devo começar pelas histórias', 'que nos uniram nessa descoberta.', '', 'Eu vou contar a minha.']],
 
['Duplo Andantes', 'capítulo I', ['O que tem a dizer sobre essa garota?','','Pietra?','Você já sabia desse lado negro dela?','','Não...eu não fazia idéia...','Começaram a me contar a verdade depois',
'e aí começei a abrir os olhos','','Conhecia ' + rs.CHARACTERS[4]['NAME'] + '?','','Não, a gente a encontrou por acaso...','e não sabia que ela estava','sendo procurada.',
'Você e ' + rs.CHARACTERS[1]['NAME'] + ' já se conheciam?','','Não, nunca nos vimos antes.','','E Vinicius? Já o conhecia?','','Não...quer dizer, mais ou menos','Ele era um criminoso muito procurado pela polícia',
'então todos da cidade o conheciam.','',rs.CHARACTERS[0]['NAME'] + ', sobre as anomalias, você sabia','o que eram?','','Não','','Sabia o real perigo que','elas representavam?','','...','','...','','...não',
'Acho que isso já é suficiente','','Obrigado senhor.','',rs.CHARACTERS[4]['NAME'] + '?','','Sim?','','Pode me dizer com detalhes','o que houve na noite em que','foi abordada?','','Claro.']],
 
['Sangue Verde', 'capítulo II', ['Lamento muito o que houve com você, Dra. ' + rs.CHARACTERS[4]['NAME'] + '.','','Obrigado...','','Você também não entendia com o que estava','mexendo, certo?','',
'Não no momento, com as pesquisas eu consegui','extrair informações importantes das amostras','mas nada que realmente fosse uma descoberta.','','Se permitir, quero que minha equipe forense colete',
'as amostras.','','Ah...não tem problema não...pode pegar.','','Também não conhecia nenhum dos criminosos?','','Não...eu não sou dessa região...','Achava que a serra era um lugar bem tranquilo...',
'Mas parece que existe violência em todo lugar','','Para quê você veio para','Campos do Jordão?','','Vim pesquisar as anomalias','','Eu também, eu vim pelo mesmo motivo','',
'Agora não, ' + rs.CHARACTERS[4]['NAME'] + '.','','Quero que me conte os detalhes da pesquisa mais tarde','','Sim, Sr. Dalibor.','','Seu nome é...','',rs.CHARACTERS[1]['NAME'] + '.','',
'Isso, me conte sua versão dos fatos.']],
 
['Não se meta com a gangue', 'capítulo III', ['']],
 
['Caminhões Canavieiros', 'capítulo IV', ['']],
 
['Peste Negra', 'capítulo V', ['']],

['O Crime Não Compensa', 'capítulo VI', ['']],
 
['Pelo Benefício do Mr. Kite!', 'capítulo VII', ['']],
 
['Dr. Estanho', 'capítulo VIII', ['']],

['Milícia x Meliante', 'capítulo IX', ['']],
 
['Não Identificado', 'capítulo X', ['']],
 
['Químicas Quimeras', 'capítulo XI', ['']],
 
['Quem tem medo de assombração?', 'capítulo XII', ['']],
 
['Afasta de mim esse Cálice', 'epílogo', ['']]
]
 
'''
HABITATS
jungle
urban
seaside
mountains
swamp
restinga
savanna-cerrado
manguezal
araucarias
   
TYPE
mammal
spirit
reptile
flying
aquatic
plant
psychic
humanoid
inorganic
fire
alien
nature
electric

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
 
0 - normal
1 - de costas
2 - repelente (anomalias não o atacam)
3 - fedor (não consegue batalhar)
4 - resfriado (não pode comer)
5 - febre (perde HP no calor)
6 - fome (perde HP por não comer)
7 - sede (perde HP por não beber)
8 - sono (erra fácil)
9 - náusea (erra facilmente)
10 - enjoo (não pode comer)
11 - fraqueza (ataques mais fracos)
12 - cegueira (perde o turno)
13 - preso (perde o turno)
14 - paralisia (perde o turno e não sai sozinho)
15 - inconsciente (não necessariamente sem HP)
16 - parasita (suga o HP)
17 - queimadura (perde HP, mas some)
18 - veneno aracnídeo (perde HP)
19 - veneno antiofídico (perde HP)
20 - veneno escorpiônico (perde HP)
21 - hemorragia (perde HP e não tem cura)
'''
      
FREAKS = {
#ANOMALIES
'eggrapper1': {'NAME': 'MC Ovinho','INFO': ['Ele vai acabar','com sua raça.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 3,'HP': 12,'RESISTANCE': 0,'PATH': 'stay','HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],'BLOOD': 10,'ITEM': None,'SONG': 'EGG_RAP'},

'eggrapper2': {'NAME': 'Ovinho Caipira','INFO': ['Ele vai acabar','com sua raça.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 3,'HP': 12,'RESISTANCE': 0,'PATH': 'stay','HABILITIES': [['Ataque',['O elemento se joga contra o','opontente, se machucando no processo.'],-5,1,100,1]],'BLOOD': 10,'ITEM': None,'SONG': 'EGG_RAP'},

'ancap': {'NAME': 'Anarcocapitalista','INFO': ['Vamos mesmo tirar sarro de uma ideologia','política utópica? Sim, vamos.'],'HEIGHT': '0,50','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 3,'HP': 12,'RESISTANCE': 0,'PATH': 'stay','HABILITIES': [['Diálogo',['O elemento tenta lhe convencer.'],-5,1,100,1]],'BLOOD': 10,'ITEM': None,'SONG': 'UNBELIEVEBLE_PEOPLE'},

'madladcat': {'NAME': 'Gato Atacado','INFO': ['É um felino sobrenatural que','flutua como um fantasma.','Pequeno e ágil, porém bem frágil.'],'HEIGHT': '0,80','HABITAT': 'jungle','TYPE': 'mammal',
'AGILITY': 5,'HP': 8,'RESISTANCE': 1,'PATH': 'stealth','HABILITIES': [['Morder',['O felino morde o oponente.'],-5,1,40,1],['Arranhar',['O felino usa suas garras,','para atacar o oponente.'],-3,10,40,10],
['Ronronar',['O felino ronrona, mostrando','seu desprezo pela situação.'],0,9,10,1],['Miar',['O felino mia para o além,','chamando outros felinos.'],['madladcat'],7,10,1]],'BLOOD': 10,'ITEM': None,'SONG': 'HEY_SAM'},
   
'lizardshrimp': {'NAME': 'Camaraleão','INFO': ['É um réptil que se fundiu com','um camarão, não se sabe se é um alimento apetitoso.'],'HEIGHT': '0,23','HABITAT': 'jungle','TYPE': 'reptile',
'AGILITY': 4,'HP': 6,'RESISTANCE': 0,'PATH': 'stay','HABILITIES': [['Camuflar',['O réptil se camufla no ambiente,','aumentando sua AGILIDADE.'],2,3],['Língua',['O réptil usa sua língua como','chicote para atacar o oponente.'],-3,1],
['Estalo',['O réptil se estala, criando','um campo de força elétrico.'],-13,1]],'BLOOD': 10,'ITEM': ['camarão',50]},
   
'peacockpigeon': {'NAME': 'Pombo Pavão','INFO': ['Um pombo urbano com uma mutação que o fez desenvolver penas de pavão com olhos reais nas suas pontas. Relativamente ágil, mas fraco.'],'HEIGHT': '0,25','HABITAT': 'urban','TYPE': 'mercenary',
'AGILITY': 3,'HP': 10,'RESISTANCE': 1,'PATH': 'horizontal','HABILITIES': [['Defecar',['A ave defeca no oponente, infectando-o.'],5,6,20,1],['Hipnose',['A ave hipnotiza o oponente com os olhos das penas de pavão, diminuindo sua AGILIDADE.'],-2,3,20,1],
['Bicar',['A ave bica o oponente.'],-4,1,50,1],['Gritar',['A ave grita, com a possibilidade de outra anomalia entrar na batalha.'],['madladcat','peacockpigeon'],7,10,1]],'BLOOD': 20,'ITEM': ['food_peanut_candy',30],'SONG': 'URBAN_PLAGUE'},
     
'crodile': {'NAME': 'Jaré','INFO': ['Um réptil que, graças á uma sílaba a menos em seu nome, perdeu dois de seus membros. Não muito ágil, mas causa muito dano.'],'HEIGHT': '1,90','HABITAT': 'swamp','TYPE': 'reptile',
'AGILITY': 2,'HP': 13,'RESISTANCE': 1,'PATH': 'stay','HABILITIES': [['Morder',['O réptil morde seu oponente'],-6,1],['Esperar',['O réptil aumenta seu ATAQUE.'],1,2],['Bote',['O réptil ataca com uma mordida em avanço.'],-5,1],
['Esconder',['O réptil se esconde no ambiente, aumentando sua AGILIDADE.'],1,3]],'BLOOD': 1},
 
'wingedcan': {'NAME': 'Lata Alada','INFO': ['Uma lata de energético que tenta ser irada e tem o único atributo que prometeu dar á quem o consumisse. É literalmente uma piada.'],'HEIGHT': '0,15','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 10,'HP': 5,'RESISTANCE': 1,'PATH': 'stay','HABILITIES': [['Voar',['Aumenta sua agilidade'],1,3],['Energizar',['Aumenta seu dano de arremesso'],2,2],['Ressaca',['A lata se auto destrói'],0,1],
['Arremessar',['A lata se joga no oponente, se machucando junto.'],-1,1]]},
    
'bunchofeyes': {'NAME': 'Cacho de Olhos','INFO': ['Vários olhos diferentes agrupados que possuem poderes hipnóticos. PS: NÃO É GUARANÁ, NÃO FAÇA SUCO.'],'HEIGHT': '0,30','HABITAT': 'jungle','TYPE': 'plant',
'AGILITY': 2,'HP': 20,'RESISTANCE': 1,'PATH': 'stay','HABILITIES':[['Encarar',['Os olhos começam a encarar o oponente, amedrontando-o e fazendo seu ATAQUE abaixar.'],-1,2],['Atirar',['Um dos olhos se lança no oponente.'],-3,1],
['Plantar',['Um olho se planta no chão com a possibilidade de germinar um novo cacho.'],0,7],['Explodir',['Todos os olhos se soltam num ataque fulminante.'],-7,1]]},
     
'bodybuilderfrog': {'NAME': 'Perereca Mil Grau','INFO': ['Um anfíbio que saiu da metamorfose antes da hora e ao mesmo tempo que manteve a cauda, desenvolveu braços fortes.'],'HEIGHT': '0,70','HABITAT': 'jungle','TYPE': 'aquatic',
'AGILITY': 2,'HP': 20,'RESISTANCE': 1,'PATH': 'follow','HABILITIES':[['Língua',['O anfíbio usa sua língua para chicotear o oponente.'],-5,1],['Porrada',['O anfíbio usa seus braços musculosos para bater no oponente.'],-8,1],
['Veneno',['O anfíbio libera toxinas nas bolsas das suas costas para infectar o oponente.'],1,4],['Salto',['O anfíbio pula pelo ambiente e aumenta sua AGILIDADE.'],2,3]]},
     
'hotman': {'NAME': 'Cremado Cremoso','INFO': ['Um homem que sofreu uma combustão espontânea mas continua vivo graças á mutação.'],'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 5,'HP': 18,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Bater',['O indivíduo bate no oponente.'],-5,1],['Cinzas',['O indivíduo joga cinzas no oponente, abaixando sua AGILIDADE.'],-3,3],
['Dançar',['O indivíduo começa a rebolar e mostrar seu charme.'],0,8],['Infectar',['O indivíduo entra dentro do oponente através das cinzas, diminuindo seu ATAQUE.'],-3,2]]},
   
'spontaneouscombustion': {'NAME': 'Combustão Espontânea','INFO': ['Uma homem normal que teve o azar','de ter essa anomalia, e agora','vive como uma tocha humana.'],'HEIGHT': '1,70','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 5,'HP': 30,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': [['Bater',['O indivíduo bate no oponente.'],-8,1],['Labareda',['O indivíduo sopra uma labareda no','oponente, fazendo ele se queimar.'],3,4],
['Queimadura',['O indivíduo se ilumina tanto que','o oponente perde a visão.'],9,6],['Bolas de Fogo',['O indivíduo arremessa bolas','de fogo que vão te atolar.'],-14,1]]},
     
'crucifiedbiscuit': {'NAME': 'Biscoito Crucificado','INFO': ['Esse ser humano não está em um estado muito bacana...É um biscoito de gengibre possuído preso num crucifixo, parece até coisa de algum filme B!'],'HEIGHT': '0,30','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 8,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Chantily','O possuído jorra chantily venenoso no oponente.',1,4],['Gargalhar','O possuído ri de uma maneira terrorífica, diminuindo o ATAQUE do oponente.',-2,2],
['Bater','O possuído usa seu crucifixo para atacar o oponente.',-8,1],['Perfurar','O possuído perfura o corpo do oponente usando o crucifixo',-10,1]]},
  
'ppap': {'NAME': 'Caneta Azul', 'INFO': ['É um objeto possuído por um fantasma','e agora tem o poder de atormentar as pessoas','com uma música irritante.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 8,'HP': 15,'RESISTANCE': 0,'PATH': 'follow','HABILITIES': [['Rabiscar',['O elemento se move contra o oponente','e o rabisca o rosto.'],-8,1],['Cantar',['O elemento atormenta o oponente','através de uma canção pertubadora.'],6,4],
['Explodir',['O elemento se estoura, espalhando','tinta na cara do oponente.'],-20,1]],'SONG': 'ppap'},
  
'armedcrab': {'NAME': 'Carangueijo Armado','INFO': ['Um carangueijo que aprendeu a','utilizar uma arma branca.'],'HEIGHT': '0,18','HABITAT': 'urban','TYPE': 'rough',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'emohipster': {'NAME': 'Emo Hipster','INFO': ['A DDA ainda não sabe se esse ser é uma anomalia ou apenas um cara estranho que chegou e parece não achar lugar no corpo que Deus encarnou.'],'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 4,'HP': 20,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Cantar',['O esquisito começa a cantar uma música dos los hermanos com uma guitarra.'],1,4],['Guitarrada',['O esquisito usa sua guitarra para atacar o oponente.'],-10,1],
['Óculos sem lente',['O esquisito põe óculos sem lente para confundir o oponente, abaixando sua AGILIDADE.'],-1,3],['Franja',['O esquisito balança sua franja, aumentando seu ATAQUE.'],2,2]],'SONG': 'EMOS_HERMANOS'},
   
'crush': {'NAME': 'Crush','INFO': ['Não conseguimos coletar muitos','dados dessa anomalia, só sabemos','que é a mais forte nunca derrotada.'],'HEIGHT': '1,60','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 99,'HP': 9999999,'RESISTANCE': 99,'PATH': 'follow','HABILITIES': [['Iludir',['A anomalia usa as palavras','como lanças e ataca o','coração do oponente.'],-99999,1]]},
     
'prettyfish': {'NAME': 'Peixe Galã','INFO': ['Um peixe que abre a boca acima dos limites de sua mandíbula e da biologia, pelo menos ele é admirável.'],'HEIGHT': '1,20','HABITAT': 'swamp','TYPE': 'aquatic',
'AGILITY': 5,'HP': 25,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Aumentar','O peixe aumenta o tamanho da sua face e volta ao normal, assustando o oponente e abaixando seu ATAQUE',-2,2],
['Saltar','O peixe salta na água e chicoteia o oponente com sua cauda',-7,1],['Morder','O peixe morde o oponente com seus dentes limpos e branquinhos.',-9,1],
['Brilhar','O peixe reflete a luz do sol cegando o oponente.',2,4]]},
     
'humanfeet': {'NAME': 'Pé de moleque','INFO': ['É um doce de amendoim delicioso muito comum em festas juninas...não pera. É um membro que se separou do corpo humano e agora consegue viver por conta própria, não confundir com mãozinha da Família Adams.'],'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Pisar','O membro pisa no oponente com toda sua força.',-10,1],['Chutar','O membro chuta o oponente, mesmo perdendo seu equilíbrio.',-12,1],
['Cura','O membro se cura utilizando uma técnica que não entendemos devido ás limitações de seu corpo.',10,1],['Agachar','O membro concentra a energia dos seus pés e aumenta seu ATAQUE.',5,2]]},
     
'flamencoflamingo': {'NAME': 'Flamingo Flamenguista','INFO': ['Uma ave com a peculiaridade de ter a anomalia FLAMENGO.'],'HEIGHT': '1,20','HABITAT': 'mangue','TYPE': 'flying',
'AGILITY': 7,'HP': 33,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Bolada','A ave chuta uma bola na face do oponente.',-13,1],['Dibre','Lamentamos o erro de ortografia de Sidney, a ave dribla o oponente fazendo sua AGILIDADE aumentar.',3,2],
['Rasteira','A ave ataca o oponente se jogando no chão e derrubando-o.',-10,1],['Gabigol','A ave recruta o profissional jogador de futebol GABIGOL, ganhando a batalha imediatamente.',-50,1]],'SONG': 'ONCE_YOU_BECOME_FOREVER_YOU_ARE'},
  
'cattlefish': {'NAME': 'Peixe Gado','INFO': ['Um búfalo que nadou tanto','que ganhou uma cauda de sereia.','Seria um tipo de Hipocampo?'],'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'aquatic',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'spidermangue': {'NAME': 'Mangue Aranha','INFO': ['Uma árvore peculiar que possui','pernas no lugar de raízes.'],'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'plant',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'crabman': {'NAME': 'Homem Carangueijo','INFO': ['Um carangueijo gigante que lembra','uma música do Chico Science.'],'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'rough',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
     
'belledoplhine': {'NAME': 'Belle Dolphine','INFO': ['Fruto de uma relação entre uma E-Girl e o Boto.'],'HEIGHT': '2,10','HABITAT': 'jungle','TYPE': 'aquatic',
'AGILITY': 7,'HP': 42,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Ahegao','O mamífero tenta sensualizar o oponente simulando um ato sexual, mas faz o efeito contrário abaixando seu ATAQUE',-3,2],['Água de banho','O mamífero oferece água de banho para o oponente, este o ingere e obtém HERPES.',2,4],
['Nadar','O mamífero nada no ambiente para recuperar sua VITALIDADE.',10,1],['Canto submarino','O mamífero entoa uma canção para chamar uma anomalia para a batalha.',1,5]]},
   
'teresacristinabust': {'NAME': 'Busto de Teresa Cristina','INFO': ['Um busto muito pesado e cheio,','de ódio no seu coração.'],'HEIGHT': '0,80','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Atacar',['O elemento se joga contra o oponente.'],-10,1],['Esmagar',['O elemento cai em cima','da cabeça do oponente.'],-20,1],['Voar',['O elemento voa ao derredor','do oponente'],0,8]]},
   
'tarsila': {'NAME': 'Tarsila','INFO': ['Um auto retrato da pintora Tarsila do Amaral, te encarando pronta pra acabar com sua raça.','Óleo sobre tela.'],'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Atacar','A pintura se joga contra o oponente, machucando a si no processo.',-10,1]]},
  
'hipocampus': {'NAME': 'Hipocampo','INFO': ['Um Hipocampo com o','formato de um hipocampo.'],'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'aquatic',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'greenchicken': {'NAME': 'Galinha Verde','INFO': ['Uma ave com a terrível','anomalia INTEGRALISMO.'],'HEIGHT': '2,30','HABITAT': 'urban','TYPE': 'flying',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'captaincatfish': {'NAME': 'Cabeça de Bagre!!','INFO': ['Um homem com cabeça de bagre','e com péssima compreensão de ritmo.'],'HEIGHT': '2,30','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'primateman': {'NAME': 'Homem Primata','INFO': ['Um humano que sabe','dançar muito bem.'],'HEIGHT': '2,30','HABITAT': 'mangue','TYPE': 'rough',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'drynwetman': {'NAME': 'Homem Seco e Molhado','INFO': ['Um homem que possui a anomalia de','estar seco e molhado ao mesmo tempo.'],'HEIGHT': '2,30','HABITAT': 'urban','TYPE': 'humanoid',
'AGILITY': 5,'HP': 50,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': []},
  
'mayanman': {'NAME': 'Tim Maia','INFO': ['Um mesoamericano com ótima.','afinação vocal.'],'HEIGHT': '1,80','HABITAT': 'jungle','TYPE': 'humanoid',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': []},
  
'elkeys': {'NAME': 'Chaves','INFO': ['Um molho de chaves','que ninguém tem paciência.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'inorganic',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': []},
 
'dorime': {'NAME': 'Dorime','INFO': ['Um ratinho santo que','e divino.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'mammal',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': []},
  
'mecanicmonkey': {'NAME': 'Macaco','INFO': ['Um macaco mecânico portando','um macaco.'],'HEIGHT': '1,80','HABITAT': 'jungle','TYPE': 'mammal',
'AGILITY': 5,'HP': 30,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': []},
     
#CHEFES
'araraucaria': {'NAME': 'Araraucária','INFO': ['Uma árvore animal que possui penas coloridas no lugar de folhas.'],'HEIGHT': '10,2','HABITAT': 'jungle','TYPE':'boss',
'AGILITY': 3,'HP': 60,'RESISTANCE': 3,'PATH': 'follow','HABILITIES': [['Algazarra',['Barulhos estranhos saem das folhas do vegetal, diminuindo o ATAQUE do oponente.'],-1,2],['Fruta',['O vegetal deixa cair uma fruta de um dos galhos.'],-6,1],['Regeneração',['O vegetal drena recursos de suas raízes e recupera 10 HP.'],10,1]]},
    
'torpedosquid': {'NAME': 'Lula Torpedo','INFO': ['Um molusco que antige seus oponentes como um torpedo. Apesar de enorme, forte e resistente, se locomove muito devagar.'],'HEIGHT': '2,10','HABITAT': 'sea','TYPE': 'boss',
'AGILITY': 1,'HP': 50,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Tentáculos','O molusco usa seus tentáculos para atacar seu oponente.',-5,1],['Jato de tinta','O molusco atira um jato de tinta que impossibilita o oponente de atacar.',-5,3],
['Camuflagem','O molusco se disfarça no ambiente, aumentando sua AGILIDADE.',2,3],['Torpedo','O molusco acerta o oponente com um ataque explosivo que acerta todos á volta, super efetivo.',-15,1]]},
 
'giantear': {'NAME': 'Orelhão','INFO': ['Um fungo que realmente existe,','e quis trabalhar pra telefônica.'],'HEIGHT': '1,30','HABITAT': 'urban','TYPE': 'boss',
'AGILITY': 3,'HP': 25,'RESISTANCE': 0,'PATH': 'follow','HABILITIES': [['Soar',['O elemento vibra seus tímpanos,','abaixando a RESISTÊNCIA do oponente.'],-5,4],['Fichas',['O elemento arremessa fichas','do seu cofrinho.'],-10,1],
['Trote',['O elemento te passa um trote,','enganando o oponente e abaixando','sua FORÇA'],1,6],['Ligação',['O elemento faz uma ligação,','chamando outra anomalia.'],2,6]]},
 
'abaporu': {'NAME': 'Abaporu','INFO': ['Uma pintura modernista que criou vida própria e por sinal é canibal.'],'HEIGHT': '2,20','HABITAT': 'urban','TYPE': 'boss',
'AGILITY': 7,'HP': 75,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Pisar','A pintura pisa no oponente esmagando-o.',-13,1],['Fúria','A pintura grita furiosamente aumentando seu ATAQUE.',3,2],
['Proteger','A pintura reforça sua proteção de acrílico sobre a tela',1,6],['Reforço','A pintura chama outra pintura para ajudar na batalha.',1,5]]},
 
'cigaruto': {'NAME': 'Xaruto','INFO': ['Estranhamente lembra um personagem de um anime que não é tão bom quanto Evangelion.'],'HEIGHT': '0,10','HABITAT': 'urban','TYPE': 'boss',
'AGILITY': 20,'HP': 20,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Fumaça ninja','O elemento solta uma fumaça com mais de 100.000 substâncias tóxicas incluindo nicotina e enxofre, envenenando o oponente.',-3,1],['Chama ninja','O elemento sopra uma labareda ardente, incendiando o oponente.',-2,1],
['Xaringan','O elemento usa uma espécime de energia oculta para aumentar seu ATAQUE.',-3,1],['Vaporizar','O elemento se transforma num cigarro eletrônico, relaxando e diminuindo sua AGILIDADE.',-3,1]],'BLOOD': 100,'ITEM': None,'SONG': 'CIGARUTO'},
 
'caesarean': {'NAME': 'Cesariana','INFO': ['Um feto dentro de uma bolha numa cesariana com poderes psíquicos.'],'HEIGHT': '1,00','HABITAT': 'urban','TYPE': 'boss',
'AGILITY': 2,'HP': 10,'RESISTANCE': 1,'PATH': 'follow','HABILITIES': [['Escudo','O feto reforça a resistência da bolha.',1,6],['Cordão Umbilical','O feto drena a energia de sua hospedeira e recupera sua VITALIDADE.',10,1],
['Grito molecular','O feto grita em um nível estratosféricamente alto, agitando as moléculas de seus oponentes.',-15,1],['Líquido Uterino','O feto arremesa o líquido uterino da bolha nos oponentes, confundindo-os e dando NÁUSEA.',2,4]]},
 
#MERCENARIES
'thuga': {'NAME': 'Bandido A','HABITAT': 'urban','TYPE': 'mercenary','AGILITY': 2,'HP': 30,'RESISTANCE': 2,'PATH': 'stay','HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]]},

'vinicius': {'NAME': 'Vinícius','HABITAT': 'urban','TYPE': 'mercenary','AGILITY': 2,'HP': 30,'RESISTANCE': 2,'PATH': 'stay','HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]]},

'pietra': {'NAME': 'Pietra','HABITAT': 'urban','TYPE': 'mercenary','AGILITY': 2,'HP': 30,'RESISTANCE': 2,'PATH': 'stay','HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]]},

'thirdchar': {'NAME': rs.CHARACTERS[2]['NAME'],'HABITAT': 'urban','TYPE': 'mercenary','AGILITY': 2,'HP': 30,'RESISTANCE': 2,'PATH': 'stay','HABILITIES': [['Atirar','',-8,1,90],['Granada','',-20,1,10]]},
 
#OTHER
'target': {'NAME': 'Alvo','HABITAT': 'urban','TYPE': 'inorganic','AGILITY': 2,'HP': 30,'RESISTANCE': 2,'PATH': 'stay','HABILITIES': [['Fazer nada',0,6]]},
 
}
 
ARMY = [[],[],[],[],[]]
for i in range(40): ARMY[0].append('madladcat')
     
ITEMS = {
#BAGS
'bag1': ['bolsinha',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 5 - Peso: 5'],1000,5,5],
'bag2': ['bolsa',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 10 - Peso: 10'],2500,10,10],
'bag3': ['mochila',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 20 - Peso: 15'],5000,20,15],
'bag4': ['mochila de viagem',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 30 - Peso: 20'],7500,30,20],
'bag5': ['mochilão',['Guarde seus itens nele e leve para qualquer lugar.','Volume: 30 - Peso: 25'],10000,30,25],
'bottle100': ['frasco de sulfúrio 100ml',['Feita especialmente para guardar sangue verde.','Capacidade de 10 inimigos'],200,1,1],
'bottle250': ['garrafa de sulfúrio 250ml',['Feita especialmente para guardar sangue verde.','Capacidade de 25 inimigos'],200,1,1],
'wallet': ['carteira',['Use para guardar seu dinheiro e coisas pequenos,','JAMAIS PERCA ISSO'],50,1,1],
   
#CUSTOM CLOTHES
'head_hairclip': ['xuxinha',['Pra amarrar o cabelo.'],30,1,1,3],
'head_cap1': ['boné',['Pra proteger do sol e ficar estiloso.'],30,2,1,1],
'head_cap2': ['gorro',['Pra proteger do sol e ficar estiloso.'],30,2,1,1],
'head_glasses1': ['óculos de grau',['Apenas pra quem precisa, senão você','ganha cegueira.'],30,2,1,1],
'head_glasses2': ['óculos escuros',['Pra quem não tem colírio.'],30,2,1,1],
'head_glasses3': ['óculos redondos',['Qualquer um que usá-lo se transforma','imediatamente no Harry Potter.'],30,2,1,1],
'head_glasses4': ['óculos retrô',['Apenas para quem é Hype de verdade.'],30,2,1,1],

'clth_shirt1': ['camisa preta',['O traje predileto dos solitários.'],30,4,1,'01'],
'clth_shirt2': ['camisa laranja',['Roupa casual.'],30,4,1,'02'],
'clth_shirt3': ['camisa vermelha',['Roupa casual.'],30,4,1,'03'],

'clth_jacket1': ['jaqueta preta',['Pra dar uma de Ramones.'],30,4,1,'01'],
'clth_jacket2': ['jaqueta verde quadriculada',['Pareçe roupa de festa junina.'],30,4,1,'02'],
'clth_jacket3': ['jaqueta vermelha qudriculada',['Conhece o Iberê? então.'],30,4,1,'03'],
'clth_jacket4': ['moletom cinza',['Pra aqueles que não tem paciêcia','pra escolher roupa.'],30,4,1,'04'],
'clth_jacket5': ['moletom azul',['Pra aqueles que não tem paciêcia','pra escolher roupa.'],30,4,1,'05'],
'clth_jacket6': ['avental',['Para pesquisadores.'],30,4,1,'06'],

#VESTS
'vest1': ['colete amarelo',['Cuidado pra não pensarem que','é um francês manifestante.'],30,3,1,1,10],
'vest2': ['colete salva-vidas',['Mesmo sem água por perto, protege bastante.'],60,2,1,3,15],
'vest3': ['colete I',['Reduz o dano do advesário','DEFESA: 5 DURAÇÃO: 25'],120,3,1,5,20],
'vest4': ['colete IIA',['Reduz o dano do advesário','DEFESA: 8 DURAÇÃO: 25'],240,3,1,8,25],
'vest5': ['colete II',['Reduz o dano do advesário','DEFESA: 10 DURAÇÃO: 30'],360,3,1,10,30],
'vest6': ['colete IIIA',['Reduz o dano do advesário','DEFESA: 12 DURAÇÃO: 35'],480,3,1,12,35],
'vest7': ['colete III',['Restrito apenas para','policiais de elite.'],600,3,1,16,40],
'vest8': ['colete IV',['Restrito apenas para','policiais de elite.'],720,3,1,20,45],
 
#CHARMS
'amulet1': ['cruz',['Conçede proteção e espanta espíritos.'],20,1,1,5,50],
'amulet2': ['ankh',['Conçede proteção e espanta espíritos.'],20,1,1,10,50],
'amulet3': ['hamsá',['Conçede força e proteção.'],20,1,1,15,50],
'amulet4': ['pentáculo',['Conçede força, proteção e vitalidade.'],20,1,1,20,50],
'amulet5': ['tríscele',['Conçede força, proteção e vitalidade'],20,1,1,25,50],
'amulet6': ['ouroboros',['Conçede força, proteção,','vitalidade e resistência.'],20,1,1,25,50],
'amulet7': ['muiraquitã',['Conçede aumento em todos os atributos.'],20,1,1,25,50],
 
#AMMO
'ammo_tranquiizer': ['tranquilizante',['Munição para pistola que faz','o inimigo adormecer.'],100,2,1,0],
'ammo.12': ['munição.12',[''],200,2,1,12],
'ammo.16': ['munição.16',[''],200,2,1,16],
'ammo.22': ['munição.22',[''],200,2,1,22],
'ammo.32': ['munição.32',[''],200,2,1,32],
'ammo.38': ['munição.38',[''],300,2,1,38],
'ammo.42': ['munição.42',[''],400,2,1,42],
'ammo.44': ['munição.44',[''],200,2,1,44],
'ammo.45': ['munição.45',[''],200,2,1,45],
'ammo.38mm': ['munição 0.38mm',[''],200,2,1,380],
'ammo.5.56mm': ['munição 5.56mm',[''],200,2,1,556],
'ammo_missile': ['míssel',[''],800,5,4,1000],
 
#TOOLS
'tool_crowbar': ['pé de cabra',['Use para abrir portas trancadas.'],50,4,3,{'DAMAGE': 5, 'UNLOCK': 'door'}],
'tool_axe': ['machado',['Use para quebrar madeira.'],50,4,4,{'DAMAGE': 5, 'UNLOCK': 'wood'}],
'tool_hammer': ['marreta',['Use para quebrar vidro.'],50,4,5,{'DAMAGE': 5, 'UNLOCK': 'stone'}],
'tool_shovel': ['pá',['Use para cavar o solo para encontrar itens e abrir passagens.'],50,5,3,{'DAMAGE': 5, 'UNLOCK': 'grass'}],
'tool_chainsaw': ['motoserra',['Use para cortar árvores grandes','e de quebra bancar o Jason.'],50,6,3,{'DAMAGE': 5, 'UNLOCK': 'wood'}],
'tool_lighter': ['isqueiro',['Use para acender bombas','e talvez cigarros, mas não se recomenda.'],6,1,1],
'magnifying_glass': ['lupa',['Use para pesquisar anomalias e registrá-las no Bestiário.'],2,1,1],
'radar': ['radar',['Use para detectar anomalias no mapa.'],300,2,1],
'handcuffs': ['algemas',['Use para capturar anomalias e levá-las para pesquisa.'],50,2,1],
'umbrella': ['guarda-chuva',['Não pegue resfriado meu filho!'],800,5,1],'umbrella_portable': ['guarda-chuva portátil',['Não pegue resfriado meu filho!','Cabe na mochila!'],800,3,1],
   
#MELEE WEAPONS
'melee_broom': ['vassoura',['Não foi feita para se armar, muito menos','para caçar ou voar, mas funciona.',10,5,2,{'DAMAGE': 2}]],
'melee_frying_pan': ['frigideira',['Se não tiver o que usar, ela quebra um galho','e ainda frita um ovo legal.',30,3,2,{'DAMAGE': 4}]],
'melee_bottle': ['garrafa de vidro',['Depois de um drink moderado','é excelente para tacar na cabeça de um nazi.'],10,3,3,{'DAMAGE': 6}],
'melee_bar': ['barra de ferro',['Dá na telha pra descer','o cacete em alguém.'],4,3,3,{'DAMAGE': 8}],
'melee_knife': ['faca',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],300,2,1,{'DAMAGE': 10}],
'melee_fishmonger': ['peixeira',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],500,4,3,{'DAMAGE': 13}],
'melee_cleaver': ['cutelo',['Foi feita para cortar ossos de carnes, mas','serve como uma boa arma também.'],700,3,2,{'DAMAGE': 16}],
'melee_katana': ['katana',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],1000,4,3,{'DAMAGE': 18}],
'melee_whip': ['chicote',['Útil para ataques corpo-a-corpo, pode ser tão letal','quanto uma arma de fogo.'],500,3,3,{'DAMAGE': 14}],
'melee_taser': ['taser',['Porque um verdadeiro meliante','não mata, causa dor.'],1500,1,3,{'DAMAGE': 8}],

#WEAPONS
'gun_revolver.22': ['revólver.22',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 16.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}],
'gun_revolver.32': ['revólver.32',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 16.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}],
'gun_revolver.38': ['revólver.38',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 16.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}],
'gun_revolver.44': ['revólver.44',['Arma de fogo para ataques de curta distância, ela usa munição de','calibre 16.'],2000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 5, 'CAPACITY': 6, 'GAUGE': 38}],
  
'gun_pistol': ['pistola',['Arma de fogo para ataques de média distância, ela usa munição de calibre 38.'],2500,3,2,{'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 3, 'CAPACITY': 16}],
  
'gun_UZI.22': ['Uzi .22',['Arma de fogo para ataques de média distância.'],4000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 1, 'CAPACITY': 10, 'GAUGE': 22}],
'gun_UZI.45': ['Uzi .45',['Arma de fogo para ataques de média distância.'],4000,3,2,{'DAMAGE': 5, 'RECHARGE': 8, 'CADENCY': 1, 'CAPACITY': 16, 'GAUGE': 45}],
  
'gun_shotgun.12': ['espingarda .12',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 5, 'RECHARGE': 4, 'CADENCY': 4, 'CAPACITY': 6, 'GAUGE': 12}],
'gun_carbine': ['carabina',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CAPACITY': 3}],
  
'gun_sniper': ['sniper',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],6000,5,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CAPACITY': 3}],
'gun_shotgun': ['escopeta',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],4000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CAPACITY': 3}],
  
'gun_assault_riffle': ['fuzil de assalto',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],4000,5,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CAPACITY': 3}],
'gun_rifle': ['fuzil',['Arma de fogo para ataques de curta distância, ela usa munição de calibre 16.'],5000,5,3,{'DAMAGE': 4, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 16}],
'gun_AK-47': ['AK-47',['Fuzil para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 7, 'RECHARGE': 3, 'CADENCY': 2, 'CAPACITY': 20, 'GAUGE': 39.0}],
'gun_M16': ['M16',['Fuzil para ataques de curta distância, ela usa munição de calibre 16.'],5000,4,3,{'DAMAGE': 6, 'RECHARGE': 3, 'CADENCY': 1, 'CAPACITY': 30, 'GAUGE': 5.56}],
  
'gun_RPG-7': ['RPG-7',['Bazuca utilizada contra tanques.'],12000,7,5,{'DAMAGE': 50, 'RECHARGE': 10, 'CADENCY': 0, 'CAPACITY': 1, 'GAUGE': 0}],
   
#BATTLE ITEMS
'grenade': ['granada',['Use numa batalha para causar dano á todos os inimigos na tela.'],100,2,3,10,1],
'grenade_smoke': ['granada de fumaça',['Use numa batalha para que todos os inimigos percam AGILIDADE.'],200,2,3,3,4],
'grenade_flash': ['granada de luz',['Use numa batalha para que todos os inimigos percam sua vez.'],500,3,3,1,6],
'pepper_spray': ['spray de pimenta',['Use numa batalha para atordoar um inimigo.'],40,3,1,2,6],
'molotov_cocktail': ['coquetel molotov',['Use numa batalha para causar dano á todos os inimigos','e possivelmente queimá-los.'],40,3,1,2,6],
'horn': ['buzina',['Use numa batalha para atordoar um inimigo.'],40,3,1,2,6],
'extinguisher': ['extintor',['Use num caso de emergência.','...mas não é pra jogar num bulldogue.'],40,4,1,2,6],
'rope': ['corda',['Use em batalhas para prender seus oponentes','ou dentro de cavernas para descer e subir'],70,4,1],
   
#DRUGS
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

#CONDIMENTS
'condiment_ketchup': ['ketchup',['Condimento muito usado em salgados.'],5,1,1,6,'0100'],
'condiment_sugar': ['açúcar',['Condimento muito usado em doces.'],5,1,1,6,'0100'],
'condiment_salt': ['sal',['Condimento muito usado em refeições.'],5,1,1,6,'0100'],
'condiment_pepper': ['pimenta',['Condimento muito usado em refeições.'],5,1,1,6,'0100'],
'condiment_oregano': ['orégano',['Condimento muito usado em salgados.'],5,1,1,6,'0100'],
'condiment_shoyu': ['shoyu',['Condimento muito usado em refeições.'],5,1,1,6,'0100'],

#DRINK
'drink_water': ['água',['O básico pra te manter de pé','no calor e no cansaço, BEBA ÁGUA.'],8,2,1,10,'0100'],
'drink_juice_orange': ['suco de laranja',['Saudável e nutritivo, o Jailson aprova.'],8,3,1,10,'0100'],
'drink_juice_passion_fruit': ['suco de maracujá',['Saudável e nutritivo, acalma a alma e o espírito.'],8,3,1,10,'0100'],
'drink_coffee': ['café',['Bebida que aumenta a sua energia.'],8,3,1,10,'0100'],
'drink_chocolate': ['chocolate quente',['Vai bem com biscoitos'],8,3,1,10,'0100'],
'drink_milk': ['leite',['Vai bem no café.'],8,3,1,10,'0100'],
'drink_coffeenmilk': ['café com leite',['Bebida preferida do criador','do jogo, foi muito útil.'],8,3,1,10,'0100'],
'drink_energy': ['energético',['Bebida que acelera o metabolismo','e aumenta a energia.'],8,3,1,10,'0100'],
'drink_cola': ['refri',['A bomba calórica que a gente gosta.'],8,3,1,10,'0100'],
'drink_guarana': ['guaraná',['Um suquinho barato e muito açúcarado','mas é bom, não confundir com cachos de olhos.'],8,3,1,10,'0100'],
'drink_beer': ['álcool',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,10,'0100'],
'drink_whiskey': ['uísque',['Bebida alcóolica para aumentar a energia','Pelo amor de deus COM MODERAÇÃO.'],8,2,1,10,'0100'],
'drink_yogurt': ['iogurte',['Delicioso e saudável.'],8,3,1,10,'0100'],
 
#FOOD
'food_orange': ['laranja',['Fruta fácil de se achar','num pomar.'],3,1,1,2,'0100'],
'food_fish': ['pirarucu',['Peixe de água doce.'],3,1,1,2,'0100'],
'food_bread': ['pão',['O alimento matinal de cada dia.'],15,2,2,30,'0300'],
'food_peanut_candy': ['paçoca',['Doce de amendoim, fácil de encontrar em padarias.'],1,1,1,2,'0100'],
'food_peanut_candy': ['paçoca',['Doce de amendoim, fácil de encontrar em padarias.'],1,1,1,2,'0100'],
'food_coxinha': ['coxinha',['Salgado feito com massa frita e recheada com frango, fácil de','encontrar em lanchonetes.'],5,2,1,8,'0100'],
'food_pastry': ['pastel',['Salgado feito com massa frita e recheado com queijo.'],3,2,1,5,'0100'],
'food_puff_pastry': ['pastel folheado',['Salgado feito com várias camadas de massa e queijo.'],6,2,1,12,'0100'],
'food_brigadeiro': ['brigadeiro',['Doce de chocolate.'],2,1,1,3,'0100'],
'food_cheese_bread': ['pão de queijo',['Salgado feito com massa de queijo.'],5,1,1,7,'0100'],
'food_pudding': ['pudim',['Doce feito com leite condensado.'],10,3,1,15,'0300'],
'food_cake_corn': ['bolo de fubá',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,'0500'],
'food_cake_carrot': ['bolo de cenoura',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,'0500'],
'food_cake_chocolate': ['bolo de chocolate',['Doce feito com ovos, leite, fubá, manteiga, trigo e fermento.'],12,3,2,18,'0500'],
'food_packed_lunch': ['marmita',['Tem muitas coisas diferentes dentro, além de ser bem nutritivo!'],15,3,2,30,'0300'],
'food_egg': ['ovo',['Ele te deixa forte pra enfrentar qualquer perigo.'],15,2,2,30,'0300'],
'food_lamen': ['miojo',['O macarrão instantâneo','do cara que mora sozinho.'],15,2,2,30,'0300'],
'food_cookies': ['bolachas',['Biscoito com recheio sempre','foi chamado assim.'],15,2,2,30,'0300'],
'food_snack': ['salgadinhos',['50% do saco é de puro vento.'],15,2,2,30,'0300'],
'food_pizza_mussarella': ['pizza de mussarela',['Quem não gosta de pizza?.'],15,2,2,30,'0300'],
'food_pizza_shaggy': ['pizza de calabresa',['Quem não gosta de pizza?.'],15,2,2,30,'0300'],
'food_pizza_chicken': ['pizza de frango',['Quem não gosta de pizza?.'],15,2,2,30,'0300'],
'food_pizza_4cheese': ['pizza de 4 queijos',['Quem não gosta de pizza?.'],15,2,2,30,'0300'],
 
#WASTED FOOD
'food_coxinha_wasted': ['coxinha fria',['Não é mais tão gostosa quanto antes,','mas é comestível.'],2,1,1,4],
'food_peanut_candy_wasted': ['paçoca esfarelada',['O que antes era um doce maravilhoso','agora são apenas migalhas...'],1,1,1,1],
'food_egg_wasted': ['ovo podre',['ALGUÉM DESTRUIU O MEU OVO'],15,2,2,30],
 
#TRASH
'trash_packing': ['embalagem',['Um papel que não serve pra absolutamente nada','a menos que seja uma esponja amarela.'],8,1,1,10,'0100'],
'trash_bottle': ['garrafa de vidro',['Um item meio perigoso de se levar','nas suas costas,','sabe-se lá o que pode fazer com isso'],8,1,1,10,'0100'],
   
#KEY ITEMS
'key_bedroom': ['chave do quarto',['Se perder vai ficar sem caminha.'],10,1,1],
'key_chest': ['chave de baú',['Use para abrir um compartimento.'],10,1,1],
'key_vehicle': ['chave do veículo',['É o que põe o motor pra funcionar.'],10,1,1],
'key_park': ['chave do parque',['Ela serve pra entrar no parque nacional','onde você achou é outra história.'],10,1,1],
'key_lab': ['chave do laboratório',['Que honra ter as chaves do laboratório Fiocruz!'],10,1,1],
'key_office': ['chave do escritório',['Um homem simpático que deu','ele quer mesmo é ver o circo pegar fogo.'],10,1,1],
'key_cave': ['signo de mercúrio',['Uma placa de ferro com a inscrição','de mercúrio... estranho'],10,1,1],
'dungeon_key': ['chave',['Use dentro de instalações para abrir caminhos.'],10,1,1],
   
#ESSENTIALS
'id_card0': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'id_card1': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'id_card2': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'id_card3': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'id_card4': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'id_card5': ['identidade',['Mostra suas informações básicas e prova sua autoridade acima','dos civis.'],0,1,1],
'credit_card': ['cartão de crédito',['Um item muito necessário na vida de um jovem adulto, use nos caixas','de banco, nem imagine em jogar fora!'],0,1,1],
'charger': ['carregador',['Use para carregar seu celular.'],40,1,1],
'portable_charger': ['carregador portátil',['Use para carregar seu celular.'],100,1,1],
'headphone': ['fones de ouvido',['Ao obter um, você consegue escutar o rádio do celular, mas atenção! ele quebra nos momentos mais inesperados.'],60,1,1],
'phone': ['celular',['Mais importante que o cartão só o celular, pode ser usado para fazer','chamadas e receber emails, mas lembre-se de recarregar.'],0,1,1],
 
#PILLS
'pill_strenght': ['suplemento de força',['Aumenta a FORÇA permanentemente em +10.'],500,1,1,0],
'pill_attack': ['suplemento de ataque',['Aumenta o ATAQUE permanentemente em +10.'],500,1,1,1],
'pill_agility': ['suplemento de agilidade',['Aumenta a AGILIDADE permanentemente em +10.'],500,1,1,2],
'pill_resistance': ['suplemento de resistência',['Aumenta a RESISTÊNCIA permanentemente em +10.'],500,1,1,3],
'pill_vitality': ['suplemento de vitalidade',['Aumenta a VITALIDADE em +10'],500,1,1,4],
'pill_mistery': ['suplemento misterioso',['Aumenta um atributo aleatório'],500,1,1,4],
   
#REPELLENTS
'repellent1': ['repelente básico',['Evita anomalias de aparecer por 10 minutos.'],50,2,1,10],
'repellent2': ['super repelente',['Evita anomalias de aparecer por 30 minutos.'],100,2,1,30],
'repellent3': ['ultra repelente',['Evita anomalias de aparecer por 60 minutos.'],250,2,1,60],
   
#ACESSORIES
'aim1': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,1],
'aim2': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,2],
'aim3': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,3],
'aim4': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,4],
'aim5': ['mira 1',['Customiza a mira de sua arma.'],200,1,1,5],
 
'acc_silencer': ['silenciador',['Aumenta o ATAQUE de uma pistola.'],200,1,1,1],
'acc_cartridge': ['cartucho extra',['Aumenta a capacidade da arma.'],100,1,1,2],
'acc_gun_butt': ['coronha',['Aumenta a AGILIDADE da arma.'],100,1,1,3],
'acc_bandolier': ['bandoleira',['Adiciona um espaço extra no inventário.'],100,1,1,3],
 
'locksmith1': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith2': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith3': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith4': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith5': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith6': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
'locksmith7': ['chaveiro',['Use para guardar até duas chaves.'],10,1,1,3],
 
#CRAFTING
'craft_spring_small': ['mola pequena','',0,1,1],
'craft_fuel': ['combustível','',0,1,1],
'craft_cloth': ['pano','',0,1,1],
'craft_powder': ['pólvora','',0,1,1],
   
#TREASURES
'treasure_vase': ['vaso marajoara',['Um antigo vaso indígena feita da cerâmica do marajó.'],2000,3,3,0],
 
'jewel_emerald': ['esmeralda',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_diamond': ['diamante',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_ruby': ['rubi',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_amethyst': ['ametista',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_sapphire': ['safira',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_opal': ['opala',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_gold': ['ouro',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'jewel_quartz': ['quartzo',['Essa jóia deve custar uma fortuna!'],2000,1,3,0],
'mysterious': ['???',['Você não faz idéia do que é isso.'],0,1,1,0]
}
 
INVENTORY = [
[[['_','0000','_','_'],['phone','360100','_','_'],['wallet','00005000000300','credit_card','id_card0'],['locksmith1','02020000','key_bedroom','key_vehicle'],['_','0000','_','_']],
[['amulet1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['clth_jacket1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['ammo.38','0000','_','_'],['_','0000','_','_']],
[['clth_shirt1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['gun_revolver.38','0006','aim1','acc_cartridge'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
 
[[['head_glasses1','0000','_','_'],['food_peanut_candy','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['clth_jacket3','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
 
[[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
 
[[['amulet4','0000','_','_'],['repellent1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['amulet5','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['food_coxinha','1103','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['charger','000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['gun_revolver.38','0006','aim3','acc_gunbutt'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
 
[[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
 
[[['amulet7','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['amulet6','0000','_','_'],['condiment_ketchup','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['amulet2','0000','_','_'],['_','0000','_','_'],['pill_vitality','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['amulet3','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']],
[['bag1','0000','_','_'],['gun_revolver.38','0006','aim2','acc_bandolier'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]],
]
 
STORAGE = [['jewel_ruby','0000','_','_'],['drink_whiskey','1503','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],
['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],
['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],
['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],
['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_'],['_','0000','_','_']]

CHESTS = {
'1bedroom_202': [False],
'hauntedhouse_4': [False],
'hauntedhouse_5': [False]
}

PRODUCTS = [
[['drink_beer','drink_whisky'],0,0],
[['vest1','repellent1','food_coxinha','pill_vitality','melee_knife','amulet1','aim1'],1,10],
[['grenade','pepper_spray','gun_revolver.38'],1,2],
[['melee_fishmonger','portable_charger','headphone'],4,0]
]
 
VEHICLES = {
'moto_0': {'SPEED': 8, 'ACCELERATION': 0.5, 'CAPACITY': 100, 'GAS': 0.075, 'LIGHTS': 2},
'moto_1': {'SPEED': 10, 'ACCELERATION': 0.25, 'CAPACITY': 100, 'GAS': 0.05, 'LIGHTS': 1}
}
 
NUMBERS = [['Sidney','989074454'],['Jane','991124257'],['Renan','990435671'],['Diego','926148930'],['Bianca','976564008'],['Lúcia','990271802'],
['Maicon','923778988'],['Iago','977904623'],['Sofia','923578103'],['Vinícius','960428331'],['Pietra','940028922'],['Paulo','987690021'],['João Grande','956230401'],
['Pizza Delivery','953478809'],['Correios','909236521'],['Mercador','969696969']]
 
EMAILS = [
['prfrj@cmail.com','Caso de anomalia',['Boas novas','','Uma anomalia foi encontrada nos','arredores do Parque Nacional do Itatiaia,','É necessário a eliminação do','indivíduo assim que o possível','','Encontrem seus próprios meios','para adentrar o local.']],
 
['prfrj@cmail.com','Caso de anomalia',['Boas novas','','Uma anomalia foi encontrada nos','arredores da cidade de Resende,','É necessário a eliminação do','indivíduo assim que o possível','','Encontrem seus próprios meios','para adentrar o local.']],
 
['cangaceirostv@cmail.com','Proposta de entrevista',
['Boas novas, ' + rs.CHARACTERS[0]['NAME'] + ' ' + rs.CHARACTERS[0]['LASTNAME'] + '.', ' ', 'Com a repercussão dos casos de', 'anomalias do Departamento de', 'Detenção de Anomalias de',
'Itatiaia, sugerimos uma', 'entrevista com você e dois', 'participantes para o', 'Jornal da Noite.', ' ', 'A entrevista será ás 5:30 PM', 'e será gravado nos estúdios', 'da Cangaceiros TV, na',
'Av. Getúlio Vargas.', ' ', 'Aguardamos sua resposta', 'no local.']],
 
['mendoncapietra7@cmail.com','Oiee',
['Só tô te testando menino']],
]
 
NEWS = [
#DIA 1
[
[['Polícia Municipal abre a','renovação da carteira'],'Tereza Rocha',['Em 4 de abril, a Polícia Municipal abriu a renovação da carteira para mercenários. A carteira de identificação de Mercenário é \
obrigatória não só por identificação, mas por questões de segurança, depois que a câmara dos deputados aprovou a reforma armamentista, qualquer cidadão com a identificação de mercenário é livre para portar \
e possuir uma arma de fogo.','',' Recentemente, houveram vários casos de assassinatos não registrados pela polícia, pela incapacidade da polícia de analisar todos os casos separadamente, mercenários tem sido \
recompensados para cuidar desses assassinatos misteriosos.','','Devido a isso os dados de homicídio por armas de fogo aumentaram consideravelmente no estado, isso se deve á facilidade de se obter uma arma e também de \
reduzir a pena de um criminoso para servir ao estado como mercenário. O criminólogo Mauro Fidélis fala sobre a situação.','','"O que a polícia do rio de janeiro fez foi um ato irresponsável e inpensável, pois \
graças á essa facilidade de se armar, vários criminosos podem se aproveitar e utilizá-las para fins maliciosos, e mesmo com tantos casos de homicídios não registrados, o que custava a polícia recrutar mais policiais ou \
fazer uma investigação profunda e mais elaborada á respeito?"','','Sabendo disso, tudo o que podemos esperar é que os mercenários façam bom uso de seu poder bélico.']],
[1,['sex','32',0],['sab','25',1],['dom','22',1],['seg','18',2],['ter','15',3]],
[2,0]
],
 
#DIA 2
[
[['Parque Nacional do Itatiaia','é invadido'],'Jéssica Ramone',['Na tarde do dia anterior, um','caso que deixou autoridades','em estado de alerta, foram','filmadas imagens de vândalos',
'invadindo o parque nacional.','','"não é o que se espera','dessa juventude, não é?", diz','Marcelo Marinho, fiscal do','IBAMA e principal supervisor','do parque','',
'O Parque Nacional do Itatiaia','é uma área de preservação','da fauna brasileira protegida','por lei, pois é onde se','encontra o que resta da','mata atlântica, que vem','sofrendo drásticas degradações',
'com o tempo.','','Mas o maior desafio do','parque não são os vândalos,','mas sim os mercenários,','vários invadem locais restritos','atrás das presas e do','dinheiro, colocando em risco',
'a fauna e a flora da','natureza. A PRF já','possui conhecimento de tais','atos ediondos.','','"É lamentável, a gente pensa','que confia mas eles','só mostram que estamos',
'se enganando", diz Paulo Sousa','','O IBAMA, instituição','responsável pelo monitoramento','do parque, emitiu uma nota','avisando que irão reforçar','a segurança no local,',
'policiais militares armados','e cães de guarda são','apenas um pouco do','que os mercenários podem','temer de agora em','diante.']]
],
 
#DIA 3
[
[['Relato de assombração em Itatiaia','pode ser verdadeiro'],'Jéssica Ramone',['Ás 11:30 da noite passada,','moradores de Itatiaia relataram','um caso incomum entre vários','da polícia, \
foi registrado um','caso de uma assombração','(vulgo Poltergeist) na casa de','Maria Elisângela das Dores,','35 anos.','','"Não sabia o que fazer, eu nunca','imaginei que assombrações\
 ou','fantasmas realmente existissem,','sempre achei que eram apenas','contos de criança.", diz','Maria Elisângela.','','Apesar de inesperado e muito','estranho, o relato foi comprovado','\
por filmagens do Departamento','de Detenção de Anomalias de','Itatiaia, além dos danos','causados pela assombração na','casa e nos moradores da região.','','Aparentemente este não é o','\
único relato de moradores a','respeito de uma assombração,','foram registrados 5 relatos em','um único mês e 12 em 3 meses, mas','se as investigações persistirem','este pode ser o \
primeiro','relato confirmado de uma','assombração no país.']],
[['Engarrafamento na zona sul'],'Gisele Peres',['Muito trânsito']]
],

#DIA 4
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 5
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 6
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 7
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 8
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 9
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 10
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 11
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 12
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 13
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 14
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 15
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 16
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 17
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 18
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 19
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 20
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 21
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 22
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 23
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 24
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 25
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']],
[['Dicas de culinária da','Senhora dolores'],'Gustavo Barriloche',['asg','asfsag']]
],

#DIA 26
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 27
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 28
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 29
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 30
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
],

#DIA 31
[
[['Museu Histórico de Petrópolis','é fechado por assombrações'],'Jéssica Ramone',['Na terça feira passada do dia 13 de Novembro, visitantes do Museu Imperial presenciaram uma cena assustadora, \
As exposições começaram a atacar os visitantes, como é relatado por vários entrevistados.','"Foi começando devagar, uma pintura ia se despendurando da parede...uma estátua começava a piscar...\
e quando percebe estão fechando os corredores e chamando os seguranças."','']],
[['FLA x FLU'],'Gustavo Pinhão',['Muito disputado']]
]
]
 
if rs.CHARACTERS[0]['GENDER'] == 'male': gn = 'moço'; prps = 'meu'
elif rs.CHARACTERS[0]['GENDER'] == 'female': gn = 'moça'; prps = 'minha'
else: gn = 'moçe'; prps = 'minhe'
 
if rs.TIME[0] > 17: dt = 'Boa noite'
elif rs.TIME[0] > 11: dt = 'Boa tarde'
elif rs.TIME[0] > 5: dt = 'Bom dia'
else: dt = 'Boa noite'

'''
0 - outro falante
1 - pausar
2 - começo do capítulo
3 - fim do capítulo

0 - ganhar dinheiro
1 - ganhar item
2 - moralidade
3 - marcador do mapa
4 - ligação
5 - novo email
6 - nova tarefa
7 - contato adicionado
8 - troféu
9 - subir de rank
10 - escolha de diálogo
11 - avançar diálogos
12 - voltar diálogos
13 - batalha
14 - exército
15 - som/música
16 - check character
17 - delivery
18 - mudar party
19 - abaixar status
20 - aumentar status
21 - dlgsav
22 - nomear
23 - outro diálogo
24 - mover personagem
25 - emoção do personagem
26 - câmera
27 - esperar
28 - tutorial
29 - outro local
30 - adicionar npc
31 - censura
'''
 
DIALOGS = {}
TASKINDEX = []

def load_dialogs(r=False):
	global DIALOGS
	global TASKINDEX

	TASKINDEX = ['Falar com a ' + rs.CHARACTERS[5]['NAME'],'Procure algo pra beber']

	DIALOGS = {
	#OBJECTS
	'MIRROR': [['Que peste feia é essa?',1,'ah.','Sou eu.',1],['Estou bonita...?',1],['Bigodin finin','Cabelin na régua',1],['Dá pra sair',1],['Sempre arrasando',1],['Tô bem arrumada',1]],
	'SIDNEY WARDROBE': [['Qual roupa vou vestir agora?',(10,['Casaco xadrez','Ok'],['Blusa preta de banda','Sempre gostei do HUG'],['Blusa social','Essa tá boa'])]],
	'BROKEN CLOCK': [['Isso tá quebrado faz tempo.',1]],
	'SIETRA PORTRAIT': [['Essa foto me traz muitas lembranças...',1,'...lembranças ruins.',1],['...',1,'Eles se davam bem...',1]],
	'JANAGO PORTRAIT': [['Legal.',1],['Essa foto foi em Búzios.',1,'Foi o dia em que nós','começamos a morar juntos.',1,'A gente comeu muito camarão naquele dia.',1]],
	'BED': [['Ah não...',1,'a cama tá bagunçada de novo',1,'...',1,'...abracadabra, cama arrumada!',1]],
	'PICTURE': [['É uma pintura bonita.',1,'não tô entendendo nada,','só sei que é bonita.',1]],
	'DIRTY SINK': [['A pia está cheia de louça suja...',1]],
	'DIRTY COOKER': [['Tem arroz frio e uma frigideira engordurada no fogão.',1]],
	'EMPTY FRIDGE': [['Água,sachês de ketchup e ovos...',1,'Considero isso uma geladeira vazia.',1],['Tá na de fazer as compras do mês.',1]],
	'JANE FRIDGE': [['A visão do paraíso.',1],['O Iago comprou um monte de sorvete.',1,'Esse idiota me conhece.',1]],
	'OLD PC': [['Esse pc ainda usa Windows XP.',1]],
	'MODERN PC': [['No canto da tela diz "Não é genuíno".',1]],
	'PC GAMER': [['O teclado LED brilhando me deixa','ma',1,'lu',1,'co.',1]],
	'OLD TV': [['O Maicon precisa trocar logo essa TV.',1]],
	'PLUG': ['Você pode encaixar um carregador aqui.',1],

	#CHESTS
	'EMPTY CHEST': ['Não tem nada aqui...',1],
	'HHBEDROOMCHEST': [[(1,'key_bedroom',0,1,'0001')]],
	'SIDNEY NIGHTSTAND': [[(1,'food_peanut_candy',0,1)],[0,'Não deveria mexer nas','coisas dos outros',1]],
	'HH FRIDGE': [[(1,'drink_beer',0,1)],[0,'Não deveria mexer nas','coisas dos outros',1]],
	'TRASH CAN': [[(1,'melee_bottle',0,1)]],
	 
	#PAPERS & SIGNS
	'TAROT POSTER': ['BÚZIOS E CARTAS','Trago seu amor aos seus pés!','978543322'],
	'MISSING POSTER': ['PROCURA-SE','Talita Manhães','Se você a viu, favor, ligue para: 992120342'],

	#ENEMIES
	'BATTLEDIALOG': [
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	[(10,['Motivar',(20,2,2)],['Ameaçar',(23,None)])],
	],

	'IRRATIONAL': ['A anomalia não entende nada do que você tá falando',1],
	'MADLADCAT': ['Miau miau','miau miau miau','miau',1,(10,['Sábias palavras','miau',1],['Magnífico',0,(31,'Não ajudou em porra nenhuma','Não me ajudou em nada'),1])],
	'TARGET': ['Parece bobo, eu sei','Mas é bom já pegar o jeito da coisa.','Ás vezes você pode negociar com o oponente','E assim poupar sua vida.','Também pode obter informações','Importantes dele',
	'Ou mesmo convencê-lo a parar de lutar'],
	 
	'VINICIUS': [(10,['Eu não quero brigar contigo','Eu também não quero','Mas é preciso'],['Você pode ficar com a recompensa','Você está blefando?',(10,['Vai pegar?','É claro que vou!','...assim que acabar com você!'],['Esqueçe','Agora estou mais invocado!'])])],
	 
	'EMOHIPSTER': [(10,['O que você escuta?','conhece aquela banda?','HUG','muito boa',(10,['eu também gosto de HUG!','sério?!','ai meu deus! que legal!'],['já ouvi falar','é muito boa cara','você tem que escutar'])],['se manda daqui ô barbudo!','como é que é?','o que você tem contra barba?',(10,['Nada oxe','é bom mesmo'],['Isso não é barba','mas...eu cuido tanto dela...'])])],
	 
	'HOTMAN': [(10,['Cê tá bem mano?','Claro que não né?? Estou queimando feito palha nessa desgraça!'],['Vaza ou meto chumbo','Eu não tenho medo de você'],['A gente não quer nada contigo',
	'Mas eu quero','Preciso de sangue!!'])],
	 
	#PLACES
	'DEPOSIT': [['Olá!','Me chamou?',1,],['Se precisar de qualquer coisa,','é só chamar!',1,(24,'n',('px300','py0'),0)]],
	'PIZZA DELIVERY': [['Aqui está.',1,(1,'food_pizza_mussarella',20,0),(24,'n',('px300','py0'),0)]],
	'REWARD':[['Ei! Você não tem sangue nenhum!','Volte quando tiver pego alguma coisa!',1],['Só isso?','Vou dar sua recompensa, mas poderia ter se esforçado mais',1],['Você conseguiu bastante sangue','Aqui está sua recompensa',1],['Uau! isso é muito sangue!','Aqui está sua recompensa pelo seu trabalho duro!',1]],
	'MERCATOR': [['Olá cliente!','Interessado em alguns produtos?',1],['Foi mal cara, mas sem grana, sem acordo.',1],['Espera um pouco cara!','Você tá sem espaço!',1,'Não quer dar para outra pessoa?',1]],
	'CASHIER INGRID': [['Os produtos estão nas pratileiras','é só você ir pegar e trazer aqui',1,0,'O quê? você quer que eu vá buscar pra você?!',1],['Você não tem dinheiro?',1,'Sério?',1],['Você tá cheio de coisas...','Não sei se posso deixar levar tudo isso.',1]],
	'CASHIER SANDRA': [['Vai pedir alguma coisa?',1],['Você tá sem dinheiro.',1],['Você tá sem espaço',1]],
	'CASHIER YASMIN': [['Eu tenho que dormir...','compra logo o que tu quer...',1],['Como é que você leva coisas','que não pode comprar??',1],['Fala sério',1,'Por favor leve só o que puder levar',1]],

	'DRITHR SANDRA': [['Licença, aqui é o Drive Thru',1],['Você tá sem dinheiro.',1],['Você tá sem espaço',1]],
	 
	'FARMACEUTIC': [['Não sabe que remédios comprar?',(10,['Não...','O que você quer tratar?',(10,['Resfriados e alergias','Se você estiver sentindo algum resfriado,','gripe, tontura ou fraqueza, um\
	 simples','xarope já basta'],['Infecções e hemorragias','Esses são problemas fortes, mas não muito graves','Para infecções, use o antibiótico correspondente ao tipo de','contaminação.',0,'Se tiver\
	  hemorragias, primeiro cicatrize a ferida','e depois ponha um band-aid para','evitar mais saída de sangue'],['Contaminação e Mal-estar','Caso se sinta alguma coisa parecida, pode ser','sinal de envenenamento ou\
	   intoxicação, existem','várias pílulas para diversos tipos de tóxicos']),'Mais alguma pergunta?',(12,7)],['Tô de boa','Tudo bem','Se tiver alguma dúvida é só perguntar','Fique á vontade'])]],
	 
	'HOTEL ATTENDANT': [['Bom dia!','O que deseja?',(10,['Uma noite apenas','O custo é de 20 por pessoa',(10,['Ok','Aqui, seu quarto é o N° 902',(0,'chave',20)],['Deixa pra lá','Volte a hora que quiser'])],
	['Estou apenas olhando','Sinta-se á vontade'])]],

	'BUS WAITER': [['Esse ônibus demora mesmo',1,'Pego ele todo dia pra','descer a serra até a capital',1,'São só 4h de viagem!',1,2]],
	'SQUARE OLD MAN': [['Eu adoro alimentar os pombinhos',1,'ainda mais aqueles que','tem um monte de penas','lindas no rabo',1,(10,['como assim?','elas chegam a hipnotizar...',
	'eu fico olhando e perco','a noção do tempo.',1],['legal','são adoráveis',1])]],
	'HOMELESS MAN': [['Pode me dar um trocado','por favor?',1,(10,['...','é sempre assim...',1],['Tudo bem',(0,-1),'Deus te abençoe!',1])]],
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
	 
	'OLD MAN': [['É bom você sempre','tirar dúvidas com o','entendido do assunto.',1,'Minha filha comprou um','antibiótico e pensou que','era pra beber.',1,'Agora ela tá no hospital...',1,'Essa menina...',1]],
	'INJURIED DAUGHTER': [['É bem vergonhoso dizer o motivo',1,'Mas estou internada porque','bebi antibiótico',1,'Devia ter escutado meu pai...',1]],
	'PRETTY MOM': [['Minha filha tá me','pertubando pra levar alguns','doces pra ela.',1,'É assim toda hora,','ela vai parar já já.',1]],
	'PRESSING CHILD': [['Mãe!','Tem tantos doces aqui!',1,'Eu quero!','Eu quero!','EU QUERO!',1]],
	 
	'DOCTOR': [['Você sofreu várias fraturas no corpo.','A conta dos cuidados foi de $100 por pessoa.',1]],
	'WORRIED NURSE': [['Você deveria se cuidar mais.','É muito comum te ver por aqui.',1]],
	'HINT NURSE': [['Tome cuidado com sua vida!',1,'Não digo por causa da saúde, mas pelo dinheiro.',1,'Se não tiver dinheiro da próxima vez, pode','entrar em prejuízo.',1]],
	'PATIENT': [['Eu quero ir pra casa logo!','A comida daqui é horrível!',1]],
	'IMPATIENT PATIENT': [['Eu tô na fila desde anteontem','Parece até que nunca anda!',1]],
	 
	'BANK GUARD': [['Ponha qualquer objeto de metal que tiver','na caixa ao lado.',1]],
	'UNLUCKY MAN': [['Não é possível','uma coisa dessas!',1,'O caixa acabou de entrar','em manutenção!',1,'ERA MINHA VEZ!',1]],
	'OLD WOMAN': [['Como que faz pra','tirar a telesena aqui?',1]],
	'SUSPICIOUS MAN': [['Estão falando que tem uma anomalia','solta na rodovia.',1,'Sendo honesto, eu não acredito','que existam anomalias.',1]],
	    
	'NPC': ['Oi...eu te conheço?','Você não deveria estar falando com estranhos','Agora não ' + gn + '! Eu tô com pressa!','Afe, mercenários...','Não quero falar com você','Licença'],
	'DOOR': ['Não conheço você','Quem é você?','O que você quer?','Vai embora!'],
	    
	'HOTEL DOOR': ['Esse é meu quarto','Aqui não é seu quarto, ' + gn, gn + 'está perdido?'],

	#PROLOGUE DIALOG
	'DALIBOR': [['VEM AQUI TODO MUNDO!!',1,0,'Que foi isso?!!',1,0,(26,4),(24,None,(184,370),8),(24,1,(180,350),2,'stand'),(24,2,(230,380),6,'stand'),(24,3,(200,330),2,'stand'),(24,4,(230,350),4,'stand'),(27,70),(25,4,'BLANKL'),
	'Estão todos os mercenários aqui?',1,(25,4,'BLANKLD'),0,'Não, tem um lá fora e outro','não chegou ainda.',1,(25,4,'BLANKDD'),0,'Ah pronto.',1,'não tenho idade pra essas coisas...',1,(25,4,'BLANKD'),
	'seguinte...',1,'vamos fazer assim então.',1,(25,4,'BLANKLD'),'você.',1,0,'quem, eu?',1,0,'Sim! você!','Pode falar o nome e sobrenome','de vocês seis?',1,(10,['Não ( nomes padrões )','Não sabe?',1,(25,4,'BLANKLU'),'Era só o que me faltava...',1,(25,4,'BLANKL'),
	'então a mulher do seu lado','vai me dizer.',1,'Beleza?',1,(22,False)],['Sim ( nomear personagens )','Ok,','Vai falando.',1,(22,True)]),'Muito bom,','Quando todos chegarem','nós vamos dar início ao','interrogatório.',1,
	(24,4,(330,300),3,'seat'),(27,20),(26,1),(27,20),(25,1,'BLANKD'),'Esquisito.',1,'Eu imaginava que um interrogatório','fosse bem mais...',1,'...pesado.','digamos assim.',1,0,'Verdade...',1,(25,1,'BLANKDD'),0,(27,30),(21,'DALIBOR',1),(23,'HHBIANCA',1)],
	['Chame todo mundo pra','começar as gravações,','por favor.',1],
	['Estão todos aqui',1,'vamos começar?',1,(10,['Espera um pouco','Venha quando','estiver pronta.',1],['Podemos','Excelente.',1,'Atenção!','Põe essa máquina','pra rodar!',1,3])]],

	'DDA AGENT 1': [['Tá procurando alguém?',1,(10,['Não','Tudo bem',1,'Se estiver precisando','de ajuda, é só','falar',1],['Sim','Eu vi um homem subindo','as escadas',1,'Deve estar lá','em cima',1])]],

	'DDA AGENT 2': [['Vocês entraram em encrenca',1,'Tem noção do que seus','preciosos olhos testemunharam?',1,(10,['Do que tá falando?','Não se faça de besta!',1,'Espero que tenha','muita coisa pra',
	'contar para o','Senhor Dalibor!',1],['Nem imagino','Você não tem noção',1,'Nunca antes se','viu um evento','dessa magnitude',1,'Por isso mesmo','nós precisamos que','vocês contem tudo','pra gente',1],
	['Eu tô com pressa','Que isso',1,'Se acalma',1,'Bebe um copo','de água',1,'Você vai ter','bastante tempo','quando falar com','o Senhor Dalibor',1])]],

	'HHSIDNEY': [[0,'Oi, ' + rs.CHARACTERS[0]['NAME'] + '.',1,(27,100),rs.CHARACTERS[0]['NAME'] + '?',1,0,'Oi ' + rs.CHARACTERS[4]['NAME'] + '.',1,0,'O que tá fazendo?',1,0,'Nada não...',1,'Só apreciando a vista...',1,0,'Ah sim...',1,(24,None,(None,None),8),(27,100),
	0,'A noite não é linda?',1,'É a minha parte favorita do dia.',1,'Ficar vendo as estrelas...',1,'As pessoas não tem mais','tempo para essas coisas','hoje em dia.',1,(10,['Verdade','Tem muita coisa que as','pessoas perdem por causa','do tempo delas.',1,
	'as pessoas deveriam aproveitar','mais as coisas a sua volta.',1,(27,100)],
	['Estava falando com ela?',(27,200),'Não é surpresa nenhuma...',1,'...né?',1]),'O que veio fazer aqui?',1,(10,['Queria saber como estava.','Ah..',1,'Valeu...',1],['Lá dentro tá chato.','Pior...',1]),(30,(320,520),'051011','HHLUCY'),
	'Olha lá.','É a ' + rs.CHARACTERS[5]['NAME'] + '.',1,(6,0,False),(21,'HHSIDNEY',1),(21,'HHJANE',1),(21,'HHLUCY',1),(28,'NOTIFICATION'),(18,[0,0,'HHJANE'])],
	['Eu já vou.',1,'Espera só um pouquinho.',1],
	['...',1,'A lua está mesmo linda',1,(27,300),'Tem algo de estranho nessa lua','Não é possível',1]],

	'HHJANE': [['Por favor vê onde',1,'O ' + rs.CHARACTERS[0]['NAME'] + ' foi.',1],
	[(24,None,(None,None),2),(30,(150,220),'011014','HHJANE'),(15,'DOOR_KICK',0),(27,60),0,'Você sabe bater a porta?',1,0,'Desculpa aí.','Achei que tinha ninguém',1,(21,'HHJANE',2),(18,[1,9]),(28,'SIGNALI')],
	['Melhor você entrar',1,'Estão te esperando',1,'Ainda mais o ' + rs.CHARACTERS[3]['NAME']]],

	'HHRENAN': [[0,'Onde será que está esse miserável?',1,(29,'highway040',1160,360),0,(31,'Puta que pariu','Que merda'),'espero não estar atrasado!',1,(21,'HHRENAN',1),(18,[2,None])],
	['Finalmente',1,(24,None,(390,160),6),(26,2),0,'Eu demorei muito?',1,0,'Tá todo mundo lá dentro','esperando você.',1,0,'Putz...',1,'Tive que resolver uma parada','antes de vir pra cá.',1,'Mas pra quê me chamaram?',1,0,'Detetives',1,0,
	'Quê??',0,'Detetives vieram pra cá',0,'Como assim??',0,'Calma aí!',0,'Véi estamos muito ferrados!',0,'O Paulo tá de boa',1,0,'Como assim?',1,0,'Pô como ninguém ia saber','o que aconteceu depois daquilo?',1,0,
	'Sei lá!','Mas o que vieram fazer aqui?',1,0,'Nem eu sei direito...','Mas eles são da PM',1,'Vão entrevistar a gente',1,0,'Beleza...',1,0,'Entra lá dentro que','Só falta você.',1,(21,'HHRENAN',2),(21,'HHDIEGO',1)],
	[(6,'drink_beer',['Eu espero você.',1],['Aí sim meu rapaz!',1,'Mano, sabe onde a ' + rs.CHARACTERS[5]['NAME'] + ' tá?',1,(10,['Não faço idéia','Putz.','Preciso resolver um negócio com ela.'],['Estava no banheiro','Ah...','Valeu']),'Já volto já.',(21,'HHRENAN',3),(18,[2,9])])],
	['Você tá carregando muita tralha!',1,'Aproveita para jogar fora','esse lixo na sua mochila',1]],

	'HHDIEGO': [[(10,['Oi ' + rs.CHARACTERS[3]['NAME'],'E aí',1],['Sabe onde está o ' + rs.CHARACTERS[0]['NAME'] + '?','Velho,','acho que ele tá lá fora.','atrás da casa.',1,
	(10,['Obrigada.','Valeu',1],['Ah tá','Deve estar falando','com aquela garota','de novo.',1,0,'Já imaginava.',1])])],
	[rs.CHARACTERS[2]['NAME'] + '!','Finalmente!',1,(10,['O que aconteceu?','Nem queira saber','A gente encontrou um espírito','aqui nessa casa',1,0,'Não brinca',1,0,'Tô te falando.',
	'Queria ver tua reação.',1,0,'Aí, mal aí por não ter vindo','Se não estivesse ocupado eu','ajudava vocês',1,0,'Que nada cara, tranquilo',1],['Já vai começar a entrevista?','A gente ia começar',
	'Mas o ' + rs.CHARACTERS[0]['NAME'] + ' tá falando','no celular',1,0,'Não é a...',0,'Sim, ela mesma.',1,0,'Putz...',1,0]),'Aí vou buscar alguma','coisa pra gente',1,0,'Beleza',1,(18,[3,7,'HHRENAN'])],
	[]],

	'HHBIANCA': [['O que foi?',1,0,'Era Iago.','Perguntou se eu tava bem.',0,1,'Ah tá.',1,2,'Pelo menos ele se preocupa','com você.',1,0,(25,None,'BLANKDD'),'Sim.',0,1,(27,100),'Percebeu onde a gente.','conseguiu chegar?',
	1,0,(25,None,'BLANKLD'),'Como assim?',0,1,'Ás vezes nós não','nos damos conta...',1,'...mas agora a pouco eu','era pesquisadora,',1,'e agora além de tudo a gente','sai pra caçar monstros.',1,'não é esquisito?',1,
	(10,['Não são monstros','Você entendeu o que eu','quis dizer!',1],['Muito esquisito','Não é?',1]),'Isso parece até coisa de filme.',1,'Mas isso não é errado?',1,(10,['Acho que não','Mas por que?',1,0,
	'A gente não está salvando','as pessoas?',1,'Eu acho que isso é o','que importa.',0,1],['Eu não ligo','Sei não...',1,'Não gosto dessa coisa de matar','bichinhos.',1,0,(24,None,(None,None),5),(25,None,'BLANKL'),'Mas não são bichos, garota!',0,1]),
	'Eu sei',1,'Mas mesmo assim...',1,0,'Ei',0,1,'O quê?',1,(10,['Não se culpe por isso',0,'No começo parece que','você está fazendo a coisa','mais cruel do mundo,',1,'se já deve ser difícil',
	'pra quem trabalha na polícia,','imagine pra gente!',1,'Nós apenas estamos fazendo','o que é melhor pra todos.',0,1],['Eu já me acostumei',0,'Não ligue para o que os','outros dizem.',1,
	'Eles não são a gente','pra dizer alguma coisa!',1,'Se estivessem no nosso lugar','fariam o mesmo.',0,1]),'Sim, mas...',1,'...',1,'...precisa ser matando...?',1,(21,'HHBIANCA',1),(23,'DALIBOR',0)],
	[0,'Viu o ' + rs.CHARACTERS[0]['NAME'] + '?',1,(25,1,'BLANKD'),0,'Não, não vi...',1,0,'Vê onde ele está, por favor?',1,0,'Tudo bem.',1,(18,[4,1,'HHJANE']),(28,'WALK')],
	['Ei, você viu','se ele já voltou?',1,(10,['Eu ia perguntar isso','É, ele não aparece',1,(10,['Pode procurar ele?','Claro'],['Não vi ele','Ele tá demorando','muito...',1]),'Eu já volto',1,(18,[4,1,'HHLUCY'])])],
	[rs.CHARACTERS[3]['NAME'] + '!','Quem mandou você entrar aqui??!!',1]],

	'HHLUCY': [['O ' + rs.CHARACTERS[2]['NAME'] + 'tá demorando muito.',1,'Acho que vamos ter que','começar sem ele.',1],
	['E aí ' + rs.CHARACTERS[0]['NAME'] + '.','Daqui a pouco vão começar a entrevista',(10,['O ' + rs.CHARACTERS[2]['NAME'] + ' chegou?','Ainda não...','Mas já deve estar chegando.',1,
	'O Dalibor está pensando em','começar logo sem ele.',1,0,'Quem é Dalibor?',1,0,'O detetive.',1],
	['Espera eu terminar','Muito ocupado você hein...',1]),'Então tá.','Quando acabar aí vem pra sala.',1,(21,'HHLUCY',2),(21,1),(18,[5,2,'HHSIDNEY'])]],

	'HHBASEMENT': [['O que é isso?',1,(15,'TREASURE',0),(27,100),(1,'mysterious',0,1),'Que esquisito.','Preciso mostrar pra ' + rs.CHARACTERS[4]['NAME'] + ' depois.',1,'Espera',1,'Ah não...',1,(13,'missingno3')]],

	'HHMERCHANT': [['Hey!',1,'Psiu!',1,(27,20),'Aqui!',0,'Que susto mano!',0,(10,['Que tá fazendo aí?','Eu tô no armário',1,(15,'LAUGHS',0),(27,120)],['Isso é hora cara?','Preciso arrumar meu trampo',
	'Não tá fácil pra ninguém']),0,'Você não devia estar aqui.',1,'Tá rolando mó treta aqui','por causa de uma assombração.',1,0,'Nem pensar.',0,'Papo reto','É o que me disseram.',1,0,'Olha',
	'Eu posso até não acreditar,','Mas sejam dias de luta ou','dias de glória eu vou','continuar meus negócios.',1,'Não quer descolar nada não?',1,0,'Agora não véi',0,'Sabe que te considero muito né?','Você é meu mano né não?',0,
	'Sim mas-',0,'Ajuda o parça aqui pô','Vai me deixar na mão?',0,'AGORA NÃO DESGRAÇA!',1,0,rs.CHARACTERS[2]['NAME'] + '?',(24,None,(None,None),3),(30,(260,200),'051011','HHLUCY'),0,'Ah, oi' + rs.CHARACTERS[5]['NAME'],'Tava te procurando',1,0,'Mesmo?',1,
	'Todo mundo tá procurando você!',1,0,'Sério?',1,0,'Sim! o que tá fazendo aí?',1,0,'Tava só-',0,'Vai logo pra sala!',(21,'HHRENAN',3),(18,[5,10,'HHRENAN'])]],

	'HHCLIFFS': [[(28,'CLIFFS')]],

	#DUPLO ANDANTES
	'CH1IAGO': [[(31,'CARALHO!!','MERDA!!'),1,0,'O QUE FOI ISSO!?',0,'EU NÃO SEI!',1,(27,200),'A gente deveria dar uma olhada?',1,(10,['Você vai sozinho!','Tá bom, tá bom,',0,'Fica aí que eu já volto.',1],
	['Melhor a gente olhar','Ok...','...mas vamos devagar.']),(27,500),0,'ai meu deus.',1,'AI',1,'MEU','DEUS',1,0,'Fica calma ' + rs.CHARACTERS[1]['NAME'] + '.','Tá tudo bem...',0,
	'COMO ASSIM TUDO BEM!?','A GENTE ATROPELOU UM BULLDOGUE ' + NAMES[0] + '!!',(31,'PUTA QUE PARIU!','MISERICÓRDIA!!'),1,(27,20),'A gente não pode deixar isso aqui!',1,'Que que a gente faz?!',1],
	[(27,300),'Me desculpe bem.',1,'Não havia nada que','possamos fazer.',1,(27,300),0,'Iago...',1,'O que é isso?',1,(27,200),0,'Mais um...',1,'Bul...','...dogue?',1,0,'Não...','É....','Não pode ser....',1,(27,200),
	'CORRE IAGO!!',0,'COMO É?',0,(31,'CORRE BUCETA','NÃO PARA'),'ELE TÁ VINDO!!',0,'ISSO É LOUCURA!',0,'AAAAAHHH!!!',0,'AHHHHHH!!!',(13,'CERBERUS')]],
	    
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
	'Ei pera!',1,(27,100),'Tá vindo alguém!',0,'Rápido se escon-',(13,'pietra')]],

	#NÃO SE META COM A GANGUE
	'PROLOGUE': [['Hey?','...','Está me ouvindo?','hm?','Você entendeu o que eu disse?','Pra ser sincera, não','...','Estava pensando, com a cabeça em outro lugar...','...sobre o quê você estava pensando?','...eu...eu fiz\
	 coisas...','...','...eu fiz coisas que...tantas coisas...que não...pensei direito','...','...eu me arrependo tanto, nada disso deveria ter acontecido, foi tudo por causa de uma briga, e eu trouxe essa desgraça\
	 pra minha vida...eu achei que poderia ajudar nós dois, achei que eu seria aquela que iria nos tirar do buraco...','...','...mas no final eu só afundei ainda mais....','é natural pensar coisas assim, mas tente sempre\
	 se lembrar que o que você fez você não fez por mal, você estava querendo ajudar, achar uma solução','...sim...','isso não te anima?','nem um pouco...porque eu atrapalhei ao invés de ajudar...não fui inteligente','é\
	 difícil','muito...mesmo...','...','você está fazendo atitutes inteligentes agora, está procurando ajuda, reconhecendo seu erro, se afastando daquilo que te traz problema','...sim...','você precisa\
	 continuar assim','...','ei','?','me prometa de que você nunca mais vai voltar a pegar em uma arma, certo?','certo! certo!','nem que um monstro apareça no mato ou um bandido invada sua casa, nunca, NUNCA MAIS, encoste\
	 em nenhum arma!','...','está me ouvindo?','sim','ótimo...','...','já está na hora de ir','não pode ficar mais um pouco?','desculpa, mas pode continuar amanhã, eu também tenho sanidade mental','claro, \
	desculpa...',[2,'990435671',True]]],
	    
	'CH3MAICON': [['Então...',1,'Como tá o trampo?',1,0,'Que trampo?',1,0,'Você sabe,','o de mercenário',1,(27,60),'Tá muito puxado?',1,0,'...bastante.',1,0,'Acho que já ouviu','alguns comentários sobre eles.',1,0,'Sim...',1,'Até demais, mas nem ligo.',1,0,
	'Como não?',1,0,'Mano, foi graças á essa vida','que tô onde tô agora.',1,'Não vou deixar que alguns comentários','mudem minha cabeça.',1,'Eu gosto do que faço',1,0,'Sim, mas seria melhor você arranjar','alguma outra coisa né?',1,0,'Isso até eu quero né?',1,0,'Então por que você',' não sai dessa?',1,0,'Porque não dá cara!','Não vão contratar alguém','com ficha suja',1,0,'Ah, é mesmo...',1,0,'Além do mais eu já','me garanto onde eu tô,','se eu trocar de emprego ','posso ser demitido de novo',1,0,'Já passou perrengue demais, não é?',1,0,'Sim',1,0,'...sei não.','Ainda acho melhor você fazer','alguma outra coisa.',1,'Esse negócio de matar e','arriscar a própria vida...',1,0,'Que vida?',(27,300),0,'Ficou parecendo aqueles','adolescentes sadboys.',1,0,'É eu sei...',1,
	'Eu já tô indo',1,0,'Deixa que eu pago essa',1,0,'Sério?',1,0,'Sim','É por minha conta',1,0,'Você é demais cara',(6,2,False)]],

	'CH3JANE': [[0,'Teria sido melhor','ficar lá no bar',1,(27,300),0,'BORA LOGO!',1,'NÃO TENHO O DIA TODO!',1,'Que saco...',1,'Que demora',1,'Pra você ver né,','Até pra isso tem','toda essa baboseira',1,0,'Hã?','Ah, sim, sim, sim...',1,0,'Era pra ser um negócio rapidinho...','tranquilo, de boa, mas não!','Eu sou obrigada a ficar','aqui esperando!',1,0,'Eu já tô até acostumado',1,0,'Ai não ia me acostumar nunquinha,','deus me livre',1,0,'É que já é coisa da rotina,','todo ano tem isso.',1,0,
	'É?',1,0,'Ahã...','só que agora saiu mais cedo,','geralmente é só lá pra setembro',1,0,'Você é mercenário?',1,0,'Sou.',1,0,'Ah...','Pra saber dessas coisas...',1,0,'Por que?','Você não é?',1,0,'Não, mas daqui a pouco','já tô virando uma!',1,0,'Mas aqui não é onde','renova a carteira?',1,0,'Não, disseram que o registro','é aqui também',1,0,'onde?',1,0,'no último guinchê',1,0,'Ah sim, agora eu vi',1,0,'Vem cá, e como é essa coisa','toda de mercenário, matar pessoas...',1,0,'A gente não mata pessoas',1,0,'Ah sim, desculpa...',1,0,'Não, tudo bem, é normal',1,0,'Então o que vocês fazem exatamente?',1,0,'Olha, a primeira coisa que','você deve saber se quiser','virar mercenária, é que certas','coisas são totalmente confidenciais',1,0,
	'Uh! sério?',1,0,'Sim, sigiloso',1,0,'Tipo homens de preto né?',1,0,'Não é pra tanto,','Mas é tipo',1,0,'Mas eu achava que era só','matar e ganhar dinheiro!',1,0,'ihhhh...',1,'Vai sonhando, é um bicho chato',1,0,'Sério?',1,0,'Quer dizer, tirando toda a diversão,','ainda é um trabalho, tem que','estar sempre disposto, te chamam na','hora que querem, é cansativo,','tem os chefes, a gente recebe pouco...',0,'QUÊ?',0,'fala baixo!',0,'desculpa',1,(27,120),'...recebe pouco?',1,0,'depende do quanto você caça.',1,0,'Ah...então se eu','caço bastante...',0,'ganha bastante, isso aí',1,0,'Mas o que vocês caçam exatamente?',1,0,'segredo',1,0,'Ah! deixa disso!','Fala logo!',1,0,'Se quiser saber mesmo,','Vai ter que esperar até lá dentro',1,0,'tá bom então...',1,'Ô agente G',1,'Beleza James Bond',1,0,'tá já chega',1,0,'ei já tá na sua vez',1,0,'ah sim',1],
	['Então esse é seu nome?',1,0,'Sim...' + rs.CHARACTERS[0]['NAME'] + rs.CHARACTERS[0]['LASTNAME'],1,0,
	'Prazer, ' + rs.CHARACTERS[1]['NAME'],1,0,'Prazer',1,0,'Então...o que tem que fazer agora?',1,0,'Bom, agora você pode','pegar sua primeira arma ali.',1,'E se quiser já pode treinar','Um pouco de tiro',1,0,'Você vem comigo?',1,0,
	'Não...eu já tenho que ir',0,'Ah por favor!','Eu não entendo das coisas aqui!',1,'please!',1,(10,['Tá bom','YASS',0,'Não se empolga, tá.',1,0,'Então tá,','Onde que pega o brinquedinho?',1,0,'Me segue',(11,1)],['Agora não','Tudo bem então...',1,'A gente se vê por aí',1,0,'Eu tô aqui todo dia',1,0,'Beleza!',1,(27,180),'Ah! eu só posso vir','aqui nos sábados!',1,0,'Beleza!',1,0,'Tchau!',1,(27,210),0,'Essa garota tá querendo alguma coisa comigo...',(11,3)])],
	['É aqui que faz o treinamento?',1,0,'exatamente',1,0,'Ok...',1,(27,60),'me ensina a atirar?',1,0,'Tudo bem',1,(9,2),'Primeiro põe esses óculos aí',1,0,'esses?',1,0,'sim, agora mira','Não põe muito perto','senão machuca o olho',1,0,'Já sei disso',1,0,'e...aperta o gatilho',1,(13,'Alvo')],
	['Nossa!',1,'Mandou muito!',1,0,'Eu sou demais!',1,0,'Não sério,','Você já atirou antes?',1,0,'Um pouquinho',1,0,'Um pouquinho?!',1,0,'Tá, eu sei atirar',1,0,'Se você já sabia atirar,','por que pediu minha ajuda?',1,0,
	'Ai,ai...','Faz muito tempo já,',1, 'Começei quando...',(3,EMAILS[0].copy()),0,'Pera aí rapidinho',1,0,'O que foi?',1,0,'Chegou email',1,(27,200),'Desculpa ' + rs.CHARACTERS[1]['NAME'] + ', eu tenho que ir!',1,0,'De novo?',1,0,
	'É um caso pra resolver',1,0,'Agora?',1,0,'É o que eu te falei antes',1,0,'Posso ir com você?',1,0,'Vai devagar querida,','Eu tô em outro nível',1,0,'Por que não posso ir?',1,0,'Muita coisa ainda, muita coisa,','Te explico depois',1,0,'Pera aí! Mizera...']],

	'CH3VINICIUS': [[(15,'battle_incoming',1),'O que tá fazendo aqui?',1,0,'Quem pergunta sou eu!','O que VOCÊ tá fazendo aqui?',1,0,'Com certeza não é deixar você','roubar minha recompensa',1,0,'E quem disse que ela é sua?',1,0,'Garoto,melhor sair do meio,','ou vai dar muito mal','pra nós dois',1,0,'que assim seja então!',1,(13,'madladcat','vinicius')],
	['Lembra de mim, filho da mãe?',1,0,'você!',1,0,'Essa é pra aprender a não mexer comigo!',(9,2),'???','O que você estava fazendo?',(10,[],[])]],

	#CAMINHÕES CANAVIEIROS
	'CH4PAUL': [['Vocês já estão chegando','no local?',1,0,'Não se preocupe.',1,'Nós estamos a caminho.',1]],

	#O PASSADO TE CONDENA
	'CH5RENAN': [[(15,'battle_incoming',1),'Você mexeu com a','turma errada, cara!',1,'Tá na hora de','aprender uma lição!',1,(14,0)]],

	#O CRIME NÃO COMPENSA
	'CH6VINICIUS': [[0,'FIOCRUZ?',1,0,'Pois é.',1,0,'Por que a gente assaltaria','um lugar desses?',1,0,'Ele falou que lá dentro','tem uma coisa muito importante.',1,'Ao que parece são','amostras de sangue.',1,(27,20),0,
	'...ele quer fraldar um teste de DNA?',0,'Eu lá vou saber cara!',1,'Mas parece que ele vai',' pagar bastante pra gente fazer isso.',1,'E a gente também tem algumas','informações pra nos ajudar.',1,
	'Vocês estão sabendo da festa','que vai ter lá na Cinelândia, certo?',1,0,'ahã.',0,'então,','lá vai estar uma pesquisadora','que é a quem manda nas amostras.',1,'É só a gente ir atrás dela!',1,0,'Ah, vai ser moleza!']],

	#PELO BENEFÍCIO DE MR. KITE!

	#DR. ESTANHO

	#MILÍCIA X MELIANTE

	#NÃO IDENTIFICADO
	'CH10HERMES': [[0,'Olá?',1,(27,60),'Alguém em casa?',1,(27,100),0,'Olá!',1,'Em que posso ajudá-los?',1,0,'Boa tarde senhor,','Essa fazenda é sua?',1,0,'Oh sim, é minha desde','que meu avô começou a capinar,','quando tudo isso ainda era mato!',1,0,'...mas só tem mato aqui senhor',1,0,
	'Pois é.',1,'Faz um bom tempo que','não tem ninguém para','cuidar da minha fazendinha.',1,'Só resta eu e minha maloca...',1,0,'Mas esses animais também são seus?',1,0,'Ah não.','Apareceram aí!',1,'Não são criatuinhas de Deus?',1,
	'Nossa ' + rs.CHARACTERS[1]['NAME'] + ', tem um Boi Dourado ali!',1,0,rs.CHARACTERS[3]['NAME'] + '!','Se concentra!',1,'Então...nós somos...',1,0,'...detetives?',1,(27,120),'...sim! sim, detetive ' + rs.CHARACTERS[3]['NAME'],'E minha colega, detetive ' + rs.CHARACTERS[1]['NAME'] + '.',1,
	'Muito prazer, me chamo Hermes.',1,'Eu já imaginava que fossem,','pois não tem uma semana','que alguém bate na minha porta!',1,0,'É mesmo?',1,0,'Sim! vocês não sabem?',1,0,'Não, viemos de outra cidade',1,0,'Ah...',1,'Vieram de onde?',1,0,'Vargi...',1,0,'Itatiaia!',0,'Pera, quê?',0,
	'Não é que ele',0,'A gente acabou de vir de Itatiaia, mas estamos indo pra Varginha',1,0,'É, isso mesmo',1,0,'Interessante...',1,'É porque Policiais vieram','aqui perguntando um monte de baboseira...',1,'Umas presepada que','não sei nem o nome!',1,0,'Geóglifos?',1,0,
	'Sim',1,'E acho que você gostariam','de saber algo a respeito, não é?',1,0,'Sim, o depoimento dos moradores','próximos é muito importante!',1,0,'Bom, eu não sei nada desses','Zoológicos coisa nenhuma.',1,'Mas por alguma razão','todos vem me perguntar',1,0,'É porque, Sr. Hermes,','os Geóglifos estão na sua fazenda',1,0,'Pois é, mas é justamente porque','ela está a tanto tempo parada','que não me informo','dessas coisas, entende?',1,'Talvez alguma pessoa tenha','invadido meus campos e fez','esses desenhos no mato!',1,0,'Hermes...',0,'Olha ' + rs.CHARACTERS[1]['NAME'] + ', acho que já','conseguimos informações o','suficiente do Sr. Hermes.',1,'E aliás, acho que','um vândalo qualquer seria','mais suspeito do que','qualquer aposentado de','meia-idade',1,'Eu trabalho',1,'Ah, sério?',1,'Sim, eu vendo artesanato',1,'Boas vendas, Hermes',1,'Muito obrigado...',1,rs.CHARACTERS[3]['NAME'] + '.',rs.CHARACTERS[3]['NAME'] + '!','Muito obrigado pela','ajuda de vocês!',1,'O prazer é todo nosso!',1,(27,120),0,'Por que fez isso?',1,0,'Muita gente já falou com ele.',1,'Se fizermos perguntas demais','ele pode fazer alguma coisa!',1,0,'O quê? destruir provas?',1,0,'Exatamente isso',1,0,'Por que ele faria isso?',1,0,'É o que estamos','tentando descobrir!',1]],

	'CH10JANE': [['Ainda não entendo como','foi tão simpático com','aquele velho...',1,'Por que?','Você acha ele mau?',1,0,'Não...mas eu desconfio dele.',1,'Não deveria falar','desse jeito com ele',1,0,'Então o que você sugere?',1,0,'Seja mais duro?!',1,0,'Não dá pra gente','conseguir nada das','pessoas sendo duro com elas',1,0,'Os policiais conseguem',1,0,
	'Ele é um cara muito suspeito,','isso a gente já sabe,','mas como ninguém conseguiu','tirar provas dele,','quer dizer que ele é','muito bom em guardar segredo',1,0,'Eu não sei...',1,'acho que a gente','devia sequestrar ele',0,
	'Claro que não!',0,'Nossa calma!','Eu só tava falando...',1,(27,60),'Então o que a','gente vai fazer?',1,0,'Vamos continuar investigando',1,0,'Ah sim,','Claro que sim...',1,0,'O problema de leigos','como você é que eles','tentam começar de cima...',1,(24,None,(None,None),3),(27,60),0,'Como é que é?',1,0,'É a verdade',1,0,
	'Olha me escuta aqui ' + rs.CHARACTERS[3]['LASTNAME'] + '!','Você não sabe quem','eu sou e de onde eu vim!',1,'Então é bom você ficar','calado que aí você ganha','mais e não caga pela boca!',1,0,'Ok...',1]],

	#QUÍMICAS QUIMERAS
	'CH11SIDNEY': [[0,'Aí está você.',1,0,'Pois é...',1,'A gente já vai embora.','Precisamos capturar anomalias','para competir.',1,0,'Hã? Como é?',1,0,'Foi o único jeito.',1,0,'Achava que era','contra essas coisas!',1,0,'Agora as coisas são','um pouco diferentes',1,'Ou são 3 galos de combate','ou é toda a fauna da','mata atlântica.',1,'De quebra a gente','pode ganhar uma grana!',1,0,'Ah sim...',1,'Tem isso aí...',1,0,
	'Falando nisso, onde','estão meus 300 reais?',1,0,'Então...',1,(27,60),0,rs.CHARACTERS[0]['NAME'] + '.',1,'Cadê meus 300 reais?',1,0,'Olha só tenta','entender a situação.',1,'Eu queria ajudar a gente','apostando dinheiro nas','anomalias de combate.',1,'Eu tava indo bem,','bem pra caramba.',1,'Só que...',0,'Só que o quê?!',1,0,'Bom...',1,'Como tava ganhando muito','eu fui logo com tudo.',1,
	'Então apostei todo o','dinheiro que a gente tinha.',1,(27,300),0,'Oi?',1,'A gente ia ganhar o dobro!',0,'CARA QUAL É TEU PROBLEMA!!',0,'VOCÊ FARIA O MESMO!!','EU TAVA ENRIQUECENDO A GENTE!!',0,'Eu não acredito nisso','Era o bolsa família da minha mãe',0,'Tá e o que você quer','que eu faça?',0,
	(31,'QUERO QUE VÁ SE FUDER ' + rs.CHARACTERS[0]['NAME'] + '!','QUERO QUE VÁ SE FERRAR ' + rs.CHARACTERS[0]['NAME'] + '!'),0,(31,'VAI TOMAR NO CU TAMBÉM','VÁ TE CATAR TAMBÉM'),(27,180),0,'Eu preciso desse dinheiro...',1,'Você nem tem noção...',1,0,'Ok...eu tô te devendo essa.',1,'Eu vou te ajudar a','capturar algumas pestes.',1,0,
	'Eu ia te chamar','de qualquer jeito!',1,0,'Tá bom!','Se acalma!',1,0,(31,'Puta que pariu...','Misericórdia...'),'Vamos embora logo...',1]],

	#QUEM ACREDITA EM ASSOMBRAÇÃO?
	'POLTERGEIST': [[(10,['Você está aqui?',(27,120),'Mexeu!','Como isso é possível?',0,'Silêncio!'],['Charlie Charlie'])]],

	#AFASTA DE MIM ESSE CÁLICE


	#CONTACTS CALL
	'989074454': [['Sidney']],
	    
	'991124257': [['Oi! Sou eu, a Jane']],
	  
	'990435671': [[[rs.CHARACTERS[1]['NAME']+'! Precisamos de você aqui AGORA!','Eu sei que você saiu e coisa e tal, mas a gente PRECISA DE VOCÊ!','Estamos na Av. Jobim, venha logo!',[4, 'Urgência na Av. Jobim']],
	['Caramba '+rs.CHARACTERS[1]['NAME']+', será que você não entende a gravidade da situação??','Só você pode deter essa anomalia!']]],
	    
	'926148930': [['E aí mano? Beleza?','Então, aquela parada da transferência deu certo, adivinha?','Amanhã á noite eu tô indo pra Nova Friburgo!',0,'Tá tendo umas paradas estranhas lá, e me mandaram examinar','Vamos aproveitar pra gente se ver, beleza?']],
	  
	'976564008': [['Agora não, ' + rs.CHARACTERS[0]['NAME'] + '! Eu tô trabalhando!','Me ligue depois, estou fazendo coisa importante aqui!']],
	  
	'940028922': [['Oh, olá! como vai, '+rs.CHARACTERS[0]['NAME']+'?','Tenho andado ocupada esses dias, muita coisa pra fazer...','Não dá pra falar com você agora, desculpa','Me ligue mais tarde, ok?'],
	['oie']],
	    
	'990271802': [['Garoto, o chefe quer te ver o mais cedo possível na delegacia',1,'Espero que não tenha feito merda...',1,'Bláblabla','blablabla','blablabalbala','blablablaba',1,0,'entendeu?',1]],
	    
	'987690021': [['Paulo']],
	  
	'953478809': [[dt + ', em que posso ajudar?',(10,['uma pizza grande','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 2, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY'})],
		['uma pizza média','já estamos á caminho',1,(17,'deliver',600,{'TYPE': 2, 'INDEX': '001003', 'WHO': 'PIZZA DELIVERY'})])]],
	  
	'909236521': [[dt + ', correios']],
	  
	'923778988': [['Alô?',1,(16,0,[rs.CHARACTERS[0]['NAME'] + '! a quanto tempo cara!',1]),'Precisando de ajuda em','carregar algumas coisas?',1,'Não tem problema, o pai tá aí','pra resolver já já!',1,
	(17,'deliver',600,{'TYPE': 4, 'INDEX': '001003', 'WHO': 'DEPOSIT'})]],
	  
	'969696969': [['Olá ' + prps + ' cliente, em que posso ajudar?','você está a procura de meus serviços?','chegarei em instantes',1,[17,'mercador',0,3]]],
	  
	'977904623': [['Hey!','Você está bem?','Onde você tá?','O que tá acontecendo?','Você se machucou?',[10,['Eu tô bem','Mesmo?',1,'Ufa...',1],['Fique calmo','Não consigo me acalmar',1]],'Eu estava preocupado','com você',1,
	'mas graças a','Deus você está bem',1,'Aquela mulher chamando','vocês aos prantos me','deixou assustado',1,'Você deve estar','cansada depois de','tudo o que passou',1,'Engraçado, não é?',1,'Você mal saiu','dessa coisa de mercenária',
	'e já tá na ativa','novamente',1,'Mas assim...',1,'...',[10,['Pode falar','não...','é que...',1,'Não quero que a gente','se afaste de novo',1,'Não agora que tá','tudo dando muito certo',1,'Não precisa ser','que nem seu amigo','mercenário',1,
	'ah é, esqueci','de te contar',1,'Eu fiquei sabendo','dele e tudo isso','sobre aquela garota',1,'bem problemático',1,'Não...',1,'Esquece eu só','falei besteira',1,'Só quero que','você não seja','ausente como eu','fui com você',1,'entende?',1,
	[10,['Sim','Ainda bem que','entendeu',1],['Não','Esquece isso',1]]],
	['Eu já ligo de volta','Tudo bem','Você deve estar','muito ocupada agora',1]]
	,'A gente se fala mais','em casa, então',1,'te amo, ok?',1]],
	  
	'923578103': [['Sofia']],
	  
	'960428331': [['Vinícius']],
	 
	'978543322': [['Oi, em que posso ajudar?','Ah...eu já parei de fazer isso há muitos anos','Tchau']],

	#EASTER EGGS
	'TWNN CLOCK': ['Você tem a hora certa?',1,(15,'TWNN',0),(27,600),0,'Não.',1],
	'KONAMI GUY': ['Hey, sabe o que acontece se você apertar cima, cima, baixo, baixo, esquerda, direita, esquerda, direita, B, A e START?','Merda nenhuma!'],
	'MATT KAI': [['EU AMO PINK FLOYD','EU AMO PINK FLOYD','EU AMO PINK FLOYD',1,0,'Esse é o criador do jogo?',1,0,'Ele mesmo',1,0,'Sem nexo',1,0,'Mó fita',1]],

	#ADVICE
	'ADVICE': ['Desculpe interromper','Mas é uma história muito longa','para se contar.',1,'Não vai querer continuar amanhã?','Nós gravamos tudo o que você falou',1,'E então?',(10,['Tudo bem','Ótimo','rapazes, guardem suas coisas',4],['Espere um pouco','Tá bom então...','vamos prosseguir',1])]
	}

	if r == True:
		rs.DLGSAV = {}
		for i in DIALOGS: rs.DLGSAV[i] = 0

SIGNS = {
'INN': 'pousada', 'PUB': 'bar', 'HOTEL': 'hotel', 'DRUGSTORE': 'drogaria', 'BAKERY': 'padaria', 'BAZAAR': 'bazar', 'MARKET': 'mercado', 'BANK': 'banco','GAS': 'posto','HOSPITAL': 'hospital',
'POLICE': 'delegacia', 'SHOP': 'loja'
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
     
MANUAL = [['CONTROLES',['Aperte ' + pygame.key.name(rs.LEFT[0]) + ', ' + pygame.key.name(rs.RIGHT[0]) + ', ' + pygame.key.name(rs.UP[0]) + ' e ' + pygame.key.name(rs.DOWN[0]) + ' para mover seu personagem']],\
['CELULAR',['O celular é o equivalente ao','menu do jogo, acesse-o','apertando ' + pygame.key.name(rs.PHONE[0]) + '.','\
','Na barra superior do celular,','aparecem informações de data,','hora, sinal e carga.','\
','Atente-se á carga do celular:','ao se esgotar, você fica','incapacitado de utilizá-lo, para','carregar, use o carregador.','Utilize carregadores portáteis','ao se afastar da área urbana.','\
','Os créditos servem para fazer','ligações, recarregue-os na','farmácia.','\
','Fora da área urbana, o sinal',' pode diminuir, e alguns','aplicativos estarão indisponíveis.','\
','Esses são os aplicativos que','pode usar:','\
','MAPA: ver o mapa da cidade,','traçar rotas e ver informações','dos locais. Não mostra as','regiões florestais.','\
','CHAMADAS: ver os contatos','salvos, histórico de ligações','e fazer chamadas. Quanto mais','longa for a chamada, mais','créditos são gastos.','\
','EMAIL: ver emails enviados da','agência e outras instituições.','\
','NOTÍCIAS: ver as últimas notícias','da região, podem aparecer casos','resolvidos e casos para resolver.','\
','RÁDIO: escutar música aleatória','de várias estações diferentes,','ao se afastar da área urbana','não é possível utilizá-lo.','É necessário um fone de','ouvido para usá-lo.','\
','CÂMERA: tirar capturas de tela e','ver capturas salvas.','\
','TAREFAS: ver missões e casos','já cumpridos ou para cumprir.','\
','STATUS: ver as informações','completas dos atributos','do jogador.','\
','BESTIÁRIO: banco de dados da','agência onde se registram','todas as anomalias.','\
','CONQUISTAS: ver todas as',' conquistas do jogo.','\
','PLACAR: ver sua posição no','placar do jogo.','\
','AJUDA: ler o manual completo','do jogo.','\
','CONFIGURAÇÕES: editar opções','de som, imagem, controles,','idioma e etc.','\
','SOBRE: ver créditos e liçenca GNU.','\
','SALVAR: salva o progresso','atual do jogo.']],\
['BATALHA',['Para vencer uma batalha, você deve derrotar todos os inimigos da tela ao mesmo tempo que deve se defender dos ataques inimigos.','\
HP: A barra vermelha mostra seu HP, ela pode ser maior dependendo do seu nível de VITALIDADE, a barra diminui com o ataque inimigo e uma barra amarela diminui lentamente com ela, baseada no nível de RESISTÊNCIA.\n\n\
PP: Mostra a quantidade de munição para as armas de fogo, sendo a barra diferente para cada arma.','\
XP: Seu nível de experiência, quanto mais experiente for nas batalhas, maior seu grau dentro da agência.','\
Numa batalha, aparecem como opções os itens equipados, mas você também pode abrir seu inventário e fugir da batalha. Seu desempenho ao atacar é baseado nos seus atributos, \
ao mesmo tempo em que os inimigos também possuem seus atributos para defender, sendo esses: ','\
ATAQUE: distância dos extremos da barra','\
AGILIDADE: velocidade do cursor da barra','\
RESISTÊNCIA: velocidade de consumo da barra de HP','']],\
['LOCAIS',['']]]
    
BATTLE = [' aparece no caminho!',' encurrala você!',' é emboscado!',
'incrível!','errou...','outra vez!',
'vitória!','perfeito!','derrota...','acertos: ','dano total: ','vitalidade perdida: ','bônus de tempo: ',' de experiência',
' foi promovido para o nível ',
' tentou fugir','...mas falhou','...e consegue!',
' vai ',' usa ',' perdeu ',' ganhou ',' de ATAQUE',' de AGIIDADE',' de FORÇA','de RESISTÊNCIA',
' está com resfriado',' está com febre',' está desidratado',' está com náusea',' não consegue se mexer!',' está inconsciente...',' foi atacado por um parasita',
' está queimando!',' foi envenenado!',' está com hemorragia!',
' foi quebrado...',
' entrou na batalha!', 'Mas não funcionou...',
'força','ataque','agilidade','resistência','vitalidade',
'Um exército aparece para te atacar!','maravilhoso!']
  
MENU = ['mapa','chamadas','correios','notícias','rádio','câmera','bestiário','tarefas','status','táticas','conquistas','placar','manual','ajustes','sobre',
'sem conexão','não há contatos','sem créditos...','sem dinheiro...','não há mensagens','sem sinal','nenhuma anomalia registrada','não há tarefas',
'grupos','contatos','histórico','novas','lidas','todas','fazer','feitas','novo grupo',
'créditos: ','chamando...','DE: ','PARA: ','nova tática','VITALIDADE: ','FORÇA: ','ATAQUE: ','AGILIDADE: ','RESISTÊNCIA:',
'RESFRIADO','FEBRE','SEDE','NÁUSEA','PARALISIA','INCONSCIÊNCIA','PARASITA','QUEIMADURA','VENENO','HEMORRAGIA','REFORÇOS','ROUBAR',
'equipamento 1','equipamento 2','equipamento 3','equipamento 4','dialogar','defender','fugir','nova história',
'idioma','sfx','música','mover cima','mover baixo','mover esquerda','mover direita','ato','celular','inventário','velocidade','cor R','cor G','cor B','salvar',
'escolha um botão','volume','peso','Nome','Sobrenome','Tudo certo?','Sim','Não','Tem certeza?','correr','borda','gameplay','áudio','controles','muito lento','lento','médio','rápido','muito rápido',
'censura','dicas']
  
SHOP = ['comprar','sair','nada aqui','banco: $','dinheiro: $','sacar','depositar','cancelar','Mercador','vender']

HOLIDAYS = [(1,1,'Feliz ano novo!'),(3,8,'Feliz dia da mulher!'),(3,15,'É aniversário do autor!'),(4,7,'Feliz páscoa!'),(4,22,'Feliz dia da terra!'),(10,31,'Feliz Halloween!'),(12,25,'Feliz natal!')]

ABOUT = ['MUTATION PURGE','Matt Kai (2020)','Source code por Matt Kai','Feito em Python','Twitter','GitHub','GNU General Public License']
  
DISCLAIMER = ['Esta é uma obra de ficção,','e quaisquer semelhanças com','acontecimentos reais são','mera coincidência.','',
'Uma certa porcentagem da','população sofre de condições','como eplepsia e convulsões,','por isso sempre consulte','seu médico antes de jogar']

ERROR = ['Oops!','Alguma coisa deu errado... =(','Ignorar','Fechar']
 
ACHIEVEMENTS = [
['Zerado','Ganhar todos os troféus',0,''],
   
['YAS','Fique na 1 posição do placar',0,''],
['Meh','Fique na 2 posição do placar',0,''],
['Bruh','Fique na 3 posição do placar',0,''],
   
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

LOADING = ['Hello World!','Carregando cabeças dos personagens','Carregando corpo dos personagens','Carregando animações de batalha','Iniciando Mixer','Carregando músicas','Carregando mais músicas']

MESSAGES = [
['Não feche o jogo se','o ícone de carregamento','aparecer no canto da tela'],
['Esta é uma obra de ficção,','e quaisquer semelhanças com','acontecimentos reais podem','ter alterações artísticas.'],
['Uma certa porcentagem da','população sofre de condições','como eplepsia e convulsões,','por isso sempre consulte','seu médico antes de jogar'],
['Conecte-se na Steam ou','No Google Play para salvar','seus dados'],
['Algum youtuber está','jogando isso aqui?'],
['A vingança nunca é plena','mata a alma e a envenena'],
['A morte faz você morrer'],
['O jogo não travou, só','tá carregando, beleza?'],
['Você tem louça para lavar?'],
['Caso esteja carregando o jogo','pela primeira vez, ele irá','demorar para carregar','todos os recursos'],
['Feche outros programas','para o jogo rodar mais rápido'],
['Nunca deixe de explorar','entre as entrelinhas'],
['insira uma mensagem aqui'],
['Escute Pink Floyd','Escute Pink Floyd','Escute Pink Floyd']
]