# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

"""Implementation of all anonymization techniques."""

from aindo.anonymize.techniques.binning import Binning
from aindo.anonymize.techniques.char_masking import CharacterMasking
from aindo.anonymize.techniques.data_nulling import DataNulling
from aindo.anonymize.techniques.hashing import KeyHashing
from aindo.anonymize.techniques.identity import Identity
from aindo.anonymize.techniques.mocking import Mocking, MockingGeneratorMethods
from aindo.anonymize.techniques.perturbation import PerturbationCategorical, PerturbationNumerical
from aindo.anonymize.techniques.swapping import Swapping
from aindo.anonymize.techniques.top_bottom_coding import TopBottomCodingCategorical, TopBottomCodingNumerical

__all__ = [
    "Binning",
    "CharacterMasking",
    "DataNulling",
    "KeyHashing",
    "Identity",
    "Mocking",
    "MockingGeneratorMethods",
    "PerturbationCategorical",
    "PerturbationNumerical",
    "TopBottomCodingCategorical",
    "Swapping",
    "TopBottomCodingNumerical",
]
