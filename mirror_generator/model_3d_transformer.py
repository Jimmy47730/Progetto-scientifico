from dataclasses import dataclass

import numpy as np


@dataclass
class Model3DTransformer:
    def revolve_profile(self, r: np.ndarray, z: np.ndarray, n_theta: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        theta = np.linspace(0.0, 2.0 * np.pi, n_theta, endpoint=False)
        theta = np.concatenate([theta, [2.0 * np.pi]])

        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        x = np.outer(r, cos_t)
        y = np.outer(r, sin_t)
        z3 = np.repeat(z[:, None], len(theta), axis=1)
        return x, y, z3
