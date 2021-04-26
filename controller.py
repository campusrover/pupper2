import keyboard
from UDPComms import Publisher

# Manual controls are:
# "space": (de)activate robot
# "w/s/q/e": walk forward/backward/left/right
# "a/d": yaw left/right
# For calibration see the original documentation: https://github.com/stanfordroboticsclub/StanfordQuadruped/tree/dji
class Controller:
    def __init__(self, port=8830, rate=20):
        self.keybinds = {
            "space": self.toggle,
            "w": self.move_forward,
            "a": self.rotate_left,
            "s": self.move_backward,
            "d": self.rotate_right,
            "q": self.move_left,
            "e": self.move_right,
            "v": self.trot
        }

        keyboard.on_press(lambda c: self.keypress(c))

        self.velocity = 10 # Needs tuning
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
        
        print("Controller initialized")
    
    def keypress(self, c):
        print("Key pressed: ", c.name)
        if c.name in self.keybinds:
            self.keybinds[c.name]()
    
    def move(self, lx=0.0, ly=0.0, yaw=0.0):
        msg = self.blank_msg.copy()
        msg["lx"] = lx
        msg["ly"] = ly
        msg["rx"] = yaw

        print(msg)
        self.pub.send(msg)
    
    def move_forward(self, yaw=0.0):
        self.move(ly=self.velocity, yaw=yaw)

    def move_backward(self, yaw=0.0):
        self.move(ly=self.velocity, yaw=yaw)

    # Move/rotate left/right might be reversed
    def move_left(self):
        self.move(lx=self.velocity)
    
    def move_right(self):
        self.move(lx=-self.velocity)

    def rotate_right(self):
        self.move(yaw=self.velocity)

    def rotate_left(self):
        self.move(yaw=-self.velocity)
    
    def toggle(self, state=1):
        msg = self.blank_msg.copy()
        msg["L1"] = state
        self.pub.send(msg)
        
    def trot(self):
        msg = self.blank_msg.copy()
        msg["R1"] = 1
        self.pub.send(msg)
            
        
if __name__ == "__main__":
    c = Controller()
    keyboard.wait()
    

