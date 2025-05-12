# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import os

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike
from scipy.stats import chisquare, ks_2samp


def assert_categorical_distribution(
    observed: pd.Series, expected: pd.Series | None = None, significance_level: float = 0.05
) -> None:
    """
    Use the chi-square test to determine if the observed categorical data
    has the same frequencies as expected.
    By default the expected categories are assumed to be equally likely.
    """

    _, p = chisquare(
        observed.value_counts(normalize=True), expected.value_counts(normalize=True) if expected is not None else None
    )

    assert p >= significance_level


def assert_same_distribution(a: ArrayLike, b: ArrayLike, significance_level: float = 0.05) -> None:
    """
    Use the Kolmogorov-Smirnov test to determine if two 1-D arrays
    are likely drawn from the same underlying distribution.
    """
    _, p = ks_2samp(a, b)

    assert p >= significance_level  # type: ignore


def file_data_path(*path: str) -> str:
    """Retrieves a data file relative to tests/anonymize/data folder"""
    return os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "./data",
            *path,
        )
    )


def insert_missing_values(sr: pd.Series) -> pd.Series:
    """Returns the input Series with the first and last values as NaN."""
    out = sr.copy()
    out.iat[0] = np.nan
    out.iat[-1] = np.nan
    return out


def assert_missing_values(sr: pd.Series, preserved: bool) -> None:
    """Assert that missing values are either preserved or overwritten (i.e., no longer present).

    Intended for use in conjunction with `insert_missing_values`.
    """
    if preserved:
        assert pd.isna(sr.iat[0]) and pd.isna(sr.iat[-1])
    else:
        assert all(sr.notna())
