# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Literal

import pandas as pd
import pytest

from aindo.anonymize.techniques.char_masking import CharacterMasking, StartingDirection


@pytest.mark.parametrize("column_name", ["string_column", "categorical_column"])
def test_masking_direction_left(column_name: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(column_name)
    mask_length: Literal[3] = 3
    anonymizer = CharacterMasking[str](starting_direction="left", mask_length=mask_length)
    out: pd.Series = anonymizer.anonymize_column(column)

    assert column.size == out.size
    for original, anonymized in zip(column.values, out.values):
        assert anonymized[:mask_length] == anonymizer.symbol * mask_length
        assert original[mask_length:] == anonymized[mask_length:]


@pytest.mark.parametrize("column_name", ["string_column", "categorical_column"])
def test_masking_direction_right(column_name: str, request: pytest.FixtureRequest):
    column: pd.Series = request.getfixturevalue(column_name)
    mask_length: Literal[3] = 3
    anonymizer = CharacterMasking[str](starting_direction="right", mask_length=mask_length)
    out: pd.Series = anonymizer.anonymize_column(column)

    assert column.size == out.size
    for original, anonymized in zip(column.values, out.values):
        assert anonymized[-mask_length:] == anonymizer.symbol * mask_length
        assert original[:-mask_length] == anonymized[:-mask_length]


@pytest.mark.parametrize("mask_length", ("max", -1))
@pytest.mark.parametrize("starting_direction", ("left", "right"))
def test_masking_full_mask(starting_direction: StartingDirection, mask_length: str | int, string_column: pd.Series):
    _mask_len: int
    if isinstance(mask_length, str):
        _mask_len: int = string_column.str.len().max()
    else:
        _mask_len = mask_length
    anonymizer = CharacterMasking[str](starting_direction=starting_direction, mask_length=_mask_len)
    out: pd.Series = anonymizer.anonymize_column(string_column)

    assert string_column.size == out.size
    for _, value in out.items():
        assert value == anonymizer.symbol * len(value)


@pytest.mark.parametrize(
    "param_name, param_value",
    [("mask_length", -2), ("symbol", "XX")],
    ids=["mask_length", "symbol"],
)
def test_masking_wrong_param(param_name: str, param_value: int | str):
    with pytest.raises(ValueError):
        CharacterMasking(**{param_name: param_value})  # type: ignore


def test_masking_symbol(string_column: pd.Series):
    symbol: Literal["X"] = "X"
    anonymizer = CharacterMasking[str](mask_length=1, symbol=symbol)
    out: pd.Series = anonymizer.anonymize_column(string_column)

    assert string_column.size == out.size
    for _, value in out.items():
        assert value[0] == symbol
