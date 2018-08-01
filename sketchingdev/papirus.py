from doodledashboard.configuration.config import ConfigSection
from doodledashboard.display import Display
from doodledashboard.notifications import TextNotification, ImageNotification

from papirus import Papirus, PapirusText, PapirusImage


# https://github.com/SketchingDev/Doodle-Dashboard/commit/ef8572abe01165d44e7d6c4c7c49d9b1b838d8d9
from sketchingdev.bmp_converter import _convert_bmp


class PapirusDisplay(Display):
    _WHITE = (255, 255, 255)

    def __init__(self):
        self._screen = Papirus()
        self._image = PapirusImage()
        self._text = PapirusText()

    def draw(self, notification):
        self._screen.update()
        if isinstance(notification, TextNotification):
            self._text.write(notification.get_text())
        elif isinstance(notification, ImageNotification):
            image_path = _convert_bmp(notification.get_image_path())
            self._image.write(image_path)

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
