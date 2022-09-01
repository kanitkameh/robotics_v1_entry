#!/usr/bin/env python3
from curses.ascii import isspace
from typing import (
    List,
    Tuple,
    Union
)

from utils.ImageMatrixConverter import matrixToPackedImage, matrixToStrideImage, pixelsToMatrix
from utils.corner import Corner
from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)

from utils.eye_pattern import *
from utils.function_tracer import FunctionTracer
from utils.pixel import Pixel
from utils.resolution import Resolution

# the value of the red channel needed in the non white pixels to be filtered
RED_COMPONENT_EYE_THRESHOLD = 200
RED_REDUCTION = 150

def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for i in range(0,len(images)):
        filteredMatrix = processImage(images[i])
        if isinstance(images[i], PackedImage):
            images[i] = matrixToPackedImage(filteredMatrix)
        if isinstance(images[i], StrideImage):
            images[i] = matrixToStrideImage(filteredMatrix)

    del ft




def processImage(image: Union[PackedImage, StrideImage]) -> PackedImage:
    resolution = image.resolution
    # transform the list of pixels to 2d array of pixels
    matrix = pixelsToMatrix(image)
    for row in range(0, resolution.height):
        for column in range(0, resolution.width):
            topLeftCorner = Corner(row, column)
            pattern = findMatchingPattern(matrix, topLeftCorner)

            if(not(pattern is None)):
                filterRedEyes(matrix, pattern, topLeftCorner)

    return matrix


def findMatchingPattern(matrix: [[Pixel]], topLeftCorner: Corner):
    patterns = [EYE_PATTERN_1, EYE_PATTERN_2, EYE_PATTERN_3, EYE_PATTERN_4]
    for pattern in patterns:
        if checkPattern(matrix, topLeftCorner, pattern):
            return pattern
    return None

# checks if the pattern is
def checkPattern(matrix: [[Pixel]], topLeftCorner: Corner, pattern: EyePattern) -> bool:
    for rowOffset in range(0, len(pattern)):
        for columnOffset in range(0, len(pattern[0])):
            patternSymbol = pattern[rowOffset][columnOffset]
            matrixRedComponnet = matrix[topLeftCorner.row + rowOffset][topLeftCorner.column + columnOffset].red
            if(not(isspace(patternSymbol)) and matrixRedComponnet < RED_COMPONENT_EYE_THRESHOLD):
                return  False
    return True

def filterRedEyes(matrix: [[Pixel]], pattern, topLeftCorner: Corner):
    for rowOffset in range(0, len(pattern)):
        for columnOffset in range(0, len(pattern[0])):
            patternSymbol = pattern[rowOffset][columnOffset]
            if(not(isspace(patternSymbol))):
                matrix[topLeftCorner.row + rowOffset][topLeftCorner.column + columnOffset].red -= RED_REDUCTION
