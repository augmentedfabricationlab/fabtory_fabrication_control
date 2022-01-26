import compas_rrc as rrc
from compas.geometry import Frame, Scale



def move_to_frame(robot, plane, speed):
    #scale frame
    frame = Frame(plane.Origin/0.001, plane.XAxis, plane.YAxis)
    robot.abb_client.send(rrc.MoveToFrame(frame, speed, rrc.Zone.FINE))