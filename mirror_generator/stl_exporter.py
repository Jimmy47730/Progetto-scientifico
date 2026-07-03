from dataclasses import dataclass
import os

import numpy as np

try:
    import trimesh
except ImportError:  # pragma: no cover
    trimesh = None

from config import Config
from model_2d_builder import Model2DBuilder
from ring import Ring


@dataclass
class STLExporter:
    config: Config
    model2d: Model2DBuilder

    def export(self, rings: list[Ring]) -> None:
        if trimesh is None:
            print("  [skip] trimesh non disponibile")
            return

        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

        # Build combined profile from all rings
        n_per_ring = max(4, self.config.RES_STL_RADIAL // max(len(rings), 1))
        segments_r: list[np.ndarray] = []
        segments_z: list[np.ndarray] = []
        for ring in rings:
            r, z = self.model2d.build_ring_profile(ring, n_per_ring)
            mask = ~np.isnan(z)
            segments_r.append(r[mask])
            segments_z.append(z[mask])

        r_all = np.concatenate(segments_r)
        z_all = np.concatenate(segments_z)

        # Remove duplicate r values at ring boundaries
        keep = np.ones(len(r_all), dtype=bool)
        keep[1:] = np.abs(np.diff(r_all)) > 1e-10
        r_profile = r_all[keep]
        z_profile = z_all[keep]

        # Handle center convergence (r ≈ 0)
        use_center = r_profile[0] < 1e-4
        z_center_top = z_profile[0]
        if use_center:
            r_profile = r_profile[1:]
            z_profile = z_profile[1:]

        n_r = len(r_profile)
        n_t = max(8, self.config.RES_STL_ANGULAR)
        z_base = rings[0].z_min - self.config.BASE_THICKNESS

        theta = np.linspace(0.0, 2.0 * np.pi, n_t, endpoint=False)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # --- Vertices ---
        # Top surface:  i * n_t + j           (i=0..n_r-1, j=0..n_t-1)
        # Bottom surface: S + i * n_t + j
        X = np.outer(r_profile, cos_t)
        Y = np.outer(r_profile, sin_t)
        Z_top = np.tile(z_profile[:, None], (1, n_t))
        Z_bot = np.full_like(Z_top, z_base)

        top_v = np.column_stack([X.ravel(), Y.ravel(), Z_top.ravel()])
        bot_v = np.column_stack([X.ravel(), Y.ravel(), Z_bot.ravel()])
        verts = np.vstack([top_v, bot_v])
        S = n_r * n_t  # offset for bottom surface indices

        # --- Face index helpers ---
        i_idx = np.arange(n_r - 1)[:, None]
        j_idx = np.arange(n_t)[None, :]
        j1 = (j_idx + 1) % n_t

        t00 = i_idx * n_t + j_idx
        t10 = (i_idx + 1) * n_t + j_idx
        t11 = (i_idx + 1) * n_t + j1
        t01 = i_idx * n_t + j1

        # Top surface faces
        top_f = np.vstack([
            np.column_stack([t00.ravel(), t10.ravel(), t11.ravel()]),
            np.column_stack([t00.ravel(), t11.ravel(), t01.ravel()]),
        ])

        # Bottom surface faces (reversed winding)
        bot_f = np.vstack([
            np.column_stack([(t00 + S).ravel(), (t11 + S).ravel(), (t10 + S).ravel()]),
            np.column_stack([(t00 + S).ravel(), (t01 + S).ravel(), (t11 + S).ravel()]),
        ])

        # Outer wall (i = n_r - 1)
        j_arr = np.arange(n_t)
        j1_arr = (j_arr + 1) % n_t
        last = n_r - 1
        ot = last * n_t + j_arr
        ot1 = last * n_t + j1_arr
        ob = ot + S
        ob1 = ot1 + S
        outer_f = np.vstack([
            np.column_stack([ot, ot1, ob1]),
            np.column_stack([ot, ob1, ob]),
        ])

        all_faces = np.vstack([top_f, bot_f, outer_f])

        # Inner closure
        if use_center:
            ct_idx = len(verts)
            cb_idx = ct_idx + 1
            verts = np.vstack([
                verts,
                [[0.0, 0.0, z_center_top]],
                [[0.0, 0.0, z_base]],
            ])
            top_fan = np.column_stack([np.full(n_t, ct_idx), j1_arr, j_arr])
            bot_fan = np.column_stack([np.full(n_t, cb_idx), S + j_arr, S + j1_arr])
            all_faces = np.vstack([all_faces, top_fan, bot_fan])
        else:
            it = j_arr
            it1 = j1_arr
            ib = it + S
            ib1 = it1 + S
            inner_f = np.vstack([
                np.column_stack([it, ib1, it1]),
                np.column_stack([it, ib, ib1]),
            ])
            all_faces = np.vstack([all_faces, inner_f])

        mesh = trimesh.Trimesh(vertices=verts, faces=all_faces, process=True)
        trimesh.repair.fix_normals(mesh)

        path = os.path.join(self.config.OUTPUT_DIR, "specchio_solido.stl")
        mesh.export(path)
        print(f"  [OK] STL -> {path} (watertight: {mesh.is_watertight})")
