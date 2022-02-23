import compas_rrc as rrc
from compas.geometry import Frame, Transformation, Scale

from compas.robots import Joint
from compas_fab.robots import Configuration



def move_to_frame(robot, frame, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    robot.abb_client.send(rrc.MoveToFrame(frame, speed, zone))


def move_to_robtarget(robot, frame, cart, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    #cart=rrc.ExternalAxes(cart*scalefactor)
    robot.abb_client.send(rrc.MoveToRobtarget(frame, cart, speed, zone))

