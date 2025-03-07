# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import pandas as pd
import pytest

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class FakeTechnique(BaseSingleColumnTechnique):
    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([1 for _ in col])


class TestBaseSingleColumnTechnique:
    @pytest.mark.parametrize(
        "dataframe", [pd.DataFrame(), pd.DataFrame({"A": range(0, 10), "B": range(10, 20)})], ids=["empty", "two-col"]
    )
    def test_anonymize_validate_dataframe(self, dataframe: pd.DataFrame):
        anonymizer = FakeTechnique()
        with pytest.raises(ValueError, match="Dataframe should have exactly one column"):
            anonymizer.anonymize(dataframe)

    def test_anonymize_dataframe_is_copied(self):
        df = pd.DataFrame({"A": range(0, 10), "B": range(10, 20)})
        anonymizer = FakeTechnique()
        out = anonymizer.anonymize(df[["A"]])

        assert isinstance(out, pd.DataFrame)
        assert (out.A == 1).all()
        assert (df.A == range(0, 10)).all()
