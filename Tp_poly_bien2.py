#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:23:45 2025

@author: bautistacenci
"""

class Poly(object):
    
    def __init__(self, n=0, coefs=[0]):
        if n != len(coefs)-1:
            raise ValueError("El n no es igual al grado de polinomio")  
        self.n = n
        self.coefs = coefs[:] 



    def get_expression(self):
        """ devuelve la expresion del polinomio"""
        expresion = ""
        grado = self.n 
        for coef in self.coefs:
            if coef != 0:
                if coef > 0 and len(expresion) > 0:
                    expresion += f"+{coef}x^{grado} "
                else:
                    expresion += f"{coef}x^{grado} "
            grado -= 1      
        print(f"F(x) = {expresion}")




    def __call__(self, x):
        """ permite valuar mi polinomio en el x que le doy """
        resultado = 0
        grado = self.n
        for coef in self.coefs:
            resultado += coef * x**grado
            grado -= 1
        return resultado




    def ply_plt(self, a, b, ax=None, **kwargs):
        import matplotlib.pyplot as plt 
        import numpy as np 
        
        def f(x):
            grado = self.n
            resultado = 0
            for coef in self.coefs: 
                resultado += coef*x**grado
                grado -= 1
            return resultado 
                
        x = np.linspace(a, b, 300)
        y = f(x)
    
        if ax is None:
            plt.plot(x, y, **kwargs)
            plt.xlabel("x")
            plt.ylabel("F(x)")
            plt.title("Polinomio")
            plt.grid(True)
            plt.show()
        else:
            ax.plot(x, y, **kwargs)
            ax.set_xlabel("x")
            ax.set_ylabel("F(x)")
            ax.set_title("Polinomio")
            ax.grid(True)



    def grado(self):
        return self.n




    def __add__(self, other):
        """ suma dos polinomios """
        if isinstance(other, (int, float)):
            other = Poly(n=0, coefs=[other])

        max_length = max(len(self.coefs), len(other.coefs))
        coefs1 = [0] * (max_length - len(self.coefs)) + self.coefs 
        coefs2 = [0] * (max_length - len(other.coefs)) + other.coefs 
        
        new_coefs = [a + b for a, b in zip(coefs1, coefs2)]
        return Poly(n=len(new_coefs)-1, coefs=new_coefs)
   
    
    def __radd__(self, other): 
        return self + other 




    def __sub__(self, other):
        """ resta dos polinomios, en other pones el polinomio que le queres restar"""
        """ resta los coeficientes de igual grado y devuelve un polinomio con el resultado de la resta de los mismos"""
        if isinstance(other, (int, float)):
            other = Poly(n=0, coefs=[other])

        max_length = max(len(self.coefs), len(other.coefs))
        coefs1 = [0] * (max_length - len(self.coefs)) + self.coefs 
        coefs2 = [0] * (max_length - len(other.coefs)) + other.coefs
        
        new_coefs = [a - b for a, b in zip(coefs1, coefs2)]
        return Poly(n=len(new_coefs)-1, coefs=new_coefs)


    def __rsub__(self, other):
        return Poly(n=0, coefs=[other]) - self





    def __mul__(self, other):
        """ multiplica polinomios, en other pones el polinomio por el que queres multiplicar"""
        """ devuelve un polinomio cuyo grado va a ser la suma de los grados de los dos poli que quieor multiplicar """
        if isinstance(other, (int, float)):
            new_coefs = [coef * other for coef in self.coefs] 
            return Poly(n=len(self.coefs)-1, coefs=new_coefs)
        
        if isinstance(other, Poly):
            grado = self.n + other.n
            new_coefs = [0] * (grado + 1)
            for i, coef1 in enumerate(self.coefs):
                for j, coef2 in enumerate(other.coefs):
                    new_coefs[i + j] += coef1 * coef2 

            return Poly(n=grado, coefs=new_coefs)




    def __rmul__(self, other):
        return self * other              




    def __floordiv__(self, other):
        """ divide polinomios, en other pones el polinomio por el que queres dividir """
        """ devuelve  """
        if isinstance(other, (int, float)):
           # División entre un polinomio y un número
           new_coefs = [coef / other for coef in self.coefs]
           return Poly(n=self.n, coefs=new_coefs)
       
        if isinstance(other, Poly):
            resultado = []
            dividendo = self.coefs[:]
            divisor = other.coefs[:]

            def division_recu(dividendo, divisor, resultado):
                if len(dividendo) < len(divisor):
                    return Poly(n=len(resultado)-1, coefs=resultado)        

                coef = dividendo[0] / divisor[0]                     
                resultado.append(coef)
                num_a_restar = [coef * d for d in divisor] + [0] * (len(dividendo) - len(divisor)) 
                nuevo_dividendo = [a - b for a, b in zip(dividendo, num_a_restar)]

                while nuevo_dividendo and nuevo_dividendo[0] == 0:
                    nuevo_dividendo.pop(0)

                if not nuevo_dividendo:
                    return Poly(n=len(resultado)-1, coefs=resultado)

                return division_recu(nuevo_dividendo, divisor, resultado)

            return division_recu(dividendo, divisor, resultado)
        
        raise TypeError("El divisor debe ser un polinomio.")





    def __rfloordiv__(self, other):
        return Poly(n=0, coefs=[other]) // self 





    def __mod__(self, other):
        """ Devuelve el resto de la división entre polinomios """
        if isinstance(other, Poly):
            cociente = self // other  # Calculamos el cociente
            producto = other * cociente  # Multiplicamos divisor por el cociente
            resto = Poly(n=len(self.coefs) - 1, coefs=self.coefs) - producto  # Resto = Dividendo - (Cociente * Divisor)
            return resto





    def findroot(self, x0, tol=1e-8, max_iter=100):
        """ devuelve una raiz si es que la tiene"""
        def derivada():
            coefs_derivada = []
            grado = self.n
            for coef in self.coefs:
                coefs_derivada.append(coef * grado)
                grado -= 1
            return Poly(len(coefs_derivada) - 1, coefs_derivada)
    
        f = self
        f_prime = derivada()
        x = float(x0)
    
        for _ in range(max_iter):
            fx = f(x)
            fpx = f_prime(x)
            if fpx == 0:
                raise ZeroDivisionError("La derivada es cero. No se puede continuar.")
            x_nuevo = x - fx / fpx
            if abs(x_nuevo - x) < tol:
                return round(x_nuevo, 6)
            x = x_nuevo
    
        raise ValueError("No se encontró una raíz en el número máximo de iteraciones.")
   
        
    def findroots_biseccion(self, intervalo_inicio=-1000, intervalo_fin=1000, cantidad_subintervalos=2000, tolerancia=1e-8):
        """Encuentra todas las raíces reales del polinomio, con su multiplicidad.
        Devuelve una lista de tuplas (raíz, multiplicidad) y el polinomio residual."""
        lista_de_raices = []
        polinomio_actual = self  # copiamos el polinomio original para ir dividiendo
        puntos = [intervalo_inicio + i * (intervalo_fin - intervalo_inicio) / cantidad_subintervalos for i in range(cantidad_subintervalos + 1)]
    
        for i in range(cantidad_subintervalos):
            x_izq = puntos[i]
            x_der = puntos[i + 1]
            valor_izq = polinomio_actual(x_izq)
            valor_der = polinomio_actual(x_der)
    
            if valor_izq * valor_der < 0:
                try:
                    raiz_encontrada = polinomio_actual.biseccion(x_izq, x_der, tol=tolerancia)
    
                    # Verificar que no sea una raíz ya encontrada (muy cercana)
                    ya_encontrada = any(abs(raiz_encontrada - raiz_existente[0]) < 1e-6 for raiz_existente in lista_de_raices)
                    if ya_encontrada:
                        continue
    
                    # Contar la multiplicidad
                    multiplicidad = 0
                    monomio_raiz = Poly(1, [1, -raiz_encontrada])
    
                    while True:
                        resto = (polinomio_actual % monomio_raiz).coefs
                        if all(abs(coef) < 1e-8 for coef in resto):
                            polinomio_actual = polinomio_actual // monomio_raiz
                            multiplicidad += 1
                        else:
                            break
    
                    lista_de_raices.append((raiz_encontrada, multiplicidad))
    
                except Exception:
                    continue
    
        return lista_de_raices, polinomio_actual

    
    def findroots_newton(self):
        """devuelve las raíces del poli con su multiplicicdad y ademas devuelve los coefs del poli residual en caso de que lo haya"""
        raices = []
        poli = self
    
        candidatos = list(range(-10000, 10000))
        i = 0
    
        while poli.n > 0 and i < len(candidatos):
            x0 = candidatos[i]
            i += 1
    
            raiz_encontrada = False
            raiz_posible = None
    
            # Intentamos encontrar una raíz desde x0
            resultado = None
            try:
                resultado = poli.findroot(x0)
            except Exception:
                resultado = None
    
            if resultado is not None:
                # Chequeamos que no esté repetida
                ya_esta = any(abs(resultado - r[0]) < 1e-6 for r in raices)
                if not ya_esta:
                    raiz_encontrada = True
                    raiz_posible = resultado
    
            if raiz_encontrada:
                monomio = Poly(1, [1, -raiz_posible])
                multiplicidad = 0
    
                while True:
                    resto = (poli % monomio).coefs
                    if all(abs(c) < 1e-8 for c in resto):
                        poli = poli // monomio
                        multiplicidad += 1
                    else:
                        break
    
                raices.append((raiz_posible, multiplicidad))
                i = 0  # Reiniciamos para buscar nuevas raíces desde -20 a 20 otra vez
    
        return raices, poli.coefs
    
    
    
    
    
        
    def factorize(self):
        """ devuelve la expresion del polinomio utilizando findroots para que le de las raices con su multiplicidad """ 
        """Devuelve e imprime la expresión factorizada del polinomio con raíces reales y multiplicidades"""
        expresion_poly = ""
        lista_raices, coef_residual = self.findroots_newton()
        
        for raiz, multiplicidad in lista_raices:
            # Formateo del término según el valor de la raíz
            if abs(raiz) < 1e-8:
                termino = "x"
            elif raiz < 0:
                termino = f"(x + {abs(raiz):.4g})"
            else:
                termino = f"(x - {raiz:.4g})"
    
            # Multiplicidad
            if multiplicidad == 1:
                expresion_poly += termino
            else:
                expresion_poly += f"{termino}^{multiplicidad}"
    
        # Construcción del residual
        if not (len(coef_residual) == 1 and abs(coef_residual[0] - 1) < 1e-8):
            # Si el residual no es 1, se agrega como polinomio
            residual = Poly(len(coef_residual) - 1, coef_residual)
            expresion_poly += f" · ({residual})"
    
        print(" Factorización del polinomio:")
        print(f"p(x) = {expresion_poly}")
        
        return expresion_poly

      

    def calc_derivada(self):
        derivada = []
        grado = len(self.coefs) - 1
    
        for coef in self.coefs:
            derivada.append(coef * grado)
            grado -= 1
    
        while derivada and derivada[-1] == 0:
            derivada.pop()
    
        return Poly(n=len(derivada) - 1, coefs=derivada)



    def fprime(self,k ,x0 = None):
        """ Te devuelve la derivada de self, ejemplo: p.fprime"""
        
       
        poly = self
        for i in range(k): 
          poly = poly.calc_derivada()
        
        if x0 == None:
            return poly
        else:
            valor = poly(x0)
            print(valor)
            return valor 
 

 
        
 





        
        
        
        
        