from typing import Union

from utils.image import PackedImage, StrideImage
from utils.pixel import Pixel
from utils.resolution import Resolution


def pixelsToMatrix(image: Union[PackedImage, StrideImage]) -> [[Pixel]]:
    pixels = None
    if isinstance(image, PackedImage):
        pixels = image.pixels
    if isinstance(image, StrideImage):
        pixels = image.merge_pixel_components()

    result = []
    # TODO is the assumption below correct?
    # assuming that the pixels are ordered by rows instead of columns
    # wether we start from the first or the last row shouldn't matter in the currenct case
    # since the patterns are symmetric
    for i in range(0, (len(pixels)), image.resolution.width):
        result.append(pixels[i: i + image.resolution.width])

    return result


def matrixToPackedImage(matrix: [[Pixel]]) -> PackedImage:
    pixels = []
    for row in matrix:
        pixels += row
    return PackedImage(Resolution(width=len(matrix[0]), height=len(matrix)), pixels)
def matrixToStrideImage(matrix: [[Pixel]]) -> StrideImage:
    pixels = []
    for row in matrix:
        pixels += row
    return StrideImage(Resolution(width=len(matrix[0]), height=len(matrix)), pixels)
