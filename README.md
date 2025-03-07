<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

# Aindo Anonymize

[![PyPI release](https://img.shields.io/pypi/v/aindo-anonymize.svg)](https://pypi.python.org/pypi/aindo-anonymize)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aindo-anonymize.svg)](https://github.com/aindo-com/aindo-anonymize)
[![PyPI - License](https://img.shields.io/pypi/l/aindo-anonymize)](https://github.com/aindo-com/aindo-anonymize/blob/main/LICENSES/MIT.txt)

**Aindo Anonymize** is a lightweight Python library that provides various techniques
for anonymizing tabular data.

## Quick start

### Install
```console
pip install aindo-anonymize
```

### Start Anonymizing

Initialize the desired anonymization technique class, set its options,
and apply the anonymize method to your data.

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

## Help

Check the [documentation](https://docs.anonymize.aindo.com/) for more details.

## Contributing

For instructions on setting up a development environment and how to make a contribution, refer to
[Contributing to Aindo Anonymize](https://docs.anonymize.aindo.com/latest/developers/contributing/).
