# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import ClassVar

import pandas as pd


class BaseTechnique(ABC):
    """Abstract base class for all anonymization techniques."""

    preserve_type: ClassVar[bool]

    @abstractmethod
    def anonymize(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applies the anonymization technique to the given data.

        Args:
            dataframe: The input data to be anonymized.

        Returns:
            The anonymized version of the input data.
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        fields: str = ",".join([f"{k!s}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_")])
        return f"{self.__class__.__name__}({fields})"


class BaseSingleColumnTechnique(BaseTechnique, ABC):
    """Abstract base class for anonymization techniques applied to a single column.

    Subclasses should implement the `anonymize_column` method,
    which defines the logic for anonymizing a single column.
    """

    preserve_type: ClassVar[bool] = True

    @abstractmethod
    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        raise NotImplementedError()

    def anonymize_column(self, col: pd.Series) -> pd.Series:
        """Applies the anonymization technique to a single column.

        Args:
            col: The input data to be anonymized.

        Returns:
            The anonymized version of the input data.
        """
        out: pd.Series = self._apply_to_col(col)
        if self.preserve_type:
            return out.astype(col.dtype, copy=False)
        else:
            return out

    def anonymize(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applies the anonymization technique to a single-column dataframe.

        This is analogous to calling `anonymize_column()` on a single Pandas Series.
        It is a convenience method shared across all types of anonymizers.

        Args:
            dataframe: The input data. Must have exactly one column.

        Returns:
            The anonymized version of the input data.
        """
        if dataframe.shape[1] != 1:
            raise ValueError("Dataframe should have exactly one column")
        return pd.DataFrame(self.anonymize_column(dataframe.iloc[:, 0]), columns=dataframe.columns)
