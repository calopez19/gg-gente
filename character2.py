from PyQt5.QtCore import QObject, pyqtSignal,QThread, QRect
from PyQt5.Qt import QTest
from os import path
import ventana_inicial
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QRect
from PyQt5.Qt import QTest
from collections import deque
from random import randint
from threading import Lock

mapa=[]
with open(path.join("mapas", "mapa_1.txt"), encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(";")
        data = data[0].split(" ")
        mapa.append(data)

def esta(tamaño_casilla,lista,posicion_x,posicion_y):
    n=posicion_x//tamaño_casilla
    b=posicion_y//tamaño_casilla
    if b<0 or n <0:
        return None
    if lista[n][b]=="R":
        return True
    else:
        return False
class Esta_en_tienda(QThread):
    signal_tienda=pyqtSignal()
    def __init__(self,posicion_x,posicion_y):
        super().__init__()

        self.posicion_x=posicion_x
        self.posicion_y=posicion_y
    def run(self):
        while True:
            self.esta_parado_al_medio()
            QTest.qWait(450)
    def esta_parado_al_medio(self):
        if self.posicion_x==300 and self.posicion_y==300:
            self.signal_tienda.emit()


class Mapa(QObject):
    mandar_mapa_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.mandar_mapa_signal.connect(crear_lista_mapa)

    def crear_lista_mapa(self,nombre):
        print ("se creo")
        with open(path.join("mapas", nombre), encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(";")
                data = data[0].split(" ")
                mapa.append(data)
        self.mapa=mapa
        self.crear_mapa_signal.emit(self.mapa)

class Character(QObject):
    """
    Clase que se encargará de manejar los datos internos del personaje.
    Es parte del back-end del programa, al contener parte de la lógica.
    """

    update_character_signal = pyqtSignal(str)
    def __init__(self, x, y):
        super().__init__()
        # Datos iniciales
        self.direction = 'R'
        self._x = x
        self._y = y
        self.lista=[[0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 0], [210, 0], [240, 0], [270, 0], [300, 0], [390, 0], [420, 0], [450, 0], [480, 0], [510, 0], [540, 0], [570, 0], [600, 0], [630, 0], [0, 30], [570, 30], [0, 60], [570, 60], [630, 60], [0, 90], [150, 90], [240, 90], [270, 90], [450, 90], [480, 90], [630, 90], [0, 120], [210, 120], [450, 120], [630, 120], [0, 150], [600, 150], [630, 150], [0, 180], [630, 180], [0, 210], [510, 210], [540, 210], [210, 240], [360, 240], [390, 240], [510, 240], [210, 270], [240, 270], [270, 270], [300, 270], [330, 270], [360, 270], [510, 270], [30, 300], [210, 300], [510, 300], [630, 300], [0, 330], [30, 330], [60, 330], [90, 330], [120, 330], [150, 330], [180, 330], [210, 330], [240, 330], [270, 330], [300, 330], [330, 330], [360, 330], [390, 330], [420, 330], [450, 330], [480, 330], [510, 330], [540, 330], [570, 330], [600, 330], [630, 330]]
        # Se inicializa nula la señal de actualizar la interfaz
        self.update_window_signal = None
        # Se conecta la señal de actualizar datos del personaje
        self.update_character_signal.connect(self.move)
        ######
        self.esta=Esta_en_tienda(self.x,self.y)

    def update_window_character(self, position='stand'):
        """
        Envía los datos del personaje mediante una señal a la
        interfaz para ser actualizados.
        :param position: str
        :return: None
        """
        if self.update_window_signal:
            self.update_window_signal.emit({
                'x': self.x,
                'y': self.y,
                'direction': self.direction,
                'position': position
            })

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        """
        Actualiza el valor de y del personaje y envía señal de
        actualización a la interfaz.
        :param value: int
        :return: None
        """
        if  -5< value < 340 and not (50<value<100 and 325<self.x<390):
            self._y = value
            self.update_window_character('walk')

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        """
        Chequea que la coordenada x se encuentre dentro los límites
        y envía la señal de actualización a la interfaz.
        :param value: int
        :return: None
        """

        if -5 < value < 660-10 and not (50<value<100 and 325<self.y<390) :
            self._x = value
            print (self.x,self.y)
            self.update_window_character('walk')

    def move(self, event):
        """
        Función que maneja los eventos de movimiento desde la interfaz.
        :param event: str
        :return: None
        """
        if event == 'R':
            self.direction = 'R'
            self.x += 10
        elif event == 'L':
            self.direction = 'L'
            self.x -= 10
        elif event == 'D':
            self.direction = 'D'
            self.y += 10
        elif event == "U":
            self.direction = 'U'
            self.y -= 10

