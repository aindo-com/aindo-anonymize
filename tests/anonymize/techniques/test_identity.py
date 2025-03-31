# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT


import pandas as pd

from aindo.anonymize.techniques.identity import Identity


def test_identity(dataframe_all_types: pd.DataFrame):
    anonymizer = Identity()
    out = anonymizer.anonymize(dataframe_all_types)

    assert out.equals(dataframe_all_types)
