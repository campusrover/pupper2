import matplotlib.pyplot as plt
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)


class Vizualizer:
    def __init__(self):
        self.obs = []
        self.ego = None
        self.bds = []
        self.path = None
        self.nodes = []
        self.plot_size_x = params['vizualization_settings']['plot_dim_x']
        self.plot_size_y = params['vizualization_settings']['plot_dim_y']
        self.show_ = params['vizualization_settings']['show_plot']
        self.name = params['vizualization_settings']['map_name']
        
    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_obs(self, obs):
        self.obs = obs

    def set_ego(self, ego):
        self.ego = ego

    def set_bds(self, bds):
        self.bds = bds

    def set_path(self, pts):
        self.path = pts

    def is_valid(self):
        return self.ego is not None

    def show(self):
        if self.is_valid():
            plt.xlim([-self.plot_size_x, self.plot_size_x])
            plt.ylim([-self.plot_size_y, self.plot_size_y])
            # plt.xlim([-self.plot_size_x, self.plot_size_x])
            # plt.ylim([-self.plot_size_y, self.plot_size_y])

            for ob in self.obs:
                ob_x = list(map(lambda p: p.x, ob.points))
                ob_y = list(map(lambda p: p.y, ob.points))
                ob_x.append(ob_x[0])
                ob_y.append(ob_y[0])
                plt.plot(ob_x, ob_y, color='r')
                plt.text(ob_x[0], ob_y[0], ob.uid)
            for bd in self.bds:
                bd_x = list(map(lambda p: p.x, bd))
                bd_y = list(map(lambda p: p.y, bd))
                bd_x.append(bd_x[0])
                bd_y.append(bd_y[0])
                plt.scatter(bd_x, bd_y, color='b', s=10)
            if self.path:
                #print(len(self.path))
                path_x = list(map(lambda p: p.x, self.path))
                path_y = list(map(lambda p: p.y, self.path))
                plt.plot(path_x, path_y, color='g')
            if self.nodes:
                plt.scatter(self.nodes[0], self.nodes[1], color='orange', s=0.1)
            plt.text(path_x[-1], path_y[-1], "X")
            ego_x = list(map(lambda p: p.x, self.ego.points))
            ego_y = list(map(lambda p: p.y, self.ego.points))
            ego_x.append(ego_x[0])
            ego_y.append(ego_y[0])
            plt.plot(ego_x, ego_y, color='y')
            
            if self.show_:
                plt.show()
            else:
                plt.savefig(os.path.join('plots', self.name))