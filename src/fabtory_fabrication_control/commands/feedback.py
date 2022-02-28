import compas_rrc as rrc
from compas.geometry import Scale
import math


def get_frame(robot, scalefactor=0.001):
    frame = robot.abb_client.send_and_wait(rrc.GetFrame())
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    return (frame)

def get_rob_target(robot, scalefactor=0.001):
    frame, external_axes = robot.abb_client.send_and_wait(rrc.GetRobTarget())
    return (frame, external_axes)

def get_joints(robot, scalefactor=0.001):
    joints, external_axes = robot.abb_client.send_and_wait(rrc.GetJoints())

    joints = rrc.RobotJoints(joints.values[1:])
    joints.append(math.degrees(joints))

    cart = rrc.ExternalAxes(external_axes.values[0]) #store cart value in m
    cart = cart*scalefactor

    rrc.ExternalAxes.to_configuration(cart, joints)
    return (configuration)

#def get_configuration(robot, scalefactor=0.001):
