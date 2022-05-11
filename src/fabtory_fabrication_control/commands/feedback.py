import compas_rrc as rrc
from compas.geometry import Scale

__all__ = ["get_frame",
           "get_robtarget",
           "get_joints"]


def get_frame(robot, scalefactor=0.001):
    """
    send get frame command to receive robot's frame in mm to m conversation
    """
    frame = robot.abb_client.send_and_wait(rrc.GetFrame())
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    return (frame)


def get_robtarget(robot, scalefactor=0.001):
    """
    send get robtarget command to receive robot's frame and external axes,
    converted from mm to m
    """
    frame, external_axes = robot.abb_client.send_and_wait(rrc.GetRobtarget())
    # Scale robot frame from mm in m
    S = Scale.from_factors([scalefactor] * 3)
    frame.transform(S)
    # Store robot cart value in mm to m conversion
    cart = rrc.ExternalAxes(external_axes.values[0]*scalefactor)
    return (frame, cart)


def get_joints(robot):
    """
    send get joints command to receive robot's joint configuration
    """
    joints, external_axes = robot.abb_client.send_and_wait(rrc.GetJoints())
    ext_val = external_axes.values + joints.values
    axes = rrc.ExternalAxes(ext_val)
    configuration = axes.to_configuration(robot)
    return (configuration)
