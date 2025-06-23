# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 00:40:57 2025

@author: Gaston
"""

from bonos import Bono
from fechas import Fechas
from spline_cubica import cubica

def crear_bono(maturity_years, annual_coupon, price):
    specs = {
        'ticker': f'BONO_{maturity_years}Y',
        'empresa': 'Tesoro',
        'descripcion': f'Bono {maturity_years} años, cupón {annual_coupon*100}%',
        'pais': 'PAIS',
        'moneda': 'USD',
        'fecha_emision': (1, 1, 2025),
        'primer_cupon': (1, 7, 2025),
        'vencimiento': (1, 1, 2025 + maturity_years),
        'madurez': (1, 1, 2025 + maturity_years),
        'tasas_cupones': [annual_coupon / 2],
        'fechas_tasas_cupones': [((1, 1, 2025), (1, 1, 2025 + maturity_years))],
        'frecuencia_cupon': 2,
        'cupon_irregular': False,
        'tipo_cupon_irregular': '',
        'tipo_cupon': 'bullet',
        'tasa_cap_cupones': [],
        'fecha_cap_cupones': [],
        'amortizaciones': 0,
        'porcentajes_amort': [],
        'fechas_amort': [],
        'tipo': 'bullet',
        'valor_nominal': 100,
        'conteo_dias': 'actual/actual',
        'convencion': '30/360',
        'liquidacion': 2
    }
    bono = Bono(specs)
    tir = bono.Tir(precio=price)
    return bono, tir

def calcular_spots(bonos_data, overnight_rate):
    # Crear bonos y calcular TIR
    bonos = []
    for data in bonos_data:
        _, tir = crear_bono(data['maturity'], data['annual_coupon'], data['price'])
        bonos.append({'maturity': data['maturity'], 'tir': tir})

    # Calcular tasa semestral overnight
    overnight_rate_sem = (1 + overnight_rate) ** (182/365) - 1

    # Armar listas para interpolar
    x = [0] + [bono['maturity'] * 2 for bono in bonos]  # semestres: 0,2,4,6...
    y = [overnight_rate_sem] + [bono['tir'] for bono in bonos]

    # Instanciar interpolador cúbico
    spline = cubica(x, y)

    return spline

# def tasa_spot_interpolada(spline, semestre):
#     return spline.interpolar(semestre)


def tasa_spot_interpolada(spline, semestre):
    M, Y = spline.interpolar()
    solucion = M.resolver_sistema(Y.elems)#[1].elems
    tramos = [solucion[i:i+4] for i in range(0, len(solucion), 4)]
    x = spline.x
    
    # Buscar tramo donde semestre cae entre x[i] y x[i+1]
    for i in range(len(x) - 1):
        if x[i] <= semestre <= x[i+1]:
            coefs = tramos[i]  # coeficientes del tramo
            # Evaluar polinomio cúbico: a*x^3 + b*x^2 + c*x + d
            val = sum(coefs[j] * semestre**(3-j) for j in range(4))
            return val

    raise ValueError("Semestre fuera del rango de interpolación")
