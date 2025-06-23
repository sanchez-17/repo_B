#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 09:37:28 2025

@author: bautistacenci
"""
from Tp_poly_bien2 import Poly
from Fechas_2 import Fechas
import pandas as pd 
pd.set_option('display.max_rows', None)    # para mostrar todas las filas
pd.set_option('display.max_columns', None) # para mostrar todas las columnas
pd.set_option('display.width', None)       # para que no corte horizontalmente
pd.set_option('display.max_colwidth', None) # para que muestre el contenido completo de cada celda


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

                    
class Bono(object):   
    
    def __init__(self, specs):
        # 1. Identificación
        self.ticker = specs['ticker']
        self.empresa = specs['empresa']
        self.descripcion = specs['descripcion']
        self.pais = specs['pais']
        self.moneda = specs['moneda']

        # 2. Fechas
        self.fecha_emision = specs['fecha_emision']
        self.primer_cupon = specs['primer_cupon']
        self.vencimiento = specs['vencimiento']
        self.madurez = specs['madurez']

        # 3. Cupones
        self.tasas_cupones = specs['tasas_cupones']                 # hacer funcion que convierta las tasas 
        self.fechas_tasas_cupones = specs['fechas_tasas_cupones']
        self.frecuencia_cupon = specs['frecuencia_cupon']
        
        self.cupon_irregular = specs['cupon_irregular']
        self.tipo_cupon_irregular = specs['tipo_cupon_irregular']
        self.tipo_cupon = specs['tipo_cupon']
        self.tasas_cap_sobre_cupones = specs['tasa_cap_cupones']
        self.fecha_cap_cupones = specs['fecha_cap_cupones']

        # 4. Amortización
        self.amortizaciones = specs['amortizaciones']
        self.porcentajes_amort = specs['porcentajes_amort']          # hacer funcion que convierta las tasas 
        self.fechas_amort = specs['fechas_amort']

        # 5. Financiera
        self.tipo = specs['tipo']
        self.valor_nominal = specs['valor_nominal']
        self.conteo_dias = specs['conteo_dias']
        self.convencion = specs['convencion']

        # 6. Liquidación
        self.liquidacion = specs['liquidacion']

        # 7. Calendario
        self.calendario_cupones = self.calendario(self.fecha_emision, self.vencimiento, self.primer_cupon, self.frecuencia_cupon)
        self.dias_hasta_la_fecha = self.dias_hasta_fecha()
        
        #self.clean_price, self.dirty_price, self.df = self.precio_clean_dirty_por_tasa_curva(fecha_valorizacion= , tir= )
        
         

    @staticmethod
    def calendario(emision, vencimiento, primer_pago_cupon, frecuencia):
        fechas = Fechas.schedule(primer_pago_cupon, vencimiento, frecuencia) 
        if emision == primer_pago_cupon:
            return fechas
        else:
            fechas.insert(0, emision)
            return fechas

    def dias_hasta_fecha(self):
        dias_hasta_fecha_list = []
        fecha_emision = Fechas(self.fecha_emision)
        for f in self.calendario_cupones:
            fecha_cupon = Fechas(f)
            dias_hasta_fecha_list.append(fecha_emision.timetodate(fecha_cupon))
        return dias_hasta_fecha_list
            
     
    def copy(self):
        copia = self.lista.copy()  # forma común para listas
        # o bien: copia = list(self.lista)
        return copia
    
    
    def cupones_amortizaciones_capital(self):
        capital = self.valor_nominal
        cupones = []
        amortizaciones = []
        capitales = [round(capital, 2)]  # Capital inicial
        capitalizacion_pendiente = 0  # Para llevar la capitalización que se aplicará en el próximo período
    
        fechas = self.calendario_cupones
        fechas_nums = [Fechas(f).date2num() for f in fechas]
        fecha_emision_num = Fechas(self.fecha_emision).date2num()
    
        # Inicializamos con 0 para la primera fecha
        cupones.append(0)
        amortizaciones.append(0)
    
        for i in range(1, len(fechas)):
            fecha_num = fechas_nums[i]
            cupon = 0
            amort = 0
    
            # Aplicamos la capitalización pendiente del período anterior
            capital += capitalizacion_pendiente
            capital = round(capital, 2)
            capitalizacion_pendiente = 0  # Reiniciamos para este período
    
            # Guardamos el capital ACTUAL (después de capitalización anterior)
            capital_actual = capital
            capitales.append(round(capital_actual, 2))
    
            # === 1. CUPÓN IRREGULAR LARGO ===
            if self.cupon_irregular and self.tipo_cupon_irregular in ["LFC", "LFCRV"]:
                if i == 1:
                    # En la primera fecha no se paga cupón
                    cupones.append(0)
                    amortizaciones.append(0)
                    continue
                elif i == 2:
                    tasa = self.tasas_cupones[0]
                    if self.tipo_cupon_irregular == "LFC":
                        if self.convencion == "30/360":
                            dias = fechas_nums[i] - fecha_emision_num
                            factor = dias / (self.frecuencia_cupon * 30)
                        else:
                            dias = Fechas(fechas[i], "real").date2num() - Fechas(self.fecha_emision, "real").date2num()
                            factor = dias / 365
                        cupon = capital_actual * tasa * factor
                    elif self.tipo_cupon_irregular == "LFCRV":
                        cupon = capital_actual * tasa
                    cupones.append(round(cupon, 2))
                    amortizaciones.append(0)
                    continue
    
            # === 2. TASA DEL CUPÓN ===
            tasa_cupon = None
            for j, (ini, fin) in enumerate(self.fechas_tasas_cupones):
                if Fechas(ini).date2num() <= fecha_num <= Fechas(fin).date2num():
                    tasa_cupon = self.tasas_cupones[j]
                    break
    
            if tasa_cupon is None:
                cupones.append(0)
                amortizaciones.append(0)
                continue
    
            cupon = capital_actual * tasa_cupon
    
            # === 3. CAPITALIZACIÓN ===
            for k, (ini_cap, fin_cap) in enumerate(self.fecha_cap_cupones):
                if Fechas(ini_cap).date2num() <= fecha_num <= Fechas(fin_cap).date2num():
                    tasa_cap = self.tasas_cap_sobre_cupones[k]
                    capitalizacion_pendiente = cupon * tasa_cap
                    cupon -= capitalizacion_pendiente
                    break
    
            # === 4. AMORTIZACIÓN ===
            amort_aplicada = False
            for m, (ini_amort, fin_amort) in enumerate(self.fechas_amort):
                if fecha_num == Fechas(fin_amort).date2num():
                    tasa_amort = self.porcentajes_amort[m]
                    amort = round(capital_actual * tasa_amort, 2)
                    capital -= amort
                    capital = round(capital, 2)
                    amort_aplicada = True
                    break
            if not amort_aplicada:
                amort = 0
    
            # === 5. GUARDAR ===
            cupones.append(round(cupon, 2))
            amortizaciones.append(amort)
    
        # Ajustamos el capital mostrado cuando hay amortización
        for i in reversed(range(len(amortizaciones))):
            if amortizaciones[i] > 0:
                capitales[i] = amortizaciones[i]
                break
    
        flujos = [c + a for c, a in zip(cupones, amortizaciones)]
    
        df = pd.DataFrame({
            "Dias_hasta_la_fecha": self.dias_hasta_la_fecha,
            "Fechas": self.calendario_cupones,
            "Capital": capitales,
            "Amortizaciones": amortizaciones,
            "Cupones": cupones,
            "Flujos": flujos
        })
    
        return df

    
    
    
    def interes_corrido(self, fecha_valorizacion):
        """
        Calcula el interés corrido:
        - Desde emisión hasta primer cupón si aún no se pagó ninguno.
        - Desde último cupón hasta la fecha si ya se pagó al menos uno.
        """
        fecha_val = Fechas(fecha_valorizacion)
        fecha_val_num = fecha_val.date2num()
        emision_num = Fechas(self.fecha_emision).date2num()
        primer_cupon_num = Fechas(self.primer_cupon).date2num()
    
        # Tasa aplicable
        tasa = 0
        for j, (ini, fin) in enumerate(self.fechas_tasas_cupones):
            if Fechas(ini).date2num() <= fecha_val_num <= Fechas(fin).date2num():
                tasa = self.tasas_cupones[j]
                break
        if tasa == 0 and len(self.tasas_cupones) == 1:
            tasa = self.tasas_cupones[0]
    
        capital = self.valor_nominal
    
        # Caso 1: antes del primer cupón → usar emisión → primer cupón
        if fecha_val_num < primer_cupon_num:
            fecha_ini = self.fecha_emision
            fecha_fin = self.primer_cupon
    
        # Caso 2: después del primer cupón
        else:
            # Quitamos emisión si no paga
            calendario = [f for f in self.calendario_cupones if f != self.fecha_emision or f == self.primer_cupon]
            fechas_num = [Fechas(f).date2num() for f in calendario]
    
            fecha_ini = None
            fecha_fin = None
            for i in range(1, len(fechas_num)):
                if fechas_num[i - 1] <= fecha_val_num < fechas_num[i]:
                    fecha_ini = calendario[i - 1]
                    fecha_fin = calendario[i]
                    break
            else:
                # Si no se encuentra intervalo, puede ser que fecha_val sea igual al último cupón
                if fecha_val_num == fechas_num[-1]:
                    return 0
                return 0  # fecha fuera del rango de cupones futuros
    
        # Cálculo de días
        dias_transcurridos = Fechas(fecha_ini).timetodate(Fechas(fecha_valorizacion), units='d')
        dias_totales = Fechas(fecha_ini).timetodate(Fechas(fecha_fin), units='d')
    
        if dias_totales == 0 or dias_transcurridos < 0:
            return 0
    
        interes = capital * tasa * (dias_transcurridos / dias_totales)
        return round(interes, 4)


    
    
    def precio_clean_dirty_por_tasa_curva(self, fecha_valorizacion=None, tir=None):
        """
        Calcula el precio clean y dirty usando una TIR y una fecha de valorización.
        No usa tasas de cupones, solo descuenta los flujos desde la fecha de valorización completa.
        """
        if fecha_valorizacion is None:
            fecha_valorizacion = self.fecha_emision
        if tir is None:
            raise ValueError("Debés proporcionar una TIR para calcular el precio.")
    
        self.fecha_valorizacion = fecha_valorizacion
        df = self.cupones_amortizaciones_capital()
    
        # Fecha en días desde el origen
        fecha_val_num = Fechas(fecha_valorizacion).date2num()
    
        # Descontar cada flujo desde fecha de valorización
        t_i = df["Fechas"].apply(
            lambda f: (Fechas(f).date2num() - fecha_val_num) / (self.frecuencia_cupon * 30)
        )
    
        df["VA_flujo"] = df["Flujos"] / (1 + tir) ** t_i
    
        # Sumar los valores descontados
        dirty_price = df["VA_flujo"].sum()
    
        # Calcular fecha de liquidación
        fecha_liquidacion = Fechas(fecha_valorizacion).add2date(self.liquidacion)
    
        # Calcular interés corrido desde último cupón hasta liquidación
        try:
            interes_corrido = self.interes_corrido(fecha_liquidacion)
        except:
            interes_corrido = 0
    
        clean_price = dirty_price - interes_corrido
    
        return round(clean_price, 4), round(dirty_price, 4), df



   
    def Tir(self, precio=None, fecha=None):
        """
        Calcula la TIR usando la clase Poly. 
        Usa t_i = (días entre flujo y fecha_valorizacion) / (frecuencia * 30), redondeados a enteros.
        """
        if precio is None:
            precio = self.clean_price
        if fecha is None:
            fecha = self.fecha_emision
    
        fecha_val = Fechas(fecha)
        fecha_val_num = fecha_val.date2num()
    
        df = self.cupones_amortizaciones_capital()
        
        # Buscar flujos posteriores o iguales a la fecha de valorización
        fechas_futuras = []
        flujos_futuros = []
        for i in range(len(df)):
            fecha_flujo_num = Fechas(df.loc[i, "Fechas"]).date2num()
            if fecha_flujo_num >= fecha_val_num:
                fechas_futuras = df["Fechas"].tolist()[i:]
                flujos_futuros = df["Flujos"].tolist()[i:]
                break
    
        if not flujos_futuros:
            print("No hay flujos posteriores o iguales a la fecha dada")
            return None
    
        # Calcular los t_i (en períodos) redondeados a enteros
        dias_futuros = [Fechas(f).date2num() - fecha_val_num for f in fechas_futuras]
        t_list = [int(round(d / (self.frecuencia_cupon * 30))) for d in dias_futuros]
    
        # Insertar el -precio en t = 0
        flujos = [-precio] + flujos_futuros
        t_list = [0] + t_list
    
        # Armar lista de coeficientes para el polinomio (grado mayor corresponde a flujo más lejano)
        max_grado = max(t_list)
        coefs = [0.0] * (max_grado + 1)
    
        for f, t in zip(flujos, t_list):
            coefs[max_grado - t] += float(f)
    
        # Eliminar coeficiente penúltimo si es ~0
        if len(coefs) > 2 and abs(coefs[-2]) < 1e-6:
            coefs.pop(-2)
    
        # Crear el polinomio y encontrar raíces
        poly = Poly(n=len(coefs) - 1, coefs=coefs)
        raices, _ = poly.findroots_newton()
    
        positivas = [r for r, m in raices if r > 0]
        if not positivas:
            print("No se encontraron raíces reales positivas")
            return None
    
        x_min = min(positivas)
        tir = (1 / x_min) - 1
        self.tir = tir
    
        print(f"Fecha valorización: {fecha}")
        print(f"TIR: {round(tir, 6)}")
        return round(tir, 6)

    def tasas_spots(tires, tasa_spot="6M", tasa_cupon=None, valor_nominal=100,frecuencia=2 ):
        periodos = ["1M", "2M", "3M", "4M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
        meses = {"M": 1, "Y": 12}
    
        # Convertir los períodos a semestres
        semestres = []
        for p in periodos:
            cantidad = int(''.join([c for c in p if c.isdigit()]))
            unidad = ''.join([c for c in p if c.isalpha()])
            meses_totales = cantidad * meses[unidad]
            s = meses_totales // 6
            semestres.append(s)
    
        # Buscar desde qué índice arranca la tasa_spot conocida
        i0 = periodos.index(tasa_spot)
        spot = [0] * (semestres[-1] + 1)
        
        # Inicializamos la tasa spot conocida (suponemos bono cero cupón → spot = tir)
        spot[semestres[i0]] = tires[i0]
    
        # Cálculo de cupones
        C = tasa_cupon * valor_nominal / frecuencia
    
        # Bootstrapping desde el siguiente semestre
        for i in range(semestres[i0] + 1, 31):  # hasta semestre 30
            flujos = [C] * (i - 1)
            suma = sum([C / (1 + spot[j])**j for j in range(1, i)])
            precio = valor_nominal  # asumimos precio 1000
            residual = precio - suma
            tasa_i = ((C + valor_nominal) / residual)**(1 / i) - 1
            spot[i] = tasa_i
    
        # Crear DataFrame final
        import pandas as pd
        df = pd.DataFrame({
            "semestre": list(range(1, 31)),
            "spot (%)": [round(spot[i] * 100, 6) for i in range(1, 31)]
        })
        return df

        
        
        
        
        
        
        
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

specs = {
    'ticker': 'BULLET_TIR_POS',
    'empresa': 'Empresa Positiva',
    'descripcion': 'Bono bullet con cupones anuales del 10% y TIR positiva',
    'pais': 'ARG',
    'moneda': 'ARS',

    'fecha_emision': (1, 1, 2023),
    'primer_cupon': (1, 1, 2024),
    'vencimiento': (1, 1, 2026),
    'madurez': (1, 1, 2026),

    'tasas_cupones': [0.10],  # 10% anual
    'fechas_tasas_cupones': [((1, 1, 2023), (1, 1, 2026))],
    'frecuencia_cupon': 12,  # anual
    'cupon_irregular': False,
    'tipo_cupon_irregular': '',
    'tipo_cupon': 'fijo',

    'tasa_cap_cupones': [],
    'fecha_cap_cupones': [],

    'amortizaciones': [(1, 1, 2026)],
    'porcentajes_amort': [1.0],
    'fechas_amort': [((1, 1, 2023), (1, 1, 2026))],

    'tipo': 'BULLET',
    'valor_nominal': 1000,
    'conteo_dias': '30/360',
    'convencion': '30/360',

    'liquidacion': 2
}





tires = [0.0422, 0.0443, 0.0434, 0.0436, 0.0431, 0.0411, 0.0395, 0.0391, 0.0402, 0.0421, 0.0444, 0.0496, 0.0495]
df = Bono.tasas_spots(tires,tasa_spot="6M",tasa_cupon=0.10,valor_nominal=100,frecuencia=2)
print(df)
bono = Bono(specs)
# print(bono.calendario_cupones)
# print(bono.dias_hasta_fecha())
data_f = bono.cupones_amortizaciones_capital()
bono.Tir(950,(1,6,2024))
clean, dirty, df = bono.precio_clean_dirty_por_tasa_curva(fecha_valorizacion=(1,6,2024),tir=0.10) 
print(clean)
print(dirty)
print(df.to_string(index=False))
# bono.Tir()
# print(bono.dv01())



