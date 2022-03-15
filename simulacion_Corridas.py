#Simulacion de Corrida de Programas

#Nombre: Andrea Ximena Ramirez Recinos 
#Carne: 21874
#Algoritmos y Estructuras de Datos Seccion 20, 2022

#Pasos:
#Llega al sistema operativo
#Solicita memoria, y si hay pasa a que lo atienda el CPU
#El CPU lo atiende y realiza 3 intrucciones del proceso
#Si ya no hay mas intrucciones culmina, si hay genera un numero al azar entre 1 y 2
#Si es 1, pasa nuevamente a la cola de waiting
#Si es 2, pasa automaticamente a que lo antienda el CPU

from ast import Global
import simpy
import random 
import statistics

print(f'Simulacion de Corrida de Programas')
print(f'Porfavor ingrese la cantidad de procesos a realizar')

amountOfProcesses = int(input())
str1 = ""

process_times = []
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
RAM = simpy.Container(env, init=100, capacity=100)
IO = simpy.Resource(env)
TotalTime = 0
random.seed(10)


def Proceso(env, proceso):
    TotalTimeProcess = 0
    global TotalTime
    global CPU
    global RAM
    global IO
    Arrival_Time = int(random.expovariate(1.0 / 1))
    MemoryNeeded = random.randint(1, 10)
    InstructionsNeeded = random.randint(1, 10)

    yield env.timeout(Arrival_Time)
    yield RAM.get(MemoryNeeded)
    

    print(f'Proceso {proceso} entrando en cola en {env.now}')
    
    irruption = 2
    while InstructionsNeeded > 0 and irruption == 2:  
        print('Proceso %s en cola READY en %d cantidad instrucciones pendientes %d' % (proceso, env.now, InstructionsNeeded))

        with CPU.request() as req:
            yield req
            InstructionsNeeded = InstructionsNeeded - 6
            yield env.timeout(1)
            print(f'Proceso {proceso} atendido en {env.now}')
            

        if InstructionsNeeded > 0:
            irruption = random.randint(1, 2)
            if irruption == 1:
                yield env.timeout(1)    
                irruption = 2
    
    yield RAM.put(MemoryNeeded)
        
    print('Proceso %s termino en tiempo %d' % (proceso, env.now))
    TotalTime += (env.now - Arrival_Time)
    process_times.append(env.now - Arrival_Time) #Recoleccion de Data

for i in range(amountOfProcesses): 
    env.process(Proceso(env, i))

#Corriendo el Entorno 
env.run()
Mean = TotalTime/amountOfProcesses
SD = statistics.stdev(process_times)
print(f"\nDesviacion Estandar de Muestra: {SD}")
print(f"Tiempo {TotalTime}")
print('Tiempo promedio %f' % Mean)