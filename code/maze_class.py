from enum import Enum
import random as rd

from cells_class import *
from directions_enum import *

#set rd seed to allow reproduction
rd.seed(42)


class Maze():
    def __init__(self, ascii_maze, nb_rows=10, nb_cols=10,
                sm_ex=1, l_ex=1000, 
                sm_dmg=5, l_dmg=10000,
                sm_rwd=1, l_rwd=10):
        self.small_exit_rwd = sm_ex
        self.large_exit_rwd = l_ex
        self.small_trap_damage = sm_dmg
        self.large_trap_damage = l_dmg
        self.small_reward = sm_rwd
        self.large_reward = l_rwd
        self.ascii_maze = ascii_maze
        self.nb_rows = nb_rows+2    #wall padding
        self.nb_cols = nb_cols+2    #wall padding
        self.the_maze = self.create_obj_maze_from_ascii_maze()
    
    def get_state_by_coord(self, row, col):
        return self.the_maze[row+1][col+1]

    def create_obj_maze_from_ascii_maze(self):
        #padding added to ease qtab, by default any cell is a wall

        try:
            maze = [[Wall(row,col) for col in range(self.nb_cols)] for row in range(self.nb_rows)]
        except:
            print("Failed to create an object maze, check ASCII file.")

        for r in range(1,self.nb_rows-1):            #for each row aka sub-list

            for c in range(1,self.nb_cols-1):    #for each element in that row/sub-list

                try:
                    symbol = self.ascii_maze[r-1][c-1]  #-1 because ascii_maze is smaller than padded obj_maze
                except:
                    print("Ooops, failed to get a symbol from the maze... check your ASCII file.")

                if symbol == '~':
                    new_cell = Floor(r,c)
                elif symbol == 'E':
                    new_cell = Entry(r,c)
                elif symbol == 'X':
                    new_cell = Exit(r,c,self.large_exit_rwd)
                elif symbol == 'x':
                    new_cell = Exit(c,r,self.small_exit_rwd)
                elif symbol == 'T':
                    new_cell = Trap(r,c,-self.large_trap_damage)
                elif symbol == 't':
                    new_cell = Trap(r,c,-self.small_trap_damage)
                elif symbol == 'R':
                    new_cell = Treasure(r,c,self.large_reward)
                elif symbol == 'r':
                    new_cell = Treasure(r,c,self.small_reward)
                elif symbol == 'W':
                    new_cell = Wall(r,c)
                else:
                    raise ValueError("Unaccepted character")

                maze[r][c] = new_cell #adding the cell to the maze

        return maze