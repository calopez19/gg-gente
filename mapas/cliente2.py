__author__ = "chapito96 & fringlesinthestreet" + " & StroveLight"

import threading
import socket
import json
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication
import sys

from cliente_ventana import Interfaz

class Client(QObject):

    '''
    Esta es la clase encargada de conectarse con el servidor e intercambiar información
    Hereda de QObject con el único motivo de poder emitir y conectar señales.
    Se recomienda que exista un BackEnd aparte del cliente (y que se relacionen).
    '''

    # Señal para avisar cuando llegan resultados del servidor
    enviar_a_interfaz = pyqtSignal(dict)
    enviar_mensaje_a_interfaz = pyqtSignal(str)
    error_usuario = pyqtSignal(str)
    escoger_salas = pyqtSignal(dict)
    entrar_a_sala = pyqtSignal(dict)
    volver_usuario = pyqtSignal()
    def __init__(self):

        # Como heredamos de QObject hay que hacer el llamado a super()
        super().__init__()
        print("Inicializando cliente...")

        # Inicializamos el socket principal del cliente.
        # Este corresponde al de una conexión TCP
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Primero definimos la dirección a la cual nos conectaremos.
        # En este caso se trabaja de manera local
        self.host = "localhost"
        self.usuario = None
        self.sala = None
        self.estado = "ingresando_usuario"
        # Definimos un Puerto al cual será conectado el cliente
        self.port = 1238
        self.personaje = None
        try:
            # Primero nos conectamos al servidor, pasándole como argumento la tupla
            # (HOST, PORT) al cual nos queremos conectar.
            # Esto tira error si la conexión es privada o si no hay un servidor "escuchando"
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor...")

            self.connected = True

            # Luego, creamos un thread para comenzar a escuchar lo que nos envía el servidor
            # Usamos un thread para permitir que el programa realice otras cosas
            # mientras escucha al servidor
            thread = threading.Thread(target=self.listen_thread, daemon=True)
            thread.start()
            print("Escuchando al servidor...")

            # Finalmente, conectamos la señal con un método de la ventana
            self.interfaz = Interfaz()
            self.interfaz.senal_a_backend.connect(self.enviar_al_servidor)
            self.error_usuario.connect(self.interfaz.no_esta_usuario)
            self.escoger_salas.connect(self.interfaz.pasar_a_escoger_sala)
            self.enviar_a_interfaz.connect(self.interfaz.desplegar_resultado)
            self.entrar_a_sala.connect(self.interfaz.pasar_a_sala)
            self.volver_usuario.connect(self.interfaz.volver_usuario)
        except ConnectionRefusedError:
            # Si la conexión es rechazada, entonces se 'cierra' el socket
            print("No se encontró un servidor\nAbortando...")
            self.socket_cliente.close()
            exit()
    def listen_thread(self):
        '''
        Este método es el usado en el thread y la idea es que reciba lo que
        envía el servidor. Implementa el protocolo de agregar los primeros
        4 bytes, que indican el largo del mensaje
        :return:
        '''

        # Si desean que un usuario pueda desconectarse
        while self.connected:
            # Primero recibimos los 4 bytes del largo
            response_bytes_length = self.socket_cliente.recv(4)
            # Los decodificamos
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")

            # Luego, creamos un bytearray vacío para juntar el mensaje
            response_bytes = bytearray()

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response_bytes) < response_length:
                largo_por_recibir = min(response_length - len(response_bytes), 256)
                response_bytes += self.socket_cliente.recv(largo_por_recibir)

            # Una vez que tenemos todos los bytes, entonces ahí decodificamos
            response = response_bytes.decode()

            # Luego, debemos cargar lo anterior utilizando json
            decoded = json.loads(response)

            # Para evitar hacer muy largo este método, el manejo del mensaje se
            # realizará en otro método
            print (type(decoded))
            if str(type(decoded)) == "<class 'dict'>" :
                self.manejar_comando(decoded)
                print ("hola")
            else:
                print ("hhhh")
                self.mensaje_de_alguien(decoded)

    def manejar_comando(self, mensaje):
        '''
        :param mensaje: diccionario con la información
        :return:
        '''
        # Podemos imprimir para verificar que toodo anda bien
        print("Mensaje Recibido: {}".format(mensaje))
        if len(mensaje)==1:
            self.error_usuario.emit(mensaje["usuario"])
            pass
        elif len(mensaje) ==2 and "estado_sala" not in mensaje.keys() :
            if mensaje["estado"]=="ingresando_usuario":
                self.usuario=None
                self.personaje=None
                self.estado=mensaje["estado"]
                self.volver_usuario.emit()
            else:
                ##entra en sala
                self.sala = mensaje["sala"]
                self.estado = mensaje["estado"]
        elif 'mensaje' in mensaje.keys() and mensaje["estado"]=="escogiendo_sala" and 'cantidad_en_sala' in mensaje.keys():
            ##sale de la sala
            self.estado = mensaje["estado"]
            self.escoger_salas.emit({"personaje":self.personaje,"usuario":self.usuario,"cantidad_en_sala":mensaje["cantidad_en_sala"]})
        elif "personaje" in mensaje.keys():
            print ("fffffffffffff")
            self.usuario = mensaje["usuario"]
            self.estado= mensaje["estado"]
            self.personaje = mensaje["personaje"]
            self.escoger_salas.emit({"usuario":self.usuario,"personaje": self.personaje, "usuario": self.usuario,"cantidad_en_sala":mensaje["cantidad_en_sala"]})
        elif "estado_sala" in mensaje.keys():
            self.entrar_a_sala.emit(mensaje)

    def mensaje_de_alguien(self,mensaje):
        print("Mensaje Recibido: {}".format(mensaje))

    def send(self, msg):
        '''
        :param msg: diccionario con la información
        :return:
        '''

        # Le hacemos json.dumps y luego lo transformamos a bytes
        msg_json = json.dumps(msg)
        msg_bytes = msg_json.encode()

        # Luego tomamos el largo de los bytes y creamos 4 bytes de esto
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        # Finalmente, los enviamos al servidor
        self.socket_cliente.send(msg_length + msg_bytes)


    def enviar_al_servidor(self, palabra):
        '''
        Este método es el que se gatilla con la señal y manda la información al método send
        :param palabra: string que representa la palabra a japonizar
        :return:
        '''
        # Tomamos la información del evento y la pasamos al formato antes descrito
        if self.estado == "ingresando_usuario":
            data = {"usuario": palabra,"estado":"ingresando_usuario"}
            pass
        elif self.estado == "escogiendo_sala":
            data = {"usuario": self.usuario, "sala":palabra,"estado":self.estado}
            pass
        elif self.estado == "en_sala":
            data = {"usuario": self.usuario,"estado":self.estado, "sala":self.sala,"mensaje":palabra}
        # Llamamos al método send para enviar la info al servidor
        self.send(data)



if __name__ == "__main__":
    app = QApplication([])

    client = Client()

    sys.exit(app.exec_())