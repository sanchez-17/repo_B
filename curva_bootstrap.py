# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 01:36:38 2025

@author: Gaston
"""

# curva_bootstrap.py

def bootstrapping(tasas_par, valor_nominal=100):
    """
    Calcula la curva de tasas cero cupón mediante bootstrapping a partir de tasas par anuales.

    Args:
        tasas_par (list of float): tasas par anuales en decimales para 1Y, 2Y, 3Y, ...
        valor_nominal (float): valor nominal del bono (default: 100)

    Returns:
        list of float: tasas spot anuales (cero cupón) para cada año
    """
    spots = []
    for n, c in enumerate(tasas_par):
        n += 1  # el primer bono tiene vencimiento a 1 año
        cupon = c * valor_nominal
        precio = valor_nominal  # los bonos par tienen precio 100

        suma_descuentos = sum([cupon / (1 + spots[i])**(i + 1) for i in range(n - 1)]) if n > 1 else 0

        # Usamos la ecuación de valuación de un bono bullet:
        # P = sum_{i=1}^{n-1} C / (1+z_i)^i + (C + FV) / (1+z_n)^n
        flujo_final = cupon + valor_nominal
        z_n = ((flujo_final) / (precio - suma_descuentos))**(1/n) - 1
        spots.append(z_n)

    return spots


def mostrar_curva(spots):
    print("Año\tSpot anual (%)")
    for i, z in enumerate(spots):
        print(f"{i+1}\t{z*100:.4f}")
        
        
def valuar_bono_con_spot(valor_nominal, cupon_anual, spots):
    """
    Calcula el precio libre de arbitraje de un bono a partir de la curva de tasas cero cupón (spots).

    Args:
        valor_nominal (float): valor nominal del bono (e.g., 100)
        cupon_anual (float): tasa de cupón anual en decimal (e.g., 0.09 para 9%)
        spots (list of float): tasas spot anuales para cada año (longitud igual a años de madurez)

    Returns:
        float: precio del bono calculado descontando sus flujos con las tasas spot
    """
    flujo_cupon = cupon_anual * valor_nominal
    precio = 0.0
    for i, z in enumerate(spots):
        t = i + 1
        if t < len(spots):
            precio += flujo_cupon / (1 + z)**t
        else:
            # Último flujo: cupón + valor nominal
            precio += (flujo_cupon + valor_nominal) / (1 + z)**t
    return precio

