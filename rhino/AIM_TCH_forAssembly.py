import math
import copy
import operator

from compas.geometry import Point, Box, Frame, Vector, scale_vector, normalize_vector, Polygon, Rotation, is_point_in_polygon_xy, angle_vectors_signed

from compas.geometry import intersection_line_line_xy, distance_point_point, is_point_in_polygon_xy
from compas.geometry import distance_point_point_xy
from assembly_information_model.assembly import Element, Assembly
from compas.geometry import Translation


# default setup that collects the relevant functions
def floorslab_creation(self):
    # calculates the basic centre lines
    # basically just a list of numbers, the rest comes later
    def __grid_creation():
        # in case the timber boards on the inside are the same size as usual
        if self.primary_board_height_inside < 0 or self.primary_board_width_inside < 0:
            primary_span_board_width_inside = self.primary_board_width_outside
            self.primary_board_height_inside = self.primary_board_height_outside

        # check for minimal distance
        # -.1 in order to be on the safe side
        self.gap_min -= .1
        if self.primary_board_height_outside < self.gap_min or self.primary_board_height_inside < self.gap_min or \
            (self.primary_interval - self.primary_board_width_outside) < self.gap_min or \
            (self.primary_interval - self.primary_board_width_inside) < self.gap_min:
            print("Too little gap")
            return 1

        # side_dedensification_intensity = how many elements do we kick out
        self.primary_dedensification *= 1000.0

        # define the room
        centre_ratio = (self.secondary_length - self.primary_falloff * 2) / self.secondary_length

        primary_graph_centre_line_x = self.secondary_length / 2

        # go into the borders
        # 1000 just so that we get nicer numbers
        primary_graph_default_ascent = 1000.0 / self.primary_interval
        primary_graph_centre_line_y = (primary_graph_centre_line_x // self.primary_interval) * 1000.0 - self.primary_dedensification
        primary_graph_centre_minimum_x = primary_graph_centre_line_x - centre_ratio * primary_graph_centre_line_x

        # adjust the centre ratio in a way the endpoints fit perfectly
        # not sure what this was supposed to do precisely, didn't work in this instance
        inacc = (primary_graph_centre_line_x - primary_graph_centre_minimum_x) % self.primary_interval
        target = primary_graph_centre_minimum_x + inacc

        centre_ratio = (target - primary_graph_centre_line_x) / -primary_graph_centre_line_x

        # now start from scratch now with a different ratio
        primary_graph_centre_minimum_x = primary_graph_centre_line_x - centre_ratio * primary_graph_centre_line_x
        primary_graph_centre_maximum_x = primary_graph_centre_line_x + centre_ratio * primary_graph_centre_line_x

        # +.1 is a bit of a dirty fix against float inaccuracies
        no_elements = ((primary_graph_centre_line_x - primary_graph_centre_minimum_x) + 0.001) // self.primary_interval

        primary_graph_centre_minimum_y = primary_graph_centre_line_y - 1000.0 * no_elements
        primary_graph_centre_maximum_y = primary_graph_centre_line_y + 1000.0 * no_elements
        secondary_graph_y_maximum = primary_graph_centre_line_y * 2.0

        # math function for later
        falloff_calculation_factor = 2.0
        b = -1
        g = primary_graph_centre_minimum_x * 1.0
        d = primary_graph_centre_minimum_y
        s = primary_graph_default_ascent

        # loop is necessary because of the different falloff setups; without it, there are sometimes no boards on the ends
        if self.primary_dedensification > 1:
            while b < 0:
                b = (falloff_calculation_factor * d) / g - s
                falloff_calculation_factor += 0.05
        else:
            b = (falloff_calculation_factor * d) / g - s
        a = (s - b) / (falloff_calculation_factor * g)

        primary_span_grid = [[], []]

        def graph_function(y):
            # in central part
            if y >= primary_graph_centre_minimum_y and y <= primary_graph_centre_maximum_y:
                x_value = primary_graph_centre_minimum_x + self.primary_interval * (y - primary_graph_centre_minimum_y) / 1000
                return x_value
            # error
            elif y > primary_graph_centre_line_y * 2 or y < 0:
                return 2
            # on the one hand; recalls the own function in a mirrored way and executes the last part of the function
            elif y > primary_graph_centre_maximum_y:
                # mirror everything to be on the safe side
                y = secondary_graph_y_maximum - y
                x_value = graph_function(y)
                return self.secondary_length - x_value
            # it's outside the centre: do the differential
            else:
                # unexplainable math function; derived from differential
                x_value = ((b * -1) + math.sqrt(b ** 2 - 4 * a * (-y))) / (2 * a)
                if x_value < 1:
                    x_value = self.primary_board_width_outside / 2
                return x_value


        # now we create the primary span grid
        # +1 is an inelegant solution that makes sure the highest element is still respected
        for i in range(0, int(secondary_graph_y_maximum) + 1, 1000):
            # omnidirectional case
            if self.primary_dedensification > 0:
                result = graph_function(i)
                if result == 2:
                    break
            # monodirectional case
            else:
                result = self.primary_board_width_outside / 2 + (i / 1000) * self.primary_interval
            primary_span_grid[0].append(result)

        # dirty solution because otherwise the last board would have been skipped
        if self.primary_dedensification == 0:
            primary_span_grid[0].append(self.secondary_length - self.primary_board_width_outside / 2)
        # another little dirty fix because the last board isn't always skipped by default and then we have one too many
        if abs(primary_span_grid[0][-1] - primary_span_grid[0][-2]) < self.primary_board_width_outside:
            primary_span_grid[0].pop(-2)

        # now create also the alternative lines in the gaps of the grid
        if self.primary_dedensification > 0:
            for i in range(500, int(secondary_graph_y_maximum) + 1, 1000):
                result = graph_function(i)
                if result == 2:
                    break
                else:
                    primary_span_grid[1].append(result)
        else:
            for i in range(len(primary_span_grid[0])-1):
                new_entry = (primary_span_grid[0][i] + primary_span_grid[0][i+1]) / 2
                primary_span_grid[1].append(new_entry)

        # now a safety thing to make sure that there is a position at the ends
        if primary_span_grid[0][0] > self.primary_board_width_outside / 1.9:
            print("Warning: No board on the sides")

        ############################################################
        ############################################################
        ############################################################
        # now comes the long span
        secondary_span_centre = self.primary_length // 2

        # helps to determine the graph function
        def longspan_function(val, searched):
            if searched == "y":
                return val ** self.secondary_interval_development
            if searched == "x":
                value = val ** (1 / self.secondary_interval_development)
                return value

        no_secondary_span_elements = self.primary_length // self.secondary_interval
        # determine the steps
        secondary_graph_y_max = longspan_function(secondary_span_centre, "y")
        secondary_graph_y_min = secondary_graph_y_max * -1
        secondary_graph_y_step = secondary_graph_y_max / ((no_secondary_span_elements - 1) / 2)

        # go through the function to get the final values
        secondary_graph_y_current = 0
        secondary_graph_y_list_positive = []
        secondary_graph_y_list_final = []
        while secondary_graph_y_current <= secondary_graph_y_max + 1:
            # function only works for positive values!
            secondary_graph_y_list_positive.append(longspan_function(secondary_graph_y_current, "x"))
            secondary_graph_y_current += secondary_graph_y_step

        # now create a negative list
        for i in range(len(secondary_graph_y_list_positive) - 1, 0, -1):
            secondary_graph_y_list_final.append(secondary_graph_y_list_positive[i] * -1)
        # and now fuse them
        secondary_graph_y_list_final += secondary_graph_y_list_positive
        # and now push it by half the room width
        for val in range(len(secondary_graph_y_list_final)):
            secondary_graph_y_list_final[val] += self.primary_length / 2

        secondary_span_grid = [[], [], []]

        for element in range(1, len(secondary_graph_y_list_final) - 1, 2):
            secondary_span_grid[0].append(secondary_graph_y_list_final[element])
            secondary_span_grid[1].append(secondary_graph_y_list_final[element])
        for element in range(2, len(secondary_graph_y_list_final) - 1, 2):
            secondary_span_grid[0].append(secondary_graph_y_list_final[element])
            secondary_span_grid[2].append(secondary_graph_y_list_final[element])
        for j in range(len(secondary_span_grid)):
            secondary_span_grid[j].insert(0, self.secondary_board_width / 2)
            secondary_span_grid[j].append(self.primary_length - self.secondary_board_width / 2)

        secondary_span_grid[0].sort()
        return primary_span_grid, secondary_span_grid

    # adapts the advanced boards to meaningful lengths
    def __advanced_length_correction():
        # inside shear supports
        if self.primary_inside_support_length > 0.0:
            position = 0
            while self.primary_inside_support_length > self.floorslab_grids[1][0][position]:
                position += 1
            # //1 just to get a nicer number
            self.primary_inside_support_length = ((self.floorslab_grids[1][0][position] + self.secondary_board_width / 2)
                                                  + self.secondary_board_width/2) // 1
            self.primary_inside_support_dimensions[2] = self.primary_inside_support_length

        # outside momentum supports
        if self.primary_outside_support_length > 0.0:
            outside_grid = self.floorslab_grids[1][0]
            outside_centre_id = len(outside_grid) // 2
            position = 1
            while outside_grid[outside_centre_id + position] - outside_grid[outside_centre_id - position] < self.primary_outside_support_length:
                position += 1
            # //1 just to get a nicer number
            self.primary_outside_support_length = ((outside_grid[outside_centre_id + position] - outside_grid[outside_centre_id - position]) +
                                                   self.secondary_board_width) // 1 + .01
            self.primary_outside_support_dimensions[2] = self.primary_outside_support_length

    # makes sure that the program doesn't crash when the user/algorithm enters some nonsense
    def input_check():
        input_validity = True
        # check for too much dedensification
        if self.primary_dedensification > 0:
            if self.primary_falloff / self.primary_interval - self.primary_dedensification < 1:
                input_validity = False
                print("Too much dedensification")

        # check whether the interval is realistic
        if self.primary_dedensification == 0:
            interval_intolerance = (self.secondary_length - self.primary_board_width_outside) % self.primary_interval
            no_intervals = (self.secondary_length - self.primary_board_width_outside) // self.primary_interval
            if interval_intolerance > 0.1:
                interval_intolerance /= no_intervals
                self.primary_interval += interval_intolerance
        return input_validity

    def vert_sup_setup(prim_board_sup=False, sec_board_sup=False, available_lengths=None, gap_tolerance=0.2, vert_gap_min=5.0):
        self.prim_vert_sup = prim_board_sup
        self.sec_vert_sup = sec_board_sup
        self.vert_sup_lengths = available_lengths
        self.vert_sup_gap_tolerance = gap_tolerance
        self.vert_sup_gap_min = vert_gap_min

    # to do the sorting
    def __lt__(self, other):
        return self.grid_position < other.grid_position

    # creates the timber board instances and equips them with dimensions and z-location
    # momentum support pieces missing now
    def __board_data_setup(advanced):
        def element_data_creator(dims, lay, global_c, layer_c, z, len_dir, w_dir, grid_pos, vert_support, perpendicular=False, loc="centre"):
            myElement = Element.from_dimensions(dims[2], dims[0], dims[1])
            myElement.layer = lay
            myElement.global_count = global_c
            myElement.no_in_layer = layer_c
            myElement.z_drop = z
            myElement.length_direction = len_dir
            myElement.width_direction = w_dir
            myElement.grid_position = grid_pos
            myElement.location = loc
            myElement.width = dims[0]
            myElement.height = dims[1]
            myElement.length = dims[2]
            myElement.perp = perpendicular
            myElement.vert_sup = vert_support
            myElement.glue_givers = []
            myElement.glue_receivers = []
            myElement.glue_surfaces = []
            myElement.glue_paths = []
            myElement.receiving_neighbours = []
            myElement.giving_neighbours = []
            myElement.stack_index = None
            myElement.stack_pick_frame = None
            myElement.stack_center_frame = None
            self.add_element(myElement)

            # very wide pieces that both carry vertical load and connect to the other boards
            if myElement.vert_sup and not myElement.perp:
                if layer_c == 0:
                    myElement.grid_position -= myElement.width/2
                    myElement.grid_position += (self.vertical_support_interlock - self.vertical_support_width)/2
                else:
                    myElement.grid_position += myElement.width/2
                    myElement.grid_position -= (self.vertical_support_interlock - self.vertical_support_width)/2
                myElement.width = self.vertical_support_interlock + self.vertical_support_width
                if self.prim_vert_sup and self.sec_vert_sup:
                    myElement.length += self.vertical_support_width*2

            # not so wide pieces that only carry vertical load
            elif myElement.perp:
                if self.prim_vert_sup and self.sec_vert_sup:
                    myElement.length -= self.vertical_support_interlock * 2
                myElement.width = self.vertical_support_width

        z_value = 0
        global_counter = 0
        for layer in range(self.layer_no):
            layer_counter = 0
            # outside layer, primary_span
            if layer == 0 or (layer == self.layer_no - 1 and layer % 2 == 0):
                boardheight = self.primary_board_height_outside
                z_value += boardheight
                # main part
                for i in range(len(self.floorslab_grids[0][0])):
                    if self.sec_vert_sup and (i == 0 or i == len(self.floorslab_grids[0][0])-1):
                        vert_sup = True
                    else:
                        vert_sup = False

                    board_position = self.floorslab_grids[0][0][i]
                    element_data_creator(self.primary_board_outside_dimensions, layer, global_counter, layer_counter, z_value,
                                         self.primary_direction, self.secondary_direction, board_position, vert_sup)

                    global_counter += 1
                    layer_counter += 1

                # inserts the momentum support pieces if it's wished
                last_piece = self.network.node[global_counter-1]["element"]
                last_grid_pos = last_piece.grid_position
                last_layer_pos = last_piece.no_in_layer

                if self.advanced_setup and self.primary_outside_support_length > 0:
                    for i in range(global_counter - 1, global_counter - last_layer_pos - 1, -1):
                        current_layer_counter = self.network.node[i]["element"].no_in_layer - 1
                        # check for the layer
                        if (self.network.node[i]["element"].grid_position - self.network.node[i - 1]["element"].grid_position >
                            self.primary_outside_support_gap_min and
                            (self.network.node[i]["element"].grid_position - self.network.node[i - 1]["element"].grid_position) / 2 -
                            self.primary_board_width_outside > self.gap_min and
                            self.floorslab_grids[0][1][current_layer_counter] > self.primary_outside_support_distance_to_edge_min and
                            self.secondary_length - self.floorslab_grids[0][1][current_layer_counter] > self.primary_outside_support_distance_to_edge_min and
                            self.floorslab_grids[0][1][current_layer_counter] < self.primary_outside_support_distance_to_edge_max and
                            self.secondary_length - self.floorslab_grids[0][1][current_layer_counter] < self.primary_outside_support_distance_to_edge_max and
                            (last_piece.layer in self.primary_outside_support_layers or self.primary_outside_support_layers == [])
                        ):
                            dims = [self.primary_board_outside_dimensions[0], self.primary_board_outside_dimensions[1],
                                    self.primary_outside_support_length]
                            element_data_creator(dims, layer, global_counter, layer_counter, z_value,
                                                 self.primary_direction, self.secondary_direction, self.floorslab_grids[0][1][current_layer_counter], False)

                            global_counter += 1
                            layer_counter += 1

                if self.prim_vert_sup:
                    dims = [self.primary_board_outside_dimensions[0], self.primary_board_outside_dimensions[1],
                            self.secondary_board_dimensions[2]]

                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.primary_direction, self.secondary_direction,
                                         self.secondary_length/2, True, True, "low")
                    global_counter += 1
                    layer_counter += 1
                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.primary_direction, self.secondary_direction,
                                         self.secondary_length/2, True, True, "high")
                    global_counter += 1
                    layer_counter += 1

            # inside layer, primary span
            elif layer % 2 == 0:
                boardheight = self.primary_board_height_inside
                z_value += boardheight
                # no dedensification on the inside
                if not self.skipping:
                    for i in range(len(self.floorslab_grids[0][0])):
                        if self.sec_vert_sup and (i == 0 or i == len(self.floorslab_grids[0][0]) - 1):
                            vert_sup = True
                        else:
                            vert_sup = False

                        element_data_creator(self.primary_board_inside_dimensions, layer, global_counter, i, z_value,
                                             self.primary_direction, self.secondary_direction,
                                             self.floorslab_grids[0][0][i], vert_sup)
                        global_counter += 1

                # dedensification on the inside
                else:
                    # not sure about the -1
                    for i in range(0, len(self.floorslab_grids[0][0]), 2):
                        if self.sec_vert_sup and (i == 0 or i == len(self.floorslab_grids[0][0])-1):
                            vert_sup = True
                        else:
                            vert_sup = False
                        element_data_creator(self.primary_board_inside_dimensions, layer, global_counter, layer_counter,
                                            z_value, self.primary_direction, self.secondary_direction,
                                            self.floorslab_grids[0][0][i], vert_sup)
                        global_counter += 1
                        layer_counter += 1

                    # last element??
                    if len(self.floorslab_grids[0][0]) % 2 != 1:
                        if self.sec_vert_sup:
                            vert_sup = True
                        else:
                            vert_sup = False
                        element_data_creator(self.primary_board_inside_dimensions, layer, global_counter, layer_counter,
                                             z_value, self.primary_direction, self.secondary_direction,
                                             self.floorslab_grids[0][0][-1], vert_sup)

                        global_counter += 1
                        layer_counter += 1

                    # inserts the shear support pieces if wished
                    if self.advanced_setup and self.primary_inside_support_length > 0 and self.skipping:
                        iteration_counter = 0
                        fixed_global_counter = global_counter
                        for i in range(len(self.floorslab_grids[0][0]) - 1, 1, -2):
                            iteration_counter += 1
                            current_layer_counter = self.network.node[i]["element"].no_in_layer - 1
                            # now check whether there should really be a board at that position
                            upper_element = self.network.node[fixed_global_counter - iteration_counter]["element"]
                            lower_element = self.network.node[fixed_global_counter - iteration_counter - 1]["element"]
                            if (upper_element.grid_position - lower_element.grid_position > self.primary_inside_support_gap_min and

                                self.floorslab_grids[0][0][i] > self.primary_inside_support_distance_to_edge_min and
                                self.secondary_length - self.floorslab_grids[0][0][i] > self.primary_inside_support_distance_to_edge_min and
                                self.floorslab_grids[0][0][i] < self.primary_inside_support_distance_to_edge_max and
                                self.secondary_length - self.floorslab_grids[0][0][i] < self.primary_inside_support_distance_to_edge_max and
                                (self.primary_inside_support_layers == [] or layer in self.primary_inside_support_layers)):

                                dims = [self.primary_board_inside_dimensions[0], self.primary_board_inside_dimensions[1],
                                        self.primary_inside_support_length]

                                element_data_creator(dims, layer, global_counter, layer_counter, z_value,
                                                     self.primary_direction, self.secondary_direction,
                                                     self.floorslab_grids[0][0][current_layer_counter], False, loc="low")
                                layer_counter += 1
                                global_counter += 1

                                element_data_creator(dims, layer, global_counter, layer_counter, z_value,
                                                     self.primary_direction, self.secondary_direction,
                                                     self.floorslab_grids[0][0][current_layer_counter], False, loc="high")
                                global_counter += 1
                                layer_counter += 1
                            else:
                                continue

                if self.prim_vert_sup:
                    dims = [self.primary_board_inside_dimensions[0], self.primary_board_inside_dimensions[1],
                            self.secondary_board_dimensions[2]]

                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.primary_direction, self.secondary_direction,
                                         self.secondary_length / 2, True, True, "low")
                    global_counter += 1
                    layer_counter += 1
                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.primary_direction, self.secondary_direction,
                                         self.secondary_length / 2, True, True, "high")
                    global_counter += 1
                    layer_counter += 1



            # secondary span
            else:
                boardheight = self.secondary_board_height
                z_value += boardheight
                x = len(self.floorslab_grids[1][0])
                for i in range(0, len(self.floorslab_grids[1][0])):
                    if self.prim_vert_sup and (i == 0 or i == len(self.floorslab_grids[1][0])-1):
                        vert_sup = True
                    else:
                        vert_sup = False

                    element_data_creator(self.secondary_board_dimensions, layer, global_counter, layer_counter,
                                         z_value, self.secondary_direction, self.primary_direction,
                                         self.floorslab_grids[1][0][i], vert_sup)

                    global_counter += 1
                    layer_counter += 1

                if self.sec_vert_sup:
                    dims = [self.secondary_board_dimensions[0], self.secondary_board_dimensions[1],
                            self.primary_board_outside_dimensions[2]]

                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.secondary_direction, self.primary_direction,
                                         self.primary_length/2, True, True, "low")
                    global_counter += 1
                    layer_counter += 1
                    element_data_creator(dims, layer, global_counter, layer_counter,
                                         z_value, self.secondary_direction, self.primary_direction,
                                         self.primary_length/2, True, True, "high")
                    global_counter += 1
                    layer_counter += 1

    # the actual geometry setup
    def board_geometry_setup():
        for my_element in self.elements():
            my_board = my_element[1]
            if my_board.layer % 2 == 0:
                my_frame = self.origin_fr
                layer_standard_length = self.primary_length
            else:
                my_frame = self.sec_fr
                layer_standard_length = self.secondary_length

            my_dir1 = normalize_vector(my_frame[1])
            my_dir2 = normalize_vector(my_frame[2])
            dist = my_board.grid_position

            if my_board.location == "high":
                if not my_board.perp:
                    length_attribute_1 = layer_standard_length - my_board.length / 2
                else:
                    length_attribute_1 = layer_standard_length + my_board.width / 2
            elif my_board.location == "low":
                if not my_board.perp:
                    length_attribute_1 = my_board.length / 2
                else:
                    length_attribute_1 = -my_board.width / 2
            else:
                length_attribute_1 = layer_standard_length / 2

            # position parallel to the boards (if not sup)
            my_vec1 = scale_vector(my_dir1, length_attribute_1)
            # position perpendicular to board direction (if not sup)
            my_vec2 = scale_vector(my_dir2, dist)
            # height vector
            my_vec3 = Vector(0, 0, my_board.z_drop - my_board.height / 2)
            my_centre = self.origin_pt + my_vec1 + my_vec2 + my_vec3
            my_board.centre_point = my_centre

            my_board.drop_point = my_centre + Vector(0, 0, my_board.height / 2)
            """
            OLD SOLUTION: PROBABLY UNNECESSARILY COMPLICATED + CREATED ISSUES; KEPT JUST IN CASE THE NEWER ONE SHOULD TURN OUT DYSFUNCTIONAL
            if not my_board.perp:
                my_board.length_vector = normalize_vector(my_vec1)
                my_board.width_vector = normalize_vector(my_vec2)
            else:
                my_board.length_vector = normalize_vector(my_vec2)
                my_board.width_vector = normalize_vector(my_vec1)"""

            if not my_board.perp:
                my_board.length_vector = Vector(my_dir1[0], my_dir1[1], my_dir1[2])
                my_board.width_vector = Vector(my_dir2[0], my_dir2[1], my_dir2[2])
            else:
                my_board.length_vector = Vector(my_dir2[0], my_dir2[1], my_dir2[2])
                my_board.width_vector = Vector(my_dir1[0], my_dir1[1], my_dir1[2])

            old_centre = Point(my_board.center[0], my_board.center[1], my_board.center[2])
            my_vec = Vector.from_start_end(old_centre, my_centre)
            T = Translation.from_vector(my_vec)
            self.network.node[my_board.global_count]['x'] = my_centre[0]
            self.network.node[my_board.global_count]['y'] = my_centre[1]
            self.network.node[my_board.global_count]['z'] = my_centre[2]

            my_board.transform(T)
            my_board.board_frame = Frame(my_board.centre_point, my_board.length_vector, my_board.width_vector)
            if (my_board.layer % 2 != 0 and not my_board.perp) or (my_board.layer % 2 == 0 and my_board.perp):
                if self.flip_toolframe_sec:
                    my_board.tool_frame = Frame(my_board.drop_point, my_board.length_vector, my_board.width_vector*-1)
                else:
                    my_board.tool_frame = Frame(my_board.drop_point, my_board.length_vector*-1, my_board.width_vector)
            else:
                my_board.tool_frame = Frame(my_board.drop_point, my_board.length_vector, my_board.width_vector)
            my_board.box = Box(my_board.board_frame, my_board.length, my_board.width, my_board.height)

    if input_check():
        self.floorslab_grids = []
        self.floorslab_grids = __grid_creation()
        if self.advanced_setup:
            __advanced_length_correction()
        __board_data_setup(self.advanced_setup)

        board_geometry_setup()
        self.setup_done = True
        """for brd in self.elements():
            board = brd[1]
            print("Global Count: {}, Layer: {}, Frame: {}, Location: {}, Supporter: {}, Perpendicular: {}".format(
                board.global_count, board.layer+1, board.board_frame, board.location, board.vert_sup, board.perp))"""

        return self

    else:
        return 1


# creates all the gluepoints between the boards and specifies neighbour relationships
def gluepoints(system):
    def corner_point_finder(my_board):
        def sidepoints(pt):
            left_pt = pt - scale_vector(my_board.width_vector, my_board.width/2)
            right_pt = pt + scale_vector(my_board.width_vector, my_board.width / 2)
            return left_pt, right_pt

        upper_boarder_centre = my_board.centre_point + scale_vector(my_board.length_vector, my_board.length/2)
        lower_boarder_centre = my_board.centre_point + scale_vector(my_board.length_vector, -my_board.length/2)

        left_pt_up = upper_boarder_centre + scale_vector(my_board.width_vector, -my_board.width / 2)
        right_pt_up = upper_boarder_centre + scale_vector(my_board.width_vector, my_board.width / 2)
        left_pt_down = lower_boarder_centre + scale_vector(my_board.width_vector, -my_board.width / 2)
        right_pt_down = lower_boarder_centre + scale_vector(my_board.width_vector, my_board.width / 2)

        return [left_pt_up, right_pt_up, right_pt_down, left_pt_down]

    def line_maker(points):
        lines = []
        for i in range(len(points)-1):
            pt1 = (points[i][0], points[i][1], points[i][2])
            pt2 = (points[i+1][0], points[i+1][1], points[i+1][2])
            lines.append((pt1, pt2))
        pt1 = (points[-1][0], points[-1][1], points[-1][2])
        pt2 = (points[0][0], points[0][1], points[0][2])
        lines.append((pt1, pt2))
        return lines

    def board_intersection(brd1, brd2):
        def surface_calc(upper_board, lower_board, intersection):
            vec1 = Vector(lower_board.length_vector[0], lower_board.length_vector[1], lower_board.length_vector[2])
            vec2 = Vector(upper_board.length_vector[0], upper_board.length_vector[1], upper_board.length_vector[2])
            if upper_board.width > .01:
                ang = vec1.angle(vec2)
            if vec1.angle(vec2) > 0.5:
                len_intersection = lower_board.width
                wid_intersection = upper_board.width
            else:
                # for now we assume that they are parallel in this case, potential error source for later, though
                len_intersection = min(upper_board.length, lower_board.length)
                wid_intersection = min(upper_board.width, lower_board.width)

            dim1 = scale_vector(upper_board.length_vector, len_intersection * .5)
            dim2 = scale_vector(upper_board.width_vector, wid_intersection * .5)

            # this procedure is necessary only because of the glue path planning to make sure points are always ordered clockwise
            ang = angle_vectors_signed(dim1, dim2, Vector(0, 0, 1))
            if ang > 0:
                pt1 = intersection + dim1 - dim2
                pt2 = intersection + dim1 + dim2
                pt3 = intersection - dim1 + dim2
                pt4 = intersection - dim1 - dim2
            else:
                pt1 = intersection - dim1 + dim2
                pt2 = intersection + dim1 + dim2
                pt3 = intersection + dim1 - dim2
                pt4 = intersection - dim1 - dim2

            intersection_surf = Polygon([pt1, pt2, pt3, pt4])
            return intersection_surf

        vec1 = Vector(brd1.length_vector[0], brd1.length_vector[1], brd1.length_vector[2])
        vec2 = Vector(brd2.length_vector[0], brd2.length_vector[1], brd2.length_vector[2])
        line1 = line_creator(brd1.centre_point, vec1, brd1.length)
        line2 = line_creator(brd2.centre_point, vec2, brd2.length)

        standard_option_enabled = False
        # to check whether the boards are parallel
        if ((brd1.vert_sup is False and brd2.vert_sup is False) or
            (brd1.vert_sup and not brd1.perp and brd2.vert_sup and not brd2.perp)) and \
            abs(vec1.angle(vec2)) > 0.1:

            int_pt = intersection_line_line_xy(line1, line2)
            if int_pt is None:
                return None
            # since intersection also hits when the lines intersect in their continuation, we have to add that one
            if distance_point_point(brd1.centre_point, int_pt) < brd1.length / 2 and \
                distance_point_point(brd2.centre_point, int_pt) < brd2.length / 2 and int_pt is not None and int_pt != 0:
                intersection_point = Point(int_pt[0], int_pt[1], brd2.z_drop)
                int_srf = surface_calc(brd1, brd2, intersection_point)
                return int_srf
            else:
                return None
        else:
            pts1 = corner_point_finder(brd1)
            rec1 = Polygon(pts1)
            line1 = line_maker(pts1)
            pts2 = corner_point_finder(brd2)
            rec2 = Polygon(pts2)
            line2 = line_maker(pts2)
            # calculate intersection points
            intersects = set()
            final_points = set()
            segments = []
            # unnecessary, just for checking
            intsct_counter = 0
            for l1 in line1:
                for l2 in line2:
                    intersection_pt = intersection_line_line_xy(l1,l2)
                    if intersection_pt is not None:
                        # check that the intersection point is actually on the line or somewhere in the distance
                        line1_length = distance_point_point_xy(l1[0], l1[1])
                        int1_dist_1 = distance_point_point_xy(l1[0], intersection_pt)
                        int1_dist_2 = distance_point_point_xy(l1[1], intersection_pt)
                        line2_length = distance_point_point_xy(l2[0], l2[1])
                        int2_dist_1 = distance_point_point_xy(l2[0], intersection_pt)
                        int2_dist_2 = distance_point_point_xy(l2[1], intersection_pt)
                        if line1_length*1.01 > (int1_dist_1 + int1_dist_2) and line2_length*1.01 > (int2_dist_1 + int2_dist_2):
                            intsct_counter += 1
                            # now check which points are in the polygon and create segments accordingly
                            if is_point_in_polygon_xy(l1[0], rec2):
                                final_points.add(l1[0])
                                segments.append([l1[0], intersection_pt])
                            if is_point_in_polygon_xy(l1[1], rec2):
                                final_points.add(l1[1])
                                segments.append([l1[1], intersection_pt])
                            if is_point_in_polygon_xy(l2[0], rec1):
                                final_points.add(l2[0])
                                segments.append([l2[0], intersection_pt])
                            if is_point_in_polygon_xy(l2[1], rec1):
                                final_points.add(l2[1])
                                segments.append([l2[1], intersection_pt])

            surface_points = set()

            def segment_cleaner(segs):
                deletes = set()
                for j, seg in enumerate(segs):
                    # check whether the length might be 0
                    difference = 0
                    for i in range(2):
                        difference += abs(seg[0][i] - seg[1][i])
                    if difference == 0.0:
                        deletes.add(j)
                    else:
                        # now check whether they might be just duplicates
                        for k in range(j+1, len(segs)):
                            other_seg = segs[k]
                            if (seg[0] == other_seg[0] and seg[1] == other_seg[1]) or (seg[1] == other_seg[0]
                                and seg[0] == other_seg[1]):
                                deletes.add(k)
                for index in sorted(deletes, reverse=True):
                    del segs[index]
                return segs

            for segment in segments:
                for pt in segment:
                    new_point = (pt[0], pt[1], brd2.z_drop)
                    surface_points.add(new_point)

            if len(segments) > 4:
                segments = segment_cleaner(segments)

            if 2 <= len(segments):
                # three cases:
                # 1) Vectors parallel and same direction
                # 2) Vectors parallel but opposite directions
                # 3) Vectors perpendicular originating in the same point
                corner_pts_temp = []
                for corner_pt in surface_points:
                    corner_pts_temp.append(corner_pt)

                if len(corner_pts_temp) == 2:
                    return None

                # just in case 3 to add the last point
                if len(corner_pts_temp) == 3:
                    v01 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[1])
                    v02 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[2])
                    v12 = Vector.from_start_end(corner_pts_temp[1], corner_pts_temp[2])
                    v01_blank = [v01[0], v01[1], v01[2]]
                    v02_blank = [v02[0], v02[1], v02[2]]
                    v12_blank = [v12[0], v12[1], v12[2]]
                    pt0 = [corner_pts_temp[0][0], corner_pts_temp[0][1], corner_pts_temp[0][2]]
                    pt1 = [corner_pts_temp[1][0], corner_pts_temp[1][1], corner_pts_temp[1][2]]
                    pt2 = [corner_pts_temp[2][0], corner_pts_temp[2][1], corner_pts_temp[2][2]]

                    last_pt = [0,0,0]
                    if max(v01.length, v02.length, v12.length) == v01.length:
                        for i in range(3):
                            last_pt[i] = pt2[i] - v02_blank[i] - v12_blank[i]
                    elif max(v01.length, v02.length, v12.length) == v02.length:
                        for i in range(3):
                            last_pt[i] = pt1[i] - v01_blank[i] + v12_blank[i]
                    else:
                        for i in range(3):
                            last_pt[i] = pt0[i] + v01_blank[i] + v02_blank[i]

                    last_pt_final = (last_pt[0], last_pt[1], last_pt[2])
                    corner_pts_temp.append(last_pt_final)

                vec01 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[1])
                vec02 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[2])
                vec03 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[3])

                # make sure that the second point is right
                if vec01.length > max(vec02.length, vec03.length):
                    a = corner_pts_temp[1]
                    corner_pts_temp[1] = corner_pts_temp[2]
                    corner_pts_temp[2] = a

                # now make sure that the third point is right
                vec12 = Vector.from_start_end(corner_pts_temp[1], corner_pts_temp[2])
                vec13 = Vector.from_start_end(corner_pts_temp[1], corner_pts_temp[3])
                if vec13.length < vec12.length:
                    a = corner_pts_temp[2]
                    corner_pts_temp[2] = corner_pts_temp[3]
                    corner_pts_temp[3] = a

                # now make sure that the points are clockwise
                vec01 = Vector.from_start_end(corner_pts_temp[0], corner_pts_temp[1])
                vec12 = Vector.from_start_end(corner_pts_temp[1], corner_pts_temp[2])

                # if it's clockwise
                if Vector.angle_signed(vec01, vec12, Vector(0, 0, 1)) > 0:
                    return Polygon([corner_pts_temp[0], corner_pts_temp[1], corner_pts_temp[2], corner_pts_temp[3]])
                else:
                    return Polygon([corner_pts_temp[0], corner_pts_temp[3], corner_pts_temp[2], corner_pts_temp[1]])

            # no intersection
            else:
                return None

    def line_creator(pt_a, vec, length):
        pt_b = pt_a + scale_vector(vec, length / 2)
        pt_a = pt_a - scale_vector(vec, length / 2)
        return pt_a, pt_b

    def gluepath_creator(int_surf, path_width, board):
        def interval_checker(dimension):
            underflow = dimension % path_width
            if underflow > 0.02:
                no_paths = dimension//path_width + 1
                new_path_width = dimension/no_paths
                return new_path_width
            else:
                return path_width

        wid_gap = int_surf[1] - int_surf[0]
        wid_vec = Vector(wid_gap[0],wid_gap[1], wid_gap[2])
        wid = wid_vec.length
        wid_vec.unitize()
        len_gap = int_surf[2] - int_surf[1]
        len_vec = Vector(len_gap[0], len_gap[1], len_gap[2])
        len = len_vec.length
        len_vec.unitize()
        wid_path = interval_checker(wid)
        len_path = interval_checker(len)
        path_dims = [wid_path, len_path]
        path_points = []
        iteration = 0
        path_unfinished = True
        current_pt = int_surf[0] + scale_vector(wid_vec, wid_path/2) + scale_vector(len_vec, len_path/2)
        current_vec = len_vec.unitized()
        len_left = len - len_path
        wid_left = wid - wid_path
        dims_left = [len_left, wid_left]
        path_points.append(current_pt)
        R = Rotation.from_axis_and_angle([0, 0, 1], -math.pi/2)
        while path_unfinished:
            current_index = iteration % 2
            current_dim = dims_left[current_index]
            if iteration > 2:
                current_dim -= path_dims[current_index]
                dims_left[current_index] = current_dim

            if current_dim < path_width*0.95:
                break
            current_pt = current_pt + scale_vector(current_vec, current_dim)
            path_points.append(current_pt)
            current_vec.transform(R)
            current_vec.unitize()
            iteration += 1
            if not is_point_in_polygon_xy(current_pt, int_surf):
                print("Warning: Gluepath point not in polygon")
                print(board.global_count)
                print("\n")

        return path_points

    # actual procedure
    for layer_number in range(1, system.layer_no):
        for brd in system.elements():
            board = brd[1]
            if board.layer < layer_number:
                continue
            elif board.layer > layer_number:
                break
            else:
                for i, other_brd in enumerate(system.elements()):
                    other_board = other_brd[1]
                    if other_board.layer < layer_number - 1:
                        continue
                    elif other_board.layer > layer_number - 1:
                        break
                    else:
                        my_glue_surface = board_intersection(board, other_board)
                        if my_glue_surface is None:
                            continue

                        board.glue_surfaces.append(my_glue_surface)
                        board.glue_paths.append(gluepath_creator(my_glue_surface, system.gluepathwidth, board))
                        system.network.edge[board.global_count][i] = system.network.node[other_board.global_count]
    return system

"""
def grasshopper_draw(system):
    def box_update(elmnt):
        elmnt.board_frame = Frame(elmnt.centre_point, elmnt.length_vector, elmnt.width_vector)
        elmnt.box = Box(elmnt.board_frame, elmnt.length, elmnt.width, elmnt.height)
        return elmnt.board_frame, elmnt.box

    visualisations = []
    for brd in system.elements():
        board = brd[1]
        # visualise all the boards
        my_box = box_update(board)[1]
        mesh_box = Mesh.from_shape(my_box)
        artist = MeshArtist(mesh_box)

        box_visualisation = artist.draw_mesh()
        visualisations.append(box_visualisation)

    return visualisations
"""

def component_stack_export(system):
    stack = []
    for brd in system.elements():
        board = brd[1]
        stack.append([board.width, board.height, board.length])
    return stack


def component_instances_export(system):
    global_boards = []
    for brd in system.elements():
        board = brd[1]
        board_format = (board.width, board.height)
        format_entry_complete = False
        length_entry_complete = False
        # now loop through the whole list to see whether your entry is already there

        for j, formats in enumerate(global_boards):
            # format[0][0] are the dimensions of the board
            # format[0][1] is the total length of the format
            if formats[0][0] == board_format:
                format_entry_complete = True
                # the format already exists

                for i in range(1, len(formats)):
                    # the length already exists
                    if board.length == formats[i][0]:
                        formats[i][1] += 1
                        length_entry_complete = True
                        break
                # if it didn't find an entry
                if not length_entry_complete:
                    formats.append([board.length, 1])
                formats[0][1] += board.length

        if not format_entry_complete:
            global_boards.append([[board_format, board.length], [board.length, 1]])

    print("[[[profile_width_1, profile_height_1], total_length_1], [length_a, no_pieces], [length_b, no_pieces], .....]"
          "[[profile_width_2, profile_height_2], total_length_2], [length_a, no_pieces], [length_b, no_pieces], .....]"
          "...]")
    return global_boards


# weight calculation
def weight_calculator(system, protective_clay_height=5.0, density_timber=460, density_clay=1700, fill_limit=None):
        # safety loop in the beginning
        if not system.setup_done:
            print("Error: Setup not completed yet")
            return 1

        area = ((system.primary_length / 100) * (system.secondary_length / 100))
        unit_factor = 1000000

        def calc_clay_volume(ar, clay_hi, timber_vol, unit_fac):
            total_vol = (clay_hi / 100 * ar)
            timber_vol /= unit_fac
            return total_vol - timber_vol

        # actual program

        total_height = protective_clay_height
        timber_volume = 0.0
        clay_volume = 0.0
        current_layer = -1
        """
        for current_layer, board_layer in enumerate(system.timberboards):
            if fill_limit:
                if current_layer == fill_limit:
                    clay_volume = calc_clay_volume(area, total_height, timber_volume, unit_factor)
            total_height += board_layer[0].height
            for board in board_layer:
                timber_volume += board.width * board.height * board.length
       """
        clay_total_height = protective_clay_height
        clay_timber_volume = -1
        for brd in system.elements():
            board = brd[1]
            if board.no_in_layer == 0:
                current_layer += 1
                total_height += board.height
                if current_layer == fill_limit:
                    clay_total_height = total_height
                # at the beginning of the next layer, take the total timber volume
                if current_layer == fill_limit+1:
                    clay_timber_volume = timber_volume

            timber_volume += board.width * board.height * board.length

        if not fill_limit or fill_limit > current_layer:
            clay_timber_volume = timber_volume
            clay_total_height = total_height
        if clay_timber_volume == -1 and fill_limit or fill_limit == 0:
            clay_timber_volume = 0
            clay_total_height = protective_clay_height
        clay_volume = calc_clay_volume(area, clay_total_height, clay_timber_volume, unit_factor)

        timber_volume /= unit_factor
        total_weight = clay_volume * density_clay + timber_volume * density_timber
        relative_weight = total_weight / area
        total_volume = total_height / 100 * area
        void_volume = total_volume - clay_volume - timber_volume

        print("Total Weight: {} kg, Weight/sqm: {} kg, Area: {} m2, Total Volume: {} m3, \nTotal Timber Volume: {} m3, "
              "Total Clay Volume: {} m3, Void Volume: {} m3".format(round(total_weight, 2), round(relative_weight, 2), round(area, 2),
                                                                    round(total_volume, 2), round(timber_volume, 2), round(clay_volume, 2), round(void_volume, 2)))

        return [total_weight, relative_weight, area, total_volume, timber_volume, clay_volume, void_volume]


# Advanced geometry setup
def advanced_floorslab_setup(system, prim_in_sup_length, prim_out_sup_length, prim_in_sup_gap_min=0.0, prim_in_sup_layers=None,
                             prim_in_sup_dist_edge_min=0.0, prim_in_sup_dist_edge_max=100000000, prim_out_sup_gap_min=0.0,
                             prim_out_sup_layers=None, prim_out_sup_dist_edge_min=0.0, prim_out_sup_dist_edge_max=100000000):

    if prim_out_sup_layers is None:
        prim_out_sup_layers = []
    if prim_in_sup_layers is None:
        prim_in_sup_layers = []
    system.advanced_setup = True

    # Inside Supporters
    system.primary_inside_support_gap_min = prim_in_sup_gap_min
    system.primary_inside_support_length = prim_in_sup_length
    system.primary_inside_support_layers = prim_in_sup_layers
    system.primary_inside_support_distance_to_edge_min = prim_in_sup_dist_edge_min
    system.primary_inside_support_distance_to_edge_max = prim_in_sup_dist_edge_max
    system.primary_inside_support_dimensions = copy.deepcopy(system.primary_board_inside_dimensions)
    system.primary_inside_support_dimensions[2] = system.primary_inside_support_length

    # Outside Supporters
    system.primary_outside_support_gap_min = prim_out_sup_gap_min
    system.primary_outside_support_length = prim_out_sup_length
    system.primary_outside_support_layers = prim_out_sup_layers
    system.primary_outside_support_distance_to_edge_min = prim_out_sup_dist_edge_min
    system.primary_outside_support_distance_to_edge_max = prim_out_sup_dist_edge_max
    system.primary_outside_support_dimensions = copy.deepcopy(system.primary_board_outside_dimensions)
    system.primary_outside_support_dimensions[2] = system.primary_outside_support_length


def stack_creator(system, stack_origin_frame, max_height = 10, max_width = 4, bottom_pickup = 0, col_pickup = 0,
                  distance_within_stack = 0.08, distance_between_stacks = 0.12):
    instances = component_instances_export(system)
    stacks = []
    bottom_row_pickup_z = bottom_pickup
    col_pickup_pos = col_pickup
    first_column_position = 0
    # since leftover pieces are often put on top
    max_height -= 1
    for profile in instances:
        profile_width = profile[0][0][0]
        profile_height = profile[0][0][1]
        for i in range(1, len(profile)):
            profile_length = profile[i][0]
            no_elements = profile[i][1]
            no_columns = no_elements // max_height
            overflow = no_elements % max_height
            no_rows = max_height
            if overflow > 0 and no_columns > 0:
                # if columns * rows does not lead to no_elements leave away the first few pieces in the top row
                first_board_picked = overflow
                no_rows += 1
            elif overflow > 0:
                # if there are not even enough elements for one regular column
                no_rows = overflow
                no_columns = 1
                first_board_picked = 0
            else:
                # if it just works out
                no_rows = max_height
                first_board_picked = 0
            new_stack = {"profile_width": profile_width, "profile_height": profile_height,
                         "profile_length": profile_length, "no_elements": no_elements,
                         "no_rows": no_rows, "no_columns": no_columns, "next_board": first_board_picked,
                         "first_column_position": col_pickup_pos + profile_width/2,
                         "first_row_position": bottom_row_pickup_z + profile_height}

            stacks.append(new_stack)
            first_column_position += no_columns * profile_width + (no_columns // max_width) * distance_within_stack\
                                     + distance_between_stacks

    # now that the stacks have been created, we can assign boards to them
    for my_brd in system.elements():
        my_board = my_brd[1]

        for stack_id, my_stack in enumerate(stacks):
            if (my_board.length == my_stack["profile_length"] and my_board.width == my_stack["profile_width"] and
                    my_board.height == my_stack["profile_height"]):
                no_in_stack = my_stack["next_board"]
                col = no_in_stack % my_stack["no_rows"]
                row = my_stack["no_rows"] - no_in_stack // my_stack["no_columns"]
                my_stack["next_board"] += 1

                pick_x = my_stack["profile_length"] / 2
                pick_y = my_stack["first_column_position"] + col*my_stack["profile_width"] + col//max_width * distance_within_stack
                pick_z = row * my_stack["profile_height"] + my_stack["profile_height"]
                stack_origin_point = stack_origin_frame[0]
                pick_point = (stack_origin_point + stack_origin_frame[1]*pick_x + stack_origin_frame[2]*pick_y +
                                    Vector(0, 0, 1) * pick_z)
                stack_pick_fram = Frame(pick_point, stack_origin_frame[1], stack_origin_frame[2])
                stack_center_fram = Frame(Point(pick_point[0], pick_point[1], pick_point[2] - my_stack["profile_height"]/2),
                                          stack_origin_frame[1], stack_origin_frame[2])
                my_board.stack_pick_frame = stack_pick_fram
                my_board.stack_center_frame = stack_center_fram
                my_board.stack_index = stack_id

# secondary_span_interval_development: 1 = constant, <1: denser in the centre, >1: denser on the edges
# operable range approximately 0.6/6

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
#gluepoints(Slabassembly)
weight_calculator(Slabassembly, protective_clay_height=5.0, fill_limit=1, density_clay=1900)


stack_frame = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, -1, 0))
stack_creator(Slabassembly, stack_frame)

myboard = Slabassembly.network.node[1]
mine = myboard["element"].box

print("hello")
# secondary_span_interval_development: 1 = constant, <1: denser in the centre, >1: denser on the edges
# operable range approximately 0.6/6

