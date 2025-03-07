# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import pandas as pd

from aindo.anonymize.config import BaseSpec, Config


class AnonymizationPipeline:
    """A high-level interface for orchestrating the anonymization process.

    This class provides a quick way to apply anonymization techniques to a dataset,
    allowing users to run anonymization pipelines with minimal setup.

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
        with pd.option_context("mode.copy_on_write", True):
            result: pd.DataFrame = dataframe.copy()
            for step in self.config.steps:
                method: BaseSpec = step.method
                if step.columns is not None:
                    anonymized: pd.DataFrame = method.anonymize(dataframe.loc[:, step.columns])
                    if not method.preserve_type:
                        for col_name, dtype in anonymized.dtypes.to_dict().items():
                            result[col_name] = result[col_name].astype(dtype)
                    result.loc[:, step.columns] = anonymized

                else:
                    result = method.anonymize(result)

            return result
