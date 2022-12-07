import pandas as pd
# salida
import sys
# Graficador
import graphviz

from Lexico import get_tokens


counter = 0
cont = 0
copia = []
copia2 = []
dot = graphviz.Digraph('round-table', comment='parser')
# Para acceder a los datos del archivo CSV, necesitamos una función read_csv() que recupere los datos en forma de Dataframe.
# index_col: Si no hay ninguno, no se muestran números de índice junto con los registros.
syntax_table = pd.read_csv("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/sys.csv", index_col=0)
# Cree un gráfico creando una instancia de un nuevo objeto Graph o Digraph:
# dot = graphviz.Digraph('round-table', comment='The Round Table')
arbol = graphviz.Graph(comment="Arbol Generedo")


# Recorrer el stack
def print_stack():
    print("\nStack:")
    for e in stack:
        print(e.symbol, end=" ")
    print()


# Recorrer el tokens
def print_input():
    print("\ntokens:")
    for t in tokens:
        print(t['type'], end=" ")
    print()

# retorna un nodo del arbol sintáctico segun el id
def find_in_tree(node_list, id):
    for nod in node_list:
        if nod.symbol.id == id:
            return nod



def print_tree(node, node_list, info = False):
    global dot
    dot = "digraph G { \n"

    for nod in node_list:
        if nod.symbol.is_terminal:
            if nod.symbol.symbol == 'e':
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> > ]; \n'
            else:
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme
                dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(lexeme) +' > ]; \n'
        
        else:

            if info and (nod.symbol.symbol == 'E' or nod.symbol.symbol == 'T' or nod.symbol.symbol == "E'" or nod.symbol.symbol == 'TERM'):
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme

                if nod.visited == True:
                    dot += str(nod.symbol.id) + ' [ <b>' + nod.sumbol.symbol + '</b> <br/> ' + str(nod.type) + ' <br/> line ' + str(nod.line) + ' > ]; \n'
                else:
                    dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(nod.type) + ' > ]; \n'
            
            else:
                dot += str(nod.symbol.id) + ' [ label=" ' + nod.symbol.symbol + ' " ]; \n'
    
    print_tree_recursive(node)
    dot += "}"

    #print(dot)

    graph = graphviz.Source(dot, format= 'png')
    graph.render("D:/WorkSpacex/Python/Compiladores/Final/PackAron - copia/archivos/tree.png", view=True)

def print_tree_recursive(node):
    global dot
    tmp = []
    for child in node.children:
        dot += str(node.symbol.id) + ' -> ' + str(child.symbol.id) + '; \n'
        tmp.append(str(child.symbol.id))
        print_tree_recursive(child)
    
    if len(node.children) > 0:
        dot += "{ \n"
        dot += "    rank = same; \n"
        dot += "    edge[ style=invis]; \n"
        dot += " -> ".join(tmp) + "; \n"
        dot += "    rankdir = LR; \n"
        dot += "} \n"

# Reemplazar valores /token_type - > Es el primer elemento de tu input
def update_stack(stack, token_type):
    production = syntax_table.loc[stack[0].symbol][token_type]

    # lo que se envia
    #print("\nproceso")
    #print(production)
    #print()

    #   Error Sintactico
    if (pd.isna(production)):
        print("Error.....")
        sys.exit()

# Aqui pasar de E -> xy a xy
    elementos = production.split(" ")
    #print("Soy el elemento")
    # print(elementos)
    father = elementos[0]
   
    # elminina los valores
    elementos.pop(0)
    elementos.pop(0)
    # eliminar de la pila
    father = stack.pop(0)
    node_father = find_in_tree(node_list, father.id)
# -----------------------------------------------------------------------------
    # eliminar de la pila
    # father =  stack.pop(0)
    # IMPLEMENTA UNA FUNCION QUE ME RETORNE UNA INSTACIA A NODE PARSE A PARTIR DE FATHER.ID
    # SERA LA VARIABLE NODE_FATHER

    if elementos[0] == "''":  # nulo
        new_symbol = node_stack( 'e', True )
        nod_tree    = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        node_list.append(nod_tree)
        return True

    for prod in reversed(elementos):
        # insertamos en la pila
        new_symbol = node_stack( prod, False if prod.isupper() else True )
        stack.insert(0, new_symbol)
        
        nod_tree = node_parser( new_symbol, None, [], node_father )
        node_father.children.insert(0, nod_tree )
        node_list.append(nod_tree)

    return True

# Vamos a insertar el elemetos a stack pero primero a E
    #print("elemento -> las hojas  -> los stack despues del Proman")
    #print(elementos)
    for i in range(len(elementos) - 1, -1, -1):
        symbol = node_stack(elementos[i], not elementos[i].isupper())
        stack.insert(0, symbol)
        nod_tree = node_parser( symbol, None, [], node_father)
        node_father.children.insert(0, nod_tree )
        node_list.append(nod_tree)

    #print_stack()

# -----------------------------------------------------------------------------------------------
  # creamos y vinculamos el nodo padre al nodo hijo



# -----------------------------------------------------------------------------------------------
    # node_father -> BUSCAR
    # node_primario = node_parser(symbol,None,[],node_father,None)
    # node_father.children.append(node_primario)
# se va a generar los nodos y sus relaciones


# Nodo principal -> Se encarga de mover
class node_stack:

    def __init__(self, symbol, is_terminal):
        # cada Stack -> tendra un id para identificarlo propiamente !!!
        global counter
        self.id = counter
        self.symbol = symbol  # simbolo de la gramatica
        self.is_terminal = is_terminal
        counter += 1



# Las Hojas
class node_parser:

    def __init__(self, symbol, lexeme=None, children=[], father=None, line=None):
        self.symbol = symbol
        self.lexeme = lexeme
        self.line = line
        self.children = children
        self.father = father



#  Entrada para el Stak
stack = []
symbol_1 = node_stack('$', True)  # numero 0 en stack
symbol_2 = node_stack('PROGRAM', False)  # numero 1 en stack
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)
# Se creara los hijos
# Creaer el node -> raiz -> symbol_2
root = node_parser(symbol_2, [])
node_list = []
node_list.append(root)

# ------------------------------------------------------------------------------------
#  Entrada para el Input -> se modifica
# lexema -> tu como usuario has ingresado
# type -> tipo (identificador)
#tokens = guardar_token
# Empezamos las condicionales

def principal(tokens):
    while True:
        #print("ITERATION ...")
        #print_stack()
        #print_input()
        if stack[0].symbol == '$' and tokens[0]['type'] == '$':
            print("Todo bien!")
            break

        if stack[0].is_terminal:
            #print("terminales ...")
            if stack[0].symbol == tokens[0]['type']:
                nod = find_in_tree(node_list, stack[0].id)
                nod.lexeme = tokens[0]['lexeme'] #tokens[0][1]
                nod.line = tokens[0]['line'] #tokens[0][2]
                stack.pop(0)
                tokens.pop(0)
            else:
                print("ERROR sintáctico")
                break

        # Cuando Son diferentes y se tiene que reemplazar segun la tabla
        else:
            update_stack(stack, tokens[0]['type'])

    return root, node_list


if __name__ == "__main__":
    fp = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/ingreso.txt")
    tokens = get_tokens(fp)
    tokens.append([ '$', None, None ])
    principal(tokens)
    # renderizar arbol
    print_tree(root, node_list, info = False)

    print()
    #print(dot)
