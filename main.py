import subprocess
import re
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
arreglo_type = ''
arreglo_types_dict = {}
arreglo_values_dict = {}


def process_variable_split(variable_line):
    parts = variable_line.split(':')
    if len(parts) == 2:
        variable_info = parts[0].strip().split()
        if len(variable_info) >= 2:
            variable_name = variable_info[1]
            variable_type = parts[1].strip().rstrip(';').strip()
            if 'arreglo' in variable_type:
                arr_is_valid = True
                arreglo_type = ''
                arreglo_attributes = []
                arreglo_parts = variable_type.split('[')
                variable_type = arreglo_parts[0].strip()

                arr_declaration = re.split(
                    r'\s*]\s*de', arreglo_parts[1])

                for attribute in arr_declaration[0].split('..'):
                    arreglo_attributes.append(attribute.strip())

                arreglo_type = arr_declaration[1].strip()

                for arr_attribute in arreglo_attributes:
                    if arr_attribute == arreglo_type:
                        continue
                    else:
                        arr_is_valid = False
                        print('Arreglo has different data types declaration')
                        break

                if arr_is_valid:
                    symbols_table_type(variable_name, variable_type)
                    symbols_table_value(variable_name, [])
                    create_arreglo_types(variable_name, arreglo_attributes)

            elif variable_type in data_types:
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


def get_variable_value_arr(assignation_start):
    semicolon_index = content.find(';', assignation_start)
    if semicolon_index != -1:
        value_line = content[assignation_start + 1:semicolon_index]
        result = re.findall(r'\d+(?:\.\d+)?', value_line)
        var_arreglo_index = result[0]
        var_arreglo_value = result[1]

        return var_arreglo_value, var_arreglo_index


def symbols_table_type(identifier_name, identifier_type):
    id_name = identifier_name.strip()

    already_in_symTable = obj_symbols_table.lookup(id_name)

    if already_in_symTable:
        obj_symbols_table.update_attributes(
            id_name, {'type': identifier_type, 'value': obj_symbols_table.get_attribute(id_name, "value"), 'scope': 'global'})

    else:
        obj_symbols_table.insert(
            id_name, {'type': identifier_type, 'value': None, 'scope': 'global'})


def symbols_table_value(identifier_name, identifier_value):

    def update():
        obj_symbols_table.update_attributes(
            id_name, {'value': identifier_value})

    id_name = identifier_name.strip()
    id_type = obj_symbols_table.get_attribute(id_name, "type")

    already_in_symTable = obj_symbols_table.lookup(id_name)

    if already_in_symTable:
        if id_type == 'booleano':
            if identifier_value == 'verdadero' or identifier_value == 'falso':
                update()
            else:
                identifier_value = 'Not correct data type booleano'
                update()

        elif id_type == 'caracter' and len(identifier_value.strip()) == 3:
            if check_word(identifier_value) == 'cadena':
                update()

        elif id_type == 'arreglo':
            update()

        elif id_type == check_word(identifier_value):
            update()

        else:
            identifier_value = 'Not correct data type'
            print(f'{identifier_name.strip()}: {identifier_value}')
            update()

    else:
        print(identifier_name, ': undefined')


def values_arreglo(identifier_name, identifier_value, idemtifier_index):

    def update():
        obj_symbols_table.update_attributes(
            id_name, {'value': arreglo_values_dict[id_name+'_array']})

    id_name = identifier_name.strip()
    id_type = obj_symbols_table.get_attribute(id_name, "type")

    already_in_symTable = obj_symbols_table.lookup(id_name)

    if already_in_symTable:
        if id_type == 'arreglo':
            if (id_name+'_array') in arreglo_values_dict:
                update_arreglo_values(
                    id_name, int(idemtifier_index), identifier_value)
                update()
            else:
                create_arreglo_values(id_name)
                update_arreglo_values(
                    id_name, int(idemtifier_index), identifier_value)
                update()

    else:
        print(identifier_name, ': undefined')

# Handle_arrays


def create_arreglo_types(identifier_name, new_arr_types):
    key = (identifier_name + '_array')
    arreglo_types_dict[key] = new_arr_types


def create_arreglo_values(identifier_name):
    key = (identifier_name + '_array')
    arreglo_values_dict[key] = []


def update_arreglo_values(identifier_name, add_arreglo_value, arreglo_position):
    key = (identifier_name + '_array')
    arreglo_values_dict[key].insert(
        add_arreglo_value, arreglo_position)
    return arreglo_values_dict[key]


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

                if word_type == 'id':
                    current_id = word

                if word_type == '=' and last_word_type == 'id':
                    var_value = get_variable_value(i)
                    var_value_type = check_word(var_value)
                    if var_value_type:
                        symbols_table_value(current_id, var_value)

                if word_type == '[' and last_word_type == 'id':
                    var_value, var_index = get_variable_value_arr(i)
                    var_value_type = check_word(var_value)
                    if var_value_type and var_index:
                        values_arreglo(
                            current_id, var_value, var_index)
                    else:
                        print('Cannot insert arreglo values')

                lexer_write(word_type)
                word = ''  # Reset the word to start accumulating the next word
                current_state = 'q0'
            else:
                print(f'{word} is invalid')


'''
#RUN SYNTAX ANALYZER
# Specify the path to the Python file you want to execute
file_path = 'syntax.py'

# Execute the Python file
subprocess.run(['python', file_path])
'''

with open('SYMBOLS_TABLE.txt', 'w') as sym_file:
    sym_file.write('')

obj_symbols_table.print_table()
