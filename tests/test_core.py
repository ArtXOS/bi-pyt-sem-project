from pytest import fixture
from numpy.testing import assert_equal
from sem.filters import *
from sem.helpers import *
import numpy as np
import subprocess
import os


@fixture
def image():
    return open_image('tests/lenna.png')


@fixture
def image_rotate():
    return np.array(open_image('tests/image_rotate.png'), dtype=np.uint8)


@fixture
def image_mirror():
    return np.array(open_image('tests/image_mirror.png'), dtype=np.uint8)


@fixture
def image_inverse():
    return np.array(open_image('tests/image_inverse.png'), dtype=np.uint8)


@fixture
def image_grayscale():
    return np.array(open_image('tests/image_grayscale.png'), dtype=np.uint8)


@fixture
def image_brightness_change_50d():
    return np.array(open_image('tests/image_brightness_change_50d.png'), dtype=np.uint8)


@fixture
def image_brightness_change_100d():
    return np.array(open_image('tests/image_brightness_change_100d.png'), dtype=np.uint8)


@fixture
def image_brightness_change_50l():
    return np.array(open_image('tests/image_brightness_change_50l.png'), dtype=np.uint8)


@fixture
def image_brightness_change_100l():
    return np.array(open_image('tests/image_brightness_change_100l.png'), dtype=np.uint8)


@fixture
def image_sharpen():
    return np.array(open_image('tests/image_sharpen.png'), dtype=np.uint8)


def test_rotate_r(image, image_rotate):
    assert_equal(np.array(rotate_r(image), dtype=np.uint8), image_rotate)


def test_mirror(image, image_mirror):
    assert_equal(np.array(mirror(image), dtype=np.uint8), image_mirror)


def test_inverse(image, image_inverse):
    assert_equal(np.array(inverse(image), dtype=np.uint8), image_inverse)


def test_grayscale(image, image_grayscale):
    assert_equal(np.array(grayscale(image), dtype=np.uint8), image_grayscale)


def test_brightness_change_50d(image, image_brightness_change_50d):
    assert_equal(np.array(brightness_change(image, '-d', 50), dtype=np.uint8), image_brightness_change_50d)


def test_brightness_change_100d(image, image_brightness_change_100d):
    assert_equal(np.array(brightness_change(image, '-d', 100), dtype=np.uint8), image_brightness_change_100d)


def test_brightness_change_50l(image, image_brightness_change_50l):
    assert_equal(np.array(brightness_change(image, '-l', 50), dtype=np.uint8), image_brightness_change_50l)


def test_brightness_change_100l(image, image_brightness_change_100l):
    assert_equal(np.array(brightness_change(image, '-l', 100), dtype=np.uint8), image_brightness_change_100l)


def test_invalid_input_file_name_output():
    output = subprocess.Popen("python editor.py ./data/lena.png ./data/dwq -r", shell=True,
                              stdout=subprocess.PIPE).stdout.read()
    target = b"Invalid input file name\n"
    assert target == output


def test_invalid_output_file_name_output():
    output = subprocess.Popen("python editor.py ./data/lenna.png ./data/dwq -r", shell=True,
                              stdout=subprocess.PIPE).stdout.read()
    target = b"Processing your image...\nRotation...\nYour image has been processed!\nInvalid output file name\n"
    assert target == output


def test_no_transform_output():
    output = subprocess.Popen("python editor.py ./data/lenna.png ./data/dwq.png", shell=True,
                              stdout=subprocess.PIPE).stdout.read()
    target = b"At least one transformation(filter) is required\n"
    assert target == output


def test_order_of_processing():
    output = subprocess.Popen("python editor.py ./data/lenna.png ./data/dwq.png -r -m -r -m -m -s", shell=True,
                              stdout=subprocess.PIPE).stdout.read()
    target = b"""Processing your image...
Rotation...
Mirroring...
Rotation...
Mirroring...
Mirroring...
Sharpening...
Your image has been processed!
Saving to..../data/dwq.png
Done!\n"""
    os.remove('./data/dwq.png')
    assert target == output
