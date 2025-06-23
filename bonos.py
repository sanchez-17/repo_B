#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 09:37:28 2025

@author: bautistacenci
"""
from poly import Poly
from fechas import Fechas
import pandas as pd 
from specs import specs_bono_1
pd.set_option('display.max_rows', None)    # para mostrar todas las filas
pd.set_option('display.max_columns', None) # para mostrar todas las columnas
pd.set_option('display.width', None)       # para que no corte horizontalmente
pd.set_option('display.max_colwidth', None) # para que muestre el contenido completo de cada celda

                    
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
    
            # Si no matchea ningún intervalo, pero hay una sola tasa: la uso por defecto
            if tasa_cupon is None:
                if len(self.tasas_cupones) == 1:
                    tasa_cupon = self.tasas_cupones[0]
                else:
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
            
            
    def duration_convexity(self, tir=None, fecha=None):
        """
        Calcula la Duration modificada y la Convexity del bono,
        que son medidas de sensibilidad del precio al cambio en la TIR.
        """
        if tir is None:
            if hasattr(self, "tir"):
                tir = self.tir
            else:
                raise ValueError("Debe proveer una TIR o ejecutar el método Tir primero.")
        
        if fecha is None:
            fecha = self.fecha_emision
    
        fecha0 = Fechas(fecha).date2num()
        df = self.cupones_amortizaciones_capital()
    
        flujos = []
        tiempos = []
    
        for _, row in df.iterrows():
            tnum = Fechas(row["Fechas"]).date2num()
            if tnum <= fecha0:
                continue
            dias = tnum - fecha0
            t = dias / 365.0
            tiempos.append(t)
            flujos.append(float(row["Flujos"]))
    
        # Precio actual descontado (sin interés corrido)
        P = sum(F / (1 + tir)**t for F, t in zip(flujos, tiempos))
    
        # Duration modificada
        D = sum(t * F / (1 + tir)**(t + 1) for F, t in zip(flujos, tiempos)) / P
    
        # Convexidad
        C = sum(t * (t + 1) * F / (1 + tir)**(t + 2) for F, t in zip(flujos, tiempos)) / P
    
        return round(D, 6), round(C, 6)

   
    # def Tir(self, precio=None, fecha=None): #FUNCIONA PARA ENTEROS
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
    
            
    # def Tir(self, precio=None, fecha=None, tol=1e-8, max_iter=100):
    #     """
    #     Calcula la TIR resolviendo f(y)=0 con exponentes continuos t_i usando:
    #      1) Newton-Raphson
    #      2) Si no converge o f'(y) muy pequeño, bisección sobre [0, b_max].
    
    #     f(y) = sum F_i / (1+y)^{t_i}, con F_0 = -precio.
    #     """
    #     from fechas import Fechas
    #     import math
    
    #     # --- 1) Validación inicial ---
    #     if precio is None:
    #         precio = self.clean_price
    #     if fecha is None:
    #         fecha = self.fecha_emision
    
    #     # --- 2) Armar flujos y tiempos exactos en años ---
    #     fecha0 = Fechas(fecha).date2num()
    #     df = self.cupones_amortizaciones_capital()
    
    #     flujos = [-precio]
    #     tiempos = [0.0]
    #     for _, row in df.iterrows():
    #         tnum = Fechas(row["Fechas"]).date2num()
    #         if tnum <= fecha0:
    #             continue
    #         dias = tnum - fecha0
    #         flujos.append(float(row["Flujos"]))
    #         tiempos.append(dias / 365.0)
    
    #     if len(flujos) <= 1:
    #         print("No hay flujos futuros. No se calcula TIR.")
    #         return None
    
    #     # --- 3) Definir f(y) y f'(y) para Newton ---
    #     def f(y):
    #         return sum(F / ((1+y)**t) for F, t in zip(flujos, tiempos))
    
    #     def f_prime(y):
    #         # derivada respecto a y de F/(1+y)^t = -t * F / (1+y)^(t+1)
    #         return sum(-t * F / ((1+y)**(t+1)) for F, t in zip(flujos, tiempos))
    
    #     # --- 4) Newton–Raphson inicial ---
    #     y = 0.05  # semilla 5%
    #     for _ in range(max_iter):
    #         fy = f(y)
    #         fpy = f_prime(y)
    #         if abs(fpy) < 1e-12:
    #             break      # derivada muy pequeña, puede divergir
    #         y_new = y - fy/fpy
    #         if y_new <= -1:
    #             break      # yield imposible (< -100%)
    #         if abs(y_new - y) < tol:
    #             y = y_new
    #             break
    #         y = y_new
    
    #     # Si Newton no convergió razonablemente (f(y) lejos de cero):
    #     if not math.isfinite(y) or abs(f(y)) > tol:
    #         # --- 5) Bisección como fallback ---
    #         a, fa = 0.0, f(0.0)
    #         b, fb = 0.1, f(0.1)
    #         while fa * fb > 0 and b < 1e4:
    #             b *= 2
    #             fb = f(b)
    #         if fa * fb > 0:
    #             print("No hay cambio de signo en [0,b] para bisección:", fa, fb)
    #             return None
    
    #         low, high = a, b
    #         for _ in range(max_iter):
    #             mid = 0.5*(low+high)
    #             fm = f(mid)
    #             if abs(fm) < tol:
    #                 y = mid
    #                 break
    #             if fa * fm < 0:
    #                 high, fb = mid, fm
    #             else:
    #                 low, fa = mid, fm
    #         else:
    #             y = 0.5*(low+high)
    
    #     # --- 6) Validar resultado final ---
    #     if not math.isfinite(y):
    #         print("TIR no finita tras métodos numéricos")
    #         return None
    
    #     self.tir = y
    #     print(f"Fecha valorización: {fecha}")
    #     print(f"TIR encontrada: {round(y, 8)}")
    #     return y

    def Tir(self, precio=None, fecha=None, tol=1e-8, max_iter=100):
        
        """
        Usa Newton-Raphson y biseccion para cualquier funcion, no solo polinomios - Chequear si esto es posible.
        Si los t_i son racionales no puedo usar los metodos originales de Poly
        """
        
        # --- 1) Validación inicial ---
        if precio is None:
            precio = self.clean_price
        if fecha is None:
            fecha = self.fecha_emision
    
        # --- 2) Armar flujos y tiempos exactos en años ---
        fecha0 = Fechas(fecha).date2num()
        df = self.cupones_amortizaciones_capital()
    
        flujos = [-precio]
        tiempos = [0.0]
        for _, row in df.iterrows():
            tnum = Fechas(row["Fechas"]).date2num()
            if tnum <= fecha0:
                continue
            dias = tnum - fecha0
            flujos.append(float(row["Flujos"]))
            tiempos.append(dias / 365.0)
    
        if len(flujos) <= 1:
            print("No hay flujos futuros. No se calcula TIR.")
            return None
        def f(y):       return sum(F/((1+y)**t) for F,t in zip(flujos, tiempos))
        def f_prime(y): return sum(-t*F/((1+y)**(t+1)) for F,t in zip(flujos, tiempos))
    
        # 1) Newton–Raphson vía Poly.newton_root
        try:
            y = Poly.newton_root_R(f, f_prime, x0=0.05, tol=tol, max_iter=max_iter)
        except ValueError:
            # 2) Si falla, bisección fallback
            y = Poly.find_root_R(f, 0.0, 1.0, tol=tol, max_iter=max_iter)
    
        self.tir = y
        print(f"TIR encontrada: {y:.8f}")
        return y


#%%
tires = [0.0422, 0.0443, 0.0434, 0.0436, 0.0431, 0.0411, 0.0395, 0.0391, 0.0402, 0.0421, 0.0444, 0.0496, 0.0495]
df = Bono.tasas_spots(tires,tasa_spot="6M",tasa_cupon=0.10,valor_nominal=100,frecuencia=2)
print(df)
specs= specs_bono_1()
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


#%%

specs = {
'ticker': 'BONO_TEST',
'empresa': 'Test',
'descripcion': 'Bono 1 año 10%',
'pais': 'PAIS',
'moneda': 'USD',
'fecha_emision': (1, 1, 2025),
'primer_cupon': (1, 7, 2025),
'vencimiento': (1, 1, 2026),
'madurez': (1, 1, 2026),
'tasas_cupones': [0.10 / 2],
'frecuencia_cupon': 6,
'fechas_tasas_cupones': [((1, 1, 2025), (1, 1, 2026))],
'cupon_irregular': False,
'tipo_cupon_irregular': '',
'tipo_cupon': 'bullet',
'tasa_cap_cupones': [],
'fecha_cap_cupones': [],
'amortizaciones': 1,
'porcentajes_amort': [1.0],
'fechas_amort' : [((1, 1, 2025), (1, 1, 2026))],
'tipo': 'bullet',
'valor_nominal': 100,
'conteo_dias': 'actual/actual',
'convencion': '30/360',
'liquidacion': 2
}
#%%       Probamos TIR
bono = Bono(specs)
precio = 105
tir = bono.Tir(precio=precio)
assert tir is not None, "TIR no debería ser None"
assert isinstance(tir, float)
assert 0 < tir < 0.1, f"TIR fuera de rango: {tir}"
print(f"TIR calculada por bisección: {tir:.6f}")



#%%        Probamos duration y convexity
bono = Bono(specs)
precio = 100
tir = bono.Tir(precio=precio)
D, C = bono.duration_convexity(tir=tir)
print("Duration modificada:", D)
print("Convexidad:", C)
