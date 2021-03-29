from manim import *
import numpy as np
import math

e=math.e


def sigmoid(x):
    return 1/(1+e**(-x+5))

def sig(x):
    return 100/(1+e**(-x+5))

def dsig(x):
    return 100*(1-sigmoid(x))*sigmoid(x)


class WhatIsDerivative(GraphScene, ZoomedScene):
    CONFIG={
            "x_axis_width":10.,
            "x_min":0,
            "x_max":10,
            "y_axis_height":6.,
            "y_min":0,
            "y_max":100,
            "x_labeled_nums":[1,2,3,4,5,6,7,8,9,10],
            "y_labeled_nums":[10,20,30,40,50,60,70,80,90,100],
            "graph_origin":3 * DOWN + 5.2 * LEFT,
            "x_axis_label":Text("時間(秒)"),
            "y_axis_label":Text("距離(m)"),
            "y_tick_freq": 10,
            "x_axis_config":{"numbers_with_elongated_ticks":[]},
            "y_axis_config":{"numbers_with_elongated_ticks":[]},
            "stroke_width":2.5,
            "dot_radius":0.05,
            "func": sig,
            "d_func": dsig,
            # for ZoomedScene
            "zoom_factor": 0.25,
            "zoomed_display_height": 5,
            "zoomed_display_width": 5,
            "image_frame_stroke_width": 1,
            "zoomed_camera_config": {
                "default_frame_stroke_width": 1,
        },
    }
    def setup(self):
        GraphScene.setup(self)
        ZoomedScene.setup(self)

    def construct(self):

        """choose class method animation from below"""
        #self.animate_point_p_moving_along_numberline()
        #self.animate_point_p_moving_on_the_graph(self.func)
        #self.show_how_to_read_the_graph()
        #self.visualize_average_speed()
        #self.visualize_dissociation()
        #self.visualize_dissociation2()
        #self.animate_how_derivative_calculated()
        self.draw_derivative_cruve()


    def animate_point_p_moving_along_numberline(self):
        """ objects """
        numberline=Line([-4,0,0],[4,0,0])
        dot_m=Dot(color=BLUE).move_to(numberline.get_start())

        dot_l=Dot().move_to([-4,0,0])
        dot_r=Dot().move_to([4,0,0])

        pointA=MathTex("A").next_to(dot_l,DOWN)
        pointB=MathTex("B").next_to(dot_r,DOWN)
        line_group=VGroup(numberline, dot_l, dot_r, pointA, pointB)

        pointP=MathTex("P").set_color(BLUE).next_to(dot_m,UP)
        pointP.add_updater(lambda x: x.next_to(dot_m,UP))

        brace=BraceBetweenPoints(dot_l.get_center(),dot_r.get_center(), UP, buff=0.2)
        distance=MathTex("100\\rm m").next_to(brace,1*UP)
        braces=VGroup(brace, distance)

        t=ValueTracker(0)
        time=DecimalNumber(t.get_value(), num_decimal_places=0).shift(2*UP)
        time.add_updater(lambda m: m.set_value(t.get_value()))
        seconds=Text("秒").scale(0.6).next_to(time,1*RIGHT)
        # to use method as function as below
        def timecount(time):
            return time.set_value(10.0)

        self.add(line_group, dot_m, pointP, braces)
        self.wait()
        self.play(FadeOut(braces))
        self.play(
            ShowCreation(time),
            ShowCreation(seconds),
            )
        self.wait()
        self.play(
            MoveAlongPath(dot_m, numberline, rate_func=smooth),
            # ApplyFunction allows us to use method as a function
            # that enables setting up different rate_func in one animation 
            ApplyFunction(timecount, t, rate_func=linear),
            run_time=10,
            )
        pointP.clear_updaters()
        time.clear_updaters()

        self.play(
            dot_m.move_to, numberline.get_start(),
            )
        
        self.wait()

    def animate_point_p_moving_on_the_graph(self, func, loc_l=[-4,0,0], loc_r=[4,0,0], p_color=BLUE, v_line_color=BLUE, h_line_color=YELLOW, stroke_width=2.5):  
        """ objects """
        #numberline
        numberline=Line(loc_l,loc_r)
        # dots
        dot_P=Dot(color=p_color).move_to(numberline.get_start())
        # setup 
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(func, stroke_width=stroke_width)
        # a dot moves along the curve
        dot=Dot(radius=0).move_to(self.coords_to_point(0,0))
        # a dot moves along x_axis
        dot_h=Dot(radius=0).move_to(self.coords_to_point(0,0))
        dot_h.add_updater(lambda x: x.move_to([dot.get_center()[0],self.coords_to_point(0,0)[1],0]))
        # a dot moves along y_axis
        dot_v=Dot(color=v_line_color).move_to(self.coords_to_point(0,0))
        dot_v.add_updater(lambda x: x.move_to([self.coords_to_point(0,0)[0],dot.get_center()[1],0]))
        # a line across dot and dot_h
        line_h=Line(dot, dot_h, stroke_width=2, color=h_line_color)
        line_h.add_updater(lambda x: x.become(Line(dot, dot_h, stroke_width=2, color=h_line_color)))
        # a line across dot and dot_v        
        line_v=Line(dot, dot_v, stroke_width=2, color=v_line_color)
        line_v.add_updater(lambda x: x.become(Line(dot, dot_v, stroke_width=2, color=v_line_color)))
        
        # Animations
        self.add(numberline, dot_P)
        self.play(
            ReplacementTransform(numberline, self.y_axis),
            ReplacementTransform(dot_P, dot_v),
            ShowCreation(self.x_axis),
            dot_h.add,
            line_h.add,
            line_v.add,
            run_time=2
            )
        self.bring_to_front(dot_v)
        self.wait(0.5)
        self.play(
            MoveAlongPath(dot, curve.copy()),
            ShowCreation(curve),
            run_time=10
            )
        self.wait()
        dot_h.clear_updaters()
        dot_v.clear_updaters()
        line_h.clear_updaters()
        line_v.clear_updaters()
        self.play(
            FadeOut(dot_h), FadeOut(dot_v), FadeOut(dot), FadeOut(line_h), FadeOut(line_v),
            )

    def show_how_to_read_the_graph(self):
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(self.func, stroke_width=2.5)
        # points 5
        p5=Dot(radius=0.05).move_to(self.coords_to_point(5,0))
        p5_y=Dot(radius=0).move_to(self.coords_to_point(0, self.func(5)))
        p5_on_c=Dot(radius=0).move_to(self.coords_to_point(5, self.func(5)))
        v_line5=DashedLine(p5,p5_on_c,color=YELLOW, stroke_width=2)
        h_line5=DashedLine(p5_y, p5_on_c, color=BLUE,stroke_width=2)
        brace_5=Brace(v_line5,RIGHT, width=80)
        label_5a=Text("５秒時点の")
        label_5b=Text("総移動距離").next_to(label_5a,0.65*DOWN)
        label_5=VGroup(label_5a,label_5b).scale(0.45).next_to(brace_5,RIGHT)
        # points 8
        p8=Dot(radius=0.05).move_to(self.coords_to_point(8,0))
        p8_y=Dot(radius=0).move_to(self.coords_to_point(0, self.func(8)))
        p8_on_c=Dot(radius=0).move_to(self.coords_to_point(8, self.func(8)))
        v_line8=DashedLine(p8,p8_on_c,color=YELLOW, stroke_width=2)
        h_line8=DashedLine(p8_y, p8_on_c, color=BLUE,stroke_width=2)
        brace_8=Brace(v_line8,RIGHT, width=120)
        label_8a=Text("８秒時点の")
        label_8b=Text("総移動距離").next_to(label_8a,0.65*DOWN)
        label_8=VGroup(label_8a,label_8b).scale(0.45).next_to(brace_8,RIGHT)

        self.add(
            self.axes,
            curve,
            p5,p5_on_c,v_line5,h_line5,brace_5,label_5,
            p8,p8_on_c,v_line8,h_line8,brace_8,label_8,
            )
   
    def visualize_average_speed(self):
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(self.func, stroke_width=2.5)
        # secant line group
        secant_slope_group=self.get_secant_slope_group(
            0,
            curve,
            dx=10,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label="\\Delta x=10\\mathrm{s}",
            df_label="\\Delta y=100\\mathrm{m}",
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=13,
            stroke_width=2.5,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        #label
        label=Text("平均速度：").scale(0.55).set_color(PINK)
        labela=Text("２点を結ぶ直線の傾き").scale(0.4).next_to(label,RIGHT)
        label=VGroup(label,labela)

        label1=Fraction(
            num=MathTex("100\\mathrm{m}").set_color(YELLOW),denom=MathTex("10\\mathrm{s}").set_color(BLUE)
            ).scale(0.8)
        eq1=MathTex("=").scale(0.8).next_to(label1,RIGHT)
        label2=MathTex("10\\mathrm{m/s}").scale(0.8).set_color(PINK).next_to(eq1,RIGHT)
        labels=VGroup(label1, eq1,label2,).next_to(label,DOWN)
        labels=VGroup(label,label1, eq1,label2,).add_background_rectangle().move_to(self.coords_to_point(2.75,65))


        self.add(
            self.axes,
            curve,
            secant_slope_group,
            labels
            )

    def visualize_dissociation(self):
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(self.func, stroke_width=2.5)
        slope=self.get_graph(lambda x: 10*x, color=PINK, stroke_width=2)
        secant_slope_group=self.get_secant_slope_group(
            0,
            curve,
            dx=10,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label="\\Delta x",
            df_label="\\Delta y",
            include_secant_line=False,
            secant_line_color=PINK,
            secant_line_length=13,
            stroke_width=2.5,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        # define area
        area=self.get_area(curve, 0, 10,bounded=slope, dx_scaling=0.1, area_color=BLUE)
        # description
        desc_a=Text("ここの面積の大きさが")
        desc_b=Text("平均変化率と実際との").next_to(desc_a,0.75*DOWN)
        desc_c=Text("乖離の大きさを示す。").next_to(desc_b,0.75*DOWN)
        desc=VGroup(desc_a,desc_b,desc_c).scale(0.5).move_to(self.coords_to_point(2.5,81.7)).add_background_rectangle()
        line1=Line(desc.get_right(), self.coords_to_point(7.5, self.func(7.5)-10), stroke_width=1.5, buff=0.2)
        line2=Line(desc.get_bottom(), self.coords_to_point(2.5, self.func(2.5)+5), stroke_width=1.5, buff=0.2)
        self.add(
            self.axes,
            area, curve, slope, desc, line1, line2,
            secant_slope_group)

    def visualize_dissociation2(self):
        w=1.5
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(self.func, stroke_width=2)
        slope=self.get_graph(lambda x: 14.9738*(x-2.2), x_min=3, x_max=4, color=PINK, stroke_width=1.5)
        area=self.get_area(curve, 3, 4, bounded=slope, dx_scaling=0.1, area_color=BLUE)
        #secants
        s1=self.get_secant_slope_group(
            0,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s2=self.get_secant_slope_group(
            1,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s3=self.get_secant_slope_group(
            2,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s4=self.get_secant_slope_group(
            3,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.3,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s5=self.get_secant_slope_group(
            4,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.65,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s6=self.get_secant_slope_group(
            5,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.65,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s7=self.get_secant_slope_group(
            6,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.3,
            stroke_width=w,
            label_scale=0.8,
            background_rectangle=True,
            dashed=True
            )
        s8=self.get_secant_slope_group(
            7,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=1.1,
            background_rectangle=True,
            dashed=True
            )
        s9=self.get_secant_slope_group(
            8,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=1.1,
            background_rectangle=True,
            dashed=True
            )
        s10=self.get_secant_slope_group(
            9,
            curve,
            dx=1,
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label=None,
            df_label=None,
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=1.1,
            stroke_width=w,
            label_scale=1.1,
            background_rectangle=True,
            dashed=True
            )
        #Label
        t=Text("乖離した面積").scale(0.175*0.65).move_to(self.coords_to_point(3.2, self.func(3.9)))
        line=Line(t.get_bottom(), self.coords_to_point(3.5,self.func(3.5)), stroke_width=0.2, buff=0.025)

        zoomed_camera=self.zoomed_camera
        zoomed_display=self.zoomed_display.to_corner(UR)
        frame=zoomed_camera.frame
        #zoomed_display_frame=zoomed_display.display_frame
        frame.move_to(self.coords_to_point(3.5,self.func(3.5)))


        self.add(
            self.axes,
            area,
            curve,
            s1,
            s2,
            s3,
            s4,
            s5,
            s6,
            s7,
            s8,
            s9,
            s10,
            slope,
            t,
            line
            )
        self.activate_zooming()

    def animate_how_derivative_calculated(self):
        w=1.5
        axes=self.setup_axes()
        # define a curve  
        curve=self.get_graph(self.func, stroke_width=2)
        # dx value updater
        dx_value=ValueTracker(1)
        # dx counter
        dx_counter=DecimalNumber(dx_value.get_value(), num_decimal_places=4).set_color(BLUE)
        dx_counter.add_updater(lambda m: m.set_value(dx_value.get_value()))
        # dy counter
        dy_counter=DecimalNumber(self.func(5+dx_value.get_value())-self.func(5), num_decimal_places=4).set_color(YELLOW)
        dy_counter.add_updater(lambda m: m.set_value(self.func(5+dx_value.get_value())-self.func(5)))

        """
        for formula
        """

        fl1=Text("瞬間の変化率").scale(0.6)
        #eq1=MathTex("=").next_to(fl1,RIGHT)
        fl2=Fraction(num=MathTex("dy").set_color(YELLOW), denom=MathTex("dx").set_color(BLUE)).scale(0.8)
        eq2=MathTex("=").next_to(fl2,RIGHT)
        dy_dx_counter=Fraction(num=dy_counter,denom=dx_counter).scale(0.8).next_to(eq2,RIGHT)
        eq3=MathTex("=").next_to(eq2,3.5*DOWN)
        # calculator: value of dydx 
        dydx=DecimalNumber(
            (self.func(5+dx_value.get_value())-self.func(5))/dx_value.get_value(),
            num_decimal_places=4).next_to(eq3,RIGHT).scale(0.8).set_color(PINK)
        dydx.add_updater(
            lambda x: x.become(DecimalNumber((self.func(5+dx_value.get_value())-self.func(5))/dx_value.get_value(),
            num_decimal_places=4).scale(0.8).next_to(eq3,RIGHT).set_color(PINK)))
        fl2_g=VGroup(fl2, eq2, dy_dx_counter, eq3, dydx).next_to(fl1,1.4*DOWN)
        fl_group=VGroup(fl1,fl2_g).add_background_rectangle().to_corner(UL).shift(1.8*RIGHT+DOWN)
        
        # secant slope group
        secant_group=self.get_secant_slope_group(
            5,
            curve,
            dx=dx_value.get_value(),
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label="dx",
            df_label="dy",
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=6,
            stroke_width=w,
            label_scale=1,
            background_rectangle=True,
            dashed=False
            )
        def secant_group_updater(x):
            x.become(self.get_secant_slope_group(
            5,
            curve,
            dx=dx_value.get_value(),
            dx_line_color=BLUE,
            df_line_color=YELLOW,
            dx_label="dx",
            df_label="dy",
            include_secant_line=True,
            secant_line_color=PINK,
            secant_line_length=6,
            stroke_width=w,
            label_scale=1,
            background_rectangle=True,
            dashed=False
            ))
        secant_group.add_updater(secant_group_updater)
        # for zoomed scene setup
        zoomed_camera=self.zoomed_camera
        zoomed_display=self.zoomed_display.to_corner(UR)
        frame=zoomed_camera.frame
        frame.move_to(self.coords_to_point(5.1,self.func(5.015)))

        self.add(
            self.axes,
            curve,
            secant_group,
            fl_group
            )
        self.wait()
        self.play(
            dx_value.set_value, 0.1,
            run_time=5
            )
        self.activate_zooming(animate=True)
        self.wait()
    
    def draw_derivative_cruve(self, stroke_width=2.5):
        self.setup_axes()
        curveA=self.get_graph(
            self.func,
            stroke_width=stroke_width,
            )
        line=VMobject()
        dot_start=Dot(radius=self.dot_radius).move_to(self.coords_to_point(0,self.func(0)))
        # add updater to tangent line
        line.add_updater(self.get_derivative_updater(dot_start))
        self.add(self.axes,curveA, line, dot_start)

        self.move_dot_and_draw_derivative_function(
            dot_start,      # put a dot to move
            0,           # where a dot starts from
            10.,            # where a dot to go
            d_func=self.d_func,   # put a function
            run_time=10
            )
        self.wait()

        # remove updater after the animation
        line.clear_updaters()

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

    def get_line_across_points(self,d1,d2,buff=2, color=PINK, stroke_width=3, length=6):
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
                color=PINK,
            )
            derivative.set_length(length)
            derivative.move_to(dot)
            derivative.set_color(PINK)
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


class Subtitle(VGroup):
    CONFIG={
        "sub1":Text("字幕"),
        "sub2":None,
        "sub3":None,
        "sub4":None,
        "sub5":None,
        "sub6":None,
        "position":[0,-3.5,0],
        "position2":[0,-3.3,0],
        }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.s1=self.sub1
        self.sub=VGroup(self.s1).move_to([self.position]).scale(0.55).add_background_rectangle()
        if self.sub2:
            self.sub_a=VGroup(self.s1).scale(1/0.55)
            self.s2=self.sub2.next_to(self.sub_a, 1*RIGHT)
            self.sub=VGroup(self.sub_a,self.s2).move_to([self.position]).scale(0.55).add_background_rectangle()
        if self.sub3:
            self.sub_a=VGroup(self.s1, self.s2,).scale(1/0.55)
            self.s3=self.sub3.next_to(self.sub_a, RIGHT)
            self.sub=VGroup(self.sub_a,self.s3).move_to([self.position]).scale(0.55).add_background_rectangle()
        if self.sub4:
            self.sub_a=VGroup(self.s1, self.s2, self.s3).scale(1/0.55)
            self.s4=self.sub4.next_to(self.sub_a, 0.8*DOWN)
            self.sub=VGroup(self.sub_a, self.s4).move_to([self.position2]).scale(0.55).add_background_rectangle()
        if self.sub5:
            self.sub.scale(1/0.55)
            self.sub_a=VGroup(self.s1, self.s2, self.s3)
            self.s5=self.sub5.next_to(self.s4, 1*RIGHT)
            self.sub_b=VGroup(self.s4, self.s5).next_to(self.sub_a, 0.8*DOWN)
            self.sub=VGroup(self.sub_a, self.sub_b).move_to([self.position2]).scale(0.55).add_background_rectangle()
        if self.sub6:
            self.sub.scale(1/0.55)
            self.sub_a=VGroup(self.s1, self.s2, self.s3)
            self.s6=self.sub6.next_to(self.s5, 1*RIGHT)
            self.sub_b=VGroup(self.s4, self.s5, self.s6).next_to(self.sub_a, 0.8*DOWN)
            self.sub=VGroup(self.sub_a, self.sub_b).move_to([self.position2]).scale(0.55).add_background_rectangle()  
        
        self.add(self.sub)

class Fraction(VGroup):
    CONFIG={
    "num":MathTex("1"),
    "denom":MathTex("2")
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.numerator=self.num
        self.denominator=self.denom
        self.div_line=Line(self.numerator.get_left(), self.numerator.get_right(), buff=0, stroke_width=2)
        self.numerator.next_to(self.div_line,0.8*UP)
        self.denominator.next_to(self.div_line,0.8*DOWN)
        self.fraction=VGroup(self.numerator,self.div_line, self.denominator)
        self.add(self.fraction)

