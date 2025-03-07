# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import re
from typing import Literal

import pandas as pd
import pytest

from aindo.anonymize.techniques.hashing import KeyHashing
from tests.anonymize.conftest import COLUMN_NAMES

SECRET_KEY: Literal["secret"] = "secret"
SALT: Literal["salt"] = "salt"
HASH_PATTERN: re.Pattern = re.compile(r"^[-A-Za-z0-9+/]*={0,3}$")


def wrong_hash_name():
    with pytest.raises(ValueError, match="Algorithm 'wrong' not available"):
        KeyHashing(key="key", hash_name="wrong")


def test_different_salts():
    data = pd.Series([1])
    anonymizer1 = KeyHashing(key=SECRET_KEY, salt=SALT)
    out1 = anonymizer1.anonymize_column(data)[0]
    anonymizer2 = KeyHashing(key=SECRET_KEY, salt="new salt")
    out2 = anonymizer2.anonymize_column(data)[0]

    assert out1 != out2


def test_salt_generation():
    assert KeyHashing.generate_salt() != KeyHashing.generate_salt()


@pytest.mark.parametrize("column_type", COLUMN_NAMES)
def test_hashing(column_type: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(f"{column_type}_column")
    anonymizer = KeyHashing(key=SECRET_KEY, salt=SALT)
    out = anonymizer.anonymize_column(column)

    assert column.size == out.size
    assert out.apply(lambda x: bool(HASH_PATTERN.match(x))).all()
