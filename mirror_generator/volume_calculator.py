"""Calcolo del volume del solido in millimetri cubi.

Il solido viene definito come un profilo assiale ruotato intorno all'asse z.
Per ogni anello, si campiona il profilo r-z e si applica la formula del
solido di rivoluzione:

    V = 2 * pi * \int r * (z(r) - z_base) dr

Dove z_base è il piano inferiore del solido (profilo z_min meno lo spessore
 della base). Le dimensioni del modello sono espresse in millimetri, quindi
 il volume risultante è in mm^3.
"""

import math
import numpy as np

from main_app import MainApp
from model_2d_builder import Model2DBuilder
from ring import Ring
from config import Config


def compute_ring_volume(ring: Ring, config: Config, n_samples: int = 2000) -> float:
    """Calcola il volume di un singolo anello ruotato attorno all'asse z."""
    z_base = ring.z_min - config.BASE_THICKNESS
    r, z = Model2DBuilder(config).build_ring_profile(ring, n_samples)
    valid = ~np.isnan(z)
    if not np.any(valid):
        return 0.0

    r = r[valid]
    z = z[valid]
    z_rel = z - z_base
    volume = 2.0 * math.pi * np.trapz(r * z_rel, r)
    return float(volume)


def compute_volume(rings: list[Ring], config: Config, n_samples_per_ring: int = 2000) -> float:
    """Calcola il volume totale del solido formato dagli anelli."""
    total_volume = 0.0
    for ring in rings:
        total_volume += compute_ring_volume(ring, config, n_samples=n_samples_per_ring)
    return total_volume


def main() -> None:
    app = MainApp()
    rings = app.build_rings()

    volume_mm3 = compute_volume(rings, app.config)
    volume_cm3 = volume_mm3 / 1000.0

    print("\n** Volume del solido **")
    print(f"  Volume totale: {volume_mm3:.2f} mm^3")
    print(f"  Volume totale: {volume_cm3:.2f} cm^3")


if __name__ == "__main__":
    main()
