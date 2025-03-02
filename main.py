from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys

from ApiWorker import ApiWorker


class MapApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("map_finder.ui", self)

        self.api_worker = ApiWorker()
        self.mapLabel.setPixmap(QPixmap(300, 300))

        self.shift = [0, 0]

        self.coordinates = "Москва, Красная Площадь 1"
        self.image_path = "map.png"

        self.api_worker.find_static_map_info(self.coordinates)
        self.set_image()

    def keyPressEvent(self, event):
        zoom = self.api_worker.get_zoom()
        coordinates = self.api_worker.get_coordinates()

        key = event.key()
        if key == Qt.Key.Key_PageUp or key == Qt.Key.Key_Q and all([0.001 < value / 2 for value in zoom]):
            self.api_worker.set_zoom([value / 2 for value in zoom])
        elif key == Qt.Key.Key_Down or key == Qt.Key.Key_E and all([value * 2 < 21 for value in zoom]):
            self.api_worker.set_zoom([value * 2 for value in zoom])
        elif key == Qt.Key.Key_Up or key == Qt.Key.Key_W and abs(self.shift[1] + zoom[1]) < abs(5 * zoom[1]):
            self.shift[1] += zoom[1]
            self.api_worker.set_coordinates([coordinates[0], coordinates[1] + zoom[1]])
        elif key == Qt.Key.Key_Down or key == Qt.Key.Key_S and abs(self.shift[1] + zoom[1]) < abs(5 * zoom[1]):
            self.shift[1] -= zoom[1]
            self.api_worker.set_coordinates([coordinates[0], coordinates[1] - zoom[1]])
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_D and abs(self.shift[0] + zoom[0]) < abs(5 * zoom[0]):
            self.shift[0] += zoom[0]
            self.api_worker.set_coordinates([coordinates[0] + zoom[0], coordinates[1]])
        elif key == Qt.Key.Key_Left or key == Qt.Key.Key_A and abs(self.shift[0] + zoom[0]) < abs(5 * zoom[0]):
            self.shift[0] -= zoom[0]
            self.api_worker.set_coordinates([coordinates[0] - zoom[0], coordinates[1]])

        self.set_image()

    def set_image(self):
        self.api_worker.load_static_map_info()
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.mapLabel.setPixmap(pixmap)
            self.mapLabel.setScaledContents(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())
