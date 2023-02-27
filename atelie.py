import matplotlib.font_manager
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'Atelie'
		self.left = 200
		self.top = 200
		self.width = 320
		self.height = 100

		self.outxt = QFont('Times', 12)
		self.fonts = []
		fnts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
		for i in fnts:
			f = matplotlib.font_manager.FontProperties(fname=i).get_name()
			if f not in self.fonts:
				self.fonts.append(f)
		self.fonts.sort()

		self.bar = self.menuBar()
		self.bopt = (
			('Arquivo',('Novo','Ctrl+N'),('Abrir','Ctrl+O'),('Salvar','Ctrl+S'),('Salvar como','Ctrl+Shift+S'),('Sair',None)),
			('Editar',('Desfazer','Ctrl+Z'),('Refazer','Ctrl+Y'),('Recortar','Ctrl+X'),('Copiar','Ctrl+C'),('Colar','Ctrl+V')),
			('Exibir',('Mostrar barra de status','Ctrl+O')),
			('Ajuda',('Sobre','Ctrl+O'))
			)

		for i in self.bopt:
			mn = self.bar.addMenu(i[0])
			for j in i[1:]:
				opt = QAction(j[0],self)
				if j[1] != None: opt.setShortcut(j[1])
				mn.addAction(opt)
			mn.triggered[QAction].connect(self.file_manage)

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.draw()
		holder = QWidget()
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.horizontalGroupBox)
		holder.setLayout(windowLayout)
		self.setCentralWidget(holder)
		self.show()

	def file_manage(self, f):
		print(f.text())

	def font_edit(self, t):
		if t == 0: self.outxt.setBold(True)
		if t == 1: self.outxt.setItalic(True)
		if t == 2: self.outxt.setUnderline(True)
		if t == 3: self.outxt.setFamily(self.fonts[self.ffm.currentIndex()])
		if t == 4: self.outxt.setPixelSize(self.fsz.value())
		self.txt.setCurrentFont(self.outxt)

	def upgrade(self):
		otx = self.txt.toPlainText()
		self.stts.setText(str(0) + ', ' + str(len(otx)))

	def textedit(self):
		#self.horizontalGroupBox = QGroupBox("Grid")
		self.horizontalGroupBox = QWidget()
		self.gridlayout = QGridLayout()
		#self.gridlayout.setColumnStretch(1, 4)
		#self.gridlayout.setColumnStretch(2, 4)
		#FAMILIY & SIZE
		self.ffm = QComboBox()
		for i in self.fonts: self.ffm.addItem(i)
		self.gridlayout.addWidget(self.ffm,0,0)
		self.ffm.currentIndexChanged.connect(lambda: self.font_edit(3))
		self.fsz = QSpinBox()
		self.fsz.setRange(5,100)
		self.gridlayout.addWidget(self.fsz,0,1)
		self.fsz.valueChanged.connect(lambda: self.font_edit(4))
		#BUTTONS
		self.btn = [QPushButton('B'),QPushButton('I'),QPushButton('U')]
		for i in range(len(self.btn)):
			self.gridlayout.addWidget(self.btn[i],0,2+i)
			self.btn[i].clicked.connect(lambda args, j=i: self.font_edit(j))
		#TEXT EDITOR
		self.txt = QTextEdit()
		self.txt.setCurrentFont(self.outxt)
		self.gridlayout.addWidget(self.txt,2,0,1,5)
		self.txt.textChanged.connect(self.upgrade)
		#STATUS
		otx = self.txt.toPlainText()
		self.stts = QLabel(str(0) + ', ' + str(len(otx)))
		self.gridlayout.addWidget(self.stts,3,0,1,5)
		self.horizontalGroupBox.setLayout(self.gridlayout)

	def draw(self):
		self.horizontalGroupBox = QWidget()
		self.gridlayout = QGridLayout()
		#TEXT
		self.txt = QTextEdit()
		self.gridlayout.addWidget(self.txt,0,0)
		self.horizontalGroupBox.setLayout(self.gridlayout)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	ex = App()
	sys.exit(app.exec_())