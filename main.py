# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 00:41:55 2025

@author: Gaston
"""

from curva_spot import calcular_spots, tasa_spot_interpolada

def main():
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

if __name__ == "__main__":
    main()
