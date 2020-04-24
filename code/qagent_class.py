from enum import Enum
import random as rd
from cells_class import *
from maze_class import *
from directions_enum import *
from operator import itemgetter

# list of the 10 random seeds used in learn function
#seeds = [42, 1954, 31418, 1618, 5, 7, 11, 13, 17, 19]
rd.seed(3)


class QAgent():

    def __init__(self, obj_mazes):
        self.obj_mazes = obj_mazes
        self.qtab = self.create_qtab_from_obj_maze()
        self.scores = {}
        self.path_followed = []



    def create_qtab_from_obj_maze(self):
        """
        Generates a Q-table from a maze filled with cell objects.
        The Q-table will be 2 rows and 2 cols "smaller" than maze since
        outer walls are considered padding for the neighbour-testing operation
        """
        nb_rows = self.obj_mazes[0].nb_rows
        nb_cols = self.obj_mazes[0].nb_cols
        max_rwd = self.obj_mazes[0].large_reward

        try:
            self.qtab = [[{Dir.UP:max_rwd, Dir.DOWN:max_rwd, Dir.LEFT:max_rwd, Dir.RIGHT:max_rwd} for c in range(nb_cols)] for r in range(nb_rows)]
        except:
            print("Failed to create a Q-table, check the maze.")

        self.adapt_qtab_to_maze()

        return self.qtab



    def adapt_qtab_to_maze(self):
        """
        Adapts the q-table to make it fit the maze, making all actions leading to a wall impossible.
        """
        nb_rows = self.obj_mazes[0].nb_rows
        nb_cols = self.obj_mazes[0].nb_cols

        for r in range(0,nb_rows):            #for each row aka sub-list

            for c in range(0,nb_cols):    #for each element in that row/sub-list
                cell = self.obj_mazes[0].the_maze[r][c]

                if cell.is_wall(): #now checking for object nature of the cell
                    self.qtab[r][c].clear() #remove all actions

                else: #now for all cells, remove actions leading to a wall
                    if self.obj_mazes[0].the_maze[r-1][c].is_wall(): #testing upper neighbour
                        self.qtab[r][c].pop(Dir.UP)

                    if self.obj_mazes[0].the_maze[r][c+1].is_wall(): #testing right neighbour
                        self.qtab[r][c].pop(Dir.RIGHT)

                    if self.obj_mazes[0].the_maze[r+1][c].is_wall(): #testing lower neighbour
                        self.qtab[r][c].pop(Dir.DOWN)

                    if self.obj_mazes[0].the_maze[r][c-1].is_wall(): #testing left neighbour
                        self.qtab[r][c].pop(Dir.LEFT)




    def compute_next_state(self, action, curr_st, curr_maze=0, rd_factor=0):
        """
        Computes the state an agent reaches upon taking a specific action in 
        a specific state. Markovian property is respected: next state 
        depends only on current state and action
        :param action: the direction which the agent intends to follow
        :type action:  Dir enum item
        :param curr_st: the cell where the agent is before taking the 
                        desired transition action
        :type curr_st: Cell
        :curr_maze: the maze the agent is currently in
        :type curr_maze: Maze
        :rd_factor: probability of not being able to take the intended action,
                     corresponds to the envronment's dynamics
        :type rd_factor: float
        """
        curr_row = curr_st.row
        curr_col = curr_st.col

        if rd.uniform(0,1) < rd_factor: #probability of not going where the 
                                        # agent intends to
            #note that in this configuration, it's also possible to end-up in 
            # the initially desired state since all possible actions from the 
            # current state are cnsidered as candidates
            try:
                action = rd.choice(list(self.qtab[curr_st.row][curr_st.col].keys()))
            except:
                print("Ooops, something went wrong, we were unable to pick a random action.")

        #now that action has been updated (either the desired or random one)
        if action == Dir.UP:
            reached_st = self.obj_mazes[curr_maze].the_maze[curr_row-1][curr_col]

        elif action == Dir.DOWN:
            reached_st = self.obj_mazes[curr_maze].the_maze[curr_row+1][curr_col]

        elif action == Dir.LEFT:
            reached_st = self.obj_mazes[curr_maze].the_maze[curr_row][curr_col-1]

        elif action == Dir.RIGHT:
            reached_st = self.obj_mazes[curr_maze].the_maze[curr_row][curr_col+1]

        else:
            raise ValueError("Impossible action")

        return action, reached_st



    def find_optimal_action(self, curr_st):
        """
        Scans through the dictionary containnig all possible actions
         in this particular state, looking for max
        :param curr_st: the state the agent is currently in when
                        trying to pick an action
        :type curr_st: Cell
        :return: the action with highest q-value available and
                the given q-value
        :rtype: Tuple (Dir, float)
        """
        possible_actions = self.qtab[curr_st.row][curr_st.col]
        best_act = max(possible_actions.items(), key=itemgetter(1))[0]
        max_val = possible_actions[best_act]
        try:
            assert (best_act is not None), "Ooops, something went wrong... there seems to be no best action"
        except AssertionError:
            print("Best action doesn't exist (yet?)!")

        return best_act, max_val





    def take_step(self, curr_st, curr_maze=0, epsilon=0.1, rd_factor=0):
        """
        Does a one-step exploration or exploitation action,
        depending on randomness
        :param curr_st: the agent's position before taking the step
        :type curr_st: Cell
        :param epsilon: the exploration rate
        :type epsilon: float
        :param rd_factor: the environment's stochasticity,
                        aka the possibility for the agent to not
                        be able to take the action it had intended
        :type rd_factor: float
        :return: the action the agent will have effectively taken,
                having taken into account all sources of randomness,
                and the state the egnt ends up in after having performed this action
        :rtype: Tuple (Dir, Cell)
        """
        if rd.uniform(0,1) < epsilon: #explore
            act_taken = rd.choice(list(self.qtab[curr_st.row][curr_st.col].keys()))

        else: #greedy exploitation
            act_taken, _ = self.find_optimal_action(curr_st)

        final_action, reached_st = self.compute_next_state(act_taken, curr_st, curr_maze, rd_factor)

        self.scores[curr_maze] += reached_st.reward #update the agent's score

        return final_action, reached_st



    def update_qtable(self, act_taken, curr_st, next_st, alpha, gamma, nb_steps):
        """
        Performs the update of the agent's q-table values
        :param act_taken: the action the agent is taking,
                        transitioning from current_st to next_st
        :type act_taken: Dir
        :param curr_st: the agent's position before transition
        :type curr_st: Cell
        :param next_st: the position the agent will be in after transition
        :type next_st: Cell
        :param alpha: learning rate
        :type alpha: float
        :param gamma: discount factor
        :type gamma: float
        :param nb_steps: the number of steps the agent has already taken,
                        corresponding to a time penalty
        :type nb_steps: int
        :return: None
        :rtype: None
        """
        # the value of the action according to the current state (the position in qtable)
        curr_st_val_for_taken_action = self.qtab[curr_st.row][curr_st.col][act_taken]

        # the value of the optimal choice in next state
        _ , next_st_opti_val = self.find_optimal_action(next_st)

        reward = next_st.reward - nb_steps

        #q-table update equation, including time penalty
        computed_val = ( curr_st_val_for_taken_action +
                        alpha * ( reward + gamma * (
                            next_st_opti_val - curr_st_val_for_taken_action))) #- nb_steps

        #update q-table
        self.qtab[curr_st.row][curr_st.col][act_taken] = computed_val




    def do_one_episode(self, start_st, curr_maze, alpha=0.5, gamma=0.9, epsilon=0.1, rd_factor=0):
        finished = False
        path = []
        curr_st = start_st
        nb_steps = 0

        while not finished: #as long as maze not exited...

            #... take a step into the maze
            act_taken, reached_st = self.take_step(curr_st, curr_maze, epsilon, rd_factor)

            #update qtable
            self.update_qtable(act_taken, curr_st, reached_st, alpha, gamma, nb_steps)

            path.append(act_taken) #update path

            curr_st = reached_st #prepare next iteration
            nb_steps += 1   #to compute punishment for loitering

            if curr_st.is_exit(): #check whether exit has been reached
                finished = True #update flag to exit loop

        return path, curr_st



    def learn(self, opti_steps, start_st,
            alpha_init=0.5, alpha_decrease=0.001,
            gamma=0.9,
            init_epsilon=0.95, epsilon_decrease_factor=0.99,
            rd_factor=0, nb_episodes=1000,
            acceptability_tolerance=10):
        """
        Performs the full learning over all mazes given as input
        :param opti_steps: number of steps contained in the best path
        :type opti_steps: int
        :param start_st: the cell where the agent is initially placed 
                        when starting exploration of the maze
        :type start_st: Cell
        :param alpha_init: initial value of the learning rate
        :type alpha_init: float
        :param alpha_decrease: percentage regulating the decrease of 
                                the learning rate at each cycle
        :type alpha_decrease: float
        :param gamma: importance given to long-term or near-term rewards
        :type gamma: float
        :param init_epsilon: initial value of the exploration tendency
        :type init_epsilon: float
        :param epsilon_decrease_factor: the factor by which epsilon should 
                                        be decreased at each cycle
        :type epsilon_decrease_factor: float
        :param rd_factor: stochastics of the environment, aka possibility of 
                            not taking intended action depsite trying to
        :type rd_factor: float
        :param nb_episodes: desired number of episodes to run
        :type nb_episodes: int
        :param acceptability_tolerance: percentage representing the range 
                                        bounds of acceptable number of steps
                                         to be considered optimal
        :type acceptability_tolerance: int
        """

        nb_of_mazes = len(self.obj_mazes)
        epsilon = init_epsilon
        alpha = alpha_init
        convergence_thresholds = [0]  * nb_of_mazes #one convergence th per maze
        convergence_threshold_def = False
        opti_ub = opti_steps + opti_steps//acceptability_tolerance #+x% tolerance
        opti_lb = opti_steps - opti_steps//acceptability_tolerance #-x% tolerance
        paths = [None] * nb_of_mazes
        reached_sts = [None] * nb_of_mazes
        #for each maze, contains a tuple with Y being length of path before exit and X the episode
        perf_monitor = [[[0 for i in range(nb_episodes)],[0 for i in range(nb_episodes)]]] * nb_of_mazes

        maze_num = 0
        for m in self.obj_mazes: #for each maze
            self.scores[maze_num] = 0 # initialize this maze's score

            for i in range(nb_episodes): #do the desired number of episodes

                self.scores[maze_num] = 0   #re-init this round's score

                paths[maze_num], reached_sts[maze_num] = self.do_one_episode(start_st, maze_num, alpha, gamma, epsilon, rd_factor)
                perf_monitor[maze_num][0][i] = i #X episode
                perf_monitor[maze_num][1][i] = len(paths[maze_num]) #Y, number of steps
                #print(self.scores[maze_num])

                #update hyper-parameters
                if alpha > 0 + alpha_decrease: #alpha can never become negative
                    alpha -= alpha_decrease
                    epsilon *= epsilon_decrease_factor

                #check whether convergence is attained
                curr_nb_steps = len(paths[maze_num])
                if (not convergence_threshold_def) and (curr_nb_steps <= opti_ub) and (curr_nb_steps >= opti_lb):#acceptability_threshold):
                    convergence_thresholds[maze_num] = i
                    convergence_threshold_def = True #update only the first time it's reached
            
            #Preparing for next maze
            convergence_threshold_def = False
            maze_num += 1
            epsilon = init_epsilon
            alpha = alpha_init

        return convergence_thresholds, paths, reached_sts, perf_monitor
