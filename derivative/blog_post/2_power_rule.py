from manim import *
import numpy as np
import math
import itertools as it

    
class PowerRuleAsArea(GraphScene):
    CONFIG={
            "x_axis_width":5.5,
            "x_min":0,
            "x_max":5,
            "y_axis_height":5.5,
            "y_min":0,
            "y_max":25,
            "x_labeled_nums":[1,2,3,4,5],
            "y_labeled_nums":[5,10,15,20,25],
            "graph_origin":2.5 * DOWN + 0.75 * RIGHT,
            "x_axis_label":MathTex("x"),
            "y_axis_label":MathTex("y"),
            "y_tick_freq": 5,
            "x_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "y_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "stroke_width":2.5,
            "dot_radius":0.05,
            "func": lambda x: x**2,
            "d_func": lambda x: 2*x,
            "o_rec_color":BLUE_E,

    }

    def construct(self):
        self.imagine_power_function_as_area_of_square()
        self.what_happens_to_the_area_when_dx()
        self.calculate_df()
        self.minimize_dx()


    def imagine_power_function_as_area_of_square(self):
        """ sub """
        sub=Text("関数ｆ(ｘ)＝ｘ^２は、このように正方形の面積として考えることができます。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        lab_g=MathTex("f(x)","=","x","{}^2").scale(0.8).move_to(self.coords_to_point(3.5,23))
        # x_value
        x_value=ValueTracker(2.5)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # area
        area=Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        area.add_updater(lambda x: x.become(Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)))
        br_u=Brace(area,0.5*UP).add_updater(lambda x: x.become(Brace(area,0.5*UP)))
        br_r=Brace(area,0.5*RIGHT).add_updater(lambda x: x.become(Brace(area,0.5*RIGHT)))
        lab_u=MathTex("x").scale(0.8).next_to(br_u,0.5*UP).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_u,0.5*UP)))
        lab_r=MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT)))
        lab_x2=MathTex("x^2").scale(0.8).move_to(area).add_updater(lambda x: x.become(MathTex("x^2").scale(0.8).move_to(area)))
        areas=VGroup(area, br_u, br_r, lab_u, lab_r, lab_x2)

        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)
        h_line.add_updater(lambda x: x.become(Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)))


        self.add(self.axes, curve, lab_g ,area, v_line, h_line,dot_m)
        self.play(ShowCreation(sub), run_time=2, rate_func=linear)
        self.play(
            ReplacementTransform(lab_g[2].copy(),lab_u),
            ShowCreation(br_u),
            )
        self.play(
            ReplacementTransform(lab_g[2].copy(),lab_r),
            ShowCreation(br_r),
            )
        self.play(ShowCreation(lab_x2))
        self.play(
            x_value.set_value, 5,
            rate_func=there_and_back,
            run_time=10
            )
        self.wait()
        self.play(
            x_value.set_value, 3,
            rate_func=smooth,
            run_time=2
            )
        self.wait()

    def what_happens_to_the_area_when_dx(self):
        """ sub """
        sub1=Text("ｘの値がｄｘ増加すると、その分だけ面積も増加します。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub2=Text("具体的には、この黄色で示した部分がｄｘによる増加面積ｄｆです。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        lab_g=MathTex("f(x)","=","x","{}^2").scale(0.8).move_to(self.coords_to_point(3.5,23))
        # x_value
        x_value=ValueTracker(3)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # area
        area=Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        area.add_updater(lambda x: x.become(Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)))
        br_u=Brace(area,0.5*UP).add_updater(lambda x: x.become(Brace(area,0.5*UP)))
        br_r=Brace(area,0.5*RIGHT).add_updater(lambda x: x.become(Brace(area,0.5*RIGHT)))
        lab_u=MathTex("x").scale(0.8).next_to(br_u,0.5*UP).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_u,0.5*UP)))
        lab_r=MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT)))
        lab_x2=MathTex("x^2").scale(0.8).move_to(area).add_updater(lambda x: x.become(MathTex("x^2").scale(0.8).move_to(area)))
        areas=VGroup(area, br_u, br_r, lab_u, lab_r, lab_x2)

        d_area=DerivativeSquaresArea(original_square_kwargs={"width":3, "height":3}).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        o_brs_and_labels=d_area.get_o_braces_and_labels()
        dx_brs_and_labels=d_area.get_dx_braces_and_labels()
        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)

        v_line2=Line(self.coords_to_point(3.25,0), self.coords_to_point(3.25, self.func(3.25)), stroke_width=1.5).set_color(YELLOW)
        # dx line
        dx_line=Line(self.coords_to_point(3,0), self.coords_to_point(3.25,0))
        br_dx_line=Brace(dx_line,0.5*DOWN).add_background_rectangle().shift(0.1*UP)
        lab_dx_br=MathTex("dx").set_color(BLUE).scale(0.8).next_to(br_dx_line,0.15*DOWN).add_background_rectangle()
        br_lab_dx_line=VGroup(br_dx_line, lab_dx_br)

        # df(x)
        interim_point=Dot(radius=0).move_to(self.coords_to_point(3.25, self.func(3)))
        df_line=Line(interim_point, self.coords_to_point(3.25,self.func(3.25)), stroke_width=1.5).set_color(YELLOW)
        df_brace=Brace(df_line,0.5*RIGHT).shift(0.1*LEFT)
        df_label=MathTex("df").scale(0.8).set_color(YELLOW).next_to(df_brace,0.5*RIGHT)
        df_braces=VGroup(df_brace, df_label)

        # formula
        df_fl1=MathTex("df","=").move_to([1.,0.92,0])
        df_fl1[0].set_color(YELLOW)
        bar1=d_area.dx_square_right.copy().next_to(df_fl1,RIGHT)
        plus=MathTex("+").next_to(bar1,RIGHT)
        bar2=d_area.dx_square_right.copy().next_to(plus,RIGHT)
        plus2=MathTex("+").next_to(bar2,RIGHT)
        dxdx=d_area.dxdx_square.copy().next_to(plus2,RIGHT)

        self.add(self.axes, curve, lab_g ,areas, v_line, h_line, dot_m)
        self.play(ShowCreation(sub1), rate_func=linear, run_time=2)
        self.play(FadeOut(self.y_axis), FadeOut(h_line))
        self.play(
            x_value.set_value, 3.25,
            ShowCreation(dx_line),
            rate_func=linear,
            run_time=1.5,
            )
        self.play(ShowCreation(v_line2))
        self.play(
            x_value.set_value, 3,
            rate_func=linear,
            run_time=1.5,
            )

        self.play(ShowCreation(br_lab_dx_line))
        self.wait()
        self.add(
            d_area.original_square,
            d_area.x2_label,
            o_brs_and_labels,
            )
        self.remove(areas)

        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), rate_func=linear, run_time=2.5)

        self.play(
            FadeIn(d_area.dx_square_right),
            FadeIn(d_area.dx_square_down),
            FadeIn(d_area.dxdx_square),
            FadeIn(dx_brs_and_labels),
            o_brs_and_labels[2:].shift, 0.25*RIGHT,
            ) 
        
        self.play(
            ShowCreation(df_braces),
            dx_line.move_to, self.coords_to_point(3.125,self.func(3)),
            br_lab_dx_line.move_to, self.coords_to_point(3.125,7.5),
            d_area.dx_square_right.shift, 0.2*RIGHT,
            d_area.dx_square_down.shift, 0.2*DOWN,
            d_area.dxdx_square.shift, 0.2*DOWN+0.2*RIGHT,
            o_brs_and_labels[2:].shift, 0.2*RIGHT,
            dx_brs_and_labels[:2].shift, 0.2*RIGHT,
            dx_brs_and_labels[2:].shift, 0.2*DOWN+0.2*RIGHT,
            )
        self.wait()
        self.play(lab_g.move_to, self.coords_to_point(4.5, 27))
        self.play(ReplacementTransform(df_label.copy(), df_fl1))
        self.play(ReplacementTransform(d_area.dx_square_right.copy(), bar1))
        self.play(ShowCreation(plus))
        self.play(ReplacementTransform(d_area.dx_square_down.copy(), bar2))
        self.play(ShowCreation(plus2))
        self.play(ReplacementTransform(d_area.dxdx_square.copy(),dxdx))
        self.wait()

    def calculate_df(self):
        """ sub """
        sub1=Text("ｘの値がｄｘ増加すると、その分だけ面積も増加します。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub2=Text("具体的には、この黄色で示した部分がｄｘによる増加面積ｄｆです。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        lab_g=MathTex("f(x)","=","x","{}^2").scale(0.8).move_to(self.coords_to_point(3.5,23))
        # x_value
        x_value=ValueTracker(3)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # area
        area=Rectangle(
            width=x_value.get_value(),
            height=x_value.get_value(),
            color=self.o_rec_color,
            fill_color=self.o_rec_color,
            fill_opacity=1,
            ).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        area.add_updater(lambda x: x.become(Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)))
        br_u=Brace(area,0.5*UP).add_updater(lambda x: x.become(Brace(area,0.5*UP)))
        br_r=Brace(area,0.5*RIGHT).add_updater(lambda x: x.become(Brace(area,0.5*RIGHT)))
        lab_u=MathTex("x").scale(0.8).next_to(br_u,0.5*UP).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_u,0.5*UP)))
        lab_r=MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT).add_updater(lambda x: x.become(MathTex("x").scale(0.8).next_to(br_r,0.5*RIGHT)))
        lab_x2=MathTex("x^2").scale(0.8).move_to(area).add_updater(lambda x: x.become(MathTex("x^2").scale(0.8).move_to(area)))
        areas=VGroup(area, br_u, br_r, lab_u, lab_r, lab_x2)

        d_area=DerivativeSquaresArea(original_square_kwargs={"width":3, "height":3}).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        o_brs_and_labels=d_area.get_o_braces_and_labels()
        dx_brs_and_labels=d_area.get_dx_braces_and_labels()
        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)

        v_line2=Line(self.coords_to_point(3.25,0), self.coords_to_point(3.25, self.func(3.25)), stroke_width=1.5).set_color(YELLOW)
        # dx line
        dx_line=Line(self.coords_to_point(3,0), self.coords_to_point(3.25,0))
        br_dx_line=Brace(dx_line,0.5*DOWN).add_background_rectangle().shift(0.1*UP)
        lab_dx_br=MathTex("dx").set_color(BLUE).scale(0.8).next_to(br_dx_line,0.15*DOWN).add_background_rectangle()
        br_lab_dx_line=VGroup(br_dx_line, lab_dx_br)

        # df(x)
        interim_point=Dot(radius=0).move_to(self.coords_to_point(3.25, self.func(3)))
        df_line=Line(interim_point, self.coords_to_point(3.25,self.func(3.25)), stroke_width=1.5).set_color(YELLOW)
        df_brace=Brace(df_line,0.5*RIGHT).shift(0.1*LEFT)
        df_label=MathTex("df").scale(0.8).set_color(YELLOW).next_to(df_brace,0.5*RIGHT)
        df_braces=VGroup(df_brace, df_label)

        # formula
        df_fl1=MathTex("df","=").move_to([0.5,1.5,0])
        df_fl1[0].set_color(YELLOW)
        bar1=d_area.dx_square_right.copy().next_to(df_fl1,RIGHT)
        plus=MathTex("+").next_to(bar1,RIGHT)
        bar2=d_area.dx_square_right.copy().next_to(plus,RIGHT)
        plus2=MathTex("+").next_to(bar2,RIGHT)
        dxdx=d_area.dxdx_square.copy().next_to(plus2,RIGHT)
        # formula continued
        br_bars=Brace(VGroup(bar1,plus,bar2),DOWN)
        lab_bars=MathTex("2x","(dx)")
        lab_bars[1].set_color(BLUE)
        lab_bars.add_background_rectangle().next_to(br_bars,DOWN)
        br_lab_bars=VGroup(br_bars, lab_bars)

        br_dxdx=Brace(dxdx,DOWN)
        lab_dxdx=MathTex("(dx)^2").set_color(BLUE).add_background_rectangle().next_to(br_dxdx,DOWN)
        br_lab_dxdx=VGroup(br_dxdx, lab_dxdx)

        self.add(self.axes, curve, lab_g ,areas, v_line, h_line, dot_m)
        self.play(ShowCreation(sub1), rate_func=linear, run_time=2)
        self.play(FadeOut(self.y_axis), FadeOut(h_line))
        self.play(
            x_value.set_value, 3.25,
            ShowCreation(dx_line),
            rate_func=linear,
            run_time=1.5,
            )
        self.play(ShowCreation(v_line2))
        self.play(
            x_value.set_value, 3,
            rate_func=linear,
            run_time=1.5,
            )

        self.play(ShowCreation(br_lab_dx_line))
        self.wait()
        self.add(
            d_area.original_square,
            d_area.x2_label,
            o_brs_and_labels,
            )
        self.remove(areas)

        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), rate_func=linear, run_time=2.5)

        self.play(
            FadeIn(d_area.dx_square_right),
            FadeIn(d_area.dx_square_down),
            FadeIn(d_area.dxdx_square),
            FadeIn(dx_brs_and_labels),
            o_brs_and_labels[2:].shift, 0.25*RIGHT,
            ) 
        
        self.play(
            ShowCreation(df_braces),
            dx_line.move_to, self.coords_to_point(3.125,self.func(3)),
            br_lab_dx_line.move_to, self.coords_to_point(3.125,7.5),
            d_area.dx_square_right.shift, 0.2*RIGHT,
            d_area.dx_square_down.shift, 0.2*DOWN,
            d_area.dxdx_square.shift, 0.2*DOWN+0.2*RIGHT,
            o_brs_and_labels[2:].shift, 0.2*RIGHT,
            dx_brs_and_labels[:2].shift, 0.2*RIGHT,
            dx_brs_and_labels[2:].shift, 0.2*DOWN+0.2*RIGHT,
            )
        self.wait()
        self.play(FadeOut(lab_g))
        self.play(ReplacementTransform(df_label.copy(), df_fl1))
        self.play(ReplacementTransform(d_area.dx_square_right.copy(), bar1))
        self.play(ShowCreation(plus))
        self.play(ReplacementTransform(d_area.dx_square_down.copy(), bar2))
        self.play(ShowCreation(br_lab_bars))
        self.play(ShowCreation(plus2))
        self.play(ReplacementTransform(d_area.dxdx_square.copy(),dxdx))
        self.play(ShowCreation(br_lab_dxdx))
        self.wait()

    def minimize_dx(self):
        areas=DerivativeSquaresAreaSplitted().move_to([-3,0,0])
        brs_labs=areas.get_braces_and_labels()
        # valuetracker
        dx_value=ValueTracker(0.25)
        # updaters
        areas.dx_square_right.add_updater(lambda x: x.become(
            Rectangle(
            width=dx_value.get_value(),
            height=3,
            color=YELLOW_E,
            fill_color=YELLOW_E,
            fill_opacity=1
            ).next_to(areas.original_square,RIGHT,buff=0).shift(0.2 *RIGHT)
            ))
        areas.dx_square_down.add_updater(lambda x: x.become(
            Rectangle(
            width=3,
            height=dx_value.get_value(),
            color=YELLOW_E,
            fill_color=YELLOW_E,
            fill_opacity=1
            ).next_to(areas.original_square,DOWN,buff=0).shift(0.2*DOWN)
            ))
        areas.dxdx_square.add_updater(lambda x: x.become(
            Rectangle(
            width=dx_value.get_value(),
            height=dx_value.get_value(),
            color=YELLOW_E,
            fill_color=YELLOW_E,
            fill_opacity=1
            ).next_to(areas.dx_square_right,DOWN,buff=0.2)
            ))
        areas.brace_down.add_updater(lambda x: x.become(Brace(areas.dx_square_down,DOWN)))
        areas.label_down.add_updater(lambda x: x.become(MathTex("x").set_color(WHITE).next_to(areas.brace_down, DOWN)))
        areas.brace_right.add_updater(lambda x: x.become(Brace(areas.dx_square_right,RIGHT)))
        areas.label_right.add_updater(lambda x: x.become(MathTex("x").set_color(WHITE).next_to(areas.brace_right, RIGHT)))
        areas.dx_brace_up.add_updater(lambda x: x.become(Brace(areas.dx_square_right,UP)))
        areas.dx_label_up.add_updater(lambda x: x.become(MathTex("dx").set_color(BLUE).next_to(areas.dx_brace_up, UP)))
        areas.dx_brace_right.add_updater(lambda x: x.become(Brace(areas.dxdx_square,RIGHT)))
        areas.dx_label_right.add_updater(lambda x: x.become(MathTex("dx").set_color(BLUE).next_to(areas.dx_brace_right, RIGHT)))
        # formula
        df_fl1=MathTex("df","=").move_to([1.5,0.,0])
        df_fl1[0].set_color(YELLOW)
        dx_right=Rectangle(
            width=dx_value.get_value(),height=3,color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(df_fl1).add_updater(lambda x: x.become(Rectangle(
            width=dx_value.get_value(),height=3,color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(df_fl1)))
        plus1=MathTex("+").next_to(dx_right).add_updater(lambda x:x.next_to(dx_right))
        dx_right2=Rectangle(
            width=dx_value.get_value(),height=3,color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(plus1).add_updater(lambda x: x.become(Rectangle(
            width=dx_value.get_value(),height=3,color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(plus1)))
        plus2=MathTex("+").next_to(dx_right2).add_updater(lambda x:x.next_to(dx_right2))
        dxdx_square=Rectangle(
            width=dx_value.get_value(),height=dx_value.get_value(),color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(plus2).add_updater(lambda x: x.become(Rectangle(
            width=dx_value.get_value(),height=dx_value.get_value(),color=YELLOW_E,fill_color=YELLOW_E,fill_opacity=1
            ).next_to(plus2)))

        self.add(areas, brs_labs, df_fl1, dx_right, plus1, dx_right2, plus2, dxdx_square)

        self.play(
            dx_value.set_value, 0.01,
            run_time=2.5
            )
        self.wait()

class PowerRuleAsVolume(GraphScene):
    CONFIG={
            "x_axis_width":5.5,
            "x_min":0,
            "x_max":3,
            "y_axis_height":5.5,
            "y_min":0,
            "y_max":30,
            "x_labeled_nums":[1,2,3],
            "y_labeled_nums":[5,10,15,20,25,30],
            "graph_origin":2.5 * DOWN + 0.75 * RIGHT,
            "x_axis_label":MathTex("x"),
            "y_axis_label":MathTex("y"),
            "y_tick_freq": 5,
            "x_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "y_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "stroke_width":2.5,
            "dot_radius":0.05,
            "func": lambda x: x**3,
            "d_func": lambda x: 3*x**2,
            "o_rec_color":BLUE_E,

    }

    def construct(self):
        #self.imagine_power_function_as_volume()
        #self.animate_volume_change_when_dx()
        self.minimize_dx()


    def imagine_power_function_as_volume(self):
        """subs"""
        sub=Text("関数ｆ(ｘ)＝ｘ^3は、このように立方体の体積として考えることができます。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        """objects"""
        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        label_g=MathTex("f(x)","=","x","{}^3").scale(0.8).move_to(self.coords_to_point(2.8,30))
        """x_value_tracker"""
        x_value=ValueTracker(2)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)
        h_line.add_updater(lambda x: x.become(Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)))
        # volume updater
        y=15*PI/180
        x=10*PI/180
        y_mat=[[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]]  #y軸周りに回転
        x_mat=[[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]]  #x軸周りに回転
        cube=DerivativeCubeVolume().to_corner(UL).shift(0.5*RIGHT+DOWN)
        cube.cube.add_updater(lambda x: x.become(Cube(
            fill_color=BLUE_E,
            stroke_color=WHITE,
            fill_opacity=0.75,
            stroke_width=0.5,
            side_length=x_value.get_value()
            ).apply_matrix(y_mat).apply_matrix(x_mat).to_corner(UL).shift(1.6*RIGHT+1.15*DOWN)))
        cube.br_cube.add_updater(lambda x: x.become(Brace(cube.cube,LEFT).scale(0.8).shift(0.1*UP)))
        cube.lab_cube.add_updater(lambda x: x.next_to(cube.br_cube,LEFT))


        self.add(
            self.axes, curve, label_g,
            dot_m,v_line,h_line,
            cube.cube, 
            )

        self.play(ShowCreation(sub), run_time=3, rate_func=linear)

        self.play(
            ShowCreation(cube.br_cube),
            ReplacementTransform(label_g[2].copy(), cube.lab_cube)
            )

        self.play(
            x_value.set_value, 3,
            rate_func=there_and_back,
            run_time=6,
            )

        self.play(
            x_value.set_value, 0.5,
            rate_func=there_and_back,
            run_time=6,
            )
        self.wait()

    def animate_volume_change_when_dx(self):
        """ sub """
        sub1=Text("ｘの値がｄｘ増加すると、その分だけ体積も増加します。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub2=Text("そして体積の増加分ｄｆはこれらの六面体の和になります。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        """objects"""
        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        label_g=MathTex("f(x)","=","x","{}^3").scale(0.8).move_to(self.coords_to_point(2.8,30))
        """x_value_tracker"""
        x_value=ValueTracker(2)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(self.coords_to_point(x_value.get_value(),0), dot_m, stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)
        h_line.add_updater(lambda x: x.become(Line(self.coords_to_point(0, self.func(x_value.get_value())), dot_m, stroke_width=1.5).set_color(BLUE)))
        # volume updater
        y=15*PI/180
        x=10*PI/180
        y_mat=[[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]]  #y軸周りに回転
        x_mat=[[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]]  #x軸周りに回転
        cube=DerivativeCubeVolume().to_corner(UL).shift(0.5*RIGHT+DOWN)
        cube.cube.add_updater(lambda x: x.become(Cube(
            fill_color=BLUE_E,
            stroke_color=WHITE,
            fill_opacity=0.75,
            stroke_width=0.5,
            side_length=x_value.get_value()
            ).apply_matrix(y_mat).apply_matrix(x_mat).to_corner(UL).shift(1.67*RIGHT+1.2*DOWN)))
        cube.br_cube.add_updater(lambda x: x.become(Brace(cube.cube,LEFT).scale(0.8).shift(0.1*UP)))
        cube.lab_cube.add_updater(lambda x: x.next_to(cube.br_cube,LEFT))

        new_cube=DerivativeCubeVolume().to_corner(UL).shift(0.5*RIGHT+DOWN)
        # dx
        dx_line=Line(self.coords_to_point(2,0), self.coords_to_point(2.25,0))
        br_dx_line=Brace(dx_line,DOWN).shift(0.1*UP).add_background_rectangle()
        lab_dx_line=MathTex("dx").scale(0.8).set_color(BLUE).next_to(br_dx_line,0.5*DOWN).add_background_rectangle()
        br_lab_dx=VGroup(br_dx_line, lab_dx_line)
        dx_v_line=Line(self.coords_to_point(2.25, 0), self.coords_to_point(2.25, self.func(2.25)), color=YELLOW,stroke_width=1.5)
        br_df=BraceBetweenPoints(self.coords_to_point(2.25, self.func(2)), self.coords_to_point(2.25, self.func(2.25)),0.5*RIGHT)
        lab_df=MathTex("df").scale(0.8).set_color(YELLOW).next_to(br_df,0.5*RIGHT)
        br_lab_df=VGroup(br_df, lab_df)
        # formula
        df1=MathTex("df","=").move_to([0.5,2,0])
        df1[0].set_color(YELLOW)
        cube1=Prism(
            dimensions=[2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            )
        cube2=Prism(
            dimensions=[2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.2,0,0])
        cube3=Prism(
            dimensions=[2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.4,0,0])
        cubes=VGroup(cube1,cube2,cube3).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(df1,RIGHT)
        plus=MathTex("+").next_to(cubes,RIGHT)
        bar1=Prism(
            dimensions=[0.2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            )
        bar2=Prism(
            dimensions=[0.2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.35,0,0])
        bar3=Prism(
            dimensions=[0.2,2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.7,0,0])
        bars=VGroup(bar1,bar2,bar3).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(plus,RIGHT)
        plus2=MathTex("+").next_to(bars,RIGHT)
        dx_cube=Prism(
            dimensions=[0.2,0.2,0.2],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(plus2,RIGHT)
        # formula continued
        br1=Brace(cubes,DOWN)
        lab_br1=MathTex("3","x^2","(dx)").next_to(br1,DOWN)
        lab_br1[2].set_color(BLUE)
        lab_br1.add_background_rectangle()
        br1s=VGroup(br1, lab_br1)
        br2=Brace(bars,DOWN)
        lab_br2=MathTex("3","x","(dx)^2").next_to(br2,DOWN)
        lab_br2[2].set_color(BLUE)
        lab_br2.add_background_rectangle()
        br2s=VGroup(br2, lab_br2)
        br3=Brace(dx_cube,DOWN)
        lab_br3=MathTex("(dx)^3").set_color(BLUE).next_to(br3,DOWN).add_background_rectangle()
        br3s=VGroup(br3, lab_br3)


        self.add(
            self.axes, curve, label_g,
            dot_m,v_line,h_line,
            cube.cube, cube.br_cube, cube.lab_cube
            )
        self.play(ShowCreation(sub1), run_time=2.5, rate_func=linear)

        self.play(
            ShowCreation(dx_line),
            x_value.set_value, 2.25,
            rate_func=smooth,
            run_time=2,
            )
        self.add(dx_v_line)
        self.play(
            x_value.set_value, 2,
            rate_func=smooth,
            run_time=2,        )
        self.play(
            ShowCreation(br_lab_dx),
            )
        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), run_time=2.5, rate_func=linear)
        self.play(
            dx_line.move_to, self.coords_to_point(2.125, 8),
            br_lab_dx.move_to, self.coords_to_point(2.125, 6),
            )
        h_line.clear_updaters()
        cube.cube.clear_updaters()
        cube.br_cube.clear_updaters()
        cube.lab_cube.clear_updaters()
        self.play(
            ShowCreation(br_lab_df),
            ReplacementTransform(cube.cube, new_cube.cube),
            ReplacementTransform(cube.br_cube, new_cube.br_cube),
            ReplacementTransform(cube.lab_cube, new_cube.lab_cube),
            ShowCreation(new_cube.cube_f),
            ShowCreation(new_cube.cube_r),
            ShowCreation(new_cube.cube_t),
            ShowCreation(new_cube.bar_f),
            ShowCreation(new_cube.bar_r),
            ShowCreation(new_cube.bar_t),
            ShowCreation(new_cube.cube_dx),
            ShowCreation(new_cube.br_cube_t),
            ShowCreation(new_cube.lab_cube_t),
            )
        self.bring_to_back(new_cube.cube)
        self.play(
            new_cube.cube_f.shift, 0.2*DOWN+0.2*RIGHT,
            new_cube.cube_t.shift, 0.5*UP,
            new_cube.cube_r.shift, 0.8*RIGHT,
            new_cube.bar_f.shift, 0.25*UP+0.25*RIGHT,
            new_cube.bar_t.shift, 0.5*UP+0.8*RIGHT,
            new_cube.bar_r.shift, 1.2*RIGHT,
            new_cube.cube_dx.shift, 0.2*UP+1.2*RIGHT,
            new_cube.br_cube_t.shift, 0.5*UP,
            new_cube.lab_cube_t.shift, 0.5*UP,
            )

        self.play(
            FadeOut(self.y_axis),
            FadeOut(h_line),
            FadeOut(label_g),
            )

        self.play(
            ReplacementTransform(lab_df.copy(),df1),
            )
        self.play(
            ReplacementTransform(VGroup(new_cube.cube_f.copy(),new_cube.cube_r.copy(),new_cube.cube_t.copy()),cubes)
            )
        self.play(ShowCreation(br1s))
        self.play(
            ShowCreation(plus),
            ReplacementTransform(VGroup(new_cube.bar_f.copy(),new_cube.bar_r.copy(),new_cube.bar_t.copy()),bars)
            )
        self.play(ShowCreation(br2s))
        self.play(
            ShowCreation(plus2),
            ReplacementTransform(new_cube.cube_dx,dx_cube)
            )
        self.play(ShowCreation(br3s))

        self.wait()

    def minimize_dx(self):
        y=15*PI/180
        x=10*PI/180
        y_mat=[[math.cos(y),0,math.sin(y)],[0,1,0],[-math.sin(y),0,math.cos(y)]]  #y軸周りに回転
        x_mat=[[1,0,0],[0,math.cos(x),-math.sin(x)],[0,math.sin(x),math.cos(x)]]  #x軸周りに回転
        t=0.001

        cube=DerivativeCubeVolumeSplitted(added_cubes_kwargs={"thickness":t}).shift(3.5*LEFT)
        cube.lab_cube_t.shift(0.5*UP)

        df1=MathTex("df","=").move_to([1,0,0])
        df1[0].set_color(YELLOW)
        cube1=Prism(
            dimensions=[2,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            )
        cube2=Prism(
            dimensions=[2,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.5,-0.5,0])
        cube3=Prism(
            dimensions=[2,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([1,-1,0])
        cubes=VGroup(cube1,cube2,cube3).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(df1,RIGHT)
        plus=MathTex("+").next_to(cubes,RIGHT)
        bar1=Prism(
            dimensions=[t,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            )
        bar2=Prism(
            dimensions=[t,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.35,0,0])
        bar3=Prism(
            dimensions=[t,2,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).move_to([0.7,0,0])
        bars=VGroup(bar1,bar2,bar3).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(plus,RIGHT)
        plus2=MathTex("+").next_to(bars,RIGHT)
        dx_cube=Prism(
            dimensions=[t,t,t],
            fill_opacity=0.4,
            fill_color=YELLOW_E,
            color=YELLOW,
            stroke_width=0.5,
            ).apply_matrix(y_mat).apply_matrix(x_mat).scale(0.8).next_to(plus2,RIGHT)


        self.add(cube, df1, cubes, plus, bars, plus2, dx_cube)

class PowerRuleNegative(GraphScene):
    CONFIG={
            "x_axis_width":15,
            "x_min":0,
            "x_max":5,
            "y_axis_height":9,
            "y_min":0,
            "y_max":3,
            "x_labeled_nums":[1,2,3,4,5],
            "y_labeled_nums":[1,2,],
            "graph_origin":2.5 * DOWN + 6 * LEFT,
            "x_axis_label":None,
            "y_axis_label":None,
            "x_tick_freq": 0.5,
            "y_tick_freq": 0.5,
            "x_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "y_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "stroke_width":2.5,
            "dot_radius":0.05,
            "func": lambda x: x**-1,
            "d_func": lambda x: -1*x**-2,
            "o_rec_color":BLUE_E,

    }
    def construct(self):
        #self.visualize_negative_power()
        self.what_happens_when_dx()


    def visualize_negative_power(self):
        """subtitles"""
        sub1=Text("関数ｘ^-1は、このように面積が常に１の長方形でイメージできます。").scale(0.55).move_to([0,-3.5,0])
        """setup"""
        axes=self.setup_axes()
        lab_g=MathTex("f(x)=\\dfrac{1}{x}").move_to(self.coords_to_point(1.3,1.8))
        """valuetracker"""
        # x conter
        x_value=ValueTracker(1)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        x_counter.add_updater(lambda m: m.set_value(x_value.get_value()))
        # 1/x counter
        y_counter=DecimalNumber(1/x_value.get_value(), num_decimal_places=2)
        y_counter.add_updater(lambda m: m.set_value(1/x_value.get_value()))
        # area objects
        area=Polygon(
            self.graph_origin,
            self.coords_to_point(0,1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),0),
            stroke_width=1,
            fill_color=BLUE,
            color=GREY,
            fill_opacity=0.4,
            ).add_updater(lambda x: x.become(Polygon(
            self.graph_origin,
            self.coords_to_point(0,1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),0),
            stroke_width=1,
            fill_color=BLUE,
            color=GREY,
            fill_opacity=0.4,
            )))
        br_right=Brace(area,RIGHT).add_updater(lambda x: x.become(Brace(area,RIGHT)))
        lab_right=MathTex("\\dfrac{1}{x}").next_to(br_right,RIGHT).add_updater(lambda x: x.next_to(br_right,RIGHT))
        br_lab_r=VGroup(br_right, lab_right)
        br_u=Brace(area,UP).add_updater(lambda x: x.become(Brace(area,UP)))
        lab_u=MathTex("x").next_to(br_u,UP).add_updater(lambda x: x.next_to(br_u,UP))
        br_lab_u=VGroup(br_u, lab_u)
        lab_area=MathTex("1").move_to(area).add_updater(lambda x: x.move_to(area))
        # curve
        curve=self.get_graph(self.func)

        self.add(self.axes)
        self.play(ShowCreation(sub1), run_time=2, rate_func=linear)
        self.play(ShowCreation(area))
        self.play(ShowCreation(br_lab_r), ShowCreation(br_lab_u), ShowCreation(lab_area))
        self.play(x_value.set_value, 3)
        self.play(x_value.set_value, 0.01)
        self.play(
            x_value.set_value, 5,
            ShowCreation(curve),
            run_time=2
            )
        self.bring_to_back(curve)
        self.play(x_value.set_value, 1.2)
        self.play(ShowCreation(lab_g))
        self.wait()

    def what_happens_when_dx(self):
        """subtitles"""
        sub1=Text("ｘがｄｘだけ変化すると、この長方形は次のように変化します。").scale(0.55).move_to([0,-3.5,0])
        sub2=Text("具体的には横の長さがｄｘ増加し、高さがｄ(1/ｘ)減少します。").scale(0.55).move_to([0,-3.5,0])
        sub3=Text("なお増加面積と減少面積は常に釣り合います。").scale(0.55).move_to([0,-3.5,0])
        sub4=Text("この高さの減少を横の長さの増加で割ったものが微分です。").scale(0.55).move_to([0,-3.5,0])
        """setup"""
        axes=self.setup_axes()
        lab_g=MathTex("f(x)=\\dfrac{1}{x}").move_to(self.coords_to_point(1.3,1.8))
        curve=self.get_graph(self.func)
        d_curve=self.get_graph(self.d_func)
        """valuetracker"""
        # x conter
        x_value=ValueTracker(1.2)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        x_counter.add_updater(lambda m: m.set_value(x_value.get_value()))
        # 1/x counter
        y_counter=DecimalNumber(1/x_value.get_value(), num_decimal_places=2)
        y_counter.add_updater(lambda m: m.set_value(1/x_value.get_value()))
        # area objects
        area=Polygon(
            self.graph_origin,
            self.coords_to_point(0,1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),0),
            stroke_width=1,
            fill_color=BLUE,
            color=GREY,
            fill_opacity=0.4,
            ).add_updater(lambda x: x.become(Polygon(
            self.graph_origin,
            self.coords_to_point(0,1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),0),
            stroke_width=1,
            fill_color=BLUE,
            color=GREY,
            fill_opacity=0.4,
            )))
        br_right=Brace(area,RIGHT).add_updater(lambda x: x.become(Brace(area,RIGHT)))
        lab_right=MathTex("\\dfrac{1}{x}").scale(0.9).next_to(br_right,RIGHT).add_updater(lambda x: x.next_to(br_right,RIGHT))
        br_lab_r=VGroup(br_right, lab_right)
        br_u=Brace(area,UP).add_updater(lambda x: x.become(Brace(area,UP)))
        lab_u=MathTex("x").next_to(br_u,UP).add_updater(lambda x: x.next_to(br_u,UP))
        br_lab_u=VGroup(br_u, lab_u)
        lab_area=MathTex("1").scale(0.65).move_to(area).add_updater(lambda x: x.move_to(area))

        """dx objects"""
        # dx
        dx_line=Line(self.coords_to_point(1.2,0), self.coords_to_point(1.35,0))
        dx_rec1=Polygon(
            self.graph_origin,
            self.coords_to_point(0,1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),1/x_value.get_value()),
            self.coords_to_point(x_value.get_value(),0),
            stroke_width=1,
            fill_color=BLUE,
            color=BLUE_E,
            fill_opacity=0.2,
            )
        dx_rec2=Polygon(
            self.graph_origin,
            self.coords_to_point(0, 1/(x_value.get_value()+0.15)),
            self.coords_to_point(x_value.get_value()+0.15,1/(x_value.get_value()+0.15)),
            self.coords_to_point(x_value.get_value()+0.15,0),
            stroke_width=1,
            fill_color=BLUE,
            color=BLUE_E,
            fill_opacity=0.2,
            )
        dx_rec=VGroup(dx_rec1, dx_rec2)
        # new br and labs
        new_br_r=Brace(area,RIGHT).shift(0.45*RIGHT)
        new_lab_r=MathTex("\\dfrac{1}{x}").scale(0.9).next_to(new_br_r,RIGHT)
        new_br_lab_r=VGroup(new_br_r,new_lab_r)
        new_br_u=Brace(dx_rec1,UP)
        new_lab_u=MathTex("x").next_to(new_br_u,UP)
        new_br_lab_u=VGroup(new_br_u,new_lab_u)
        # dx labels
        """
        "dash_length": 0.1,
        "dash_spacing": None,
        "positive_space_ratio": 0.5,
        """
        dx_l1=DashedLine(self.coords_to_point(1.2, 0), self.coords_to_point(1.2,1), color=BLUE, dash_length=0.05)
        dx_l2=DashedLine(self.coords_to_point(1.35, 0), self.coords_to_point(1.35,1), color=BLUE, dash_length=0.05)
        dx_ls=VGroup(dx_l1,dx_l2)
        dx_brace=BraceBetweenPoints(self.coords_to_point(1.2,1), self.coords_to_point(1.35,1), UP)
        dx_lab=MathTex("dx").next_to(dx_brace,UP).set_color(BLUE)
        dx_braces=VGroup(dx_brace,dx_lab)

        dx_lr1=DashedLine(self.coords_to_point(0,1/1.35), self.coords_to_point(1.5,1/1.35), color=YELLOW, dash_length=0.05)
        dx_lr2=DashedLine(self.coords_to_point(0,1/1.2), self.coords_to_point(1.5,1/1.2), color=YELLOW, dash_length=0.05)
        dx_lrs=VGroup(dx_lr1, dx_lr2)
        dx_brace_r=BraceBetweenPoints(self.coords_to_point(1.5,1/1.35), self.coords_to_point(1.5,1/1.2), RIGHT)
        dx_lab_r=MathTex("d(\\dfrac{1}{x})").scale(0.85).next_to(dx_brace_r,RIGHT).set_color(YELLOW)
        dx_brace_rs=VGroup(dx_brace_r, dx_lab_r)

        # colored area
        area_g=Polygon(
            self.coords_to_point(1.2,0),
            self.coords_to_point(1.35,0),
            self.coords_to_point(1.35,1/1.35),
            self.coords_to_point(1.2,1/1.35),
            color=GREEN,
            fill_color=GREEN,
            stroke_width=1,
            fill_opacity=1,
            )
        area_r=Polygon(
            self.coords_to_point(0,1/1.35),
            self.coords_to_point(0,1/1.2),
            self.coords_to_point(1.2, 1/1.2),
            self.coords_to_point(1.2,1/1.35),
            color=RED_C,
            fill_color=RED_C,
            stroke_width=1,
            fill_opacity=1,
            )
        lab_area_g=Text("増加した面積").scale(0.5).move_to(self.coords_to_point(0.7,0.15))
        line_area_g=Arrow(lab_area_g.get_right(), area_g.get_center(), buff=0.1, stroke_width=2)
        lab_line_g=VGroup(lab_area_g,line_area_g)
        lab_area_r=Text("減少した面積").scale(0.5).move_to(self.coords_to_point(0.4,0.55))
        line_area_r=Arrow(lab_area_r.get_top(), area_r.get_center(), buff=0.1, stroke_width=2)
        lab_line_r=VGroup(lab_area_r,line_area_r)

        #formula
        dfdx=Fraction(num=MathTex("dy").set_color(YELLOW), denom=MathTex("dx").set_color(BLUE)).move_to([1,2.9,0])
        equal1=MathTex("=").next_to(dfdx,RIGHT)
        dfdx2=MathTex("d(\\frac{1}{x})","\\cdot","\\frac{1}{dx}").next_to(equal1,RIGHT)
        dfdx2[0].set_color(YELLOW)
        dfdx2[2].set_color(BLUE)
        equal2=MathTex("=").next_to(equal1,5.3*DOWN)
        dfdx3=MathTex("(\\frac{1}{x+dx}-\\frac{1}{x})","\\cdot", "\\frac{1}{dx}").next_to(equal2,RIGHT)
        dfdx3[0].set_color(YELLOW)
        dfdx3[2].set_color(BLUE)
        equal3=MathTex("=").next_to(equal2,5.3*DOWN)
        dfdx4=MathTex("\\frac{dx}{x(x+dx)}","\\cdot","\\frac{1}{dx}").next_to(equal3,RIGHT)
        dfdx4[0].set_color(YELLOW)
        dfdx4[2].set_color(BLUE)
        dfdx4s=VGroup(equal3, dfdx4)
        equal4=MathTex("=").next_to(equal3, 5.3*DOWN)
        dfdx5=MathTex("-\\frac{1}{x^2}").next_to(equal4,RIGHT).set_color(LIGHT_PINK)
        dfdx5s=VGroup(equal4,dfdx5).add_background_rectangle()
        


        




        self.add(self.axes, curve, area, br_lab_r, br_lab_u, lab_area, lab_g)
        self.play(ShowCreation(sub1), run_time=2, rate_func=linear)
        self.play(
            ShowCreation(dx_line),
            x_value.set_value, 1.35,
            run_time=1)
        self.play(x_value.set_value, 1.2, run_time=1)
        area.clear_updaters()
        br_lab_r.clear_updaters()
        br_lab_u.clear_updaters()
        self.play(
            ReplacementTransform(area, dx_rec),
            ReplacementTransform(br_lab_r, new_br_lab_r),
            ReplacementTransform(br_lab_u, new_br_lab_u),
            )
        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), run_time=2, rate_func=linear)
        self.play(ShowCreation(dx_ls))
        self.play(ShowCreation(dx_braces))
        self.play(ShowCreation(dx_lrs))
        self.play(ShowCreation(dx_brace_rs))
        self.play(FadeOut(sub2))
        self.play(ShowCreation(sub3), run_time=1.75, rate_func=linear)
        self.play(ShowCreation(area_g), ShowCreation(lab_line_g), ShowCreation(area_r), ShowCreation(lab_line_r))
        self.wait()
        self.play(FadeOut(area_g), FadeOut(lab_line_g), FadeOut(area_r), FadeOut(lab_line_r), FadeOut(sub3))
        self.play(ShowCreation(sub4), run_time=2.5, rate_func=linear)
        self.play(ShowCreation(dfdx))
        self.play(
            ShowCreation(equal1),
            ShowCreation(dfdx2[1]),
            ReplacementTransform(dx_lab.copy(), dfdx2[0]),
            ReplacementTransform(dx_lab_r.copy(), dfdx2[2]),
            )
        self.play(
            ShowCreation(equal2),
            ShowCreation(dfdx3)
            )
        self.play(ShowCreation(dfdx4s))
        self.play(ShowCreation(dfdx5s))
        
        self.wait()

class PowerRuleRoot(GraphScene):
    CONFIG={
            "x_axis_width":5.5,
            "x_min":0,
            "x_max":5,
            "y_axis_height":5.5,
            "y_min":0,
            "y_max":5,
            "x_labeled_nums":[1,2,3,4,5],
            "y_labeled_nums":[1,2,3,4,5],
            "graph_origin":2.5 * DOWN + 0.75 * RIGHT,
            "x_axis_label":MathTex("x"),
            "y_axis_label":MathTex("y"),
            "y_tick_freq": 1,
            "x_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "y_axis_config":{"numbers_with_elongated_ticks":[], "number_scale_val":0.5,},
            "stroke_width":2.5,
            "dot_radius":0.05,
            "func": lambda x: x**(1/2),
            "d_func": lambda x: 1_2*x**(-1/2),
            "o_rec_color":BLUE_E,

    }
    def construct(self):
        #self.imagine_as_area_of_square()
        self.what_happens_when_dx()

        """
        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        d_curve=self.get_graph(self.d_func)

        squares=DerivativeSquaresArea().to_corner(UL).shift(DOWN)
        o_brs_labs=squares.get_o_braces_and_labels(label="\\sqrt{x}")

        dx_brs_labs=squares.get_dx_braces_and_labels(label="d\\sqrt{x}")
        self.add(self.axes, curve)
        self.add(squares.original_square, o_brs_labs)
        """


    def imagine_as_area_of_square(self):
        """ sub """
        sub1=Text("関数ｆ(ｘ)＝ｘ^(１/２）は面積がｘの正方形の辺としてイメージできます。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub2=Text("ｘが大きくなれば辺の長さも伸び、小さくなれば辺の長さも短くなります。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        lab_g=MathTex("f(x)","=","x","{}^{\\frac{1}{2}}").scale(0.8).move_to(self.coords_to_point(4,5))
        # x_value
        x_value=ValueTracker(2.5)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # area
        area=Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        area.add_updater(lambda x: x.become(Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=self.o_rec_color,fill_color=self.o_rec_color,fill_opacity=1,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)))
        br_u=Brace(area,0.5*UP).add_updater(lambda x: x.become(Brace(area,0.5*UP)))
        br_r=Brace(area,0.5*RIGHT).add_updater(lambda x: x.become(Brace(area,0.5*RIGHT)))
        lab_u=MathTex("\\sqrt{x}").scale(0.8).next_to(br_u,0.5*UP).add_updater(lambda x: x.become(MathTex("\\sqrt{x}").scale(0.8).next_to(br_u,0.5*UP)))
        lab_r=MathTex("\\sqrt{x}").scale(0.8).next_to(br_r,0.5*RIGHT).add_updater(lambda x: x.become(MathTex("\\sqrt{x}").scale(0.8).next_to(br_r,0.5*RIGHT)))
        lab_x2=MathTex("x").scale(0.8).move_to(area).add_updater(lambda x: x.become(MathTex("x").scale(0.8).move_to(area)))
        areas=VGroup(area, br_u, br_r, lab_u, lab_r, lab_x2)

        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(dot_m, self.coords_to_point(x_value.get_value(),0), stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(dot_m, self.coords_to_point(x_value.get_value(),0), stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(dot_m, self.coords_to_point(0, self.func(x_value.get_value())), stroke_width=1.5).set_color(BLUE)
        h_line.add_updater(lambda x: x.become(Line(dot_m, self.coords_to_point(0, self.func(x_value.get_value())),  stroke_width=1.5).set_color(BLUE)))


        self.add(self.axes, curve, lab_g ,area, v_line, h_line,dot_m)
        self.play(ShowCreation(sub1), run_time=2, rate_func=linear)
        self.play(
            ReplacementTransform(lab_g[2].copy(),lab_u),
            ShowCreation(br_u),
            )
        self.play(
            ReplacementTransform(lab_g[2].copy(),lab_r),
            ShowCreation(br_r),
            )
        self.play(ShowCreation(lab_x2))
        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), run_time=2, rate_func=linear)
        self.play(
            x_value.set_value, 5,
            rate_func=smooth,
            run_time=2
            )
        self.play(
            x_value.set_value, 1,
            rate_func=smooth,
            run_time=3
            )
        self.play(
            x_value.set_value, 2.5,
            rate_func=smooth,
            run_time=2
            )

        self.wait()

    def what_happens_when_dx(self):
        """subs"""
        sub1=Text("ｘがｄｘ増加すると、このように辺の長さと面積が増加します。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub2=Text("増加した面積がｄｘ、増加した辺の長さがｄ(ｘ^1/2)に該当します。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()
        sub3=Text("この辺の長さの増加分を面積の増加分で割ったものがｘ^1/2の微分です。").scale(0.55).move_to([0,-3.5,0]).add_background_rectangle()

        """setup"""
        axes=self.setup_axes()
        curve=self.get_graph(self.func)
        lab_g=MathTex("f(x)","=","x","{}^{\\frac{1}{2}}").scale(0.8).move_to(self.coords_to_point(4,5))
        # x_value
        x_value=ValueTracker(2.5)
        x_counter=DecimalNumber(x_value.get_value(), num_decimal_places=2)
        # area
        area=Rectangle(width=x_value.get_value(),height=x_value.get_value(),color=WHITE,fill_color=WHITE,fill_opacity=0.2,).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        d_area=DerivativeSquaresArea(
            original_square_kwargs={"label":"x", "width":2.5, "height":2.5},
            dx_square_right_kwargs={"width":0.2, "height":2.5},
            dx_square_down_kwargs={"width":2.5, "height":0.2},
            dxdx_square_kwargs={"width":0.2, "height":0.2},
            ).to_corner(UL).shift(0.5*RIGHT+1.05*DOWN)
        o_brs_labs=d_area.get_o_braces_and_labels(label="\\sqrt{x}")

        dx_brs_labs=d_area.get_dx_braces_and_labels(label="d(\\sqrt{x})")

        # a dot moving along the curve
        dot_m=Dot(radius=0.05).move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value())))
        dot_m.add_updater(lambda x: x.move_to(self.coords_to_point(x_value.get_value(),self.func(x_value.get_value()))))
        v_line=Line(dot_m, self.coords_to_point(x_value.get_value(),0), stroke_width=1.5).set_color(YELLOW)
        v_line.add_updater(lambda x: x.become(Line(dot_m, self.coords_to_point(x_value.get_value(),0), stroke_width=1.5).set_color(YELLOW)))
        h_line=Line(dot_m, self.coords_to_point(0, self.func(x_value.get_value())), stroke_width=1.5).set_color(BLUE)
        h_line.add_updater(lambda x: x.become(Line(dot_m, self.coords_to_point(0, self.func(x_value.get_value())),  stroke_width=1.5).set_color(BLUE)))

        #dx
        dx_line=Line(self.coords_to_point(2.5,0), self.coords_to_point(2.7,0))
        lab_dx_line=MathTex("dx").scale(0.8).set_color(YELLOW).next_to(dx_line,DOWN).shift(0.1*UP).add_background_rectangle()
        h_line2=Line(self.coords_to_point(0,self.func(2.7)), self.coords_to_point(2.7, self.func(2.7)), stroke_width=1.5).set_color(BLUE)
        v_line2=Line(self.coords_to_point(2.7,0), self.coords_to_point(2.7, self.func(2.7)), stroke_width=1.5).set_color(YELLOW)

        df_line=Line(self.coords_to_point(0,self.func(2.5)), self.coords_to_point(0, self.func(2.7)))
        lab_df_line=MathTex("d(\\sqrt{x})").scale(0.8).next_to(df_line,LEFT).shift(0.1*RIGHT).add_background_rectangle()

        #formulas
        fm1=Fraction(num=MathTex("d(\\sqrt{x})"), denom=MathTex("dx").set_color(YELLOW))
        equal1=MathTex("=").next_to(fm1,1.5*RIGHT)
        fm2=Fraction(num=MathTex("d(\\sqrt{x})"), denom=MathTex("2","(d\\sqrt{x})","(\\sqrt{x})").set_color(YELLOW)).next_to(equal1,1.5*RIGHT)
        equal2=MathTex("=").next_to(equal1,6.5*DOWN)
        fm3=Fraction(num=MathTex("1"), denom=MathTex("2(\\sqrt{x})")).set_color(LIGHT_PINK).next_to(equal2,1.5*RIGHT)
        formula=VGroup(fm1, equal1, fm2, equal2, fm3).shift(1*RIGHT+2.4*UP)



        self.add(self.axes, curve, lab_g, d_area.original_square, d_area.x2_label, o_brs_labs, dot_m, v_line, h_line)
        self.play(ShowCreation(sub1), run_time=2, rate_func=linear)
        self.play(
            FadeIn(d_area.dx_square_right),
            FadeIn(d_area.dx_square_down),
            FadeIn(d_area.dxdx_square),
            ShowCreation(dx_line),
            ShowCreation(df_line),
            o_brs_labs[2:].shift, 0.2*RIGHT,
            x_value.set_value, 2.7,
            run_time=2)
        self.add(h_line2, v_line2)
        self.play(
            x_value.set_value, 2.5,
            run_time=2)
        self.play(FadeOut(sub1))
        self.play(ShowCreation(sub2), run_time=2, rate_func=linear)
        self.play(ShowCreation(lab_df_line),ShowCreation(lab_dx_line))
        self.play(
            ReplacementTransform(lab_df_line[1].copy(),dx_brs_labs[1]),
            ReplacementTransform(lab_df_line[1].copy(),dx_brs_labs[3]),
            ShowCreation(dx_brs_labs[0]),
            ShowCreation(dx_brs_labs[2]),
            )
        self.play(
            d_area.dx_square_right.shift, 0.2*RIGHT,
            d_area.dx_square_down.shift, 0.2*DOWN,
            d_area.dxdx_square.shift, 0.2*DOWN+0.2*RIGHT,
            o_brs_labs[2:].shift, 0.2*RIGHT,
            dx_brs_labs[:2].shift, 0.2*RIGHT,
            dx_brs_labs[2:].shift, 0.2*DOWN+0.2*RIGHT,
            )
        self.play(FadeOut(sub2))
        self.play(ShowCreation(sub3), run_time=2.5, rate_func=linear)
        self.play(FadeOut(self.y_axis), FadeOut(lab_g))
        self.play(
            ShowCreation(fm1.div_line),
            ReplacementTransform(VGroup(d_area.dx_square_down, d_area.dx_square_right, d_area.dxdx_square).copy(),fm1.denominator),
            ReplacementTransform(VGroup(dx_brs_labs[1], dx_brs_labs[3]).copy(), fm1.numerator)
            )
        self.play(ShowCreation(equal1), ShowCreation(fm2))
        self.play(ShowCreation(equal2), ShowCreation(fm3))
        self.wait()



class Subtitle(VGroup):
    CONFIG={
        "sub1":Text("字幕"),
        "sub2":Text("字幕"),
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
        self.s2=self.sub2.next_to(self.s1, 1*RIGHT)
        self.sub=VGroup(self.s1, self.s2,).move_to([self.position]).scale(0.55).add_background_rectangle()
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

class DerivativeSquaresArea(VGroup):
    """
    In manim, CONFIG is an dictionary cotaining useful variables for the Class and SubClasses.
    CONFIG values are called digest_config() method, the method of Container class.
    If we make a class extending scene or mobject, the digest_config() method is run
    and look for self.CONFIG values and make own variables for the class,
    and then goes to the parent class and looks for self.CONFIG there and adds those entries into the variables. 
    If there is the same keys already, it ignores the values from the parent class. 
    """
    CONFIG={
    "original_square_kwargs":{
        "label": "x",
        "width":3,
        "height":3,
        "color":BLUE_E,
        "fill_color":BLUE_E,
        "fill_opacity":1,
        },
    "dx_square_right_kwargs":{
        "width":0.25,
        "height":3,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    "dx_square_down_kwargs":{
        "width":3,
        "height":0.25,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    "dxdx_square_kwargs":{
        "width":0.25,
        "height":0.25,
        "color":YELLOW_E,
        "fill_color":YELLOW_E,
        "fill_opacity":1,
        },
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.original_square=Rectangle(**self.original_square_kwargs)
        self.dx_square_right=Rectangle(**self.dx_square_right_kwargs).next_to(self.original_square,RIGHT,buff=0)
        self.dx_square_down=Rectangle(**self.dx_square_down_kwargs).next_to(self.original_square,DOWN,buff=0)
        self.dxdx_square=Rectangle(**self.dxdx_square_kwargs).next_to(self.dx_square_right,DOWN,buff=0)
        self.x2_label=MathTex(self.original_square_kwargs["label"]).scale(0.8).move_to(self.original_square)
        self.add(self.original_square, self.dx_square_right, self.dx_square_down, self.dxdx_square, self.x2_label)

    def get_o_braces_and_labels(self, label_color1=BLUE, label_color2=YELLOW, label="x"):
        self.brace_up=Brace(self.original_square,0.5*UP)
        self.label_up=MathTex(label).scale(0.8).next_to(self.brace_up, 0.5*UP)
        self.brace_right=Brace(self.original_square,0.5*RIGHT)
        self.label_right=MathTex(label).scale(0.8).next_to(self.brace_right, 0.5*RIGHT)
        self.o_braces=VGroup(self.brace_up, self.label_up, self.brace_right, self.label_right)
        return self.o_braces

    def get_dx_braces_and_labels(self, label="dx", color=WHITE):
        self.dx_brace_up=Brace(self.dx_square_right,UP)
        self.dx_label_up=MathTex(label).scale(0.8).set_color(color).next_to(self.dx_brace_up, UP)
        self.dx_brace_right=Brace(self.dxdx_square,RIGHT)
        self.dx_label_right=MathTex(label).scale(0.8).set_color(color).next_to(self.dx_brace_right, RIGHT)


        self.dx_braces_and_labels=VGroup(
            self.dx_brace_up, self.dx_label_up, self.dx_brace_right, self.dx_label_right
            )
        return self.dx_braces_and_labels

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
        self.dx_square_down.shift(self.kwargs["split_factor"]*DOWN)
        self.dxdx_square.shift(self.kwargs["split_factor"]*DOWN+self.kwargs["split_factor"]*RIGHT)
        self.add(self.original_square, self.dx_square_right, self.dx_square_down, self.dxdx_square)

    def get_dx_areas(self):
        return VGroup(self.dx_square_right,down)

    def get_braces_and_labels(self, label_color1=WHITE, label_color2=BLUE):
        self.brace_down=Brace(self.dx_square_down,DOWN)
        self.label_down=MathTex("x").set_color(label_color1).next_to(self.brace_down, DOWN)
        self.brace_right=Brace(self.dx_square_right,RIGHT)
        self.label_right=MathTex("x").set_color(label_color1).next_to(self.brace_right, RIGHT)
        self.dx_brace_up=Brace(self.dx_square_right,UP)
        self.dx_label_up=MathTex("dx").set_color(label_color2).next_to(self.dx_brace_up, UP)
        self.dx_brace_right=Brace(self.dxdx_square,RIGHT)
        self.dx_label_right=MathTex("dx").set_color(label_color2).next_to(self.dx_brace_right, RIGHT)


        self.braces_and_labels=VGroup(
            self.brace_down, self.label_down, self.brace_right, self.label_right,
            self.dx_brace_up, self.dx_label_up, self.dx_brace_right, self.dx_label_right
            )
        return self.braces_and_labels

class DerivativeCubeVolume(VGroup):
    CONFIG={
        "original_cube_kwargs":{
            "color":BLUE_E,
            "stroke_color":WHITE,
            "opacity":0.75,
            "stroke_width":0.5,
            "side_length": 2,
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
            "label_color":WHITE,
            },
        "brace_and_label_kwargs_for_dx_cube":{
            "brace_color":WHITE,
            "label_color":BLUE,
            },
        }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)

        c_opacity_cubes=0.4
        # transform_matrix
        y=15*PI/180
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
    CONFIG={
        "original_cube_kwargs":{
            "color":BLUE_E,
            "opacity":0.6,
            "stroke_width":0.5
            },
        "added_cubes_kwargs":{
            "color":YELLOW_E,
            "opacity":0.4,
            "stroke_width":0.5,
            },
        
        }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.cube_f.shift(0.2*DOWN+0.2*RIGHT)
        self.cube_t.shift(0.5*UP)
        self.cube_r.shift(0.8*RIGHT)
        self.bar_f.shift(0.25*UP+0.25*RIGHT)
        self.bar_t.shift(0.5*UP+0.8*RIGHT)
        self.bar_r.shift(1.2*RIGHT)
        self.cube_dx.shift(0.2*UP+1.2*RIGHT)

        self.cubes=VGroup(self.cube, self.cube_f, self.cube_t, self.cube_r, self.bar_f, self.bar_t, self.bar_r, self.cube_dx)
        self.add(self.cubes)

    def get_dx_cubes(self):
        return VGroup(self.cube_f, self.cube_t, self.cube_r)
        

    def get_braces_and_labels(self):
        self.br_cube=Brace(self.cube,LEFT).scale(0.75).shift(0.15*UP+0.1*RIGHT)
        self.lab_cube=MathTex("x").next_to(self.br_cube,1*LEFT)
        self.br_cube_t=Brace(self.cube_t,LEFT, width=80).scale(0.25).shift(0.15*UP+0.5*RIGHT)
        self.lab_cube_t=MathTex("dx").set_color(WHITE).next_to(self.br_cube_t,1*LEFT)
            
        return VGroup(self.br_cube, self.lab_cube, self.br_cube_t, self.lab_cube_t)

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
        self.div_line=Line(self.denominator.get_left(), self.denominator.get_right(), buff=0, stroke_width=2)
        self.numerator.next_to(self.div_line,0.8*UP)
        self.denominator.next_to(self.div_line,0.8*DOWN)
        self.fraction=VGroup(self.numerator,self.div_line, self.denominator)
        self.add(self.fraction)






