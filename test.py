from bots import xo_bot
import torch

a = xo_bot.XO_Bot(13)
board = [0] * 169
state = torch.FloatTensor(board).to(a.device)

a.model(state)
a.train(100000)

a.save("bot_xo.mdl")

# from bots import ttt_bots

# a = ttt_bots.TicTacToeBot.load("data/bot/test_1.pkl")
# print(1)
