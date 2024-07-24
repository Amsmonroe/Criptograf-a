from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

def generate_3des_key():
    # Genera una llave aleatoria (24 bytes)
    key = DES3.adjust_key_parity(get_random_bytes(24))
    
    # LLave en base 64
    base64_key = base64.b64encode(key).decode('utf-8')
    
    # Escribe la llave en el archivo
    with open('3des_key.txt', 'w') as file:
        file.write(base64_key)

    print("Generada exitosamente ver archivo '3des_key.txt'.")

generate_3des_key()
