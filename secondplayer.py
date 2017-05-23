from abc import abstractmethod

from block_drawer import GhostBlockDrawer
from figure import Figure
from lan import LanServer, LanClient
from menu import Menu
from stage import Stage


class SecondPlayer:
    @abstractmethod
    def receive_data(self):
        pass

    @abstractmethod
    def send_data(self, figure: Figure, stage: Stage, attack):
        pass

    @abstractmethod
    def draw(self, stage_surface, menu_surface):
        pass


class LanSecondPlayer(SecondPlayer):

    def __init__(self, menu: Menu, server_ip='localhost'):
        self.figure = Figure([])  # type: Figure
        self.stage = Stage()  # type: Stage
        self.stage.block_drawer = GhostBlockDrawer()
        self.menu = menu

        if server_ip == 'localhost':
            self.lan = LanServer()
        else:
            self.lan = LanClient()

        self.lan.start((server_ip, 8082))

    def receive_data(self):
        attack = 0
        data = self.lan.get_data()

        if data:
            data_array = eval(data)
            if len(data_array) == 5:
                self.figure.blocks = data_array[0]
                self.figure.x = data_array[1]
                self.figure.y = data_array[2]
                self.stage.blocks = data_array[3]
                attack = data_array[4]

        return attack

    def send_data(self, figure: Figure, stage: Stage, attack):
        data_array = list()
        data_array.append(figure.blocks)
        data_array.append(figure.x)
        data_array.append(figure.y)
        data_array.append(stage.blocks)
        data_array.append(attack)
        self.lan.send_data(data_array)

    def draw(self, stage_surface, menu_surface):
        self.stage.draw(stage_surface)
        self.figure.draw(stage_surface)
        self.menu.draw_second_player(menu_surface, self.stage.score, self.stage.completed_lines)


class NoPlayer(SecondPlayer):
    def draw(self, stage_surface, menu_surface):
        pass

    def send_data(self, figure: Figure, stage: Stage, attack):
        pass

    def receive_data(self):
        pass
