"""
Universidad del Valle de Guatemala

Teoria de la computación

Diego Valdez - 21328
Sebastian Estrada - 21405
"""

from graphviz import Digraph

class NFA:
    def __init__(self, start_state, accept_state, transitions):
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = transitions
        self.alfabeto = {symbol for (from_state, symbol) in transitions.keys() if symbol != 'ε'}

    def _obtener_alfabeto(self):
        """
        Extrae el alfabeto del NFA basado en las transiciones.
        """
        alfabeto = set()
        for (estado, simbolo), destinos in self.transitions.items():
            if simbolo != 'ε':  
                alfabeto.add(simbolo)
        return alfabeto

    def get_epsilon_transitions(self, state):
        return self.transitions.get((state, 'ε'), set())

    def get_transitions(self, state, symbol):
        return self.transitions.get((state, symbol), set())

    def get_accept_states(self):

        return {self.accept_state}


class ThompsonNFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.accept_state = None

    def create_state(self):
        state = len(self.states)
        self.states.add(state)
        return state
    
    def drop_transition(self, from_state, symbol, to_state):
        if (from_state, symbol) in self.transitions:
            self.transitions[(from_state, symbol)].remove(to_state)
            if len(self.transitions[(from_state, symbol)]) == 0:
                del self.transitions[(from_state, symbol)]

    def add_transition(self, from_state, symbol, to_state):
        if (from_state, symbol) not in self.transitions:
            self.transitions[(from_state, symbol)] = set()
        self.transitions[(from_state, symbol)].add(to_state)

    def create_basic_nfa(self, symbol):
        start_state = self.create_state()
        accept_state = self.create_state()
        self.add_transition(start_state, symbol, accept_state)
        return NFA(start_state, accept_state, self.transitions)

    def create_kleene_star_nfa(self, sub_nfa):
        start_state = self.create_state()
        accept_state = self.create_state()
        self.add_transition(start_state, 'ε', sub_nfa.start_state)
        self.add_transition(start_state, 'ε', accept_state)
        self.add_transition(sub_nfa.accept_state, 'ε', sub_nfa.start_state)
        self.add_transition(sub_nfa.accept_state, 'ε', accept_state)
        return NFA(start_state, accept_state, self.transitions)

    def create_plus_nfa(self, sub_nfa):
        start_state = self.create_state()  
        accept_state = self.create_state()  

        if (sub_nfa.start_state, 'ε') in self.transitions and sub_nfa.accept_state in self.transitions[(sub_nfa.start_state, 'ε')]:
            self.drop_transition(sub_nfa.start_state, 'ε', sub_nfa.accept_state)

        self.add_transition(start_state, 'ε', sub_nfa.start_state)


        self.add_transition(sub_nfa.accept_state, 'ε', accept_state)


        self.add_transition(sub_nfa.accept_state, 'ε', sub_nfa.start_state)

        return NFA(start_state, accept_state, self.transitions)


    def create_concatenation_nfa(self, left_nfa, right_nfa):
        self.add_transition(left_nfa.accept_state, 'ε', right_nfa.start_state)
        return NFA(left_nfa.start_state, right_nfa.accept_state, self.transitions)

    def create_union_nfa(self, left_nfa, right_nfa):
        start_state = self.create_state()
        accept_state = self.create_state()
        self.add_transition(start_state, 'ε', left_nfa.start_state)
        self.add_transition(start_state, 'ε', right_nfa.start_state)
        self.add_transition(left_nfa.accept_state, 'ε', accept_state)
        self.add_transition(right_nfa.accept_state, 'ε', accept_state)
        return NFA(start_state, accept_state, self.transitions)

    def create_question_nfa(self, sub_nfa):
        start_state = self.create_state()
        accept_state = self.create_state()
        self.add_transition(start_state, 'ε', sub_nfa.start_state)
        self.add_transition(start_state, 'ε', accept_state)
        self.add_transition(sub_nfa.accept_state, 'ε', accept_state)
        return NFA(start_state, accept_state, self.transitions)

    def thompson_from_ast(self, node):
        if node is None:
            return None

        if node.value.isalnum() or node.value == '𝜀':
            return self.create_basic_nfa(node.value)

        if node.value in ['*', '+', '?']:
            sub_nfa = self.thompson_from_ast(node.right)
            if node.value == '*':
                return self.create_kleene_star_nfa(sub_nfa)
            elif node.value == '+':
                return self.create_plus_nfa(sub_nfa)
            elif node.value == '?':
                return self.create_question_nfa(sub_nfa)
        

        if node.value == '.':
            left_nfa = self.thompson_from_ast(node.left)
            right_nfa = self.thompson_from_ast(node.right)
            return self.create_concatenation_nfa(left_nfa, right_nfa)
        

        if node.value == '|':
            left_nfa = self.thompson_from_ast(node.left)
            right_nfa = self.thompson_from_ast(node.right)
            return self.create_union_nfa(left_nfa, right_nfa)
        
        raise ValueError(f"Operador no reconocido en el AST: {node.value}")
    
    def visualize_nfa(self, nfa, expression):
        dot = Digraph()
        dot.attr(rankdir='LR')

        with dot.subgraph() as s:
            s.attr(rank='same', label=expression)
            s.node('start', shape='point')
            s.edge('start', str(nfa.start_state))


        all_states = set()
        for (from_state, _), to_states in nfa.transitions.items():
            all_states.add(from_state)
            all_states.update(to_states)
        for state in all_states:
            if state == nfa.start_state:
                dot.node(str(state), shape='doublecircle', color='green', label='Start')
            elif state == nfa.accept_state:
                dot.node(str(state), shape='doublecircle', color='red', label='Accept')
            else:
                dot.node(str(state), shape='circle')

        for (from_state, symbol), to_states in nfa.transitions.items():
            if symbol == 'ε':
                for to_state in to_states:
                    dot.edge(str(from_state), str(to_state), label='ε', style='dashed', color='blue')
            else:
                for to_state in to_states:
                    dot.edge(str(from_state), str(to_state), label=symbol)

        return dot