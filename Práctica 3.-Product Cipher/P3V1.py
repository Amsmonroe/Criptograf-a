#Alfabeto para obtener el orden de las letras de la palabra clave
alfabeto = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

#Obtenemos las posiciones de las letras de forma ordenada
def reorder(keyIndexes):
    keyword = []
    #Creamos una lista auxiliar que contenga los indices ordenados
    #para analizar quien aparece primero en el alfabeto
    keyAuxiliar = sorted(keyIndexes)
    #print("keyIndexes: ",keyIndexes)
    #print("keyauxiliar: ",keyAuxiliar)

    #Recorremos ambas listas, la desordenada y ordenada
    #Si el elemento ordenado coincide con el elemento desordenado
    #guardamos su posicion + 1, resaltando el orden real de 
    #las apariciones de las letras en el alfabeto
    #Asegurarse de colocar bien los ciclos
    for i in range(len(keyAuxiliar)):
        for j in range(len(keyIndexes)):
            if(keyIndexes[j]==keyAuxiliar[i]):
                keyword.append(j+1)
                break
    #Ej. para 5, en keyauxiliar se recorre hasta llegar a la
    #posicion 1 (de 0 a 4), como keyIndexes y keyAuxiliar coinciden
    #en esa posicion, se guarda la j y se le suma 1. (descomentar keyindexes y keyauxiliar para comprender mejor)
    #print("Valores de llave ordenada: ",keyword)
    return keyword

#Para el cifrado, creamos la matriz de acuerdo al tamaño de la palabra clave y el mensaje
def crearMatriz(keyword, mensajeCifrado, posiciones):
    #print("mensaje cifrado",mensajeCifrado)

    numeroColumnas = len(keyword)
    numeroFilas = (len(mensajeCifrado) + numeroColumnas - 1) // numeroColumnas + 1  # Añadir una fila adicional
    matriz = [['-' for _ in range(numeroColumnas)] for _ in range(numeroFilas)]
    
    for j in range(numeroColumnas):
        matriz[0][j] = keyword[j]

    #Llenamos la matriz con el mensajeCifrado
    contador = 0
    for fila in range(1, numeroFilas+1):
        for columna in range(numeroColumnas):
            if contador < len(mensajeCifrado):
                matriz[fila][columna] = mensajeCifrado[contador]
                contador += 1
            else:
                break

    for fila in matriz:
        print(fila)
    
    #Tomamos las palabras columna por columna y las guardamos en un archivo de texto
    cadena=""
    archivoCifrado = ("cifrado.txt")
    with open(archivoCifrado,'w') as cifrado:
        #Convertimos el arreglo de la palabra clave en una cadena
        for i in keyword:
            cadena += ''.join(map(str,i))
        cifrado.write(f"Palabra Clave: {cadena}\n")

        # Imprimir una palabra separada por cada columna en el orden de las posiciones
        for index, columna in enumerate(posiciones):
            palabra_columna = ""
            for fila in range(1, numeroFilas):
                palabra_columna += matriz[fila][columna - 1]  # Usamos columna - 1 porque las posiciones están indexadas desde 1
            cifrado.write(f"{palabra_columna} ")
    print("Cifrado completado: checar cifrado.txt")


def productCipher():
    #Creamos la matriz base del alfabeto
    matrizMadre = [[0,'A','D','F','G','V','X'],
                   ['A','8','P','3','D','1','N'],
                   ['D','L','T','4','O','A','H'],
                   ['F','7','K','B','C','5','Z'],
                   ['G','J','U','6','W','G','M'],
                   ['V','X','S','V','I','R','2'],
                   ['X','9','E','Y','0','F','Q']]

    #Pedimos al usuario que ingrese un mensaje a cifrar y lo capitalizamos
    mensajeCifrar = input("Inserte el mensaje a cifrar: ")
    mensajeCifrarArreglo = list(mensajeCifrar.upper())

    #Pedimos la palabra clave
    keyword = input("Ingrese la palabra clave: ")
    keyword=keyword.upper()
    keyword=list(keyword)

    CoordenadaColumnas = (0,0)
    CoordenadaFilas = (0,0)
    listaCoordenadas = []
    
    #Recorremos la matriz madre para buscar caracter por caracter del mensaje cifrado
    #Cada una de las coordenadas que lo ubican, tanto columnas como filas
    #y guardamos la información en una lista
    for i in range(len(mensajeCifrarArreglo)):
        for j in range(1,len(matrizMadre)):
            for k in range(1,len(matrizMadre[0])):

                #print(matrizMadre[i][j],mensajeCifrarArreglo[i])
                if matrizMadre[j][k]==mensajeCifrarArreglo[i]:
                    #print(matrizMadre[j][k],mensajeCifrarArreglo[i])
                    CoordenadaColumnas = (0,k)			
                    CoordenadaFilas = (j, 0)
                    listaCoordenadas.append(CoordenadaFilas)
                    listaCoordenadas.append(CoordenadaColumnas)

                    #listaCoordenadas.sort(reverse=True)

    #print("Coordenadas: ", CoordenadaColumnas, CoordenadaFilas)
    #print("listaCoordenadas",listaCoordenadas)
     
    
    #Buscamos las letras correspondientes a las coordenadas
    mensajeCifrado=[]
    for coordenada in listaCoordenadas:
            mensajeCifrado.append(matrizMadre[coordenada[1]][coordenada[0]])

    keyIndexes = []
    #Otra aproximacion de for para buscar los indices de las letras del mensaje el alfabeto
    #Esto para posteriormente encontrar las apariciones de las letras
    for letter in keyword:
        for index, letraAlfabeto in enumerate(alfabeto):
            if letter == letraAlfabeto:
                keyIndexes.append(index)
    #print("keyindexes: ",keyIndexes)
    
    #Conseguimos las apariciones de las letras
    keywordPositions = reorder(keyIndexes)	
    #print(keywordPositions)

    crearMatriz(keyword, mensajeCifrado,keywordPositions)
    
def productDecipher():
    #Creamos la matrizMadre del alfabeto completo
    matrizMadre = [[0,'A','D','F','G','V','X'],
                   ['A','8','P','3','D','1','N'],
                   ['D','L','T','4','O','A','H'],
                   ['F','7','K','B','C','5','Z'],
                   ['G','J','U','6','W','G','M'],
                   ['V','X','S','V','I','R','2'],
                   ['X','9','E','Y','0','F','Q']]
    
    #Pedimos la palabra clave
    keyword=""
    keyword=input("Ingrese la palabra clave: ")
    keyword=keyword.upper()

    #Leemos el texto del archivo cifrado
    archivoADescifrar = "cifrado.txt"
    with open(archivoADescifrar, 'r') as extractCiphered:
        for i in range(1):
            next(extractCiphered)
        for line in extractCiphered:
            mensajeCifrado = line
    keyIndexes = []
    #Otra aproximacion de for para buscar los indices de las letras del mensaje el alfabeto
    #Esto para posteriormente encontrar las apariciones de las letras
    for letter in keyword:
        for index, letraAlfabeto in enumerate(alfabeto):
            if letter == letraAlfabeto:
                keyIndexes.append(index)
    #print("keyindexes: ",keyIndexes)
    
    #Conseguimos las apariciones de las letras
    keywordPositions = reorder(keyIndexes)
    #print("Posiciones: ", keywordPositions)

    #Partimos el mensaje por cada espacio que haya, cada partición será una lista
    #de caracteres de igual forma, convirtiendose en un arreglo de arreglos
    mensajeCifradoLen = mensajeCifrado.replace(" ","")
    mensajeRefactored = list(mensajeCifradoLen)
    mensajeCifradoPartes = [list(part) for part in mensajeCifrado.split()]
    #print("mensajeCifradoPartes", mensajeCifradoPartes)
    #print("mensajecifradoLen",mensajeCifradoLen)
    #Generamos el diccionario, asignando una clave del 1 al 5 y cada palabra que se partió del mensaje cifrado
    columnasCorrespondientes = {}
    for i, mensajeCifradoParte in enumerate(mensajeCifradoPartes):
            columnasCorrespondientes[keywordPositions[i]] = mensajeCifradoParte

    #print("columnasCorrespondientes: ", columnasCorrespondientes)
    #Creamos la matriz de acuerdo a la palabra clave y el mensaje cifrado
    numeroColumnas = len(keyword)
    numeroFilas = (len(mensajeCifradoLen) + numeroColumnas - 1) // numeroColumnas + 1 
    matriz = [['-' for _ in range(numeroColumnas)] for _ in range(numeroFilas)]
    
    #Llenamos la cabecera de la matriz
    for j in range(numeroColumnas):
        matriz[0][j] = keyword[j]

    keywordPositions.sort()
    #Rellenamos la matriz por columna y de acuerdo a las posiciones que se obtienen de keywordPositions (palabra clave)
    # i representa la columna actual
    # position es la clave del diccionario
    for i, position in enumerate(keywordPositions):
        #print("Posicion: ", position)
        #Utilizamos como clave keywordPositions, esto para asegurarnos de que estamos escribiendo el contenido
        #de la columna correspondiente de forma correcta en la matriz.
        # Recorremos las letras que se contienen en las listas del diccionario, respecto a su clave (en este caso basandonos en keywordPositions)
        #Tomamos el primer numero de keyWordPositions, tomamos esa columnaCorrespondiente (esa particion del texto cifrado)
        #y lo metemos a la matriz en ese orden
        for j, letra in enumerate(columnasCorrespondientes[position]):
            #j es la fila, donde se va a ir bajando de campo en campo
            # para ingresar los valores
            matriz[j+1][i] = letra

    #imprimimos la matriz
    for fila in matriz:
        print(fila)
    
    #Leemos el texto de la matriz de forma ordenada
    mensajeRefactored=""
    for i in range (1,len(matriz)):
        for j in range (len(matriz[0])):
            mensajeRefactored+=matriz[i][j]
    #print("mensajeRefactored",mensajeRefactored)

    mensajeRefactored = list(mensajeRefactored)
    #Recuperamos coordenadas de todas las letras del mensaje tomado de la matriz
    listaCoordenadasDuos=[]
    for i in range(len(mensajeRefactored)):
        for j in range (len(matrizMadre)):
            for k in range (len(matrizMadre[0])):
                #Si el numero es par, es columna, si es impar, es fila
                if(matrizMadre[j][k]==mensajeRefactored[i] and i%2==0):
                    CoordenadaColumna= (j,k)                    
                    listaCoordenadasDuos.append(CoordenadaColumna)
                    #print(f"mensajeRefactored[{i}],({j},{k})")
                    #print("coords:",i, matrizMadre[j][k])
                elif(matrizMadre[k][j]==mensajeRefactored[i] and i%2==1):
                    CoordenadaFila= (k,j)                    
                    listaCoordenadasDuos.append(CoordenadaFila)
                    #print(f"mensajeRefactored[{i}],({k},{j})")
                    #print("coords:",i, matrizMadre[j][k])                    
            break

    #print("listaCoordenadasDuos: ",listaCoordenadasDuos)
    #Sumamos las coordenadas,al primera con la de delante
    
    listaCoordenadasFinales = []
    # Iteramos sobre los índices de la lista original con un paso de dos
    # Sumamos los valores con el fin de obtener la coordenada resultante
    for i in range(0, len(listaCoordenadasDuos) - 1, 2):
        tupla_actual = listaCoordenadasDuos[i]
        tupla_siguiente = listaCoordenadasDuos[i + 1]
        
        # Sumamos las tuplas actuales y siguientes
        suma = (tupla_actual[0] + tupla_siguiente[0], tupla_actual[1] + tupla_siguiente[1])
        
        # Agregamos la suma a la lista de coordenadas finales
        listaCoordenadasFinales.append(suma)

    #print("listacoordenadasfinales: ", listaCoordenadasFinales)

    mensajeDescifrado=""
    #Ya teniendo las coordenadas finales las buscamos en la matriz madre
    for tupla in listaCoordenadasFinales:
        #print("tupla: ", tupla, tupla[0],tupla[1])
        for j in range (1,len(matrizMadre)):
            for k in range (1,len(matrizMadre[0])):
                if (j==tupla[0] and k==tupla[1]):
                    mensajeDescifrado += matrizMadre[k][j]
    
    print("Mensaje Descifrado: ", mensajeDescifrado)
    
def main():
    menu = ("1. Product Cipher \n2. Product Decipher \n>>" )
    opcion = int(input(f"Qué operación deseas realizar? \n{menu}"))

    match opcion:
        case 1: 
            productCipher()
        case 2:
            productDecipher()
        case _:
            print("FATAL ERROR")

main()
