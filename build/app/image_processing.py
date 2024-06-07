import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def open_image(file_name: str) -> Image:
    try:
        image_box = Image.open(file_name)
        return image_box
    except:
        return None


def mark_plot(
        im: Image, r: float, b: float, g: float, line_percentage: int = 10, horisontal=False
) -> None:
    image_array = np.array(im) / 255
    horisontal_size, vertical_size = image_array.shape[0:2]
    line_size = (vertical_size + horisontal_size) / 2
    line_size = int(line_size / 100 * line_percentage)
    if horisontal:
        center = (vertical_size // 2, horisontal_size // 10)
    else:
        center = (vertical_size // 10, horisontal_size // 2)
    try:
        for i, color in enumerate((r, g, b)):
            if horisontal:
                image_array[-center[1] - line_size // 2 : -center[1], :, i] = color
                image_array[-center[1] : -center[1] + line_size // 2, :, i] = color

                image_array[:, center[0] - line_size // 2 : center[0], i] = color
                image_array[:, center[0] : int(center[0] + line_size // 2), i] = color
            else:
                image_array[-center[1] - line_size // 2 : -center[1], :, i] = color
                image_array[-center[1] : -center[1] + line_size // 2, :, i] = color

                image_array[:, center[0] - line_size // 2 : center[0], i] = color
                image_array[:, center[0] : center[0] + line_size // 2, i] = color
        image = Image.fromarray((255.0 * image_array).astype(np.uint8))
        print(image)
    except Exception as e:
        print(e)
        return None
    return image


def image_color_distribution(image: str) -> plt.figure:
    image = Image.open(image)
    image = np.array(image)
    fig = plt.figure()
    red = fig.add_subplot(1, 3, 1)
    blue = fig.add_subplot(1, 3, 2)
    green = fig.add_subplot(1, 3, 3)
    red.set_axis_off()
    blue.set_axis_off()
    green.set_axis_off()
    red.imshow(image[:, :, 0], cmap="Reds")
    blue.imshow(image[:, :, 2], cmap="Blues")
    green.imshow(image[:, :, 1], cmap="Greens")
    fig.tight_layout()
    return fig
