# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 18:20:00 2025

@author: Gaston
"""
from matplotlib import pyplot as plt
from matriz import Matriz

class cubica:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def interpolar(self):
        x = self.x
        y = self.y
        n = len(x) - 1
        M = Matriz([0] * (4 * n)**2, 4 * n, 4 * n, True)
        Y = Matriz([0] * (4 * n), 4 * n, 1, True)
        fila = 0
        # Paso 1: paso por nodos en local s
        for i in range(n):
            h = x[i+1] - x[i]
            # s=0
            M.elems[M.get_pos(fila, 4*i + 3)] = 1
            Y.elems[Y.get_pos(fila, 0)] = y[i]
            fila += 1
            # s=h
            for k in range(4):
                M.elems[M.get_pos(fila, 4*i + k)] = h ** (3 - k)
            Y.elems[Y.get_pos(fila, 0)] = y[i+1]
            fila += 1
        # Paso 2: continuidad 1ª derivada
        for i in range(1, n):
            h_prev = x[i] - x[i-1]
            for k in range(3):
                M.elems[M.get_pos(fila, 4*(i-1) + k)] = (3 - k) * (h_prev ** (2 - k))
            M.elems[M.get_pos(fila, 4*i + 2)] = -1
            Y.elems[Y.get_pos(fila, 0)] = 0
            fila += 1
        # Paso 3: continuidad 2ª derivada
        for i in range(1, n):
            h_prev = x[i] - x[i-1]
            for k in range(2):
                M.elems[M.get_pos(fila, 4*(i-1) + k)] = (3 - k)*(2 - k) * (h_prev ** (1 - k))
            M.elems[M.get_pos(fila, 4*i + 1)] = -2
            Y.elems[Y.get_pos(fila, 0)] = 0
            fila += 1
        # Paso 4: Not-a-Knot
        M.elems[M.get_pos(fila, 0)] = 1
        M.elems[M.get_pos(fila, 4)] = -1
        Y.elems[Y.get_pos(fila, 0)] = 0
        fila += 1
        M.elems[M.get_pos(fila, 4*(n-2))] = 1
        M.elems[M.get_pos(fila, 4*(n-1))] = -1
        Y.elems[Y.get_pos(fila, 0)] = 0
        return M, Y

    def calcular_coeficientes(self):
        M, Y = self.interpolar()
        sol = M.resolver_sistema(Y.elems)
        self.polinomios = [sol[i:i+4] for i in range(0, len(sol), 4)]

    def evaluar(self, x_eval):
        if x_eval <= self.x[0]: idx = 0
        elif x_eval >= self.x[-1]: idx = len(self.x) - 2
        else:
            idx = next(i for i in range(len(self.x)-1)
                       if self.x[i] <= x_eval <= self.x[i+1])
        a, b, c, d = self.polinomios[idx]
        s = x_eval - self.x[idx]
        return a*s**3 + b*s**2 + c*s + d

    def graficar(self, x_start=None):
        import numpy as np
        import matplotlib.pyplot as plt
        if not hasattr(self, 'polinomios'):
            self.calcular_coeficientes()
        fig, ax = plt.subplots()
        for coef, xi, xj in zip(self.polinomios, self.x[:-1], self.x[1:]):
            if x_start is not None and xj < x_start:
                continue
            a, b, c, d = coef
            h = xj - xi
            # determinar rango local s
            if x_start is None or x_start <= xi:
                s0 = 0
            else:
                s0 = x_start - xi
                h = xj - xi  # h remains full length for plotting
            s_vals = np.linspace(s0, h, 200)
            y_vals = a*s_vals**3 + b*s_vals**2 + c*s_vals + d
            ax.plot(xi + s_vals, y_vals)
        ax.scatter(self.x, self.y, color='red')
        plt.title("Spline Cúbica")
        plt.grid(True)
        plt.show()
