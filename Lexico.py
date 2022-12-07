import ply.lex as lex


reserved = {
    'true': 'true',
    'false': 'false',
    'if': 'if',
    'else': 'else',
    'return': 'return',
    'int': 'int',
    'bool': 'bool',
    'def': 'def'
}
tokens = [
    'id',
    'num',
    'addition',
    'subtract',
    'multiplication',
    'division',
    'equal',
    'mayor',
    'minor',
    'lparem',
    'rparem',
    'ini_llave',
    'fin_llave',
    'dotcomma',
    'comma'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_addition = r'\+'
t_subtract = r'\-'
t_multiplication = r'\*'
t_division = r'\/'
t_equal = r'\='
t_mayor = r'\>'
t_minor = r'\<'
t_lparem = r'\('
t_rparem = r'\)'
t_ini_llave = r'\{'
t_fin_llave = r'\}'
t_dotcomma = r'\;'
t_comma = r'\,'


# A regular expression rule with some action code

def t_num(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema
    #print("se reconocio el numero")
    return t


def t_id(t):
    r'[a-zA-Z]+([a-zA-Z0-9]*)'
    t.type = reserved.get(t.value, 'id')
    return t

   # Define a rule so we can track line numbers


def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

   # A string containing ignored characters (tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Traenis la informacion de un txt


def get_tokens(fp):

  data = fp.read()
  print(data)
  fp.close()


  # Give the lexer some input
  lexer.input(data)
  # Guarda la informacion

  guardar_token = []

  while True:
    tok = lexer.token()
    if not tok:
      break      # No more input
    # print(tok)
    #print(tok.type, tok.value, tok.lineno, tok.lexpos)
    guardar_token.append({'type': tok.type.lower(), 'lexeme': str(tok.value).lower(), 'line': tok.lineno})

  guardar_token.append({'type': '$', 'lexeme': '$', 'line': guardar_token[-1]['line']})
  return guardar_token


if __name__ == "__main__":
    fp = open("/Compiladores/Final/PythonOldTimes/ProyectoParcial/ingreso.txt")
    tokens = get_tokens(fp)
    #print(tokens)
