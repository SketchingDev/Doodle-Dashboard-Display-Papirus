from sketchingdev.error import contains_all_in_error_message

try:
    from PIL import Image
except ImportError as err:
    if contains_all_in_error_message(err, ["libopenjp2.so.7", "no such file or directory"]):
        raise ImportError(
            "Your RaspberryPi is missing the dependency 'libopenjp2-7', which is used by the library 'Pillow' to " +
            "draw images to your PaPiRus display. Don't worry though! It should be easy enough to install by running " +
            "'sudo apt-get install libopenjp2-7'"
        )
    else:
        raise

_white = (255, 255, 255)


def convert_bmp(image_path, output_path):
    image = Image \
        .open(image_path) \
        .convert("RGBA")
    bg = Image.new("RGB", image.size, _white)
    bg.paste(image, (0, 0), image)

    bg.save(output_path, "BMP")
