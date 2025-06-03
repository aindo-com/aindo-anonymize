# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from datetime import date, datetime, time, timedelta, timezone
from typing import Literal

import numpy as np
import pandas as pd
import pytest
from faker import Faker

DEFAULT_SCOPE: Literal["session"] = "session"
SEED: Literal[12345] = 12345
COL_SIZE: Literal[100] = 100
INT_TYPE: pd.Int64Dtype = pd.Int64Dtype()
FLOAT_TYPE: type = np.float64
COLUMN_NAMES: list[str] = ["integer", "numerical", "categorical", "string", "date", "datetime", "time"]


@pytest.fixture(scope=DEFAULT_SCOPE)
def rng() -> np.random.Generator:
    return np.random.default_rng(SEED)


@pytest.fixture(scope=DEFAULT_SCOPE)
def faker() -> Faker:
    """
    Fixture that returns a seeded and suitable `Faker` instance.
    """
    fake = Faker(locale="en_US", use_weighting=False)
    fake.seed_instance(SEED)
    fake.unique.clear()
    return fake


@pytest.fixture(scope=DEFAULT_SCOPE)
def integer_column(rng: np.random.Generator) -> pd.Series:
    values: list[int] = [int(val) for val in rng.binomial(n=40, p=0.5, size=COL_SIZE)]
    return pd.Series(sorted(values), dtype=INT_TYPE)


@pytest.fixture(scope=DEFAULT_SCOPE)
def numerical_column(rng: np.random.Generator) -> pd.Series:
    return pd.Series(sorted(rng.normal(loc=0, scale=0.5, size=COL_SIZE)), dtype=FLOAT_TYPE)


@pytest.fixture(scope=DEFAULT_SCOPE)
def categorical_column() -> pd.Series:
    categories: list[str] = [f"CATEGORY_{x}" for x in range(0, 6)]
    frequencies: list[float] = [0.01, 0.08, 0.15, 0.2, 0.26, 0.3]
    assert sum(frequencies) == 1
    values: list[str] = []
    for category, freq in zip(categories, frequencies):
        values += [category] * int(freq * COL_SIZE)
    assert len(values) == COL_SIZE
    return pd.Series(values, dtype="category")


@pytest.fixture(scope=DEFAULT_SCOPE)
def string_column(faker: Faker) -> pd.Series:
    return pd.Series([faker.name() for _ in range(0, COL_SIZE)])


@pytest.fixture(scope=DEFAULT_SCOPE)
def datetime_column() -> pd.Series:
    start_date: datetime = datetime(2025, 1, 1, tzinfo=timezone.utc)
    values: list[datetime] = [start_date + timedelta(days=i) for i in range(COL_SIZE)]
    return pd.Series(values)


@pytest.fixture(scope=DEFAULT_SCOPE)
def date_column() -> pd.Series:
    start_date: datetime = datetime(2025, 1, 1, tzinfo=timezone.utc)
    values: list[date] = [(start_date + timedelta(days=i)).date() for i in range(COL_SIZE)]
    return pd.Series(values)


@pytest.fixture(scope=DEFAULT_SCOPE)
def time_column() -> pd.Series:
    start_date: datetime = datetime(2025, 1, 1, tzinfo=timezone.utc)
    values: list[time] = [(start_date + timedelta(days=i)).time() for i in range(COL_SIZE)]
    return pd.Series(values)


@pytest.fixture(scope=DEFAULT_SCOPE)
def dataframe_all_types(
    integer_column: pd.Series,
    numerical_column: pd.Series,
    categorical_column: pd.Series,
    string_column: pd.Series,
    datetime_column: pd.Series,
    date_column: pd.Series,
    time_column: pd.Series,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "integer_column": integer_column,
            "numerical_column": numerical_column,
            "categorical_column": categorical_column,
            "string_column": string_column,
            "datetime_column": datetime_column,
            "date_column": date_column,
            "time_column": time_column,
        }
    )
