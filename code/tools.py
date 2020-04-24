from plotting import *

def display_results(agent, paths, conv_ths, last_sts, perfs, nb_mazes=1):
    for i in range(nb_mazes):
        print("##########################")
        print("######## MAZE ", i, " ########")
        print("##########################")
        print("Score == ", agent.scores[i])
        print("Number of steps in best path == ", len(paths[i]))
        print("Convergence threshold == ", conv_ths[i])
        print("Exit coordinates == ", last_sts[i])
        print()
        print_track_followed(paths[i])
        label = "maze_" + str(i) + "_perfs"
        do_plot_2D(perfs[i][0], perfs[i][1], label, "number of episodes", "number of steps")
        print()
        print()


def print_track_followed(path):
    i=0
    for step in range(len(path)):
        print(path[step], end=" -> ")
        i += 1
        if i % 10 == 0:
            print()