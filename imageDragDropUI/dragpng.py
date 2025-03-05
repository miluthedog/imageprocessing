'''
input: .png, make it moveable

output: its coordinates
'''
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QCursor
from PyQt6.QtCore import Qt, QPoint, QRect

class DraggableImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap("imageDragDropUI/images/test2.png") # setup image

        self.image_pos = QPoint(50, 50)                         # (ini) store potision
        self.offset = QPoint()                                  # (ini) store offset

        self.dragging = False                                   # state: not drag
        
        self.setMouseTracking(True)                             # enable mouse tracking

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:                                                 # event: left click
            img_x, img_y = event.pos().x() - self.image_pos.x(), event.pos().y() - self.image_pos.y()   # relative motion of image = relative motion of click
            if (0 <= img_x < self.image.width() and 0 <= img_y < self.image.height()):                  # check if click valid
                pixel = self.image.toImage().pixelColor(img_x, img_y)
                if pixel.alpha() > 0:
                    self.dragging = True                                        # state: drag
                    self.offset = event.pos() - self.image_pos                  # store offset
                    self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))    # (change cursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:                               # check state
            self.image_pos = event.pos() - self.offset  # store position
            self.update()                               
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:         # event: stop left click
            self.dragging = False                               # state: not drag
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor)) # (change cursor)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
            # coordinates
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawLine(-50, 50, self.width(), 50)
        painter.drawLine(50, -50, 50, self.height())
            # redraw (moved) image
        painter.drawPixmap(self.image_pos, self.image)
            # display position
        painter.setPen(QColor(0, 255, 255))
        self.scaled_x, self.scaled_y = ((self.image_pos.x() - 50) / 5) , ((self.image_pos.y() - 50) / 5)    # rescale for cnc
        text = f"Position: ({self.scaled_x}, {self.scaled_y})"
        text_rect = QRect(20, 20, self.width() - 40, self.height() - 40)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("testing")
        self.setGeometry(100, 100, 800, 600)
        self.widget = DraggableImageWidget()
        self.setCentralWidget(self.widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())