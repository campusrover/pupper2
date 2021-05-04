import _pickle as pickle
import time
from path_finder import PathFinder
from boundary_detection import * 
import matplotlib.pyplot as plt

env = pickle.load(open('sample_env.pkl', 'rb'))
p = PathFinder(env, env.agent, Point(2, 7))
p.solve()
env.path = p.export_path()
env.update_viz()
env.show_viz()
# path_x = list(map(lambda p: p.x, env.path))
# path_y = list(map(lambda p: p.y, env.path))
# plt.plot(path_x, path_y, color='g')
# plt.show()