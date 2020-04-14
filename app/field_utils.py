import math
import random

from typing import Tuple


def get_distance(coordinate_1: Tuple[int, int], coordinate_2: Tuple[int, int]) -> int:
    return int(math.sqrt((coordinate_2[0] - coordinate_1[0]) ** 2 + (coordinate_2[1] - coordinate_1[1]) ** 2))


def generate_random_coordinates(horizontal_board_size: int, vertical_board_size: int) -> Tuple[int, int]:
    x = random.randint(0, horizontal_board_size - 1)
    y = random.randint(0, vertical_board_size - 1)
    return x, y
