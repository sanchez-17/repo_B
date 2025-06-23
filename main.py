# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 00:41:55 2025

@author: Gaston
"""

#%%  Ejercicio 4 a)

from curva_spot import calcular_spots, tasa_spot_interpolada


bonos_data = [
    {'maturity': 1, 'annual_coupon': 0.10, 'price': 106.56},
    {'maturity': 2, 'annual_coupon': 0.08, 'price': 106.20},
    {'maturity': 3, 'annual_coupon': 0.08, 'price': 106.45}
]
overnight_rate = 0.005

spline = calcular_spots(bonos_data, overnight_rate)

print("Tasas spot interpoladas (semestrales):")
for semestre in range(0, 7):
    spot = tasa_spot_interpolada(spline, semestre)
    print(f"Semestre {semestre}: {spot:.6f}")

# if __name__ == "__main__":
#     main()

#%% 
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
