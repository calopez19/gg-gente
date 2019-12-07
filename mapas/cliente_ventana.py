import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt, pyqtSlot, QRect
import re
import json
from os import path


window_name, base_class = uic.loadUiType("ventana_inicial2.ui")

class Interfaz(window_name, base_class):
    senal_a_backend = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.manejar_boton)
        self.pushButton_2.clicked.connect(self.entrar_sala_1)
        self.pushButton_3.clicked.connect(self.entrar_sala_2)
        self.pushButton_4.clicked.connect(self.entrar_sala_3)
        self.pushButton_5.clicked.connect(self.entrar_sala_4)
        self.pushButton_6.clicked.connect(self.salir)
        self.pushButton_7.clicked.connect(self.volver)
        self.textEdit.setVisible(False)
        self.textEdit_6.setVisible(False)
        self.textEdit_2.setVisible(False)
        self.textEdit_3.setVisible(False)
        self.textEdit_4.setVisible(False)
        self.textEdit_5.setVisible(False)
        # Para que se edite el texto correctamente, se conecta a una funcion
        # que se activará con cada edicion del QLineEdit
        self.lineEdit.textEdited.connect(self.editar_texto)
        self.volver_usuario()
        self.show()
    def manejar_boton(self):
        self.senal_a_backend.emit(self.lineEdit.text())
        self.lineEdit.setText("")
    def desplegar_resultado(self, dict):
        print (dict)

    def editar_texto(self):
        self.lineEdit.setText(re.sub(r"[#*<>\'&]", '', self.lineEdit.text()))
        if len(self.lineEdit.text()) is None: # Si no hay texto no se envía
            print (self.lineEdit.text() is None)
            self.pushButton.setEnabled(False)
        else:
            self.pushButton.setEnabled(True)
    def no_esta_usuario(self,str):
        self.label_3.setText(str)
        self.label_3.setStyleSheet("font: 10pt Comic Sans MS")
    def pasar_a_escoger_sala(self,dict):
        self.textEdit.setVisible(False)
        self.textEdit_2.setVisible(False)
        self.textEdit_3.setVisible(False)
        self.textEdit_4.setVisible(False)
        self.textEdit_5.setVisible(False)
        self.textEdit_6.setVisible(False)
        self.lineEdit.setVisible(False)
        self.label.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(True)
        self.label_5.setVisible(True)
        self.label_6.setVisible(True)
        self.label_7.setVisible(True)
        self.label_8.setVisible(True)
        self.label_9.setVisible(True)
        self.label_5.setText("quedan {} cupos en la sala".format(dict["cantidad_en_sala"][0]))
        self.label_5.setStyleSheet("font: 12pt Comic Sans MS")
        self.label_6.setText("quedan {} cupos en la sala".format(dict["cantidad_en_sala"][1]))
        self.label_6.setStyleSheet("font: 12pt Comic Sans MS")
        self.label_7.setText("quedan {} cupos en la sala".format(dict["cantidad_en_sala"][2]))
        self.label_7.setStyleSheet("font: 12pt Comic Sans MS")
        self.label_8.setText("quedan {} cupos en la sala".format(dict["cantidad_en_sala"][3]))
        self.label_8.setStyleSheet("font: 12pt Comic Sans MS")
        self.label_9.setText("Nombre de usuario: {}".format(dict["usuario"]))
        self.label_9.setStyleSheet("font: 12pt Comic Sans MS")
        self.label_11.setVisible(False)
        self.label_12.setVisible(False)
        self.label_14.setVisible(False)
        self.label_15.setVisible(False)
        self.label_14.setVisible(False)
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.pushButton_4.setVisible(True)
        self.pushButton_5.setVisible(True)
        self.pushButton_7.setVisible(True)
        pixeles = QPixmap(path.join("sprites", "personajes", dict["personaje"], 'wide.png'))
        self.label_4.setPixmap(pixeles)
    def entrar_sala_1(self):
        self.senal_a_backend.emit("sala_1")
    def entrar_sala_2(self):
        self.senal_a_backend.emit("sala_2")

    def entrar_sala_3(self):
        self.senal_a_backend.emit("sala_3")

    def entrar_sala_4(self):
        self.senal_a_backend.emit("sala_4")
    def pasar_a_sala(self,dict):
        self.label_4.setVisible(False)
        self.label_11.setVisible(False)
        self.label_12.setVisible(False)
        self.label_14.setVisible(False)
        self.label_13.setVisible(False)
        self.label_15.setVisible(False)
        self.lineEdit.setVisible(True)
        self.pushButton.setVisible(True)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.pushButton_3.setVisible(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_5.setVisible(False)
        pixeles = QPixmap(path.join("sprites", "fondos", '1.png'))
        self.label.setPixmap(pixeles)
        self.label.setScaledContents(True)
        self.label.setVisible(True)
        print ("que pasas")
        print (dict['estado_sala'])
        for c in dict['estado_sala']:
            print (c)
            if dict['estado_sala'][c]["label"] == 5:
                print ("llegamos hasta aqui")
                pixeles = QPixmap(
                    path.join("sprites", "personajes",
                              dict['estado_sala'][c]["personaje"], 'wide.png'))
                self.label_4.setPixmap(pixeles)
                self.label_4.setVisible(True)
                self.textEdit.setVisible(True)
                if "ultimo_mensaje" in dict['estado_sala'][c]:
                    self.textEdit.setText(dict['estado_sala'][c]["ultimo_mensaje"])
                pass
            elif dict['estado_sala'][c]["label"] == 4:
                pixeles2 = QPixmap(
                    path.join("sprites", "personajes",
                              dict['estado_sala'][c]["personaje"], 'wide.png'))
                self.label_11.setPixmap(pixeles2)
                self.label_11.setVisible(True)
                self.textEdit_2.setVisible(True)
                if "ultimo_mensaje" in dict['estado_sala'][c]:
                    self.textEdit_2.setText(dict['estado_sala'][c]["ultimo_mensaje"])
            elif dict['estado_sala'][c]["label"] == 3:
                pixeles3 = QPixmap(
                    path.join("sprites", "personajes",
                              dict['estado_sala'][c]["personaje"], 'wide.png'))
                self.label_12.setPixmap(pixeles3)
                self.label_12.setVisible(True)
                self.textEdit_3.setVisible(True)
                if "ultimo_mensaje" in dict['estado_sala'][c]:
                    self.textEdit_3.setText(dict['estado_sala'][c]["ultimo_mensaje"])
            elif dict['estado_sala'][c]["label"] == 2:
                pixeles4 = QPixmap(
                    path.join("sprites", "personajes",
                              dict['estado_sala'][c]["personaje"], 'wide.png'))
                self.label_13.setPixmap(pixeles4)
                self.label_13.setVisible(True)
                self.textEdit_4.setVisible(True)
                if "ultimo_mensaje" in dict['estado_sala'][c]:
                    self.textEdit_4.setText(dict['estado_sala'][c]["ultimo_mensaje"])
            elif dict['estado_sala'][c]["label"] == 1:
                pixeles4 = QPixmap(
                    path.join("sprites", "personajes",
                              dict['estado_sala'][c]["personaje"], 'wide.png'))
                self.label_15.setPixmap(pixeles4)
                self.label_15.setVisible(True)
                self.textEdit_5.setVisible(True)
                if "ultimo_mensaje" in dict['estado_sala'][c]:
                    self.textEdit_5.setText(dict['estado_sala'][c]["ultimo_mensaje"])
    def salir(self):
        self.close()
    def volver(self):
        self.senal_a_backend.emit("volver")
    def volver_usuario(self):
        self.label.setVisible(False)
        self.label_2.setVisible(True)
        self.lineEdit.setText("")
        self.lineEdit.setVisible(True)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.label_14.setVisible(True)
        self.pushButton.setVisible(True)
        self.pushButton_2.setVisible(False)
        self.pushButton_3.setVisible(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(True)
        self.pushButton_7.setVisible(False)
if __name__ == '__main__':
    app = QApplication([])

    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    front = Interfaz()

    sys.exit(app.exec_())