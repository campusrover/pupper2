import _pickle as pickle
import time
from path_finder import PathFinder
from boundary_detection import * 
from path_profiler import Profiler
import matplotlib.pyplot as plt

env = pickle.load(open('sample_env.pkl', 'rb'))

pf = PathFinder(env, env.agent, Point(2, 7))
pf.solve()
env.path = pf.export_path()
print(len(env.path))

env.update_viz()
env.show_viz()

pr = Profiler()
pr.add_path(env.path)
pp = pr.get_profile()
pr.smooth_path()

