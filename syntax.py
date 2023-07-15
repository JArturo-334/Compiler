import re


class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 1

    def parse(self):
        if tokens[0] == '$':
            self.current_token = self.tokens[1]
            self.programa()
            print("Syntax is valid.")
        else:
            print(
                f"Syntax error: Expected $ at first position, found '{tokens[0]}'")

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.advance()
        else:
            raise SyntaxError(
                f"Syntax error: Expected '{expected_token}', found '{self.current_token}'")

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def programa(self):
        # Production rule: PROGRAMA -> programa id ; CUERPO .
        self.match('programa')
        self.match('id')
        self.match(';')
        self.cuerpo()
        self.match('.')

    def cuerpo(self):
        # Production rule: CUERPO -> DECLARACIONES PRINCIPAL | PRINCIPAL
        if self.current_token == 'variable':
            self.declaraciones()
            self.principal()
        elif self.current_token == '{':
            self.principal()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {self.current_token}")

    def declaraciones(self):
        # Production rule: DECLARACIONES -> variable LISTAID : TIPOS ; AUX1
        self.match('variable')
        self.listaid()
        self.match(':')
        self.tipos()
        self.match(';')
        self.aux1()

    def aux1(self):
        # Production rule: AUX1 -> LISTAID : TIPOS ; AUX1 | EPSILON
        if self.current_token == 'id':
            self.listaid()
            self.match(':')
            self.tipos()
            self.match(';')
            self.aux1()

    def listaid(self):
        # Production rule: LISTAID -> id AUX2
        self.match('id')
        self.aux2()

    def aux2(self):
        # Production rule: AUX2 -> , id AUX2 | EPSILON
        if self.current_token == ',':
            self.match(',')
            self.match('id')
            self.aux2()

    def tipos(self):
        # Production rule: TIPOS -> ESTANDAR | VECTORES
        if self.current_token in ['int', 'real', 'cadena', 'byte', 'caracter', 'booleano']:
            self.estandar()
        elif self.current_token == 'arreglo':
            self.vectores()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {self.current_token}")

    def estandar(self):
        # Production rule: ESTANDAR -> int | real | cadena | byte | caracter | booleano
        if self.current_token in ['int', 'real', 'cadena', 'byte', 'caracter', 'booleano']:
            self.match(self.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a standard type, found {self.current_token}")

    def vectores(self):
        # Production rule: VECTORES -> arreglo [ int .. int ] de ESTANDAR
        self.match('arreglo')
        self.match('[')
        self.match('int')
        self.match('..')
        self.match('int')
        self.match(']')
        self.match('de')
        self.estandar()

    def principal(self):
        # Production rule: PRINCIPAL -> { ESTATUTOS }
        self.match('{')
        self.estatutos()
        self.match('}')

    def estatutos(self):
        # Production rule: ESTATUTOS -> ESTATUTO ; AUX3
        self.estatuto()
        self.match(';')
        self.aux3()

    def aux3(self):
        # Production rule: AUX3 -> ESTATUTO ; AUX3 | EPSILON
        if self.current_token in ['id', 'leer', 'escribir', 'si', 'repetir', 'para', 'mientras']:
            self.estatuto()
            self.match(';')
            self.aux3()

    def estatuto(self):
        # Production rule: ESTATUTO -> ASIGNACION | CICLOPARA | CICLOMIENTRAS | CICLOREPETIR | ENTRADA | SALIDA | CONDICIONALSI
        if self.current_token == 'id':
            self.asignacion()
        elif self.current_token == 'repetir':
            self.ciclorepetir()
        elif self.current_token == 'para':
            self.ciclopara()
        elif self.current_token == 'mientras':
            self.ciclomientras()
        elif self.current_token == 'leer':
            self.entrada()
        elif self.current_token == 'escribir':
            self.salida()
        elif self.current_token == 'si':
            self.condicionalsi()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {self.current_token}")

    def asignacion(self):
        # Production rule: ASIGNACION -> VARIABLES = EXPRESION
        self.variables()
        self.match('=')
        self.expresion()

    def variables(self):
        # Production rule: VARIABLES -> id AUX5
        self.match('id')
        self.aux5()

    def aux5(self):
        # Production rule: AUX5 -> , EXPRESION AUX5 | EPSILON
        if self.current_token == ',':
            self.match(',')
            self.expresion()
            self.aux5()

    def ciclorepetir(self):
        # Production rule: CICLOREPETIR -> repetir ESTATUTO hasta EXPRESION
        self.match('repetir')
        self.estatuto()
        self.match('hasta')
        self.expresion()

    def ciclopara(self):
        # Production rule: CICLOPARA -> para CONTADOR do { ESTATUTOS }
        self.match('para')
        self.contador()
        self.match('do')
        self.match('{')
        self.estatutos()
        self.match('}')

    def contador(self):
        # Production rule: CONTADOR -> id = EXPRESION para EXPRESION
        self.match('id')
        self.match('=')
        self.expresion()
        self.match('para')
        self.expresion()

    def ciclomientras(self):
        # Production rule: CICLOMIENTRAS -> mientras EXPRESION hacer { ESTATUTOS }
        self.match('mientras')
        self.expresion()
        self.match('hacer')
        self.match('{')
        self.estatutos()
        self.match('}')

    def entrada(self):
        # Production rule: ENTRADA -> leer ( VARIABLES AUX6
        self.match('leer')
        self.match('(')
        self.variables()
        self.aux6()

    def aux6(self):
        # Production rule: AUX6 -> , VARIABLES AUX6 | )
        if self.current_token == ',':
            self.match(',')
            self.variables()
            self.aux6()
        elif self.current_token == ')':
            self.match(')')

    def salida(self):
        # Production rule: SALIDA -> escribir ( EXPRESION AUX7
        self.match('escribir')
        self.match('(')
        self.expresion()
        self.aux7()

    def aux7(self):
        # Production rule: AUX7 -> , EXPRESION AUX7 | )
        if self.current_token == ',':
            self.match(',')
            self.expresion()
            self.aux7()
        elif self.current_token == ')':
            self.match(')')

    def condicionalsi(self):
        # Production rule: CONDICIONALSI -> si EXPRESION entonces { ESTATUTOS } AUX8
        self.match('si')
        self.expresion()
        self.match('entonces')
        self.match('{')
        self.estatutos()
        self.match('}')
        self.aux8()

    def aux8(self):
        # Production rule: AUX8 -> Sino { ESTATUTOS } fin_sino | fin_sino
        if self.current_token == 'Sino':
            self.match('Sino')
            self.match('{')
            self.estatutos()
            self.match('}')
            self.match('fin_sino')
        elif self.current_token == 'fin_sino':
            self.match('fin_sino')

    def expresion(self):
        # Production rule: EXPRESION -> EXP | EXP RELACIONAL EXP
        self.exp()
        if self.current_token in ['=', '<', '>', '<=', '>=', '<>']:
            self.relacional()
            self.exp()

    def exp(self):
        # Production rule: EXP -> TERMINO AUX9
        self.termino()
        self.aux9()

    def aux9(self):
        # Production rule: AUX9 -> + TERMINO AUX9 | - TERMINO AUX9 | o TERMINO AUX9 | EPSILON
        if self.current_token in ['+', '-', 'o']:
            self.match(self.current_token)
            self.termino()
            self.aux9()

    def relacional(self):
        # Production rule: RELACIONAL -> = | < | > | <= | >= | <>
        if self.current_token in ['=', '<', '>', '<=', '>=', '<>']:
            self.match(self.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a relational operator, found {self.current_token}")

    def termino(self):
        # Production rule: TERMINO -> FACTOR AUX10
        self.factor()
        self.aux10()

    def aux10(self):
        # Production rule: AUX10 -> * FACTOR AUX10 | / FACTOR AUX10 | division FACTOR AUX10 | modulo FACTOR AUX10 | y FACTOR AUX10 | EPSILON
        if self.current_token in ['*', '/', 'division', 'modulo', 'y']:
            self.match(self.current_token)
            self.factor()
            self.aux10()

    def factor(self):
        # Production rule: FACTOR -> ( EXPRESION ) | VARIABLES | CONSTANTES | no EXPRESION
        if self.current_token == '(':
            self.match('(')
            self.expresion()
            self.match(')')
        elif self.current_token == 'id':
            self.variables()
        elif self.current_token in ['entero', 'real', 'cadena', 'caracter', 'verdadero', 'falso']:
            self.constantes()
        elif self.current_token == 'no':
            self.match('no')
            self.expresion()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {self.current_token}")

    def constantes(self):
        # Production rule: CONSTANTES -> entero | real | cadena | caracter | verdadero | falso
        if self.current_token in ['entero', 'real', 'cadena', 'caracter', 'verdadero', 'falso']:
            self.match(self.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a constant value, found {self.current_token}")


with open('lexical_result.txt', 'r') as file:
    content = file.read()

tokens = content.split()

syntax_analyzer = SyntaxAnalyzer(tokens)
syntax_analyzer.parse()
