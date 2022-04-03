import math 
  
emissor = [10, 10]
listener = [50, 10]

sndamp = 100 #a amplitude original do som (10^-2 W/m² = 100db)
r = 5 #raio da circunferência
area = 2 * math.pi * r #o círculo em volta do emissor =)
t = 1 #tempo

for i in range(40):
    emissor[0] += 1
    t += 1
    x = (sndamp * abs (emissor[0] - listener[0])) #FORÇA x DISTÂNCIA
    y =  (area * t) #ÁREA x TEMPO
    volume = x * y
    
    print ('ÁREA SONORA: ' + str(x))
    print ('DISTÂNCIA: ' + str(y))
    print ('VOLUME: ' + str(volume))
    print ('---------------')
