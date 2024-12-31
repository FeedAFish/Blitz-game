import os
import pytest
import sys

sys.path.append(os.path.abspath("./"))


def test_dl():
    from utils import data_dl

    data_dl.Download_UI(
        version="0.2",
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
        game.board_xo()
    except Exception as e:
        with open("error.log", "a") as f:
            f.writelines(str(e))
        assert False
    assert True
