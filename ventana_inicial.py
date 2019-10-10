import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt, pyqtSlot, QRect

window_name, base_class = uic.loadUiType("ventana_inicial.ui")
print( os.path.isfile(os.path.join("mapas", "mapa_2.txt")))

class MenuWindow(window_name, base_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.game_control)
        self.mapa = self.lineEdit.text()
        self.mandar_mapa_signal=None
    def game_control(self):
        print ("ff")
        mapa= self.lineEdit.text()
        if os.path.isfile(os.path.join("mapas", str(mapa))):
            print ("gg")
            self.mandar_mapa_signal.emit(mapa)
            self.hide()
            self.show_game_signal.emit()



