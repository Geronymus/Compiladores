import LL1
import Lexico


# debe imprimir nuestras varibles
ingreso = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/ingreso.txt")
keys = Lexico.get_tokens(ingreso)
keys.append(['$', None, None])
root, node_list = LL1.principal(keys)

class evaluar:
    def __init__(self, lexema, tipo, categoria , funcion_padre, line = None):        
        self.lexema = lexema
        self.tipo = tipo 
        self.categoria = categoria 
        self.funcion_padre = funcion_padre
        self.line = line

lista = []
listaVar = []
## para que los valores sean globales de la funcion y podamos tener mas de 1 funcion
listaNam = []
ids = []
operadores = []
alls = []
lista2 = []

##------------------------------ Aqui agregamos los valores ------------------------------------------
def agregar(lexema, tipo, categoria, funcion_padre, valor):
    node_symbol = evaluar(lexema, tipo, categoria, funcion_padre, valor)
    lista.append(node_symbol)

def part_one(): #inicio del assembly
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    file.write(".data\n")
    file.close()

def principal(): #main del assembly
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    file.write(".text\n")
    file.write("\nmain:\n")
    file.close()

def declarar_assambly(variable):
    part_one()
    valor_res = variable[::-1]
    for i in range(len(valor_res)):
        file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
        file.write("var_"+ str(valor_res[i])+":    "".word      ""0:1" + "\n")
        file.close()
    principal()

#----------------------------------------------------------------------------------------------------

def identificar(root):
    # Aqui  se envia el papa  -> root
    #  root.children -> saca los hijos de papa 
    stack = root.children
    # creamos un array para  comparar 
    arr = []
    valor = []
    signo = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == "OPER":
            signo.append(stack[0].children[0].lexeme)
        # En este caso --- buscamos el papa donde se encuentra las variables
        if stack[0].symbol.symbol == 'TERM':
        # agregamos e los hijos  al arrray creado
            arr.append(stack[0].children[0].symbol.symbol)
            valor.append(stack[0].children[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        # vamos a iterrar sobre los valores para insertalos en el stack 
        for i in temp:
            stack.insert(0, i)
    ty = arr[0]
    flag = False
    for j in arr:
        if j != ty:
            flag = True
            break
    if flag:
        return "Error", valor, signo
    return ty, valor, signo

##--------------------------------------------------------------------------------------------------

###-------------------------------------------------------------------------------------------------
def head(root):
    stack = root.children
    ids = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'DECLARATION':
            ids.append(stack[0].children[1].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i) 
    declarar_assambly(ids)

##---------------------------------------------------------------------------------------------------

## --------------------------------------------------------------------------------------------------
def asignacionIF(root):
    stack = root.children
    ids = []
    operadores = []
    arr = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            ids.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'OPERCON':
            operadores.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'id':
            arr.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    return ids, operadores, arr

    ###-----------------------------------------------------------------------------------------------
def asignacionELSE(root):
    stack = root.children
    ids = []
    arr = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            ids.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'id':
            arr.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    return ids, arr

###--------------------------------------------------------------------------------------------------
def localizar(root):
    stack = root.children
    # ids = []
    # operadores = []
    listaNam.append(root.children[1].lexeme)
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'num':
            ids.append(stack[0].lexeme)
        if stack[0].symbol.symbol == 'OPER':
            operadores.append(stack[0].children[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)

    alls = (list(zip(ids, operadores, listaNam)))
    return alls

def scope(lexema):
    valor = False
    for symbol in lista:
        if symbol.lexema == lexema:
            valor = True
    return valor  

## Apartado Asembly ------------------ toda la logica esta aqui---------------------------------------
##----------------------------------------------------------------------------------------------------
## Esta funcione es para hacer operaciones matematicas 

def cambiaso(variable, signo, valor):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    valor_res = valor[::-1]
    lista2.append(valor_res)
    signo_res = signo[::-1]
    index = len(signo_res)
    index_signo = 0
    listaVar.append(variable)


    if len(signo_res) > 0:
            for j in range(len(valor_res)):
                if j == 0:
                    # Si la primera posicion de Valor_res == listaVar -_ solo se asigna
                    for  i in range(len(listaVar)):
                        if valor_res[j] == listaVar[i].lexeme:
                            file.write("\n\nla   $t0," + "   var_"+listaVar[i].lexeme)
                            file.write("\nlw  " + "$a0," + "  0($t0)")
                            break
                    ## si la primera varible de VALOR_RES no es IGUAL a listaVar -> se Creaera la variable
                    else:
                        file.write("\nli $a0,    "  + str(valor_res[j]) + "\n") 
                if  j >= 1:
                    for  i in range(len(listaVar)):
                        if valor_res[j] == listaVar[i].lexeme:
                            file.write("\n\nsw  " + "$a0,  " + "0($sp)")
                            file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")
                            file.write("\n\nla $t0, var_"+listaVar[i].lexeme)
                            file.write("\nlw  " + "$a0," + "  0($t0)")
                            break

                    else:
                        file.write("\n\nsw  " + "$a0,  " + "0($sp)")
                        file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")
                        file.write("\nli $a0,   "  + str(valor_res[j]) + "\n")
                        
                    if index_signo < index:
                        if signo_res[index_signo] == "+":
                            file.write("\nlw   " + "$t1,   "  + "4($sp) \n")
                            file.write("add  " + "$a0,  "   "$a0,  " + "$t1 \n")
                            file.write("\naddiu  "  + "$sp  "+ "$sp  " + "4")
                            index_signo += 1

            file.write("\n\nla   " +"$t0,  " + "var_"+variable.lexeme)
            file.write("\nsw  " +"$a0,  "+ "0($t0)")
            file.close()

    else:  
        file.write("\nli $a0,    "  + str(valor_res[0]) + "\n") 
        file.write("\nla   $t0," + "   var_"+variable.lexeme)
        file.write("\nsw  " + "$a0," + "  0($t0)")
        file.close()

###--------------------------------------------------------------------------------------------------
# esta es la funcion para la condicional if y else

def headIF(numero, simbolo, asig, copia, copia3):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    print(numero, simbolo, asig, copia,copia3)
    print(print(listaVar[0].lexeme))
    for  i in range(len(listaVar)):
        file.write("\n\nla $t0, var_"+listaVar[i].lexeme)
        file.write("\nlw  " + "$a0,  " + "0($t0)")
        file.write("\n\nsw  " + "$a0,  " + "0($sp)")
        file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")

    if  len(numero) > 0:

        if copia[1].isdigit():

            file.write("\nli $a0,    "  + numero[0] + "\n")

            if simbolo[0] == ">":       #bgt $t0, $t1, mayor 	t0 > t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nbgt  " + "$a0,  " + "$t1,  " +  "label_true")

            elif simbolo[0] == "<":     #blt $t0, $t1, menor	# t0 < t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nblt  " + "$a0,  " + "$t1,  " +  "label_true")
        else:

            file.write("\nli $a0,    "  + numero[0] + "\n")

            if simbolo[0] == ">":       #bgt $t0, $t1, mayor 	t0 > t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nblt  " + "$a0,  " + "$t1,  " +  "label_true")

            elif simbolo[0] == "<":     #blt $t0, $t1, menor	# t0 < t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nbgt  " + "$a0,  " + "$t1,  " +  "label_true")


    else:
        
        if copia3[1].isdigit():

            if simbolo[0] == ">":       #bgt $t0, $t1, mayor 	t0 > t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nbgt  " + "$a0,  " + "$t1,  " +  "label_true")

            elif simbolo[0] == "<":     #blt $t0, $t1, menor	# t0 < t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nblt  " + "$a0,  " + "$t1,  " +  "label_true")

        else:

            if simbolo[0] == ">":       #bgt $t0, $t1, mayor 	t0 > t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nblt  " + "$a0,  " + "$t1,  " +  "label_true")

            elif simbolo[0] == "<":     #blt $t0, $t1, menor	# t0 < t1
                file.write("\nlw  " + "$t1,  " + " 4($sp)")
                file.write("\nadd  " + "$sp,  " + "$sp, 4")
                file.write("\nbgt  " + "$a0,  " + "$t1,  " +  "label_true")
    
##---------------------------------------------------------------------------------------------------
    file.close()

##---------------------------------------Logica IF Y ElSE--------------------------------------------

def CreateIF(asig):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    file.write("\nlabel_true:")
    for h in range(len(asig)):
        for f in range(len(listaVar)):
            if asig[h][1] == listaVar[f].lexeme:
                file.write("\nli $a0,    "  + (asig[h][0]) + "\n") 
                file.write("\nla   $t0," + "   var_"+listaVar[f].lexeme)
                file.write("\nsw  " + "$a0," + "  0($t0)\n")
    file.write("\n\nlabel_end:")
    file.close()


def CreateELSE(asig):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    file.write("\n\nlabel_false:")
    for h in range(len(asig)):
        for f in range(len(listaVar)):
            if asig[h][1] == listaVar[f].lexeme:
                file.write("\nli $a0,    "  + (asig[h][0]) + "\n") 
                file.write("\nla   $t0," + "   var_"+listaVar[f].lexeme)
                file.write("\nsw  " + "$a0," + "  0($t0)\n")
    file.write("\nb  " + "label_end\n")
    file.close()

###--------------------------------------logica funciones--------------------------------------------


def llamada(valor, variable, nameFuction):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")

    # int x; solo actualizamos la tabla de simbolos

    # x = f1(5); $ invocacion a una funcion
    file.write("\nsw  " + "$fp  " + "0($sp)")
    file.write("\naddiu  " + "$sp  " + "$sp-4")

    # generamos codigo para cada parametro

    file.write("\n\nli  " + "$a0,  " + valor)

    # metemos el parametro a la pila
    file.write("\n\nsw  " + "$a0  " + "0($sp)")
    file.write("\naddiu  " + "$sp  " + "$sp-4")

    file.write("\n\njal  " + nameFuction)  # invocamos a la funcion

    # actualizamos la variable x en memoria   ##########################
    # el registro $t0, sera el puntero a la varaible en memoria
    file.write("\n\nla  " + "$t0,  " + "var_"+str(variable))
    file.write("\nsw  " + "$a0,  " "0($t0)")

    # ##################################################################

    # mostramos lo que tenemos en el acumulador
    # li $v0, 1
    # syscall
    file.write("\n\nli $v0, 1")
    file.write("\nsyscall")

    # # terminamos el codigo
    # li $v0, 10
    # syscall
    file.write("\n\nli $v0, 10")
    file.write("\nsyscall")

# ---------------------------------------------------------------------------------------------------

def generador(valor, signo, nombreFuncion):
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")

    file.write("\n\n" + nombreFuncion + ":")

    file.write("\n\nmove  " + "$fp  " + "$sp  ")

    file.write("\n\nsw  " + "$ra,  " + "0($sp)")
    file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")

    file.write("\nlw  " + "$a0,  " + "8($sp)")

    file.write("\n\nsw  " + "$a0,  " + "0($sp)")
    file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")

    # for
    # # 10
    if len(signo) > 2:
        print("Espera")
    else:

        # li $a0, 10
        file.write("\nli $a0,    " + valor + "\n")
        if signo == "+":
            # # suma
            # lw $t1, 4($sp)
            # add $a0, $a0, $t1
            file.write("\nlw   " + "$t1,   " + "4($sp) \n")
            file.write("add  " + "$a0,  "   "$a0,  " + "$t1 \n")

        # # pop
        file.write("\n\naddiu  " + "$sp,  " + "$sp,  4")

    # # fin expresion de la funcion ###############################################

    file.write("\n\nlw  " + "$ra  " + "4($sp)\n")
    file.write("addiu  " + "$sp  " + "$sp  12\n")  # 12 = 4*num_param + 8
    file.write("\nlw  "  + "$fp  " + "0($sp)\n")
    file.write("jr  " + "$ra")

    file.close()

##---------------------------------------Terminar Asembly--------------------------------------------

def footer():
    file = open("D:/WorkSpacex/Python/Compiladores/Final/PythonOldTimes/ProyectoParcial/assambly.txt", "a")
    file.write("\n\nli $v0, 1")
    file.write("\nsyscall")
    file.write("\n\njr $ra ")
    file.close()

##-----------------------------Aqui termina la logica del Asembly ----------------------------------------------

##----------------------------aqui comienza la logica  para buscar los valoeres del arbol-----------------------
def recorrerRoot(root):
    global valorGlobal
    # Creacion de funciones-------------------------------------------------
    if root.symbol.symbol == "FUNCTION":
        if scope(root.children[1].lexeme):
            print("FUNCION FAIL",
                root.children[1].line)
        else:
            print("FUNCION OK")
            tipo = "FUNCION"
            categoria = None
            padre = "LIBRE"
            agregar(root.children[1].lexeme, tipo, categoria, padre, None)

## -----------------------Aqui se recopilara toda la informacion para las funciones-------------------------
            valorGlobal = localizar(root)

##----------------------------------------------------------------------------------------------------------
    if (root.symbol.symbol == 'DECLARATION'):
        variable = root.children[1]
        nodo_tipo = root.children[0]
        expresion, valor, signo = identificar(root)
        aux = root

        for i  in (lista):
            for j in range(len(valor)):
                if i.lexema == valor[j]:
                    expresion = i.categoria


        padre_asigando = "LIBRE"
        ## tomanos el nombre de la funcion perteneciente 
        if aux.symbol.symbol == 'FUNCTION':
            padre_asigando = aux.children[1].lexeme


        if scope(variable.lexeme):
            print("VARIABLE YA CREADA")
        else:

            if nodo_tipo.children[0].lexeme == "bool" and  expresion == "BOOLEAN" :
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                agregar(variable.lexeme, tipo, categoria, padre)
                print("VARIABLE CREADA" )

            elif nodo_tipo.children[0].lexeme == "int" and  expresion == "num": 
                print("VARIABLE CREADA" )
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                cambiaso(variable, signo, valor)
                agregar(variable.lexeme, tipo, categoria, padre,valor)
            else:
                print("INVOCACION DE LA FUNCION")
## ----------------------Soporta mas de una funcion con fe que se pueda ---------------------------------------
                for j in range(len(valorGlobal)):
                    if valorGlobal[j][2] == valor[0]:
                        #print(valorGlobal[j])
                        #print(valor[0])

                        llamada(valor[1], variable.lexeme, valor[0] )
                        # cambiaso(variable, signo, valor)
                        generador(valorGlobal[j][0], valorGlobal[j][1], valorGlobal[j][2])

## --------------------------------Deteccion de el if y el else ---------------------------------------------

    if root.symbol.symbol == 'IF' or root.symbol.symbol == 'ELSE':

        global sub_red

        if root.symbol.symbol == 'IF':
            aux  = root
            arr_valor,arr_sim, arr_id = (asignacionIF(root))
            arrCond = []

            copia2 = arr_valor[:2]

            for i in range(len(copia2)):
                if lista[0].lexema ==  copia2[i]:
                    arrCond.append(copia2[i])
                    break

            copia = arr_valor[:2]

            arr_valor1 = arr_valor[:2]
            sub_arr = arr_valor[2:]
            sup_arr = []
            arr_id = arr_id[1:]
            sub = (list(zip(sub_arr, arr_id)))
            sub_red = sub[::-1]
            flag =  0
            con = 0
## aqui se combierte para los signos (x>y) o (y>x)
            copia3 =arr_valor[:2]
            for i in range(len(copia3)):
                if copia3[i] == arrCond[0]:
                    copia3[i] = "0"
            print(copia3)
            for j in range(len(lista)):
                for i in arr_valor1:
                    if i == lista[j].lexema:
                        flag += 1
                        con += 1
                    elif i.isdigit():
                        flag += 1
                        con += 1
                        sup_arr.append(i)
                    else:
                        flag += 0
                        con += 1
            stack = aux
            ids = []
            arr = []
            if flag >= 1:
                headIF(sup_arr,arr_sim, sub_red, copia, copia3)

            
        if root.symbol.symbol == 'ELSE':

            arr_valor, arr_id = (asignacionELSE(root))
            print(arr_valor, arr_id)


            sub_arr = arr_valor[:]
            sup_arr = []
            arr_id = arr_id[:]
            sub = (list(zip(sub_arr, arr_id)))
            sub_red1 = sub[::-1]
            CreateELSE(sub_red1)
            CreateIF(sub_red)

    ## Eliminacion de los valores de las funciones -------------------------------------

    if root.symbol.symbol == 'fin_llave' and root.father.symbol.symbol == 'FUNCTION':
        count = 0
        for i in lista:
            if i.funcion_padre == root.father.children[1].lexeme:
                count = count + 1
            while count > 0:
                for j in lista:
                    if j.funcion_padre == root.father.children[1].lexeme:
                        lista.remove(j)
            count = count - 1

    for child in root.children:
        recorrerRoot(child)

## -----------------------Aqui termina la busqueda para el llamado al arbol------------------------------


##----------------------------Creacion de la cabezera y cuerpo del progama ------------------------------

#head(root)
recorrerRoot(root)
footer()
##-------------------------------------------Fin---------------------------------------------------------