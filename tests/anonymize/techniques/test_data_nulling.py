# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import pandas as pd
import pytest

from aindo.anonymize.techniques.data_nulling import DataNulling
from tests.anonymize.conftest import COLUMN_NAMES
from tests.anonymize.utils import assert_missing_values, insert_missing_values


@pytest.mark.parametrize("column_type", COLUMN_NAMES)
def test_data_nulling(column_type: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(f"{column_type}_column")
    anonymizer = DataNulling(constant_value="BLANK")
    out = anonymizer.anonymize_column(column)

    assert column.size == out.size
    assert (out == "BLANK").all()


def test_constant_is_none(integer_column: pd.Series):
    anonymizer = DataNulling(constant_value=None)
    out = anonymizer.anonymize_column(integer_column)

    assert (out.isna()).all()
    assert out.dtype == object


def test_with_missing_values(string_column: pd.Series):
    anonymizer = DataNulling(constant_value="BLANK")
    input = insert_missing_values(string_column)
    out: pd.Series = anonymizer.anonymize_column(input)

    assert_missing_values(out, preserved=False)
