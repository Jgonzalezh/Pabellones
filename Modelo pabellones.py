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
#Horario de funcionamiento 8:00-21:00
diccionario_T=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], #turno de 8 a 17
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0], #turno de 8:30 a 17:30
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0], #turno de 9 a 18:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0], #turno de 11:00 a 20:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0], #turno de 11:30 a 20:30
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #turno de 9:30 a 13:30
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], #14:00 a 18:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8:00-12:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8:30-12_30
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9:00-13:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9:00-15:00
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]] #12-18
            #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12-16
            #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #11-15
            #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #10-14
            #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]] #16-20
            
prueba=[]



for j in range (16,42):    
    for i in [16]:#]range(16,42):
        largo=[]
    
        for k in range(16):
            largo.append(0)
        if i<=j:
            largo.append(1)
        else:
            largo.append(0)
        for g in range(42,48):
            largo.append(0)
        


#Definir problema
modelo=LpProblem('Bloques de pabellones', LpMinimize) # Se define el modelo
#Variables
A=LpVariable.dicts('Bloques propuestos', [(e,p,h,d)for h in index for d in dias for p in P for e in E],lowBound=0, upBound=None,cat='Binary')

#Función objetivo        
modelo+=pulp.lpSum([A[(e,p,h,d)] for h in index for d in dias for p in P for e in E])
#Restricciones
for  p in P:
    for d in dias:
        for h in index:
            modelo+=pulp.lpSum([A[(e,p,h,d)] for e in E])<=1 #Solo se asigna a una especialidad al mismo tiempo el pabellón
for e in E:
    modelo+=pulp.lpSum([A[(e,p,h,d)] for h in index for d in dias for p in P])>=Q_horas[e]*2 # Se satisface la demanda semanal

for h in index[1:-1]:
    modelo

    
        




#modelo+=pulp.lpSum([F*D[c][mes][1][d][i]*H_C*1.16 for i in index])<=pulp.lpSum([C[(d,i,m)] for i in index for m in Q_controles])   