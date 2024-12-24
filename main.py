from utils import main_game

# Run the download file
from utils import data_dl

data_dl.Download_UI(
    version="0.2",
    url="https://drive.google.com/uc?id=1_e2zIMJjbTr-qf5qGEiFO4UQTw8pqBTF",
)

# Run the main game
try:
    game = main_game.Game(800, 600)
    game.run()
except Exception as e:
    with open("error.log", "a") as f:
        f.writelines(str(e))
