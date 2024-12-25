import sys
import os
from utils import main_game, data_dl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_download_ui():
    data_dl.Download_UI(
        version="0.2",
        url="https://drive.google.com/uc?id=1_e2zIMJjbTr-qf5qGEiFO4UQTw8pqBTF",
    )
    assert os.path.exists("data.7z")
    with open("data/version.ini", "r") as f:
        assert f.read() == "0.2"


def test_game_initialization():
    game = main_game.Game(800, 600)
    assert game.running == True
    assert len(game.load_list) == 3
    game.choice_menu()
    assert len(game.load_list) == 4
    game.board_ttt()
    game.board_snake()
    game.board_lines()
    game.exit()
