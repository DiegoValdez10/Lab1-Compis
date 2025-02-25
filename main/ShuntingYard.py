
from graphviz import Digraph

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


    def __str__(self):
        return f"Node({self.value}, {self.left}, {self.right})"

class ShuntingYard:
    def __init__(self):
        self.precedencia = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1, '(': 0}
        self.operandos = set('abcdefghijklmnopqrstuvwxyz0123456789𝜀ε')

    def es_operador(self, c):
        return c in self.precedencia

    def precedencia_operador(self, operador):
        precedencia = {'*': 3, '+': 3, '.': 2, '|': 1}
        return precedencia.get(operador, 0)

    def add_concatenation_operators(self, expression):
        result = []
        for i, char in enumerate(expression):
            if i > 0:
                prev = expression[i-1]
                if (char in self.operandos or char == '(') and (prev in self.operandos or prev in '*+?)'):
                    result.append('.')
            result.append(char)
        return ''.join(result)


    def infix_to_postfix(self, expression):
        output = []
        operadores = []
        expression = self.add_concatenation_operators(expression)


        if expression.count('(') != expression.count(')'):
            raise ValueError("Error: Paréntesis desbalanceados en la expresión.")

        for c in expression:
            if c.isalnum() or c == '𝜀':
                output.append(c)
            elif c == '(':
                operadores.append(c)
            elif c == ')':
                while operadores and operadores[-1] != '(':
                    output.append(operadores.pop())
                if operadores and operadores[-1] == '(':
                    operadores.pop()
                else:
                    raise ValueError("Error: Se encontró ')' sin un '(' correspondiente.")
            else: 
                while (operadores and operadores[-1] != '(' and
                       self.precedencia_operador(operadores[-1]) >= self.precedencia_operador(c)):
                    output.append(operadores.pop())
                operadores.append(c)

        while operadores:
            if operadores[-1] == '(':
                raise ValueError("Error: Expresión no balanceada, falta ')'.")
            output.append(operadores.pop())

        postfix = ''.join(output)
        return postfix


    def build_ast(self, postfix):
        stack = []
        for char in postfix:
            if char.isalnum() or char == '𝜀':
                stack.append(Node(char))
            elif char in {'*', '+', '.', '|', '?'}:
                if char == '*':
                    node = Node(char)
                    node.right = stack.pop()
                    stack.append(node)
                elif char == '+':
                    node = Node(char)
                    node.right = stack.pop()
                    stack.append(node)
                elif char == '?':
                    node = Node(char)
                    node.right = stack.pop()
                    stack.append(node)
                else:
                    node = Node(char)
                    node.right = stack.pop()
                    node.left = stack.pop()
                    stack.append(node)
            else:
                raise ValueError(f"Operador no reconocido: {char}")
        return stack.pop()


    def draw_ast(self, node, graph=None, parent=None):
        if graph is None:
            graph = Digraph()

        if node:
            graph.node(str(id(node)), node.value)
            if parent:
                graph.edge(str(id(parent)), str(id(node)))
            self.draw_ast(node.left, graph, node)
            self.draw_ast(node.right, graph, node)

        return graph