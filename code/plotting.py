import matplotlib.pyplot as plt
import os

def do_plot_2D(x,y,f_name, x_lab="X", y_lab="Y"):
    # f, ax = plt.subplots(1)
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'Plots/')
    file_name = "plot_" + f_name + ".png"

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    plt.plot(x,y)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    # ax.plot(x, y)
    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=0)
    #plt.show()
    plt.savefig(results_dir + file_name)

"""a = [1, 10, 100, 1000]
b = [1, 2, 3, 4]
do_plot(a, b, "yeah")"""