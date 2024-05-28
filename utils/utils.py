from PIL import Image, ImageDraw, ImageFont
import numpy as np


class PhotoConverter:
    def __init__(
        self,
        text_size=60,
        place=(0.2, 0.3),
        font_path="./utils/font.ttf",
        color: tuple = (0, 0, 0),
    ):
        self.text_size = text_size
        self.place = place
        self.font = ImageFont.truetype(font_path, self.text_size)
        self.text = "Привет"
        self.color = color

    def __call__(self, image_path):
        img = Image.open(image_path)
        graphics = ImageDraw.Draw(img)
        size = np.array(img).shape
        point = (int(size[1] * self.place[0]), int(size[0] * self.place[1]))
        graphics.text(point, self.text, font=self.font, fill=self.color)
        img.save(image_path + ".png")
