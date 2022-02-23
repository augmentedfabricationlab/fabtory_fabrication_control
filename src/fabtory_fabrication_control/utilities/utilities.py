from compas.geometry import Frame, Scale
from compas_ghpython import draw_frame
from compas_ghpython.artists import FrameArtist

def plane_to_frame(plane):
    frame = Frame(plane.Origin, plane.XAxis, plane.YAxis)
    return frame


def frame_to_plane(frame):
    plane = FrameArtist(frame).draw()
    return plane
