import math
import copy
import operator

from compas.geometry import Point, Box, Frame, Vector, scale_vector, normalize_vector, Polygon, Rotation, is_point_in_polygon_xy, angle_vectors_signed

from compas.geometry import intersection_line_line_xy, distance_point_point, is_point_in_polygon_xy
from compas.geometry import distance_point_point_xy
from assembly_information_model.assembly import Element, Assembly
from compas.geometry import Translation
from AIM_TCH_forAssembly.py import floorslab_creation

layer_no = 5
gap_min = 4.0
primary_length = 320.0
secondary_length = 600.0
omnidirectional = True
primary_board_width_outside = 6.0
primary_board_height_outside = 4.0
primary_board_width_inside = 6.0
primary_board_height_inside = 4.0
primary_board_outside_dimensions = [primary_board_width_outside, primary_board_height_outside, primary_length]
primary_board_inside_dimensions = [primary_board_width_inside, primary_board_height_inside, primary_length]
secondary_board_width = 8.0
secondary_board_height = 4.0
secondary_board_dimensions = [secondary_board_width, secondary_board_height, secondary_length]

primary_interval = 12
primary_falloff = 100.0
primary_dedensification = 2
secondary_interval = 24.0
secondary_interval_development = 1.0
skip_centrals = True

primary_direction = 0
secondary_direction = 1

origin_point = Point(0, 0, 0)
origin_vector_primary = Vector(0, 1, 0)
origin_vector_secondary = Vector(1, 0, 0)
origin_frame = Frame(origin_point, origin_vector_primary, origin_vector_secondary)

Slabassembly = Assembly()
Slabassembly.layer_no = layer_no
Slabassembly.gap_min = gap_min/100
Slabassembly.primary_length = primary_length/100
Slabassembly.secondary_length = secondary_length/100
Slabassembly.omnidirectional = omnidirectional
Slabassembly.primary_board_width_outside = primary_board_width_outside/100
Slabassembly.primary_board_height_outside = primary_board_height_outside/100
Slabassembly.primary_board_width_inside = primary_board_width_inside/100
Slabassembly.primary_board_height_inside = primary_board_height_inside/100
Slabassembly.primary_board_outside_dimensions = [Slabassembly.primary_board_width_outside,
                                                 Slabassembly.primary_board_height_outside, Slabassembly.primary_length]
Slabassembly.primary_board_inside_dimensions = [Slabassembly.primary_board_width_inside,
                                                Slabassembly.primary_board_height_inside, Slabassembly.primary_length]
Slabassembly.secondary_board_width = secondary_board_width/100
Slabassembly.secondary_board_height = secondary_board_height/100
Slabassembly.secondary_board_dimensions = [Slabassembly.secondary_board_width, Slabassembly.secondary_board_height,
                                           Slabassembly.secondary_length]
Slabassembly.primary_interval = primary_interval/100
if Slabassembly.omnidirectional:
    Slabassembly.primary_falloff = primary_falloff/100
    Slabassembly.primary_dedensification = primary_dedensification
else:
    Slabassembly.primary_falloff = 0.0
    Slabassembly.primary_dedensification = 0
Slabassembly.secondary_interval = secondary_interval/100
Slabassembly.secondary_interval_development = secondary_interval_development
Slabassembly.skipping = skip_centrals
Slabassembly.primary_direction = 0
Slabassembly.secondary_direction = 1
Slabassembly.origin_fr = origin_frame
Slabassembly.origin_pt = origin_frame[0]
Slabassembly.prim_dir = origin_frame[1]
Slabassembly.sec_dir = origin_frame[2]
Slabassembly.sec_fr = Frame(Slabassembly.origin_pt, Slabassembly.sec_dir, Slabassembly.prim_dir)
Slabassembly.flip_toolframe_prim = False
Slabassembly.flip_toolframe_sec = False

Slabassembly.timberboards = []
Slabassembly.setup_done = False

Slabassembly.prim_vert_sup = True
Slabassembly.sec_vert_sup = False
Slabassembly.vert_sup_lengths = None
Slabassembly.vert_sup_gap_tolerance = 0.002
Slabassembly.vert_sup_gap_min = 0.005

# ADVANCED PARAMETERS
Slabassembly.vertical_support_width = 12.0/100
Slabassembly.vertical_support_interlock = 10.0/100
Slabassembly.gluepathwidth = .3/100
Slabassembly.advanced_setup = False

advanced_floorslab_setup(Slabassembly, 0.0, 0.0)
floorslab_creation(Slabassembly)
gluepoints(Slabassembly)
weight_calculator(Slabassembly, protective_clay_height=5.0, fill_limit=1, density_clay=1900)


myboard = Slabassembly.network.node[1]
mine = myboard["element"].box

print("hello")
# secondary_span_interval_development: 1 = constant, <1: denser in the centre, >1: denser on the edges
# operable range approximately 0.6/6
