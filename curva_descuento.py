# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 01:10:37 2025

@author: Gaston
"""

from spline_cubica import cubica

def calcular_factores_descuento(spline, max_semestre):
    """
    Calcula los factores de descuento para semestres 0 hasta max_semestre usando la curva spot interpolada.
    
    Args:
        spline (cubica): objeto spline cúbica con la curva spot.
        max_semestre (int): semestre máximo hasta donde calcular factores.
    
    Returns:
        list: factores de descuento para cada semestre (índice 0 es semestre 0, valor 1)
    """
    factores = []
    for semestre in range(max_semestre + 1):
        tasa_spot = spline.interpolar(semestre)
        # tasa spot semestral en decimal, aplicamos fórmula factor de descuento:
        # DF = 1 / (1 + r)^t
        factor = 1 / (1 + tasa_spot) ** semestre if semestre > 0 else 1.0
        factores.append(factor)
    return factores

def valuar_flujos(flujos, factores_descuento):
    """
    Calcula el valor presente de un conjunto de flujos futuros dados los factores de descuento.
    
    Args:
        flujos (list of tuples): lista de tuplas (semestre, monto_flujo).
        factores_descuento (list): factores de descuento por semestre.
        
    Returns:
        float: valor presente total descontado.
    """
    vp_total = 0.0
    for semestre, monto in flujos:
        if semestre >= len(factores_descuento):
            raise ValueError(f"Factor de descuento no calculado para semestre {semestre}")
        vp_total += monto * factores_descuento[semestre]
    return vp_total
