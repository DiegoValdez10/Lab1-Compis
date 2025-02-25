"""
Universidad del Valle de Guatemala
Teoria de la computación
"""

from graphviz import Digraph
from ShuntingYard import Node
from Minimizado import AFD

class AFD_Directo:
    def __init__(self):
        self.anulable = {}
        self.primera_pos = {}
        self.ultima_pos = {}
        self.siguiente_pos = {}
        self.posiciones_hojas = {}
        self.simbolos_posiciones = {}  
        self.contador_posicion = 1
        self.alfabeto = set()



    def marcar_posiciones_hojas(self, nodo):
        """Marca las posiciones de las hojas y guarda el símbolo correspondiente"""
        if nodo is None:
            return
        
        if nodo.value.isalnum() or nodo.value == "#":
            self.posiciones_hojas[nodo] = self.contador_posicion
            self.simbolos_posiciones[self.contador_posicion] = nodo.value
            self.contador_posicion += 1
            if nodo.value != "#":
                self.alfabeto.add(nodo.value)
        
        self.marcar_posiciones_hojas(nodo.left)
        self.marcar_posiciones_hojas(nodo.right)

    def calcular_anulable(self, nodo):
        """Calcula si un nodo es anulable"""
        if nodo is None:
            return False

        resultado = False
        if nodo.value == "𝜀":
            resultado = True
        elif nodo.value.isalnum() or nodo.value == "#":
            resultado = False
        elif nodo.value == "|":
            resultado = self.calcular_anulable(nodo.left) or self.calcular_anulable(nodo.right)
        elif nodo.value == ".":
            resultado = self.calcular_anulable(nodo.left) and self.calcular_anulable(nodo.right)
        elif nodo.value in ["*", "?", "+"]:
            resultado = True if nodo.value in ["*", "?"] else self.calcular_anulable(nodo.right)

        self.anulable[nodo] = resultado
        return resultado

    def calcular_primera_pos(self, nodo):
        if nodo is None:
            return set()

        if nodo in self.primera_pos:
            return self.primera_pos[nodo]

        resultado = set()
        if nodo in self.posiciones_hojas:
            resultado = {self.posiciones_hojas[nodo]}
        elif nodo.value == "|":
            resultado = self.calcular_primera_pos(nodo.left) | self.calcular_primera_pos(nodo.right)
        elif nodo.value == ".":
            if self.anulable.get(nodo.left, False):
                resultado = self.calcular_primera_pos(nodo.left) | self.calcular_primera_pos(nodo.right)
            else:
                resultado = self.calcular_primera_pos(nodo.left)
        elif nodo.value in ["*", "?", "+"]:
            resultado = self.calcular_primera_pos(nodo.right)

        self.primera_pos[nodo] = resultado
        return resultado

    def calcular_ultima_pos(self, nodo):
        if nodo is None:
            return set()

        if nodo in self.ultima_pos:
            return self.ultima_pos[nodo]

        resultado = set()
        if nodo in self.posiciones_hojas:
            resultado = {self.posiciones_hojas[nodo]}
        elif nodo.value == "|":
            resultado = self.calcular_ultima_pos(nodo.left) | self.calcular_ultima_pos(nodo.right)
        elif nodo.value == ".":
            if self.anulable.get(nodo.right, False):
                resultado = self.calcular_ultima_pos(nodo.left) | self.calcular_ultima_pos(nodo.right)
            else:
                resultado = self.calcular_ultima_pos(nodo.right)
        elif nodo.value in ["*", "?", "+"]:
            resultado = self.calcular_ultima_pos(nodo.right)

        self.ultima_pos[nodo] = resultado
        return resultado

    def calcular_siguiente_pos(self, nodo):

        if nodo is None:
            return

        if nodo.value == ".":
            ultima_pos_izq = self.calcular_ultima_pos(nodo.left)
            primera_pos_der = self.calcular_primera_pos(nodo.right)
            for pos in ultima_pos_izq:
                if pos not in self.siguiente_pos:
                    self.siguiente_pos[pos] = set()
                self.siguiente_pos[pos].update(primera_pos_der)


        elif nodo.value in ["*", "+"]:
            ultima_pos = self.calcular_ultima_pos(nodo.right)
            primera_pos = self.calcular_primera_pos(nodo.right)
            for pos in ultima_pos:
                if pos not in self.siguiente_pos:
                    self.siguiente_pos[pos] = set()
                self.siguiente_pos[pos].update(primera_pos)


        self.calcular_siguiente_pos(nodo.left)
        self.calcular_siguiente_pos(nodo.right)

    def mover_a(self, estado, simbolo):
        nuevo_estado = set()
        for pos in estado:
            if (pos in self.siguiente_pos and 
                self.simbolos_posiciones.get(pos) == simbolo):
                nuevo_estado.update(self.siguiente_pos[pos])
        return frozenset(nuevo_estado)

    def construir_afd(self, ast):

        self.alfabeto = set()
        self.posiciones_hojas = {}
        self.simbolos_posiciones = {}
        self.siguiente_pos = {}
        self.primera_pos = {}
        self.ultima_pos = {}
        self.anulable = {}
        self.contador_posicion = 1

        ast_concatenado = Node(".")
        ast_concatenado.left = ast
        ast_concatenado.right = Node("#")

        self.marcar_posiciones_hojas(ast_concatenado)
        self.calcular_anulable(ast_concatenado)
        self.calcular_primera_pos(ast_concatenado)
        self.calcular_ultima_pos(ast_concatenado)
        self.calcular_siguiente_pos(ast_concatenado)

        estado_inicial = frozenset(self.primera_pos[ast_concatenado])
        estados_por_procesar = [estado_inicial]
        estados_procesados = set()
        nombres_estados = {estado_inicial: "q0"}
        transiciones = {}
        estados_finales = set()
        contador_estado = 1
        
        while estados_por_procesar:
            estado_actual = estados_por_procesar.pop(0)
            if estado_actual in estados_procesados:
                continue
                
            estados_procesados.add(estado_actual)
            nombre_actual = nombres_estados[estado_actual]
            transiciones[nombre_actual] = {}
            

            if self.contador_posicion - 1 in estado_actual:
                estados_finales.add(nombre_actual)
            

            for simbolo in self.alfabeto:
                siguiente_estado = set()
                for pos in estado_actual:
                    if (pos in self.siguiente_pos and 
                        self.simbolos_posiciones.get(pos) == simbolo):
                        siguiente_estado.update(self.siguiente_pos[pos])
                
                if siguiente_estado:
                    siguiente_estado = frozenset(siguiente_estado)
                    if siguiente_estado not in nombres_estados:
                        nombres_estados[siguiente_estado] = f"q{contador_estado}"
                        contador_estado += 1
                        estados_por_procesar.append(siguiente_estado)
                    
                    transiciones[nombre_actual][simbolo] = nombres_estados[siguiente_estado]
        
        return AFD(
            estados=list(nombres_estados.values()),
            alfabeto=list(self.alfabeto),
            transiciones=transiciones,
            estado_inicial="q0",
            estados_finales=list(estados_finales)
        )