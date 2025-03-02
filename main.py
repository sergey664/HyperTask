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

        self.coordinates = "Москва, Красная Площадь 1"
        self.image_path = "map.png"

        self.api_worker.find_static_map_info(self.coordinates)
        self.set_image()

    def keyPressEvent(self, event):
        zoom = self.api_worker.get_zoom()

        key = event.key()
        if key == Qt.Key.Key_PageUp or key == Qt.Key.Key_W and all([0.001 < value / 2 < 1 for value in zoom]):
            self.api_worker.set_zoom([value / 2 for value in zoom])
        elif key == Qt.Key.Key_Down or key == Qt.Key.Key_S and all([0.001 < value * 2 < 1 for value in zoom]):
            self.api_worker.set_zoom([value * 2 for value in zoom])

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
