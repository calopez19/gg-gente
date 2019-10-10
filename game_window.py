from os import path
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from character2 import Character
from nueva import Tienda
from intento_crear_lista_mapa import Mapa


mapa=[]
with open(path.join("mapas", "mapa_2.txt"), encoding="utf-8") as file:
    for line in file:
        data = line.strip().split(";")
        data = data[0].split(" ")
        mapa.append(data)

class GameWindow(QWidget):
    """
    Clase para crear la ventana del juego mismo. Es parte del front-end
    del programa, al solo modificar la interfaz gráfica.
    """
    signal_tienda= pyqtSignal()
    show_tienda_signal = pyqtSignal()
    mapa_signal=pyqtSignal(list)
    update_window_signal = pyqtSignal(dict)
    show_game_signal = pyqtSignal()
    # Se almacena en un diccionario las rutas de imágenes del personaje
    sprites_paths = {
        ('stand', 'R'): path.join("sprites", 'personaje', 'right_1.png'),
        ('stand', 'L'): path.join( "sprites",'personaje', 'left_1.png'),
        ('stand', 'U'): path.join("sprites", 'personaje', 'up_1.png'),
        ('stand', 'D'): path.join("sprites",'personaje', 'down_1.png'),
        ('walk', 'R', 1): path.join("sprites", 'personaje', 'right_2.png'),
        ('walk', 'R', 2): path.join("sprites", 'personaje', 'right_3.png'),
        ('walk', 'R', 3): path.join("sprites", 'personaje', 'right_4.png'),
        ('walk', 'L', 1): path.join( "sprites",'personaje', 'left_2.png'),
        ('walk', 'L', 2): path.join( "sprites",'personaje', 'left_3.png'),
        ('walk', 'L', 3): path.join("sprites", 'personaje', 'left_4.png'),
        ('walk', 'U', 1): path.join("sprites", 'personaje', 'up_2.png'),
        ('walk', 'U', 2): path.join( "sprites",'personaje', 'up_3.png'),
        ('walk', 'U', 3): path.join("sprites", 'personaje', 'up_4.png'),
        ('walk', 'D', 1): path.join( "sprites",'personaje', 'down_2.png'),
        ('walk', 'D', 2): path.join( "sprites",'personaje', 'down_3.png'),
        ('walk', 'D', 3): path.join( "sprites",'personaje', 'down_4.png')
    }

    def __init__(self):
        super().__init__()
        ####
        self.mapa=Mapa()
        # Se instancia el personaje del backend
        self.backend_character = Character(0, 300)
        self._frame = 1
        self.libraries = dict()
        # Se definen los otros atributos internos de la instancia
        self.background = None
        self.front_character = None
        self.current_sprite = None
        self.update_character_signal = None
        self.show_tienda_signal= None
        # Se inicializa la interfaz y las señales a usar
        self.init_gui()
        self.init_signals()
    def lista_mapa(self,lista_mapa):
        print (lista_mapa)

    def init_gui(self):
        ruta_imagen = {"O": path.join( "sprites",'mapa', 'tile006.png'),
                       "R": path.join( "sprites",'mapa', 'tile087.png'),
                       "T": path.join("sprites", 'mapa', 'store.png'),
                       "H": path.join("sprites",'mapa', 'house.png'),
                       "C": path.join( "sprites",'mapa', 'tile007.png')}
        """
        Método que inicializa los componentes visuales de la ventana.
        """
        self.setGeometry(100, 100, len(mapa[0])*30, len(mapa)*30)
        # Se setea la imagen de fondo.
        n = 30
        p = 0
        coordenadas_no_pisar=[]
        cantidad_tiendas = 0
        cantidad_casas = 0
        for c in mapa:
            t = 0
            for d in c:
                if (cantidad_tiendas == 3 or cantidad_casas == 3) and (d == "H" or d == "T"):
                    pixeles = QPixmap(ruta_imagen["O"])
                    self.label = QLabel(self)
                    self.label.setGeometry(QRect(n * t, n * p, n, n))
                    self.label.setPixmap(pixeles)
                    self.label.setScaledContents(True)
                    pixeles = QPixmap((ruta_imagen[d]))
                    self.label = QLabel(self)
                    self.label.setGeometry(QRect(n * (t - 1), n * (p - 1), 2 * n, 2 * n))
                    self.label.setPixmap(pixeles)
                    self.label.setScaledContents(True)
                    if cantidad_casas == 3:
                        cantidad_casas = 0
                    if cantidad_tiendas == 3:
                        cantidad_tiendas = 0
                else:
                    pixeles = QPixmap(ruta_imagen["O"])
                    self.label = QLabel(self)
                    self.label.setGeometry(QRect(n * t, n * p, n, n))
                    self.label.setPixmap(pixeles)
                    self.label.setScaledContents(True)
                    if d == "T":
                        cantidad_tiendas = cantidad_tiendas + 1
                    elif d == "H":
                        cantidad_casas = cantidad_casas + 1
                    else:
                        if d=="R":
                            coodenada=[]
                            coodenada.append(n * t)
                            coodenada.append(n * p)
                            coordenadas_no_pisar.append(coodenada)
                        pixeles = QPixmap(ruta_imagen[d])
                        self.label = QLabel(self)
                        self.label.setGeometry(QRect(n * t, n * p, n, n))
                        self.label.setPixmap(pixeles)
                        self.label.setScaledContents(True)
                t = t + 1
            p = p + 1
        print (coordenadas_no_pisar)
        # Se crea el personaje en el frontend.
        self.front_character = QLabel(self)
        self.current_sprite = QPixmap(self.sprites_paths[('stand', 'R')])
        self.front_character.setPixmap(self.current_sprite)
        self.front_character.move(0, 300)

    def init_signals(self):
        """
        Método que inicializa las señales a utilizar.
        """
        # Se conecta la señal para abrir esta ventana con el método show
        self.mapa_signal.connect(self.lista_mapa)
        self.show_game_signal.connect(self.show)
        # Se conecta la señal de actualización con un método
        self.update_window_signal.connect(self.update_window)
        # Define la señal que actualizará el personaje en back-end
        self.update_character_signal = self.backend_character.update_character_signal
        # Se le asigna al back-end la señal para actualizar esta ventana
        self.backend_character.update_window_signal = self.update_window_signal
        #####
        self.signal_tienda.connect(self.mostrar_tienda)


    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        """
        Actualiza el estado de animación de la imagen del personaje.
        Solo tiene 3 estados.
        :param value: int
        :return: None
        """
        self._frame = value if value < 3 else 1

    # Diccionario para asociar teclas con la acción del personaje
    key_event_dict = {
        Qt.Key_D: 'R',
        Qt.Key_A: 'L',
        Qt.Key_W: 'U',
        Qt.Key_S: 'D',
        Qt.Key_Right: 'R',
        Qt.Key_Left: 'L',
        Qt.Key_Up: 'U',
        Qt.Key_Down: 'D'
    }

    def keyPressEvent(self, event):
        """
        Dada la presión de una tecla se llama a esta función. Al
        apretarse una tecla chequeamos si está dentro de las teclas del
        control del juego y de ser así, se envía una señal al backend
        con la acción además de actualizar el sprite.
        :param event: QKeyEvent
        :return: None
        """
        if event.key() in self.key_event_dict:
            action = self.key_event_dict[event.key()]
            self.update_character_signal.emit(action)
        if event.key()==Qt.Key_L:
            print ("hola")
            self.hide()
            self.show_tienda_signal.emit()
    def mostrar_tienda(self):
        print ("hola")
        self.hide()
        self.show_tienda_signal.emit()

    def update_window(self, event):
        """
        Función que recibe un diccionario con la información del
        personaje y las actualiza en el front-end.
        :param event: dict
        :return: None
        """
        direction = event['direction']
        position = event['position']
        if position == 'walk':
            self.frame += 1
            self.current_sprite = QPixmap(self.sprites_paths[(position, direction, self.frame)])
        else:
            self.current_sprite = QPixmap(self.sprites_paths[(position, direction)])
        self.front_character.setPixmap(self.current_sprite)
        self.front_character.move(event["x"], event['y'])

    def update_from_backend(self, event):
        status = event['status']
        if status == 'move':
            self.move_snake_part(event)

        elif status == 'new_library':
            self.create_library(event)

    def create_library(self, event):
        library = QLabel('', self)
        library.setGeometry(event['location'])
        library.setPixmap(QPixmap(path.join('otros', 'axe.png')))
        self.libraries[event['coordenates']] = library
        library.show()