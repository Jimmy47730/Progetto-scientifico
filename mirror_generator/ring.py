from dataclasses import dataclass
from typing import Callable


@dataclass
class Ring:
    index: int
    c_n: float
    r_inner: float
    r_outer: float
    z_min: float
    z_max: float
    fn: Callable[[float], float]
    fn_name: str

    def evaluate(self, r):
        return self.fn(r)

    def __repr__(self) -> str:
        return (
            f"Ring(n={self.index}, C={self.c_n:.4f}, "
            f"fn={self.fn_name}, r=[{self.r_inner:.4f},{self.r_outer:.4f}], "
            f"z=({self.z_min:.4f},{self.z_max:.4f}])"
        )
