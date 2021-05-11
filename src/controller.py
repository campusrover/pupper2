from UDPComms import Publisher
import keyboard

# Manual controls are:
# "space": Toggle between trot/rest
# "v": (de)activate robot
# "w/s/q/e": walk forward/backward/left/right
# "a/d": yaw left/right
# "x" stop walking
# For calibration, see the original documentation:  https://github.com/stanfordroboticsclub/StanfordQuadruped/tree/dji
class Controller:
    def __init__(self, port=8830, rate=20):
        self.keybinds = {
            "space": self.toggle_trot,
            "v": self.activate,
            "w": self.move_forward,
            "a": self.rotate_left,
            "s": self.move_backward,
            "d": self.rotate_right,
            "q": self.move_left,
            "e": self.move_right,
            "x": self.move
        }

        self.velocity = 1 # Needs tuning
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.l_alpha = 0.15
        self.r_alpha = 0.3

        self.pub = Publisher(port)
        self.rate = rate
        self.blank_msg = {
            "ly": 0,
            "lx": 0,
            "rx": 0,
            "ry": 0,
            "L2": 0,
            "R2": 0,
            "R1": 0,
            "L1": 0,
            "dpady": 0,
            "dpadx": 0,
            "x": 0,
            "square": 0,
            "circle": 0,
            "triangle": 0,
            "message_rate": self.rate,
        }

        keyboard.on_press(lambda c: self.keypress(c))

        print("Controller initialized")
    
    def keypress(self, c):
        print("Key pressed: ", c.name)
        if c.name in self.keybinds:
            self.keybinds[c.name]()

    def move(self, lx=0.0, ly=0.0, yaw=0.0):
        msg = self.blank_msg.copy()
        self.lx = self.l_alpha * lx + (1 - self.l_alpha) * self.lx
        msg["lx"] = self.lx

        self.ly = self.l_alpha * ly + (1 - self.l_alpha) * self.ly
        msg["ly"] = self.ly

        self.rx = self.r_alpha * yaw + (1 - self.r_alpha) * self.rx
        msg["rx"] = self.rx

        print(msg)
        self.pub.send(msg)

    def move_forward(self, yaw=0.0):
        self.move(ly=self.velocity, yaw=yaw)

    def move_backward(self, yaw=0.0):
        self.move(ly=-self.velocity, yaw=yaw)

    # Move/rotate left/right might be reversed
    def move_left(self):
        self.move(lx=-self.velocity)
    
    def move_right(self):
        self.move(lx=self.velocity)

    def rotate_right(self):
        self.move(yaw=self.velocity)

    def rotate_left(self):
        self.move(yaw=-self.velocity)

    def activate(self):
        msg = self.blank_msg.copy()
        msg["L1"] = 1
        self.pub.send(msg)
        
    def toggle_trot(self):
        msg = self.blank_msg.copy()
        msg["R1"] = 1
        self.pub.send(msg)

if __name__ == "__main__":
    c = Controller()
    keyboard.wait()

