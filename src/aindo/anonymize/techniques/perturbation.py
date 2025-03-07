# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC
from typing import Generic, Literal, TypeVar, cast

import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique
from aindo.anonymize.techniques.common import AlphaProbability, Seeder, SeedT

SamplingMode = Literal["uniform", "weighted"]
NumericsT = TypeVar("NumericsT", int, float)


class BasePerturbation(BaseSingleColumnTechnique, Seeder, AlphaProbability, ABC):
    """Base class for perturbation implementations."""

    def __init__(self, alpha: float, **kwargs: SeedT):
        Seeder.__init__(self, **kwargs)
        AlphaProbability.__init__(self, alpha)


class PerturbationNumerical(BasePerturbation, Generic[NumericsT]):
    """Implements perturbation for numerical columns.

    Perturbation consists of modify each value based on the specified perturbation intensity (alpha)
    and replacement strategy.
    It supports two modes of replacement: uniform sampling and distribution-preserving sampling.

    Attributes:
        alpha: The perturbation intensity, a value in the range [0, 1].
            - `alpha=0`: No perturbation; values remain unchanged.
            - `alpha=1`: Maximum perturbation; values are fully replaced according to the specified sampling mode.
        sampling_mode: The strategy used to sample replacement values:
            - `uniform`: Values are perturbed with random values uniformly sampled from the range [min, max].
            - `weighted`: Values are perturbed in a way to keep the original distribution.
        perturbation_range: A tuple[min, max] within which random values are sampled.
            If not set, the range is automatically computed as the minimum and maximum of the input data.
    """

    sampling_mode: SamplingMode = "uniform"
    perturbation_range: tuple[NumericsT, NumericsT] | None = None

    def __init__(
        self,
        alpha: float,
        sampling_mode: SamplingMode = "uniform",
        perturbation_range: tuple[NumericsT, NumericsT] | None = None,
        **kwargs: SeedT,
    ) -> None:
        super().__init__(alpha, **kwargs)
        self.sampling_mode = sampling_mode
        self.perturbation_range = perturbation_range

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        if self.alpha == 0.0:
            return col.copy()

        if self.sampling_mode == "weighted":
            transformer = QuantileTransformer(output_distribution="normal", n_quantiles=min(1_000, col.shape[0]))
            col_r: np.ndarray = transformer.fit_transform(col.to_numpy().reshape(-1, 1))
            random_values: np.ndarray = self.generator.normal(size=col_r.shape)
            col_r = np.sqrt(1 - self.alpha) * col_r + np.sqrt(self.alpha) * random_values
            col_r = cast(np.ndarray, transformer.inverse_transform(col_r)).reshape(-1)

            if np.issubdtype(col.dtype.type, np.integer):
                col_r = col_r.round()
            return pd.Series(col_r, dtype=col.dtype)

        else:
            perturbation_range: tuple[NumericsT, NumericsT]
            if self.perturbation_range is None:
                perturbation_range = (col.min(), col.max())
            else:
                perturbation_range = self.perturbation_range
            min_, max_ = perturbation_range

            random_values: np.ndarray = self.generator.uniform(low=min_, high=max_, size=col.size)
            col_out: pd.Series = (1 - self.alpha) * col + self.alpha * random_values
            return col_out.astype(col.dtype)


class PerturbationCategorical(BasePerturbation):
    """Implements perturbation for categorical columns.

    Perturbation consists of replacing values with randomized alternatives based on the specified
    sampling mode and perturbation intensity (alpha).
    It supports two modes of replacement: uniform sampling and distribution-preserving sampling.

    Attributes:
        alpha: The perturbation intensity, a value in the range [0, 1].
            - `alpha=0`: No perturbation; values remain unchanged.
            - `alpha=1`: Maximum perturbation; values are fully replaced according to the specified sampling mode.
        sampling_mode: The strategy used to sample replacement values:
            - `uniform`: Replaces values with others chosen uniformly at random.
            - `weighted`: Replaces values based on their original distribution.
        frequencies: Optional mapping of unique values to their relative frequencies, used for weighted sampling mode.
            Automatically computed if not provided.
    """

    sampling_mode: SamplingMode = "uniform"
    frequencies: dict[str, float] | None = None

    def __init__(
        self,
        alpha: float,
        sampling_mode: SamplingMode = "uniform",
        frequencies: dict[str, float] | None = None,
        **kwargs: SeedT,
    ) -> None:
        super().__init__(alpha, **kwargs)
        self.sampling_mode = sampling_mode
        self.frequencies = frequencies

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        frequencies: dict[str, float]
        if self.frequencies is None:
            value_counts: pd.Series = col.value_counts(normalize=True)
            frequencies = dict(zip(value_counts.index.to_numpy(), value_counts.values))
        else:
            frequencies = self.frequencies

        categories: np.ndarray = np.array(list(frequencies))
        probabilities: np.ndarray | None = (
            np.array(list(frequencies.values())) if self.sampling_mode == "weighted" else None
        )
        rand_values = self.generator.choice(categories, size=col.size, p=probabilities)

        return pd.Series(np.where(self.generator.random() <= self.alpha, rand_values, col), dtype="category")
