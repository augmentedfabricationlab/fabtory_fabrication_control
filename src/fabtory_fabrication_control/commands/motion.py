from compas.geometry import Scale
from compas.robots import Joint
import compas_rrc as rrc
import math

__all__ = ["move_to_frame",
           "move_to_robtarget",
           "move_to_joints",
           "move_to_joints_2"]


def move_to_frame(robot, frame, speed=250, zone=rrc.Zone.FINE,
                  scalefactor=1000, feedback_level=0, send_and_wait=False):
    """
    send move to frame command to robot in m to mm conversion
    """
    # Scale frame from m to mm
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    if send_and_wait:
        # Send command to robot
        return robot.abb_client.send_and_wait(rrc.MoveToFrame(frame, speed, zone, feedback_level=feedback_level))
    else:
        # Send command to robot
        return robot.abb_client.send(rrc.MoveToFrame(frame, speed, zone, feedback_level=feedback_level))


def move_to_robtarget(robot, frame, cart, speed=250, zone=rrc.Zone.FINE,
                      scalefactor=1000, feedback_level=0, send_and_wait=False):
    """
    send move to robtarget command to robot in m to mm conversion
    """
    # Scale frame from m to mm
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    # Scale cart
    cart = cart*scalefactor
    ext_axes = rrc.ExternalAxes([cart])
    if send_and_wait:
        # Send command to robot
        return robot.abb_client.send_and_wait(rrc.MoveToRobtarget(frame, ext_axes, speed, zone, feedback_level=feedback_level))
    else:
        # Send command to robot
        return robot.abb_client.send(rrc.MoveToRobtarget(frame, ext_axes, speed, zone, feedback_level=feedback_level))


def move_to_joints(robot, configuration, speed=250, zone=rrc.Zone.FINE,
                   scalefactor=1000, feedback_level=0, send_and_wait=False):
    """
    send move to joints command to robot in m to mm conversion
    """
    # Store joint values in degree from configuration
    joints = []
    for i, joint_type in enumerate(configuration.joint_types):
        if joint_type == Joint.REVOLUTE:
            joints.append(math.degrees(configuration.joint_values[i]))
    joints = rrc.RobotJoints(joints)
    # Store cart values from configuration in m
    cart = (configuration.joint_values[0])
    # Scale cart value in mm
    cart = cart*scalefactor
    cart = rrc.ExternalAxes(cart)
    if send_and_wait:
        # Send joints and cart values to robot
        return robot.abb_client.send_and_wait(rrc.MoveToJoints(joints, cart, speed, zone, feedback_level=feedback_level))
    else:
        # Send joints and cart values to robot
        return robot.abb_client.send(rrc.MoveToJoints(joints, cart, speed, zone, feedback_level=feedback_level))


def move_to_joints_2(robot, configuration, speed=250, zone=rrc.Zone.FINE,
                     send_and_wait=False):
    """
    send move to joints command to robot in m to mm conversion using
    the ExternalAxes Class from compas.rrc
    """
    # Store all robot values from configuration
    ext_axes = rrc.ExternalAxes.from_configuration(configuration)
    # Store cart values from robot values
    cart = rrc.ExternalAxes(ext_axes.values[0])
    # Store joint values from robot values
    joints = rrc.RobotJoints(ext_axes.values[1:])
    if send_and_wait:
        # Send move to joints command
        return robot.abb_client.send_and_wait(rrc.MoveToJoints(joints, cart,
                                                        speed, zone))
    else:
        # Send move to joints command
        return robot.abb_client.send(rrc.MoveToJoints(joints, cart, speed, zone))
