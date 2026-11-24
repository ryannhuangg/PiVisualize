from manim import *

CURVE = "#b488ff"
TANGENT = "#d1b6f0"
AUX_CURVE = "#93928c"
PAUSE = 1.5
BEAT = 0.5

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
            self.wait(BEAT)
            self.play(Create(vline), FadeIn(point))
            self.wait(BEAT)
            self.play(Create(tan))
            self.wait(BEAT)

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
        self.play(Create(dotfinal))
        self.wait(PAUSE)
        self.play(Write(dotfinal_label))
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
        self.wait(PAUSE)
        self.play(Create(ggraph), Write(glabel))
        self.wait(PAUSE)
        self.play(FadeOut(hgraph, hlabel, ggraph, glabel))
        self.play(Create(fgraph), Write(flabel))
        self.wait(BEAT)

        def step(x, i, hi=0.3):
            s = self.camera.frame.width / config.frame_width
            dot = Dot(axes.c2p(x, 0), radius=0.08 * s, color=WHITE)
            dot_label = MathTex(f"x_{i}").scale(0.7 * s).next_to(dot, DOWN, buff=0.15 * s)
            vline = DashedLine(axes.c2p(x, 0), axes.c2p(x, f(x)), dash_length=0.05 * s, stroke_width=4 * s, color=WHITE)
            point = Dot(axes.c2p(x, f(x)), radius=0.08 * s, color=WHITE)
            tan = axes.plot(lambda t: f(x) + df(x) * (t - x), x_range=[x - 0.6, x + hi], color=TANGENT)
            self.play(FadeIn(dot), Write(dot_label))
            self.wait(BEAT)
            self.play(Create(vline), FadeIn(point))
            self.wait(BEAT)
            self.play(Create(tan))
            self.wait(BEAT)

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
        self.play(Create(dotfinal))
        self.wait(PAUSE)
        self.play(Write(dotfinal_label))
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
        self.wait(PAUSE)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(PAUSE)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(PAUSE)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(2)

def pf_step(scene, axes, f, df, x, i, a, b):
    dot = Dot(axes.c2p(x, 0), radius=0.08, color=WHITE)
    dot_label = MathTex(f"x_{i}").scale(0.7).next_to(dot, UP if f(x) < 0 else DOWN, buff=0.15)
    vline = DashedLine(axes.c2p(x, 0), axes.c2p(x, f(x)), dash_length=0.05, stroke_width=4, color=WHITE)
    point = Dot(axes.c2p(x, f(x)), radius=0.08, color=WHITE)
    tan = axes.plot(lambda t: f(x) + df(x) * (t - x), x_range=[a, b], color=TANGENT)
    scene.play(FadeIn(dot), Write(dot_label))
    scene.wait(BEAT)
    scene.play(Create(vline), FadeIn(point))
    scene.wait(BEAT)
    scene.play(Create(tan))
    scene.wait(BEAT)

class NewtonPF1(Scene):
    def construct(self):
        f = lambda x: x**3 - x
        df = lambda x: 3 * x**2 - 1

        axes = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[-1.5, 1.5, 0.5], x_length=8, y_length=5, tips=False).center().shift(DOWN * 0.3)
        graph = axes.plot(f, x_range=[-1.45, 1.45], color=CURVE)
        label = MathTex("f(x)=x^3-x", color=CURVE).scale(0.8).to_edge(UP)
        self.play(Create(axes), Create(graph), Write(label))
        self.wait(BEAT)

        roots = VGroup(*[Dot(axes.c2p(r, 0), radius=0.08, color=AUX_CURVE) for r in (-1, 0, 1)])
        self.play(LaggedStart(*[GrowFromCenter(r) for r in roots], lag_ratio=0.3))
        self.wait(PAUSE)

        x0 = 0.5
        pf_step(self, axes, f, df, x0, 0, -1.3, 0.8)

        x1 = x0 - f(x0) / df(x0)
        dot1 = Dot(axes.c2p(x1, 0), radius=0.12, color=WHITE)
        dot1_label = MathTex("x_1 = -1").scale(0.7).next_to(dot1, DR, buff=0.1)
        self.play(Create(dot1), Write(dot1_label))
        self.wait(PAUSE)

        note = MathTex(r"\text{Closest roots to } x_0 \text{ are } 0 \text{ and } 1 \text{, but we land on } {-1}").scale(0.6).next_to(label, DOWN, buff=0.25)
        self.play(Write(note), Indicate(roots[1]), Indicate(roots[2]))
        self.wait(2)

class NewtonPF2(Scene):
    def construct(self):
        f = lambda x: x**2 - 1
        df = lambda x: 2 * x

        axes = Axes(x_range=[-2, 2, 1], y_range=[-1.5, 3, 1], x_length=7, y_length=4, tips=False).center().shift(DOWN * 1.1)
        graph = axes.plot(f, x_range=[-2, 2], color=CURVE)
        label = MathTex("f(x)=x^2-1", color=CURVE).scale(0.8).to_edge(UP)
        self.play(Create(axes), Create(graph), Write(label))
        self.wait(BEAT)

        pf_step(self, axes, f, df, 0, 0, -2, 2)

        eq = MathTex(r"x_1 = x_0 - \frac{f(x_0)}{f'(x_0)} = 0 - \frac{-1}{0}").scale(0.7).next_to(label, DOWN, buff=0.3)
        self.play(Write(eq))
        self.wait(PAUSE)

        note = MathTex(r"\text{Undefined: the tangent never crosses the x-axis}", color=TANGENT).scale(0.6).next_to(eq, DOWN, buff=0.25)
        self.play(Write(note))
        self.wait(2)

class NewtonPF3(Scene):
    def construct(self):
        f = lambda x: np.cbrt(x)
        df = lambda x: 1 / (3 * np.cbrt(x) ** 2)

        axes = Axes(x_range=[-4.5, 2.5, 1], y_range=[-2, 2, 1], x_length=10, y_length=4.2, tips=False).center().shift(DOWN * 0.9)
        graph = axes.plot(f, x_range=[-4.5, 2.5, 0.005], color=CURVE)
        label = MathTex(r"f(x)=x^{1/3}", color=CURVE).scale(0.8).to_edge(UP)
        self.play(Create(axes), Create(graph), Write(label))
        self.wait(BEAT)

        x = 0.5
        for i in range(3):
            nxt = -2 * x
            a, b = sorted((x, nxt))
            pf_step(self, axes, f, df, x, i, a - 0.3, b + 0.3)
            x = nxt

        dot3 = Dot(axes.c2p(x, 0), radius=0.12, color=WHITE)
        dot3_label = MathTex("x_3 = -4").scale(0.7).next_to(dot3, UP, buff=0.15)
        self.play(Create(dot3), Write(dot3_label))
        self.wait(PAUSE)

        note = MathTex(r"x_{n+1} = x_n - \frac{x_n^{1/3}}{\tfrac{1}{3}x_n^{-2/3}} = -2x_n \;\Rightarrow\; |x_n| \to \infty").scale(0.65).next_to(label, DOWN, buff=0.25)
        self.play(Write(note))
        self.wait(2)
