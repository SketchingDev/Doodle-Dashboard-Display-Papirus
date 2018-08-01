import os
import unittest
from PIL import Image
from os import path

from sketchingdev.bmp_converter import _convert_bmp


class TestBmpConversion(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        data_dir = path.join(TestBmpConversion._get_current_directory(), "data/")
        cls.expected_image = path.join(data_dir, "expected_image.bmp")
        cls.test_images = [
            {
                "path": path.join(data_dir, "png_with_transparency.png"),
                "percentage_diff_from_expected": 0
            },
            {
                "path": path.join(data_dir, "png_without_transparency.png"),
                "percentage_diff_from_expected": 0
            },
            {
                "path": path.join(data_dir, "gif_with_transparency.gif"),
                "percentage_diff_from_expected": 0.71
            },
            {
                "path": path.join(data_dir, "gif_without_transparency.gif"),
                "percentage_diff_from_expected": 0
            },
            {
                "path": path.join(data_dir, "jpg_without_transparency.jpg"),
                "percentage_diff_from_expected": 0.39
            },
            {
                "path": path.join(data_dir, "png_with_semi_transparent_bg.png"),
                "percentage_diff_from_expected": 0
            },
        ]

    def test_conversion_of_images_to_bmp(self):
        for image_test in self.test_images:
            path = image_test["path"]
            acceptable_percentage_diff = image_test["percentage_diff_from_expected"]

            converted_image_path = _convert_bmp(path)

            percentage_diff = self._image_difference(converted_image_path, self.expected_image)

            msg = "Difference between image '%s' and the expected image should be below %s percent but was %s" % \
                  (converted_image_path, acceptable_percentage_diff, percentage_diff)
            self.assertLessEqual(acceptable_percentage_diff, percentage_diff, msg)

    @staticmethod
    def _get_current_directory():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def _image_difference(image_1_path, image_2_path):
        """
        Calculates the percentage difference between two images.
        Original source: https://rosettacode.org/wiki/Percentage_difference_between_images#Python

        :return: Percentage difference between two images
        """

        image_1 = Image.open(image_1_path)
        image_2 = Image.open(image_2_path)

        if image_1.mode != image_2.mode:
            # Different kinds of images.
            return 100

        if image_1.size != image_2.size:
            # Different sizes
            return 100

        pairs = zip(image_1.getdata(), image_2.getdata())
        if len(image_1.getbands()) == 1:
            # for gray-scale JPEGS
            dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        else:
            dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        n_components = image_1.size[0] * image_1.size[1] * 3
        return (dif / 255.0 * 100) / n_components


if __name__ == "__main__":
    unittest.main()
