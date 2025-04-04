# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import json
from typing import Any

import pandas as pd
import pytest

from aindo.anonymize.config import (
    ALL_TECHNIQUES,
    ALL_TECHNIQUES_SPEC,
    Config,
    TechniqueItem,
    TechniqueType,
    _get_type_from_class,
)
from tests.anonymize.conftest import SEED
from tests.anonymize.utils import file_data_path


@pytest.fixture(scope="module")
def full_config() -> dict:
    """Return the complete configuration as a dictionary."""
    # Note: full_config file should contain all the techniques with all parameters.
    with open(file_data_path("full_config.json"), "r") as filein:
        config_data: dict = json.load(filein)
    return config_data


def test_get_type_from_class():
    for _cls, _type in zip(ALL_TECHNIQUES, TechniqueType):
        out: TechniqueType = _get_type_from_class(_cls)
        assert out == _type

    for _cls, _type in zip(ALL_TECHNIQUES_SPEC, TechniqueType):
        out: TechniqueType = _get_type_from_class(_cls)
        assert out == _type


@pytest.mark.parametrize(
    "params,technique_cls,spec_cls,columns",
    [
        ({"bins": 10}, ALL_TECHNIQUES[0], ALL_TECHNIQUES_SPEC[0], ["integer"]),  # binning
        ({"mask_length": 3}, ALL_TECHNIQUES[1], ALL_TECHNIQUES_SPEC[1], ["string"]),  # char masking
        ({"constant_value": "BLANK"}, ALL_TECHNIQUES[2], ALL_TECHNIQUES_SPEC[2], ["string"]),  # data nulling
        ({"key": "key"}, ALL_TECHNIQUES[3], ALL_TECHNIQUES_SPEC[3], ["integer"]),  # key hashing
        ({}, ALL_TECHNIQUES[4], ALL_TECHNIQUES_SPEC[4], ["integer", "string"]),  # identity
        ({"data_generator": "name", "seed": SEED}, ALL_TECHNIQUES[5], ALL_TECHNIQUES_SPEC[5], ["string"]),  # mocking
        ({"alpha": 0.5, "seed": SEED}, ALL_TECHNIQUES[6], ALL_TECHNIQUES_SPEC[6], ["categorical"]),  # perturbation cat
        ({"alpha": 0.5, "seed": SEED}, ALL_TECHNIQUES[7], ALL_TECHNIQUES_SPEC[7], ["integer"]),  # perturbation num
        ({"alpha": 0.5, "seed": SEED}, ALL_TECHNIQUES[8], ALL_TECHNIQUES_SPEC[8], ["integer"]),  # swapping
        ({"q": 0.2}, ALL_TECHNIQUES[9], ALL_TECHNIQUES_SPEC[9], ["categorical"]),  # top/bottom coding cat
        ({"q": 0.2}, ALL_TECHNIQUES[10], ALL_TECHNIQUES_SPEC[10], ["integer"]),  # top/bottom coding num
    ],
    ids=[c.__name__ for c in ALL_TECHNIQUES],
)
def test_spec_classes(
    params: dict[str, Any],
    technique_cls: type,
    spec_cls: type,
    columns: list[str],
    dataframe_all_types: pd.DataFrame,
):
    # Verify that "Spec" classes are, aside from the type attribute, identical to their corresponding technique class,
    # particularly that initialization behaves as expected.
    # For example, previous implementations with dataclasses had issues with parent class initialization methods.
    df = dataframe_all_types.loc[:, [f"{c}_column" for c in columns]]
    technique = technique_cls(**params)
    t_out = technique.anonymize(df)
    spec = spec_cls(**params)
    s_out = spec.anonymize(df)

    assert t_out.equals(s_out)


class TestTechniqueItem:
    @pytest.mark.parametrize(
        "value,expected_match",
        [
            ({}, "Invalid input: 'method'"),
            ({"method": {"constant_value": None}}, "Invalid input: 'method'"),
            ({"method": {"type": "wrong-type"}}, "Invalid input: unknown technique"),
            ({"method": {"type": "identity"}, "columns": []}, "Invalid input: the columns list cannot be empty"),
        ],
        ids=["missing-method", "missing-type", "unknown-technique", "empty-columns-list"],
    )
    def test_from_dict_error(self, value: dict[str, Any], expected_match: str):
        with pytest.raises(ValueError, match=expected_match):
            TechniqueItem.from_dict(value)

    def test_from_dict_ok(self, full_config: dict):
        for technique_dict in full_config["steps"]:
            t = TechniqueItem.from_dict(technique_dict)
            assert t and isinstance(t, TechniqueItem)

    def test_to_dict(self, full_config: dict):
        for technique_dict in full_config["steps"]:
            t = TechniqueItem.from_dict(technique_dict)
            out_dict = t.to_dict()
            # Remove unset attributes since we don't have them in the written config
            out_dict["method"] = {k: v for k, v in out_dict["method"].items() if v is not None}
            assert technique_dict == out_dict

    @pytest.mark.parametrize(
        "a,b,result",
        [
            ({"type": "swapping", "alpha": 0.8}, {"type": "swapping", "alpha": 0.8}, True),
            (
                {"type": "swapping", "alpha": 0.8, "seed": None},
                {"type": "swapping", "alpha": 0.8},
                True,
            ),
            ({"type": "swapping", "alpha": 0.8}, {"type": "swapping", "alpha": 0}, False),
            ({"type": "data_nulling"}, {"type": "swapping", "alpha": 0}, False),
        ],
        ids=["same-param", "seed-is-None", "diff-param", "diff-technique"],
    )
    def test_equality(self, a: dict, b: dict, result: bool):
        t1 = TechniqueItem.from_dict({"method": a, "columns": ["a"]})
        t2 = TechniqueItem.from_dict({"method": b, "columns": ["a"]})
        assert (t1 == t2) == result


class TestConfig:
    def test_from_dict_error(self):
        with pytest.raises(ValueError, match="Invalid input: 'steps'"):
            Config.from_dict({})

    def test_from_dict_ok(self, full_config: dict):
        c = Config.from_dict(full_config)
        assert c and isinstance(c, Config)

    def test_to_dict(self, full_config: dict):
        c = Config.from_dict(full_config)
        out_dict = c.to_dict()
        assert isinstance(out_dict["steps"], list) and len(out_dict["steps"]) == len(c.steps)

    def test_full_config(self, full_config: dict):
        # Test a complete configuration to ensure every technique is correctly loaded
        conf: Config = Config.from_dict(full_config)

        assert conf and isinstance(conf, Config)
