from PIL import Image

_white = (255, 255, 255)


def _convert_bmp(image_path):
    image = Image.open(image_path)
    if image.format == "BMP":
        return image_path
    else:
        image = image.convert("RGBA")
        bg = Image.new("RGB", image.size, _white)
        bg.paste(image, (0, 0), image)

        new_image_path = image_path + "-papirus.bmp"
        bg.save(new_image_path, "BMP")

        return new_image_path
