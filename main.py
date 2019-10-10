import sys
from PyQt5.QtWidgets import QApplication
from ventana_inicial import MenuWindow
from game_window import GameWindow
from nueva import Tienda
from intento_crear_lista_mapa import Mapa

if __name__ == '__main__':
    app = QApplication([])
    mapa = Mapa()
    tienda = Tienda()
    menu_window = MenuWindow()
    game_window = GameWindow()
    menu_window.mandar_mapa_signal = mapa.mandar_mapa_signal
    game_window.show_tienda_signal = tienda.show_tienda_signal
    menu_window.show_game_signal = game_window.show_game_signal
    Tienda.show_game_signal = game_window.show_game_signal
    menu_window.show()
    sys.exit(app.exec_())
