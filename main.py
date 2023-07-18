import subprocess
import transitions
import symbol_table

transition_table = transitions.transition_table
accepting_states = transitions.accepting_states
reserved_words = transitions.reserved_words
data_types = transitions.data_types
obj_symbols_table = symbol_table.SymbolTable()


# Clear content in lexical_result.txt
with open('lexical_result.txt', 'w') as f:
    f.write('')


def check_word(word):
    # Initialize the automaton
    current_state = 'q0'
    word_type = None

    # Define the character types and their mappings
    char_types = {
        'letter': str.isalpha,
        'digit': str.isdigit,
        '$': lambda c: c == '$',
        '.': lambda c: c == '.',
        '/': lambda c: c == '/',
        '*': lambda c: c == '*',
        "'": lambda c: c == "'",
        '=': lambda c: c == '=',
        '>': lambda c: c == '>',
        '<': lambda c: c == '<',
        '!': lambda c: c == '!',
        '+': lambda c: c == '+',
        '-': lambda c: c == '-',
        ';': lambda c: c == ';',
        '&': lambda c: c == '&',
        '|': lambda c: c == '|',
        '{': lambda c: c == '{',
        '}': lambda c: c == '}',
        '(': lambda c: c == '(',
        ')': lambda c: c == ')',
        '[': lambda c: c == '[',
        ']': lambda c: c == ']',
        ':': lambda c: c == ':',
        '?': lambda c: c == '?',
        '¿': lambda c: c == '¿',
        '!': lambda c: c == '!',
        '¡': lambda c: c == '¡',
        ' ': lambda c: c == ' '
    }

    if word in reserved_words:
        word_type = word

    else:
        # Accumulate characters until no valid transition exists
        for char in word:
            char_type = 'other'
            # Check the type of character
            for type_name, char_check in char_types.items():
                if char_check(char):
                    char_type = type_name
                    break

            # Check if there is a transition defined for the current state and input character
            if current_state in transition_table and char_type in transition_table[current_state]:
                current_state = transition_table[current_state][char_type]
            else:
                break  # No valid transition, stop accumulating

        # Check if the final state is an accepting state
        if current_state in accepting_states:
            word_type = accepting_states[current_state]

    if word_type == 'operator':
        word_type = word

    return word_type


# Check symbol to change according to transition table rules -------------------------
def check_symbol(sym):
    if sym.isalpha():
        sym = 'letter'

    if sym.isdigit():
        sym = 'digit'

    return sym


# Read words from file and process characters individually --------------------------
with open('code.txt', 'r') as file:
    content = file.read()

word = ''
current_state = 'q0'


# Write in a new file ---------------------------------------------------------------
def lexer_write(line):
    with open('lexical_result.txt', 'a') as f:
        f.write(f'{line} ')


# Check first and last code symbols -------------------------------------------------
first_symbol = content[0]
end_symbol = content[len(content)-1]


def check_first_symbol():
    return first_symbol == '$' or print('Program must start with "$" symbol')


def check_last_symbol():
    return end_symbol == '.' or print('Program must end with "." symbol')


# Function for symbols table actions --------------------------------------------------
# Find variables and process their declarations
def process_variable_declarations(content):
    variable_start = content.find('variable')
    while variable_start != -1:
        semicolon_index = content.find(';', variable_start)
        if semicolon_index != -1:
            variable_line = content[variable_start:semicolon_index+1]
            process_variable_split(variable_line)
            variable_start = content.find('variable', semicolon_index)
        else:
            break


# Process a single variable declaration
def process_variable_split(variable_line):
    parts = variable_line.split(':')
    if len(parts) == 2:
        variable_info = parts[0].strip().split()
        if len(variable_info) >= 2:
            variable_name = variable_info[1]
            variable_type = parts[1].strip().rstrip(';').strip()
            if variable_type in data_types:
                symbols_table_type(variable_name, variable_type)
            else:
                print(variable_name, ' invalid data type')


# Process variable assignment
def get_variable_value(assignation_start):
    semicolon_index = content.find(';', assignation_start)
    if semicolon_index != -1:
        value_line = content[assignation_start + 1:semicolon_index]
        variable_value = value_line.strip()

        return variable_value


def symbols_table_type(identifier_name, identifier_type):
    id_name = identifier_name.strip()

    already_in_symTable = obj_symbols_table.lookup(id_name)

    if already_in_symTable:
        obj_symbols_table.update_attributes(
            id_name, {'type': identifier_type, 'value': None, 'scope': 'global'})

    else:
        obj_symbols_table.insert(
            id_name, {'type': identifier_type, 'value': None, 'scope': 'global'})


def symbols_table_value(identifier_name, identifier_value):
    id_name = identifier_name.strip()

    already_in_symTable = obj_symbols_table.lookup(id_name)

    if already_in_symTable:
        obj_symbols_table.update_attributes(
            id_name, {'value': identifier_value})


process_variable_declarations(content)

# Review code ------------------------------------------------------------------------
word_type = ''

for i, char in enumerate(content):

    last_word_type = word_type

    if i == 0:
        if check_first_symbol():
            lexer_write(first_symbol)
            continue
        else:
            break

    if i == len(content)-1:
        if check_last_symbol():
            lexer_write(end_symbol)
            continue
        else:
            break

    else:
        word += char
        char = check_symbol(char)
        next_char = content[i + 1] if i + 1 < len(content) else ''
        next_char = check_symbol(next_char)

        current_state = transition_table[current_state].get(char, None)

        if current_state == None:
            if char == '\n':
                word = ''
            else:
                word_type = check_word(word.strip())
                if word_type:
                    lexer_write(word_type)
                    word = ''  # Reset the word to start accumulating the next word
                    current_state = 'q0'
                elif next_char == ' ' or next_char == '\n':
                    print(word, 'is invalid')

            current_state = 'q0'

        if current_state in accepting_states and next_char not in transition_table[current_state]:
            # Exclude the current character
            word_type = check_word(word.strip())
            if word_type:

                if word_type == 'cadena' and len(word.strip()) == 3:
                    word_type = 'caracter'

                if word_type == 'id':
                    current_id = word

                if word_type == '=' and last_word_type == 'id':
                    var_value = get_variable_value(i)
                    if check_word(var_value):
                        symbols_table_value(current_id, var_value)

                lexer_write(word_type)
                word = ''  # Reset the word to start accumulating the next word
                current_state = 'q0'
            else:
                print(f'{word} is invalid')


'''
RUN SYNTAX ANALYZER
# Specify the path to the Python file you want to execute
file_path = 'syntax.py'

# Execute the Python file
subprocess.run(['python', file_path])
'''

obj_symbols_table.print_table()
