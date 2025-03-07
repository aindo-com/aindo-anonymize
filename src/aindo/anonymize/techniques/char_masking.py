# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from typing import AnyStr, ClassVar, Generic, Literal

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique

StartingDirection = Literal["left", "right"]


class CharacterMasking(BaseSingleColumnTechnique, Generic[AnyStr]):
    """Implements character masking.

    Character masking involves replacing, usually partially, the characters of a data value
    with a constant symbol.
    Full masking is achieved by setting `mask_length=-1`.

    Attributes:
        starting_direction: The direction in which masking starts. Default is "left".
        mask_length: The number of characters to mask.
            Set to -1 to mask the entire value.
            Defaults to 1.
        symbol: The symbol used for masking. Defaults to "*".
    """

    preserve_type: ClassVar[bool] = False

    mask_length: int = 1
    symbol: AnyStr = "*"  # type: ignore
    starting_direction: StartingDirection = "left"

    def __init__(
        self,
        mask_length: int = 1,
        symbol: AnyStr = "*",
        starting_direction: StartingDirection = "left",
    ) -> None:
        super().__init__()
        if (mask_length <= 0) and (mask_length != -1):
            raise ValueError("mask_length should be greater than zero or equal to -1")
        if len(symbol) != 1:
            raise ValueError("symbol should be a single character")

        self.starting_direction = starting_direction
        self.mask_length = mask_length
        self.symbol = symbol

    def _compute_mask(self, value: AnyStr) -> AnyStr:
        if self.mask_length == -1:
            return self.symbol * len(value)

        _mask_len: int = min(self.mask_length, len(value))
        mask: AnyStr = self.symbol * _mask_len
        if self.starting_direction == "right":
            return value[: -self.mask_length] + mask
        return mask + value[self.mask_length :]

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([self._compute_mask(value) for value in col], dtype="str")
