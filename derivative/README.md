#  derivative.py


## Objects

### DerivativeSquaresArea()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeSquaresArea()
        self.add(mob)
```

![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724064-ebaf9200-88a7-11eb-94fb-65f39d043954.png)

### DerivativeSquaresAreaSplitted()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeSquaresAreaSplitted()
        self.add(mob)
```

![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724501-b5bedd80-88a8-11eb-90a0-608eb2a94b2e.png)

### DerivativeCubeVolume()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeCubeVolume()
        self.add(mob)
```

![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724735-1f3eec00-88a9-11eb-8375-2a2476e7afe4.png)

### DerivativeCubeVolumeSplitted()

```python
class DerivativeSquaresAndCubes(Scene):
    def construct(self):
        mob=DerivativeCubeVolumeSplitted()
        self.add(mob)
```
![DerivativeSquaresAndCubes](https://user-images.githubusercontent.com/80928294/111724779-35e54300-88a9-11eb-8784-a01621b825e9.png)

## Animations


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

