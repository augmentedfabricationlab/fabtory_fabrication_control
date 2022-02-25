import compas_rrc as rrc
from compas.geometry import Scale

def get_frame(robot, frame, scalefactor = 0.01):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    robot.abb_client.send_and_wait(rrc.GetFrame(frame))

def get_rob_target(robot, frame, cart, scalefactor=0.001):
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    cart = rrc.ExternalAxes(cart)
    robot.abb_client.send_and_wait(rrc.GetRobtarget(frame, cart))

def get_joints(robot, joints, cart):
    joints = rrc.RobotJoints(joints)
    cart = rrc.ExternalAxes(cart)
    robot. abb_client.send_and_wait(rrc.GetJoints(joints, cart))