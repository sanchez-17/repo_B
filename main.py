# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 00:41:55 2025

@author: Gaston
"""

#%%  Ejercicio 4 a)
from curva_spot import calcular_spots, tasa_spot_interpolada

# Datos de mercado
bonos_data = [
    {'maturity': 1, 'annual_coupon': 0.10, 'price': 106.56},
    {'maturity': 2, 'annual_coupon': 0.08, 'price': 106.20},
    {'maturity': 3, 'annual_coupon': 0.08, 'price': 106.45}
]

overnight_rate = 0.005

# a) Construir yield curve y spline
spline = calcular_spots(bonos_data, overnight_rate)

print("Tasas spot interpoladas (semestrales):")
for semestre in range(0, 7):
    spot = tasa_spot_interpolada(spline, semestre)
    print(f"Semestre {semestre}: {spot:.6f}")

#%%  Ejercicio 4 b)

from curva_descuento import calcular_factores_descuento, valuar_flujos

# Supongamos que ya tienes spline (de punto a)
max_semestre = 30  # por ejemplo, hasta 15 años si semestres
factores = calcular_factores_descuento(spline, max_semestre)

# Ejemplo de flujos (semestre, monto)
flujos_ejemplo = [
    (2, 5.0),   # semestre 2 paga 5 unidades monetarias
    (4, 5.0),
    (6, 105.0)  # último pago con capital + cupón
]

vp = valuar_flujos(flujos_ejemplo, factores)
print(f"Valor presente descontado de los flujos: {vp:.4f}")

#%% Ejercicio 4 c)

from curva_bootstrap import bootstrapping, mostrar_curva

# Tasas par anuales en decimal (simuladas o del punto b)
tasas_par = [0.05, 0.055, 0.057]  # 5%, 5.5%, 5.7% anual

spots = bootstrapping(tasas_par)
mostrar_curva(spots)

#%% Ejercicio 4 d)

from curva_bootstrap import valuar_bono_con_spot

valor_nominal_bono4 = 100
cupon_anual_bono4 = 0.09  # 9%

vp_bono4 = valuar_bono_con_spot(valor_nominal_bono4, cupon_anual_bono4, spots)
print(f"\nPrecio libre de arbitraje del Bono 4: {vp_bono4:.4f}")

precio_mercado_bono4 = 109.01
print(f"Precio de mercado del Bono 4: {precio_mercado_bono4:.2f}")

#%% Ejercicio 4 d)
if vp_bono4 < precio_mercado_bono4:
    print("El bono 4 está sobrevaluado en el mercado.")
    #print("Estrategia de arbitraje: Vender el bono 4 y comprar sus flujos replicados con strip bonds.")
elif vp_bono4 > precio_mercado_bono4:
    print("El bono 4 está subvaluado en el mercado.")
    #print("Estrategia de arbitraje: Comprar el bono 4 y vender sus flujos replicados con strip bonds.")
else:
    print("El bono 4 está correctamente valuado. No hay oportunidad de arbitraje.")

