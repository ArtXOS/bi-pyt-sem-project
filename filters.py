import numpy as np
from PIL import Image


def rotate_r(img: Image, *args) -> Image:
    """
    90 degree right rotate
    :param img: PIL Image to rotate
    :return: rotated PIL Image
    """
    print('Rotation...')
    img = np.array(img, dtype=np.uint8)
    img = np.swapaxes(img, 0, 1)[:, ::-1, ...]
    return Image.fromarray(img)


def mirror(img: Image, *args) -> Image:
    """
    Mirrors the image (y axis)
    :param img: PIL Image
    :return: mirrored image
    """
    print('Mirroring...')
    img = np.array(img, dtype=np.uint8)
    img = np.fliplr(img)
    return Image.fromarray(img)


def inverse(img: Image, *args) -> Image:
    """
    Inverts image colors
    :param img: PIL Image
    :return: image with inverted colors
    """
    print('Inverting...')
    img = np.array(img, dtype=np.uint8)
    img = 255 - img
    return Image.fromarray(img)


def grayscale(img: Image, *args) -> Image:
    """
    Converts the image to gray scale
    :param img: PIL Image
    :return: gray scaled image
    """
    print('Gray scaling...')
    if img.mode == "RGBA":
        img = np.array(img, dtype=np.uint8)
        img = np.sum(img * (0.299, 0.587, 0.114, 1), axis=2)
    else:
        img = np.array(img, dtype=np.uint8)
        img = np.sum(img * (0.299, 0.587, 0.114), axis=2)
    img = img.astype(dtype=np.uint8)
    return Image.fromarray(img)


def brightness_change(img: Image, mode: str, percent: int) -> Image:
    """
    Changes the brightness of an image: lighten or darken
    :param img: PIL Image
    :param mode: specifies lighten(-l | --lighten) or darken(-d | --darken) mode
    :param percent: 0 - 100 value. 0 - no effect, 100 - image is completely black or white
    :return: edited image
    """
    print('Changing brightness...')
    value = 0
    if mode == '-l' or mode == '--lighten':
        value = 255 * int(percent) / 100
    elif mode == '-d' or mode == '--darken':
        value = -255 * int(percent) / 100
    img = np.array(img, dtype=np.uint8)
    img.setflags(write=True)
    img = img.T
    if value > 0:
        img = np.where((255 - img) < value, 255, img + value)
    else:
        img = np.where((img + value) < 0, 0, img + value)
    img = img.T
    img = img.astype(dtype=np.uint8)
    return Image.fromarray(img)


def apply_filter_channel(image: np.array, kernel: np.array) -> np.array:
    """
    Applies transformation kernel (convolution) to the one color channel.
    :param image: numpy array - array with the values of each pixel
    :param kernel: transformation matrix
    :return: numpy array - edited channel
    """
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image)
    offset = kernel.shape[0] // 2
    image_padded = np.zeros((image.shape[0] + 2 * offset, image.shape[1] + 2 * offset))
    image_padded[offset:-offset, offset:-offset] = image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            result = int((kernel * image_padded[y:y + kernel.shape[0], x:x + kernel.shape[0]]).sum()
            if result < 0:
                result = 0
            elif result > 255:
                result = 255
            output[y][x] = result
    return output


def sharpen(img: Image, *args) -> Image:
    """
    Sharps an image. Function uses convolution method
    :param img: PIL Image
    :return: edited image
    """
    print('Sharpening...')
    img = np.array(img, dtype=np.uint8)
    img.setflags(write=True)
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ])

    if img.ndim == 2:
        img = apply_filter_channel(img, kernel)
    else:
        r_channel = np.zeros((img.shape[0], img.shape[1]))
        g_channel = np.zeros((img.shape[0], img.shape[1]))
        b_channel = np.zeros((img.shape[0], img.shape[1]))

        for i in range(img.shape[0]):
            for j in range(img.shape[0]):
                r_channel[i][j] = img[i][j][0]
                g_channel[i][j] = img[i][j][1]
                b_channel[i][j] = img[i][j][2]

        r_channel = apply_filter_channel(r_channel, kernel)
        g_channel = apply_filter_channel(g_channel, kernel)
        b_channel = apply_filter_channel(b_channel, kernel)

        y, x, z = img.shape
        img = np.zeros((y, x, z))
        for i in range(y):
            for j in range(x):
                layer = np.array([r_channel[i][j], g_channel[i][j], b_channel[i][j]])
                img[i][j] = layer

    img = img.astype(dtype=np.uint8)
    return Image.fromarray(img)

