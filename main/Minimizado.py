from graphviz import Digraph

class AFD:
    def __init__(self, estados=None, alfabeto=None, transiciones=None, estado_inicial=None, estados_finales=None):
        self.estados = estados if estados is not None else []
        self.alfabeto = alfabeto if alfabeto is not None else []
        self.transiciones = transiciones if transiciones is not None else {}
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales if estados_finales is not None else []

    def _obtener_estados_alcanzables(self):
        visitados = set()
        por_visitar = [self.estado_inicial]
        
        while por_visitar:
            estado = por_visitar.pop(0)
            if estado not in visitados:
                visitados.add(estado)
                for simbolo in self.alfabeto:
                    siguiente = self.transiciones.get(estado, {}).get(simbolo)
                    if siguiente and siguiente not in visitados:
                        por_visitar.append(siguiente)
                        
        print("\n=== Estados alcanzables ===")
        print(f"Estados alcanzables desde {self.estado_inicial}: {visitados}")
        return visitados

    def _obtener_grupo_estado(self, estado, particiones):
        """Obtiene el índice del grupo al que pertenece un estado"""
        for i, grupo in enumerate(particiones):
            if estado in grupo:
                return i
        return None

    def _son_estados_distinguibles(self, estado1, estado2, P):
        """
        Determina si dos estados son distinguibles basándose en sus transiciones
        y el comportamiento del autómata
        """
        # Si uno es final y el otro no, son distinguibles
        if (estado1 in self.estados_finales) != (estado2 in self.estados_finales):
            print(f"Estados {estado1} y {estado2} son distinguibles por ser/no ser finales")
            return True

        # Para cada símbolo del alfabeto
        for simbolo in self.alfabeto:
            dest1 = self.transiciones.get(estado1, {}).get(simbolo)
            dest2 = self.transiciones.get(estado2, {}).get(simbolo)

            # Si uno tiene transición y el otro no
            if (dest1 is None) != (dest2 is None):
                print(f"Estados {estado1} y {estado2} son distinguibles por transición con {simbolo}")
                return True

            # Si ambos tienen transiciones
            if dest1 is not None and dest2 is not None:
                # Si van a diferentes grupos
                dest1_grupo = None
                dest2_grupo = None
                for i, grupo in enumerate(P):
                    if dest1 in grupo:
                        dest1_grupo = i
                    if dest2 in grupo:
                        dest2_grupo = i
                    if dest1_grupo is not None and dest2_grupo is not None:
                        break

                if dest1_grupo != dest2_grupo:
                    print(f"Estados {estado1} y {estado2} son distinguibles por destinos diferentes con {simbolo}")
                    return True

        print(f"Estados {estado1} y {estado2} NO son distinguibles")
        return False

    def _encontrar_equivalentes(self, estado, estados, P):
        """
        Encuentra todos los estados equivalentes a un estado dado
        """
        equivalentes = {estado}
        for otro_estado in estados:
            if otro_estado != estado and not self._son_estados_distinguibles(estado, otro_estado, P):
                equivalentes.add(otro_estado)
        return equivalentes

    def minimizacion(self):
        print("\n=== Iniciando minimización del AFD ===")
        print(f"Estados iniciales: {self.estados}")
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados finales: {self.estados_finales}")
        print("Transiciones iniciales:")
        for estado, trans in self.transiciones.items():
            print(f"  Desde {estado}: {trans}")

        # Paso 1: Obtener estados alcanzables
        estados_alcanzables = self._obtener_estados_alcanzables()
        
        # Paso 2: Partición inicial (estados finales y no finales)
        P = [
            {estado for estado in estados_alcanzables if estado in self.estados_finales},
            {estado for estado in estados_alcanzables if estado not in self.estados_finales}
        ]
        P = [grupo for grupo in P if grupo]
        
        print("\n=== Partición inicial ===")
        print(f"Grupos iniciales: {P}")
        
        while True:
            nuevos_grupos = []
            cambio = False
            
            for grupo in P:
                if len(grupo) <= 1:
                    nuevos_grupos.append(grupo)
                    continue
                    
                # Tomar un estado como representante
                estados_restantes = grupo.copy()
                while estados_restantes:
                    estado = estados_restantes.pop()
                    equivalentes = self._encontrar_equivalentes(estado, estados_restantes, P)
                    
                    # Crear nuevo grupo con estado y sus equivalentes
                    nuevo_grupo = {estado} | equivalentes
                    nuevos_grupos.append(nuevo_grupo)
                    
                    # Remover estados equivalentes de estados_restantes
                    estados_restantes -= equivalentes
                    
                if len(nuevos_grupos) > len(P):
                    cambio = True
            
            if not cambio:
                break
                
            P = nuevos_grupos

        # Crear el AFD minimizado
        mapeo_estados = {}
        for i, grupo in enumerate(P):
            nuevo_estado = f"q{i}"
            for estado in grupo:
                mapeo_estados[estado] = nuevo_estado

        nuevas_transiciones = {}
        for grupo in P:
            estado_repr = next(iter(grupo))
            nuevo_estado = mapeo_estados[estado_repr]
            nuevas_transiciones[nuevo_estado] = {}
            
            if estado_repr in self.transiciones:
                for simbolo, destino in self.transiciones[estado_repr].items():
                    nuevas_transiciones[nuevo_estado][simbolo] = mapeo_estados[destino]

        nuevo_inicial = mapeo_estados[self.estado_inicial]
        nuevos_finales = sorted({mapeo_estados[estado] for estado in self.estados_finales})

        # Imprimir información de diagnóstico
        print("\n=== Grupos finales ===")
        for i, grupo in enumerate(P):
            print(f"Grupo {i}: {grupo}")
        
        print("\n=== Mapeo de estados ===")
        print("Mapeo:", mapeo_estados)
        
        afd_min = AFD(
            estados=sorted(set(mapeo_estados.values())),
            alfabeto=self.alfabeto,
            transiciones=nuevas_transiciones,
            estado_inicial=nuevo_inicial,
            estados_finales=nuevos_finales
        )
        
        print("\n=== AFD Minimizado ===")
        print(f"Estados: {afd_min.estados}")
        print(f"Estado inicial: {afd_min.estado_inicial}")
        print(f"Estados finales: {afd_min.estados_finales}")
        print("Transiciones:")
        for estado, trans in afd_min.transiciones.items():
            print(f"  Desde {estado}: {trans}")
        
        return afd_min

    def visualizar(self, titulo="AFD"):
        dot = Digraph()
        dot.attr(rankdir='LR')
        dot.node('', shape='none')  # Estado inicial invisible

        for estado in self.estados:
            if estado in self.estados_finales:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado, shape='circle')
            
            if estado == self.estado_inicial:
                dot.edge('', estado)

        for estado_origen, transiciones in self.transiciones.items():
            for simbolo, estado_destino in transiciones.items():
                dot.edge(estado_origen, estado_destino, label=simbolo)

        dot.attr(label=titulo)
        return dot

    def simular(self, cadena):
        if not self.estados or not self.estado_inicial:
            return False

        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            if estado_actual not in self.transiciones or simbolo not in self.transiciones[estado_actual]:
                return False
            estado_actual = self.transiciones[estado_actual][simbolo]

        return estado_actual in self.estados_finales