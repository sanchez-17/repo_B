#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:34:36 2025

@author: bautistacenci
"""
# En add2date comente el while.
# En dias_a_fecha meti na guarda para cuando estoy en el mes 12, indexe en 0. Y no se va de rango.
# Agregue add_dias_habiles

class Fechas(object):
    """"En fechas tengo que poner los meses com si fueran del 1 al 12, el codigo se encarga de devolver bien las cosas"""
    """ la fecha origen es 1 del 1 del 2000"""
    fecha_base = (1, 1, 2000)
    
    meses = {
        'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
    }

    dias = {
        'lun': 0, 'mar': 1, 'mie': 2,
        'jue': 3, 'vie': 4, 'sab': 5, 'dom': 6
    }

    dias_por_mes = {
    0: 31,  # enero
    1: 28,  # febrero
    2: 31,  # marzo
    3: 30,  # abril
    4: 31,  # mayo
    5: 30,  # junio
    6: 31,  # julio
    7: 31,  # agosto
    8: 30,  # septiembre
    9: 31,  # octubre
    10: 30, # noviembre
    11: 31  # diciembre
    }


    def __init__(self, fecha, regla="30/360"):
        
        if isinstance(fecha, str):
            fecha_spliteada = fecha.split("-")
            resultado = []
            for parte in fecha_spliteada:
                if parte.isdigit():
                    resultado.append(int(parte))
                elif parte in self.meses:
                    resultado.append(self.meses[parte])
                elif parte in self.dias:
                    resultado.append(self.dias[parte])
            fecha = tuple(resultado)
            
        if not (isinstance(fecha, tuple) and len(fecha) == 3):
            raise ValueError("Formato de fecha no válido. Debe ser string o tupla (día, mes, año).")
            
        self.regla = "30/360"
        self.fecha = fecha    
        self.fecha_num = self.dias_desde_1_1_1()
        self.dow = self.dia_de_semana()

    @staticmethod
    def es_bisiesto(anio):
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def dias_desde_1_1_1(self):
        if self.regla != "30/360":
            dias = 0
            for anio in range(1, self.fecha[2]):
                dias += 366 if self.es_bisiesto(anio) else 365
            for mes in range(0, self.fecha[1]):
                if mes == 1 and self.es_bisiesto(self.fecha[2]):
                    dias += 29
                else:
                    dias += self.dias_por_mes[mes]
            dias += self.fecha[0] - 1
            return dias
        else:
            dias = 0
            for anio in range(1, self.fecha[2]):
                dias += 360  # <-- corregido a 360 días por año
            dias += (self.fecha[1] - 1) * 30  # meses * 30 días
            dias += self.fecha[0] - 1
        return dias

    def distancia_en_dias(self, fechaB):
        """devuelve la distancia en dias desde la fecha base"""
        d1 = self.dias_desde_1_1_1()
        d2 = fechaB.dias_desde_1_1_1()
        if d1 > d2: 
            return d1 - d2
        return d2-d1
    
    def dia_de_semana(self):
        """"devuelve el nombre del dia de la fecha"""
        dias_dicci = {
            0: 'lun',
            1: 'mar',
            2: 'mie',
            3: 'jue',
            4: 'vie',
            5: 'sab',
            6: 'dom'}
        dia = self.dias_desde_1_1_1()
        r = dia % 7 
        return dias_dicci[r]
        
    def date2num(self):
        return self.dias_desde_1_1_1() 
    
    
    @staticmethod
    def dias_a_fecha(dias,regla="30/360"):
        if regla == "real":       
           anio = 1
           while True:
               dias_anio = 366 if Fechas.es_bisiesto(anio) else 365
               if dias >= dias_anio:
                   dias -= dias_anio
                   anio += 1
               else:
                   break
    
           mes = 0
           while True:
               if mes > 11:
                   mes = 0
                   anio += 1
               
               dias_mes = Fechas.dias_por_mes[mes]
               if mes == 1 and Fechas.es_bisiesto(anio):
                   dias_mes = 29
               if dias >= dias_mes:
                   dias -= dias_mes
                   mes += 1
               else:
                   break
    
           dia = dias + 1
           return (dia, mes, anio)
        anios = dias // 360
        resto = dias % 360
        meses = resto // 30
        dias_restantes = resto % 30
        return (dias_restantes + 1, meses + 1, anios + 1)
    
    def add_dias_habiles(self, dias_habiles):
        """Suma días hábiles a la fecha actual y ajusta si cae en fin de semana."""
        fecha_actual = self.fecha
        dias_sumados = 0
    
        while dias_sumados < dias_habiles:
            # Suma 1 día calendario
            fecha_actual = self.add2date(dias=1, meses=0, anios=0)
            fecha_obj = Fechas(fecha_actual, self.regla)
            dow = fecha_obj.dia_de_semana()
            if dow not in ['sab', 'dom']:
                dias_sumados += 1
            self.fecha = fecha_obj.fecha  # Actualizo la fecha interna
    
        # Verifico si la fecha final cae en fin de semana y la corrijo
        dow_final = self.dia_de_semana()
        if dow_final == 'sab':
            self.fecha = self.add2date(dias=2, meses=0, anios=0)
        elif dow_final == 'dom':
            self.fecha = self.add2date(dias=1, meses=0, anios=0)
    
        return self.fecha
             
    def add2date(self, dias=0, meses=0, anios=0):
        """Desplaza una fecha sumando días, meses y años de forma precisa."""
        if self.regla != "30/360":
            dia, mes, anio = self.fecha  
        
            # Paso 1: Sumar años (ajustando para años bisiestos si es 29/02)
            anio += anios
            if mes == 2 and dia == 29 and not self.es_bisiesto(anio):
                dia = 28  
        
            # Paso 2: Sumar meses
            mes += meses
            anio += (mes - 1) // 12
            mes = ((mes - 1) % 12) + 1
            # while mes > 12:
            #     mes -= 12
            #     anio += 1
        
            # Ajustar día si excede los días del nuevo mes (ej: 31/04 → 30/04)
            dias_en_mes = self.dias_por_mes[mes - 1]  # Restamos 1 porque el diccionario usa 0-11
            if mes == 2 and self.es_bisiesto(anio):
                dias_en_mes = 29
            if dia > dias_en_mes:
                dia = dias_en_mes
        
            # Paso 3: Sumar días (manejando desbordamiento de mes/año)
            dia += dias
            while True:
                dias_en_mes = self.dias_por_mes[mes - 1]
                if mes == 2 and self.es_bisiesto(anio):
                    dias_en_mes = 29
                if dia <= dias_en_mes:
                    break
                dia -= dias_en_mes
                mes += 1
                if mes > 12:
                    mes = 1
                    anio += 1
        
            return (dia, mes, anio)
        
        dias= dias+(meses*30)+(anios*360)
        fecha_corrida =  self.date2num()
        nueva_fecha_endias = fecha_corrida + dias
        fecha = Fechas.dias_a_fecha(nueva_fecha_endias)
        return fecha
     
    def timetodate(self, dateB, units="d"):
        if not isinstance(dateB, Fechas):
            dateB = Fechas(dateB, self.regla)
            
        fecha1endias = self.dias_desde_1_1_1()
        fecha2endias = dateB.dias_desde_1_1_1()
        diferencia = fecha2endias - fecha1endias
    
        if self.regla == "real":
            if units == "d" or units == "":
                return diferencia
    
            # Trabajar de menor a mayor fecha para evitar negativos en meses/días
            if diferencia < 0:
                start = dateB.fecha
                end = self.fecha
                signo = -1
            else:
                start = self.fecha
                end = dateB.fecha
                signo = 1
    
            d1, m1, y1 = start
            d2, m2, y2 = end
    
            anios = y2 - y1
            meses = m2 - m1
            dias = d2 - d1
    
            if dias < 0:
                meses -= 1
                mes_prev = (m2 - 2) % 12
                anio_corr = y2 if m2 > 1 else y2 - 1
                if mes_prev == 1 and Fechas.es_bisiesto(anio_corr):
                    dias += 29
                else:
                    dias += Fechas.dias_por_mes[mes_prev]
    
            if meses < 0:
                anios -= 1
                meses += 12
    
            if units == "dm":
                return (signo * dias, signo * (meses + anios * 12))
            elif units == "dmy":
                return (signo * dias, signo * meses, signo * anios)
            else:
                raise ValueError("Unidad no reconocida. Usar 'd', 'dm' o 'dmy'.")
    
        else:
            # Para regla 30/360 o similares
            signo = -1 if diferencia < 0 else 1
            dias_totales = abs(diferencia)
            anios = dias_totales // 360
            dias_restantes = dias_totales % 360
            meses = dias_restantes // 30
            dias = dias_restantes % 30
    
            if units == "d" or units == "":
                return signo * diferencia
            elif units == "dm":
                return (signo * dias, signo * (meses + anios * 12))
            elif units == "dmy":
                return (signo * dias, signo * meses, signo * anios)
            else:
                raise ValueError("Unidad no reconocida. Usar 'd', 'dm' o 'dmy'.")

           
    def schedule(start_date, end_date, frecuencia_meses, regla="30/360"):
        if not isinstance(start_date, Fechas):
            start_date = Fechas(start_date, regla)
        if not isinstance(end_date, Fechas):
            end_date = Fechas(end_date, regla)
        
        if not isinstance(frecuencia_meses, int) or frecuencia_meses <= 0:
            raise ValueError("La frecuencia debe ser un número entero positivo de meses.")
        
        dias = 0
        meses = frecuencia_meses
    
        calendario = []
        current_date = start_date
    
        while True:
            if current_date.date2num() > end_date.date2num():
                break
    
            calendario.append(current_date.fecha)
    
            nueva_fecha = current_date.add2date(dias, meses, 0)
            current_date = Fechas(nueva_fecha, regla)
    
        return calendario

    
    
    
    
    
    
    
    
    
    
    
    
    