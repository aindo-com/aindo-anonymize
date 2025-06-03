# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Any

import pandas as pd

from aindo.anonymize.config import Config
from aindo.anonymize.pipeline import AnonymizationPipeline
from aindo.anonymize.techniques import KeyHashing, PerturbationNumerical
from tests.anonymize.conftest import SEED
from tests.anonymize.utils import assert_missing_values, insert_missing_values

EXAMPLE_CONFIG: Config = Config.from_dict(
    {
        "steps": [
            {
                "columns": ["integer_column"],
                "method": {"type": "perturbation_numerical", "alpha": 0.1, "seed": SEED},
            },
            {
                "columns": ["string_column"],
                "method": {"type": "key_hashing", "key": "secret key", "salt": "secret salt", "hash_name": "sha256"},
            },
        ],
    }
)


def test_simple_run(string_column: pd.Series, integer_column: pd.Series):
    dataframe = pd.DataFrame({"string_column": string_column, "integer_column": integer_column})
    workflow = AnonymizationPipeline(EXAMPLE_CONFIG)
    out: pd.DataFrame = workflow.run(dataframe)

    assert isinstance(out, pd.DataFrame)
    assert out.columns.to_list() == ["string_column", "integer_column"]

    perturbation = PerturbationNumerical(alpha=0.1, seed=SEED)
    col_out = perturbation.anonymize_column(integer_column)
    assert out["integer_column"].equals(col_out)

    hashing = KeyHashing(key="secret key", salt="secret salt")
    col_out = hashing.anonymize_column(string_column)
    assert out["string_column"].equals(col_out)


def test_check_copy():
    # Verify that original dataframe is not modified.
    df = pd.DataFrame({"string_column": ["A", "B", "C"], "integer_column": [1, 2, 3]})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "columns": ["integer_column"],
                "method": {"type": "data_nulling", "constant_value": "BLANK"},
            }
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert df.string_column.equals(pd.Series(["A", "B", "C"]))
    assert df.integer_column.equals(pd.Series([1, 2, 3]))

    assert out.integer_column.equals(pd.Series(["BLANK" for _ in [1, 2, 3]]))


def test_unused_cols():
    df = pd.DataFrame({"string_column": ["A", "B", "C"], "integer_column": [1, 2, 3]})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "columns": ["integer_column"],
                "method": {"type": "data_nulling", "constant_value": "BLANK"},
            }
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert out.columns.to_list() == ["integer_column"]


def test_repetition():
    # This test ensures that techniques are applied to previously anonymized columns.
    # Normally, character masking cannot be applied to an integer column,
    # but here, data nulling is applied first, transforming the type to string.
    df = pd.DataFrame({"integer_column": [1, 2, 3]})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "columns": ["integer_column"],
                "method": {"type": "data_nulling", "constant_value": "BLANK"},
            },
            {
                "columns": ["integer_column"],
                "method": {"type": "character_masking", "mask_length": 3, "starting_direction": "right"},
            },
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert out.integer_column.equals(pd.Series(["BL***", "BL***", "BL***"]))


def test_anonymize_all_dataframe():
    df = pd.DataFrame({"string_column": ["A", "B", "C"], "integer_column": [1, 2, 3]})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "method": {"type": "identity"},
            }
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert out.equals(df)


def test_with_missing_values(string_column: pd.Series, integer_column: pd.Series):
    dataframe = pd.DataFrame(
        {"string_column": insert_missing_values(string_column), "integer_column": insert_missing_values(integer_column)}
    )
    workflow = AnonymizationPipeline(EXAMPLE_CONFIG)
    out: pd.DataFrame = workflow.run(dataframe)

    assert isinstance(out, pd.DataFrame)
    assert_missing_values(out["string_column"], preserved=True)
    assert_missing_values(out["integer_column"], preserved=True)


def test_change_of_dtype(integer_column: pd.Series):
    df = pd.DataFrame({"integer_column": integer_column})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "columns": ["integer_column"],
                "method": {"type": "binning", "bins": 10},
            }
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert isinstance(out, pd.DataFrame)
    assert out["integer_column"].dtype == "category"
