import random

from typing import Tuple, List, Union

import config
from app.field_utils import get_distance
from app.classes.game_state import GameState
from app.classes.mine_field import MineField


class Sweeper:
    """
    To make sweeper win more often, a very basic game strategy was implemented.
    Once there is a cell with nearest mine cell distance > 1, sweeper tries to discover cells next to it(safe cells).
    If no other safe cells with undiscovered neighbors are left on the mine field, random guesses are made.

    For example, it is safe to discover all cells with question marks on the field below,
    because nearest mine cell is located 2 cells form it.

    | ?   | ?   | ... |
    | ?   | 2   | ... |
    | ... | ... | ... |
    Example mine field map extract.
    """

    def __init__(self, mine_field: MineField):
        self._mine_field = mine_field
        self._horizontal_field_size = len(mine_field.get_field_state()[0])
        self._vertical_field_size = len(mine_field.get_field_state())
        self._mine_cell = config.MINE_CELL
        self._empty_cell = config.EMPTY_CELL
        self._unknown_cell = config.UNKNOWN_CELL
        self._non_distance_cells = [self._mine_cell, self._empty_cell, self._unknown_cell]

    def sweep(self) -> str:
        """
        Tries to clean mine field.
        Should be called 1-once per initialized instance.

        Usage example:

        ```
            from app.classes.sweeper import Sweeper
            from app.classes.mine_field import MineField

            mine_field = MineField(horizontal_size=5, vertical_size=5, mines=4, discoverable_radius=2, opened_cells=5)
            sweeper = Sweeper(mine_field)
            print(sweeper.sweep())
        ```

        :return (str): Final game state ("won" or "lost"). Can be used for further evaluation of how good algorithm is.
        """

        game_state = self._mine_field.get_game_state()
        while game_state == GameState.InProgress.value:
            safe_cell_coordinates = self._find_next_safe_cell_coordinates()
            if safe_cell_coordinates:
                next_move_coordinates = safe_cell_coordinates
            else:
                unknown_cells_coordinates = self._get_unknown_cells_coordinates(self._mine_field.get_field_state())
                random_unknown_cell_coordinate_index = random.randint(0, len(unknown_cells_coordinates) - 1)
                next_move_coordinates = unknown_cells_coordinates[random_unknown_cell_coordinate_index]
            self._mine_field.discover_cell(next_move_coordinates[0], next_move_coordinates[1])
            game_state = self._mine_field.get_game_state()
        return game_state

    def _find_next_safe_cell_coordinates(self) -> Union[Tuple[int, int], None]:
        field_state = self._mine_field.get_field_state()
        for y, row in enumerate(field_state):
            for x, cell in enumerate(row):
                if cell not in self._non_distance_cells:  # Cell contains distance to mine.
                    mine_distance = cell
                    if mine_distance > 1:
                        coordinates = self._get_unknown_cell_inside_radius(field_state, x, y, mine_distance)
                        if coordinates and field_state[coordinates[1]][coordinates[0]] == self._unknown_cell:
                            return coordinates

    def _get_unknown_cell_inside_radius(self, field_state, x1, y1, radius) -> Union[Tuple[int, int], None]:
        for y2, row in enumerate(field_state):
            for x2, cell in enumerate(row):
                distance = get_distance((x1, y1,), (x2, y2,))
                if distance < radius and cell == self._unknown_cell:
                    return x2, y2

    def _get_unknown_cells_coordinates(self, field_state) -> List[Tuple[int, int]]:
        unknown_cells_coordinates = []
        for y, row in enumerate(field_state):
            for x, cell in enumerate(row):
                if cell == self._unknown_cell:
                    unknown_cells_coordinates.append((x, y,))
        return unknown_cells_coordinates

    def __repr__(self):
        return "Sweeper(mine_field=MineField())"
