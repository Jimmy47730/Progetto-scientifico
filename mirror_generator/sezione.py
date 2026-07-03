from dataclasses import dataclass, field

import numpy as np

from functions import get_function


@dataclass
class Sezione:
    r0: float
    r1: float
    function_name: str
    params: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not (0.0 <= self.r0 < self.r1 <= 1.0):
            raise ValueError(f"Intervallo sezione non valido: [{self.r0}, {self.r1}]")

    def contains(self, r_norm: np.ndarray) -> np.ndarray:
        return (r_norm >= self.r0) & (r_norm <= self.r1)

    def evaluate(self, r_abs: np.ndarray, c_n: float) -> np.ndarray:
        fn = get_function(self.function_name)
        return fn(r_abs, c_n, self.params)

