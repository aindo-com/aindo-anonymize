# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Any, ClassVar

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class DataNulling(BaseSingleColumnTechnique):
    """Implements data nulling.

    Data nulling replaces the original data with a `None` value
    (or a custom constant value).

    Attributes:
        constant_value: The value that will replace the original data. Default to None.
    """

    preserve_type: ClassVar[bool] = False

    constant_value: Any = None

    def __init__(self, constant_value: Any = None) -> None:
        super().__init__()
        self.constant_value = constant_value

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([self.constant_value for _ in col], dtype=type(self.constant_value))
