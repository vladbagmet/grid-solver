import pytest
from copy import deepcopy

from typing import List, Union

import config
from app.classes.mine_field import MineField
from app.classes.game_state import GameState

"""
Pre-defined mine field map representation.

[
    [" ", " "],
    [" ", "X"],
    ["?", "?"]
]
"""
PRE_DEFINED_MINE_FIELD_MAP = [
    [config.EMPTY_CELL, config.EMPTY_CELL],
    [config.EMPTY_CELL, config.MINE_CELL],
    [config.UNKNOWN_CELL, config.UNKNOWN_CELL]
]


def get_pre_defined_mine_field(mine_field_map: List[List[Union[str, int]]]) -> MineField:
    mine_field = MineField(
        horizontal_size=3,
        vertical_size=3,
        mines=1,
        discoverable_radius=1,
        opened_cells=1
    )
    # Coping to avoid pre-defined data changes between tests.
    mine_field.set_pre_defined_field_map(deepcopy(mine_field_map))
    return mine_field


def test_correct_cell_discovery():
    x = 0
    y = 2
    mine_field = get_pre_defined_mine_field(PRE_DEFINED_MINE_FIELD_MAP)
    assert mine_field.get_field_state()[y][x] == config.UNKNOWN_CELL, "The value of the cell " \
                                                                      "should be unknown before discovery."
    mine_field.discover_cell(x, y)
    assert mine_field.get_field_state()[y][x] != config.UNKNOWN_CELL, "The value of the cell should be changed " \
                                                                      "to non-unknown value after discovery."


def test_outside_mine_field_cell_discovery():
    x = 100
    y = 100
    mine_field = get_pre_defined_mine_field(PRE_DEFINED_MINE_FIELD_MAP)
    with pytest.raises(ValueError) as _:
        mine_field.discover_cell(x, y)


def test_mine_cell_discovery():
    x = 1
    y = 1
    mine_field = get_pre_defined_mine_field(PRE_DEFINED_MINE_FIELD_MAP)
    assert mine_field.get_game_state() == GameState.InProgress.value, "Before cell discovery the state " \
                                                                      "of the mine field " \
                                                                      f"should be `{GameState.InProgress.value}`."
    mine_field.discover_cell(x, y)
    assert mine_field.get_game_state() == GameState.Lost.value, "After cell discovery the state " \
                                                                "of the mine field should be changed " \
                                                                f"to `{GameState.Lost.value}`."


def test_mine_field_cleaning_completion():
    mine_field = get_pre_defined_mine_field(PRE_DEFINED_MINE_FIELD_MAP)

    mine_field.discover_cell(0, 2)
    assert mine_field.get_game_state() == GameState.InProgress.value

    mine_field.discover_cell(1, 2)
    assert mine_field.get_game_state() == GameState.Won.value, "Leaving 1 unknown cell on the 1-mine field " \
                                                               f"should change game state to `{GameState.Won.value}`."
