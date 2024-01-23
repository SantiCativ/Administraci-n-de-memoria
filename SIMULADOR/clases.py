# Definir una clase
from typing import Any


class Trabajo:
    def __init__(self, id, nombre,tamanio,duracion,instanteArribo):
        self.id = id
        self.nombre = nombre
        self.tamanio = tamanio
        self.duracion = duracion
        self.instanteArribo = instanteArribo
    
    def __str__(self):
        return f"Trabajo {self.id}"
    
# Ahora puedes acceder a las instancias de la clase Trabajo en la lista "trabajos"

class Particion:
    # Variable de clase para llevar un registro del último ID generado
    ultimo_id = 0  
    tiempo_inicio=0

    def __init__(self,estado,tiempoInicio,tiempoFinalizacion,tamanio,ejeY,idTrabajo):
        self.estado = estado
        #tiempoInicio= tiempo carga a mp + tiempo de seleccion de particion +tiempo actual
        self.tiempoInicio=tiempoInicio
        #tiempo_finalizacion= tiempo de inicio+ duracion del trabajo+liberacion particion
        self.tiempoFinalizacion = tiempoFinalizacion
        self.tamanio=tamanio
        self.ejeY=ejeY
        self.idTrabajo=idTrabajo
        self.id = Particion.generar_id()  # Llama al método para generar un nuevo ID
       
        
    
    def __str__(self):
        return f"id: {self.id},estado: {self.estado}. tiempo Inicio:{self.tiempoInicio} Tiempo Finalizacion:{self.tiempoFinalizacion} tamaño:{self.tamanio} idTrabajo:{self.idTrabajo}"
    
    @classmethod
    def generar_id(cls):
        cls.ultimo_id += 1
        return cls.ultimo_id


class Simulador:
    def __init__(self):
        pass
       
    def unificar_particiones(self, particione):
        i = 0
        while i < len(particione) - 1:
            particion_actual = particione[i]
            particion_siguiente = particione[i + 1]
           
            if particion_actual.estado and particion_siguiente.estado:
                # Unifica las particione libres contiguas
                tmanio=particion_actual.tamanio + particion_siguiente.tamanio
                # Crea una nueva instancia de Particion para la partición resultante
                nueva_particion = Particion(True,-1 ,-1, tmanio,0,-1)
                particione[i] = nueva_particion
                # Elimina la partición siguiente
                del particione[i + 1]
               
                     
            else:
                i += 1
                
        
        return particione
    
    def generar_id(self):
        id
    
        
        
