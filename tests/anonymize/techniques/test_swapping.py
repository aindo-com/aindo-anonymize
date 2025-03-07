# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd
import pytest

from aindo.anonymize.techniques.swapping import Swapping
from tests.anonymize.conftest import COLUMN_NAMES


def test_has_random_generator():
    anonymizer = Swapping(alpha=1)
    assert anonymizer.generator


def test_no_swapping(rng: np.random.Generator, numerical_column: pd.Series):
    anonymizer = Swapping(alpha=0, seed=rng)
    out: pd.Series = anonymizer.anonymize_column(numerical_column)

    assert out.equals(numerical_column)


@pytest.mark.parametrize("column_type", COLUMN_NAMES)
def test_full_swapping(rng: np.random.Generator, column_type: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(f"{column_type}_column")
    anonymizer = Swapping(alpha=1, seed=rng)
    out: pd.Series = anonymizer.anonymize_column(column)

    assert out.size == column.size
    assert set(out) == set(column)
