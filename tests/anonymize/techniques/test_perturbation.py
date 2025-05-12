# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import get_args

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from aindo.anonymize.techniques.perturbation import PerturbationCategorical, PerturbationNumerical, SamplingMode
from tests.anonymize.conftest import FLOAT_TYPE, INT_TYPE
from tests.anonymize.utils import assert_categorical_distribution, assert_same_distribution


class TestPerturbationNumerical:
    alpha: float = 0.5

    def test_has_random_generator(self):
        anonymizer = PerturbationNumerical[FLOAT_TYPE](self.alpha)
        assert anonymizer.generator

    @pytest.mark.parametrize("column_name", ["integer_column", "numerical_column"])
    def test_out_type(self, rng: np.random.Generator, column_name: str, request: pytest.FixtureRequest):
        column: pd.Series = request.getfixturevalue(column_name)
        _type = FLOAT_TYPE if column_name.startswith("numerical") else INT_TYPE
        anonymizer = PerturbationNumerical[_type](alpha=1, seed=rng)
        out = anonymizer.anonymize_column(column)

        assert out.dtype == column.dtype == _type

    @pytest.mark.parametrize(
        "sampling_mode",
        get_args(SamplingMode),
        ids=[f"sampling_{val}" for val in get_args(SamplingMode)],
    )
    def test_no_perturbation(self, rng: np.random.Generator, numerical_column: pd.Series, sampling_mode: SamplingMode):
        anonymizer = PerturbationNumerical[FLOAT_TYPE](alpha=0, sampling_mode=sampling_mode, seed=rng)
        out: pd.Series = anonymizer.anonymize_column(numerical_column)

        assert numerical_column.equals(out)

    @pytest.mark.parametrize("column_name", ["integer_column", "numerical_column"])
    def test_full_perturbation_uniform(
        self, rng: np.random.Generator, column_name: str, request: pytest.FixtureRequest
    ):
        column: pd.Series = request.getfixturevalue(column_name)
        _type = FLOAT_TYPE if column_name.startswith("numerical") else INT_TYPE
        anonymizer = PerturbationNumerical[_type](alpha=1, sampling_mode="uniform", seed=rng)
        out = anonymizer.anonymize_column(column)

        min: float = column.min()
        max: float = column.max()
        uniform_var = stats.uniform.rvs(loc=min, scale=(max - min), random_state=rng)
        assert_same_distribution(out, uniform_var)

    @pytest.mark.parametrize("column_name", ["integer_column", "numerical_column"])
    def test_full_perturbation_weighted(
        self, rng: np.random.Generator, column_name: str, request: pytest.FixtureRequest
    ):
        column: pd.Series = request.getfixturevalue(column_name)
        anonymizer = PerturbationNumerical[FLOAT_TYPE](alpha=1, sampling_mode="weighted", seed=rng)
        out: pd.Series = anonymizer.anonymize_column(column)

        assert_same_distribution(column, out)


class TestPerturbationCategorical:
    def test_has_random_generator(self):
        anonymizer = PerturbationCategorical(0.5)

        assert anonymizer.generator

    def test_out_type(self, rng: np.random.Generator, categorical_column: pd.Series):
        anonymizer = PerturbationCategorical(alpha=1, seed=rng)
        out = anonymizer.anonymize_column(categorical_column)

        assert out.dtype == "category"

    @pytest.mark.parametrize(
        "sampling_mode",
        get_args(SamplingMode),
        ids=[f"sampling_{val}" for val in get_args(SamplingMode)],
    )
    def test_no_perturbation(
        self, rng: np.random.Generator, categorical_column: pd.Series, sampling_mode: SamplingMode
    ):
        anonymizer = PerturbationCategorical(alpha=0, sampling_mode=sampling_mode, seed=rng)
        out: pd.Series = anonymizer.anonymize_column(categorical_column)

        assert categorical_column.equals(out)

    def test_full_perturbation_uniform(self, rng: np.random.Generator, categorical_column: pd.Series):
        anonymizer = PerturbationCategorical(alpha=1, sampling_mode="uniform", seed=rng)
        out = anonymizer.anonymize_column(categorical_column)

        assert categorical_column.cat.categories.equals(out.cat.categories)
        assert_categorical_distribution(out)

    def test_full_perturbation_weighted(
        self,
        rng: np.random.Generator,
        categorical_column: pd.Series,
    ):
        anonymizer = PerturbationCategorical(alpha=1, sampling_mode="weighted", seed=rng)
        out = anonymizer.anonymize_column(categorical_column)

        assert categorical_column.cat.categories.equals(out.cat.categories)
        assert_categorical_distribution(out, categorical_column)
