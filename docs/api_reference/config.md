<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

::: aindo.anonymize.config.Config
    options:
      show_docstring_attributes: false
      merge_init_into_class: false

### Configuration Schema

The [`Config.from_dict`][aindo.anonymize.config.Config.from_dict]
method accepts a Python dictionary following the schema below.  

| Key                       | Type                | Description                                             |
|---------------------------|---------------------|---------------------------------------------------------|
| `steps`                   | `list[dict]`        | A list of anonymization steps.                          |
| `steps[i].method`         | `dict`              | Defines the anonymization technique and its parameters. |
| `steps[i].method.type`    | `str`               | The name of the anonymization technique in snake_case.  |
| `steps[i].method.<param>` | `dict`              | Additional key-value pairs for technique-specific parameters. See the [list](./techniques.md#techniques) of anonymization techniques and their respective parameters.    |
| `steps[i].columns`        | `list[string] | None` | The list of column names to which the anonymization method applies. If set to None, the technique is applied to all columns. An empty list is not allowed. |

For a full configuration example, see the code below.
Note that some parameters may be mutually exclusive and are therefore not included in this example.  
For a complete reference of technique-specific parameters, see the [API reference - Techniques](./techniques.md#techniques).


??? "Full configuration example"
    ```json {title="config.json"}
    --8<-- "full_config.json"
    ```
