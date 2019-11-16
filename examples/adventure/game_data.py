import os


class Location:

    def __init__(self, num, x_cor, y_cor, points, full_desc, brief_desc):
        '''(int, int, int, str, str) -> Location
        num: a unique positive integer to identify the location
        x_cor: a non-negative integer indicating East position on World map
        y_cor: a non-negative integer indicating South position on World map
        points: the number of points recieved (or lost) visiting the location
        full_desc: a long description of the location
        brief_desc: a short description of the location     
        '''
        self._visited = False
        self.location_num = num
        self._xcor = x_cor
        self._ycor = y_cor
        self.points = points
        self._full_description = full_desc
        self._brief_description = brief_desc
        self._items = {}

    def get_x(self):
        """(Location) -> int"""
        return self._xcor

    def get_y(self):
        """(Location) -> int"""
        return self._ycor

    def get_brief_description(self):
        """(Location) -> str
        Return brief description of location.
        """
        return "\n----------------------- LOCATION: " + str(self.location_num)\
            + " -----------------------\n" + self._brief_description

    def get_full_description(self):
        """(Location) -> str
        Return long description of location.
        """
        return "\n----------------------- LOCATION: " + str(self.location_num)\
            + " -----------------------\n" + self._full_description

    def get_items(self):
        """(Location) -> dict"""
        return self._items

    def is_new(self):
        """(Location) -> bool"""
        return not self._visited

    def visit(self):
        """(Location) -> NoneType"""
        self._visited = True

    def add_item(self, item):
        """(Location) -> NoneType"""
        self._items[item.get_name()] = item

    def remove_item(self, item):
        """(Location) -> NoneType"""
        del self._items[item.get_name()]


class Item:

    def __init__(self, name, start, target, target_points):
        '''(str, int, int, int) -> Item
        name: titlecased name of item
        start: non-negative, the original location of the item
        target: non-negative, the destination the item is required to reach
        target_points: points acquired by player for properly delivering item
        '''
        self._name = name
        self._start = start
        self._target = target
        self._target_points = target_points

    def get_starting_location(self):
        '''(Item) -> int'''

        return self._start

    def get_name(self):
        '''(Item) -> str'''
        return self._name

    def get_target_location(self):
        '''(Item) -> int'''
        return self._target

    def get_target_points(self):
        '''(Item) -> int'''
        return self._target_points


class World:

    def __init__(self, mapdata='map.txt', locdata='locations.txt', itemdata='items.txt'):
        """([str, str, str]) -> World
        Creates a new World object, with a map, and data about every
        location and item in this game world.

        mapdata: name of text file containing map data in grid format:
            (integers represent each location, separated by space)
                E.G.
                1 -1 3
                4 5 6
            Where each number represents a different location,
            and -1 represents an invalid, inaccessible space.

        locdata: name of text file containing location data in the format:
            LOCATION #\n           - (All caps, as given)
            POINTS\n               - (this must be an integer)
            SHORT DESCRIPTION\n    - (no newlines allowed inside description)
            LONG DESCRIPTION\n     - (no newlines allowed inside description)
            END\n                  - (All caps, as given)
            \n                     - (as given)

        itemdata: name of text file containing item data in the format:
            ORIGIN DESTINATION POINTS NAME
            int    int         int    str, in Title Case
        """
        self.locked = True
        # The map MUST be stored in a nested list
        self.map = self.load_map(mapdata)
        # self.locations ... You may choose how to store location and item data
        # This data must be stored somewhere. Up to you how you choose to do it
        self.locations = self.load_locations(locdata)
        # This data must be stored somewhere. Up to you how you choose to do it
        self.load_items(itemdata)

    def load_map(self, filename):
        '''(World, str) -> list of lists
        Load map from filename (map.txt) as a nested list of integers like so:
            1 2 5
            3 -1 4
        becomes [[1,2,5], [3,-1,4]]
        filename: name of txt file in which map data is located in grid format:
            (integers represent each location, separated by space)
                1 -1 3
                4 5 6
            Where each number represents a different location,
            and -1 represents an invalid, inaccessible space.
        return: return nested list of integers representing map of game
        '''
        with open(filename, 'r') as handle:
            map = []
            for line in handle:
                line = line.split()
                locations = []
                for location in line:
                    x = int(location.rstrip())
                    locations.append(x)
                map.append(locations)
        return map

    def load_locations(self, filename='locations.txt'):
        '''(World, str) -> dict{int:Location}
        Load all locations from filename (locations.txt) as a dictionary
        filename: name of text file in which text data is located in format:
            'LOCATION' #\n         - (All caps, then a positive integer)
            POINTS\n               - (this must be an integer)
            SHORT DESCRIPTION\n    - (no newlines allowed inside description)
            LONG DESCRIPTION\n     - (no newlines allowed inside description)
            'END'\n                - (All caps, as given)
            \n                     - (as given)
        return: Dictionary of location number as key, Location object as value
        '''
        with open(filename, 'r') as handle:
            lines = handle.readlines()

        locations = {}
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if idx % 6 == 0:
                location_num = int(line[9:-1])
            elif idx % 6 == 1:
                location_points = int(line)
            elif idx % 6 == 2:
                short_description = line
            elif idx % 6 == 3:
                long_description = line
            elif idx % 6 == 4:
                row_idx = 0
                column_idx = -1
                while row_idx < len(self.map) and column_idx < 0:
                    if location_num in self.map[row_idx]:
                        column_idx = self.map[row_idx].index(location_num)
                    else:
                        row_idx += 1
                locations[location_num] = Location(location_num,
                                                   column_idx, row_idx,
                                                   location_points,
                                                   long_description,
                                                   short_description)
            idx += 1
        return locations

    def load_items(self, filename):
        """(World, str) -> NoneType
        Loads item data into Item objects and stores items in Location objects
        filename: name of text file containing item data in the format:
            ORIGIN DESTINATION POINTS NAME
            int    int         int    str, in Title Case
            (if origin location is 0, player has the item already) 
        return: None
        """
        if os.path.exists('pers_items.txt'):
            filename = 'pers_items.txt'
        with open(filename, 'r') as handle:
            for line in handle:
                data = line.split()
                start, end, points = int(data[0]), int(data[1]), int(data[2])
                name = line[line.rfind(data[2])+len(data[2])+1:].rstrip()
                item = Item(name, start, end, points)
                if start != 0:
                    self.locations[start].add_item(item)

    def save_items(self, filename='pers_items.txt'):
        """(World, str) -> NoneType
        Saves a copy of the original items file, with start locations 
        modified to where the user has moved the items, with location 0
        indicating that the item is in the user's inventory.
        filename: name of text file containing item data in the format:
            ORIGIN DESTINATION POINTS NAME
            int    int         int    str, in Title Case
            (if origin location is 0, player has the item already) 
        return: None
        """
        with open(filename, 'w') as handle:
            for location_number in self.locations:
                location = self.locations[location_number]
                for key in location.get_items():
                    item = location.get_items()[key]
                    handle.write(str(location_number) + ' ' +
                                 str(item.get_target_location()) + ' ' +
                                 str(item.get_target_points()) + ' ' +
                                 item.get_name() + '\n')

    def get_available_actions(self, location, inventory):
        """(World, Location, dict of str mapping to Item objs) -> list of str
        return: list of the available actions in this location."""
        actions = []
        current_x, current_y = location.get_x(), location.get_y()
        if self.get_location(current_x + 1, current_y) != None:
            actions.append('Go East')
        if self.get_location(current_x - 1, current_y) != None:
            actions.append('Go West')
        if self.get_location(current_x, current_y + 1) != None:
            actions.append('Go South')
        if self.get_location(current_x, current_y - 1) != None:
            actions.append('Go North')
        for item_name in inventory:
            actions.append('Drop ' + item_name)
        for item_name in location.get_items():
            actions.append('Take ' + item_name)
        if ('Bolt Cutter' in inventory and location.location_num == 7
                and self.locked == True):
            actions.append('Cut Lock')
        if location.location_num == 38:
            actions.append('Close Locker')
        return actions

    def get_location(self, x, y):
        '''Check if location exists at location (x,y) in world map.
        x: non-negative integer x representing x-coordinate of world map
        y: non-negative integer y representing y-coordinate of world map
        return: Location object associated with this location if it does.
                else, return None.
        '''
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[y]):
            location_number = self.map[y][x]
        else:
            location_number = -1
        location = None
        if location_number != -1:
            location = self.locations[location_number]
        return location
