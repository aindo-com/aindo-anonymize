# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone

import pandas as pd

from aindo.anonymize.techniques.binning import Binning


def test_binning_out_type(integer_column: pd.Series):
    anonymizer = Binning(bins=range(0, 100, 10))
    out = anonymizer.anonymize_column(integer_column)

    assert out.dtype == "category"


def test_binning_integer(integer_column: pd.Series):
    anonymizer = Binning(bins=[0, 12, 20, 30])
    out = anonymizer.anonymize_column(integer_column)

    categories: list[pd.Interval] = [
        pd.Interval(0, 12, closed="right"),
        pd.Interval(12, 20, closed="right"),
        pd.Interval(20, 30, closed="right"),
    ]

    assert integer_column.size == out.size
    assert (out.cat.categories == categories).all()


def test_binning_numerical(numerical_column: pd.Series):
    anonymizer = Binning(bins=[-1, 0, 1.5])
    out = anonymizer.anonymize_column(numerical_column)

    categories: list[pd.Interval] = [
        pd.Interval(-1, 0, closed="right"),
        pd.Interval(0, 1.5, closed="right"),
    ]

    assert numerical_column.size == out.size
    assert (out.cat.categories == categories).all()


def test_binning_datetime(datetime_column):
    anonymizer = Binning(bins=pd.date_range(datetime_column.iat[0], freq="1ME", periods=5))  # type: ignore
    out = anonymizer.anonymize_column(datetime_column)

    tzinfo: timezone = timezone.utc
    categories: pd.IntervalIndex = pd.IntervalIndex.from_tuples(
        [
            (datetime(2025, 1, 31, tzinfo=tzinfo), datetime(2025, 2, 28, tzinfo=tzinfo)),
            (datetime(2025, 2, 28, tzinfo=tzinfo), datetime(2025, 3, 31, tzinfo=tzinfo)),
            (datetime(2025, 3, 31, tzinfo=tzinfo), datetime(2025, 4, 30, tzinfo=tzinfo)),
            (datetime(2025, 4, 30, tzinfo=tzinfo), datetime(2025, 5, 31, tzinfo=tzinfo)),
        ]
    )

    assert datetime_column.size == out.size
    assert (out.cat.categories == categories).all()
