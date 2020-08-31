from PIL import Image


def open_image(path: str) -> Image:
    """
    Opens an image and returns it. Handling of an invalid file name is included
    :param path: path to the image
    :return: PIL Image | False in case of an invalid file name
    """
    try:
        image = Image.open(path, mode='r')
    except FileNotFoundError:
        print('Invalid input file name')
        return False
    else:
        return image


def save_img(image: Image, path: str) -> bool:
    """
    Saves an edited image. Handling of an invalid file name (path) is included
    :param image: PIL Image
    :param path: file name, where you want to save the image
    :return: True | False in case of an invalid file name
    """
    try:
        image.save(path)
    except ValueError:
        print('Invalid output file name')
        return False
    else:
        print(f"Saving to...{path}")
        return True
