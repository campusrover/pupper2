import matplotlib.pyplot as plt
class Vizualizer:
    def __init__(self):
        self.obs = []
        self.ego = None

    def set_obs(self, obs):
        self.obs = obs

    def set_ego(self, ego):
        self.ego = ego

    def is_valid(self):
        return len(self.obs) > 0 and self.ego is not None

    def show(self):
        if self.is_valid():
            for ob in self.obs:
                ob_x = list(map(lambda p: p.x, ob.points))
                ob_y = list(map(lambda p: p.y, ob.points))
                ob_x.append(ob_x[0])
                ob_y.append(ob_y[0])
                plt.plot(ob_x, ob_y, marker = 'o', color='r')
            ego_x = list(map(lambda p: p.x, self.ego.points))
            ego_y = list(map(lambda p: p.y, self.ego.points))
            ego_x.append(ego_x[0])
            ego_y.append(ego_y[0])
            plt.plot(ego_x, ego_y, marker = 'o', color='g')
            plt.show()