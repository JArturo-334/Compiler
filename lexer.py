import subprocess
import transitions

transition_table = transitions.transition_table
accepting_states = transitions.accepting_states
reserved_words = transitions.reserved_words


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
        "+": lambda c: c == "+",
        '-': lambda c: c == '-',
        ';': lambda c: c == ';',
        '&': lambda c: c == '&',
        '|': lambda c: c == '|',
        "{": lambda c: c == "{",
        "}": lambda c: c == "}",
        '(': lambda c: c == '(',
        ')': lambda c: c == ')',
        '[': lambda c: c == '[',
        ']': lambda c: c == ']',
        ":": lambda c: c == ":",
        '?': lambda c: c == '?',
        "¿": lambda c: c == "¿",
        '!': lambda c: c == '!',
        "¡": lambda c: c == "¡",
        " ": lambda c: c == " "
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


def check_symbol(sym):
    if sym.isalpha():
        sym = 'letter'

    if sym.isdigit():
        sym = 'digit'

    return sym


# Read words from file and process characters individually
with open('code.txt', 'r') as file:
    content = file.read()

word = ''
current_state = 'q0'

# Write in a new file


def lexer_write(line):
    with open('lexical_result.txt', 'a') as f:
        f.write(f'{line} ')


first_symbol = content[0]
end_symbol = content[len(content)-1]

for i, char in enumerate(content):

    if i == len(content)-1:
        if end_symbol == '.':
            lexer_write(end_symbol)
            continue
        else:
            print('Program must end with "." symbol')
            break

    if i == 0:
        if first_symbol == '$':
            lexer_write(first_symbol)
            continue
        else:
            print('Program must start with $ symbol')
            break

    else:
        word += char

        char = check_symbol(char)

        next_char = content[i + 1] if i + 1 < len(content) else ''
        next_char = check_symbol(next_char)

        if i == len(content) - 1:
            next_char = ''

        current_state = transition_table[current_state].get(char, None)

        if current_state == None:
            if char == '\n':
                word = ''
            else:
                word_type = check_word(word.strip())
                if word_type:
                    lexer_write(word_type)
                    print(word.strip())
                    word = ''  # Reset the word to start accumulating the next word
                    current_state = 'q0'

            current_state = 'q0'

        if current_state in accepting_states and next_char not in transition_table[current_state]:
            # Exclude the current character
            word_type = check_word(word.strip())
            if word_type:
                lexer_write(word_type)
                print(f'{word_type}')
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
