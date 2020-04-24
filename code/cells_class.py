class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighbours = {}
        self.reward = 0 #default

    def is_wall(self):
        return False

    def is_exit(self):
        return False

    def is_entry(self):
        return False
        
    def is_trap(self):
        return False
    
    def is_treasure(self):
        return False

    def add_neighbour(self, direction, Cell):
        self.neighbours[direction] = Cell
    
    def __str__(self):
        return self.__class__.__name__+"("+str(self.row)+","+str(self.col)+")"
    
    def __repr__(self):
        return " "+self.__class__.__name__+"("+str(self.row)+","+str(self.col)+") "
        
###############################################################################


class Wall(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)

    def is_wall(self):
        return True

###############################################################################

class Floor(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)

###############################################################################

class Trap(Cell):
    def __init__(self, row, col, damage):
        super().__init__(row, col)
        self.reward = damage

    def is_trap(self):
        return True

###############################################################################

class Exit(Cell):
    def __init__(self, row, col, reward):
        super().__init__(row, col)
        self.reward = reward

    def is_exit(self):
        return True

###############################################################################

class Entry(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)

    def is_entry(self):
        return True
###############################################################################

class Treasure(Cell):
    def __init__(self, row, col, reward):
        super().__init__(row, col)
        self.reward = reward
    
    def is_treasure(self):
        return True