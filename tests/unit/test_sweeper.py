from app.classes.sweeper import Sweeper
from app.classes.game_state import GameState
from app.classes.mine_field import MineField


def test_game_finished():
    horizontal_size = 3
    vertical_size = 3
    mine_field = MineField(
        horizontal_size=horizontal_size,
        vertical_size=vertical_size,
        mines=1,
        discoverable_radius=1,
        opened_cells=1
    )
    sweeper = Sweeper(mine_field)

    while True:
        if mine_field.get_game_state() != GameState.InProgress.value:
            break
        sweeper.sweep()
    assert mine_field.get_game_state() in [GameState.Won.value, GameState.Lost.value], "Game should be finished."
