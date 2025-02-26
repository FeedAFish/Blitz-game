import os
import pytest
import sys
import traceback

sys.path.append(os.path.abspath("./"))


def test_dl():
    from utils import data_dl

    data_dl.Download_UI(
        version="0.4",
        url="https://drive.google.com/uc?id=1_e2zIMJjbTr-qf5qGEiFO4UQTw8pqBTF",
    )
    assert not os.path.exists("data.zip")
    assert os.path.exists("data/version.ini")


def test_main_game():
    from utils import main_game

    try:
        game = main_game.Game(800, 600)
        game.choice_menu()
        game.board_ttt()
        game.board_snake()
        game.board_lines()
        game.board_2048()
        game.board_animal()
        game.board_bejeweled()
        # game.board_xo()
    except Exception as e:
        traceback.print_exc()
        assert False
    assert True
