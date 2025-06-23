# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 00:47:22 2025

@author: Gaston
"""

from spline_cubica import cubica
from matriz import Matriz  # asegurate que está disponible

def test_interpolacion():
    # Datos ejemplo: plazos en años y tasas spot (en decimales)
    plazos = [0.5, 1, 2, 3]
    tasas_spot = [0.0025, 0.025, 0.03, 0.035]

    spl = cubica(plazos, tasas_spot)
    M, Y = spl.interpolar()
    solucion = M.resolver_sistema(Y.elems)#[1].elems
    tramos = [solucion[i:i+4] for i in range(0, len(solucion), 4)]

    def evaluar_spline(x):
        for i in range(len(plazos) - 1):
            if plazos[i] <= x <= plazos[i+1]:
                coefs = tramos[i]
                return sum([coefs[j] * x**(3-j) for j in range(4)])
        raise ValueError("x fuera del rango")

    x_test = 1.5
    y_test = evaluar_spline(x_test)
    print(f"Tasa spot interpolada en {x_test} años: {y_test:.6f}")

if __name__ == "__main__":
    test_interpolacion()
