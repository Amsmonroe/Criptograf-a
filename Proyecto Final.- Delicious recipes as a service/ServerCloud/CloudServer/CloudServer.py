#python .\CloudServer.py
import socket
import pickle
import threading
import os

# Folder path to store encrypted recipes and public keys
RECIPES_FOLDER = "recipes"
KEYS_FOLDER = "keys"
CONTRACTS_FOLDER = "contracts"

# Ensure the folders exist
os.makedirs(RECIPES_FOLDER, exist_ok=True)
os.makedirs(KEYS_FOLDER, exist_ok=True)

def handle_client(client_socket):
    try:
        request = client_socket.recv(8192)#recepción de 8192 bytes del cliente 
        request_data = pickle.loads(request) #deserializar 
        action = request_data['action']#extraer acción
        collaborator_id = request_data['collaborator_id']#extraer id colaborador

        if action == 'store':
            encrypted_recipe = request_data['encrypted_recipe']#extraer receta cifrada
            encrypted_symmetric_key = request_data['encrypted_symmetric_key']#extraer clave simetrica
            
            # Store the encrypted recipe and key in files
            recipe_filename = os.path.join(RECIPES_FOLDER, f"{collaborator_id}_recipe.dat") #guardar la receta en archivo .dat
            with open(recipe_filename, 'wb') as recipe_file:
                recipe_file.write(encrypted_recipe)

            key_filename = os.path.join(RECIPES_FOLDER, f"{collaborator_id}_key.dat")#guarda la clave simetrica cifrada 
            with open(key_filename, 'wb') as key_file:
                key_file.write(encrypted_symmetric_key)

            response = 'Stored'
            client_socket.send(response.encode())#mensaje al cliente para que vea que la operación fue exitosa 

        elif action == 'retrieve':
            recipe_filename = os.path.join(RECIPES_FOLDER, f"{collaborator_id}_recipe.dat") #recuperar receta cifrada
            key_filename = os.path.join(RECIPES_FOLDER, f"{collaborator_id}_key.dat")#recuperar clave simetrica cifrada

            if os.path.exists(recipe_filename) and os.path.exists(key_filename): #verifica si existe la rectea cifrada y la clave cifrada
                with open(recipe_filename, 'rb') as recipe_file:
                    encrypted_recipe = recipe_file.read()#lectura de rectea cifrada

                with open(key_filename, 'rb') as key_file:
                    encrypted_symmetric_key = key_file.read()#lectura de clave cifrada

                response = {#diccionario que contiene la receta cifrada y la clave cifrada 
                    'encrypted_recipe': encrypted_recipe,
                    'encrypted_symmetric_key': encrypted_symmetric_key
                }
                client_socket.send(pickle.dumps(response))#el diccionario se serializa y se envia al cliente por medio del socket
            else:
                client_socket.send(b'Not Found') #si no se encuentra ninguno de los archivos se envia Not Found

        elif action == 'send_public_key_and_contract': #guarda la clave publica y el contrato 
            public_key = request_data['public_key'] #extrae clave publica
            contrato = request_data['contrato'] #extrae el contrato 
            public_key_filename = os.path.join(KEYS_FOLDER, f"{collaborator_id}_public_key.pem")#crear nombre de los archivos
            contrato_filename = os.path.join(CONTRACTS_FOLDER, f"{collaborator_id}_contrato.txt")
            with open(public_key_filename, 'wb') as key_file:
                key_file.write(public_key)#guardar clave publica 
            with open(contrato_filename, 'wb') as contrato_file:
                contrato_file.write(contrato)#guarda el contrato 
            client_socket.send(b'Public key and contract stored') #se envia respuesta al cliente 

        elif action == 'get_public_key_and_contract':
            public_key_filename = os.path.join(KEYS_FOLDER, f"{collaborator_id}_public_key.pem")#revuperar llave publica 
            contrato_filename = os.path.join(CONTRACTS_FOLDER, f"{collaborator_id}_contrato.txt")#recuperar contrato             
            #print(public_key_filename)
            if os.path.exists(public_key_filename) and os.path.exists(contrato_filename):
                with open(public_key_filename, 'rb') as key_file:
                    public_key = key_file.read()#lectura de clave publica 

                with open(contrato_filename, 'rb') as contrato_file:
                    contrato = contrato_file.read()  #lectura de contrato                  
                
                response = {#guardar en diccionario
                    'collaborator_public_key': public_key,
                    'contrato_firmado': contrato
                }                
                client_socket.send(pickle.dumps(response))#serializa para enviarlo a traves del socket
            else:
                client_socket.send(b'Public key not found')

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def server():
    #ocket.gethostbyname= obtener dirección IP del host local 
    host = socket.gethostbyname(socket.gethostname())#obtiene el nombre del host lcoal (el nombre de la maquina en la que se está ejecutando el script) 
    print(host)
    server_address = (host, 5555)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(server_address)
        s.listen()
        print("Server listening on", server_address)
        while True:
            client_socket, client_address = s.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server()
