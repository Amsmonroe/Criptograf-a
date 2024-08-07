from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

def generar_clave_3des():
    """
    Genera una clave aleatoria para 3DES y la guarda en un archivo en base64.
    """
    # Genera una clave aleatoria de 24 bytes (3DES requiere una longitud de 24 bytes).
    clave = DES3.adjust_key_parity(get_random_bytes(24))
    
    # Codifica la clave en base64.
    clave_base64 = base64.b64encode(clave).decode('utf-8')
    
    # Guarda la clave codificada en base64 en un archivo de texto.
    with open('3des_clave.txt', 'w') as archivo:
        archivo.write(clave_base64)
    
    print("Clave 3DES generada y guardada en '3des_clave.txt'.")

def cifrar_archivo_texto(clave_archivo, texto_archivo, cifrado_archivo):
    """
    Cifra un archivo de texto usando 3DES y guarda el resultado en un archivo de texto codificado en base64.
    """
    # Lee la clave codificada en base64 del archivo de clave.
    with open(clave_archivo, 'r') as archivo:
        clave_base64 = archivo.read()
    
    # Decodifica la clave de base64.
    clave = base64.b64decode(clave_base64) #obtener representación binaria 
    
    # Lee el texto plano del archivo de texto.
    with open(texto_archivo, 'rb') as archivo:
        texto_plano = archivo.read()
    
    # Crea un cifrador 3DES en modo CBC con un IV aleatorio.
    cifrador = DES3.new(clave, DES3.MODE_CBC)
    iv = cifrador.iv
    
    # Rellena el texto plano para que sea múltiplo del tamaño de bloque (8 bytes para 3DES).
    pad_len = 8 - (len(texto_plano) % 8)
    texto_plano += bytes([pad_len]) * pad_len
    
    # Cifra el texto plano.
    texto_cifrado = cifrador.encrypt(texto_plano)
    
    # Combina el IV y el texto cifrado y codifica en base64 para ser almacenado o transmitido como texto.
    texto_cifrado_base64 = base64.b64encode(iv + texto_cifrado).decode('utf-8')
    
    # Guarda el texto cifrado codificado en base64 en un archivo de texto.
    with open(cifrado_archivo, 'w') as archivo:
        archivo.write(texto_cifrado_base64)
    
    print(f"El archivo '{texto_archivo}' ha sido cifrado y guardado en '{cifrado_archivo}'.")

def descifrar_archivo_texto(clave_archivo, cifrado_archivo, descifrado_archivo):
    """
    Descifra un archivo de texto cifrado usando 3DES y guarda el texto plano recuperado en un archivo de texto.
    """
    # Lee la clave codificada en base64 del archivo de clave.
    with open(clave_archivo, 'r') as archivo:
        clave_base64 = archivo.read()
    
    # Decodifica la clave de base64.
    clave = base64.b64decode(clave_base64)
    
    # Lee el texto cifrado codificado en base64 del archivo de texto cifrado.
    with open(cifrado_archivo, 'r') as archivo:
        texto_cifrado_base64 = archivo.read()
    
    # Decodifica el texto cifrado de base64.
    texto_cifrado = base64.b64decode(texto_cifrado_base64)
    
    # Extrae el IV y el texto cifrado de los datos combinados.
    iv = texto_cifrado[:8]
    texto_cifrado_real = texto_cifrado[8:]
    
    # Crea un descifrador 3DES en modo CBC con el IV extraído.
    descifrador = DES3.new(clave, DES3.MODE_CBC, iv)
    
    # Descifra el texto cifrado.
    texto_descifrado = descifrador.decrypt(texto_cifrado_real)
    
    # Elimina el relleno.
    pad_len = texto_descifrado[-1]
    texto_descifrado = texto_descifrado[:-pad_len]
    
    # Guarda el texto plano descifrado en un archivo de texto.
    with open(descifrado_archivo, 'wb') as archivo:
        archivo.write(texto_descifrado)

    print(f"El archivo cifrado de '{cifrado_archivo}' ha sido descifrado y guardado en '{descifrado_archivo}'.")

def main():
    """
    Función principal que llama a otras funciones para generar la clave 3DES, cifrar y descifrar archivos.
    """
    # Generar una clave 3DES y guardarla en base64.
    generar_clave_3des()
    
    # Cifrar un archivo de texto.
    cifrar_archivo_texto('3des_clave.txt', 'texto_plano.txt', 'texto_cifrado.txt')
    
    # Descifrar el archivo de texto cifrado.
    descifrar_archivo_texto('3des_clave.txt', 'texto_cifrado.txt', 'texto_descifrado.txt')

main()
