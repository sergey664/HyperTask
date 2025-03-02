from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap
import sys

from ApiWorker import ApiWorker


class MapApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("map_finder.ui", self)

        self.api_worker = ApiWorker()
        self.mapLabel.setPixmap(QPixmap(300, 300))

        self.find_location()

    def find_location(self):
        coords = "Москва, Красная Площадь 1"
        self.api_worker.load_static_map_info(coords)
        image_path = "map.png"
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.mapLabel.setPixmap(pixmap)
            self.mapLabel.setScaledContents(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())
