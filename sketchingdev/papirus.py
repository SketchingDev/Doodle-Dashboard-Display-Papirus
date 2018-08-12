import os

from doodledashboard.configuration.config import ConfigSection
from doodledashboard.display import Display
from doodledashboard.notifications import TextNotification, ImageNotification

from sketchingdev.bmp_converter import convert_bmp
from sketchingdev.error import contains_all_in_error_message

try:
    from papirus import Papirus, PapirusText, PapirusImage
except ImportError as err:
    if contains_all_in_error_message(err, ["No module named", "papirus"]):
        raise ImportError(
            "I've not been able to find the PaPiRus software for Python 3+ on your Raspberry Pi...\n" +
            "If you haven't installed it then you should follow the instructions at " +
            "https://github.com/PiSupply/PaPiRus#auto-installation"
        )
    else:
        raise


class PapirusDisplay(Display):
    _WHITE = (255, 255, 255)
    _IMAGE_SUFFIX = "-papirus.bmp"

    def __init__(self):
        self._screen = Papirus()
        self._image = PapirusImage()
        self._text = PapirusText()

    def draw(self, notification):
        self._screen.update()
        if isinstance(notification, TextNotification):
            self._text.write(notification.get_text())
        elif isinstance(notification, ImageNotification):
            image_path = notification.get_image_path()
            converted_image_path = image_path + self._IMAGE_SUFFIX

            if not os.path.exists(converted_image_path):
                convert_bmp(image_path, converted_image_path)

            self._image.write(converted_image_path)

    @staticmethod
    def get_supported_notifications():
        return [TextNotification, ImageNotification]

    @staticmethod
    def get_id():
        return "papirus"

    def __str__(self):
        return "Papirus display"

    @staticmethod
    def get_config_factory():
        return PapirusConfig()


class PapirusConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "display", "papirus"

    def create(self, config_section):
        return PapirusDisplay()
