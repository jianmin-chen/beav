from pymavlink import mavutil
import turtle


class Beaver:
    def addmethod(self, name, ref):
        setattr(self, name, ref)


class AUV(Beaver):
    """
    Simulate with QGroundControl -> actual AUV.
    """

    def __init__(self) -> None:
        super().__init__()
        self.mav_connection = mavutil.mavlink_connection("udpin:0.0.0.0:14550")

    def forward(self, dist):
        pass

    def backward(self, dist):
        pass

    def right(self, angle):
        pass

    def left(self, angle):
        pass


class Turtle(Beaver):
    """
    Simulate with Python turtle.
    """

    def __init__(self):
        super().__init__()

    def forward(self, dist):
        turtle.forward(dist)

    def backward(self, dist):
        turtle.backward(dist)

    def right(self, angle):
        turtle.right(angle)

    def left(self, angle):
        turtle.left(angle)
