# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

"""Implementation of the identity technique."""

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
        """Anonymize the input data using the identity technique.

        Args:
            dataframe: The input data to be anonymized.

        Returns:
            The anonymized version of the input data.
        """
        return dataframe.copy()
