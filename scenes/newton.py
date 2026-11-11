from manim import *

CURVE = "#4a6ae0"
TANGENT = "#7260d6"
AUX_CURVE = "#72a0ff" 

class NewtonEx1(MovingCameraScene):
    def construct(self):
        f = lambda x: x**2 - 2
        df = lambda x: 2 * x

        axes = Axes(
            x_range=[-0.5, 3, 1],
            y_range=[-3, 4, 1],
            x_length=7,
            y_length=5,
            tips=False,
        ).center()
        graph = axes.plot(f, x_range=[-0.5, 2.3], color=CURVE)
        label = MathTex("f(x)=x^2-2", color=CURVE).scale(0.8).next_to(axes, UP, buff=0.2)
        self.play(Create(axes), Create(graph), Write(label))

        def step(x, i, hi=0.3):
            s = self.camera.frame.width / config.frame_width
            dot = Dot(axes.c2p(x, 0), radius=0.08 * s, color=WHITE)
            dot_label = MathTex(f"x_{i}").scale(0.7 * s).next_to(dot, DOWN, buff=0.15 * s)
            vline = DashedLine(axes.c2p(x, 0), axes.c2p(x, f(x)), dash_length=0.05 * s, stroke_width=4 * s, color=WHITE)
            point = Dot(axes.c2p(x, f(x)), radius=0.08 * s, color=WHITE)
            tan = axes.plot(lambda t: f(x) + df(x) * (t - x), x_range=[x - 0.6, x + hi], color=TANGENT)
            self.play(FadeIn(dot), Write(dot_label))
            self.play(Create(vline), FadeIn(point))
            self.play(Create(tan))

        x0 = 2.0
        step(x0, 0)

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(axes.c2p(1.75, 0.8)),
            run_time=2,
        )

        x1 = x0 - f(x0) / df(x0)
        step(x1, 1, hi=0.6)

        self.play(
            self.camera.frame.animate.scale(0.25).move_to(axes.c2p(1.46, 0.12)),
            run_time=2,
        )

        x2 = x1 - f(x1) / df(x1)
        s = self.camera.frame.width / config.frame_width
        dotfinal = Dot(axes.c2p(x2, 0), radius=0.12 * s, color=WHITE)
        dotfinal_label = MathTex(r"x_2 \approx \sqrt{2}").scale(0.9 * s).next_to(dotfinal, UL, buff=0.1 * s)
        self.play(Create(dotfinal), Write(dotfinal_label))
        self.wait(1)

class NewtonEx2(MovingCameraScene):
    def construct(self):
        h = lambda x: np.cos(x)
        g = lambda x: x
        f = lambda x: np.cos(x) - x
        df = lambda x: -1 * np.sin(x) - 1 

        axes = Axes(
            x_range = [-0.5, 3, 1],
            y_range = [-1, 3, 1],
            x_length = 7,
            y_length = 5,
            tips = False,
        ).center()

        hgraph = axes.plot(h, x_range=[-0.5, 2.5], color=CURVE)
        ggraph = axes.plot(g, x_range=[-0.5, 2.5], color=CURVE)
        fgraph = axes.plot(f, x_range=[-0.5, 2.5], color=AUX_CURVE)

        context_label = MathTex(r"\text{Finding where } h(x) \text{ and } g(x) \text{ intersect}").scale(0.8).to_edge(UP)

        hlabel = MathTex(r"h(x) = \cos(x)", color=CURVE).scale(0.6).next_to(axes.c2p(2.2, h(2.2)), UR)
        glabel = MathTex(r"g(x) = x", color=CURVE).scale(0.6).next_to(axes.c2p(2.2, g(2.2)), UL)

        flabel = VGroup(
            MathTex(r"\text{Auxiliary Function:}", color=AUX_CURVE),
            MathTex(r"f(x) = \cos(x) - x", color=AUX_CURVE)
        ).arrange(DOWN).scale(0.6).next_to(fgraph, UP, buff=0.5)

        self.play(Create(axes))
        self.play(Write(context_label))
        self.play(Create(hgraph), Write(hlabel))
        self.wait()
        self.play(Create(ggraph), Write(glabel))
        self.wait()
        self.play(FadeOut(hgraph, hlabel, ggraph, glabel))
        self.play(Create(fgraph), Write(flabel))

        def step(x, i, hi=0.3):
            s = self.camera.frame.width / config.frame_width
            dot = Dot(axes.c2p(x, 0), radius=0.08 * s, color=WHITE)
            dot_label = MathTex(f"x_{i}").scale(0.7 * s).next_to(dot, DOWN, buff=0.15 * s)
            vline = DashedLine(axes.c2p(x, 0), axes.c2p(x, f(x)), dash_length=0.05 * s, stroke_width=4 * s, color=WHITE)
            point = Dot(axes.c2p(x, f(x)), radius=0.08 * s, color=WHITE)
            tan = axes.plot(lambda t: f(x) + df(x) * (t - x), x_range=[x - 0.6, x + hi], color=TANGENT)
            self.play(FadeIn(dot), Write(dot_label))
            self.play(Create(vline), FadeIn(point))
            self.play(Create(tan))

        x0 = 0.5
        step(x0, 0, hi=0.6)

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(axes.c2p(0.85, -0.2)),
            run_time=2,
        )

        x1 = x0 - f(x0) / df(x0)
        step(x1, 1, hi=0.2)

        self.play(
            self.camera.frame.animate.scale(0.25).move_to(axes.c2p(0.74, 0)),
            run_time=2,
        )

        x2 = x1 - f(x1) / df(x1)
        s = self.camera.frame.width / config.frame_width
        dotfinal = Dot(axes.c2p(x2, 0), radius=0.12 * s, color=WHITE)
        dotfinal_label = MathTex(r"x_2 \approx 0.739").scale(0.9 * s).next_to(dotfinal, UL, buff=0.1 * s)
        self.play(Create(dotfinal), Write(dotfinal_label))
        self.wait(2)

class NewtonDerivation(Scene):
    def construct(self):
        eq1 = MathTex("y", "-", "f(x_n)", "=", "f'(x_n)", "(", "x", "-", "x_n", ")")
        eq2 = MathTex("0", "-", "f(x_n)", "=", "f'(x_n)", "(", "x_{n+1}", "-", "x_n", ")")
        eq3 = MathTex("-", "{f(x_n) \\over f'(x_n)}", "=", "x_{n+1}", "-", "x_n")
        eq4 = MathTex("x_{n+1}", "=", "x_n", "-", "{f(x_n) \\over f'(x_n)}")
        for e in (eq1, eq2, eq3, eq4):
            e.scale(0.8)

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait()
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(2)

