# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

"""A high-level interface for orchestrating the anonymization process."""

import itertools
from typing import cast

import pandas as pd

from aindo.anonymize.config import BaseSpec, Config


class AnonymizationPipeline:
    """A high-level interface for orchestrating the anonymization process.

    This class provides a quick way to apply anonymization techniques to a dataset,
    allowing users to run anonymization pipelines with minimal setup.

    The resulting dataset will contain only the columns where a technique has been applied.
    To retain a column with its original data, use the Identity technique.

    Attributes:
        config: Configuration that specifies the anonymization steps to execute.
    """

    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Runs the anonymization steps defined in the configuration against the input data.

        Args:
            dataframe: The input data to be anonymized.

        Returns:
            The anonymized version of the input data.
        """
        if len(self.config.steps) == 0:
            return pd.DataFrame()

        with pd.option_context("mode.copy_on_write", True):
            used_cols: set[str] = set(
                itertools.chain.from_iterable(step.columns or dataframe.columns for step in self.config.steps)
            )
            unused_cols: set[str] = set(dataframe.columns.to_list()) - used_cols
            result: pd.DataFrame = dataframe.drop(labels=cast(list, unused_cols), axis=1)

            for step in self.config.steps:
                method: BaseSpec = step.method
                if step.columns:
                    anonymized: pd.DataFrame = method.anonymize(result.loc[:, step.columns])
                    if not method.preserve_type:
                        for col_name, dtype in anonymized.dtypes.to_dict().items():
                            result[col_name] = result[col_name].astype(dtype)
                    result.loc[:, step.columns] = anonymized

                else:
                    result = method.anonymize(result)

            return result
