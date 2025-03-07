# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import re
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, Type, Union

from aindo.anonymize.techniques import (
    Binning,
    CharacterMasking,
    DataNulling,
    KeyHashing,
    Mocking,
    PerturbationCategorical,
    PerturbationNumerical,
    Swapping,
    TopBottomCodingCategorical,
    TopBottomCodingNumerical,
)
from aindo.anonymize.techniques.base import BaseTechnique

ALL_TECHNIQUES: list[Type] = [
    Binning,
    CharacterMasking,
    DataNulling,
    KeyHashing,
    Mocking,
    PerturbationCategorical,
    PerturbationNumerical,
    Swapping,
    TopBottomCodingCategorical,
    TopBottomCodingNumerical,
]


class TechniqueType(str, Enum):
    BINNING = "binning"
    CHARACTER_MASKING = "character_masking"
    DATA_NULLING = "data_nulling"
    KEY_HASHING = "key_hashing"
    MOCKING = "mocking"
    PERTURBATION_CATEGORICAL = "perturbation_categorical"
    PERTURBATION_NUMERICAL = "perturbation_numerical"
    SWAPPING = "swapping"
    TOP_BOTTOM_CODING_CATEGORICAL = "top_bottom_coding_categorical"
    TOP_BOTTOM_CODING_NUMERICAL = "top_bottom_coding_numerical"


def _get_type_from_class(cls: Type) -> TechniqueType:
    """Get the `TechniqueType` for the given technique or spec class."""
    type_name: str = re.sub(r"([a-z])([A-Z])", r"\1_\2", cls.__name__)
    type_name = type_name.upper()
    if type_name.endswith("_SPEC"):
        type_name = type_name.removesuffix("_SPEC")
    return TechniqueType[type_name]


class BaseSpec(BaseTechnique):
    """Base class for "Spec" classes.

    Attributes:
        type: Specifies which technique this configuration applies to.
    """

    type: TechniqueType


def _process_technique_class(cls: Type) -> Type:
    """Derive a new class from a technique class by adding a type attribute.

    For example, a class derived from `DataNulling` will be equivalent to:
    ```python
    class DataNullingSpec(DataNulling):
        type: Literal[TechniqueType.DATA_NULLING] = TechniqueType.DATA_NULLING

    ```
    """
    _type: TechniqueType = _get_type_from_class(cls)
    field_values: dict[str, Any] = {"type": _type}
    field_annotations: dict[str, Any] = cls.__annotations__
    field_annotations.update({"type": Literal[_type]})

    return type(
        f"{cls.__name__}Spec",
        (
            BaseSpec,
            cls,
        ),
        {**field_values, "__annotations__": field_annotations},
    )


ALL_TECHNIQUES_SPEC: list[Type] = [_process_technique_class(c) for c in ALL_TECHNIQUES]

if TYPE_CHECKING:
    TechniqueMethod = BaseSpec
else:
    TechniqueMethod = Union[tuple(ALL_TECHNIQUES_SPEC)]
    """A union of technique classes with an added type attribute."""


class TechniqueItem:
    """Configuration for applying a single anonymization technique.

    Attributes:
        method: Parameters defining the technique's configuration.
        columns: Input data columns to which the technique will be applied.
    """

    method: TechniqueMethod
    columns: list[str] | None

    # Utility mapping from a type to its corresponding spec class.
    _techniques_mapping: dict[TechniqueType, Type] = {_get_type_from_class(cls): cls for cls in ALL_TECHNIQUES_SPEC}

    def __init__(self, method: TechniqueMethod, columns: list[str] | None):
        self.method = method
        self.columns = columns

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TechniqueItem":
        """Creates an instance of the class from a dictionary.

        Args:
            value: A dictionary where keys represent the attributes of the class
                and values are their corresponding values.

        Returns:
            An instance of the class populated with the data from the dictionary.
        """
        method_data: dict[str, Any] = value.get("method", {})
        if not method_data or "type" not in method_data:
            raise ValueError("Invalid input: 'method' field must have a 'type' key")

        method_type: TechniqueType = method_data.get("type", "")
        method_class: Type | None = cls._techniques_mapping.get(method_type, None)
        if method_class is None:
            raise ValueError(f"Invalid input: unknown technique type '{method_type}'")

        method_kwargs: dict[str, Any] = method_data.copy()
        method_kwargs.pop("type")
        method: TechniqueMethod = method_class(**method_kwargs)
        return cls(method=method, columns=value.get("columns"))

    def __repr__(self) -> str:
        return f"TechniqueItem(method={self.method!r},columns={self.columns!r})"

    def __str__(self) -> str:
        return f"TechniqueItem(method={self.method.__class__.__name__}(...),columns={self.columns!s})"


class Config:
    """Configuration for the high-level interface `aindo.anonymize.AnonymizationPipeline`.

    Attributes:
        steps:  A list of anonymization steps to be applied.
    """

    steps: list[TechniqueItem]

    def __init__(self, steps: list[TechniqueItem]):
        self.steps = steps

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Config":
        """Creates an instance of the class from a dictionary.

        Args:
            value: A dictionary where keys represent the attributes of the class
                and values are their corresponding values.

        Returns:
            An instance of the class populated with the data from the dictionary.
        """
        steps_data = value.get("steps")
        if steps_data is None:
            raise ValueError("Invalid input: 'steps' not found")
        steps = [TechniqueItem.from_dict(item_data) for item_data in steps_data]
        return cls(steps=steps)

    def __repr__(self) -> str:
        return f"Config(steps={self.steps!r})"
