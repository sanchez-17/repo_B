# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 03:48:27 2025

@author: Gaston
"""
# specs.py

def make_bullet_spec(maturity_years, annual_coupon, issue_date=(1,1,2025), first_coupon=(1,7,2025)):
    """
    Devuelve el dict de 'specs' para un bono bullet semestral.
    """
    # Cálculo de año de vencimiento
    y0 = issue_date[2]
    yv = y0 + maturity_years

    return {
        # 1. Identificación
        'ticker':             f'BONO_{maturity_years}Y',
        'empresa':            'Tesoro',
        'descripcion':        f'Bono {maturity_years} años, cupón {annual_coupon*100:.2f}%',
        'pais':               'PAIS',
        'moneda':             'USD',

        # 2. Fechas clave
        'fecha_emision':      issue_date,
        'primer_cupon':       first_coupon,
        'vencimiento':        (first_coupon[0], first_coupon[1], yv),
        'madurez':            (first_coupon[0], first_coupon[1], yv),

        # 3. Cupones
        'tasas_cupones':      [annual_coupon / 2],
        'fechas_tasas_cupones': [(issue_date, (first_coupon[0], first_coupon[1], yv))],
        'frecuencia_cupon':   6,     # meses entre pagos = semestral
        'cupon_irregular':    False,
        'tipo_cupon_irregular':'',
        'tipo_cupon':         'bullet',

        # 4. Capitalización sobre cupones (vacío si no aplica)
        'tasa_cap_cupones':   [],
        'fecha_cap_cupones':  [],

        # 5. Amortización bullet al vencimiento
        'amortizaciones':     1,
        'porcentajes_amort':  [1.0],
        'fechas_amort':       [(issue_date, (first_coupon[0], first_coupon[1], yv))],

        # 6. Financiera
        'valor_nominal':      100,
        'conteo_dias':        'actual/actual',
        'convencion':         '30/360',

        # 7. Liquidación
        'liquidacion':        2,

        # 8. Tipo de bono
        'tipo':               'bullet'
    }

def specs_bono_1():
        
    specs = {
        # 1. Identificación
        'ticker': 'BONO_TEST_4M', 
        'empresa': 'Empresa Prueba',
        'descripcion': 'Bono con capitalización cuatrimestral, primer cupón a 3 meses',
        'pais': 'ARG',
        'moneda': 'ARS',
    
        # 2. Fechas clave
        'fecha_emision': (1, 1, 2025),         # Emisión: 1-ene-2025
        'primer_cupon': (1, 4, 2025),          # Primer cupón: 1-abr-2025 (3 meses después)
        'vencimiento': (1, 12, 2026),          # Vencimiento: 1-dic-2026
        'madurez': (1, 12, 2026),
    
        # 3. Cupones
        'tasas_cupones': [0.08],                          
        'frecuencia_cupon': 4,                    
        'fechas_tasas_cupones': [],         # para ver desde cuando hasta cuando corre cada tasa 
       
        
        'fechas_cupon': None, 
                  
        'cupon_irregular': False,
        'tipo_cupon_irregular': None,       # para ver el tema del primer cupon cuanto corresponde etc
        'tipo_cupon': '',                   # si es bullet, etc...
        'tasa_cap_cupones': [], 
        'fecha_cap_cupones': [],            
    
        # 4. Amortización
        'tipo': '',                   # pueden ser  Bullet (todo el capital al vencimiento), 
        'amortizaciones': 0,
        'porcentajes_amort': [],            # si no es bullet tiene que tener si o si las fechas y los porcentajes de amortizacion 
        'fechas_amort': [],
    
        # 5. Financiera
        'valor_nominal': 1000,
        'conteo_dias': 'actual/actual',
        'convencion': '30/360',
    
        # 6. Liquidación
        'liquidacion': 2                     # Como los intereses se acumulan desde la emisión, cuando comprás un bono entre dos fechas de pago de cupón, vas a tener que pagarle al vendedor el interés corrido desde el último cupón hasta el settlement.         
    }  
    return specs                                      # el settelment day es el dia que recibis el cupon, osea que voy a tener que usar ese dia para calcular el VA0
