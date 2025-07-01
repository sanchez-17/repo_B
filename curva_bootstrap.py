# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 01:36:38 2025

@author: Gaston
"""



def bootstrapping(par_yields, valor_nominal=100):
    """
    Calcula la curva de tasas cero cupón (spots) mediante bootstrapping
    a partir de tasas par anuales en decimales.

    Args:
        par_yields (list of float): tasas par anuales en decimales para 1Y, 2Y, 3Y, ...
        valor_nominal (float): valor nominal del bono (default: 100)

    Returns:
        list of float: tasas spot anuales (cero cupón) para cada año
    """
    spots = []
    for n, y_par in enumerate(par_yields, start=1):
        C = y_par * valor_nominal
        if n == 1 or n == 2:
            # Para n=1: bono de un año, spot_1 = par_yield
            z1 = y_par
            spots.append(z1)
        else:
            # Suma de los cupones descontados con spots ya calculados
            suma_descuentos = sum(
                C / (1 + spots[i])**(i + 1)
                for i in range(n - 1)
            )
            # Flujo del último periodo: cupón + valor nominal
            flujo_final = C + valor_nominal
            # Despejar z_n
            z_n = (flujo_final / (valor_nominal - suma_descuentos))**(1/n) - 1
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

