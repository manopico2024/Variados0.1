import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class ImageResizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Nenhuma imagem carregada', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.btnLoad = QPushButton('Carregar Imagem', self)
        self.btnLoad.clicked.connect(self.loadImage)

        self.btnResize = QPushButton('Redimensionar Imagem', self)
        self.btnResize.clicked.connect(self.resizeImage)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnResize)
        self.setLayout(layout)

        self.setWindowTitle('Redimensionador de Imagens')
        self.setGeometry(400, 400, 400, 300)

    def loadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Carregar Imagem', '', 'Imagens (*.png *.jpg *.bmp)', options=options)
        if fileName:
            self.pixmap = QPixmap(fileName)
            self.label.setPixmap(self.pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))
            self.imagePath = fileName

    def resizeImage(self):
        if hasattr(self, 'pixmap'):
            width, ok1 = QInputDialog.getInt(self, 'Redimensionar Imagem', 'Insira a nova largura:')
            height, ok2 = QInputDialog.getInt(self, 'Redimensionar Imagem', 'Insira a nova altura:')
            if ok1 and ok2:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getSaveFileName(self, 'Salvar Imagem', '', 'Imagens (*.png *.jpg *.bmp)', options=options)
                if fileName:
                    image = Image.open(self.imagePath)
                    resized_image = image.resize((width, height))
                    resized_image.save(fileName)
                    self.label.setText('Imagem redimensionada e salva!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageResizer()
    ex.show()
    sys.exit(app.exec_())
