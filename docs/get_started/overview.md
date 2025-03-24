<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

The `aindo.anonymize` library supports `pandas.DataFrame` and `pandas.Series` data structures
for both inputs and outputs, depending on the method used (see the [`anonymize`](../api_reference/techniques.md#aindo.anonymize.techniques.base.BaseTechnique.anonymize) and
[`anonymize_column`](../api_reference/techniques.md#aindo.anonymize.techniques.base.BaseSingleColumnTechnique.anonymize_column) methods).
This means that the data must be loaded as `pandas.DataFrame` or `pandas.Series` before being processed.
The anonymization techniques will then return the anonymized data in the same format — either `pandas.DataFrame`
or `pandas.Series` — based on the method used.

It currently implements the following anonymization techniques:

- [**Identity**][aindo.anonymize.techniques.identity.Identity]:
leaves the original data untouched, useful in a declarative approach (see below).

- [**Data nulling**][aindo.anonymize.techniques.data_nulling.DataNulling]:
Replaces the original data with `None` or a custom constant value.

- [**Character masking**][aindo.anonymize.techniques.char_masking.CharacterMasking]:
Replaces some or all characters with a constant symbol.

- [**Mocking**][aindo.anonymize.techniques.mocking.Mocking]:
Generates realistic mock data for various fields, such as names, emails, and more.

- [**KeyHashing**][aindo.anonymize.techniques.hashing.KeyHashing]:
Data values are hashed using a cryptographic key and then encoded using Base64.

- [**Swapping**][aindo.anonymize.techniques.swapping.Swapping]:
Rearranges data by swapping values.

- [**Binning**][aindo.anonymize.techniques.binning.Binning]:
Groups numerical values into discrete ranges (bins), replacing each value with the corresponding range.

- [**Top/Bottom coding**][aindo.anonymize.techniques.top_bottom_coding.TopBottomCodingNumerical]:
Replaces values above or below certain thresholds with a capped value.

- [**Perturbation**][aindo.anonymize.techniques.perturbation.PerturbationNumerical]:
Slightly modifies the values according to the specified perturbation intensity and replacement strategy.

The library provides two usage approaches,
supporting different use cases and development preferences:

- *Explicit approach*: this method involves directly instantiating anonymization techniques
using the library's Python classes (e.g., [`Binning`][aindo.anonymize.techniques.binning.Binning] for data binning).  
It is particularly effective for scenarios where:
(1) a limited number of techniques need to be applied,
(2) the anonymization methods are predefined and can be hardcoded,
and (3) development environment features, such as code completion and type checking,
are leveraged to enhance productivity and maintainability.  
See a simple example [here](./quickstart.md#explicit-approach).

- *Declarative approach*: this approach allows users to define multiple anonymization techniques
within a single configuration, which is then executed sequentially on the input data.
The configuration can be instantiated from a Python dictionary
using the [`Config.from_dict`][aindo.anonymize.config.Config.from_dict] method
and can be read from files in YAML, TOML or JSON formats.  
This method is particularly advantageous when the anonymization workflow is dynamic and requires flexibility.  
See a simple example [here](./quickstart.md#declarative-approach).
