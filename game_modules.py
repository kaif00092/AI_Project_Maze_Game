from player import Player
from config import PLAYER_COLOR, SECOND_PLAYER_COLOR, COLS

class GameModes:
    @staticmethod
    def singleplayer():
        return [Player((0, 0), PLAYER_COLOR)]
    
    @staticmethod
    def multiplayer():
        return [
            Player((0, 0), PLAYER_COLOR),
            Player((0, COLS - 1), SECOND_PLAYER_COLOR)
        ]