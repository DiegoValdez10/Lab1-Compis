"""
Universidad del Valle de Guatemala

Teoria de la computación

Diego Valdez - 21328
Sebastian Estrada - 21405
"""

class NFA_Simulator:
    def __init__(self, nfa):
        self.nfa = nfa

    def epsilon_closure(self, states):

        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            epsilon_transitions = self.nfa.get_epsilon_transitions(state)
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def move(self, states, symbol):

        next_states = set()
        for state in states:
            transitions = self.nfa.get_transitions(state, symbol)
            next_states.update(transitions)
        return next_states

    def simulate(self, input_string):

        current_states = self.epsilon_closure([self.nfa.start_state])

        for symbol in input_string:

            current_states = self.epsilon_closure(self.move(current_states, symbol))


        return self.nfa.accept_state in current_states