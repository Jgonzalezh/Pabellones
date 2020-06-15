# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:23:09 2020

@author: jgonzalezh
"""
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from pulp import *
import matplotlib.colors as mcolors
import matplotlib.transforms as mtransforms
import matplotlib.patches as mpatches

def diccionario_bloques(bloque_ini,bloque_fin):
    diccionario=[]
    h=bloque_ini
    g=bloque_fin
    for k in range(h,g):
        for j in range (k,g):    
            largo=[]
            #for i in [16]:#]range(16,42):
            for k in range(k):
                largo.append(0)
            for i in range(k,g):
                if i<=j:
                    largo.append(1)
                else:
                    largo.append(0)
            for g in range(g,48):
                largo.append(0)
            diccionario.append(largo)
    return diccionario
        

#should make dictionary for variables
E_str=['EESS','COLUMNA','CPQ']
E=[0,1,2]
P=[0,1,2,3,4,5,6,7,8,9,10]#,11]
horas=['00:00:00','00:30:00','01:00:00','01:30:00','02:00:00','02:30:00','03:00:00','03:30:00',
    '04:00:00','04:30:00','05:00:00','05:30:00','06:00:00','06:30:00','07:00:00','07:30:00',
    '08:00:00','08:30:00','09:00:00','09:30:00','10:00:00','10:30:00','11:00:00','11:30:00',
    '12:00:00','12:30:00','13:00:00','13:30:00','14:00:00','14:30:00','15:00:00','15:30:00',
    '16:00:00','16:30:00','17:00:00','17:30:00','18:00:00','18:30:00','19:00:00','19:30:00',
    '20:00:00','20:30:00','21:00:00','21:30:00','22:00:00','22:30:00','23:00:00','23:30:00']
dias=[0,1,2,3,4] # se hace el ppl de lunes a viernes
index = np.arange(48) #bloques del día
dias_str=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'] 

Tipo=[1,2,3,4,5,6,7]
Q_horas=[77.7,85,90] #ordenadas por especialidad mínimo (vemos a que apuntamos acá)
Q_portramo=[[14,14,7,21,0,21,7],[15,25,25,10,5,0,5,0],[25,15,25,10,5,0,0,10]]
#Horario de funcionamiento 8:00-21:->16,42
turnos=diccionario_bloques(16,42)
T=range(len(turnos))



#Definir problema
modelo=LpProblem('Bloques de pabellones', LpMinimize) # Se define el modelo
#Variables
A=LpVariable.dicts('Bloques propuestos', [(e,p,t,d)for t in T for d in dias for p in P for e in E],lowBound=0, upBound=None,cat='Binary')

#Función objetivo        
modelo+=pulp.lpSum([A[(e,p,t,d)] for t in T for d in dias for p in P for e in E]) #minimizar N° Bloques a la semana
#Restricciones

# Solo se asigna a una especialidad al mismo tiempo el pabellón
for  p in P:
    for d in dias:
        for h in index:
            modelo+=pulp.lpSum([turnos[t][h]*A[(e,p,t,d)] for e in E for t in T])<=1 
# Se satisface la demanda semanal
for e in E:
    modelo+=pulp.lpSum([turnos[t][h]*A[(e,p,t,d)] for t in T for h in index for d in dias for p in P])>=Q_horas[e]*2 
# Bloque es continuo abordada por diccionario
# No hay más de tres bloques por día de cada especialidad
for d in dias:
    for e in E:
        modelo+=pulp.lpSum([A[(e,p,t,d)] for t in T for p in P])<=3    
# No hay más de tres bloques en simultaneo (abordada por previa, si son numeros distintos se debe hacer)
"""
for d in dias:
    for e in E:
        for h in index:
            modelo+=pulp.lpSum(A[(e,p,t,d)] for t in T for d in dias for p in P])<=3   
"""
# No se asignan más pabellones de los disponibles (ya restringidos por N de pabellones)
# A futuro poner largo máximo de un bloque(?) Puede ser en el diccionario de turnos tb para simplificar problema
"""
for  p in P:
    for d in dias:
        for e in E:
            modelo+=pulp.lpSum([turnos[t][h]*A[(e,p,t,d)] for t in T])<=24
"""
# Cantidad de bloques mínimos a la semana (ejemplo tres, pero puede ser un diccionario para cada especialidad)
for e in E:
    modelo+=pulp.lpSum([A[(e,p,t,d)] for t in T for p in P for d in dias])>=3  

# Dividiendo el instrumental se puede hacer todas las cirugías a la semana (cajas) --->FUTURA, hay que modelar los datos

modelo.solve(pulp.PULP_CBC_CMD(maxSeconds=600, msg=1, fracGap=0))#pulp.GLPK()
print(LpStatus[modelo.status])



#for h in index[1:-1]:
#    modelo

    
        




#modelo+=pulp.lpSum([F*D[c][mes][1][d][i]*H_C*1.16 for i in index])<=pulp.lpSum([C[(d,i,m)] for i in index for m in Q_controles])   