import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        #create v-box layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)
        self.setLayout(vbox)

        #alignments:
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")
        
        self.setStyleSheet("""
            QWidget {
                background-color: #B3E5FC;  /* Soft sky blue background */
                border-radius: 5px;         /* Rounded corners */
                padding: 10px;
            }

            QLabel {
                color: #333333;              /* Dark text for labels */
                font-size: 20px;             /* Medium font size */
                font-family: 'Segoe UI emoji', sans-serif;
                margin: 10px 0;
            }

            QLabel#city_label {
                font-weight: bold;
                font-size: 22px;
                color: #004D40;  /* Dark teal for the city label */
            }

            QLineEdit {
                background-color: #FFFFFF;   /* Clean white input field */
                border: 2px solid #004D40;   /* Dark teal border */
                border-radius: 12px;
                padding: 12px;
                font-size: 18px;
                margin: 12px 0;
            }

            QLineEdit:focus {
                border-color: #0288D1;       /* Blue border on focus */
            }

            QPushButton {
                background-color: #FFEB3B;   /* Bright yellow for buttons */
                color: #000000;              /* Black text for visibility */
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 30px;
                padding: 15px 30px;
                margin: 15px 0;
            }

            QPushButton:hover {
                background-color: #FFCA28;   /* Slightly darker yellow on hover */
            }

            QPushButton:pressed {
                background-color: #FF9800;   /* Darker orange when pressed */
            }

            QLabel#temp_label {
                font-size: 40px;              /* Larger font for temperature */
                font-weight: bold;
                color: #FF5722;               /* Warm orange for temperature */
                margin-top: 20px;
            }

            QLabel#emoji_label {
                font-size: 70px;
                margin-top: 15px;
                font-family: Segoe UI emoji;
            }

            QLabel#desc_label {
                font-size: 40px;
                font-weight: light;
                color: #757575;               /* Light gray for description */
            }

            /* Spacing and alignment tweaks */
            QVBoxLayout {
                spacing: 25px;                /* Space between elements */
            }

            QLineEdit {
                min-width: 280px;             /* Make input field wide enough */
            }

            /* Keyframe animation for emoji pulsing */
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            """)
        
        self.get_weather_button.clicked.connect(self.get_weather)


    
    def get_weather(self):
        api_key = "7903621eb350835c25121f8fd380f260"
        city = self.city_input.text()
        weather_timely = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={api_key}"
        weather = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        url = weather
        
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match resp.status_code:
                case 400:
                    self.display_error("400 - Bad Request\nPlease check your input and try again.")

                case 401:
                    self.display_error("401 - Unauthorized\nEnsure you are logged in and have the correct permissions.")

                case 403:
                    self.display_error("403 - Forbidden\nYou may not have the necessary permissions.")

                case 404:
                    self.display_error("404 - Not Found\nPlease check your URL and ensure the resource exists.")

                case 500:
                    self.display_error("500 - Internal Server Error\nPlease try again later.")

                case 502:
                    self.display_error("502 - Bad Gateway\nTry again or contact support.")

                case 503:
                    self.display_error("503 - Service Unavailable\nPlease try again later.")

                case 504:
                    self.display_error("504 - Gateway Timeout\nPlease try again.")

                case 505:
                    self.display_error("505 - HTTP Version Not Supported\nPlease check your client settings.")

                case 408:
                    self.display_error("408 - Request Timeout\nPlease check your network connection and try again.")

                case 429:
                    self.display_error("429 - Too Many Requests\nPlease slow down and try again later.")

                case 401:
                    self.display_error("401 - Unauthorized\nPlease log in with the correct credentials.")

                case 413:
                    self.display_error("413 - Payload Too Large\nPlease reduce the size of your request and try again.")
                    
                case _:
                    self.display_error("HTTP error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Unable to connect to the server. Please check your internet connection or the server status.")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: The request timed out. The server took too long to respond. Please try again later.")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects: The request exceeded the maximum number of redirects. Please check the URL or contact the server administrator.")

        except requests.exceptions.RequestException as e:
            self.display_error(f"Request Exception: A generic error occurred with the request. Details: {e}")
    
    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 15px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.desc_label.clear()

    def display_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 40px;")
        temp_C = f"{(data["main"]["temp"] - 273.15):.0f}°C"
        w_desc = data["weather"][0]["description"]
        self.desc_label.setText(w_desc)
        weather_id = data["weather"][0]["id"]

        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.temp_label.setText(temp_C)
    
    def display_weather_timely(self, data):
        print(data)
        
    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:
            # Group 2xx: Thunderstorm
            case 200 | 201 | 202 | 210 | 211 | 212 | 221 | 230 | 231 | 232:
                return "🌩️"  # Thunderstorm
            # Group 3xx: Drizzle
            case 300 | 301 | 302 | 310 | 311 | 312 | 313 | 314 | 321:
                return "🌧️"  # Drizzle
            # Group 5xx: Rain
            case 500 | 501 | 502 | 503 | 504 | 511 | 520 | 521 | 522 | 531:
                return "🌧️"  # Rain
            # Group 6xx: Snow
            case 600 | 601 | 602 | 611 | 612 | 613 | 615 | 616 | 620 | 621 | 622:
                return "❄️"  # Snow
            # Group 7xx: Atmosphere
            case 701 | 711 | 721 | 731 | 741 | 751 | 761 | 762 | 771 | 781:
                return "🌫️"  # Atmosphere (Mist, Smoke, Haze, etc.)
            # Group 800: Clear
            case 800:
                return "☀️"  # Clear sky (Daytime)
            case 801 | 802 | 803 | 804:
                return "☁️"  # Clouds
            # Default case for unknown weather ID
            case _:
                return "❓"  # Unknown or invalid weather ID

        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w_app = WeatherApp()
    w_app.show()
    sys.exit(app.exec_())