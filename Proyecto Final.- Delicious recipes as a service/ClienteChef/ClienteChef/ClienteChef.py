#python .\ClienteChef.py
import socket
import pickle
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os
from pathlib import Path

# Encrypt the recipe using AES tamaño de bloque de 16 bytes o 128 bits 
def encrypt_recipe(recipe, symmetric_key):
    iv = os.urandom(16) #vector de inicialización
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv)) #crear objeto cipher usando la clave simetrica 
    encryptor = cipher.encryptor() #hace encriptador 
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder() #crear el objeto padder con el tamaño de bloque 
    padded_data = padder.update(recipe) + padder.finalize()#añade padding a receta, update= añade el padding necesario y padder finalize= completar el acolchado 
    encrypted_recipe = encryptor.update(padded_data) + encryptor.finalize() #cifra los datos usando el ecriptador y completa el proceso con cualquier dato restante
    return iv + encrypted_recipe #combina 

# Encrypt the symmetric key using the collaborator's public RSA key
def encrypt_symmetric_key(symmetric_key, public_key): 
    encrypted_symmetric_key = public_key.encrypt( #usando su clave publica RSA  cifra la clave simettrica 
        symmetric_key,
        padding.OAEP( #usando padding OAEP CON SHA-256
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_symmetric_key

def chef_client():
    cloud_ip = input("Ingrese la IP de la nube: ")
    cloud_port = int(input("Ingrese el puerto del servidor: "))
    numeroColaborador = input("A qué colaborador quieres asignar esta receta?: ")
    colaborador = "collaborator_" + numeroColaborador
    #print(colaborador)
    # Connect to the server to get the public key
    server_address = (cloud_ip, cloud_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Crear un socket 
        s.connect(server_address)
        request = {#enviar una solicitud para obtener clave publica, contrato 
            'action': 'get_public_key_and_contract',
            'collaborator_id': colaborador,
            'contrato': colaborador
        }
        s.sendall(pickle.dumps(request)) #se serializa
        response = s.recv(8192)#se envia 
        if response == b'Public key not found':
            print('Llave pública o contrato no encontrado para este colaborador.\n')
            return

        response_data = pickle.loads(response) #deserializa 
        contratoFirmado = response_data['contrato_firmado']#extrae contrato firmado
        public_key_data = response_data['collaborator_public_key']#extrae colaborador clabe publica 
        collaborator_public_key = serialization.load_pem_public_key(public_key_data) #carga la clave publica 

        contratoFirmado_filename = os.path.join("signed-contracts", f"{colaborador}_signed_contract.txt")#define la ruta y el nombre del archivo donde se guardaran el contrato firmado
        with open(contratoFirmado_filename, 'wb') as contratoFile:
            contratoFile.write(contratoFirmado)#guarda el contrado enn un archivo local
        print("Contrato firmado detectado. Comenzando encriptado.\n")    
    # Read recipe from a text file
    archivo = Path(__file__).parent / "recipe.txt"
    with open(archivo, 'rb') as f:
        recipe = f.read()

    # Generate a symmetric key for encrypting the recipe
    symmetric_key = os.urandom(32)

    # Encrypt the recipe
    encrypted_recipe = encrypt_recipe(recipe, symmetric_key)

    # Encrypt the symmetric key with the collaborator's public RSA key
    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, collaborator_public_key)

    # Connect to the server and store the encrypted recipe and key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#crea un nuevo socket
        s.connect(server_address)
        request = {#enviar solitud 
            'action': 'store',
            'collaborator_id': colaborador,
            'encrypted_recipe': encrypted_recipe,
            'encrypted_symmetric_key': encrypted_symmetric_key
        }
        s.sendall(pickle.dumps(request))#serializa 
        response = s.recv(1024)#recibir hasta 1024 bytres 
        print('Server response:', response.decode())

if __name__ == "__main__":
    chef_client()
