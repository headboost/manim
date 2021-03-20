from manim import *
import numpy as np
import math


class DerivativeSquaresArea(VGroup):
    CONFIG={
    "original_square_kwargs":{
        "width":2.5,
        "height":2.5,
        "color":BLUE_E,
        "fill_color":BLUE_E,
        "fill_opacity":1,
        },
    "dx_square_right_kwargs":{
        "width":0.2,
        "height":2.5,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    "dx_square_up_kwargs":{
        "width":2.5,
        "height":0.2,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    "dxdx_square_kwargs":{
        "width":0.2,
        "height":0.2,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    "brace_and_label_kwargs_for_original_square":{
        "brace_color":WHITE,
        "label_color":BLUE,
        },
    "brace_and_label_kwargs_for_dx_squares":{
        "brace_color":WHITE,
        "label_color":YELLOW,
        },
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)

        self.original_square=Rectangle(**self.original_square_kwargs)
        self.dx_square_right=Rectangle(**self.dx_square_right_kwargs).next_to(self.original_square,RIGHT,buff=0)
        self.dx_square_up=Rectangle(**self.dx_square_up_kwargs).next_to(self.original_square,UP,buff=0)
        self.dxdx_square=Rectangle(**self.dxdx_square_kwargs).next_to(self.dx_square_right,UP,buff=0)
        self.squares=VGroup(self.original_square, self.dx_square_right, self.dx_square_up, self.dxdx_square)

        self.brace_up=Brace(self.dx_square_up,0.4*UP,)
        self.label_up=MathTex("x").scale(1).set_color(self.brace_and_label_kwargs_for_original_square["label_color"]).next_to(self.brace_up, 0.6*UP)
        self.brace_right=Brace(self.dx_square_right, 0.4*RIGHT,)
        self.label_right=MathTex("x").scale(1).set_color(self.brace_and_label_kwargs_for_original_square["label_color"]).next_to(self.brace_right, 0.6*RIGHT)
        self.braces_and_labels=VGroup(self.brace_up, self.label_up, self.brace_right, self.label_right)

        self.dx_brace_up=Brace(self.dxdx_square,0.4*UP,)
        self.dx_label_up=MathTex("dx").scale(0.9).set_color(self.brace_and_label_kwargs_for_dx_squares["label_color"]).next_to(self.dx_brace_up, 0.6*UP)
        self.dx_brace_right=Brace(self.dxdx_square,0.4*RIGHT, )
        self.dx_label_right=MathTex("dx").scale(0.9).set_color(self.brace_and_label_kwargs_for_dx_squares["label_color"]).next_to(self.dx_brace_right, 0.6*RIGHT)
        self.dx_braces_and_labels=VGroup(self.dx_brace_up, self.dx_label_up, self.dx_brace_right, self.dx_label_right)

        self.all_squares=VGroup(self.squares, self.braces_and_labels, self.dx_braces_and_labels).move_to([0,0,0])

        self.add(
            self.all_squares,
            )
        
        def get_original_square(self):
            return self.original_square

        def get_dx_square_right(self):
            return self.dx_square_right

        def get_dx_square_up(self):
            return self.dx_square_up

        def get_dxdx_square(self):
            return self.dxdx_square

        def get_brace_up(self):
            return self.brace_up

        def get_brace_right(self):
            return self.brace_right

        def get_dx_brace_up(self):
            return self.dx_brace_up

        def get_dx_brace_right(self):
            return self.dx_brace_right

        def get_label_up(self):
            return self.label_up

        def get_label_right(self):
            return self.label_right

        def get_dx_label_up(self):
            return self.dx_label_up

        def get_dx_label_right(self):
            return self.dx_label_right

class DerivativeSquaresAreaSplitted(DerivativeSquaresArea):
    CONFIG={
        "kwargs":
            {
            "split_factor": 0.2
            },
        }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.dx_square_right.shift(self.kwargs["split_factor"]*RIGHT)
        self.dx_square_up.shift(self.kwargs["split_factor"]*UP)
        self.dxdx_square.shift(self.kwargs["split_factor"]*UP+self.kwargs["split_factor"]*RIGHT)
        self.brace_up.shift(self.kwargs["split_factor"]*UP)
        self.brace_right.shift(self.kwargs["split_factor"]*RIGHT)
        self.label_up.shift(self.kwargs["split_factor"]*UP)
        self.label_right.shift(self.kwargs["split_factor"]*RIGHT)
        self.dx_brace_up.shift(self.kwargs["split_factor"]*UP+self.kwargs["split_factor"]*RIGHT)
        self.dx_brace_right.shift(self.kwargs["split_factor"]*UP+self.kwargs["split_factor"]*RIGHT)
        self.dx_label_up.shift(self.kwargs["split_factor"]*UP+self.kwargs["split_factor"]*RIGHT)
        self.dx_label_right.shift(self.kwargs["split_factor"]*UP+self.kwargs["split_factor"]*RIGHT)
        
class DerivativeCubeVolume(VGroup):
    CONFIG={
        "original_cube_kwargs":{
            "color":BLUE_E,
            "stroke_color":WHITE,
            "opacity":0.75,
            "stroke_width":0.5,
            "side_length": 2.5,
            },
        "added_cubes_kwargs":{
            "color":YELLOW_E,
            "stroke_color":YELLOW,
            "opacity":0.4,
            "stroke_width":0.5,
            "thickness": 0.2,
            },
        "brace_and_label_kwargs_for_original_cube":{
            "brace_color":WHITE,
            "label_color":BLUE,
            },
        "brace_and_label_kwargs_for_dx_cube":{
            "brace_color":WHITE,
            "label_color":YELLOW,
            },
        }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)

        c_opacity_cubes=0.4
        # transform_matrix
        y=10*PI/180
        x=10*PI/180
        y_mat=[[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]]  #y軸周りに回転
        x_mat=[[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]]  #x軸周りに回転
        # fix coordinates
        fix_c=self.original_cube_kwargs["side_length"]/2+self.added_cubes_kwargs["thickness"]/2


        self.cube=Cube(
            fill_opacity=self.original_cube_kwargs["opacity"],
            fill_color=self.original_cube_kwargs["color"],
            color=self.original_cube_kwargs["stroke_color"],
            stroke_width=self.original_cube_kwargs["stroke_width"],
            side_length=self.original_cube_kwargs["side_length"]
            ).move_to([0,0,0])

        self.cube_f=Prism(
            dimensions=[self.original_cube_kwargs["side_length"],self.original_cube_kwargs["side_length"],self.added_cubes_kwargs["thickness"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [0,0,fix_c]
            )
        self.cube_t=Prism(
            dimensions=[self.original_cube_kwargs["side_length"],self.added_cubes_kwargs["thickness"],self.original_cube_kwargs["side_length"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ). move_to(
            [0, fix_c, 0]
            )
        self.cube_r=Prism(
            dimensions=[self.added_cubes_kwargs["thickness"],self.original_cube_kwargs["side_length"],self.original_cube_kwargs["side_length"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [fix_c,0,0]
            )
        self.bar_f=Prism(
            dimensions=[self.original_cube_kwargs["side_length"],self.added_cubes_kwargs["thickness"],self.added_cubes_kwargs["thickness"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [0,
            fix_c,
            fix_c]
            )
        self.bar_r=Prism(
            dimensions=[self.added_cubes_kwargs["thickness"],self.original_cube_kwargs["side_length"],self.added_cubes_kwargs["thickness"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [fix_c,
            0,
            fix_c]
            )
        self.bar_t=Prism(
            dimensions=[self.added_cubes_kwargs["thickness"],self.added_cubes_kwargs["thickness"],self.original_cube_kwargs["side_length"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [
            fix_c,
            fix_c,
            0,]
            )
        self.cube_dx=Prism(
            dimensions=[self.added_cubes_kwargs["thickness"],self.added_cubes_kwargs["thickness"],self.added_cubes_kwargs["thickness"]],
            fill_opacity=self.added_cubes_kwargs["opacity"],
            fill_color=self.added_cubes_kwargs["color"],
            color=self.added_cubes_kwargs["stroke_color"],
            stroke_width=self.added_cubes_kwargs["stroke_width"],
            ).move_to(
            [
            fix_c,
            fix_c,
            fix_c,]
            )
        self.cubes=VGroup(
            self.cube, 
            self.cube_f, 
            self.cube_t, 
            self.cube_r, 
            self.bar_f, 
            self.bar_t, 
            self.bar_r, 
            self.cube_dx
            )

        self.br_cube=Brace(
            self.cube,LEFT
            ).move_to(
            [-(fix_c+0.2), 0, -(fix_c+0.2)]
            )

        self.lab_cube=MathTex("x").scale(1).set_color(
            self.brace_and_label_kwargs_for_original_cube["label_color"]
            ).next_to(self.br_cube,1*LEFT)
        self.br_cube_t=Brace(
            self.bar_f,LEFT
            ).move_to(
            [-(fix_c+0.2), (fix_c), -(fix_c+0.2)]
            )

        self.lab_cube_t=MathTex("dx").scale(0.9).set_color(self.brace_and_label_kwargs_for_dx_cube["label_color"]).next_to(self.br_cube_t,1*LEFT)
            
        self.braces_and_labels=VGroup(self.br_cube, self.lab_cube, self.br_cube_t, self.lab_cube_t)

        self.cubes_and_braces=VGroup(self.cubes, self.braces_and_labels).apply_matrix(y_mat).apply_matrix(x_mat)
        self.add(self.cubes_and_braces)

    def get_original_cube(self):
        return self.cube

    def get_original_brace_and_label(self):
        return VGroup(self.br_cube, self.lab_cube)

    def get_d_brace_and_label(self):
        return VGroup(self.br_cube_t, self.lab_cube_t)

    def get_dx_cubes(self):
        return VGroup(self.cube_f, self.cube_t, self.cube_r)

    def get_dxdx_cubes(self):
        return VGroup(self.bar_f, self.bar_t, self.bar_r)

    def get_dx3_cube(self):
        return self.cube_dx

class DerivativeCubeVolumeSplitted(DerivativeCubeVolume):