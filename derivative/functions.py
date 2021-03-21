from manim import *
import numpy as np
import math
    
    def get_axes(self):
        self.axes = Axes()
        # FIX Y LABELS
        y_labels = self.axes.get_y_axis().numbers
        for label in y_labels:
            label.rotate(-PI/2)
        return self.axes

    # get f(x)
    def get_f(self,x_coord):
        return self.coords_to_point(x_coord, self.func(x_coord))

    def get_dot_from_x_coord(self,x_coord,**kwargs):
        return Dot(
            self.get_f(x_coord),
            radius=self.dot_radius,
            **kwargs
        )

    def get_dot_updater(self, start, end):
        def updater(mob,alpha):
            x = interpolate(start, end, alpha)
            coord = self.get_f(x)
            mob.move_to(coord)
        return updater

    def get_dot_updater_of_d(self, start, end):
        def updater(mob,alpha):
            x = interpolate(start, end, alpha)
            coord = self.get_f_of_d(x)
            mob.move_to(coord)
        return updater

    def get_line_across_points(self,d1,d2,buff=2, color=YELLOW, stroke_width=3, length=6):
        reference_line = Line(d1.get_center(),d2.get_center())
        vector = reference_line.get_unit_vector()
        self.tangent_line=Line(
            d1.get_center() - vector * buff,
            d2.get_center() + vector * buff,
            color=color,
            stroke_width=stroke_width,
        ).set_length(length)
        return self.tangent_line

    def get_line_updater(self,d1,d2,buff=4,length=8,**kwargs):
        def updater(mob):
            mob.become(
                self.get_line_across_points(d1,d2,buff).set_length(length)
            )
        return updater

    def get_derivative_updater(self, dot, length=6):
        def updater(mob):
            derivative = Line(
                dot.get_center(),
                self.get_dot_from_x_coord(
                    self.point_to_coords(
                        dot.get_center()
                        )[0] + 0.0001
                ).get_center(),
                stroke_width=self.stroke_width,
                color=self.tangent_line_color,
            )
            derivative.set_length(length)
            derivative.move_to(dot)
            derivative.set_color(self.tangent_line_color)
            mob.become(derivative)
        return updater

    def move_dot(self,dot,start,end,*args,**kwargs):
        self.play(
            UpdateFromAlphaFunc(
                dot, self.get_dot_updater(start,end),
                *args,
                **kwargs
            )
        )  
    
    def move_dot_and_draw_derivative_function(self, dot,start,end, d_func, run_time=3, *args,**kwargs):
        self.d_curve=self.get_graph(d_func, x_min=start, x_max=end, color=GREEN)
        dot_d=Dot(radius=0)
        
        self.add(dot_d)
        self.play(
            UpdateFromAlphaFunc(dot, self.get_dot_updater(start,end), run_time=run_time, *args, **kwargs),
            MoveAlongPath(dot_d, self.d_curve, run_time=run_time),
            ShowCreation(self.d_curve, run_time=run_time),
            rate_func=smooth,            
        )

        




    
    