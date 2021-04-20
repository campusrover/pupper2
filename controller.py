import keyboard
from UDPComms import Publisher

class Controller:
	def __init__(self, port=8830, rate=20):
		self.keybinds = {
			"q": self.calibrate
		}
		
		keyboard.on_press(lambda c: self.keypress(c))
		
		self.pub = Publisher(port)
		self.rate = rate
	
	def keypress(self, c):
		if c.name in self.keybinds:
			self.keybinds[c.name]()
			
	def activate(self):
		msg = {
			"L1": 1,
			"message_rate": self.rate
		}
		self.pub.send(msg)
		
			
		
if __name__ == "__main__":
	c = Controller()
	keyboard.wait()
	
