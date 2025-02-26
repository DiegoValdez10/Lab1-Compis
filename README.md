

# Regular Expression to Automata Converter and Simulator



This project implements a program that processes a regular expression and a string Deterministic Finite Automata (DFA), and Minimized DFA. The program also simulates the evaluation of a string against the automata, determining whether the string belongs to the language defined by the regular expression.

## Features
- Input of regular expressions and strings for evaluation.
- Creation of an AFD by the direct method, and minimized DFA.
- Graphical representation of each automaton in a PNG format.
- Simulation of string evaluation for each automaton to verify membership in the language defined by the regular expression.
- Text file input processing with multiple regular expressions.

## Input Specifications
The program takes two types of inputs:
1. **Regular Expression (r)**: A valid regular expression consisting of single-character symbols and operators such as `*`, `|`, `+`, `?` and `()`.
   - Example: `(b|b)*abb(a|b)*`
2. **String (w)**: The string that will be evaluated against the language defined by the regular expression.
   - Example: `babbaaaaa`

### Epsilon Symbol (ε)
- The epsilon (`ε`) symbol is used for epsilon transitions in the automata. It should be chosen by the programmer and must be a symbol that is not likely to be part of the regular expression alphabet (avoid letters or numbers). A reasonable choice might be a special character, such as `𝜀`.

### Alphabet
- The alphabet for the regular expression is composed of all unique non-operator symbols (single characters) used in the expression.

## Output Specifications
For each regular expression processed, the following outputs are generated:

1. **Graphical Automata**:
   - A PNG image depicting:
     - The **minimized DFA** after applying minimization techniques.
   - The automata diagrams display:
     - The initial state.
     - Intermediate states.
     - The acceptance state.
     - Transitions with corresponding symbols (including epsilon transitions).
   
2. **Simulation Result**:
   - For each automaton (NFA, DFA, and minimized DFA), the program simulates the input string `w` to check if it belongs to the language defined by the regular expression `r`.
   - The result will be:
     - **"yes"** if the string is in the language (i.e., `w ∈ L(r)`).
     - **"no"** otherwise.

## Usage Instructions

1. **Input File**: 
   - The program processes regular expressions and strings from a text file where each line contains a single regular expression.
   - You will also provide a string `w` to evaluate against each regular expression in the file.

2. **Run the Program**:
   - The program reads the text file, generates the automata, and evaluates the string against them.
   - Ensure the input file is formatted correctly, with one regular expression per line.

### Example Output
1. Graphical PNG files showing the automata for the regular expression.
2. Simulation result:
3. NFA Simulation Result: yes 
4. DFA Simulation Result: yes 



## Requirements
- Python 3.x
- Graphviz (for automata visualization)
- Libraries:
- `graphviz`: For generating PNG images of the automata.


