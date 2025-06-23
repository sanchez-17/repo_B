# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 03:11:49 2025

@author: Gaston
"""


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
    'tasas_cupones': 0.08,                          
    'frecuencia_cupon': 'cuatrimestral',                    
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
}                                        # el settelment day es el dia que recibis el cupon, osea que voy a tener que usar ese dia para calcular el VA0


        
        
    # def recalcular_precio_con_tir(self, tir_forzada):
    #     """Recalcula el clean y dirty price usando una TIR forzada."""
    #     df = self.df.copy()
    
    #     dias_por_periodo = self.frecuencia_cupon * 30
    #     dias_para_va = df["Dias_hasta_la_fecha"]
    
    #     df['VA_flujo'] = df['Flujos'] / (1 + tir_forzada) ** (dias_para_va / dias_por_periodo)
    #     dirty = df['VA_flujo'].sum()
    #     clean = dirty - self.interes_corrido(self.fecha_valorizacion)
    
    #     self.clean_price = round(clean, 4)
    #     self.dirty_price = round(dirty, 4)
    
    
    # def dv01(self):
    #     """Calcula el DV01 usando una diferencia central con +/-1 bps."""
    #     """ te devuelve lo que varia el precio con un cambio de 0.0001 en la tir"""
    #     tir_actual = self.tir
    
    #     # Cambios de ±1 bps (0.0001)
    #     tir_up = tir_actual + 0.0001
    #     tir_down = tir_actual - 0.0001
    
    #     # Guardar precios actuales
    #     precio_actual = self.clean_price
    
    #     # --- Calcular precio con TIR + 1 bps ---
    #     self.recalcular_precio_con_tir(tir_up)
    #     precio_up = self.clean_price
    
    #     # --- Calcular precio con TIR - 1 bps ---
    #     self.recalcular_precio_con_tir(tir_down)
    #     precio_down = self.clean_price
    
    #     # --- Restaurar precio original ---
    #     self.recalcular_precio_con_tir(tir_actual)
    
    #     # --- Calcular DV01 ---
    #     dv01 = abs(precio_down - precio_up) / 2
    #     return round(dv01, 6), precio_up, precio_down
       
        
        #calc_tasas(maturities=[] , Tires=[]):
        
        # Duration()
        # Convexity()
    


# specs_test = {
#     # 1. Identificación
#     'ticker': 'BONO_BULLET_TEST', 
#     'empresa': 'Empresa Prueba',
#     'descripcion': 'Bono tipo bullet, capital pagado al vencimiento',
#     'pais': 'ARG',
#     'moneda': 'ARS',

#     # 2. Fechas clave
#     'fecha_emision': (1, 1, 2025),
#     'primer_cupon': (1, 4, 2025),
#     'vencimiento': (1, 12, 2026),
#     'madurez': (1, 12, 2026),

#     # 3. Cupones
#     'tasas_cupones': [0.08],             # tasa fija del 8% anual
#     'frecuencia_cupon': 'cuatrimestral', # cupones cada 4 meses
#     'fechas_tasas_cupones': [((1,1,2025), (1,12,2026))],

#     'cupon_irregular': False,
#     'tipo_cupon_irregular': None,
#     'tipo_cupon': 'bullet',

#     'tasa_cap_cupones': [],       # sin capitalización sobre cupones
#     'fecha_cap_cupones': [],

#     # 4. Amortización
#     'tipo': 'bullet',             # capital pagado íntegro al vencimiento
#     'amortizaciones': 0,
#     'porcentajes_amort': [(1.0)],
#     'fechas_amort': [((1, 12, 2026),(1, 12, 2026))],

#     # 5. Financiera
#     'valor_nominal': 1000,
#     'conteo_dias': 'actual/actual',
#     'convencion': '30/360',

#     # 6. Liquidación
#     'liquidacion': 2,             # días para
# }
# specs_amort = {
#     'ticker': 'AMORT01',
#     'empresa': 'Empresa Y',
#     'descripcion': 'Bono con amortización en cuotas iguales',
#     'pais': 'ARG',
#     'moneda': 'ARS',

#     'fecha_emision': (1, 1, 2020),
#     'primer_cupon': (1, 1, 2021),
#     'vencimiento': (1, 1, 2024),
#     'madurez': (1, 1, 2024),

#     'tasas_cupones': [0.08],
#     'fechas_tasas_cupones': [((1, 1, 2020), (1, 1, 2024))],
#     'frecuencia_cupon': 'anual',
#     'cupon_irregular': False,
#     'tipo_cupon_irregular': '',
#     'tipo_cupon': 'fijo',
#     'tasa_cap_cupones': [],
#     'fecha_cap_cupones': [],

#     'amortizaciones': [(1, 1, 2021), (1, 1, 2022), (1, 1, 2023)],
#     'porcentajes_amort': [1/4, 1/4, 1/4,1/4],  # Último cuarto queda para el vencimiento
#     'fechas_amort': [((1, 1, 2020), (1, 1, 2021)), ((1, 1, 2021), (1, 1, 2022)), ((1, 1, 2022), (1, 1, 2023)),((1, 1, 2023), (1, 1, 2024))],

#     'tipo': 'AMORTIZABLE',
#     'valor_nominal': 1000,
#     'conteo_dias': '30/360',
#     'convencion': '30/360',

#     'liquidacion': 0,
# }


 
    
 #TIR
 
 
 

   
    # def Tir(self, precio=None, fecha=None):
    #     """
    #     Calcula la TIR usando la clase Poly. 
    #     Usa t_i = (días entre flujo y fecha_valorizacion) / (frecuencia * 30), redondeados a enteros.
    #     """
    #     if precio is None:
    #         precio = self.clean_price
    #     if fecha is None:
    #         fecha = self.fecha_emision
    
    #     fecha_val = Fechas(fecha)
    #     fecha_val_num = fecha_val.date2num()
    
    #     df = self.cupones_amortizaciones_capital()
        
    #     # Buscar flujos posteriores o iguales a la fecha de valorización
    #     fechas_futuras = []
    #     flujos_futuros = []
    #     for i in range(len(df)):
    #         fecha_flujo_num = Fechas(df.loc[i, "Fechas"]).date2num()
    #         if fecha_flujo_num >= fecha_val_num:
    #             fechas_futuras = df["Fechas"].tolist()[i:]
    #             flujos_futuros = df["Flujos"].tolist()[i:]
    #             break
    
    #     if not flujos_futuros:
    #         print("No hay flujos posteriores o iguales a la fecha dada")
    #         return None
    
    #     # Calcular los t_i (en períodos) redondeados a enteros
    #     dias_futuros = [Fechas(f).date2num() - fecha_val_num for f in fechas_futuras]
    #     t_list = [int(round(d / (self.frecuencia_cupon * 30))) for d in dias_futuros]
    
    #     # Insertar el -precio en t = 0
    #     flujos = [-precio] + flujos_futuros
    #     t_list = [0] + t_list
    
    #     # Armar lista de coeficientes para el polinomio (grado mayor corresponde a flujo más lejano)
    #     max_grado = max(t_list)
    #     coefs = [0.0] * (max_grado + 1)
    
    #     for f, t in zip(flujos, t_list):
    #         coefs[max_grado - t] += float(f)
    
    #     # Eliminar coeficiente penúltimo si es ~0
    #     if len(coefs) > 2 and abs(coefs[-2]) < 1e-6:
    #         coefs.pop(-2)
    
    #     # Crear el polinomio y encontrar raíces
    #     poly = Poly(n=len(coefs) - 1, coefs=coefs)
    #     raices, _ = poly.findroots_newton()
    
    #     positivas = [r for r, m in raices if r > 0]
    #     if not positivas:
    #         print("No se encontraron raíces reales positivas")
    #         return None
    
    #     x_min = min(positivas)
    #     tir = (1 / x_min) - 1
    #     self.tir = tir
    
    #     print(f"Fecha valorización: {fecha}")
    #     print(f"TIR: {round(tir, 6)}")
    #     return round(tir, 6)
    
            