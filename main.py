import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter, QColor

SQUARE_WIDTH = 10
PAINT_WIDTH = 100


def color_to_byte(qcolor):
    color_red = qcolor.red()
    color_green = qcolor.green()
    color_blue = int((qcolor.blue() * 255) / 256)
    _byte = 0
    _byte += color_red & 0xE0
    _byte += (color_green >> 3) & 0x1C
    _byte += (color_blue >> 6) & 0x03
    return _byte


def byte_to_color(_byte):
    color_red = _byte & 0xE0
    if color_red >= 0xE0:
        color_red = 0xFF
    color_green = (_byte & 0x1C) << 3
    if color_green >= 0xE0:
        color_green = 0xFF
    color_blue = (_byte & 0x03) << 6
    if color_blue >= 0xC0:
        color_blue = 0xFF
    return QColor(color_red, color_green, color_blue)


class SolidColorRectangleWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.color = QColor(0, 0, 0)

    def initUI(self):
        self.text = "Current color"
        self.setGeometry(0, 0, 100, 40)
        self.resize(100, 40)
        self.setFixedWidth(100)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.fillRect(0, 0, 100, 40, self.color)
        qp.end()

    def setSelectedColor(self, color):
        self.color = color
        self.update()


class PaintWidget(QtWidgets.QWidget):

    def __init__(self, color_grid):
        super().__init__()
        self.initUI()
        self.curColor = QColor(0, 0, 0)
        self.color_grid = color_grid

    def initUI(self):
        self.text = "I am self.text"
        self.setGeometry(300, 800, 350, 800)
        self.show()

    def setSelectedColor(self, color):
        self.curColor = color

    def setColor(self, x, y):
        if (x % SQUARE_WIDTH + 2) > SQUARE_WIDTH or x < 0:
            return
        if (y % SQUARE_WIDTH + 2) > SQUARE_WIDTH or y < 0:
            return
        x_idx = int(x / (SQUARE_WIDTH + 2))
        y_idx = int(y / (SQUARE_WIDTH + 2))
        if y_idx >= len(self.color_grid):
            return
        if x_idx >= len(self.color_grid[0]):
            return
        self.color_grid[y_idx][x_idx] = self.curColor
        self.update()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        self.setColor(x, y)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.setColor(x, y)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.fillRect(0,0, 1400, 600, QColor(30,30,30))
        for y, col in enumerate(self.color_grid):
            for x, pixel in enumerate(col):
                x_start = (x * (SQUARE_WIDTH + 2))
                y_start = (y * (SQUARE_WIDTH + 2))
                qp.fillRect(x_start, y_start, SQUARE_WIDTH, SQUARE_WIDTH, pixel)
        qp.end()


class BackgroundButton(QtWidgets.QPushButton):

    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAutoFillBackground(True)
        self.setSelectedColor(QColor(0,0,0))

    def setSelectedColor(self, color):
        text_color = "black"
        r = 0.2126 * color.red()
        g = 0.7152 * color.green()
        b = 0.0722 * color.blue()
        luma = r + g + b
        if luma < 60:
            text_color = "white"
        self.setStyleSheet("background-color: {}; color: {}; height: 100px;".format(color.name(), text_color))
        self.update()
        

class App(QtWidgets.QWidget):

    fileSelected = QtCore.pyqtSignal()
    colorSelected = QtCore.pyqtSignal(QColor)

    def __init__(self, color_grid):
        super().__init__()
        self.color_grid = color_grid

    @QtCore.pyqtSlot()
    def on_click(self):
        self.openColorDialog()

    @QtCore.pyqtSlot()
    def on_color_selected(self):
        pass

    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.colorSelected.emit((color))

    def load_file(self):
        file_path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '~', "*.bin")
        if not file_path:
            return
        with open(file_path, 'rb') as inf:
            content = inf.read()
            size = (content[0] << 8) + content[1]
            print("loading {} pixels".format(size))
            num_rows = int((len(content) - 2) / 8)
            if num_rows != size:
                print("File has invalid format")
                return

            cur_load_idx = 2
            for row_idx in range(num_rows):
                for col_idx in range(8):
                    color = byte_to_color(content[cur_load_idx])
                    self.color_grid[col_idx][row_idx] = color
                    cur_load_idx += 1
            self.fileSelected.emit()

    def save_file(self):
        file_path, filter = QtWidgets.QFileDialog.getSaveFileName()
        if not file_path:
            return
        with open(file_path, 'wb') as ouf:
            ouf.write(bytes([0]))
            ouf.write(bytes([PAINT_WIDTH]))
            print("writing 100 pixels")
            for row_idx in range(PAINT_WIDTH):
                for col_idx in range(8):
                    _byte = color_to_byte(self.color_grid[col_idx][row_idx])
                    _bytes = bytes([_byte])
                    ouf.write(_bytes)


def fill_grid_with_rainbow(color_grid):
    colors = [
        QColor() for i in range(26)
    ]

    for i, color in enumerate(colors):
        color.setHsv(i * 15, 255, 255)

    cnt = 0
    for j in range(8):
        for i in range(100):
            color_grid[j][i] = colors[cnt]
            cnt += 1
            cnt %= len(colors)


def main():

    color_grid = [
        [
            QColor(0, 0, 0) for _ in range(PAINT_WIDTH)
        ] for _ in range(8)
    ]
    fill_grid_with_rainbow(color_grid)

    app = QtWidgets.QApplication(sys.argv)
    window = App(color_grid)
    window.setFixedSize(1400, 500)

    welcome = QtWidgets.QLabel("Welcome to MiniPOV Designer")

    vbox = QtWidgets.QVBoxLayout()

    vbox.addWidget(welcome)

    load_save_hbox = QtWidgets.QHBoxLayout()
    load_button = QtWidgets.QPushButton('Load .bin file')
    load_button.clicked.connect(window.load_file)
    load_button.setStyleSheet("height: 100px;")
    save_button = QtWidgets.QPushButton('Save .bin file')
    save_button.clicked.connect(window.save_file)
    save_button.setStyleSheet("height: 100px;")
    load_save_hbox.addWidget(load_button)
    load_save_hbox.addWidget(save_button)
    load_save_hbox_w = QtWidgets.QWidget()
    load_save_hbox_w.setLayout(load_save_hbox)
    vbox.addWidget(load_save_hbox_w)

    button = BackgroundButton('Pick color')
    button.setToolTip('Opens color dialog')
    button.clicked.connect(window.on_click)
    window.colorSelected.connect(button.setSelectedColor)

    color_widget = SolidColorRectangleWidget()
    window.colorSelected.connect(color_widget.setSelectedColor)

    hbox = QtWidgets.QHBoxLayout()
    hbox.addWidget(button)
    hbox_w = QtWidgets.QWidget()
    hbox_w.setLayout(hbox)
    vbox.addWidget(hbox_w)

    painter = PaintWidget(color_grid)
    window.colorSelected.connect(painter.setSelectedColor)
    window.fileSelected.connect(painter.update)
    vbox.addWidget(painter)

    window.setLayout(vbox)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()