import compas_rrc as rrc
from compas.geometry import Frame


def getframe(frame):
    #frame = Frame(plane.Origin/scalefactor, plane.XAxis, plane.YAxis)
    frame = rrc.GetFrame()
    return frame



