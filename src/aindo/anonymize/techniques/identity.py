# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT


import pandas as pd

from aindo.anonymize.techniques.base import BaseTechnique


class Identity(BaseTechnique):
    """Identity technique.

    Leaves the original data untouched.
    This special technique is particularly useful in a declarative approach (see documentation).
    """

    def __init__(self) -> None:
        super().__init__()

    def anonymize(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.copy()
