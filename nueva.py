import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt, pyqtSlot, QRect
import parametros_precios as p


window_name, base_class = uic.loadUiType("tienda.ui")
class Tienda(window_name, base_class):
    show_tienda_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_10.setText(str(p.PRECIO_SEMILLA_CHOCLOS))
        self.label_10.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_11.setText(str(p.PRECIO_SEMILLA_ALCACHOFAS))
        self.label_11.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_18.setText(str(p.PRECIO_ALACACHOFAS))
        self.label_18.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_19.setText(str(p.PRECIO_CHOCLOS))
        self.label_19.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_20.setText(str(p.PRECIO_LEÑA))
        self.label_20.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_21.setText(str(p.PRECIO_ORO))
        self.label_21.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_8.setText(str(p.PRECIO_HACHA))
        self.label_8.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_9.setText(str(p.PRECIO_AZADA))
        self.label_9.setStyleSheet("font: 20pt Comic Sans MS")
        self.label_23.setText(str(p.PRECIO_TICKET))
        self.label_23.setStyleSheet("font: 20pt Comic Sans MS")
        self.pushButton_9.clicked.connect(self.exit)
        self.show_tienda_signal.connect(self.show)
    def mostrar(self):
        self.show()
    def exit(self):
        '''
        Método para finalizar el programa
        '''
        self.close()
        self.show_game_signal.emit()



