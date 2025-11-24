<!--
SPDX-FileCopyrightText: 2025 Aindo SpA

SPDX-License-Identifier: MIT
-->

# Changelog

## [1.1.4](https://github.com/aindo-com/aindo-anonymize/compare/v1.1.3...v1.1.4) (2025-11-24)


### Build System

* add Python 3.14 to supported versions ([f6c2e92](https://github.com/aindo-com/aindo-anonymize/commit/f6c2e92d2da750632ffb298da2d5f24f59b24277))
* add Python 3.13 to supported versions ([dd3f756](https://github.com/aindo-com/aindo-anonymize/commit/dd3f7568256d802a794c99618128ae9b7b88d2b8))
* add Pyflakes lint rule to Ruff configuration ([b45d01c](https://github.com/aindo-com/aindo-anonymize/commit/b45d01c056f4a5ed3ea9b849fefab4f04b223f2e))


### Code Refactoring

* set default sampling mode for perturbation to weighted ([c3d96f1](https://github.com/aindo-com/aindo-anonymize/commit/c3d96f1dcd007070d925ce692efc0b58e9a71580))

## [1.1.3](https://github.com/aindo-com/aindo-anonymize/compare/v1.1.2...v1.1.3) (2025-06-05)


### Bug Fixes

* correct quantile computation for top/bottom-coding (numerical) ([cc3541e](https://github.com/aindo-com/aindo-anonymize/commit/cc3541eb02e7ec625303c34a3700951790d39451))
* handle read-only array bug on perturbation ([fb39da3](https://github.com/aindo-com/aindo-anonymize/commit/fb39da3d1f1068ba2115242671ad37d152b5d444))
* pipeline bug related to dtype casting ([dbc4ff8](https://github.com/aindo-com/aindo-anonymize/commit/dbc4ff8a51f0445932d926f98f74a499bd77fed9))

## [1.1.2](https://github.com/aindo-com/aindo-anonymize/compare/v1.1.1...v1.1.2) (2025-05-14)


### Bug Fixes

* data nulling dtype ([#14](https://github.com/aindo-com/aindo-anonymize/issues/14)) ([1d61579](https://github.com/aindo-com/aindo-anonymize/commit/1d61579894298d460272eb98b2f380b5bd7aa401))
* handle missing values correctly ([70374e2](https://github.com/aindo-com/aindo-anonymize/commit/70374e27aada43f628a0868397c82e3738ba74ac))
* perturbation random state ([c868211](https://github.com/aindo-com/aindo-anonymize/commit/c868211efe2c7f6e6d8f9aaef8a28b5f0f4b2c9d))

## [1.1.1](https://github.com/aindo-com/aindo-anonymize/compare/v1.1.0...v1.1.1) (2025-04-24)


### Documentation

* clarify that the process is "pseudonymisation" ([98bc600](https://github.com/aindo-com/aindo-anonymize/commit/98bc6008b64e15f498aaffb1eaebaafdb3997b6f))

## [1.1.0](https://github.com/aindo-com/aindo-anonymize/compare/v1.0.1...v1.1.0) (2025-04-07)


### Features

* add identity technique ([#7](https://github.com/aindo-com/aindo-anonymize/issues/7)) ([ee9f7f2](https://github.com/aindo-com/aindo-anonymize/commit/ee9f7f2dc1a74436cf92f85dcd6b6ff5cad7925e))
* method `to_dict` for config classes ([#8](https://github.com/aindo-com/aindo-anonymize/issues/8)) ([d84955c](https://github.com/aindo-com/aindo-anonymize/commit/d84955c0e69022d7000ee9317679d44ec1170b56))


### Documentation

* change fonts ([68b47c9](https://github.com/aindo-com/aindo-anonymize/commit/68b47c9eb48ad48f773136a1b868ddd20d782f57))
* minor fixes ([d7a3518](https://github.com/aindo-com/aindo-anonymize/commit/d7a3518760b9913f8f8dac29bd61d6f7d5e390ab))

## [1.0.1](https://github.com/aindo-com/aindo-anonymize/compare/v1.0.0...v1.0.1) (2025-03-07)


### Bug Fixes

* add missing parentheses in `Config.__repr__` ([ef36d25](https://github.com/aindo-com/aindo-anonymize/commit/ef36d25ed534f80e66e0ea4e2fb4b0b219ec35aa))
* invalid Config input with empty steps ([80e8856](https://github.com/aindo-com/aindo-anonymize/commit/80e8856546c0aced4b90a650bc3ee7afda35cb8f))


### Documentation

* fix license badge ([459041c](https://github.com/aindo-com/aindo-anonymize/commit/459041ca026ce435b39fddee1deccdcd89e5e08c))
* ignore some files from site build ([e7c6164](https://github.com/aindo-com/aindo-anonymize/commit/e7c616490a974aa15ed30101089e7deae8c1ad50))

## 1.0.0 (2025-03-07)

First release 🎉
