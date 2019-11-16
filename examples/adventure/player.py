import os
from game_data import Item


class Player:

    def __init__(self, x, y):
        """(int, int) -> Player
        Creates a new Player with an empty inventory (dict), a score of 0, and a specified number of moves MAX_MOVES
        x: x-coordinate of position on map, non-negative integer
        y: y-coordinate of position on map, non-negative integer
        """
        MAX_MOVES = 50
        STARTING_SCORE = 0
        self._inventory = {}
        self.victory = False

        if os.path.exists('save_game.txt'):
            handle = open('save_game.txt', 'r')
            contents = handle.readline()
            contents = contents.split()
            MAX_MOVES = int(contents[0])
            STARTING_SCORE = int(contents[1])
            x = int(contents[2])
            y = int(contents[3])
            self.load_items()

        self.x = x
        self.y = y
        self.score = STARTING_SCORE
        self.moves_remaining = MAX_MOVES

    def move(self, dx, dy):
        """(Player, int, int) -> NoneType
        Given integers dx and dy, move player to 
        new location (self.x + dx, self.y + dy)
        return: None
        """
        self.x += dx
        self.y += dy
        self.moves_remaining -= 1

    def move_north(self):
        """(Player) -> NoneType"""
        self.move(0, -1)

    def move_south(self):
        """(Player) -> NoneType"""
        self.move(0, 1)

    def move_east(self):
        """(Player) -> NoneType"""
        self.move(1, 0)

    def move_west(self):
        """(Player) -> NoneType"""
        self.move(-1, 0)

    def add_item(self, item):
        """(Player, Item) -> NoneType"""
        self._inventory[item.get_name()] = item

    def remove_item(self, item):
        """(Player, Item) -> NoneType"""
        del self._inventory[item.get_name()]

    def get_inventory(self):
        """(Player) -> dict of str to Item"""
        return self._inventory

    def load_items(self, filename='pers_items.txt'):
        """(World, str) -> NoneType
        Loads item data into Item objects and stores items in Player object
        param filename: name of text file containing item data in the format:
            ORIGIN DESTINATION POINTS NAME
            int    int         int    str, in Title Case
        return: None
        """
        if not os.path.exists('pers_items.txt'):
            return None
        with open(filename, 'r') as handle:
            for line in handle:
                data = line.split()
                start, end, points = int(data[0]), int(data[1]), int(data[2])
                name = line[line.rfind(data[2])+len(data[2])+1:].rstrip()
                item = Item(name, start, end, points)
                if start == 0:
                    self.add_item(item)

    def save(self):
        """(Player) -> NoneType
        Saves player progress data of current game to a new text file and 
        player item data to the same file as item data stored from Locations.
        """
        with open('save_game.txt', 'w') as player_filehandle:
            player_filehandle.write(str(self.moves_remaining) + ' ' +
                                    str(self.score) + ' ' + str(self.x) + ' ' + str(self.y))
        with open('pers_items.txt', 'a') as item_filehandle:
            for key, item in self.get_inventory().items():
                item_filehandle.write('0' + ' ' +
                                      str(item.get_target_location()) + ' ' +
                                      str(item.get_target_points()) + ' ' +
                                      item.get_name() + '\n')
