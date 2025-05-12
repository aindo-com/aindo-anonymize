# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Literal, get_args

import pandas as pd
import pytest
from faker import Faker

from aindo.anonymize.techniques.mocking import Mocking, MockingGeneratorMethods
from tests.anonymize.conftest import SEED
from tests.anonymize.utils import assert_missing_values, insert_missing_values


def test_mocking_wrong_param():
    with pytest.raises(ValueError, match="Faker's generator method 'wrong-method' not found"):
        Mocking(data_generator="wrong-method")  # type: ignore


def test_mocking(string_column: pd.Series):
    anonymizer = Mocking(data_generator="url", seed=SEED)
    out: pd.Series = anonymizer.anonymize_column(string_column)

    assert string_column.size == out.size
    assert (string_column != out).all()
    for value in out.values:
        assert value
        assert isinstance(value, str)


def test_faker_with_args():
    anonymizer = Mocking(data_generator="name")
    assert len(anonymizer._fake.providers) > 1

    anonymizer = Mocking(data_generator="name", faker_kwargs={"providers": ["faker.providers.person"]})
    assert len(anonymizer._fake.providers) == 1


def test_faker_generator_with_args():
    domain: Literal["aindo.com"] = "aindo.com"
    anonymizer = Mocking(data_generator="email", faker_generator_kwargs={"domain": "aindo.com"}, seed=SEED)
    out: pd.Series = anonymizer.anonymize_column(pd.Series(["0"]))

    assert domain in out.at[0]


def test_faker_generator_methods():
    # This test ensures that all names inside MockingGeneratorMethods exist in a Faker instance,
    # allowing us to track missing generator methods across Faker upgrades.
    # Note: This does not guarantee that the method exists in all supported Faker versions.
    fake = Faker()
    methods: tuple[str] = get_args(MockingGeneratorMethods)
    for method_name in methods:
        method = getattr(fake, method_name, None)
        assert method is not None


def test_with_missing_values(string_column: pd.Series):
    anonymizer = Mocking(data_generator="name")
    input = insert_missing_values(string_column)
    out: pd.Series = anonymizer.anonymize_column(input)

    assert_missing_values(out, preserved=False)
