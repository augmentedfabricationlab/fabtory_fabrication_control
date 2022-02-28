from compas.geometry import Scale
from compas.robots import Joint
import compas_rrc as rrc
import math

def move_to_frame(robot, frame, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    """
    send move to frame command to robot in m to mm conversion
    """
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    robot.abb_client.send(rrc.MoveToFrame(frame, speed, zone))

def move_to_robtarget(robot, frame, cart, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    """
    send move to robtarget command to robot in m to mm conversion
    """
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    cart = cart*scalefactor
    ext_axes = rrc.ExternalAxes([cart])
    robot.abb_client.send(rrc.MoveToRobtarget(frame, ext_axes, speed, zone))

def move_to_joints(robot, configuration, speed=250, zone=rrc.Zone.FINE, scalefactor=1000):
    """
    send move to joints command to robot in m to mm conversion
    """
    joints = [] # store joint values in degree from configuration
    for i, joint_type in enumerate(configuration.joint_types):
        if joint_type == Joint.REVOLUTE:
            joints.append(math.degrees(configuration.joint_values[i]))
    joints = rrc.RobotJoints(joints)

    cart = (configuration.joint_values[0]) # store cart values from configuration
    cart = cart*scalefactor
    cart = rrc.ExternalAxes(cart)

    robot.abb_client.send(rrc.MoveToJoints(joints, cart, speed, zone)) # send joints and cart values to robot

def move_to_joints_2(robot, configuration, speed=250, zone=rrc.Zone.FINE):
    """
    send move to joints command to robot in m to mm conversion using ExternalAxes Class from compas.rrc
    """
    ext_axes = rrc.ExternalAxes.from_configuration(configuration)

    cart = rrc.ExternalAxes(ext_axes.values[0])
    joints = rrc.RobotJoints(ext_axes.values[1:])
    
    robot.abb_client.send(rrc.MoveToJoints(joints, cart, speed, zone))