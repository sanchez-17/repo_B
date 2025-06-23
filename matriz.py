#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:37:18 2025

@author: bautistacenci
"""

# - Se agregaron test : El inversamethod paso todos los tests, se le cambio el nombre a resolversistema
import numpy as np
# j = fila 
# k columnas
class Matriz(object):

    
    def __init__(self, elems=[], rows = 0, cols = 0 , by_row=True):
        self.cols = cols
        self.rows = rows
        self.by_row = by_row
        self.elems = elems  # lista de elementos

    def copia(self):
        copia_elems = [e for e in self.elems]  # Si es lista plana
        return Matriz(copia_elems, self.rows, self.cols, self.by_row)

    def __str__(self):
        """Devuelve una representación en cadena de la matriz, con formato limpio."""
        matriz_str = ""
        for i in range(self.rows):
            fila = self.elems[i * self.cols: (i + 1) * self.cols]
            # Convierte cada fila a un string y lo alinea correctamente sin barras
            fila_str = "   ".join(f"{elem:8.3f}" for elem in fila)  # Alineación y 3 decimales
            matriz_str += f"[ {fila_str} ]\n"
        return matriz_str    

    def get_pos(self, j, k):
        """Devuelve el índice en la lista del elemento en la coordenada (j, k)"""
        if self.by_row == True:
            return j * self.cols + k
        else:
            return k * self.rows + j
    



    def get_coords(self, m):
        """Devuelve las coordenadas (k, j) del número que tiene índice m en la lista"""
        if self.by_row:
            return (m // self.cols, m % self.cols)
        else:
            return (m % self.rows, m // self.rows)



    def switch(self):
        """Devuelve una nueva matriz con la misma información, pero con el orden cambiado (filas <-> columnas)"""
        nueva_lista = []

        if self.by_row:
            # pasar de filas a columnas
            for j in range(self.cols):
                for k in range(self.rows):
                    indice = k * self.cols + j
                    nueva_lista.append(self.elems[indice])
            return Matriz(nueva_lista, cols=self.rows, rows=self.cols, by_row=False)

        else:
            # pasar de columnas a filas
            for k in range(self.rows):
                for j in range(self.cols):
                    indice = j * self.rows + k
                    nueva_lista.append(self.elems[indice])
            return Matriz(nueva_lista, cols=self.rows, rows=self.cols, by_row=True)



    def get_col(self, k): 
        """devuelve el contenido de la columna k (no los índices)"""
        cont_columna = []
        for i in range(self.rows):
            cont_columna.append(self.elems[self.get_pos(i, k)])
        return cont_columna 
    
    def get_row(self, j):
        """devuelve el contenido de la fila k (no los índices)"""
        cont_fila = []
        for i in range(self.cols):
            cont_fila.append(self.elems[self.get_pos(j, i)])
        return cont_fila
    
   
    def prod(self, B):
        """Devuelve el producto de dos matrices self * B"""
        assert self.cols == B.rows, "Las dimensiones no son compatibles para la multiplicación."
    
        elems_res = []
    
        for i in range(self.rows):
            for j in range(B.cols):
                suma = 0
                for k in range(self.cols):
                    a = self.elems[self.get_pos(i, k)]
                    b = B.elems[B.get_pos(k, j)]
                    suma += a * b
                elems_res.append(suma)

        return Matriz(elems_res, self.rows, B.cols, by_row=True)

    def rprod(self, B):
        """Producto a derecha: self * B (puede ser matriz o escalar)"""
        if isinstance(B, Matriz):
            return self.prod(B)  # Ahora solo pasas B, no self
        elif isinstance(B, (int, float)):
            nuevos_elems = [x * B for x in self.elems]
            return Matriz(nuevos_elems, self.rows, self.cols, self.by_row)
        else:
            raise TypeError("B debe ser un escalar o un objeto de tipo Matriz")

    def lprod(self, B):
        """Producto a izquierda: B * self (puede ser matriz o escalar)"""
        if isinstance(B, Matriz):
            return self.prod(B)  # Ahora solo pasas B, no self
        elif isinstance(B, (int, float)):
            nuevos_elems = [B * x for x in self.elems]
            return Matriz(nuevos_elems, self.rows, self.cols, self.by_row)
        else:
            raise TypeError("B debe ser un escalar o un objeto de tipo Matriz")



    def get_col_by_prod(self, k):
        """Devuelve la multiplicación para llegar a la columna k, mediante matriz * vector"""
    
        # Vector columna con un 1 en la posición k
        vector = []
        for num in range(self.cols):
            if num != k:
                vector.append(0)
            else:
                vector.append(1)
    
        # Convertimos el vector en una matriz columna (cols x 1)
        vector_col = Matriz(vector, self.cols, 1, by_row=True)
    
        print(f"prod (matriz * vector): {vector}")
        resultado = self.rprod(vector_col)
    
        return resultado.elems  # Lista con la columna k

    def get_row_by_prod(self, j):        
        """Devuelve la multiplicación para llegar a esa fila mediante vector * matriz.
        Devuelve la fila como una lista (no como matriz)"""
    
        # Vector fila con un 1 en la posición j
        vector = []
        for num in range(self.rows):
            if num != j:
                vector.append(0)
            else:
                vector.append(1)
    
        # Convertimos el vector en una matriz fila (1 x rows)
        vector_fila = Matriz(vector, 1, self.rows, by_row=True)
    
        print(f"prod (vector: {vector} * matriz)")
        resultado = vector_fila.rprod(self)
    
        return resultado.elems  # Lista con la fila j



    def get_elem(self, j, k):
        indice_de_elem = self.get_pos(j, k)
        elemento = self.elems[indice_de_elem]
        return elemento 
    
    

    def sub_matrix(self, row_list=[], cols_list=[]):
        """ Devuelve la submatriz que está en las filas y columnas dadas """
        sub_elem = []
        for j in row_list:
            for k in cols_list:
                elemento = self.elems[self.get_pos(j, k)]
                sub_elem.append(elemento)
    
        filas = len(row_list)
        columnas = len(cols_list)
        return Matriz(sub_elem, filas, columnas)
    
    
    def del_row(self, j):
        """Devuelve una nueva matriz eliminando la fila j (considerando by_row o no)"""
        elems_nuevos = []
    
        if self.by_row:
            for fila in range(self.rows):
                if fila != j:
                    for col in range(self.cols):
                        elems_nuevos.append(self.elems[self.get_pos(fila, col)])
        else:
            # by_row = False → hay que sacar el j-ésimo elemento de cada columna
            for col in range(self.cols):
                for fila in range(self.rows):
                    if fila != j:
                        elems_nuevos.append(self.elems[self.get_pos(fila, col)])
        
        return Matriz(elems_nuevos, self.rows - 1, self.cols, self.by_row)
 
            
            
    def del_col(self,k):
        
        elems_nuevos = []
        if self.by_row == True:
            
            for fila in range(self.rows):
                for col in range(self.cols):
                    if col != k:
                        elems_nuevos.append(self.elems[self.get_pos(fila, col)])
            matriz = Matriz(elems_nuevos,self.rows, self.cols-1, self.by_row)            
            return matriz
        else:
             for col in range(self.cols):
                 for fila in range(self.rows):
                     if col != k:
                         elems_nuevos.append(self.elems[self.get_pos(fila, col)])
             matriz = Matriz(elems_nuevos, self.rows, self.cols-1 ,self.by_row)            
             return matriz

    
    def swap_rows(self, j, k):
        """Devuelve una nueva matriz con las filas j y k intercambiadas"""
        nuevos_elems = self.elems.copy()
    
        if self.by_row:
            for col in range(self.cols):
                indice_j = self.get_pos(j, col)
                indice_k = self.get_pos(k, col)
                nuevos_elems[indice_j], nuevos_elems[indice_k] = nuevos_elems[indice_k], nuevos_elems[indice_j]
        else:
            for col in range(self.cols):
                indice_j = self.get_pos(j, col)
                indice_k = self.get_pos(k, col)
                nuevos_elems[indice_j], nuevos_elems[indice_k] = nuevos_elems[indice_k], nuevos_elems[indice_j]

        return Matriz(nuevos_elems, self.rows, self.cols, self.by_row)
        
    
    
    def swap_cols(self, l, m):
        """Devuelve una nueva matriz con las columnas l y m intercambiadas"""
        nuevos_elems = self.elems.copy()
    
        if self.by_row:
            for fila in range(self.rows):
                indice_l = self.get_pos(fila, l)
                indice_m = self.get_pos(fila, m)
                nuevos_elems[indice_l], nuevos_elems[indice_m] = nuevos_elems[indice_m], nuevos_elems[indice_l]
        else:
            for fila in range(self.rows):
                indice_l = self.get_pos(fila, l)
                indice_m = self.get_pos(fila, m)
                nuevos_elems[indice_l], nuevos_elems[indice_m] = nuevos_elems[indice_m], nuevos_elems[indice_l]
    
        return Matriz(nuevos_elems, self.rows, self.cols, self.by_row)
        
    

 
    def scale_row(self,j,x):
        """ multiplica a la fila por un numero x que le mandes """
        nueva_matriz = []
        if self.by_row:
            
    
            for fila in range(self.rows):
                for columna in range(self.cols):
                    valor = self.get_elem(fila, columna)
                    if fila == j:
                        valor *= x
                    nueva_matriz.append(valor)

         
    
        if self.by_row == False: 
            for columna in range(self.cols):
                for fila in range(self.rows):
                    valor = self.get_elem(fila, columna)
                    if fila == j:
                        valor *= x
                    nueva_matriz.append(valor)
                    
        return Matriz(elems= nueva_matriz, rows=self.rows, cols=self.cols, by_row = self.by_row)
    
    
    def scale_col(self,k,x):
        """ multiplica a la columna por un numero x que le mandes """
        
        nueva_matriz = []
        
        if self.by_row == True:
            for fila in range(self.rows):
                for columna in range(self.cols):
                    valor = self.get_elem(fila, columna)
                    if columna == k:
                        valor *= x
                    nueva_matriz.append(valor)
                    
        if self.by_row == False:
            for columna in range(self.cols):
                for fila in range(self.rows):
                    valor = self.get_elem(fila, columna)
                    if columna == k:
                        valor *= x
                    nueva_matriz.append(valor)
                    
        return Matriz(elems= nueva_matriz, rows=self.rows, cols=self.cols, by_row = self.by_row)
     
        
    def transpose (self):
        """ te da la traspuesta de la matriz """
        traspuesta = self.switch()
        traspuesta.by_row = self.by_row
        return traspuesta
        
        
    def flip_cols(self):
        nueva_matriz = []
    
        if self.by_row:
            for fila in range(self.rows):
                for columna in reversed(range(self.cols)):
                    nueva_matriz.append(self.get_elem(fila, columna))
            return Matriz(elems=nueva_matriz, rows=self.rows, cols=self.cols, by_row=True)
        
        else:
            for columna in range(self.cols):
                for fila in reversed(range(self.rows)):
                    nueva_matriz.append(self.get_elem(fila, columna))
            return Matriz(elems=nueva_matriz, rows=self.rows, cols=self.cols, by_row=False)


    def flip_rows(self):
        nueva_matriz = []
    
        if self.by_row:
            for fila in reversed(range(self.rows)):
                for columna in range(self.cols):
                    nueva_matriz.append(self.get_elem(fila, columna))
            return Matriz(elems=nueva_matriz, rows=self.rows, cols=self.cols, by_row=True)
    
        else:
            for columna in reversed(range(self.cols)):
                for fila in range(self.rows):
                    nueva_matriz.append(self.get_elem(fila, columna))
            return Matriz(elems=nueva_matriz, rows=self.rows, cols=self.cols, by_row=False)

    
    def det(self):
        """Devuelve el determinante de una matriz cuadrada usando eliminación recursiva."""
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")
        
        n = self.rows
        # Caso base 1×1
        if n == 1:
            return self.get_elem(0, 0)
        # Caso base 2×2
        if n == 2:
            return (
                self.get_elem(0, 0) * self.get_elem(1, 1)
                - self.get_elem(0, 1) * self.get_elem(1, 0)
            )

        # Expansión por la primera fila
        determinante = 0
        for j in range(n):
            cofactor = (-1) ** j
            # Obtenemos el menor eliminando fila 0 y columna j
            menor = self.del_row(0).del_col(j)
            determinante += cofactor * self.get_elem(0, j) * menor.det()

        return determinante


    def add(self, B):
        """suma la matriz mas otra que le des """
        if isinstance(B, Matriz):
            if self.rows != B.rows or self.cols != B.cols:
                raise ValueError("Las dimensiones no coinciden para la suma.")
            elems = [
                self.elems[i] + B.elems[i]
                for i in range(len(self.elems))
            ]
        else:
            elems = [x + B for x in self.elems]  # B escalar
    
        return Matriz(elems=elems, rows=self.rows, cols=self.cols, by_row=self.by_row)
    
    
    
    
    
    def sub(self, B):
        """resta la matriz por otra que le des """
        if isinstance(B, Matriz):
            if self.rows != B.rows or self.cols != B.cols:
                raise ValueError("Las dimensiones no coinciden para la resta.")
            elems = [
                self.elems[i] - B.elems[i]
                for i in range(len(self.elems))
            ]
        else:
            elems = [x - B for x in self.elems]
    
        return Matriz(elems=elems, rows=self.rows, cols=self.cols, by_row=self.by_row)
    
    def identidad(self):
        """ te devuelve la matriz identidad, tengo que poner .elems"""
        if self.rows != self.cols:
            raise ValueError("Solo se puede crear identidad desde una matriz cuadrada.")
    
        elems = []
        for i in range(self.rows):
            for j in range(self.cols):
                elems.append(1 if i == j else 0)
    
        return Matriz(elems=elems, rows=self.rows, cols=self.cols, by_row=self.by_row)

   

    def pow(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("La potencia debe ser un entero no negativo.")
        if self.rows != self.cols:
            raise ValueError("Solo se puede potenciar una matriz cuadrada.")
        
        # Caso base
        if n == 0:
            return self.identidad()
    
        resultado = self
        for _ in range(n - 1):
            resultado = resultado.rprod(self)
        
        return resultado


#
    def resolver_sistema(self, listadey): #inversametod
        """
        Resuelve el sistema Ax = y utilizando eliminación de Gauss con pivoteo parcial.
        self: matriz A (debe ser cuadrada)
        vector_y: lista con los valores del segundo miembro (y)
        """
        
        """
         #pones m.inversametod(listadey que son los reesultado, esto resuelve el sistema y te da los x)
         """
        A = self.copia()
        
        if len(listadey) != A.rows:
            raise ValueError("La longitud del vector y no coincide con la cantidad de filas de la matriz.")
        
        y = Matriz(listadey, A.rows, 1, True)
    
        n = A.rows
    
        # Paso 1: Eliminación hacia adelante con pivoteo parcial
        for i in range(n):
            # Pivoteo si el pivote es cero
            if A.get_elem(i, i) == 0:
                for k in range(i + 1, n):
                    if A.get_elem(k, i) != 0:
                        A = A.swap_rows(i, k)
                        y = y.swap_rows(i, k)
                        break
    
            pivote = A.get_elem(i, i)
    
            # Escalar fila para que el pivote sea 1
            for j in range(i, A.cols):
                pos = A.get_pos(i, j)
                A.elems[pos] /= pivote
            y.elems[y.get_pos(i, 0)] /= pivote
    
            # Hacer ceros debajo del pivote
            for f in range(i + 1, n):
                factor = A.get_elem(f, i)
                for j in range(i, A.cols):
                    pos = A.get_pos(f, j)
                    A.elems[pos] -= factor * A.get_elem(i, j)
                y.elems[y.get_pos(f, 0)] -= factor * y.get_elem(i, 0)
    
        # Paso 2: Sustitución hacia atrás
        x = [0] * n
        for i in reversed(range(n)):
            suma = 0
            for j in range(i + 1, n):
                suma += A.get_elem(i, j) * x[j]
            x[i] = y.get_elem(i, 0) - suma
        return x
        

                                
              
        

datos = [
    2, 0, 1, 3, 4,
    1, 2, 0, 1, 5,
    3, 0, 2, 2, 1,
    0, 1, 2, 2, 3,
    4, 1, 0, 5, 2
]

m = Matriz(datos, 5, 5, by_row=True)
#inversa= m.inversametod([1,2,3,4,5])
inversa= m.resolver_sistema([1,2,3,4,5])
print(inversa)