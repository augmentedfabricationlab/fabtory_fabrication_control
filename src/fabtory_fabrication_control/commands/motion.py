import compas_rrc as rrc
from compas.geometry import Scale

def move_to_frame(robot, frame, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    robot.abb_client.send(rrc.MoveToFrame(frame, speed, zone))

def move_to_robtarget(robot, frame, cart, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    cart = cart*scalefactor
    cart = rrc.ExternalAxes(cart)
    robot.abb_client.send(rrc.MoveToRobtarget(frame, cart, speed, zone))

def move_to_joints(robot, joints, cart, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    joints = rrc.RobotJoints(joints)
    cart = cart*scalefactor
    cart = rrc.ExternalAxes(cart)
    robot.abb_client.send(rrc.MoveToJoints(joints, cart, speed, zone))