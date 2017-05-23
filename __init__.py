import sys

import time

from game import Game
from lan import LanServer, LanClient

arguments = sys.argv
two_player_mode = False
server_ip = ''
lan = None

if len(arguments) > 1:
    if arguments[1] == 'y':
        two_player_mode = True

    if len(arguments) > 2:
        server_ip = arguments[2]

    if server_ip == '':
        lan = LanServer()
        lan.start((server_ip, 8082))

        while lan.connection is None:
            time.sleep(0.1)
    else:
        lan = LanClient()
        lan.start((server_ip, 8082))


game = Game(lan)
game.start_game()
