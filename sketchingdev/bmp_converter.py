from PIL import Image

_white = (255, 255, 255)


def convert_bmp(image_path, output_path):
    image = Image \
        .open(image_path) \
        .convert("RGBA")
    bg = Image.new("RGB", image.size, _white)
    bg.paste(image, (0, 0), image)

    bg.save(output_path, "BMP")
