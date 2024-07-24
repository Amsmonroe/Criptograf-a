import os
import base64
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def load_key_from_file(filename):
    with open(filename, 'r') as file:
        key = file.read().strip()
    return base64.b64decode(key)

def encrypt_file(key, input_filename, output_filename):
    backend = default_backend()
    iv = os.urandom(16)  # El tamaño del bloque AES es de 16 bytes

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(input_filename, 'rb') as infile:
        plaintext = infile.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    with open(output_filename, 'w') as outfile:
        outfile.write(base64.b64encode(iv + ciphertext).decode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python encrypt_file.py <archivo_clave> <archivo_entrada> <archivo_salida>")
        sys.exit(1)

    key_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    key = load_key_from_file(key_file)
    encrypt_file(key, input_file, output_file)
    print(f"Archivo {input_file} cifrado y guardado en {output_file}")
