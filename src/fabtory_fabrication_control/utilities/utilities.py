from compas.geometry import Frame, Scale
import Rhino.Geometry as rg

def plane_to_frame(plane, scalefactor=0.001):
    frame = Frame(plane.Origin/scalefactor, plane.XAxis, plane.YAxis)
    return frame

def frame_to_plane(frame, scalefactor=1000):
    #pass
