import random
Zn = []
ZnStar = []
Ci = []
indicesMensaje = []
#La n debe ser igual a 95

#Creo el alfabeto global
alfabeto = [
  ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
  '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
  '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
  'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'
]

# Función para obtener los factores de n y sacar posteriormente los primos
def decomposer(n):
    for i in range(n):
        for j in range(n):
            if(i * j == n):
                factores = [i,j]
                return factores

#1. Funcion que recibe el tamaño del alfabeto y genera la llave aleatoriamente.
def keyGeneration(n, areMultipleKeysNeeded):

    Zn = []
    #Genero Zn con el rango de numeros de n
    for i in range(n):
        Zn.append(i)
    
    #print(f"El conjunto de Z{n} es: ",Zn)

    #Imprimimos el conjunto Zn
    #print(f"El conjunto de Z{n} es {Zn}.\n")
    factores = []
    #Obtengo los factores para obtener los primos
    factores = decomposer(n)
    #print(f"Los factores de {n} son: ",factores)
    
    #Genero Zn*
    for i in range(1,len(Zn),1):
        #Si el modulo de alguno de los factores es 0 (o es divisible), 
        #no se puede agregar a Zn*
        if(Zn[i]%factores[0]==0 or Zn[i]%factores[1]==0):
            #print(f"El {Zn[i]} es divisible entre {factores[0]} o {factores[1]}")
            pass
        else:
            ZnStar.append(i)
    
    archivoA = "incisoA.txt"
    with open(archivoA, 'a') as archivo:
        #Creamos lista para guardar las llaves temporalmente y escribirlas en el archivo
        keyTemp = []
        #Escritura de archivo con cada una de las llaves y su inverso
        k=0
        if(areMultipleKeysNeeded is True):
            for i in range(len(Zn)):
                for j in range(len(ZnStar)):
                    keyTemp.insert(0,ZnStar[j])
                    keyTemp.insert(1,Zn[i])
                    #print(keyTemp)
                    inversoImpreso = inverse(keyTemp,n)
                    archivo.write(f"Llave no. {k} ({Zn[i]},{ZnStar[j]}) Inverso: {inversoImpreso} \n")
                    k+=1
    
    #print(f"El conjunto de Z{n}* es: ",ZnStar)
    #print(f"El conjunto de Z{n} es: ",Zn)
    key = []
    #Seleccionamos a y b para crear la llave, tomando de los conjuntos
    #Zn* para a y Zn para b
    key.append(random.choice(ZnStar)) #a
    key.append(random.choice(Zn)) #b

    #key = [7,15]
    return key

#2. Funcion que busca el multiplicativo inverso de a modulo n
def inverse(key,n):
    #Posible bug: que el inverso este al final, en ese caso hay que invertir el orden las condiciones
    aInversa = 0
    for i in range(len(ZnStar)):
        if(i == len(ZnStar)):
            return -1
        elif(((key[0]*ZnStar[i]) % n)==1):
                aInversa = ZnStar[i]
                return aInversa

#3. Funcion que cifra el texto y retorna la cadena cifrada.
def cipherAlgorithm(key,n): 
    
    #Pedimos al usuario el mensaje a cifrar y cambiamos a mayúsculas
    #mientras se crea una lista con cada letra del mensaje
    archivoAEncriptar = "textoAEncriptar.txt"
    print(f"El mensaje que quieres encriptar debe estar en el archivo {archivoAEncriptar}.\n ")

    #Archivo B1 es textoAEncriptar.txt
    with open(archivoAEncriptar, 'r') as archivoB1:
        mensaje = archivoB1.read()
        mensajeMayusculas = list(mensaje)
        #print(mensajeMayusculas)

    #Buscamos las letras en nuestro alfabeto, tomamos el índice y lo guardamos 
    #en un arreglo, los indices serviran para obtener los Ci
    #print("MensajeMayusculas", mensajeMayusculas)
    for i in range(len(mensajeMayusculas)):
        for j in range(len(alfabeto)):
            if(mensajeMayusculas[i] == alfabeto[j]):
                #print("Letras ", alfabeto[j], mensajeMayusculas[i])
                indicesMensaje.append(j)                
    
    #print("Los indices del mensaje son: ", indicesMensaje)

    #Ya con los índices, creamos nuestros Ci, de acuerdo al tamaño del
    #mensaje

    for i in range(len(indicesMensaje)):
        #print("Llave: ", key)
        #Ci.append(((7 * indicesMensaje[i]) + 15) % n)
        Ci.append(((key[0] * indicesMensaje[i]) + key[1]) % n)

    #print("Indíces del mensaje cifrado: ", Ci)

    #Creamos el mensaje cifrado de acuerdo a la posición de la letra
    #del alfabeto
    mensajeCifrado=""
    for i in range(len(Ci)):
        mensajeCifrado+=alfabeto[Ci[i]] 

    #Imprimimos el mensaje cifrado en nuestro archivo cifrado.txt
    archivoEncriptado = ("cifrado.txt")
    with open(archivoEncriptado, 'w') as archivoB2:
        archivoB2.write(f"Llave: {key} \n{mensajeCifrado}")
        
# 4. Funcion que decifra un texto encriptado
def decipherAlgorithm(key, n):
    #Generamos Zn y Zn* para obtener el inverso
    Zn = []
    #Genero Zn con el rango de numeros de n
    for i in range(n):
        Zn.append(i)
    
    #print(f"El conjunto de Z{n} es: ",Zn)

    #Imprimimos el conjunto Zn
    #print(f"El conjunto de Z{n} es {Zn}.\n")
    
    #Obtengo los factores para obtener los primos
    factores = decomposer(n)
    #print(f"Los factores de {n} son: ",factores)
    
    #Genero Zn*
    for i in range(1,len(Zn),1):
        #Si el modulo de alguno de los factores es 0 (o es divisible), 
        #no se puede agregar a Zn*
        if(Zn[i]%factores[0]==0 or Zn[i]%factores[1]==0):
            #print(f"El {Zn[i]} es divisible entre {factores[0]} o {factores[1]}")
            pass
        else:
            ZnStar.append(i)
    #Leemos contenido de archivo a descrifrar a partir de la segunda linea ya que la primera pertenece al contenido de la llave.
    archivoADescifrar = ("cifrado.txt")
    with open(archivoADescifrar, 'r') as archivoC1:
        for i in range(1):
            next(archivoC1)
        for line in archivoC1:
            mensajeCifrado = line

    msjCifradoArreglo = list(mensajeCifrado)
    #print(msjCifradoArreglo)
    indicesCifrado = []
    #Buscamos las letras en nuestro alfabeto, tomamos el índice y lo guardamos 
    #en un arreglo
    
    # print("MensajeMayusculas", mensajeMayusculas)
    for i in range(len(msjCifradoArreglo)):
        for j in range(len(alfabeto)):
            if(msjCifradoArreglo[i] == alfabeto[j]):
                #print("Letras ", alfabeto[j], mensajeMayusculas[i])
                indicesCifrado.append(j)
    
    #print("indices cifrado",indicesCifrado) 

    aInversa=inverse(key,n)

            #print("Llave: ", key)
    #print("a Inversa: ", aInversa)
    #Generamos los mi con los ci, b y a Inversa

    Mi = []
    for i in range(len(indicesCifrado)):
        #Mi.append(((indicesCifrado[i]-15)*aInversa) % n)
        Mi.append(((indicesCifrado[i]-key[1])*aInversa) % n)
    #print("MI",Mi)
    mensajeDescifrado = ""
    #Consiguiendo las letras del alfabeto de acuerdo a las posiciones
    for i in range(len(Mi)):
        mensajeDescifrado+=alfabeto[Mi[i]]
    
    #Escribimos el archivo descifrado en un nuevo archivo de texto
    archivoDescifrado = ("descifrado.txt")
    with open(archivoDescifrado, 'w') as archivoC2:
        archivoC2.write(f"Mensaje descifrado: \n{mensajeDescifrado}")

def main():
    opcionAProbar = 0
    n = int(input("Ingresa el número de elementos del conjunto Z: "))
    
    while(opcionAProbar >3 or opcionAProbar < 1):
        opcionAProbar = int(input("Que operacion desea realizar? \n 1. Obtener las llaves válidas y el inverso de a \n 2. Cifrar texto y obtener su llave \n 3. Descifrar un texto dada su llave \n >> "))

        match opcionAProbar:
            case 1:
                keyGeneration(n,True)
                print("Llaves terminadas. Revise el archivo.\n")
                
            case 2:
                key=keyGeneration(n, False)
                cipherAlgorithm(key,n)
                
            case 3:
                a = int(input("Ingrese el primer valor de la llave: "))
                b = int(input("Ingrese el segundo valor de la llave: "))
                predefinedKey = [a,b]
                decipherAlgorithm(predefinedKey, n)
                print("Mensaje Descrifrado. Revise el archivo.\n")
            case _:
                print("Elija la opción adecuada \n")

    '''
    key = keyGeneration(n)
    mensajeCifrado=""
    mensajeCifrado = cipherAlgorithm(key,n)
    
    decipherAlgorithm(key,n,mensajeCifrado)#
    '''

main()
