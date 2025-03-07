# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from numpy.random import Generator, default_rng

SeedT = int | Generator | None


class Seeder:
    """Mixin class which provides easy access to numpy `Generator`.

    Attributes:
        seed: A seed to initialize numpy `Generator`.
    """

    seed: SeedT = None

    def __init__(self, seed: SeedT = None) -> None:
        self.seed = seed
        self._generator: Generator = default_rng(seed)

    @property
    def generator(self) -> Generator:
        """Seeded numpy `Generator`."""
        return self._generator


class AlphaProbability:
    """Mixin class to assist techniques that depend on an alpha value.

    Attributes:
        alpha: A float value in the range [0, 1].
    """

    alpha: float

    def __init__(self, alpha: float) -> None:
        if not 0 <= alpha <= 1:
            raise ValueError("alpha must be between 0 and 1.")
        self.alpha = alpha
