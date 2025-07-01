#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 16:19:58 2025

@author: bautistacenci
"""
import pandas as pd
from spline_cubica import cubica
import numpy as np
from curva_bootstrap import bootstrapping

#%%
pm = np.arange(1.5, 30, 0.5)
x = [0.5, 1, 2, 3, 5, 7, 10, 20, 30]
TASAS = [0.0431, 0.0411, 0.0395, 0.0391, 0.0391, 0.0402, 0.0421, 0.0444, 0.0496]

curva = cubica(x, TASAS)
curva.calcular_coeficientes()
curva.graficar()

#%%
lista_tires = [TASAS[0],TASAS[1],]
for x in pm:
    a = curva.evaluar(x)
    lista_tires.append(a)
print(lista_tires)

lista_spot = [TASAS[0],TASAS[1]]
lista_de_flujos= []
# for y, tir in enumerate(lista_tires,start=1):
#     flujo = tir/(1+spot)**y
#     lista de flujos.append()
        
#%%

# Creo la lista de tires, y por ahora los spots valen cero.
df = pd.DataFrame({"tires":lista_tires, "spots":np.zeros(len(lista_tires))})
# Calculo todos los spots 
spots = bootstrapping(df["tires"])
df["spots"] = spots.copy()


#%% Graficamos los spots

x_spots = np.arange(1, len(spots) + 1)
curva_spots = cubica(x_spots, spots)
curva_spots.calcular_coeficientes()
curva_spots.graficar()

#%%
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
cs = CubicSpline(x_spots, spots)

x_fino = np.linspace(x_spots[0], x_spots[-1], 200)
y_fino = cs(x_fino)

# Graficar
plt.plot(x_spots, spots, 'o', label='Puntos originales')
plt.plot(x_fino, y_fino, '-', label='Interpolación cúbica')
plt.legend()
plt.grid(True)
plt.title("Interpolación cúbica con CubicSpline")
plt.show()

#%% 

df['flujos'] = []

df["valor_presente"] = df["flujos"] / (1 + df["spots"])**(df.index + 1)
