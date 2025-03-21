<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

# Quick start

In the following examples, we will demonstrate how to anonymize specific columns of the [UCI Adult dataset](https://archive.ics.uci.edu/dataset/2/adult)
using the *Explicit* and the *Declarative* approaches.

The first step is to load the CSV file into a `pandas.DataFrame`:
```python {title="Load UCI Adult dataset"}
import pandas as pd

dtypes = {
    "age": "int",
    "workclass": "category",
    "fnlwgt": "int",
    "education": "category",
    "education-num": "category",
    "marital-status": "category",
    "occupation": "category",
    "relationship": "category",
    "race": "category",
    "sex": "category",
    "capital-gain": "int",
    "capital-loss": "int",
    "hours-per-week": "int",
    "native-country": "category",
    "y": "category",
}
df = pd.read_csv("adult.data", names=list(dtypes.keys()), dtype=dtypes)
```

## Explicit approach

In the explicit the user directly instantiates techniques and apply them to specific columns. 
```python
from aindo.anonymize.techniques import Binning, TopBottomCodingCategorical # (1)!

# Replace education categories representing less or equal than 1%
# of values with "OTHER"
anonymizer = TopBottomCodingCategorical(q=0.01, other_label="OTHER") # (2)!
print(anonymizer.anonymize_column(df.education)) # (3)!

# Group age values into discrete bins and replace each age
# with its corresponding bin range
anonymizer = Binning(bins=[17, 20, 30, 50, 70, 90])
print(anonymizer.anonymize_column(df.age))
```

1. All anonymization techniques are imported from `aindo.anonymize.techniques`.
2. Create an instance of the Top-Bottom Coding technique for categorical data.
3. [`anonymizer.anonymize_column()`][aindo.anonymize.techniques.base.BaseSingleColumnTechnique.anonymize_column]
applies the anonymization technique to a single column (provided as a Pandas `Series`) and always returns a copy.


For a complete list of available techniques and their parameters,
please refer to [API reference - Techniques](../api_reference/techniques.md).

## Declarative approach

In the declarative approach a yaml configuration file needs to be created first, listing all the operations that need 
to be performed in the desired order, defining a pipeline of operations.
```yaml {title="config.yml"}
# aindo-anonymize table anonymization configuration
steps:
  - method:
      type: top_bottom_coding_categorical # specifies the technique to be configured
      q: 0.01 # specific parameter for the Top-Bottom Coding technique
    columns: [education] # list of column names to which the technique will be applied
  - method:
      type: binning
      bins: [17, 20, 30, 50, 70, 90]
    columns: [age]
```

Then, the defined configuration file can be loaded as pipeline and the pipeline executed.
```python
import yaml
from aindo.anonymize import AnonymizationPipeline, Config

config = Config.from_dict(yaml.safe_load("config.yml"))
pipeline = AnonymizationPipeline(config=config)
print(pipeline.run(df))
```

Full documentation available at [API reference - Pipeline](../api_reference/pipeline.md).
