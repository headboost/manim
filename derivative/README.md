


# Objects

## DerivativeSquaresArea()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeSquaresArea()
        self.add(mob)
```

![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724064-ebaf9200-88a7-11eb-94fb-65f39d043954.png)

## DerivativeSquaresAreaSplitted()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeSquaresAreaSplitted()
        self.add(mob)
```

![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724501-b5bedd80-88a8-11eb-90a0-608eb2a94b2e.png)

## DerivativeCubeVolume()

```python
class DerivativeSquaresAndCubes(ThreeDScene):
    def construct(self):
        mob=DerivativeCubeVolume()
        self.add(mob)
```

![DerivativeCubes](https://user-images.githubusercontent.com/80928294/111894343-7b427580-8a4d-11eb-92ef-e5b9c8007800.png)


## DerivativeCubeVolumeSplitted()

```python
class DerivativeSquaresAndCubes(ThreeDScene):
    def construct(self):
        mob=DerivativeCubeVolumeSplitted()
        self.add(mob)
```

![DerivativeCubesSplitetted](https://user-images.githubusercontent.com/80928294/111894348-8a292800-8a4d-11eb-99c6-20d4f0b3ffe7.png)


# Animations

## split_derivative_rectangles()
```python
class SplitDerivativeRectangles(Scene):
    def construct(self):
        self.split_derivative_rectangles(split_factor=0.2)

    def split_derivative_rectangles(self, split_factor=0.2, scale_factor=1, position=[0,0,0]):
        obj=DerivativeSquaresArea().move_to(position).scale(scale_factor)
        o,r,u,dx = obj.squares        
        b_u, l_u, b_r, l_r = obj.braces_and_labels
        dx_bs_ls = obj.dx_braces_and_labels
        
        self.play(FadeIn(o))
        self.play(FadeIn(r), FadeIn(u), FadeIn(dx), FadeIn(obj.braces_and_labels), FadeIn(obj.dx_braces_and_labels))
        self.play(
            r.shift, split_factor*RIGHT,
            u.shift, split_factor*UP,
            dx.shift, split_factor*UP+split_factor*RIGHT,
            b_u.shift, split_factor*UP,
            l_u.shift, split_factor*UP,
            b_r.shift, split_factor*RIGHT,
            l_r.shift, split_factor*RIGHT,
            dx_bs_ls.shift, split_factor*UP+split_factor*RIGHT,

            )
```

![SplitDerivativeRectangles](https://user-images.githubusercontent.com/80928294/111894401-d70cfe80-8a4d-11eb-9396-8b13480d40b6.gif)

## split_derivative_cubes()

```python
class SplitDerivativeCubes(ThreeDScene):
    def construct(self):
        self.split_derivative_cubes()

    def split_derivative_cubes(self, split_factor=0.2, scale_factor=1, position=[0,0,0]):
        obj=DerivativeCubeVolume().move_to(position)
        cube, cube_f, cube_t, cube_r, bar_f, bar_t, bar_r, cube_dx = obj.cubes
        br_cube, lab_cube, br_cube_t, lab_cube_t = obj.braces_and_labels

        self.add(obj)
        self.play(
            cube_f.shift, 0.2*DOWN+0.2*RIGHT,
            cube_t.shift, 0.4*UP,
            cube_r.shift, 0.6*RIGHT,
            bar_f.shift, 0.25*UP+0.25*RIGHT,
            bar_t.shift, 0.5*UP+0.6*RIGHT,
            bar_r.shift, 1.*RIGHT,
            cube_dx.shift, 0.2*UP+1.*RIGHT,
            br_cube_t.shift, 0.4*UP, 
            lab_cube_t.shift, 0.4*UP,
            )
```

![SplitDerivativeCubes](https://user-images.githubusercontent.com/80928294/111894427-f441cd00-8a4d-11eb-8599-33fb468ad3cb.gif)





```python
class DescribeTangentLine(GraphScene):
    CONFIG={
        "func": lambda x:x**3,
        "d_func": lambda x:3*x**2,
        "stroke_width":2,
        "dot_radius": 0.05,
        "tangent_line_color": YELLOW,
        "length_of_tangentline": 8,
        }
    def construct(self):
        self.setup_axes()
        # define a curve
        curveA=self.get_graph(
            self.func,
            stroke_width=self.stroke_width,
            )
        # define two dots on the curve
        dot_start=Dot(radius=self.dot_radius).move_to(self.coords_to_point(0,self.func(0)))
        dot_end=Dot(radius=self.dot_radius).move_to(self.coords_to_point(1,self.func(1)))
        # draw line between two dots
        tangent_line=self.get_line_across_points(
            dot_start,
            dot_end,
            color=self.tangent_line_color,
            stroke_width=self.stroke_width,
            length=self.length_of_tangentline
            )
        # add updater to the line above
        tangent_line.add_updater(self.get_line_updater(dot_start, dot_end, length=self.length_of_tangentline))

        self.add(curveA, tangent_line, dot_start, dot_end)
        self.move_dot(
            dot_end,  # put a dot to move
            1,             # where a dot starts from
            0.0001,        # where a dot to go
            run_time=5
            )

        # remove updater after the animation
        tangent_line.clear_updaters()
        self.remove(dot_end)
```

![DescribeTangentLine](https://user-images.githubusercontent.com/80928294/111892378-4b3fa600-8a3e-11eb-9216-e886da5fa818.gif)

```python
class MoveTangentLine(GraphScene):
    CONFIG={
        "func": lambda x:x**3,
        "d_func": lambda x:3*x**2,
        "stroke_width":3,
        "dot_radius": 0.05,
        "tangent_line_color": YELLOW,
        "length_of_tangentline": 8,
        }
    def construct(self):
        self.setup_axes()
        curveA=self.get_graph(
            self.func,
            stroke_width=self.stroke_width,
            )
        line=VMobject()
        dot_start=Dot(radius=self.dot_radius).move_to(self.coords_to_point(0,self.func(0)))
        # add updater to tangent line
        line.add_updater(self.get_derivative_updater(dot_start))
        self.add(curveA, line, dot_start)

        self.move_dot(
            dot_start,  # put a dot to move
            0.0001,     # where a dot starts from
            -1.2,         # where a dot to go
            run_time=3
            )
        self.wait()
        self.move_dot(
            dot_start,  # put a dot to move
            -1.2,     # where a dot starts from
            1.2,         # where a dot to go
            run_time=3
            )
        self.wait()

        # remove updater after the animation
        line.clear_updaters()
```

![MoveTangentLine](https://user-images.githubusercontent.com/80928294/111892451-00725e00-8a3f-11eb-9e4c-cb1850138b76.gif)

```python
class DrawDerivativeFunction(GraphScene):
    CONFIG={
        "func": lambda x:x**3,
        "d_func": lambda x:3*x**2,
        "stroke_width":3,
        "dot_radius": 0.05,
        "tangent_line_color": YELLOW,
        "length_of_tangentline": 8,
        }
    def construct(self):
        self.setup_axes()
        curveA=self.get_graph(
            self.func,
            stroke_width=self.stroke_width,
            )
        line=VMobject()
        dot_start=Dot(radius=self.dot_radius).move_to(self.coords_to_point(0,self.func(0)))
        # add updater to tangent line
        line.add_updater(self.get_derivative_updater(dot_start))
        self.add(curveA, line, dot_start)

        self.move_dot_and_draw_derivative_function(
            dot_start,      # put a dot to move
            -1.2,           # where a dot starts from
            1.2,            # where a dot to go
            d_func=self.d_func,   # put a function
            run_time=3
            )
        self.wait()

        # remove updater after the animation
        line.clear_updaters()
```

![DrawDerivativeFunction](https://user-images.githubusercontent.com/80928294/111892521-8bebef00-8a3f-11eb-8d95-955bd7869a31.gif)
