class NFA_Simulator:
    def __init__(self, nfa):
        self.nfa = nfa  

        if not hasattr(self.nfa, 'estado_inicial'):
            raise AttributeError("El objeto NFA/AFD debe tener un atributo 'estado_inicial'")
        if not hasattr(self.nfa, 'estados_finales'):
            raise AttributeError("El objeto NFA/AFD debe tener un atributo 'estados_finales'")
        if not hasattr(self.nfa, 'transiciones'):
            raise AttributeError("El objeto NFA/AFD debe tener un atributo 'transiciones'")

    def get_epsilon_transitions(self, state):

        return set()

    def get_transitions(self, state, symbol):
        next_states = set()

        if (state in self.nfa.transiciones and 
            symbol in self.nfa.transiciones[state]):

            next_states.add(self.nfa.transiciones[state][symbol])
            
        return next_states

    def epsilon_closure(self, states):

        return set(states)

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            transitions = self.get_transitions(state, symbol)
            next_states.update(transitions)
        return next_states

    def simulate(self, input_string):

        current_states = {self.nfa.estado_inicial}
        

        
        for symbol in input_string:

            
            next_states = set()
            for state in current_states:
                if (state in self.nfa.transiciones and 
                    symbol in self.nfa.transiciones[state]):
                    next_state = self.nfa.transiciones[state][symbol]
                    next_states.add(next_state)
            
            if not next_states:
                print(f"No hay transiciones para {symbol} desde {current_states}")
                return False
            
            current_states = next_states
        
        is_accepting = any(state in self.nfa.estados_finales for state in current_states)
        print(f"¿Es estado de aceptación? {is_accepting}")
        return is_accepting