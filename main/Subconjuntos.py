
from Minimizado import AFD

class Subconjuntos:
    def __init__(self, nfa):
        self.nfa = nfa
        self.alfabeto = nfa.alfabeto

    def _cerradura_epsilon(self, estados):
        cerradura = set(estados)
        stack = list(estados)
        while stack:
            estado = stack.pop()
            for siguiente_estado in self.nfa.get_epsilon_transitions(estado):
                if siguiente_estado not in cerradura:
                    cerradura.add(siguiente_estado)
                    stack.append(siguiente_estado)
        return frozenset(cerradura)

    def _mover(self, estados, simbolo):
        mover_resultado = set()
        for estado in estados:
            mover_resultado.update(self.nfa.get_transitions(estado, simbolo))
        return frozenset(self._cerradura_epsilon(mover_resultado))

    def convertir_a_afd(self):
        estado_inicial_afd = self._cerradura_epsilon({self.nfa.start_state})
        print(f"Estado inicial del AFD: {estado_inicial_afd}")
        
        estados_dfa = [estado_inicial_afd]
        estados_no_marcados = [estado_inicial_afd]
        transiciones_dfa = {}
        estados_afd_finales = set()

        while estados_no_marcados:
            estado_actual = estados_no_marcados.pop(0)
            transiciones_dfa[estado_actual] = {}

            for simbolo in self.alfabeto:
                mover_resultado = self._mover(estado_actual, simbolo)

                if mover_resultado:
                    if mover_resultado not in estados_dfa:
                        estados_dfa.append(mover_resultado)
                        estados_no_marcados.append(mover_resultado)
                    transiciones_dfa[estado_actual][simbolo] = mover_resultado
                if self.nfa.accept_state in estado_actual:
                    estados_afd_finales.add(estado_actual)

        estado_a_string = {estado: f"S{i}" for i, estado in enumerate(estados_dfa)}
    
        transiciones_dfa_formateadas = {}
        for estado, transiciones in transiciones_dfa.items():
            estado_str = estado_a_string[estado]
            transiciones_dfa_formateadas[estado_str] = {}
            for simbolo, destino in transiciones.items():
                transiciones_dfa_formateadas[estado_str][simbolo] = estado_a_string[destino]


        return AFD(
            estados=list(estado_a_string.values()),
            alfabeto=list(self.alfabeto),
            transiciones=transiciones_dfa_formateadas,
            estado_inicial=estado_a_string[estado_inicial_afd],
            estados_finales=[estado_a_string[estado] for estado in estados_afd_finales]
        )