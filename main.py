import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from weather_ui import Ui_Form
from config import API_KEY

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btnSearch.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.ui.lineEditCity.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                raise Exception(data.get("message"))
            temp = data['main']['temp']
            condition = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind = data['wind']['speed']

            self.ui.labelTemp.setText(f"Temperature: {temp} °C")
            self.ui.labelCondition.setText(f"Condition: {condition}")
            self.ui.labelHumidity.setText(f"Humidity: {humidity}%")
            self.ui.labelWind.setText(f"Wind: {wind} m/s")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get weather: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())

