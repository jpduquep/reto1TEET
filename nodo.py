import socket
import threading
import sys
import json

listaDocumentos = [("titulo","informacion"),]

def recibirMensajes(sock):
    #Funcion para recibir y gestionar los mensajes
    while True:
        data, _ = sock.recvfrom(1024)  # Hasta 1024 bytes de datos, se usa el _ porque lo segundo que devuelve el recvfrom es el addr (Ip y puerto del remitente) 
        if not data:
            break
        mensaje = json.loads(data.decode('utf-8'))
        print(f"\nMensaje recibido: ",mensaje)  # Imprimir el mensaje

def enviarMensajes(sock, puertoIzq, puertoDer, host='127.0.0.1'):
    #Funcion para enviar mensajes
    
    
    while True:
        resp = input('Digite salir si desea terminar la consola \n1: Para cargar un documento \n2: Para descargar un documento\n3: Mostrar lista de documentos\nR/ ')
        if resp.lower() == "salir":
            sock.close()
            break


        #En el 1 y 2 hay que armar el JSON para enviarlo como un API.

        elif resp == '1': #Cargar documento a la red
            titulo = input("Digitia el nombre del documento que vas a ingresar: ")
            mensaje = input("Cual es el contenido: ")
            mensajeJson = json.dumps(
                {
                    "tipoMensaje" : None,
                    "idDestinatario": None,
                    "idRemitente": None,
                    "titulo" : titulo,
                    "mensaje":mensaje

                }
            )
            #Enviando mensaje a la izquierda
            if puertoIzq:
                sock.sendto(mensajeJson.encode('utf-8'), (host, puertoIzq))
                print(f"Mensaje enviado a la izquierda (puerto",puertoIzq,")")
        
            #Enviando mensaje a la derecha
            if puertoDer:
                sock.sendto(mensajeJson.encode('utf-8'), (host, puertoDer))
                print(f"Mensaje enviado a la derecha (puerto",puertoDer,")")
            

        elif resp == '2': #Descargar documento de la red
            titulo = input("Digita el nombre del documento que buscas con extension: ")
            mensajeJson = json.dumps(
                {
                    "tipoMensaje" : None,
                    "idDestinatario": None,
                    "idRemitente": None,
                    "titulo" : titulo,
                    "mensaje":None

                }
            )
            #Enviando mensaje a la izquierda
            if puertoIzq:
                sock.sendto(mensajeJson.encode('utf-8'), (host, puertoIzq))
                print(f"Mensaje enviado a la izquierda (puerto",puertoIzq,")")
        
            #Enviando mensaje a la derecha
            if puertoDer:
                sock.sendto(mensajeJson.encode('utf-8'), (host, puertoDer))
                print(f"Mensaje enviado a la derecha (puerto",puertoDer,")")
            

        elif resp == '3':  #Mostrar listado
            print("\nListado de documentos de este nodo:")
            print("-"*20)
            for documento in listaDocumentos:
                titulo,informacion = documento[0],documento[1]
                print("Titulo: ",titulo)
                print("Informacion:\n"+informacion)
                print("-"*20)
            print("\n")

        

def iniciarNodo(puertoDeEscucha, puertoIzq, puertoDer):
    #Iniciando Nodo, inicializa la escucha y la escritura
    # Crear un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('127.0.0.1', puertoDeEscucha))  # Enlazar el socket al puerto para escuchar mensajes
        print(f"Nodo escuchando en el puerto",puertoDeEscucha)

        #Concurrencia para recibir los mensajes
        threading.Thread(target=recibirMensajes, args=(s,)).start()

        #Concurrencia para enviar los mensajes
        enviarMensajes(s, puertoIzq, puertoDer)

if __name__ == "__main__":
    puertoDeEscucha = int(sys.argv[1])
    puertoIzq = int(sys.argv[2])
    puertoDer = int(sys.argv[3])

    iniciarNodo(puertoDeEscucha, puertoIzq, puertoDer)
