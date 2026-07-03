from dataclasses import dataclass

import numpy as np

from sezione import Sezione


@dataclass
class Profilo:
    sezioni: list[Sezione]

    def __post_init__(self) -> None:
        if not self.sezioni:
            raise ValueError("Il profilo deve contenere almeno una sezione")

    def sample_radius(self, r_inner: float, r_outer: float, n_r: int, radial_power: float) -> np.ndarray:
        if r_outer <= r_inner:
            raise ValueError("r_outer deve essere maggiore di r_inner")
        u = np.linspace(0.0, 1.0, n_r)
        return r_inner + (r_outer - r_inner) * (u**radial_power)

    def evaluate(self, r_abs: np.ndarray, r_mirror: float, c_n: float) -> np.ndarray:
        r_abs = np.asarray(r_abs, dtype=float)
        z = np.full_like(r_abs, np.nan, dtype=float)
        denom = max(r_mirror, 1e-12)
        r_norm = np.clip(r_abs / denom, 0.0, 1.0)

        for sezione in self.sezioni:
            mask = sezione.contains(r_norm)
            if np.any(mask):
                z_seg = sezione.evaluate(r_abs, c_n)
                z[mask] = np.asarray(z_seg)[mask]

        return z

    def sezione_for_index(self, i: int) -> Sezione:
        if i < len(self.sezioni):
            return self.sezioni[i]
        return self.sezioni[-1]
