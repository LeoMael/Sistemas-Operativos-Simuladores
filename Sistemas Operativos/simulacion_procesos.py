import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen
from collections import deque
from queue import PriorityQueue
import random

class Worker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._stop = False

    def run(self):
        self._stop = False
        for i in range(101):
            if self._stop:
                break
            self.progress.emit(i)
            self.sleep(0.005)
        self.finished.emit()

    def stop(self):
        self._stop = True

    def sleep(self, seconds):
        import time
        time.sleep(seconds)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.dx_pos=1700
        self.dy_pos=900
        # Establece el tamaño de la ventana
        self.setGeometry(100, 100,self.dx_pos, self.dy_pos)
        self.setWindowTitle('SIMULACION DE PROCESOS Y REPRESENTACION DE RAM')

        self.Datos = {}
        self.option_global="CPU"
        self.tipo_cola = "unica"
        self.tipo_ram = "fisrt"
        self.Proceso_prim(self.option_global)
        #self.dibujar_prim()
        
        # Cambia el color de fondo de la ventana
        self.setStyleSheet("background-color: rgb(23, 25, 23 );")
        # Mostrar la ventana
        self.show()
    
    def dibujar_prim(self):
        self.estilos()
        self.grafica()
        self.botones()
        self.entradas()
        
        if self.option_global == "CPU":
            self.dibujar_CPU()
        elif self.option_global == "RAM":
            self.dibujar_RAM()
            
        self.lineas()
        self.tabla1()
        self.click_boton()
        
        #self.tabla2()
    def dibujar_CPU(self):

        self.botones_CPU()
        

        #self.tabla2()
    def dibujar_RAM(self):

        self.botones_RAM()
        self.entradas_RAM()
        self.grafico_RAM()
        
    
    def click_boton(self):
        self.Agregar.clicked.connect(self.aux)
        self.ELIMINAR.clicked.connect(self.delet)
        if self.option_global == "CPU":

            self.FCFS.clicked.connect(lambda: self.procesar("FCFS"))
            self.SRT.clicked.connect(lambda: self.procesar("SRT"))
    
        self.CPU.clicked.connect(lambda: self.Proceso_prim("CPU"))
        self.RAM.clicked.connect(lambda: self.Proceso_prim("RAM"))

        if self.option_global == "RAM":
            
            self.AgregarP.clicked.connect(self.agregar_Par)
            self.deleteP.clicked.connect(self.delete_Par)

            self.COLA.clicked.connect(lambda: self.definir_ram("unica"))
            self.MULTI.clicked.connect(lambda: self.definir_ram("multi"))

            self.FISRT.clicked.connect(lambda: self.definir_ram_model("fisrt"))
            self.BEST.clicked.connect(lambda: self.definir_ram_model("best"))
            self.WORST.clicked.connect(lambda: self.definir_ram_model("worst"))

        
    def Proceso_prim(self, option):
        if option=="CPU":
            if self.option_global == "RAM":
                self.delet_all()
            self.textos = ['PROCESO', 'TIEMPO LL.', 'TIEMPO E.']
        elif option=="RAM":
            self.Particion = []
            if self.option_global == "CPU":
                self.delet_all()
            self.textos = ['PROCESO', 'MEMORIA', 'TIEMPO E.']
            
        self.option_global=option
        
        self.actualizar()
        
    def estilos(self):
        # Define el estilo para los textos
        fontsize = int(self.dy_pos * 0.025)
        self.estilo_text = f"color: rgba(91, 242, 226, 1); font-size: {fontsize}px;"
        self.estilo_Input = "background-color: rgb(230, 233, 230 );"

        # Define los estilos para el estado normal y el estado hover del botón
        self.estilo_normal = "QPushButton { background-color: rgba(255, 255, 255, 2); color: rgb(205, 207, 209); border: 1px solid rgb(205, 207, 209);}"
        self.estilo_hover = "QPushButton:hover { background-color: rgba(7, 73, 143, 2); color: white; border: 2px solid rgb(237, 239, 241 );}"
        # Define los estilos para el estado pressed (presionado) del botón
        self.estilo_pressed = "QPushButton:pressed { background-color: rgb(164, 165, 166 ); border-style: inset; }"
        
        self.estilo_hoverE = "QPushButton:hover { background-color: rgba(200, 73, 143, 2); color: white; border: 2px solid rgb(237, 23, 24 );}"
        self.estilo_hoverA = "QPushButton:hover { background-color: rgba(7, 73, 143, 2); color: white; border: 2px solid rgb(23, 239, 24 );}"

    def botones(self):
        # Botón AGREGAR
        self.Agregar = QPushButton('AGREGAR', self)
        px_botonA = int(self.dx_pos * 0.18)
        py_botonA = int(self.dy_pos * 0.30)
        self.Agregar.setGeometry(px_botonA, py_botonA, int(self.dx_pos * 0.08), int(self.dy_pos * 0.05))

        # Botón ELIMINAR
        self.ELIMINAR = QPushButton('ELIMINAR', self)
        self.px_botonE = int(self.dx_pos * 0.60)
        self.py_botonE = int(self.dy_pos * 0.40)
        self.ELIMINAR.setGeometry(self.px_botonE - 10, self.py_botonE - 4, int(self.dx_pos * 0.07), int(self.dy_pos * 0.04))

        # Establecer estilos
        self.Agregar.setStyleSheet(self.estilo_normal + self.estilo_hoverA + self.estilo_pressed)
        self.ELIMINAR.setStyleSheet(self.estilo_normal + self.estilo_hoverE + self.estilo_pressed)

        # Botones CPU y RAM
        self.py_boton = int(self.dy_pos * 0.35)
        self.CPU = QPushButton('CPU', self)
        px_boton_cpu = int(self.dx_pos * 0.08)
        self.CPU.setGeometry(px_boton_cpu, self.py_boton, int(self.dx_pos * 0.08), int(self.dy_pos * 0.04))

        self.RAM = QPushButton('RAM', self)
        px_boton_ram = int(self.dx_pos * 0.28)
        self.RAM.setGeometry(px_boton_ram, self.py_boton, int(self.dx_pos * 0.08), int(self.dy_pos * 0.04))

        # Establecer estilos
        self.CPU.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.RAM.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)


    def botones_CPU(self):
        # Crea un botón
        self.py_boton=int(self.dy_pos*(51/100))

        self.FCFS = QPushButton('FCFS', self)
        px_boton=int(self.dx_pos*(25/100))
        self.FCFS.setGeometry(px_boton, self.py_boton, 100, 30)  # x-pos, y-pos, width, height
        # boton.setStyleSheet("background-color: rgb(7, 73, 143 );")

        self.FJS = QPushButton('FJS', self)
        px_boton1=int(self.dx_pos*(8/100))
        self.FJS.setGeometry(px_boton1, self.py_boton, 100, 30)  # x-pos, y-pos, width, height

        # Crea un botón
        self.py_boton=int(self.dy_pos*(46/100))

        self.SRT = QPushButton('SRT', self)
        px_boton=int(self.dx_pos*(25/100))
        self.SRT.setGeometry(px_boton, self.py_boton, 100, 30)  # x-pos, y-pos, width, height
        # boton.setStyleSheet("background-color: rgb(7, 73, 143 );")

        self.RR = QPushButton('RR', self)
        px_boton1=int(self.dx_pos*(8/100))
        self.RR.setGeometry(px_boton1, self.py_boton, 100, 30)  # x-pos, y-pos, width, height

        self.FCFS.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.FJS.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.SRT.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.RR.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        
    def botones_RAM(self):
        # Crea un botón
        self.py_boton=int(self.dy_pos*(40/100))

        self.AgregarP = QPushButton('AGREGAR_p', self)
        px_boton=int(self.dx_pos*(8/100))
        self.AgregarP.setGeometry(px_boton-20, self.py_boton, 100, 30)  # x-pos, y-pos, width, height
        # boton.setStyleSheet("background-color: rgb(7, 73, 143 );")

        self.deleteP = QPushButton('ELIMINAR_p', self)
        px_boton1=int(self.dx_pos*(25/100))
        self.deleteP.setGeometry(px_boton1+20, self.py_boton, 100, 30)  # x-pos, y-pos, width, height


        # Crea un botón
        self.py_boton=int(self.dy_pos*(46/100))
        
        self.COLA = QPushButton('COLA UNICA', self)
        px_boton=int(self.dx_pos*(25/100))
        self.COLA.setGeometry(px_boton, self.py_boton, 100, 30)  # x-pos, y-pos, width, height
        # boton.setStyleSheet("background-color: rgb(7, 73, 143 );")

        self.MULTI = QPushButton('MULTICOLA', self)
        px_boton1=int(self.dx_pos*(8/100))
        self.MULTI.setGeometry(px_boton1, self.py_boton, 100, 30)  # x-pos, y-pos, width, height


        # Crea un botón
        self.py_boton=int(self.dy_pos*(51/100))

        self.FISRT = QPushButton('FIRST', self)
        px_boton1=int(self.dx_pos*(8/100))
        self.FISRT.setGeometry(px_boton1-40, self.py_boton, 100, 30)  # x-pos, y-pos, width, height

        self.BEST = QPushButton('BEST', self)
        px_boton=int(self.dx_pos*(25/100))
        self.BEST.setGeometry(px_boton+40, self.py_boton, 100, 30)  # x-pos, y-pos, width, height
        # boton.setStyleSheet("background-color: rgb(7, 73, 143 );")

        self.WORST = QPushButton('WORST', self)
        px_boton1=int(self.dx_pos*(8/100))
        self.WORST.setGeometry(px_boton1+75, self.py_boton, 100, 30)  # x-pos, y-pos, width, height


        self.FISRT.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.BEST.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.WORST.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)

        self.AgregarP.setStyleSheet(self.estilo_normal + self.estilo_hoverA + self.estilo_pressed)
        self.deleteP.setStyleSheet(self.estilo_normal + self.estilo_hoverE + self.estilo_pressed)

        self.COLA.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
        self.MULTI.setStyleSheet(self.estilo_normal + self.estilo_hover + self.estilo_pressed)
            
    def entradas_RAM(self):
        self.py_boton=int(self.dy_pos*(40/100))
        px_boton=int(self.dx_pos*(8/100))

        self.entrada_texto_R = QLineEdit(self)
        self.entrada_texto_R.setGeometry(px_boton+90, self.py_boton, 70, 30)  # x-pos, y-pos, width, height
        self.entrada_texto_R.setStyleSheet(self.estilo_Input) 
 

    def entradas(self):
        # Crea una lista de textos
        texto_ix = int(self.dx_pos*(10/100))
        texto_iy = int((self.dy_pos*(10/100)))
        # Crea y configura las etiquetas de texto
        for i, texto in enumerate(self.textos):
            etiqueta = QLabel(texto, self)
            etiqueta.setGeometry( texto_ix, texto_iy+(i*50), 100, 30) # x-pos, y-pos, width, height
            etiqueta.setStyleSheet(self.estilo_text)
            print(i)

        # Crea una lista para almacenar las entradas de texto
        self.entradas_texto = []
        
        # Crea una entrada de texto
        for i in range(3):
            entrada_texto = QLineEdit(self)
            entrada_texto.setGeometry(texto_ix + 150, texto_iy+(i*50), 150, 30)  # x-pos, y-pos, width, height
            entrada_texto.setStyleSheet(self.estilo_Input) 
            # Agrega la entrada de texto a la lista
            self.entradas_texto.append(entrada_texto)

        #eliminar
        self.entrada_textoE = QLineEdit(self)
        self.entrada_textoE.setGeometry(self.px_botonE+120, self.py_botonE, 100, 30)  # x-pos, y-pos, width, height
        self.entrada_textoE.setStyleSheet(self.estilo_Input)

    def lineas(self):
         # Crea una línea GENERALES

        linea = QFrame(self)
        linea.setGeometry(int(self.dx_pos*(1/100)), int(self.dy_pos/2)-int((self.dy_pos*(5/100))), int(self.dx_pos*(98/100)), 3)  # x-pos, y-pos, width, height
        linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
        linea.setFrameShape(QFrame.HLine)  # Establece el tipo de línea horizontal
        
        # Crea una línea
        lineav = QFrame(self)
        lineav.setGeometry(int(self.dx_pos/2), int(self.dy_pos*1/100), 2, int(self.dy_pos*(98/100)))  # x-pos, y-pos, width, height
        lineav.setStyleSheet("background-color: rgb(94, 95, 94 );")
        lineav.setFrameShape(QFrame.HLine)  # Establece el tipo de línea vertical

    def tabla1(self):
        ini_x = int(self.dx_pos * 0.55)
        ini_y = int(self.dy_pos * 0.05)
        width_x = int(self.dx_pos * 0.40)
        height_y = int(self.dy_pos * 0.008)
        separacion_x = int(self.dx_pos * 0.10)
        separacion_x_tex = int(self.dx_pos * 0.035)
        separacion_y = int(self.dy_pos * 0.035)
        fontsize = int(self.dy_pos * 0.019)
        estilo_text = f"color: rgba(91, 242, 226, 1); font-size: {fontsize}px; background-color: rgba(0,0,0,0)"
        
        # Dibujar líneas horizontales
        for i in range(2):
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + i * separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
        
        # Dibujar los encabezados de la tabla
        for i, texto in enumerate(self.textos):
            etiqueta = QLabel(texto, self)
            etiqueta.setGeometry(ini_x + separacion_x * i + separacion_x_tex, ini_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta.setStyleSheet(estilo_text)
            etiqueta.show()

        ini_y += separacion_y
        ini_y_text = ini_y - int(self.dy_pos * 0.03)
        separacion_x_tex2 = int(self.dx_pos * 0.12)
        
        # Dibujar líneas horizontales para cada dato
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
            ini_y += separacion_y

        # Dibujar las letras de datos ingresados
        for clave, valor in self.Datos.items():
            etiqueta_clave = QLabel(clave, self)
            etiqueta_clave.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_clave.setStyleSheet(estilo_text)
            etiqueta_clave.show()

            # Separar el valor en dos partes
            parte1, parte2 = valor

            # Crear etiquetas para cada parte del valor
            etiqueta_valor1 = QLabel(str(parte1), self)
            etiqueta_valor1.setGeometry(ini_x + separacion_x_tex2, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_valor1.setStyleSheet(estilo_text)
            etiqueta_valor1.show()

            etiqueta_valor2 = QLabel(str(parte2), self)
            etiqueta_valor2.setGeometry(ini_x + 2 * separacion_x_tex2, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_valor2.setStyleSheet(estilo_text)
            etiqueta_valor2.show()

            ini_y_text += separacion_y


    def tabla2(self):
        self.textos2 = [' ', 'T. DE RETORNO', 'T. ESPERA']
        ini_x = int(self.dx_pos * 0.55)
        ini_y = int(self.dy_pos * 0.55)
        width_x = int(self.dx_pos * 0.40)
        height_y = int(self.dy_pos * 0.008)
        separacion_x = int(self.dx_pos * 0.10)
        separacion_x_tex = int(self.dx_pos * 0.035)
        separacion_y = int(self.dy_pos * 0.035)
        fontsize = int(self.dy_pos * 0.019)
        estilo_text = f"color: rgba(91, 242, 226, 1); font-size: {fontsize}px; background-color: rgba(0,0,0,0)"
        
        # Dibujar líneas horizontales
        for i in range(2):
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
        
        # Dibujar los encabezados de la tabla
        for i, texto in enumerate(self.textos2):
            etiqueta = QLabel(texto, self)
            etiqueta.setGeometry(ini_x + separacion_x * i + separacion_x_tex, ini_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta.setStyleSheet(estilo_text)
            etiqueta.show()

        ini_y += separacion_y
        ini_y_text = ini_y - int(self.dy_pos * 0.03)
        separacion_x_tex2 = int(self.dx_pos * 0.12)
        
        # Dibujar líneas horizontales para cada dato
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
            ini_y += separacion_y

        # Dibujar las letras
        tr = self.TR
        te = self.TE
        ini_y_text2 = ini_y_text
        for clave, valor in self.Datos.items():
            etiqueta_clave = QLabel(clave, self)
            etiqueta_clave.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_clave.setStyleSheet(estilo_text)
            etiqueta_clave.show()
            ini_y_text += separacion_y

        promedio_tr = sum(tr) / (len(tr) if len(tr) > 0 else 1)
        promedio_te = sum(te) / (len(te) if len(te) > 0 else 1)

        # Dibujar los valores de tiempo de retorno y tiempo de espera
        for i in range(len(tr)):
            self.etiqueta_valor1 = QLabel(str(tr[i]), self)
            self.etiqueta_valor1.setGeometry(ini_x + separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            self.etiqueta_valor1.setStyleSheet(estilo_text)
            self.etiqueta_valor1.show()

            self.etiqueta_valor2 = QLabel(str(te[i]), self)
            self.etiqueta_valor2.setGeometry(ini_x + 2 * separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            self.etiqueta_valor2.setStyleSheet(estilo_text)
            self.etiqueta_valor2.show()

            ini_y_text2 += separacion_y

        # Dibujar la línea horizontal final y los valores promedio
        linea = QFrame(self)
        linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
        linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
        linea.setFrameShape(QFrame.HLine)
        linea.show()

        etiqueta_promedio = QLabel("Promedio", self)
        etiqueta_promedio.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_promedio.setStyleSheet(estilo_text)
        etiqueta_promedio.show()

        etiqueta_tr = QLabel(str(promedio_tr), self)
        etiqueta_tr.setGeometry(ini_x + separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_tr.setStyleSheet(estilo_text)
        etiqueta_tr.show()

        etiqueta_te = QLabel(str(promedio_te), self)
        etiqueta_te.setGeometry(ini_x + 2 * separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_te.setStyleSheet(estilo_text)
        etiqueta_te.show()

    def tabla3(self):
        self.textos2 = ['   ', 'T. DE RETORNO', 'T. ESPERA']
        ini_x = int(self.dx_pos * 0.55)
        ini_y = int(self.dy_pos * 0.55)
        width_x = int(self.dx_pos * 0.40)
        height_y = int(self.dy_pos * 0.008)
        separacion_x = int(self.dx_pos * 0.10)
        separacion_x_tex = int(self.dx_pos * 0.035)
        separacion_y = int(self.dy_pos * 0.035)
        fontsize = int(self.dy_pos * 0.019)
        estilo_text = f"color: rgba(91, 242, 226, 1); font-size: {fontsize}px; background-color: rgba(0,0,0,0)"

        # Dibujar líneas horizontales iniciales
        for i in range(2):
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + i * separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()

        # Dibujar los encabezados de la tabla
        for i, texto in enumerate(self.textos2):
            etiqueta = QLabel(texto, self)
            etiqueta.setGeometry(ini_x + separacion_x * i + separacion_x_tex, ini_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta.setStyleSheet(estilo_text)
            etiqueta.show()

        ini_y += separacion_y
        ini_y_text = ini_y - int(self.dy_pos * 0.03)
        separacion_x_tex2 = int(self.dx_pos * 0.12)

        # Dibujar líneas horizontales para cada dato
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
            ini_y += separacion_y

        # Dibujar las letras
        tr = self.TR
        te = self.TE
        ini_y_text2 = ini_y_text
        for i, clave in enumerate(self.datos4.keys() & self.TRR.keys()):
            etiqueta_clave = QLabel(clave, self)
            etiqueta_clave.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_clave.setStyleSheet(estilo_text)
            etiqueta_clave.show()
            ini_y_text += separacion_y

        promedio_tr = 0
        promedio_te = 0
        for i, clave in enumerate(self.datos4.keys() & self.TRR.keys()):
            valor1 = self.datos4[clave]
            valor2 = self.TRR[clave]
            if clave == "P0":
                valor2 -= 1

            etiqueta_valor1 = QLabel(str(valor2), self)
            etiqueta_valor1.setGeometry(ini_x + separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_valor1.setStyleSheet(estilo_text)
            etiqueta_valor1.show()

            etiqueta_valor2 = QLabel(str(valor1), self)
            etiqueta_valor2.setGeometry(ini_x + 2 * separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_valor2.setStyleSheet(estilo_text)
            etiqueta_valor2.show()

            ini_y_text2 += separacion_y
            promedio_tr += float(valor2)
            promedio_te += float(valor1)

        dd = len(self.Datos) if self.Datos else 1
        promedio_tr /= float(dd)
        promedio_te /= float(dd)

        etiqueta_promedio = QLabel("Promedio", self)
        etiqueta_promedio.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_promedio.setStyleSheet(estilo_text)
        etiqueta_promedio.show()

        # Dibujar la línea horizontal final y los valores promedio
        linea = QFrame(self)
        linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
        linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
        linea.setFrameShape(QFrame.HLine)
        linea.show()

        etiqueta_tr = QLabel(str(promedio_tr), self)
        etiqueta_tr.setGeometry(ini_x + separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_tr.setStyleSheet(estilo_text)
        etiqueta_tr.show()

        etiqueta_te = QLabel(str(promedio_te), self)
        etiqueta_te.setGeometry(ini_x + 2 * separacion_x_tex2, ini_y_text2 + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_te.setStyleSheet(estilo_text)
        etiqueta_te.show()

    def tabla4(self):
        print("tabla4")
        
    def grafica(self):
        white = QWidget(self)
        white.setGeometry(0, int(self.dy_pos/2)-int((self.dy_pos*(5/100))), int(self.dx_pos/2), 500)
        white.setStyleSheet(f"background-color:  rgb(35,35,35); border: 1px solid black;")
        self.dxi = 50 #lado izquierdo del grafico
        self.dxf = int((self.dx_pos*40/100))
        
        self.dyi = 50+int(self.dy_pos/2)
        dyf = 200

        height = int(self.dy_pos*(40/100))
        
        cant = 1 if len(self.Datos) == 0 else len(self.Datos) 

        self.division = height/cant

        linea = QFrame(self)
        linea.setGeometry(self.dxi, self.dyi, 2, height)  # x-pos, y-pos, width, height
        linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
        linea.setFrameShape(QFrame.HLine)  # Establece el tipo de línea horizontal

        linea = QFrame(self)
        linea.setGeometry(self.dxi, self.dyi+int(self.dy_pos*(40/100)), self.dxf, 3)  # x-pos, y-pos, width, height
        linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
        linea.setFrameShape(QFrame.HLine)  # Establece el tipo de línea horizontal

        self.suma_segundo_valor_ejecucion = 1 if sum(int(valor[1]) for valor in self.Datos.values()) == 0 else sum(int(valor[1]) for valor in self.Datos.values())

        self.d_width = int(self.dxf/self.suma_segundo_valor_ejecucion)
        print(self.suma_segundo_valor_ejecucion)


        estilo_text = "color: rgba(91, 242, 226, 1); font-size: 12px; background-color: rgba(0,0,0,0)"
        self.puntos = []
        self.puntosY = []
        self.puntosY_letras = {}
        p_final = {}
        #letras verticales
        for i, (clave, valor) in enumerate(self.Datos.items()):
            self.etiqueta_clave = QLabel(clave, self)
            self.etiqueta_clave.setGeometry(self.dxi-20, self.dyi+int( (self.division*i) + 25), 30, 16)  # x-pos, y-pos, width, height
            self.etiqueta_clave.setStyleSheet(estilo_text)
            self.puntos.append((self.dxi, self.dyi + int(self.division * i)))
            self.puntosY.append((self.dxi, self.dyi+(self.division*i)))
            self.puntosY_letras[clave]=( (self.dyi + int(self.division * i)) )

        self.puntosX  = []
        #numero horizontales
        for i in range(self.suma_segundo_valor_ejecucion+1):
            self.etiqueta_clave = QLabel(str(i), self)
            self.etiqueta_clave.setGeometry(self.dxi+int(i*self.d_width), self.dyi+int(self.dy_pos*(40/100))+10, 20, 10)  # x-pos, y-pos, width, height
            self.etiqueta_clave.setStyleSheet(estilo_text)
            self.puntosX.append(self.dxi+int(i*self.d_width))
            
            linea = QFrame(self)
            linea.setGeometry(self.dxi+int(i*self.d_width), self.dyi, 1, int(self.dy_pos*(40/100)))
            linea.setStyleSheet("background-color: rgb(200,200,200);")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
            
        for punto in self.puntos:
            print(punto[0], punto[1])

    def startProgress(self):
        #self.startButton.setEnabled(False)
        #self.FCFS.setEnabled(False)
        for progressBar in self.progressBars:
            progressBar.setValue(0)
        self.currentIndex = 0
        self.workers[self.currentIndex].start()

    def startNextProgress(self):
        self.currentIndex += 1
        if self.currentIndex < len(self.Datos):
            self.workers[self.currentIndex].start()
        else:
            self.FCFS.setEnabled(True)

    def barras(self):
        print("f")

    def stopProgress(self):
        for worker in self.workers:
            worker.stop()
            
    def cal_tre(self):
        self.Datos_ordenados = dict(sorted(self.Datos.items(), key=lambda x: x[1], reverse=True))
        #self.Datos_ordenados = self.Datos
        ocupado = 0
        tiempo_eje = 0
        self_tiempo_llegada = []
        self_tiempo_retorno = []
        self_tiempo_espera = []
        self.Datos2 = {}
        clave = deque()
        tesp = 0
        
        otro = sum(int(valor[0]) for valor in self.Datos.values())
        if(otro>self.suma_segundo_valor_ejecucion):
            self.xd=otro+max(int(valor[1]) for valor in self.Datos.values())
        else:
            self.xd=self.suma_segundo_valor_ejecucion+1
        for i in range(self.xd):
            if self.Datos_ordenados:
                #ultima_clave, ultimos_valores = self.Datos_ordenados.popitem()
                ultima_clave = list(self.Datos_ordenados.keys())[-1]
                ultimos_valores = self.Datos[ultima_clave]
                print("Última clave:", ultima_clave)
                print("Últimos valores:", ultimos_valores)
                part1, part2 = ultimos_valores
                print("llegada", part1)
                print(" ejecucion", part2)
                if part1==i:
                    clave.append(ultima_clave)
                    A = self.Datos_ordenados.popitem()
           
            print(clave)
            if tiempo_eje==0:
                
                if ocupado == 1:
                    print("entroo")
                    primer_elemento = clave.popleft()
                    valores = self.Datos[primer_elemento]
                    part1, part2 = valores
                    mm = tesp-int(part1)
                    if mm < 0:
                        mm=0
                    
                    self.Datos2[primer_elemento]=(i-int(part1),mm )
                    tesp = i
                
                ocupado = 0
                if clave:

                    primer_elemento = clave[0]
                    print(primer_elemento)
                    valores = self.Datos[str(primer_elemento)]
                    part1, part2 = valores
                    tiempo_eje = int(part2)
                    ocupado = 1

            if ocupado == 1:
                tiempo_eje-=1

            
        for nombre, valor in self.Datos2.items():
            print(f"Clave: {nombre}, Valor: {valor}")

        print("helo")
        #ultimo_valor = list(self.Datos_ordenados.items())[-1][1]
        
        #print("daaaaaaaaa", ultimo_valor)
        #for i in range(self.suma_segundo_valor_ejecucion):
            #print(i)
    def timeWait(self):
        # Creamos una lista temporal para almacenar los elementos de la cola de prioridad original
        temp_list = []

        # Vaciamos la cola original y almacenamos los elementos en la lista temporal
        while not self.cola_prioridad.empty():
            elemento = self.cola_prioridad.get()
            temp_list.append(elemento)
        aax = 0
        # Iteramos sobre la lista temporal y procesamos los elementos
        for numero, nombre in temp_list:
            # Realizar las operaciones que necesites con los elementos de la cola
            if aax == 1:
                print(numero, nombre)
                self.datos4[nombre] += 1
            else:
                aax=1
        # Volvemos a agregar los elementos a la cola original
        for elemento in temp_list:
            self.cola_prioridad.put(elemento)


    def disminuir_numero(self, i):
        if not self.cola_prioridad.empty():
            self.timeWait()
            numero, nombre = self.cola_prioridad.get()
          
            numero -= 1
            if numero > 0:
                self.cola_prioridad.put((numero, nombre))
                if self.last != nombre:
                    print("cambio", i)
                    self.grafica_barr(i)
                    self.graf_i = i
                    self.last = nombre
                return 1
            else:
                part_1, part_2 = self.Datos[nombre]
                self.TRR[nombre] = i+1-part_1
                self.grafica_barr(i)
                self.graf_i = i
                self.last = nombre
                return 0
            
    def grafica_barr(self, i):

        progressBar = QProgressBar(self)
        progressBar.setGeometry( int(self.puntosX[self.graf_i]), int(self.puntosY_letras[self.last]), int(self.puntosX[i]-self.puntosX[self.graf_i]), int(self.division) )
        # Establecer el color de fondo de la barra de progreso
        progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(9, 95, 200); }")
        progressBar.setMaximum(100)
        self.progressBars.append(progressBar)

        worker = Worker()
        worker.progress.connect(progressBar.setValue)
        worker.finished.connect(self.startNextProgress)
        self.workers.append(worker)
            
        progressBar.show()
        
    def SPN(self):
        print("spm")


    def SRTt(self):
        self.Datos_ordenados = dict(sorted(self.Datos.items(), key=lambda x: x[1], reverse=True))
        #self.Datos_ordenados = self.Datos
        self.Datos3 = self.Datos
        self.datos4 = {}
        self.TRR = {}
        clave = deque()
        self.cola_prioridad = PriorityQueue()
        
        otro = sum(int(valor[0]) for valor in self.Datos.values())
        if(otro>self.suma_segundo_valor_ejecucion):
            self.xd=otro+max(int(valor[1]) for valor in self.Datos.values())
        else:
            self.xd=self.suma_segundo_valor_ejecucion+1

        for i in range(self.xd):
            print("fsffa", i)
            
            if self.Datos_ordenados:
                #ultima_clave, ultimos_valores = self.Datos_ordenados.popitem()
                ultima_clave = list(self.Datos_ordenados.keys())[-1]
                ultimos_valores = self.Datos[ultima_clave]
                print("Última clave:", ultima_clave)

                print("Últimos valores:", ultimos_valores)
                part1, part2 = ultimos_valores
                print("llegada", part1)
                print(" ejecucion", part2)
                if part1==i:
                    clave.append(ultima_clave)  #part1 = llegada, part2 = ejecucion
                    self.datos4[ultima_clave]=0
                    self.cola_prioridad.put((part2, ultima_clave))
                    A = self.Datos_ordenados.popitem()
                    
                    if i==0:
                        self.last = ultima_clave
                        print("inicioooo", i)
                        self.graf_i = i
            if not i==0:
                if not self.disminuir_numero(i):
                    self.graf_i = i-1
                    print("se hizo pop")
        self.startProgress()           
            
        for clave, valor in self.datos4.items():
            print(clave, valor)
        
        for clave, valor in self.TRR.items():
            print(clave, valor)

        for clave in self.datos4.keys() & self.TRR.keys():
            print(clave, self.datos4[clave], self.TRR[clave])

        print("srt")
        #ultimo_valor = list(self.Datos_ordenados.items())[-1][1]
        
        #print("daaaaaaaaa", ultimo_valor)
        #for i in range(self.suma_segundo_valor_ejecucion):
            #print(i)

    def procesar(self, op):
        self.actualizar()
        if len(self.Datos)==0:
            return
        self.Dato_graf = {}
        self.TR = []
        self.TE = []
        self.progressBars = []
        self.workers = []
        if op=="FCFS":
            print("FCFS")

            r_tf = 0
            tf_ant = [0]
            rango=self.puntos[0][0]

            for i, (clave, valor) in enumerate(self.Datos.items()):

                self.TE.append(tf_ant[i]-valor[0])

                print(valor[1], self.d_width)

                aux=int( int(valor[1]) * self.d_width)

                print(aux)

                progressBar = QProgressBar(self)
                progressBar.setGeometry(rango, int(self.puntos[i][1]), aux+35, int(self.division))

                linea = QFrame(self)
                linea.setGeometry(rango+aux, int(self.puntos[i][1])+int(self.division), 1, self.dyi+int(self.dy_pos*(40/100))-int(self.puntos[i][1])-int(self.division))  # x-pos, y-pos, width, height
                linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
                linea.setFrameShape(QFrame.HLine)  # Establece el tipo de línea horizontal

                r_tf+= int(valor[1])
                self.TR.append(r_tf-valor[0])
                print("TIEMPO: ", r_tf-valor[0])
                x_tf = (self.suma_segundo_valor_ejecucion*(rango+aux))/self.dxf
                print("valor", x_tf)
                
                
                tf_ant.append(r_tf)

                
                print("TIEMPO esp: ", tf_ant)
                #print(self.puntos[i][0], self.puntos[i][1])
                #print(int((valor[1]) * self.d_width))
                progressBar.setMaximum(100)
                self.progressBars.append(progressBar)

                worker = Worker()
                worker.progress.connect(progressBar.setValue)
                worker.finished.connect(self.startNextProgress)
                self.workers.append(worker)
                
                progressBar.show()
                linea.show()
                rango+=aux
            print("te:", self.TE)
            self.tabla2()
            self.startProgress()
            

            #self.Dato_graf = dict(sorted(self.Datos.items(), key=lambda item: item[1][0]))

            #print(self.Dato_graf)
            #self.barras()
            #self.start_process()
            
            #self.actualizar()
        elif op=="SPN":
            self.SPN()
            self.tabla2()
            print("spn")

        elif op=="SRT":
            self.SRTt()
            self.tabla3()
            print("srt")

        elif op=="RR":
            self.RR()
            self.tabla4()
            print("rr")
        
    def agregar_Par(self):
        valor = self.entrada_texto_R.text()
        if valor != '' and valor.isdigit():
            self.Particion.append( valor )

            self.Particion.sort(key=int)

            self.actualizar()
        print("particiones: ", self.Particion)
    def color_aleatorio(self):
        """Genera un color RGB aleatorio en formato string."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"rgb({r}, {g}, {b})"

    def grafico_RAM(self):
        if len(self.Particion) == 0:
            return
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)
        self.ini_x = self.dxi-45
        self.ini_y = self.dyi

        altura_y = int(self.dy_pos*(40/100))

        altura_y_PParticion = int(altura_y/Num_Particiones)
        print("fargsergsergsergserg", Num_Particiones)
        aumento = 0
        for valor in self.Particion:
            color_fondo = self.color_aleatorio()
            self.rectangulo = QWidget(self)
            self.rectangulo.setGeometry(self.ini_x, self.ini_y+aumento, 45, altura_y_PParticion)
            self.rectangulo.setStyleSheet(f"background-color:  {color_fondo}; border: 1px solid black;")

            etiqueta = QLabel(str(valor+' k'), self)
            etiqueta.setGeometry( self.ini_x+1, int(self.ini_y+aumento + ((altura_y_PParticion)*((40/100)))), 43, 25) # x-pos, y-pos, width, height
            etiqueta.setStyleSheet(self.estilo_text)
            aumento += altura_y_PParticion

        self.opcion_ram()

    def diagram_gant_ram(self):
        self.actualizar()
        print("dew")
        if self.Datos and self.Particion:
            print(self.Datos)
            self.Datos_T = {}
            if self.tipo_cola == "unica":
                if self.tipo_ram == "fisrt":
                    self.U_fisrt()
                elif self.tipo_ram == "best":
                    self.U_fisrt()
                else:
                    self.U_worst()
            else:
                if self.tipo_ram == "fisrt":
                    self.M_fisrt()
                elif self.tipo_ram == "best":
                    self.M_best()
                else:
                    self.U_worst()
            self.U_fisrt_Tabla()
        else:
            print("vacio")
            
    def U_fisrt_Tabla(self):
        self.textos2 = ['Name', 'T. DE RETORNO']
        ini_x = int(self.dx_pos * 0.55)
        ini_y = int(self.dy_pos * 0.55)
        width_x = int(self.dx_pos * 0.40)
        height_y = int(self.dy_pos * 0.008)
        separacion_x = int(self.dx_pos * 0.10)
        separacion_x_tex = int(self.dx_pos * 0.035)
        separacion_y = int(self.dy_pos * 0.035)
        fontsize = int(self.dy_pos * 0.019)
        estilo_text = f"color: rgba(91, 242, 226, 1); font-size: {fontsize}px; background-color: rgba(0,0,0,0)"
        
        # Dibujar líneas horizontales
        for i in range(2):
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + i * separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
        
        # Dibujar los encabezados de la tabla
        for i, texto in enumerate(self.textos2):
            etiqueta = QLabel(texto, self)
            etiqueta.setGeometry(ini_x + separacion_x * i + separacion_x_tex, ini_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta.setStyleSheet(estilo_text)
            etiqueta.show()

        ini_y += separacion_y
        ini_y_text = ini_y - int(self.dy_pos * 0.03)
        separacion_x_tex2 = int(self.dx_pos * 0.12)
        
        # Dibujar líneas horizontales para cada dato
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            linea = QFrame(self)
            linea.setGeometry(ini_x, ini_y + separacion_y, width_x, height_y)
            linea.setStyleSheet("background-color: rgb(94, 95, 94 );")
            linea.setFrameShape(QFrame.HLine)
            linea.show()
            ini_y += separacion_y

        promedio_tr = 0
        
        # Dibujar las letras de datos ingresados
        for i, clave in enumerate(self.Datos_T.keys()):
            etiqueta_clave = QLabel(clave, self)
            etiqueta_clave.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_clave.setStyleSheet(estilo_text)
            etiqueta_clave.show()
            
            etiqueta_valor1 = QLabel(str(self.Datos_T[clave]), self)
            etiqueta_valor1.setGeometry(ini_x + separacion_x_tex2, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
            etiqueta_valor1.setStyleSheet(estilo_text)
            etiqueta_valor1.show()
            
            ini_y_text += separacion_y
            promedio_tr += float(self.Datos_T[clave])
        
        dd = len(self.Datos_T) if self.Datos_T else 1
        promedio_tr /= dd

        etiqueta_promedio = QLabel("Promedio", self)
        etiqueta_promedio.setGeometry(ini_x + separacion_x_tex, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_promedio.setStyleSheet(estilo_text)
        etiqueta_promedio.show()
        
        etiqueta_tr = QLabel(str(promedio_tr), self)
        etiqueta_tr.setGeometry(ini_x + separacion_x_tex2, ini_y_text + separacion_y, int(self.dx_pos * 0.1), int(self.dy_pos * 0.03))
        etiqueta_tr.setStyleSheet(estilo_text)
        etiqueta_tr.show()

        
    def U_fisrt(self):
        
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)

        altura_y = int(self.dy_pos*(40/100))

        altura_y_PParticion = int(altura_y/Num_Particiones)
        
        aumento = 0
        i_hori = 0
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            memoria, ejecucion = valor
            for i, valor in enumerate(self.Particion):
                if int(valor) >= int(memoria):
                    color_fondo = self.color_aleatorio()
                    rectangulo = QWidget(self)
                    rectangulo.setGeometry(self.puntosX[i_hori], self.ini_y+aumento, self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion)
                    rectangulo.setStyleSheet(f"background-color:  {color_fondo}; border: 1px solid black;")
                    rectangulo.show()
                    
                    particion = int(valor) - int(memoria)

                    porcentaje_particion = int(((100*int(memoria))/int(valor)))

                    rectangulo1 = QWidget(self)
                    rectangulo1.setGeometry(self.puntosX[i_hori], self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100), self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion- (int((porcentaje_particion*(altura_y_PParticion))/100)))
                    rectangulo1.setStyleSheet(f"background-color:  red; border: 1px solid black;")
                    rectangulo1.show()

                    etiqueta = QLabel(str(str(memoria) + ' k'), self)
                    etiqueta.setGeometry( self.puntosX[i_hori] + int( 50*(self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori])/100), self.ini_y+aumento+int( 50*(altura_y_PParticion)/100), 45, 25) # x-pos, y-pos, width, height
                    etiqueta.setStyleSheet(self.estilo_text)
                    etiqueta.show()
                    
                    self.Datos_T[clave] = ejecucion+i_hori

                    print("diferenci:", self.ini_y+aumento, " ",self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100))
                    i_hori=ejecucion+i_hori
                    break
                aumento += altura_y_PParticion
            aumento = 0
        
        
    def U_best(self):
        print(self.Datos)
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)
        altura_y = int(self.dy_pos*(40/100))
        altura_y_PParticion = int(altura_y/Num_Particiones)
        aumento = 0
        i_hori = 0
    def U_worst(self):
        print(self.Datos)
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)

        altura_y = int(self.dy_pos*(40/100))

        altura_y_PParticion = int(altura_y/Num_Particiones)

        aumento = 0
        i_hori = 0
        for clave, valor in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor}")
            memoria, ejecucion = valor
            for i, valor1 in enumerate(self.Particion):
                if i == len(self.Particion)-1 and int(valor1)>=int(memoria):
                    color_fondo = self.color_aleatorio()
                    rectangulo = QWidget(self)
                    rectangulo.setGeometry(self.puntosX[i_hori], self.ini_y+aumento, self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion)
                    rectangulo.setStyleSheet(f"background-color:  {color_fondo}; border: 1px solid black;")
                    rectangulo.show()

                    porcentaje_particion = int(((100*int(memoria))/int(valor1)))

                    rectangulo1 = QWidget(self)
                    rectangulo1.setGeometry(self.puntosX[i_hori], self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100), self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion- (int((porcentaje_particion*(altura_y_PParticion))/100)))
                    rectangulo1.setStyleSheet(f"background-color:  red; border: 1px solid black;")
                    rectangulo1.show()

                    etiqueta = QLabel(str(str(memoria) + ' k'), self)
                    etiqueta.setGeometry( self.puntosX[i_hori] + int( 50*(self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori])/100), self.ini_y+aumento+int( 50*(altura_y_PParticion)/100), 45, 25) # x-pos, y-pos, width, height
                    etiqueta.setStyleSheet(self.estilo_text)
                    etiqueta.show()
                    self.Datos_T[clave] = ejecucion+i_hori
                    print("diferenci:", self.ini_y+aumento, " ",self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100))
                    i_hori=ejecucion+i_hori
                    break
                aumento += altura_y_PParticion
            aumento = 0
    def M_best(self):
        best = 9999999
        colas = []
        parti = 0
        colass = [[] for _ in range(len(self.Particion))]
        
        val=0
        for clave, valor1 in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor1}")
            memoria, ejecucion = valor1
            for i, valor in enumerate(self.Particion):
                if best > int(valor) - int(memoria) and int(valor) - int(memoria)>=0:
                    best = int(valor) - int(memoria)
                    parti = i
                    val=valor
            if int(val) >= int(memoria):
                colass[parti].append(clave)
            best = 9999999
        
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)
        altura_y = int(self.dy_pos*(40/100))
        altura_y_PParticion = int(altura_y/Num_Particiones)
        aumento = 0
        i_hori = 0
        for i, valor in enumerate(self.Particion):
            for valor2 in colass[i]:
                memoria, ejecucion =self.Datos[valor2]
                
                color_fondo = self.color_aleatorio()
                rectangulo = QWidget(self)
                rectangulo.setGeometry(self.puntosX[i_hori], self.ini_y+aumento, self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion)
                rectangulo.setStyleSheet(f"background-color:  {color_fondo}; border: 1px solid black;")
                rectangulo.show()

                porcentaje_particion = int(((100*int(memoria))/int(valor)))

                rectangulo1 = QWidget(self)
                rectangulo1.setGeometry(self.puntosX[i_hori], self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100), self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion- (int((porcentaje_particion*(altura_y_PParticion))/100)))
                rectangulo1.setStyleSheet(f"background-color:  red; border: 1px solid black;")
                rectangulo1.show()

                etiqueta = QLabel(str(str(memoria) + ' k'), self)
                etiqueta.setGeometry( self.puntosX[i_hori] + int( 50*(self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori])/100), self.ini_y+aumento+int( 50*(altura_y_PParticion)/100), 25, 15) # x-pos, y-pos, width, height
                etiqueta.setStyleSheet(self.estilo_text)
                etiqueta.show() 
                
                self.Datos_T[valor2] = ejecucion+i_hori
                
                i_hori=ejecucion+i_hori
            aumento += altura_y_PParticion
            i_hori = 0

    def M_fisrt(self):
        self.Datos_T = {}
        colass = [[] for _ in range(len(self.Particion))]
        
        for clave, valor1 in self.Datos.items():
            print(f"Clave: {clave}, Valor: {valor1}")
            memoria, ejecucion = valor1
            for i, valor in enumerate(self.Particion):
                if int(valor) >= int(memoria):
                    colass[i].append(clave)
                    break

        
        Num_Particiones = 1 if len(self.Particion) == 0 else len(self.Particion)
        altura_y = int(self.dy_pos*(40/100))
        altura_y_PParticion = int(altura_y/Num_Particiones)
        aumento = 0
        i_hori = 0
        for i, valor in enumerate(self.Particion):
            for valor2 in colass[i]:
                memoria, ejecucion =self.Datos[valor2]
                
                color_fondo = self.color_aleatorio()
                rectangulo = QWidget(self)
                rectangulo.setGeometry(self.puntosX[i_hori], self.ini_y+aumento, self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion)
                rectangulo.setStyleSheet(f"background-color:  {color_fondo}; border: 1px solid black;")
                rectangulo.show()

                porcentaje_particion = int(((100*int(memoria))/int(valor)))

                rectangulo1 = QWidget(self)
                rectangulo1.setGeometry(self.puntosX[i_hori], self.ini_y+aumento + int((porcentaje_particion*(altura_y_PParticion))/100), self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori], altura_y_PParticion- (int((porcentaje_particion*(altura_y_PParticion))/100)))
                rectangulo1.setStyleSheet(f"background-color:  red; border: 1px solid black;")
                rectangulo1.show()

                etiqueta = QLabel(str(str(memoria) + ' k'), self)
                etiqueta.setGeometry( self.puntosX[i_hori] + int( 50*(self.puntosX[ejecucion+i_hori]-self.puntosX[i_hori])/100), self.ini_y+aumento+int( 50*(altura_y_PParticion)/100), 25, 15) # x-pos, y-pos, width, height
                etiqueta.setStyleSheet(self.estilo_text)
                etiqueta.show() 
                self.Datos_T[valor2] = ejecucion+i_hori
                i_hori=ejecucion+i_hori
            aumento += altura_y_PParticion
            i_hori = 0

    def definir_ram(self, op):
        if op == "unica":
            self.tipo_cola = op
        else:
            self.tipo_cola = op
        self.opcion_ram()
        self.diagram_gant_ram()
        
    def definir_ram_model (self, op):
        if op == "fisrt":
            self.tipo_ram = op
        elif op == "best":
            self.tipo_ram = op
        else:
            self.tipo_ram = op
        self.opcion_ram()
        self.diagram_gant_ram()
        

    def opcion_ram(self):
        print("ndeedde")
        ini_x = int(self.dx_pos*(65/100))
        ini_y = int(self.dy_pos*(45/100))
        with_x = int(self.dy_pos*(40/100))
        self.texto = self.tipo_cola
        self.texto_second = self.tipo_ram

        etiqueta = QLabel(self.texto.capitalize(), self)
        etiqueta.setGeometry( ini_x, ini_y+5, 70, 20) # x-pos, y-pos, width, height
        etiqueta.setStyleSheet(self.estilo_text)
        etiqueta.show()

        etiqueta = QLabel(self.texto_second.capitalize(), self)
        etiqueta.setGeometry( ini_x+100, ini_y+5, 60, 20) # x-pos, y-pos, width, height
        etiqueta.setStyleSheet(self.estilo_text)
        etiqueta.show()


    def delete_Par(self):
        clave = self.entrada_texto_R.text()
        print(clave)
        if clave in self.Particion:
            self.Particion.remove(clave)
            self.actualizar()
        else:
            print("La clave no existe en el diccionario.")

    def aux(self):
        if len(self.Datos)==10:
            self.mostrar_advertencia(3)

        if self.Add():
            self.actualizar()
            print("prue")

    def Add(self):
        dat = []
        for entrada_texto in self.entradas_texto:
            valor = entrada_texto.text()
            if valor=='':
                self.mostrar_advertencia(1)
                return 0
            dat.append(valor)

        if dat[1].isdigit() and dat[2].isdigit():
            self.Datos[str(dat[0])]=(int(dat[1]), int(dat[2]))
        else:
            self.mostrar_advertencia(2)
            return 0
        if self.option_global == "CPU": 
            self.Datos = dict(sorted(self.Datos.items(), key=lambda x: x[1]))
        #DATOS[A]=(TLL, TE)
        # Obtener los valores como números enteros antes de ordenarlos
        #valores_numeros = [int(valor[0]) for valor in self.Datos.values()]


        # Ordenar los valores numéricos
        #valores_ordenados = sorted(valores_numeros)

        # Imprimir los valores ordenados
        #print(valores_ordenados)
        return 1
    
    def mostrar_advertencia(self, op):
        if op==1:
            QMessageBox.warning(None, 'Advertencia', '¡No puede existir datos vacios!\nPor favor, ingresar datos.')
        elif op==2:
            QMessageBox.warning(None, 'Advertencia', '¡Los tiempos deben ser numeros!\nPor favor, vuelve a ingresar los datos.')
        else:
            QMessageBox.warning(None, 'Advertencia', '¡Maximo de ingreso!\nPor favor, elimine algunos procesos.')
        
    def limpiar_all(self):
        for widget in self.findChildren(QWidget):
            if widget != self:  # No elimines la ventana principal
                widget.deleteLater()
        
        # Eliminar otros widgets de la ventana
        """
        for widget in self.findChildren(QWidget):
            if widget != self:  # No elimines la ventana principal
                widget.deleteLater()
        # Crear un bucle de eventos para esperar a que se eliminen los widgets
        
        self.loop = QEventLoop()
        QTimer.singleShot(0, self.loop.quit)
        self.loop.exec_()
        """
        
    def show_all(self):
        for widget in self.findChildren(QWidget):
            if widget != self:  # No elimines la ventana principal
                widget.show()

    def actualizar(self):
        self.limpiar_all()

        self.dibujar_prim()
        
        self.show_all()

    def delet(self):
        clave = self.entrada_textoE.text()
        print(clave)
        if clave in self.Datos:
            del self.Datos[clave]
            self.actualizar()
        else:
            print("La clave no existe en el diccionario.")
    
    def delet_all(self):
        self.Datos = {}
            
        
def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    #ventana.actualizarInterfaz()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
