import math
import os

import matplotlib.pyplot as plt
import numpy as np

try:
    import plotly.graph_objects as go
except ImportError:  # pragma: no cover
    go = None

from config import Config
from functions import make_paraboloid, make_linear
from model_2d_builder import Model2DBuilder
from model_3d_transformer import Model3DTransformer
from ring import Ring
from stl_exporter import STLExporter


class MainApp:
    config: Config = Config()

    def __init__(self) -> None:
        self.config.apply_quality_preset()
        self.model2d = Model2DBuilder(self.config)
        self.model3d = Model3DTransformer()
        self.stl_exporter = STLExporter(self.config, self.model2d)

    def build_rings(self) -> list[Ring]:
        C0 = self.config.C0
        T = self.config.T
        R = self.config.MIRROR_RADIUS
        z_min = C0
        z_max = C0 + T

        rings: list[Ring] = []
        c_n = C0
        idx = 1

        while idx <= 200:
            # ── Parabola ──
            r_in_sq = 4.0 * c_n * (c_n - C0)
            r_out_sq = 4.0 * c_n * (c_n - z_max)

            if r_out_sq < 0:
                break

            r_in = 0.0 if r_in_sq < 1e-12 else math.sqrt(r_in_sq)
            r_out = math.sqrt(r_out_sq)

            clipped = r_out > R
            if clipped:
                r_out = R

            rings.append(Ring(
                index=idx,
                c_n=c_n,
                r_inner=r_in,
                r_outer=r_out,
                z_min=z_min,
                z_max=z_max,
                fn=make_paraboloid(c_n),
                fn_name="paraboloid",
            ))
            idx += 1

            if clipped:
                break

            # ── Linear (through focus at origin) ──
            slope = z_max / r_out
            r_end = C0 / slope

            clipped_lin = r_end > R
            if clipped_lin:
                r_end = R

            rings.append(Ring(
                index=idx,
                c_n=c_n,
                r_inner=r_out,
                r_outer=r_end,
                z_min=z_min,
                z_max=z_max,
                fn=make_linear(0.0, slope),
                fn_name="linear",
            ))
            idx += 1

            if clipped_lin:
                break

            # ── Next parabola vertex ──
            c_n = (C0 - math.sqrt(C0 ** 2 + r_end ** 2)) / 2.0

        print(f"  Raggio specchio: {R:.4f}")
        print(f"  Spessore: {T:.4f}")
        print(f"  C(1): {C0:.4f}")
        print(f"  Fetta z: ({z_min:.4f}, {z_max:.4f}]")
        print(f"  Anelli calcolati: {len(rings)}")

        return rings

    def plot_2d(self, rings: list[Ring]) -> None:
        colors = self._get_colors(len(rings))
        fig = plt.figure(figsize=self.config.FIGURE_SIZE)
        ax = fig.add_subplot(111)

        z_first = z_last = None
        for i, ring in enumerate(rings):
            r, z = self.model2d.build_ring_profile(ring, self.config.RES_PLOT_RADIAL)
            ax.plot(r, z, color=colors[i], linewidth=2.0, label=f"n={ring.index}")
            ax.plot(-r, z, color=colors[i], linewidth=2.0)
            valid = z[~np.isnan(z)]
            if i == 0 and len(valid):
                z_first = valid[0]
            if len(valid):
                z_last = valid[-1]

        # Cross-section outline: base + vertical walls
        R = self.config.MIRROR_RADIUS
        z_base = self.config.C0 - self.config.BASE_THICKNESS
        if z_first is not None and z_last is not None:
            kw = dict(color='black', linewidth=1.5)
            ax.plot([R, R], [z_last, z_base], **kw)        # right wall
            ax.plot([-R, -R], [z_last, z_base], **kw)      # left wall
            ax.plot([-R, R], [z_base, z_base], **kw)        # base
            ax.plot([0, 0], [z_base, z_first], **kw)        # center wall

        ax.set_xlabel("r")
        ax.set_ylabel(self.config.AXIS_LABELS[2])
        ax.set_title("Profilo 2D dei paraboloidi", fontsize=14)
        ax.grid(True, alpha=0.25)
        ax.set_aspect("equal" if self.config.EQUAL_AXIS_SCALE else "auto", adjustable="box")
        ax.legend(
            loc="upper left", bbox_to_anchor=(1.01, 1),
            borderaxespad=0, fontsize='small',
        )

        path = os.path.join(self.config.OUTPUT_DIR, "paraboloids_profile_matplotlib.png")
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.show()
        print(f"  [OK] matplotlib -> {path}")

    def plot_3d(self, rings: list[Ring]) -> None:
        if go is None:
            print("  [skip] plotly non disponibile")
            return

        colors = self._get_colors(len(rings))
        traces = []

        for i, ring in enumerate(rings):
            r, z = self.model2d.build_ring_profile(ring, self.config.RES_PLOT_RADIAL)
            x, y, z3 = self.model3d.revolve_profile(r, z, self.config.RES_PLOT_ANGULAR)
            color_rgb = colors[i][:3]
            color = f"rgb({int(255*color_rgb[0])},{int(255*color_rgb[1])},{int(255*color_rgb[2])})"
            traces.append(
                go.Surface(
                    x=x,
                    y=y,
                    z=z3,
                    opacity=self.config.ALPHA,
                    showscale=False,
                    colorscale=[[0, color], [1, color]],
                    name=f"n={ring.index} C={ring.c_n:.2f} fn={ring.fn_name}",
                )
            )

        scene = dict(
            xaxis_title=self.config.AXIS_LABELS[0],
            yaxis_title=self.config.AXIS_LABELS[1],
            zaxis_title=self.config.AXIS_LABELS[2],
            aspectmode="data" if self.config.EQUAL_AXIS_SCALE else "auto",
        )

        fig = go.Figure(data=traces)
        fig.update_layout(title=self.config.PLOT_TITLE, scene=scene)

        path = os.path.join(self.config.OUTPUT_DIR, "paraboloids_plotly.html")
        fig.write_html(path)
        fig.show()
        print(f"  [OK] plotly -> {path}")

    def run(self) -> None:
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

        print("** Costruzione anelli **")
        rings = self.build_rings()
        for ring in rings:
            print(f"   {ring}")
        
        """
        if self.config.RUN_MATPLOTLIB:
            print("\n** Matplotlib (profilo 2D) **")
            self.plot_2d(rings)

        if self.config.RUN_PLOTLY:
            print("\n** Plotly (profilo rivolto in 3D) **")
            self.plot_3d(rings)
        """

        if self.config.RUN_STL:
            print("\n** STL solido **")
            self.stl_exporter.export(rings)

    def _get_colors(self, n: int):
        cmap = plt.get_cmap(self.config.COLORMAP)
        return [cmap(i / max(n - 1, 1)) for i in range(n)]

if __name__ == "__main__":
    app = MainApp()
    app.run()