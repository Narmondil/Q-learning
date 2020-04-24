from maze_class import *
from cells_class import *
from directions_enum import *
from qagent_class import *
from tools import *
import mazes as M


############################# SMALL 10x10 maze ################################
maze_obj_03a = Maze(M.ascii_maze_03a, nb_rows=10, nb_cols=10,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=1, l_rwd=100)

maze_obj_03b = Maze(M.ascii_maze_03b, nb_rows=10, nb_cols=10,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=1, l_rwd=100)

mazes = [maze_obj_03a, maze_obj_03b]
starting_st_01 = maze_obj_03a.get_state_by_coord(9,0)
opti_nb_steps_01 = 20


################################### MAZES #####################################

maze_a = Maze(M.ascii_maze_20x20_a, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_b = Maze(M.ascii_maze_20x20_b, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_c = Maze(M.ascii_maze_20x20_c, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_d = Maze(M.ascii_maze_20x20_d, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_e = Maze(M.ascii_maze_20x20_e, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_f = Maze(M.ascii_maze_20x20_f, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_g = Maze(M.ascii_maze_20x20_g, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_h = Maze(M.ascii_maze_20x20_h, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

<<<<<<< HEAD
mazes = [maze_g]
=======
maze_dyn0 = Maze(M.ascii_maze_20x20_dyn0, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_dyn1 = Maze(M.ascii_maze_20x20_dyn1, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_dyn2 = Maze(M.ascii_maze_20x20_dyn2, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_dyn3 = Maze(M.ascii_maze_20x20_dyn3, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_dyn4 = Maze(M.ascii_maze_20x20_dyn4, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

maze_dyn5 = Maze(M.ascii_maze_20x20_dyn5, nb_rows=20, nb_cols=20,
                sm_ex=1, l_ex=1000, 
                sm_dmg=1, l_dmg=1000,
                sm_rwd=5, l_rwd=1000)

mazes = [maze_dyn0, maze_dyn1, maze_dyn2, maze_dyn3, maze_dyn4, maze_dyn5]
#mazes = [maze_e]
>>>>>>> 7b3f73e4d8a33ad2e9f193d6245211efbd44b8c8

starting_st = maze_a.get_state_by_coord(19,0)

opti_nb_steps = 50


################################## AGENT ######################################
agent = QAgent(mazes)

conv_ths, learned_paths, last_sts, perfs = agent.learn(opti_nb_steps, starting_st, 
<<<<<<< HEAD
                                alpha_init=1, alpha_decrease=0.001, 
                                gamma=0.99, 
                                init_epsilon=0.2, epsilon_decrease_factor=1,
                                rd_factor=0,
                                nb_episodes=10000, acceptability_tolerance=5)
=======
                                alpha_init=1, alpha_decrease=0.0001, 
                                gamma=0.9, 
                                init_epsilon=0.1, epsilon_decrease_factor=1,
                                rd_factor=0.15,
                                nb_episodes=5000, acceptability_tolerance=10)
>>>>>>> 7b3f73e4d8a33ad2e9f193d6245211efbd44b8c8


################################## MAIN #####################################

display_results(agent, learned_paths, conv_ths, last_sts, perfs, len(learned_paths))
