from UDPComms import Publisher
from time import sleep
import keyboard

def direction_helper(opt1, opt2):
    return -1 if opt1 else 1 if opt2 else 0

def key(k):
    return keyboard.is_pressed(k)

if __name__ == "__main__":
    pub = Publisher(8830)

    MESSAGE_RATE = 20

    rx_ = 0.0
    ry_ = 0.0
    lx_ = 0.0
    ly_ = 0.0
    l_alpha = 0.15
    r_alpha = 0.3

    while True:
        msg = {}
        lx_ = l_alpha * direction_helper(key("a"),key("d")) + (1 - l_alpha) * lx_
        msg["lx"] = lx_
        ly_ = l_alpha * direction_helper(key("s"), key("w")) + (1 - l_alpha) * ly_
        msg["ly"] = ly_
        rx_ = r_alpha * direction_helper(key(105),key(106)) + (1-r_alpha)*rx_
        msg["rx"] = rx_
        ry_ = r_alpha * direction_helper(key(108),key(103)) + (1-r_alpha)*ry_
        msg["ry"] = ry_
        msg["x"] = 1 if key("x") else 0
        msg["square"] = 1 if key("u") else 0
        msg["circle"] = 1 if key("c") else 0
        msg["triangle"] = 1 if key("t") else 0
        msg["dpady"] = 1.0 * direction_helper(key("k"),key("i"))
        msg["dpadx"] = 1.0 * direction_helper(key("j"),key("l"))
        msg["L1"] = 1 if key("q") else 0
        msg["R1"] = 1 if key("e") else 0
        msg["L2"] = 0
        msg["R2"] = 0
        msg["message_rate"] = MESSAGE_RATE
        print(msg)

        pub.send(msg)
        sleep((1000/MESSAGE_RATE)/1000)

