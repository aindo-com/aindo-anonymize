<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

Contributions are welcome and greatly appreciated! :tada:

## Git workflow

The standard process to contribute to this project follows these steps:

1. Fork the repository on GitHub and clone your fork locally.
    ```bash
    # Clone your fork and cd into the repo directory
    git clone git@github.com:<your username>/aindo-anonymize.git
    cd aindo-anonymize
    ```
2. Check out a new branch and make your changes.
    ```bash
    # Checkout a new branch and make your changes
    git checkout -b my-new-feature-branch
    # Make your changes...
    ```

3. Commit your changes with a clear message following
the [Conventional Commit](https://www.conventionalcommits.org/) standard,
then push your changes.

4. Open a Pull Request (PR) on GitHub, describing your changes.
Provide as much information as possible, including a description of your changes and links to any relevant issues.

Unless your change is trivial (e.g., a typo), please open an issue to discuss the proposed change before submitting a pull request.


## Development setup

Fortunately, **Aindo Anonymize** has minimal dependencies and doesn't require access to external resources,
so setting up and running the tests should be straightforward.

Before getting started, you'll need the following prerequisites:

- git
- any Python version between 3.10 and 3.12
- ideally, though not required, a virtual environment tool (`venv`, `uv`, etc.) should be used.

!!! Tip
    **tl;dr**: use `pre-commit` to fix formatting, `pyright` for type checking,
    `pytest` to run tests and `mkdocs build` to build the docs.

### Installation and setup

Install `aindo-anonymize` with dependencies, including those for testing, development, and documentation.

```bash
pip install -e ".[dev,test]"
pip install -r docs/requirements.txt
```

### Run tests

Before submitting changes, make sure all tests pass and check test coverage:

```bash
coverage run -m pytest
coverage report
```

### Linting and type checking

Run the linter locally to make sure everything is working as expected.

```bash
ruff check --fix
ruff format
```

To ensure type correctness, run Pyright with `pyright`.

!!! Info
    Lint checks are automatically performed before each commit using [pre-commit](https://pre-commit.com/) hooks.

### Build documentation

After making any updates to the documentation, such as changes to function signatures,
class definitions, or docstrings that will appear in the API docs,
be sure to check that the build goes through successfully.

```bash
# Build documentation
mkdocs build
```

You can also use `mkdocs serve` to serve the documentation at `localhost:8000`.

## Documentation style

Documentation is written in Markdown and built using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
API documentation is build from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Documentation should be clear, approachable, and easy to understand,
balancing brevity with completeness to ensure all essential information is included.

### Code documentation

Ensure that all code is well-documented using properly formatted docstrings.
The following elements should include documentation:

- Modules
- Class definitions
- Function definitions
- Module-level variables

**Aindo Anonymize** follows [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
formatted according to [PEP 257](https://www.python.org/dev/peps/pep-0257/) guidelines
(see [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
for further examples).  
Class attributes and function arguments should be documented in the format `name: description.`,
as types are inferred from the signature. 
