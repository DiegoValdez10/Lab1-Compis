import os
import platform
from ShuntingYard import ShuntingYard
from Metodo_Directo import AFD_Directo
from EmulatorNFA import NFA_Simulator

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def procesar_expresiones(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def procesar_expresion(expression, index):
    sy = ShuntingYard()
    try:
        postfix = sy.infix_to_postfix(expression)
        print(f"Expresión en notación postfix: {postfix}")
    except ValueError as e:
        print(f"Error en la conversión a postfix: {str(e)}")
        return

    try:
        ast = sy.build_ast(postfix)
        ast_graph = sy.draw_ast(ast)
        ast_filename = f"./grafos/ast_{index}"
        ast_graph.render(ast_filename, format="png", cleanup=True, view=False)
        print(f"AST generado y guardado como {ast_filename}.png")
    except ValueError as e:
        print(f"Error en la construcción del AST: {str(e)}")
        return

    try:
        metodo_directo = AFD_Directo()
        dfa = metodo_directo.construir_afd(ast)
        dfa_graph = dfa.visualizar(f"AFD para {expression}")
        dfa_filename = f"./grafos/dfa_{index}"
        dfa_graph.render(dfa_filename, format="png", cleanup=True, view=False)
        print(f"AFD generado por método directo y guardado como {dfa_filename}.png")
    except Exception as e:
        print(f"Error en la construcción del AFD por método directo: {str(e)}")
        return

    try:
        afd_minimizado = dfa.minimizacion()
        min_dfa_graph = afd_minimizado.visualizar(f"AFD Minimizado para {expression}")
        min_dfa_filename = f"./grafos/min_dfa_{index}"
        min_dfa_graph.render(min_dfa_filename, format="png", cleanup=True, view=False)
        print(f"AFD Minimizado generado y guardado como {min_dfa_filename}.png")
    except Exception as e:
        print(f"Error en la minimización del AFD: {str(e)}")
        return

    try:
        

        nfa_simulator = NFA_Simulator(dfa)  
        input_string = input(f"Ingrese una cadena para evaluar en el lenguaje {expression}: ")
        

        if dfa.simular(input_string):
            print(f"La cadena '{input_string}' pertenece al lenguaje (AFD)")
        else:
            print(f"La cadena '{input_string}' NO pertenece al lenguaje (AFD)")
        

        try:
            if nfa_simulator.simulate(input_string):
                print(f"La cadena '{input_string}' pertenece al lenguaje (AFN)")
            else:
                print(f"La cadena '{input_string}' NO pertenece al lenguaje (AFN)")
        except Exception as e:
            print(f"Error específico en la simulación del AFN: {str(e)}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"Error en la simulación: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    clear_screen()
    expressions = procesar_expresiones('./ER/expresiones.txt')
    for i, expression in enumerate(expressions):
        expression = expression.strip()
        if not expression:
            print("Expresión regular vacía")
            print("\n")
            continue
        print(f"Procesando expresión: {expression}")
        procesar_expresion(expression, i)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()