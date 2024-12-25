from utils import main_game
import traceback

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
    print(e)
    with open("error.log", "w") as f:
        traceback.print_exc(file=f)
