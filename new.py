import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
import requests
from geocoder import get_ll_span


class MapApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Yandex Maps App')

        self.latitude_label = QLabel('Широта:')
        self.latitude_input = QLineEdit()

        self.longitude_label = QLabel('Долгота:')
        self.longitude_input = QLineEdit()

        self.show_map_button = QPushButton('Show Map')
        self.show_map_button.clicked.connect(self.show_map)

        self.map_image_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.latitude_label)
        layout.addWidget(self.latitude_input)
        layout.addWidget(self.longitude_label)
        layout.addWidget(self.longitude_input)
        layout.addWidget(self.show_map_button)
        layout.addWidget(self.map_image_label)

        self.setLayout(layout)

    def show_map(self):
        latitude = self.latitude_input.text()
        longitude = self.longitude_input.text()
        spn = get_ll_span(longitude + ',' + latitude)[1]
        api_url = f'https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&,400&z=14&l=map&spn={spn}'

        response = requests.get(api_url)

        if response.status_code == 200:
            map_image = QPixmap()
            map_image.loadFromData(response.content)
            self.map_image_label.setPixmap(map_image)
        else:
            print(f"Failed. Status code: {response.status_code}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_app = MapApp()
    map_app.show()
    sys.exit(app.exec_())
