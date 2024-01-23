from clases import *
import time
import matplotlib.pyplot as plt
from datetime import datetime
from collections import namedtuple


def firsFit(listaTrabajos,tamanioMp,tiempoCargaMp,tiempoSelec,tiempoLiberacion):
    print("Politica Firs Fit seleccionada")
    simulador= Simulador()
    
    #particiones, esta va ser la lista que va a devolver la funcion, con todas las particiones que hubo en el recorrido.
    particiones=[]
    #index para ir recorriendo la lista de trabajos en orden
    index=0

    #tiempo delta T actual
    tiempoActual=0

    #particion 0, es la primera particion, la cual es el tamaño de la memoria.
    # el estado de las particiones lo pienso en sentido: True= libre - False= ocupada
    particionActual=Particion(True,-1,-1,tamanioMp,0,-1)

    #creo lista de particiones dinamicas
    listaParticiones=[particionActual]

    #framentacion externa
    Fe=0
    
    while len(listaTrabajos) > 0:
        print("Trabajo: " + listaTrabajos[index].nombre+" esperando particion")
        print("tiempo actual: "+ str(tiempoActual))
        trabajoActual=listaTrabajos[index]
        #este for es para recorrer la lista de particiones y buscar si su tiempo de finalizacion es igual al tiempo delta t actual
        #para luego poner las particiones libres en true
        for particion in listaParticiones:
            if (particion.tiempoFinalizacion==tiempoActual):
                particion.estado=True

        #una vez que chekeamos si las particiones finalizaron, procedemos a evaluar si es necesario unificar particiones.
        listaParticiones=simulador.unificar_particiones(listaParticiones)
        
        
        for particion in listaParticiones:
            print("particiones disponibles: "+ "["+str(particion)+"]")

        #en este bucle voy a iterar hasta que encuentre la primera particion que libre y que me abarque
        #el espacio necesario, una vez encontrada se seteara la variable "carga" a false para
        #detener el bucle y que deje de buscar particion.
        i=0
        carga=True
        
        while (carga and i < len(listaParticiones)):
            
            if((listaParticiones[i].estado== True) and (listaParticiones[i].tamanio >= trabajoActual.tamanio)):
                #encontramos particion , seteamos variable "carga"
                carga=False
                #sacamos la particion de la lista por una cuestion de comodidad
                particion=listaParticiones[i]
               
                #-----------------------------------
                #SITUACION 1 DE ENCONTRAR PARTICION
                if(particion.tamanio==trabajoActual.tamanio):
                     #inicializamos el eje y de la particion
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        if p is particion:
                            break
                        ejeY += p.tamanio
                            
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    print(particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion),particionX)
                    #eliminamos la particion
                    listaParticiones.pop(listaParticiones.index(particion))
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
                #SITUACION 2 DE ENCONTRAR PARTICION    
                if (particion.tamanio>trabajoActual.tamanio):
                    #inicializamos el eje y de la particion
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        if p is particion:
                            break
                        ejeY += p.tamanio
                   
                    print("tamaño particion es: "+str(particion.tamanio))
                    #instancia de la particion nueva que tiene el tamaño del trabajo
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                     #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion)+1,particionX)
                           
                    #instancia de la particion sobrante libre
                    particionX=Particion(True,-1,-1,particion.tamanio-trabajoActual.tamanio,0,-1)
                    listaParticiones.insert(listaParticiones.index(particion)+2,particionX)
                    
                    #eliminamos la particion
                    listaParticiones.pop(i)
                    
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
            #sigue otro ciclo
            #incrementamos el indice para preguntar por la siguiente particion
            i+=1
            
        #recorremos todas las particiones y cuando se encuentra una o mas que esten libres sumarle su tamanio en la
        #variable Fe para calcular la fragmentracion externa
        for particion in listaParticiones:
            if particion.estado==True and len(listaTrabajos)!=0:
                Fe+=particion.tamanio
                print("Fragmentacion externa"+str(Fe))
                
        
        for particion in listaParticiones:
            print("particiones disponibles despues de actualizar: "+ "["+str(particion)+"]")
            
        
        tiempoActual+=1
        print("Longitud de la lista de trabajos:", len(listaTrabajos))
        print("------------------------------")
        # Introduce una pausa de 1 segundo
        time.sleep(1)
        
    print("indice de fragmentacion externa es:"+ str(Fe))
    
    # Obtener el objeto con el mayor tiempoFinalizacion para enviarlo por la funcion y encontrar el limite del eje de las abscisas
    objeto_mayor_tiempoFinalizacion = max(listaParticiones, key=lambda obj: obj.tiempoFinalizacion)
    
    #aca se va a mandar por la funcion la longitud x propia dicha, la lista de particiones a las que se le asigno a los
    #trabajos, y por ultimo el indice de fragmentacion externa.
    resultado=namedtuple("resultado",["LongitudX","ListaParticiones","fragmentacion"])
    return resultado(LongitudX=objeto_mayor_tiempoFinalizacion,ListaParticiones=particiones,fragmentacion=Fe)
    
    
def bestFit(listaTrabajos,tamanioMp,tiempoCargaMp,tiempoSelec,tiempoLiberacion):
    print("Opción 2 seleccionada")
    simulador= Simulador()
    #particiones, esta va ser la lista que va a devolver la funcion, con todas las particiones que hubo en el recorrido.
    particiones=[]
    #index para ir recorriendo la lista de trabajos en orden
    index=0

    #tiempo delta T actual
    tiempoActual=0

    #particion 0, es la primera particion, la cual es el tamaño de la memoria.
    # el estado de las particiones lo pienso en sentido: True= libre - False= ocupada
    particionActual=Particion(True,-1,-1,tamanioMp,0,-1)

    #creo lista de particiones dinamicas
    listaParticiones=[particionActual]

    #framentacion externa
    Fe=0

    while len(listaTrabajos) > 0:
        print("Trabajo: " + listaTrabajos[index].nombre+" esperando particion")
        print("tiempo actual: "+ str(tiempoActual))
        
        trabajoActual=listaTrabajos[index]
        #este for es para recorrer la lista de particiones y buscar si su tiempo de finalizacion es igual al tiempo delta t actual
        #para luego poner las particiones libres en true
        for particion in listaParticiones:
            if (particion.tiempoFinalizacion==tiempoActual):
                particion.estado=True

        listaParticiones=simulador.unificar_particiones(listaParticiones)

        for particion in listaParticiones:
            print("particiones disponibles: "+ "["+str(particion)+"]")
            
        
        #hago una replica de la lista de particiones 
        listaParticiones2=[]
        
        #recorro la lista de particiones original y filtro las que estan libres en la nueva lista de particiones
        for particion in listaParticiones:
            if particion.estado==True:
                listaParticiones2.append(particion)
        
        # Ordeno la lista por la propiedad "tamaño" utilizando una función de clave
        listaParticiones2 = sorted(listaParticiones2, key=lambda x: x.tamanio)
        

        #en este bucle voy a iterar hasta que encuentre la primera particion que libre y que me abarque
        #el espacio necesario, una vez encontrada se seteara la variable "carga" a false para
        #detener el bucle y que deje de buscar particion.
        i=0
        carga=True
        
        
        while (carga and i < len(listaParticiones2)):
            
            if(listaParticiones2[i].tamanio >= trabajoActual.tamanio):
                #encontramos particion , seteamos variable "carga"
                carga=False
                #sacamos la particion de la lista por una cuestion de comodidad, en este caso sacamos la particion de la lista original
                particion = next((x for x in listaParticiones if x.id == listaParticiones2[i].id), None)
                
                if(particion.tamanio==trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
            
                        if p is particion:
                            break
                        ejeY += p.tamanio
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    print(particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion),particionX)
                    #eliminamos la particion
                    listaParticiones.pop(listaParticiones.index(particion))
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
                    
                
                if (particion.tamanio>trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        if p is particion:
                            break
                        ejeY += p.tamanio
                    print("tamaño particion es: "+str(particion.tamanio))
                    #instancia de la particion nueva que tiene el tamaño del trabajo
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    listaParticiones.insert(listaParticiones.index(particion)+1,particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
        
                    #instancia de la particion sobrante libre
                    particionX=Particion(True,-1,-1,particion.tamanio-trabajoActual.tamanio,0,-1)
                    listaParticiones.insert(listaParticiones.index(particion)+2,particionX)
                    
                    
                    #eliminamos la particion #esta aca el problema...
                    listaParticiones.pop(listaParticiones.index(particion))
                    
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
            
            #sigue otro ciclo
            #incrementamos el indice para preguntar por la siguiente particion
            i+=1
           
        #recorremos todas las particiones y cuando se encuentra una o mas que esten libres sumarle su tamanio en la
        #variable Fe para calcular la fragmentracion externa
        for particion in listaParticiones:
            if particion.estado==True and len(listaTrabajos)!=0:
                Fe+=particion.tamanio
                print("Fragmentacion externa"+str(Fe))
                            
        # Introduce una pausa de 1 segundo
        tiempoActual+=1
        print("------------------------------")
        time.sleep(1)
    



    print("indice de fragmentacion externa es:"+ str(Fe))
     # Obtener el objeto con el mayor tiempoFinalizacion
    objeto_mayor_tiempoFinalizacion = max(listaParticiones, key=lambda obj: obj.tiempoFinalizacion)
    
    resultado=namedtuple("resultado",["LongitudX","ListaParticiones","fragmentacion"])
    return resultado(LongitudX=objeto_mayor_tiempoFinalizacion,ListaParticiones=particiones,fragmentacion=Fe)



def nextFit(listaTrabajos,tamanioMp,tiempoCargaMp,tiempoSelec,tiempoLiberacion):
    print("Politica Next Fit seleccionada")
    simulador= Simulador()
    
    #particiones, esta va ser la lista que va a devolver la funcion, con todas las particiones que hubo en el recorrido.
    particiones=[]
    #index para ir recorriendo la lista de trabajos en orden
    index=0

    #tiempo delta T actual
    tiempoActual=0

    #particion 0, es la primera particion, la cual es el tamaño de la memoria.
    # el estado de las particiones lo pienso en sentido: True= libre - False= ocupada
    particionActual=Particion(True,-1,-1,tamanioMp,0,-1)

    #creo lista de particiones dinamicas
    listaParticiones=[particionActual]

    #framentacion externa
    Fe=0
    
    i=0
    while len(listaTrabajos) > 0:
        print("Trabajo: " + listaTrabajos[index].nombre+" esperando particion")
        print("tiempo actual: "+ str(tiempoActual))
        
        for particion in listaParticiones:
            print("particiones: "+ "["+str(particion)+"]")
        
        trabajoActual=listaTrabajos[index]
        #este for es para recorrer la lista de particiones y buscar si su tiempo de finalizacion es igual al tiempo delta t actual
        #para luego poner las particiones libres en true
        for particion in listaParticiones:
            if (particion.tiempoFinalizacion==tiempoActual):
                particion.estado=True

        listaParticiones=simulador.unificar_particiones(listaParticiones)

        carga=True
        
        
        while (carga and i < len(listaParticiones)):
            
            if((listaParticiones[i].estado== True) and (listaParticiones[i].tamanio >= trabajoActual.tamanio)):
                #encontramos particion , seteamos variable "carga"
                carga=False
                #sacamos la particion de la lista por una cuestion de comodidad
                particion=listaParticiones[i]
                
               
                        
                if(particion.tamanio==trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        
                        if p is particion:
                                break
                        ejeY += p.tamanio
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    print(particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion),particionX)
                    #eliminamos la particion
                    listaParticiones.pop(listaParticiones.index(particion))
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
                    
                
                if (particion.tamanio>trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        
                        if p is particion:
                                break
                        ejeY += p.tamanio
                    print("tamaño particion es: "+str(particion.tamanio))
                    #instancia de la particion nueva que tiene el tamaño del trabajo
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    listaParticiones.insert(listaParticiones.index(particion)+1,particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
        
                    #instancia de la particion sobrante libre
                    particionX=Particion(True,-1,-1,particion.tamanio-trabajoActual.tamanio,0,-1)
                    listaParticiones.insert(listaParticiones.index(particion)+2,particionX)
                    
                    #eliminamos la particion
                    listaParticiones.pop(i)
                    
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
            
            #sigue otro ciclo
            #incrementamos el indice para preguntar por la siguiente particion
            i+=1
            
        #recorremos todas las particiones y cuando se encuentra una o mas que esten libres sumarle su tamanio en la
        #variable Fe para calcular la fragmentracion externa
        for particion in listaParticiones:
            if particion.estado==True and len(listaTrabajos)!=0:
                Fe+=particion.tamanio
                print(particion.tamanio)
            
        print("Fragmentacion externa"+str(Fe))      
        # Introduce una pausa de 1 segundo
        tiempoActual+=1
        #si i llego al limite de la lista de particiones, tiene que comenzar de 0 de nuevo
        if (i==len(listaParticiones)):
                i=0
            
        print("Longitud de la lista de trabajos:", len(listaTrabajos))
        print("------------------------------")
        time.sleep(1)
        

    print("indice de fragmentacion externa es:"+ str(Fe))
    # Obtener el objeto con el mayor tiempoFinalizacion
    objeto_mayor_tiempoFinalizacion = max(listaParticiones, key=lambda obj: obj.tiempoFinalizacion)
    
    resultado=namedtuple("resultado",["LongitudX","ListaParticiones","fragmentacion"])
    return resultado(LongitudX=objeto_mayor_tiempoFinalizacion,ListaParticiones=particiones,fragmentacion=Fe)
    

 
def wordFit(listaTrabajos,tamanioMp,tiempoCargaMp,tiempoSelec,tiempoLiberacion):
    print("Politica Word Fit seleccionada")
    simulador= Simulador()
    
    #particiones, esta va ser la lista que va a devolver la funcion, con todas las particiones que hubo en el recorrido.
    particiones=[]
    #index para ir recorriendo la lista de trabajos en orden
    index=0

    #tiempo delta T actual
    tiempoActual=0

    #particion 0, es la primera particion, la cual es el tamaño de la memoria.
    # el estado de las particiones lo pienso en sentido: True= libre - False= ocupada
    particionActual=Particion(True,-1,-1,tamanioMp,0,-1)

    #creo lista de particiones dinamicas
    listaParticiones=[particionActual]

    #framentacion externa
    Fe=0
    
    while len(listaTrabajos) > 0:
        print("Trabajo: " + listaTrabajos[index].nombre+" esperando particion")
        print("tiempo actual: "+ str(tiempoActual))
        
        trabajoActual=listaTrabajos[index]
        #este for es para recorrer la lista de particiones y buscar si su tiempo de finalizacion es igual al tiempo delta t actual
        #para luego poner las particiones libres en true
        for particion in listaParticiones:
            if (particion.tiempoFinalizacion==tiempoActual):
                particion.estado=True
    
        listaParticiones=simulador.unificar_particiones(listaParticiones)
        
        for particion in listaParticiones:
            print("particiones: "+ "["+str(particion)+"]")
        
        

        #hago una replica de la lista de particiones 
        listaParticiones2=[]
        
        #recorro la lista de particiones original y filtro las que estan libres en la nueva lista de particiones
        for particion in listaParticiones:
            if particion.estado==True:
                listaParticiones2.append(particion)
        
    # Ordeno la lista por la propiedad "tamaño" de mayor a menor utilizando una función de clave
        listaParticiones2 = sorted(listaParticiones2, key=lambda x: x.tamanio, reverse=True)
        
        for p in listaParticiones2:
            print("particiones libres ordenadas de mayor a menor: "+ "["+str(p)+"]")

        #en este bucle voy a iterar hasta que encuentre la primera particion que libre y que me abarque
        #el espacio necesario, una vez encontrada se seteara la variable "carga" a false para
        #detener el bucle y que deje de buscar particion.
        i=0
        carga=True
        
        
        while (carga and i < len(listaParticiones2)):
             
            if(listaParticiones2[i].tamanio >= trabajoActual.tamanio):
                #encontramos particion , seteamos variable "carga"
                carga=False
                #sacamos la particion de la lista por una cuestion de comodidad, en este caso sacamos la particion de la lista original
                particion = next((x for x in listaParticiones if x.id == listaParticiones2[i].id), None)

                print(f"se eligio particion: {particion.id}")  
                    
                # Verificar si se encontró una coincidencia
                if particion:
                    print(particion.id)
                else:
                    print("No se encontró ninguna partición con el ID especificado.")
                
                if(particion.tamanio==trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        
                        if p is particion:
                                break
                        ejeY += p.tamanio
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
                    print(particionX)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion),particionX)
                    #eliminamos la particion
                    listaParticiones.pop(listaParticiones.index(particion))
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
                    
                
                if (particion.tamanio>trabajoActual.tamanio):
                    #se calcula el ejeY
                    ejeY=0
                    for p in listaParticiones:
                        if p.estado and p is listaParticiones[-1]:
                            break
                        
                        
                        if p is particion:
                                break
                        ejeY += p.tamanio
                    
                    tiempoInicio=tiempoCargaMp+tiempoSelec+tiempoActual
                    particionX=Particion(False,tiempoInicio,tiempoInicio+trabajoActual.duracion+tiempoLiberacion,trabajoActual.tamanio,ejeY,trabajoActual.id)
                    #agregamos a la lista de particiones que luego va a ser enviada por la funcion
                    particiones.append(particionX)
                    listaParticiones.insert(listaParticiones.index(particion)+1,particionX)
                    
                    #instancia de la particion sobrante libre
                    particionX=Particion(True,-1,-1,particion.tamanio-trabajoActual.tamanio,0,-1)
                    listaParticiones.insert(listaParticiones.index(particion)+2,particionX)
                    
                    
                    #eliminamos la particion #esta aca el problema...
                    listaParticiones.pop(listaParticiones.index(particion))
                    
                    print ("el trabajo "+str(trabajoActual.nombre)+" encontro particion")
    
                    #eliminamos el trabajo
                    del listaTrabajos[index]
                    
            
            #sigue otro ciclo
            #incrementamos el indice para preguntar por la siguiente particion
            i+=1
                
        #recorremos todas las particiones y cuando se encuentra una o mas que esten libres sumarle su tamanio en la
        #variable Fe para calcular la fragmentracion externa
        for particion in listaParticiones:
            if particion.estado==True and len(listaTrabajos)!=0:
                Fe+=particion.tamanio
                print(particion.tamanio)
                
        print("Fragmentacion externa"+str(Fe))    
        # Introduce una pausa de 1 segundo
        tiempoActual+=1
        print("Longitud de la lista de trabajos:", len(listaTrabajos))
        print("------------------------------")
        
        time.sleep(1)
        
    print("indice de fragmentacion externa es:"+ str(Fe))
     # Obtener el objeto con el mayor tiempoFinalizacion
    objeto_mayor_tiempoFinalizacion = max(listaParticiones, key=lambda obj: obj.tiempoFinalizacion)
    
    resultado=namedtuple("resultado",["LongitudX","ListaParticiones","fragmentacion"])
    return resultado(LongitudX=objeto_mayor_tiempoFinalizacion,ListaParticiones=particiones,fragmentacion=Fe)

def opcion_por_defecto():
    print("Opción no válida")


#codigo del archivo

listaTrabajos = []

nombre_archivo = input("Ingrese el nombre del archivo: ")

with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()

for linea in lineas:
    valores = linea.strip().split(",")
    trabajo = Trabajo(int(valores[0]), valores[1], int(valores[2]), int(valores[3]), int(valores[4]))
    listaTrabajos.append(trabajo)

#datos de entrada
tamanioMp=int(input("Ingrese el tamaño de la memoria principal: "))
tiempoCargaMp=int(input("Ingrese el tiempo de carga del trabajo a la memoria principal: "))
tiempoSelec=int(input("Ingrese el tiempo de seleccion de la particion: "))
tiempoLiberacion=int(input("Ingrese el tiempo de liberacion de la particion: "))

# el diccionario con los casos
switch = {
    1: firsFit,
    2: bestFit,
    3: nextFit,
    4: wordFit
}

print("1-FirsFit")
print("2-BestFit")
print("3-NextFit")
print("4-WordFit")


# Obtener la entrada del usuario
opcion = int(input("Ingrese el numero de la Politica deseada: "))

# Obtener la función correspondiente al caso seleccionado
funcion = switch.get(opcion, opcion_por_defecto)

resultado=funcion(listaTrabajos,tamanioMp,tiempoCargaMp,tiempoSelec,tiempoLiberacion)


for p in resultado.ListaParticiones:
    print(f"tiempo retorno del trabajo {p.idTrabajo}: {p.tiempoFinalizacion}")

print (f"Tiempo de retorno de la tanda de trabajo: {resultado.LongitudX.tiempoFinalizacion}")
total=sum(p.tiempoFinalizacion for p in resultado.ListaParticiones)
print(f"Tiempo medio de retorno: {total/len(resultado.ListaParticiones)}")



#ACA SE CONFIGURA EL DIAGRAMA.
# Crear la figura y los ejes
fig, ax = plt.subplots()

# Configurar el rango del eje y
ax.set_ylim(0, tamanioMp+10)

# Configurar el rango del eje y
ax.set_yticks(range(0, tamanioMp+10, 10))  # Rango de 0 a 200 avanzando de 10 en 10

# Configurar las etiquetas del eje y
labels = [f"{num}k" for num in range(0, tamanioMp+10, 10)]
ax.set_yticklabels(labels)

# Configurar el rango del eje x
ax.set_xlim(0, resultado.LongitudX.tiempoFinalizacion+2)

# Configurar el rango del eje x
ax.set_xticks(range(0, resultado.LongitudX.tiempoFinalizacion+2, 1))  # Rango de 0 a n avanzando de 2 en 2

# Configurar las etiquetas del eje x
ax.set_xticklabels(range(0, resultado.LongitudX.tiempoFinalizacion+2, 1))


# Crear los segmentos del diagrama de Gantt
for p in (resultado.ListaParticiones):
    bar_height = p.tamanio
    ejey= p.ejeY+ (bar_height / 2)  # Calcular la posición del segmento en el eje Y
    ax.barh(ejey, width=p.tiempoFinalizacion - p.tiempoInicio, left=p.tiempoInicio, height=bar_height)
     # Agregar etiqueta/nombre a cada segmento
    ax.text((p.tiempoInicio+p.tiempoFinalizacion)/2, ejey, f"T{p.idTrabajo}-{p.tamanio}K", ha='center', va='center')


# Agregar texto fuera del gráfico
plt.text(5, tamanioMp+20, f"FRAGMENTACION EXTERNA:{resultado.fragmentacion}", ha='center', va='center')
plt.text(5, tamanioMp+15, f"POLITICA:{switch[opcion].__name__}", ha='center', va='center')
plt.text(10, tamanioMp+30, f"Autor: Santiago Cativa - github: https://github.com/SantiCativ", ha='center', va='center')
# Mostrar el gráfico
plt.show()




