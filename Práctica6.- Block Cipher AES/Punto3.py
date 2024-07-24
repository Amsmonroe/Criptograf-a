import base64
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def load_key_from_file(filename):
    with open(filename, 'r') as file:
        key = file.read().strip()
    return base64.b64decode(key)

def decrypt_file(key, input_filename, output_filename):
    backend = default_backend()

    with open(input_filename, 'r') as infile:
        b64data = infile.read()
    
    ciphertext = base64.b64decode(b64data)
    iv = ciphertext[:16]  # El tamaño del bloque AES es de 16 bytes
    ciphertext = ciphertext[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    
    with open(output_filename, 'wb') as outfile:
        outfile.write(plaintext)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python decrypt_file.py <archivo_clave> <archivo_entrada> <archivo_salida>")
        sys.exit(1)

    key_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    key = load_key_from_file(key_file)
    decrypt_file(key, input_file, output_file)
    print(f"Archivo {input_file} descifrado y guardado en {output_file}")
