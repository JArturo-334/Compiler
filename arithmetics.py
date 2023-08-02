import re


def is_valid_expression(expression):
    return re.match(r'^[\d+*\-/().\s]+$', expression) is not None


def tokenize(expression):
    return re.findall(r'\d+\.\d+|\d+|[+\-*/()]', expression)


def shunting_yard(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []

    for token in tokens:
        if re.match(r'\d+(\.\d+)?', token):  # Operand (number)
            output.append(float(token))
        elif token in precedence:  # Operator
            while (operator_stack and
                   operator_stack[-1] in precedence and
                   precedence[operator_stack[-1]] >= precedence[token]):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':  # Left parenthesis
            operator_stack.append(token)
        elif token == ')':  # Right parenthesis
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remove the '('

    while operator_stack:
        output.append(operator_stack.pop())

    return output


def evaluate_rpn(rpn_tokens):
    operand_stack = []

    for token in rpn_tokens:
        if isinstance(token, float):  # Operand (number)
            operand_stack.append(token)
        else:  # Operator
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()

            if token == '+':
                operand_stack.append(operand1 + operand2)
            elif token == '-':
                operand_stack.append(operand1 - operand2)
            elif token == '*':
                operand_stack.append(operand1 * operand2)
            elif token == '/':
                operand_stack.append(operand1 / operand2)

    return operand_stack[0]


def evaluate_expression(expression):
    if not is_valid_expression(expression):
        raise ValueError("Invalid characters in the expression.")

    tokens = tokenize(expression)
    rpn_tokens = shunting_yard(tokens)
    result = evaluate_rpn(rpn_tokens)

    # Convert result to an integer if it doesn't have any fractional part
    if result == int(result):
        result = int(result)

    return str(result)


'''
# Example usage:
expression = "4.5 + 2 * (6.5 - 1)"
result = evaluate_expression(expression)
print("Result:", result)
'''
