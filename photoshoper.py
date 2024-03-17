import os

from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, 
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter

app =  QApplication([])
window = QWidget()
window.resize(1000, 500)
window.setWindowTitle('Easy Editor')

button_folder = QPushButton('Папка')
list_images = QListWidget()
text_image = QLabel('Картинка')
button_left = QPushButton('Лево')
button_right = QPushButton('Право')
button_mirror = QPushButton('Зеркало')
button_sharp = QPushButton('Резкость')
button_bw = QPushButton('ч/б')
button_edges = QPushButton('Затемнить')
button_emboss = QPushButton('Высветлить')

colum1 = QVBoxLayout()
colum2 = QVBoxLayout()
row = QHBoxLayout()
main_row = QHBoxLayout()

colum1.addWidget(button_folder)
colum1.addWidget(list_images)

row.addWidget(button_left)
row.addWidget(button_right)
row.addWidget(button_mirror)
row.addWidget(button_sharp)
row.addWidget(button_bw)
row.addWidget(button_edges)
row.addWidget(button_emboss)

colum2.addWidget(text_image)
colum2.addLayout(row)

main_row.addLayout(colum1, 20)
main_row.addLayout(colum2, 80)

window.setLayout(main_row)

workdir = ''

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files):
    result = []
    extenctions = ['.jpg', '.png', '.jpeg']

    for filename in files:
        for ext in extenctions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkDir()
    files = filter(os.listdir(workdir))
    list_images.clear()
    for filename in files:
        list_images.addItem(filename)

button_folder.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'changed'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        text_image.hide()
        pixmapimage = QPixmap(path)
        width, height = text_image.width(), text_image.height()
        pixmapimage = pixmapimage.scaled(width, height, Qt.KeepAspectRatio)
        text_image.setPixmap(pixmapimage)
        text_image.show()

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def make_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_edges(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

    def make_emdoss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.saveImage()
        changed_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(changed_path)

workimage = ImageProcessor()

def showChosenImage():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

list_images.currentRowChanged.connect(showChosenImage)

button_bw.clicked.connect(workimage.make_bw)
button_right.clicked.connect(workimage.make_right)
button_left.clicked.connect(workimage.make_left)
button_mirror.clicked.connect(workimage.make_mirror)
button_sharp.clicked.connect(workimage.make_sharpen)
button_edges.clicked.connect(workimage.make_edges)
button_emboss.clicked.connect(workimage.make_emdoss)

window.show()
app.exec()