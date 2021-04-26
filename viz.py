import matplotlib.pyplot as plt
class Vizualizer:
    def __init__(self):
        self.obs = []
        self.ego = None
        self.bds = []
        self.plot_size = 2.5

    def set_obs(self, obs):
        self.obs = obs

    def set_ego(self, ego):
        self.ego = ego

    def set_bds(self, bds):
        self.bds = bds

    def is_valid(self):
        return len(self.obs) > 0 and self.ego is not None

    def show(self):
        plt.xlim([-self.plot_size, self.plot_size])
        plt.ylim([-self.plot_size, self.plot_size])
        if self.is_valid():
            for ob in self.obs:
                ob_x = list(map(lambda p: p.x, ob.points))
                ob_y = list(map(lambda p: p.y, ob.points))
                ob_x.append(ob_x[0])
                ob_y.append(ob_y[0])
                plt.plot(ob_x, ob_y, color='r')
            for bd in self.bds:
                bd_x = list(map(lambda p: p.x, bd))
                bd_y = list(map(lambda p: p.y, bd))
                bd_x.append(bd_x[0])
                bd_y.append(bd_y[0])
                plt.scatter(bd_x, bd_y, color='b', s=10)
            ego_x = list(map(lambda p: p.x, self.ego.points))
            ego_y = list(map(lambda p: p.y, self.ego.points))
            ego_x.append(ego_x[0])
            ego_y.append(ego_y[0])
            plt.plot(ego_x, ego_y, color='g')
            #plt.show()
            plt.savefig('sample_plot.png')