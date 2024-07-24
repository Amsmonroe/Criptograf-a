#Version 2, implementamos y mejoramos la funcion isPrime
#Se mejora decomposer para obtener los factores a su maxima reduccion
#Se arregla la division dentro de xgcd
#Tanto en incisoUno como incisoDos, se implementa una nueva forma de recorrer
#el arreglo Zn y factores, para comprobar la insercion de miembros adecuados

#En incisoDos se agrega la funcionalidad sobre la obtencion del inverso multiplicativo
#sobre cada miembro de Zn* y la n, los resultados se escriben el multiplicativosInversos.txt

#Alfabeto para el incisoTres
alfabeto = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]


#Funcion IMPORTANTE para saber si un numero es primo
def isPrime(n):
	if n <= 1:
		return False  # Los números menores o iguales a 1 no son primos
	
	# Iteramos desde 2 hasta la raíz cuadrada de n para optimizar la busqueda de numeros divisibles, es lo mismo hacer el modulo
	#con 25 que por 5, es por ello que si n fuera 25, reduce a su raiz cuadrada que es 25
	for i in range(2, int(n**0.5) + 1):
		if n % i == 0:
			return False  # Si n es divisible por algún número en este rango, no es primo
	return True  # Si no es divisible por ningún número en el rango, es primo

# Función para obtener los factores de n, exceptuando aquellos que NO son primos
def decomposer(n):
	factores = []
	for i in range(1, n + 1):
		#Si el numero es divisible y ademas es primo (asegurando que es el factor a su maxima reduccion) se agrega a la lista.

		if (n % i == 0 and i!=n):
			if isPrime(i):
				factores.append(i)
	return factores
				 
def xgcd(a,n):   
	u=a
	v=n
	x1=1
	x2=0
	while u>1:
		#print("u: ",u)
		q=v//u #aseguramos operacion entera
		r=v-(q*u)
		x=x2-(q*x1)
		v=u
		u=r
		x2=x1
		x1=x
	#print("Modulo inverso: ", x1%n)
	return x1 % n

def incisoUno():
	inverso=0
	n=0
	a=0
	while (n<2):
		n = int(input("Ingresa el valor de n: "))
		if(n<2):
			print("Ingrese un valor mayor o igual a 2")

	Zn = []
	ZnStar = []
	#Genero Zn con el rango de numeros de n
	for i in range(n):
		Zn.append(i)
	
	#print(f"El conjunto de Z{n} es {Zn}.\n")
	factores = []
	
	#Si el numero es primo, ZnStar y Zn son iguales
	if(isPrime(n)==True):
		ZnStar=Zn
		#Exceptuamos el cero en la lista
		#print(f"El conjunto de Z{n}* es {ZnStar[1:]}.\n")
	else:
		#Obtengo los factores para obtener los primos
		factores = decomposer(n)
		#print("factores", factores)
	#Genero Zn*
	for num in Zn:
		# Verificar si el número es divisible por algún factor
		divisible = False
		for factor in factores:
			if num % factor == 0:
				divisible = True
				break
		# Si el número no es divisible por ningún factor, agregarlo a Zn*
		if not divisible:
			ZnStar.append(num)
	#print(f"Los factores de {n} son: ",factores)

	#buscamos si a pertenece a Zn*
	found=False
	while (found==False):
		print(f"Elija alguno de los elementos de Z{n}*  {ZnStar}")
		a = int(input("Ingresa el valor de a: "))
		for i in range(len(ZnStar)):
			if(a==ZnStar[i]):
				#print(f"A Y ZN*[{i}]",a,ZnStar[i])
				found=True
				break
	#Y obtenemos el inverso con el xgcd
	inverso=xgcd(a,n)
	print("El inverso con el algoritmo extendido de euclides es: ", inverso)

def incisoDos():
	n = 0
	while(n<1):
		n = int(input("Ingrese el valor de n: "))
		if (n<1):
			print("Ingrese un valor mayor a 1.\n")
	
	Zn = []
	ZnStar = []
	#Genero Zn con el rango de numeros de n
	for i in range(n):
		Zn.append(i)
	
	#Imprimimos el conjunto Zn
	#print(f"El conjunto de Z{n} es {Zn}.\n")
	factores = []
	#Si el numero es primo, ZnStar y Zn son iguales
	#print("n ", n)
	if(isPrime(n)):
		ZnStar=Zn[1:]

		print(f"El conjunto de Z{n}* es {ZnStar}.\n")
	else:
		#Obtengo los factores para obtener los primos
		factores = decomposer(n)
		#print("factores:", factores)
			#Genero Zn*
		for num in Zn:
			# Verificar si el número es divisible por algún factor
			divisible = False
			for factor in factores:
				if num % factor == 0:
					divisible = True
					break
			# Si el número no es divisible por ningún factor, agregarlo a Zn*
			if not divisible:
				ZnStar.append(num)
		
	multiplicativosInversos = ("multiplicativosInversos.txt")
	with open(multiplicativosInversos, 'w') as multipInv:
		multipInv.write(f"Elementos de Z{n}*: {ZnStar}\n")
		multipInv.write(f"Forma de comprobar el resultado: (a*InvMult / n) <-- el residuo debe dar 1.\n\n")
		for i in range(len(ZnStar)):
			#a seria un elemento de Zn* y n seria la b
			auxMultInv=xgcd(ZnStar[i],n)	
			multipInv.write(f"Elemento de Z{n}* (a):{ZnStar[i]} - (n):{n} - Inverso Multiplicativo: {auxMultInv} \n")

	print("Operacion completada. Revise muliplicativosInversos.txt")
	
#Funcion para ordenar las letras de acuerdo a su aparicion
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
	for i in range(len(keyIndexes)):
		for j in range(len(keyAuxiliar)):
			if(keyIndexes[i]==keyAuxiliar[j]):
				keyword.append(j+1)
				break
	#Ej. para 5, en keyauxiliar se recorre hasta llegar a la
	#posicion 1 (de 0 a 4), como keyIndexes y keyAuxiliar coinciden
	#en esa posicion, se guarda la j y se le suma 1. (descomentar keyindexes y keyauxiliar para comprender mejor)
	#print("Valores de llave ordenada: ",keyword)
	return keyword

def checkDuplicates(keyword):
	arregloKeyword=list(keyword)
	#Iteramos el arreglo consigo mismo para buscar carateres repetidos
	for i in range(len(arregloKeyword)):
		for j in range(len(arregloKeyword)):
			#Si se compara consigo mismo, lo ignoramos
			if (arregloKeyword[i] == arregloKeyword[j] and i==j):
				pass
			elif(arregloKeyword[i]==arregloKeyword[j]):
				return True
	
	return False

def incisoTres():
	#Creamos una matriz de 4*5
	matriz=[[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0]]
	
	msgToCipher = "abcdefghijklmnopqrstu"
	invalidInput = True
	while(invalidInput is True):
		invalidInput = False
		while(len(msgToCipher)>20):
			msgToCipher = input("Que mensaje desea cifrar?: ")
			if len(msgToCipher)>20:
				print("Ingrese una frase menor a 20 letras")
				msgToCipher = "abcdefghijklmnopqrstu"
			
		invalidInput = any(char.isdigit() for char in msgToCipher)
		if(invalidInput is True):
			print("Asegurese de que el mensaje solo contenga letras del alfabeto inglés\n")
			msgToCipher = "abcdefghijklmnopqrstu"
	
	#Creando arreglo del mensaje a cifrar	
	msgCipherArray = list(msgToCipher) 
	
	#Llenando espacios vacios con x
	msgCipherArray += 'X' * (20-len(msgCipherArray))
	#print("msgCipherArray",msgCipherArray)

	#Manejo de errores
	keyword=""
	invalidInput = True
	repeatedChars = True
	while(invalidInput is True or repeatedChars is True):
			invalidInput = False
			repeatedChars = False
			while(len(keyword)<5):
				keyword = input("Ingrese la palabra clave: ")
				if len(keyword)!=5:
					print("Ingrese una frase de 5 letras")
					keyword=""

			invalidInput = any(char.isdigit() for char in keyword)
			repeatedChars = checkDuplicates(keyword)
			if(invalidInput is True or repeatedChars is True):
				print("Asegurese de que el mensaje solo contenga letras del alfabeto inglés y que no se repitan\n")
				keyword=""

	keywordArray = list(keyword.upper())

	keyIndexes = []
	#Otra aproximacion de for para buscar los indices de las letras del mensaje el alfabeto
	#Esto para posteriormente encontrar las apariciones de las letras
	for letter in keywordArray:
		for index, letraAlfabeto in enumerate(alfabeto):
			if letter == letraAlfabeto:
				keyIndexes.append(index)
	#print("keyindexes: ",keyIndexes)
	
	#Conseguimos las apariciones de las letras
	keywordPositions = reorder(keyIndexes)			

	# Creamos una lista con las posiciones de la matriz
	posiciones = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
				(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
				(2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
				(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]
	# Creamos una lista con los índices de los elementos en msgCipherArray correspondientes a cada posición de matriz
	# con forma de caracol
	indices = [0, 1, 2, 3, 4, 13, 14, 15, 16, 5, 12, 19, 18, 17, 6, 11, 10, 9, 8, 7]	

	# Asignamos los valores de msgCipherArray a la matriz según las posiciones dadas
	for i, (fila, columna) in enumerate(posiciones):
		matriz[fila][columna] = msgCipherArray[indices[i]]

	matrizImprimible = (f"{matriz[0]}\n{matriz[1]}\n{matriz[2]}\n{matriz[3]}\n")
	print(matrizImprimible)

	#Relacionamos los numeros del keywordPositions con cada una de las columnas
	#Creamos un dicccionario columnas correspondientes, donde la clave es el numero del keywordPositions y valor correspondiente es el
	#contenido de cada una de las columnas, pero las pasamos en el orden que queremos por medio de enumerate.
	columnasCorrespondientes = {}
	for i, number in enumerate(keywordPositions):
		#Asignamos al arreglo columna cada una de las letras contenidas de cada columna de la matriz con un recorrimiento hacia abajo
		columna = [fila[i] for fila in matriz]
		#Asignamos el diccionario, como llave el numero del keywordPositions (number) y la columna como valor
		columnasCorrespondientes[number] = columna

	#print("columnaCorrespondientes: ", columnasCorrespondientes)

	#Ordenamos diccionario por clave para sacar las palabras encriptadas posteriormente
	columnasCorrespondientesOrdenadas=dict(sorted(columnasCorrespondientes.items()))
	#print("columnaCorrespondientesOrdenadas: ", columnasCorrespondientesOrdenadas)
	
	#Escribimos el texto cifrado en un archivo
	cadena=''
	trancipher = ("trancipher.txt")
	with open(trancipher, 'w') as cipherText:
		cipherText.write(f"Password: {keyword}\n")
		#Recorremos todas las claves del diccionario (i) e imprimimos su valor en el archivo
		for i in columnasCorrespondientesOrdenadas:
			cadena += ''.join(map(str,columnasCorrespondientesOrdenadas[i]))+' '
		cipherText.write(f"{cadena}")

	print("\nCifrado Finalizado, revise trancipher.txt\n")

def transDecipher():
	#Creamos una matriz de 4*5
	matriz=[[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0]]
	# Creamos una lista con las posiciones de la matriz
	posiciones = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
				(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
				(2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
				(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]
	# Creamos una lista con los índices de los elementos en msgCipherArray correspondientes a cada posición de matriz
	# con forma de caracol
	indices = [0, 1, 2, 3, 4, 13, 14, 15, 16, 5, 12, 19, 18, 17, 6, 11, 10, 9, 8, 7]		
	
	#Pedimos la palabra clave
	keyword=""
	invalidInput = True
	repeatedChars = True
	while(invalidInput is True or repeatedChars is True):	
			invalidInput = False
			repeatedChars = False
			while(len(keyword)<5):
				keyword = input("Ingrese la palabra clave sin caracteres repetidos: ")
				if len(keyword)!=5:
					print("Ingrese una frase de 5 letras")
					keyword=""

			invalidInput = any(char.isdigit() for char in keyword)
			repeatedChars = checkDuplicates(keyword)
			if(invalidInput is True or repeatedChars is True):
				print("Asegurese de que el mensaje solo contenga letras del alfabeto inglés y que no se repitan\n")
				keyword=""
	#Pasamos la clave a mayúsculas
	keywordArray = list(keyword.upper())

	keyIndexes = []
	#Otra aproximacion de for para buscar los indices de las letras del mensaje el alfabeto
	#Esto para obtener la aparicion de las letras posteriormente
	for letter in keywordArray:
		for index, letraAlfabeto in enumerate(alfabeto):
			if letter == letraAlfabeto:
				keyIndexes.append(index)
	#print("keyindexes: ",keyIndexes)
	
	#Conseguimos la aparicion de las letras
	keywordPositions = reorder(keyIndexes)

	#Leemos el texto del archivo a partir de la segunda linea
	archivoADescifrar = "trancipher.txt"
	
	with open(archivoADescifrar, 'r') as extractCiphered:
		for i in range(1):
			next(extractCiphered)
		for line in extractCiphered:
			mensajeCifrado = line
	#Partimos el mensaje por cada espacio que haya, cada partición será una lista
	#de caracteres de igual forma, convirtiendose en un arreglo de arreglos
	mensajeCifradoPartes = [list(part) for part in mensajeCifrado.split()]
	#print("mensajeCifradoPartes", mensajeCifradoPartes)
	
	#Generamos el diccionario, asignando una clave del 1 al 5 y cada palabra que se partió del mensaje cifrado
	columnasCorrespondientes = {}
	for i, mensajeCifradoParte in enumerate(mensajeCifradoPartes):
		columnasCorrespondientes[i+1] = mensajeCifradoParte
	
	#print("columnasCorrespondientes",columnasCorrespondientes)
	
	#Rellenamos la matriz por columna y de acuerdo a las posiciones que se obtienen de keywordPositions (palabra clave)
	# i representa la columna actual
	# position es la clave del diccionario
	for i, position in enumerate(keywordPositions):
		#Utilizamos como clave keywordPositions, esto para asegurarnos de que estamos escribiendo el contenido
		#de la columna correspondiente de forma correcta en la matriz.
		# Recorremos las letras que se contienen en las listas del diccionario, respecto a su clave (en este caso basandonos en keywordPositions)
		#Tomamos el primer numero de keyWordPositions, tomamos esa columnaCorrespondiente (esa particion del texto cifrado)
		#y lo metemos a la matriz en ese orden
		for j, letra in enumerate(columnasCorrespondientes[position]):
			#j es la fila, donde se va a ir bajando de campo en campo
			# para ingresar los valores
			matriz[j][i] = letra

	matrizImprimible = (f"{matriz[0]}\n{matriz[1]}\n{matriz[2]}\n{matriz[3]}\n")
	#print("valor:",columnasCorrespondientes[2][2])
	print(matrizImprimible)

	#Concatenamos los elementos de la matriz y creamos el mensaje
	decipheredText = [''] * 20
	for i, (fila, columna) in enumerate(posiciones):
		decipheredText[indices[i]] += matriz[fila][columna]
	
	#Convertimos el arreglo a cadena y lo imprimimos en pantalla
	decipheredText = ''.join(map(str,decipheredText))
	print("Texto descifrado:",decipheredText)

def main():
	menu = "\n1. Implementación del algoritmo extendido de Euclides \n2. Zn* y sus multiplicativos inversos \n3. Transposition Cipher \n4. Transposition Decipher \n>> "
	opcion = int(input(f"Que operación deseas realizar?: {menu}"))

	match opcion:
		case 1:
			incisoUno()
		case 2:
			incisoDos()
		case 3:
			incisoTres()
		case 4:
			transDecipher()
		case _:	
			print("FATAL ERROR")		

main()
