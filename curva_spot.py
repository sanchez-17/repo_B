# curva_spot.py

from bonos import Bono
from spline_cubica import cubica
from specs import make_bullet_spec   # <-- importamos

def crear_bono(maturity_years, annual_coupon, price):
    # Generamos automáticamente el specs correcto
    specs = make_bullet_spec(maturity_years, annual_coupon)
    bono = Bono(specs)
    tir = bono.Tir(precio=price)
    return bono, tir

def calcular_spots(bonos_data, overnight_rate):
    """
    Dada una lista de bonos (con madurez, cupón anual y precio) y la tasa overnight,
    devuelve un objeto spline cúbico natural preparado para interpolar tasas spot semestrales.
    """
    bonos = []
    for data in bonos_data:
        _, tir = crear_bono(data['maturity'], data['annual_coupon'], data['price'])
        bonos.append({'maturity': data['maturity'], 'tir': tir})

    # Convertir tasa overnight anual a semestral compuesta
    overnight_rate_sem = (1 + overnight_rate) ** (182 / 365) - 1

    # Puntos para la spline (semestres)
    x = [0] + [bono['maturity'] * 2 for bono in bonos]  # ej: 0, 2, 4, 6 ...
    y = [overnight_rate_sem] + [bono['tir'] for bono in bonos]

    spline = cubica(x, y)
    spline.calcular_coeficientes()
    return spline

def tasa_spot_interpolada(spline, semestre):
    """
    Evalúa la tasa spot para un semestre dado usando la spline cúbica natural ya calculada.
    """
    return spline.evaluar(semestre)

#%%
"""
De entrada tenemos una lista de tir
bono semestral 
[tir_1, tir_2 , ...]

calcular spots 


"""