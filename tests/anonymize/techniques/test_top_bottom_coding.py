# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import Any

import pandas as pd
import pytest

from aindo.anonymize.techniques.top_bottom_coding import TopBottomCodingCategorical, TopBottomCodingNumerical


class TestTopBottomCodingNumerical:
    q: float = 0.04

    @pytest.mark.parametrize(
        "params,error_message",
        [
            ({"q": -0.1}, "The threshold 'q' should be"),
            ({"q": 2.1}, "The threshold 'q' should be"),
            ({"upper_value": 0.1}, "Quantile values"),
            ({"lower_value": 0.1}, "Quantile values"),
            ({}, "Either the threshold 'q' or"),
            ({"q": 1, "upper_value": 0.1, "lower_value": 0.1}, "Either the threshold 'q' or"),
        ],
        ids=[
            "q-lower-bound",
            "q-upper-bound",
            "quantiles-not-matching-1",
            "quantiles-not-matching-2",
            "quantiles-and-q-1",
            "quantiles-and-q-2",
        ],
    )
    def test_wrong_param(self, params: dict[str, Any], error_message: str):
        with pytest.raises(ValueError, match=error_message):
            TopBottomCodingNumerical(**params)

    @pytest.mark.parametrize("column_name", ["integer_column", "numerical_column"])
    def test_replacing(self, column_name: str, request: pytest.FixtureRequest):
        column: pd.Series = request.getfixturevalue(column_name)
        anonymizer = TopBottomCodingNumerical(self.q)
        out = anonymizer.anonymize_column(column)

        assert column.size == out.size
        # first two values are replaced and equals, same for last two
        assert (out[:2] == out[0]).all()
        assert (out[-2:] == out.iat[-1]).all()

    def test_replacing_none(self, integer_column: pd.Series):
        anonymizer = TopBottomCodingNumerical(0)
        out = anonymizer.anonymize_column(integer_column)

        assert (integer_column == out).all()

    def test_replacing_all(self, integer_column: pd.Series):
        anonymizer = TopBottomCodingNumerical(1)
        out = anonymizer.anonymize_column(integer_column)

        median: float = integer_column.median()
        assert (out == median).all()


class TestTopBottomCodingCategorical:
    q: float = 0.1

    @pytest.mark.parametrize(
        "params,error_message",
        [
            ({"q": -0.1}, "The value 'q' should"),
            ({"q": 1.1}, "The value 'q' should"),
            ({"q": 0, "other_label": None}, "The new category"),
            ({}, "Either 'q' or 'rare_categories'"),
            ({"q": 1, "rare_categories": ["A"]}, "Either 'q' or 'rare_categories'"),
        ],
        ids=["q-lower-bound", "q-upper-bound", "other_label", "q-rand-are_categories-1", "q-rand-are_categories-2"],
    )
    def test_wrong_param(self, params: dict[str, Any], error_message: str):
        with pytest.raises(ValueError, match=error_message):
            TopBottomCodingCategorical(**params)

    def test_out_type(self, categorical_column: pd.Series):
        anonymizer = TopBottomCodingCategorical(self.q)
        out = anonymizer.anonymize_column(categorical_column)

        assert out.dtype == "category"

    def test_rare_categories_set(self):
        anonymizer = TopBottomCodingCategorical(rare_categories=["C"])
        out = anonymizer.anonymize_column(pd.Series(["A", "A", "B", "B", "C"], dtype="category"))

        assert "OTHER" in out.cat.categories
        assert "C" not in out.cat.categories

    def test_replacing(self, categorical_column: pd.Series):
        # Test the replace of CATEGORY_0 and CATEGORY_1.
        # Set the threshold just above CATEGORY_1 frequency.
        anonymizer = TopBottomCodingCategorical(0.081)
        out = anonymizer.anonymize_column(categorical_column)

        assert categorical_column.size == out.size
        categories: set[str] = set(categorical_column.cat.categories) - {"CATEGORY_0", "CATEGORY_1"}
        categories.add(TopBottomCodingCategorical.other_label)
        assert categories == set(out.cat.categories)
        assert out.value_counts(normalize=True).loc[TopBottomCodingCategorical.other_label] == 0.09

    def test_replacing_none(self, categorical_column: pd.Series):
        anonymizer = TopBottomCodingCategorical(0)
        out = anonymizer.anonymize_column(categorical_column)

        assert (out.cat.categories == categorical_column.cat.categories).all()
        assert (categorical_column == out).all()

    def test_replacing_all(self, categorical_column: pd.Series):
        anonymizer = TopBottomCodingCategorical(1)
        out = anonymizer.anonymize_column(categorical_column)

        assert len(out.cat.categories) == 1
        assert out.cat.categories[0] == TopBottomCodingCategorical.other_label
        assert (out.values == TopBottomCodingCategorical.other_label).all()
