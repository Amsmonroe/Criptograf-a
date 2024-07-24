import os
import base64
import sys

def generate_aes_key(key_size):
    if key_size not in [128, 192, 256]:
        raise ValueError("Tamaño de clave inválido. Elija 128, 192 o 256 bits.")
    
    key = os.urandom(key_size // 8)  # key_size está en bits, por lo que se divide por 8 para obtener bytes
    return base64.b64encode(key).decode('utf-8')

def save_key_to_file(key, filename):
    with open(filename, 'w') as file:
        file.write(key)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Forma de ejecución: python generate_aes_key.py <tamaño_clave> <archivo_salida>")
        sys.exit(1)

    key_size = int(sys.argv[1])
    output_file = sys.argv[2]
    
    key = generate_aes_key(key_size)
    save_key_to_file(key, output_file)
    print(f"Clave AES de {key_size} bits generada y guardada en {output_file}")
