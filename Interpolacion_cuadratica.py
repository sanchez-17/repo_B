#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:27:15 2025

@author: bautistacenci
"""

from matplotlib import pyplot as plt
from matriz import Matriz
from poly import Poly
from scipy.interpolate import CubicSpline

"""
Ahora interpola bien: El error es que invertias el orden de los coeficientes pero Poly se maneja con el otro orden
Es decir, le saque el reversed(tramo) y listo.
Cambie el color para graficar. y modifique en Poly como maneja cada subplot.
inversa_method_robusto no se usa. Quizá se creo para evitar la division por cero. Pero en Matriz eso ya se tiene en cuenta. Se podria descartar este metodo.
"""

class cubica:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def interpolar(self):
        x = self.x
        y = self.y
        n = len(x) - 1  # número de tramos

        #M = myarray([0] * (4 * n)**2, 4 * n, 4 * n, True)
        M = Matriz([0] * (4 * n)**2, 4 * n, 4 * n, True)
        #Y = myarray([0] * (4 * n), 4 * n, 1, True)
        Y = Matriz([0] * (4 * n), 4 * n, 1, True)
        fila = 0

        # Paso 1: el spline pasa por cada punto inicial y final de cada tramo
        for i in range(n):
            xi, xi1 = x[i], x[i + 1]
            for j, t in enumerate([xi, xi1]):
                for k in range(4):
                    M.elems[M.get_pos(fila, 4 * i + k)] = t ** (3 - k)
                Y.elems[Y.get_pos(fila, 0)] = y[i] if j == 0 else y[i + 1]
                fila += 1

        # Paso 2: continuidad de primera derivada en nodos internos
        for i in range(1, n):
            t = x[i]
            for k in range(3):
                M.elems[M.get_pos(fila, 4*(i-1) + k)] = (3 - k) * t ** (2 - k)
                M.elems[M.get_pos(fila, 4*i + k)] = -(3 - k) * t ** (2 - k)
            Y.elems[Y.get_pos(fila, 0)] = 0
            fila += 1

        # Paso 3: continuidad de segunda derivada en nodos internos
        for i in range(1, n):
            t = x[i]
            for k in range(2):
                M.elems[M.get_pos(fila, 4*(i-1) + k)] = (3 - k)*(2 - k) * t ** (1 - k)
                M.elems[M.get_pos(fila, 4*i + k)] = -(3 - k)*(2 - k) * t ** (1 - k)
            Y.elems[Y.get_pos(fila, 0)] = 0
            fila += 1

        # Paso 4: spline natural (segunda derivada en extremos = 0)
        t0 = x[0]
        for k in range(2):
            M.elems[M.get_pos(fila, k)] = (3 - k)*(2 - k) * t0 ** (1 - k)
        Y.elems[Y.get_pos(fila, 0)] = 0
        fila += 1

        tn = x[-1]
        for k in range(2):
            M.elems[M.get_pos(fila, 4*(n-1) + k)] = (3 - k)*(2 - k) * tn ** (1 - k)
        Y.elems[Y.get_pos(fila, 0)] = 0

        return M, Y

    def graficar(self):
        import numpy as np
        M, Y = self.interpolar()
        solucion = M.resolver_sistema(Y.elems)#[1].elems
        tramos = [solucion[i:i+4] for i in range(0, len(solucion), 4)]
        polinomios = [Poly(3,list(tramo)) for tramo in tramos]
        #polinomios = []
        #for tramo in tramos:
        #    a = tramo[0]
        #    b = tramo[-1]  
        #    x = np.linspace(a, b, 300)
        #    polinomios.append(CubicSpline(x, tramo) )


        fig, ax = plt.subplots()
#        colors = plt.cm.viridis(np.linspace(0, 1, len(tramos)))
#        colors = plt.cm.cividis(np.linspace(0, 1, len(tramos)))
        colors = plt.cm.tab10(np.linspace(0, 1, len(tramos)))


        for i, (p, a, b) in enumerate(zip(polinomios, self.x[:-1], self.x[1:])):
            print(f"Tramo {i+1} entre x = {a} y x = {b}:")
            p.get_expression()
            #p.ply_plt(a, b)#, ax)
            p.ply_plt(a, b, ax=ax, color=colors[i])




        ax.scatter(self.x, self.y, color='red')
        plt.title("Spline Cúbica Natural")
        plt.grid(True)
        plt.show()

# Método robusto con pivoteo parcial para evitar división por cero
def inversametod_robusta(self, listadey):
    copia = self.copia()
    y = Matriz(listadey, copia.r, 1, True)
    identidad = copia.identidad()

    for columna in range(copia.c):
        # Pivoteo parcial: buscamos la mejor fila (mayor valor absoluto) en la columna actual
        mejor_fila = columna
        max_valor = abs(copia.get_elem(columna, columna))
        for i in range(columna + 1, copia.r):
            val = abs(copia.get_elem(i, columna))
            if val > max_valor:
                max_valor = val
                mejor_fila = i

        if max_valor == 0:
            raise ZeroDivisionError(f" Columna {columna} no tiene ningún valor no nulo debajo para pivotear.")

        if mejor_fila != columna:
            copia = copia.swap_rows(columna, mejor_fila)
            y = y.swap_rows(columna, mejor_fila)

        cofactor = copia.get_elem(columna, columna)
        for fila in range(copia.r):
            if fila == columna:
                identidad.elems[identidad.get_pos(fila, columna)] = 1 / cofactor
            else:
                identidad.elems[identidad.get_pos(fila, columna)] = -copia.get_elem(fila, columna) / cofactor

        copia = identidad.rprod(copia)
        y = identidad.rprod(y)
        identidad = copia.identidad()

    return copia, y


if __name__ == "__main__":
    # Activamos el nuevo método robusto
    #Matriz.inversametod = inversametod_robusta
    
    # Datos de prueba
    x = [1, 2, 3, 4, 5]
    y = [4, 3, 5, 9, 10]
    
    # Crear spline y graficar
    spl = cubica(x, y)
    spl.graficar()
    
#%%

# from spline_cubica import SplineCubica  # Ajustá el import según tu archivo


# Test 1: 3 puntos (caso mínimo para un solo tramo)
x = [0, 1, 2]
y = [1, 2, 0]

print("TEST 1: 3 puntos")
spline = cubica(x, y)
M, Y = spline.interpolar()

print("Matriz M:")
print(M)
print("Vector Y:")
print(Y)

spline.graficar()