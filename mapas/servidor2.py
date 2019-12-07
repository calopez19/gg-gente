__author__ = "chapito96 & fringlesinthestreet" + " & StroveLight"

import threading
import socket
import json

with open("usuarios.json", 'r', encoding="utf-8") as file:
    diccionario = json.loads(file.read())


class Server:
    def __init__(self):
        print ("""    Cliente    |    Accion    |    Detalle    |
-------------------------------------------------""")
        self.gente_en_la_sala = {"sala_1": {}, "sala_2": {}, "sala_3": {}, "sala_4": {}}
        self.label_salas = {"sala_1": {"n_label": [1, 2, 3, 4, 5]},
                            "sala_2": {"n_label": [1, 2, 3, 4, 5]},
                            "sala_3": {"n_label": [1, 2, 3, 4, 5]},
                            "sala_4": {"n_label": [1, 2, 3, 4, 5]}}
        self.id_usuario = {}
        self.sockets = dict()
        self.host = "localhost"
        self.port = 1238
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        thread = threading.Thread(target=self.accept_connections_thread, daemon=True)
        thread.start()

    def accept_connections_thread(self):
        id_ = 1
        while True:
            client_socket, _ = self.socket_servidor.accept()
            self.sockets[id_] = client_socket
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket, id_),
                daemon=True
            )
            listening_client_thread.start()
            id_ += 1

    def listen_client_thread(self, client_socket, id_cliente):
        while True:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length,
                                                 byteorder="big")
                response_bytes = bytearray()
                while len(response_bytes) < response_length:
                    largo_por_recibir = min(response_length - len(response_bytes), 256)
                    response_bytes += client_socket.recv(largo_por_recibir)
                response = response_bytes.decode()
                decoded = json.loads(response)
                self.manejar_comando(decoded, client_socket)
            except ConnectionResetError:
                del self.sockets[id_cliente]
                usuario= None
                n= 0
                for c in self.id_usuario.values():
                    if c["id"]==id_cliente:
                        usuario=c["usuario"]
                        del self.id_usuario[usuario]
                        n=1
                        break
                for c in self.gente_en_la_sala:
                    if usuario in self.gente_en_la_sala[c]:
                        sala = c
                        self.label_salas[c]["n_label"].append(
                            self.gente_en_la_sala[c][usuario]["label"])
                        del self.gente_en_la_sala[c][usuario]
                        mensaje = {"estado_sala": self.gente_en_la_sala[sala],
                                   "sala": sala}
                        n=2
                        self.sendall(mensaje, sala)
                if n== 2:
                    print (
                        f"""{usuario: ^14.2} |salir de sala |{sala: ^14}""")
                    print (f"""{usuario: ^14.2} | desconectarse|""")
                elif n == 1:
                    print (f"""{usuario: ^14.2} | desconectarse|""")
                break

    def manejar_comando(self, recibido, socket):

        if recibido["estado"] == "ingresando_usuario" and recibido["usuario"]:
            n = 0
            if recibido["usuario"] in self.id_usuario.keys():
                mensaje = {"usuario": "ya esta conectado tal usuario"}
                self.send(mensaje, socket)
                pass
            else:
                for c in diccionario:
                    if c["nombre"] == recibido["usuario"]:
                        self.id_usuario.update(
                            {recibido["usuario"]: {"usuario": recibido["usuario"],
                                                   "id": list(self.sockets.keys())[
                                                       list(
                                                           self.sockets.values()).index(
                                                           socket)],
                                                   "personaje": c["personaje"]}})
                        n = 1
                        break
                if n == 1:
                    mensaje = {"usuario": recibido["usuario"], "estado": "escogiendo_sala",
                               'personaje': c["personaje"],"cantidad_en_sala":[len(self.label_salas["sala_1"]["n_label"]),len(self.label_salas["sala_2"]["n_label"]),len(self.label_salas["sala_3"]["n_label"]),len(self.label_salas["sala_4"]["n_label"])]}
                    self.send(mensaje, socket)

                    print (f"""{recibido["usuario"]: ^14.2} |  conectarse  |""")
                    pass
                else:
                    mensaje = {"usuario": "no existe tal usuario"}
                    self.send(mensaje, socket)

        elif recibido["estado"] == "escogiendo_sala":
            if recibido["sala"] == "volver":
                mensaje = {"mensaje": "volver", "estado": "ingresando_usuario"}
                del self.id_usuario[recibido["usuario"]]
                self.send(mensaje, socket)
                print (f"""{recibido["usuario"]: ^14.2} | desconectarse|""")
                pass
            elif recibido["sala"] != "volver" and len(self.gente_en_la_sala[recibido["sala"]]) < 5:
                self.gente_en_la_sala[recibido["sala"]].update(
                    {recibido["usuario"]: self.id_usuario[recibido["usuario"]]})
                self.gente_en_la_sala[recibido["sala"]][recibido["usuario"]].update(
                    {"label": self.label_salas[recibido["sala"]]["n_label"].pop()})

                mensaje = {"estado": "en_sala", "sala": recibido["sala"]}
                self.send(mensaje, socket)
                print (f"""{recibido["usuario"]: ^14.2} |Entrar a sala |{recibido["sala"]: ^14}""")
                mensaje = {"estado": "en_sala",
                           "estado_sala": self.gente_en_la_sala[recibido["sala"]]}
                self.sendall(mensaje, recibido["sala"])
        elif recibido["estado"] == "en_sala":
            if recibido["mensaje"] == "volver":
                self.label_salas[recibido["sala"]]["n_label"].append(
                    self.gente_en_la_sala[recibido["sala"]][recibido["usuario"]]["label"])
                mensaje = {"mensaje": "volver", "estado": "escogiendo_sala","cantidad_en_sala":[len(self.label_salas["sala_1"]["n_label"]),len(self.label_salas["sala_2"]["n_label"]),len(self.label_salas["sala_3"]["n_label"]),len(self.label_salas["sala_4"]["n_label"])]}
                del self.gente_en_la_sala[recibido["sala"]][recibido["usuario"]]
                self.send(mensaje, socket)
                mensaje = {"estado_sala": self.gente_en_la_sala[recibido["sala"]],
                           "sala": recibido["sala"]}
                self.sendall(mensaje, recibido["sala"])
                print (f"""{recibido["usuario"]: ^14.2} |salir de sala |{recibido["sala"]: ^14}""")
            elif recibido["mensaje"] != "volver":
                self.gente_en_la_sala[recibido["sala"]][recibido["usuario"]].update(
                    {"ultimo_mensaje": recibido["mensaje"]})
                mensaje = {"estado_sala": self.gente_en_la_sala[recibido["sala"]],
                           "sala": recibido["sala"]}
                self.sendall(mensaje, recibido["sala"])
                pass

    @staticmethod
    def send(mensaje, socket):
        msg_json = json.dumps(mensaje)
        msg_bytes = msg_json.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        socket.send(msg_length + msg_bytes)

    def sendall(self, mensaje, sala):
        for usuario in self.gente_en_la_sala[sala]:
            if usuario != "n_label":
                id_ = self.gente_en_la_sala[sala][usuario]["id"]
                try:
                    self.send(mensaje, self.sockets[id_])
                except ConnectionResetError:
                    del self.sockets[id_]
                    print('Error de conexion con cliente')
                except ConnectionAbortedError:
                    del self.sockets[id_]
                    print('Error de conexion con cliente')
                except IndexError:
                    print('Ya se ha eliminado el cliente del diccionario')


if __name__ == "__main__":

    server = Server()

    while True:
        pass
