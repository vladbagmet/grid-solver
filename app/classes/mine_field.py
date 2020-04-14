from typing import Dict, List, Union

from tabulate import tabulate

import config
from app.classes.game_state import GameState
from app.field_utils import get_distance, generate_random_coordinates


class MineField:
    def __init__(
        self,
        horizontal_size: int,
        vertical_size: int,
        mines: int,
        discoverable_radius: int,
        opened_cells: int
    ):
        """
        Initializes mine field with the given parameters.

        :param (int) horizontal_size: Horizontal size of the mine field. Can be any positive number.
        :param (int) vertical_size: Vertical size of the mine field. Can be any positive number.
        :param (int) mines: Number of mines to set on the field. Can be any positive number.
        :param (int) discoverable_radius:  Distance from the current cell where nearest mine cells are looked for.
        :param (int) opened_cells: Cells to open on the mine field before game starts.
        """

        self._validate_init(
            horizontal_size=horizontal_size,
            vertical_size=vertical_size,
            mines=mines,
            discoverable_radius=discoverable_radius,
            opened_cells=opened_cells
        )
        self._game_state = GameState.InProgress.value
        self._empty_cell = config.EMPTY_CELL
        self._mine_cell = config.MINE_CELL
        self._unknown_cell = config.UNKNOWN_CELL

        self._discoverable_radius = discoverable_radius
        self._opened_cells = opened_cells
        self._horizontal_field_size = horizontal_size
        self._vertical_field_size = vertical_size

        self._mines = mines
        self._mines_cells_coordinates = set()
        self._mine_field = self._generate_mine_field()
        self._update_mine_field()

    def discover_cell(self, x: int, y: int) -> None:
        """
        Discovers cell by the given coordinates.

        Mine field data structure example:
        [
            [" ", "X"],
            [" ", " "],
            ["?", "?"]
        ]

        X-axis is growing from left to right.
        Y-axis — from top to the bottom.

        Mine cell coordinates from the example above are:
            x=1
            y=0

        :param (int) x: Cell x-axis coordinate to discover.
        :param (int) y: Cell y-axis coordinate to discover.
        :return (None):
        """

        self._validate_discovery(x, y)
        if (x, y,) in self._mines_cells_coordinates:
            self._game_state = GameState.Lost.value
            for x, y in self._mines_cells_coordinates:
                self._mine_field[y][x] = self._mine_cell
        else:
            self._mine_field[y][x] = self._empty_cell
        self._update_mine_field()

    def get_game_state(self) -> str:
        return self._game_state

    def get_field_state(self) -> List[List[Union[str, int]]]:
        return self._mine_field

    def to_dict(self) -> Dict:
        dict_representation = {}
        for y_index, y in enumerate(self._mine_field):
            for x_index, cell in enumerate(self._mine_field[y_index]):
                dict_representation.update({
                    f"x_{x_index}^y_{y_index}": cell
                })

        return dict_representation

    def set_pre_defined_field_map(self, mine_field_map: List[List[Union[str, int]]]) -> None:
        """
        Sets instance into known-ahead state for testing purpose.
        Input data structure example is given inside `discover_cell()` method.

        :param (List) mine_field_map: Mine field representation.
        :return (None):
        """

        mine_cells_coordinates = set()
        mines = 0

        self._mine_field = mine_field_map
        for y, row in enumerate(mine_field_map):
            for x, cell in enumerate(row):
                if cell == config.MINE_CELL:
                    mine_cells_coordinates.add((x, y,))
                    self._mine_field[y][x] = config.UNKNOWN_CELL
                    mines += 1
        self._mines_cells_coordinates = mine_cells_coordinates
        self._horizontal_field_size = len(mine_field_map[0])
        self._vertical_field_size = len(mine_field_map)
        self._mines = mines
        self._update_mine_field()

    def _generate_mine_field(self) -> List[List[Union[str, int]]]:
        empty_cell_coordinates = set()
        mine_field = [
            [self._unknown_cell for _ in range(self._horizontal_field_size)] for _ in range(self._vertical_field_size)
        ]

        while len(self._mines_cells_coordinates) < self._mines:
            self._mines_cells_coordinates.add(
                generate_random_coordinates(self._horizontal_field_size, self._vertical_field_size)
            )

        while len(empty_cell_coordinates) < self._opened_cells:
            x, y = generate_random_coordinates(self._horizontal_field_size, self._vertical_field_size)
            if (x, y,) not in self._mines_cells_coordinates:
                empty_cell_coordinates.add((x, y,))
                mine_field[y][x] = self._empty_cell

        return mine_field

    def _update_mine_field(self) -> None:
        undiscovered_mines = 0
        for x in range(self._horizontal_field_size):
            for y in range(self._vertical_field_size):
                if self._mine_field[y][x] == self._unknown_cell:
                    undiscovered_mines += 1
                elif self._mine_field[y][x] == self._empty_cell:
                    shortest_mine_distance = self._get_shortest_mine_distance(x, y)
                    if shortest_mine_distance:
                        self._mine_field[y][x] = shortest_mine_distance

        if self._mines == undiscovered_mines and self._game_state == GameState.InProgress.value:
            self._game_state = GameState.Won.value

    def _get_shortest_mine_distance(self, x: int, y: int) -> int:
        nearest_distance = None
        for coordinate in self._mines_cells_coordinates:
            distance = get_distance((x, y,), coordinate)
            if nearest_distance is None or distance < nearest_distance:
                if distance <= self._discoverable_radius:
                    nearest_distance = distance
        return nearest_distance

    def _validate_discovery(self, x, y) -> None:
        if not (x in range(self._horizontal_field_size) and y in range(self._vertical_field_size)):
            raise ValueError("it is not allowed to discover cells outside of the mine field")

        if self.get_game_state() != GameState.InProgress.value:
            raise ValueError(f"only interactions with `{GameState.InProgress.value}` mine fields are allowed")

    @staticmethod
    def _validate_init(
            horizontal_size: int,
            vertical_size: int,
            mines: int,
            discoverable_radius: int,
            opened_cells: int
    ) -> None:
        field_size = horizontal_size * vertical_size

        if horizontal_size < 1 or vertical_size < 1:
            raise ValueError("requested mine field size is incorrect")

        if field_size - opened_cells < mines:
            raise ValueError("mines, opened cells and mine field size should be balanced")

        if discoverable_radius < 0:
            raise ValueError("discoverable radius can not be negative")

    def __str__(self) -> str:
        return tabulate(self._mine_field)

    def __repr__(self) -> str:
        return "Grid(" \
               f"horizontal_size={self._horizontal_field_size}, " \
               f"vertical_size={self._vertical_field_size}, " \
               f"mines={self._mines}, " \
               f"discoverable_radius={self._discoverable_radius}, " \
               f"opened_cells={self._opened_cells})"
