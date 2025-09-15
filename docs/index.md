<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

# Aindo Anonymize

[![PyPI release](https://img.shields.io/pypi/v/aindo-anonymize.svg)](https://pypi.python.org/pypi/aindo-anonymize)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aindo-anonymize.svg)](https://github.com/aindo-com/aindo-anonymize)
[![PyPI - License](https://img.shields.io/pypi/l/aindo-anonymize)](https://github.com/aindo-com/aindo-anonymize/blob/main/LICENSES/MIT.txt)

Welcome to the documentation of the **Aindo Anonymize** library.

**Aindo Anonymize** is a lightweight Python library for anonymizing tabular data,
offering a collection of pseudonymization techniques such as masking, mocking, perturbation, and more.

## Installation

**Aindo Anonymize** can be installed via pip from PyPI.

```shell
pip install aindo-anonymize
```

It officially supports Python versions 3.10 and above.

## Quick example

The library provides a modular approach to data anonymization,
where each technique is represented by its own class.
To anonymize your tabular data, first initialize the desired anonymization technique class,
configure its options, and then apply it to your data:

```python
import pandas as pd
from aindo.anonymize.techniques import CharacterMasking

col = pd.Series(["John", "Mark", "Lucy", "Alice"])
masking = CharacterMasking(starting_direction="right", mask_length=2)

masking.anonymize_column(col)
# 0     Jo**
# 1     Ma**
# 2     Lu**
# 3    Ali**
# dtype: object
```
