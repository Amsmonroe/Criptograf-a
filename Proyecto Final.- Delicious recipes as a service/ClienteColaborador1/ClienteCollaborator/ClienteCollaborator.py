#python .\ClienteCollaborator.py
import socket
import pickle
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os
import base64

terminos_y_condiciones = """
Términos y Condiciones de Confidencialidad al Recibir Recetas

1. Introducción
Bienvenido. Agradecemos su confianza en recibir nuestras valiosas recetas con usted. Este documento describe los términos y condiciones de confidencialidad que rigen la recepción y el manejo de las recetas. Al recibir las recetas, usted acepta estos términos.

2. Confidencialidad
Usted se compromete a mantener la confidencialidad de todas las recetas recibidas. Esto significa que no compartirá, divulgará, ni utilizará sus recetas para ningún propósito que no sea el descrito en estos términos y condiciones sin nuestro consentimiento.

3. Almacenamiento y Seguridad
Todas las recetas serán almacenadas de manera segura utilizando tecnología de cifrado avanzada para proteger sus datos contra accesos no autorizados. Implementamos medidas de seguridad físicas, electrónicas y administrativas para salvaguardar y asegurar la información que recopilamos.

4. Acceso Limitado
El acceso a las recetas estará estrictamente limitado al personal autorizado que necesita conocer esta información para llevar a cabo su trabajo relacionado con los servicios que ofrecemos. Este personal está obligado por acuerdos de confidencialidad y se les ha capacitado en la importancia de mantener la privacidad de su información.

5. Uso de la Información
Las recetas recibidas serán utilizadas exclusivamente para los fines especificados en nuestra solicitud de recetas. No se utilizarán para ningún otro propósito sin su consentimiento explícito.

6. Divulgación a Terceros
No compartirá las recetas con terceros a menos que:
- Cuente con nuestro consentimiento explícito.
- Sea necesario para cumplir con la ley, una orden judicial, o un proceso legal.
- Sea necesario para proteger los derechos, propiedad o seguridad de nuestra organización, nuestros empleados, nuestros clientes u otros.

7. Derechos de Propiedad Intelectual
Nosotros conservamos todos los derechos de propiedad intelectual sobre las recetas. No podrá reclamar ningún derecho sobre ellas. El uso recetas se limita a los fines descritos en estos términos y condiciones.

8. Retención de Datos
Mantendremos las recetas únicamente durante el tiempo necesario para cumplir con los fines para los cuales fueron recopiladas y según lo requiera la ley aplicable. Una vez que ya no sean necesarias, procederemos a su eliminación segura.

9. Modificaciones a los Términos de Confidencialidad
Nos reservamos el derecho de modificar estos términos y condiciones de confidencialidad en cualquier momento. Cualquier cambio será notificado a usted mediante una actualización de este documento en nuestra página web o a través del medio que consideremos adecuado.

10. Contacto
Si tiene alguna pregunta o inquietud sobre estos términos y condiciones de confidencialidad, por favor, póngase en contacto con nosotros a través de los medios proporcionados en nuestra página web.

11. Aceptación de los Términos
Al recibir las recetas, usted confirma que ha leído, entendido y aceptado estos términos y condiciones de confidencialidad.

12. Legislación Aplicable
Estos términos y condiciones se rigen por las leyes del país donde se encuentra nuestra sede principal. Cualquier disputa relacionada con estos términos será resuelta en los tribunales de dicha jurisdicción.

Gracias por su confianza y por recibir nuestras recetas. Nos comprometemos a proteger su información y a respetar su confidencialidad en todo momento.
"""

# Generate base64 key
def generar_llave_base64(tamano_bytes=32): #esto es para la firma digital 
    bytes_aleatorios = os.urandom(tamano_bytes)#generar llave aleatoria en base 64
    llave_base64 = base64.b64encode(bytes_aleatorios).decode('utf-8')#codifica en base64
    return llave_base64

def generate_and_save_keys(): #generar clave privada y publica RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, #requisito de tamaño de clave en bits 
    )
    public_key = private_key.public_key()#clave publica a partir de la privada 

    # Save the private key
    with open('collaborator_private_key_1.pem', 'wb') as f: #nombre de archivo y guadarlo en archivo .pem
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM, # la clave privada se codifica en formato PEM
            format=serialization.PrivateFormat.TraditionalOpenSSL, #tecnica de escritura segura de bits para establecer conexines seguras
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the public key
    with open('collaborator_public_key_1.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# Load the private key from file
def load_private_key(filepath): #toma de argumento la ruta al archivo que contiene la clave privada
    with open(filepath, 'rb') as key_file: #abrimos el archivo en modo lectura
        private_key = serialization.load_pem_private_key(#cargar la clave privada a partir del contenido leido
            key_file.read(), #lee el archivo
            password=None#indica que no se requiere contraseña para decodificar la clave privada
        )
    return private_key

# Decrypt the recipe using AES
def decrypt_recipe(encrypted_recipe, symmetric_key): #toma de argumentos loa receta encriptotada y clave simetrica
    iv = encrypted_recipe[:16] #vector de inicialización, extrae los primeros 16 bytes que son los correspondientes al tamaño del IV
    encrypted_data = encrypted_recipe[16:] #extrae el resto de los datos encriptados, estos son los datos encriptados reales
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv)) #crea un objeto cipher usando AES con la clave simétrica y el modo CBC con el iv
    decryptor = cipher.decryptor()#objeto decryptor a partir del objeto anterior para desencriptar datos
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()#desencripta los datos, update=procesar los datos en bloques y finalize=completa el proceso de desencriptada, se concatenan y se asignan
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()#crea un objeto unpadder para quitar el padding utilizando el esquema PKCS7
    recipe = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return recipe

# Decrypt the symmetric key using the collaborator's private RSA key
def decrypt_symmetric_key(encrypted_symmetric_key, private_key):# descifrar la clave simétrica, clave simetrica, clave privada RSA
    symmetric_key = private_key.decrypt( #metoodo para descifrar usando clave simétrica encriptada 
        encrypted_symmetric_key,
        padding.OAEP( #esquema de padding en el proceso de descifrado 
            mgf=padding.MGF1(hashes.SHA256()), #función generadora de la mascara usando MGF1 con el algoritmo SHA-256
            algorithm=hashes.SHA256(),#espeficica el algoritmo hash usado para la mascara como para OAEP 
            label=None
        )
    )
    return symmetric_key

def collaborator_client():
    # Ensure the keys are generated and saved
    print("Bienvenido.")
    if not os.path.exists('collaborator_private_key_1.pem') or not os.path.exists('collaborator_public_key_1.pem'): #verificar  que existe clave privada y su contratp
        nombreCollab = input("Ingrese su nombre completo: ")
        print(terminos_y_condiciones)        
        aceptaTerminos = int(input("\n¿Aceptas los términos y condiciones de confidencialidad en las recetas que se te comparten? (Si: 1 / No : 0) "))
        if (aceptaTerminos == 1):            
            generate_and_save_keys() #generar sus llaves 
            print("Llaves generadas. Conectate al servidor y espera a que el chef te asigne una receta.\n")
            llaveBase64 = generar_llave_base64() #firma digital 
            compendioContrato = (terminos_y_condiciones + "\n\n" + "Nombre del colaborador: " + nombreCollab + "\nFirma Digital: " + llaveBase64).encode('utf-8')
            with open('contrato.txt', 'wb') as contrato:  #generar el contrato incluyendo firma digital y guarda en archivo  
                contrato.write(compendioContrato)
        else:
            print("Hasta pronto!")
            exit()
    # Load the collaborator's private key
    collaborator_private_key = load_private_key('collaborator_private_key_1.pem') #cargar la clave privada del colab
    
    # Load the collaborator's public key 
    with open('collaborator_public_key_1.pem', 'rb') as f: #cragar la clave publica del colab desde el archivo pem 
        collaborator_public_key = f.read()
    
    cloud_ip = input("Ingrese la IP de la nube: ")
    cloud_port = int(input("Ingrese el puerto del servidor: "))
    
    server_address = (cloud_ip, cloud_port)
    
    # Connect to the server and send the public key and contract  #conexión al servidor y envi de clave publica y contrato 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #establecer conexión con el servidor
        s.connect(server_address) #le pasamos ip y puerto 
        with open('contrato.txt', 'rb') as f: #lee el contratoo
            contrato = f.read()

        request = {
            'action': 'send_public_key_and_contract',
            'collaborator_id': 'collaborator_1',  # Change this ID as needed
            'public_key': collaborator_public_key,
            'contrato': contrato
        }
        s.sendall(pickle.dumps(request)) #envia la clave publica y contrato 
        response = s.recv(8192)
        print('Respuesta del servidor:', response.decode())
    
    # Reconnect to the server to request the encrypted recipe and key #solicitar la receta cifrada 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address)
        request = {
            'action': 'retrieve',
            'collaborator_id': 'collaborator_1',  # Change this ID as needed
        }
        s.sendall(pickle.dumps(request)) #iniciar solicitud de recuperación 
        response = s.recv(4096)
        if response == b'Not Found': #si no hay receta disponible muestra el mensaje y termina la función 
            print('No hay ninguna receta disponible para este colaborador')
            return

        response_data = pickle.loads(response) #si hay receta deserializa 
        encrypted_recipe = response_data['encrypted_recipe'] #extraer receta cifrada 
        encrypted_symmetric_key = response_data['encrypted_symmetric_key'] #ectraer clave simetrica cifrada 
        
        try: #desencriptar la clave simetrica y la receta 
            # Decrypt the symmetric key using the collaborator's private RSA key
            symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, collaborator_private_key) 

            # Decrypt the recipe
            decrypted_recipe = decrypt_recipe(encrypted_recipe, symmetric_key) #usar clave simetrica desencriptrada para desencriptar la receta 

            # Save the decrypted recipe to a text file
            with open('decrypted_recipe.txt', 'wb') as f: 
                f.write(decrypted_recipe) #guardar la receta 
            print("Receta Desencriptada en decrypted_recipe.txt")
        except ValueError as e:
            print(f"Desencriptado fallido: {e}")

if __name__ == "__main__":
    collaborator_client()
