# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import pandas as pd
import pytest

from aindo.anonymize.techniques.data_nulling import DataNulling
from tests.anonymize.conftest import COLUMN_NAMES


@pytest.mark.parametrize("column_type", COLUMN_NAMES)
def test_data_nulling(column_type: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(f"{column_type}_column")
    anonymizer = DataNulling(constant_value="BLANK")
    out = anonymizer.anonymize_column(column)

    assert column.size == out.size
    assert (out == "BLANK").all()
