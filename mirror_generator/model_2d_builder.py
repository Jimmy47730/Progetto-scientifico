from dataclasses import dataclass

import numpy as np

from config import Config
from ring import Ring


@dataclass
class Model2DBuilder:
    config: Config

    def build_ring_profile(self, ring: Ring, n_r: int) -> tuple[np.ndarray, np.ndarray]:
        r_inner = ring.r_inner
        if r_inner <= 0.0:
            r_inner = max(1e-9, ring.r_outer * 1e-6)

        u = np.linspace(0.0, 1.0, n_r)
        r = r_inner + (ring.r_outer - r_inner) * (u ** self.config.RADIAL_POWER)
        z = ring.evaluate(r)
        z = np.where((z >= ring.z_min) & (z <= ring.z_max), z, np.nan)
        return r, z
