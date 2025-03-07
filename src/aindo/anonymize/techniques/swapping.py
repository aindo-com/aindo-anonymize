# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique
from aindo.anonymize.techniques.common import AlphaProbability, Seeder, SeedT


class Swapping(BaseSingleColumnTechnique, Seeder, AlphaProbability):
    """Implements swapping.

    Swapping rearranges data by shuffling values,
    ensuring that individual values remain present but are generally not in their original position.
    The process is controlled by the `alpha` parameter,
    representing the probability of a row being swapped with another.

    Attributes:
        alpha: The perturbation intensity, a value in the range [0, 1].
    """

    def __init__(self, alpha: float, **kwargs: SeedT) -> None:
        Seeder.__init__(self, **kwargs)
        AlphaProbability.__init__(self, alpha)

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        if self.alpha == 0:
            return col.copy()

        rows_to_swap = [idx for idx in col.index if self.generator.random() <= self.alpha]
        out: pd.Series = col.copy()

        for idx in rows_to_swap:
            new_idx: int = self.generator.choice(rows_to_swap[:idx] + rows_to_swap[idx + 1 :], 1)[0]

            out[idx], out[new_idx] = out[new_idx], out[idx]

        return out
