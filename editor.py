#!/usr/bin/env python3
import argparse
import sys
from filters import *
from helpers import *

# Defining command's arguments
parser = argparse.ArgumentParser(description="Image editor")
parser.add_argument('-r', '--rotate', action='store_true', help="Right rotate 90°")
parser.add_argument('-m', '--mirror', action='store_true', help="Mirror image")
parser.add_argument('-i', '--inverse', action='store_true', help="Inverse image")
parser.add_argument('-b', '--bw', action='store_true', help="Gray scale")
parser.add_argument('-s', '--sharpen', action='store_true', help="Unsharp mask")
parser.add_argument('-l', '--lighten', type=int, help="Lighten image <0-100>%")
parser.add_argument('-d', '--darken', type=int, help="Darken image <0-100>%")
parser.add_argument('INPUT_IMAGE_PATH', help="Input image path")
parser.add_argument('OUTPUT_IMAGE_PATH', help="Output image path")


# Transformation routing
def apply_transformation(image: Image, transformation: str, optional=0) -> Image:
    """
    Choose correct transformation in accordance with input
    :param image: input PIL Image
    :param transformation: transformation option
    :param optional: percentage for darken or lighten filter
    :return: edited PIL Image
    """
    transformations = {'-r': rotate_r, '--rotate': rotate_r, '-m': mirror, '--mirror': mirror,
                       '-i': inverse, '--inverse': inverse, '-b': grayscale, '--bw': grayscale,
                       '-s': sharpen, '--sharpen': sharpen, '-l': brightness_change, '--lighten': brightness_change,
                       '-d': brightness_change, '--darken': brightness_change }
    return transformations[transformation](image, transformation, optional)


def run(arg_list: list, arg_values) -> None:
    """
    Main function of the editor. Handles the order of applying transformations(filters). Also
    checks for the validity of input arguments. In case of an invalid input - terminates the program
    :param arg_list: list of input arguments
    :param arg_values: values of arguments(True or false, value) from argparse
    """
    if len(arg_list) == 3:
        print('At least one transformation(filter) is required')
        return

    image = open_image(arg_values.INPUT_IMAGE_PATH)
    if not image:
        return

    print('Processing your image...')
    for i in range(1, len(arg_list)):
        # skipping arguments, which are image paths or lighten-darken percentage
        if not (arg_list[i][0] == '-' or arg_list[i][0:1] == '--' or type(arg_list[i]) == "class 'int'"):
            continue
        # handling lighten-darken case
        if arg_list[i] in ('-d', '--darken', '-l', '--lighten'):
            if not 0 <= int(arg_list[i + 1]) <= 100:
                print('Invalid argument value')
                return
            image = apply_transformation(image, arg_list[i], arg_list[i + 1])
            continue
        # usual case
        image = apply_transformation(image, arg_list[i])

    print('Your image has been processed!')

    if not save_img(image, arg_values.OUTPUT_IMAGE_PATH):
        return

    print('Done!')
    return


run(sys.argv, parser.parse_args())
