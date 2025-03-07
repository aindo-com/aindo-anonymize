<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

`aindo-anonymize` techniques are classes that derive from
[`BaseTechnique`][aindo.anonymize.techniques.base.BaseTechnique]
and define specific parameters and logic for anonymization.

::: aindo.anonymize.techniques.base.BaseTechnique
    options:
      members:
        - anonymize

Single-column techniques are anonymization methods designed to operate on individual data columns.
These techniques are implemented as classes that derive from
[`BaseSingleColumnTechnique`][aindo.anonymize.techniques.base.BaseSingleColumnTechnique].

::: aindo.anonymize.techniques.base.BaseSingleColumnTechnique
    options:
      members:
        - anonymize_column
        - anonymize

## Techniques

::: aindo.anonymize.techniques.data_nulling.DataNulling

::: aindo.anonymize.techniques.char_masking.CharacterMasking

::: aindo.anonymize.techniques.mocking.Mocking

::: aindo.anonymize.techniques.hashing.KeyHashing

::: aindo.anonymize.techniques.swapping.Swapping

::: aindo.anonymize.techniques.binning.Binning

::: aindo.anonymize.techniques.perturbation.PerturbationNumerical

::: aindo.anonymize.techniques.perturbation.PerturbationCategorical

::: aindo.anonymize.techniques.top_bottom_coding.TopBottomCodingNumerical

::: aindo.anonymize.techniques.top_bottom_coding.TopBottomCodingCategorical


## Types

::: aindo.anonymize.techniques.char_masking.StartingDirection

::: aindo.anonymize.techniques.common.SeedT

::: aindo.anonymize.techniques.perturbation.SamplingMode

::: aindo.anonymize.techniques.perturbation.NumericsT

::: aindo.anonymize.techniques.mocking.MockingGeneratorMethods
