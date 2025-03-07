# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import ClassVar, Sequence

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class Binning(BaseSingleColumnTechnique):
    """Implements binning for numerical columns.

    Binning works by grouping numerical values into discrete bins,
    allowing for data generalization by replacing individual values with their corresponding bin ranges.

    Attributes:
        bins: The bin edges or number of bins to use.

    Examples:
        An integer bins will form equal-width bins.
        >>> ages = pd.Series([10, 15, 13, 12, 23, 25, 28, 59, 60])
        >>> Binning(bins=3).anonymize_column(ages)
        [(9.95, 26.667], (9.95, 26.667], (9.95, 26.667], ...
        Categories (3, interval[float64, right]): [(9.95, 26.667] < (26.667, 43.333] < (43.333, 60.0]]

        A list of ordered bin edges will assign an interval for each variable.
        >>> ages = pd.Series([10, 15, 13, 12, 23, 25, 28, 59, 60])
        >>> Binning(bins=[0, 18, 35, 70]).anonymize_column(ages)
        [(0, 18], (0, 18], (0, 18], (0, 18], (18, 35], ...
        Categories (3, interval[int64, right]): [(0, 18] < (18, 35] < (35, 70]]
    """

    preserve_type: ClassVar[bool] = False

    bins: int | Sequence[int] | Sequence[float]

    def __init__(self, bins: int | Sequence[int] | Sequence[float]) -> None:
        super().__init__()
        self.bins = bins

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.cut(col, self.bins, labels=None)
