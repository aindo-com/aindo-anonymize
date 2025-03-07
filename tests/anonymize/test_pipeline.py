# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Any

import pandas as pd

from aindo.anonymize.config import Config
from aindo.anonymize.pipeline import AnonymizationPipeline
from aindo.anonymize.techniques import KeyHashing, PerturbationNumerical
from tests.anonymize.conftest import SEED

EXAMPLE_CONFIG: Config = Config.from_dict(
    {
        "steps": [
            {
                "name": "perturbation",
                "columns": ["integer_column"],
                "method": {"type": "perturbation_numerical", "alpha": 0.1, "seed": SEED},
            },
            {
                "name": "hash",
                "columns": ["string_column"],
                "method": {"type": "key_hashing", "key": "secret key", "salt": "secret salt", "hash_name": "sha256"},
            },
        ],
    }
)


def test_run(string_column: pd.Series, integer_column: pd.Series):
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


def test_run_check_copy():
    # Verify that input columns not subject to anonymization remain unchanged
    # and original dataframe is not modified.
    df = pd.DataFrame({"string_column": ["A", "B", "C"], "integer_column": [1, 2, 3]})
    config_data: dict[str, Any] = {
        "steps": [
            {
                "name": "nulling",
                "columns": ["integer_column"],
                "method": {"type": "data_nulling", "constant_value": "BLANK"},
            }
        ]
    }
    workflow = AnonymizationPipeline(config=Config.from_dict(config_data))
    out = workflow.run(df)

    assert df.string_column.equals(pd.Series(["A", "B", "C"]))
    assert df.integer_column.equals(pd.Series([1, 2, 3]))

    assert out.string_column.equals(df.string_column)
    assert out.integer_column.equals(pd.Series(["BLANK" for _ in [1, 2, 3]]))
