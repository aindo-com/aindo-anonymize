# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Any, ClassVar

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class TopBottomCodingNumerical(BaseSingleColumnTechnique):
    """Implements top/bottom coding for numerical columns.

    This technique caps values above the `(1 - q/2)` quantile (top coding) and raises
    values below the `(q/2)` quantile (bottom coding). The threshold parameter `q` specifies the
    total proportion of extreme values to code (e.g., `q=0.1` applies top/bottom coding to 5% each).

    Either the threshold `q` or both quantile values (`lower_value` and `upper_value`) must be provided,
    but not both. If `lower_value` and `upper_value` are used, they must be specified together.

    Attributes:
        q: Proportion controlling the extent of top/bottom coding, between 0 and 1.
        lower_value: Input data quantile value at q/2.
        upper_value: Input data quantile value at (1- q/2).
    """

    q: float | None = None
    lower_value: float | None = None
    upper_value: float | None = None

    def __init__(
        self, q: float | None = None, lower_value: float | None = None, upper_value: float | None = None
    ) -> None:
        super().__init__()
        if (q is not None) and (not 0 <= q <= 1):
            raise ValueError("The threshold 'q' should be a value between 0 and 1")
        if (lower_value is None) != (upper_value is None):
            raise ValueError(
                "Quantile values (lower_value and upper_value) must be provided together or omitted entirely"
            )
        if (q is None) == (lower_value is None):
            raise ValueError("Either the threshold 'q' or the quantile values must be provided, but not both")
        self.q = q
        self.lower_value = lower_value
        self.upper_value = upper_value

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        lower_value: float
        upper_value: float
        if (self.lower_value is not None) and (self.upper_value is not None):
            lower_value = self.lower_value
            upper_value = self.upper_value
        else:
            assert self.q is not None
            lower_value = col.quantile(self.q / 2) if self.lower_value is None else self.lower_value
            upper_value = col.quantile(1 - self.q / 2) if self.upper_value is None else self.upper_value

        return col.clip(lower=lower_value, upper=upper_value)


class TopBottomCodingCategorical(BaseSingleColumnTechnique):
    """Implements top/bottom coding for categorical columns.

    Categories representing less or equal than `q` of the total data are replaced with the `other_label`
    (e.g.: q=0.01 represents the 1%).

    Attributes:
        q: A proportion controlling the extent of top/bottom coding, between 0 and 1.
        other_label: The new category to replace rare categories with. Default is "OTHER".
        rare_categories: A list of rare categories to be replaced.
            This can be used instead of the `q` parameter to explicitly specify
            which categories should be replaced with `other_label`.
    """

    preserve_type: ClassVar[bool] = False

    q: float | None = None
    other_label: Any = "OTHER"
    rare_categories: list[Any] | None = None

    def __init__(
        self, q: float | None = None, other_label: Any = "OTHER", rare_categories: list[Any] | None = None
    ) -> None:
        super().__init__()
        if (q is not None) and (not 0 <= q <= 1):
            raise ValueError("The value 'q' should be a value between 0 and 1.")
        if other_label is None:
            raise ValueError("The new category cannot be None")
        if (q is None) == (rare_categories is None):
            raise ValueError("Either 'q' or 'rare_categories' must be provided, but not both")
        self.q = q
        self.other_label = other_label
        self.rare_categories = rare_categories

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        out: pd.Series
        if col.dtype.name == "category":
            out = col.copy()
        else:
            out = col.astype("category")

        rare_categories: list[Any]
        if self.rare_categories is None:
            value_counts: pd.Series = col.value_counts(normalize=True)
            self.frequencies: dict = dict(zip(value_counts.index.to_list(), value_counts.values))
            rare_categories = value_counts[value_counts <= self.q].index.to_list()
        else:
            rare_categories = self.rare_categories

        if not rare_categories:
            return out

        out = out.cat.remove_categories(rare_categories)
        out = out.cat.add_categories(self.other_label)
        out.fillna(self.other_label, inplace=True)
        return out
