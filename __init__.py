import sys

from game import Game

arguments = sys.argv
two_player_mode = False
server_ip = ''

if len(arguments) > 1:
    if arguments[1] == 'y':
        two_player_mode = True
if len(arguments) > 2:
    server_ip = arguments[2]

game = Game(two_player_mode, server_ip)
game.start_game()
