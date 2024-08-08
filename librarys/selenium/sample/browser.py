from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth


class Browser:
    def __init__(self):
        self.browser = object
        self.__driver_service = Service()
        self.__driver_options = Options()

        self.__driver_experimantal_options: dict[str, Any] = {
            "excludeSwitches": ["enable-logging"],
            "prefs": {
                "profile.default_content_setting_values": {
                    "cookies": 1,
                    "images": 2,
                    "plugins": 1,
                    "popups": 2,
                    "geolocation": 1,
                    "notifications": 1,
                    "auto_select_certificate": 1,
                    "fullscreen": 2,
                    "mouselock": 1,
                    "mixed_script": 1,
                    "media_stream": 1,
                    "media_stream_mic": 1,
                    "media_stream_camera": 1,
                    "protocol_handlers": 1,
                    "ppapi_broker": 1,
                    "automatic_downloads": 1,
                    "midi_sysex": 1,
                    "push_messaging": 1,
                    "ssl_cert_decisions": 1,
                    "metro_switch_to_desktop": 1,
                    "protected_media_identifier": 1,
                    "app_banner": 2,
                    "site_engagement": 1,
                    "durable_storage": 1,
                }
            },
            "detach": True,
        }
        self.__driver_arguments: list[str] = [
            "disable-infobars",
            "--disable-extensions",
            "--headless",
            "--no-sandbox",
            "--single-process",
            "--disable-dev-shm-usage",
            "window-size=1200x600",
        ]
        self.__stealth_options: list[str, Any] = {
            "languages": ["en-US", "en"],
            "vendor": "Google Inc.",
            "platform": "Win32",
            "webgl_vendor": "Intel Inc.",
            "renderer": "Intel Iris OpenGL Engine",
            "fix_hairline": True,
        }

        self.__initialize_browser()

    def __initialize_browser(self):
        """Selenium Browser를 초기화합니다."""
        self.__add_experimantal_options()
        self.__add_driver_arguments()
        self.__browser_setup()
        self.__browser_stealth()

    def __add_experimantal_options(self):
        for option_key, option_value in self.__driver_experimantal_options.items():
            self.__driver_options.add_experimental_option(option_key, option_value)

    def __add_driver_arguments(self):
        for argument in self.__driver_arguments:
            self.__driver_options.add_argument(argument=argument)

    def __browser_setup(self):
        self.browser = webdriver.Chrome(
            service=self.__driver_service,
            options=self.__driver_options,
        )

    def __browser_stealth(self):
        stealth(self.browser, *self.__stealth_options)


session = Browser()
