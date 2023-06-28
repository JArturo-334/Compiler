import re
import transitions

transition_table = transitions.transition_table
accepting_states = transitions.accepting_states


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

    return word_type


def check_symbol(sym):
    if 'A' <= sym <= 'Z' or 'a' <= sym <= 'z':
        sym = 'letter'

    if '0' <= sym <= '9':
        sym = 'digit'

    return sym


# Read words from file and process characters individually
with open('code.txt', 'r') as file:
    content = file.read()

word = ''
current_state = 'q0'

for i, char in enumerate(content):

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
            print(char, 'Ivalid statement')

        current_state = 'q0'

    if current_state in accepting_states and next_char not in transition_table[current_state]:
        word_type = check_word(word)  # Exclude the current character
        if word_type:
            print(f'{word.strip()} is a valid {word_type}')
            word = ''  # Reset the word to start accumulating the next word
            current_state = 'q0'
        else:
            print(f'{word} is invalid')
