# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

"""Implementation of the data nulling technique."""

from typing import Any, ClassVar

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class DataNulling(BaseSingleColumnTechnique):
    """Implements data nulling.

    Data nulling replaces the original data with a constant value.
    Missing values (`np.NaN`, `None`, `pd.NA`, `pd.NaT`) are also replaced.

    Attributes:
        constant_value: The value that will replace the original data. Default to None.
    """

    preserve_type: ClassVar[bool] = False

    constant_value: Any = None

    def __init__(self, constant_value: Any = None) -> None:
        super().__init__()
        self.constant_value = constant_value

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([self.constant_value for _ in col])
