# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from aindo.anonymize import version as aindo_version
from aindo.anonymize.config import Config
from aindo.anonymize.pipeline import AnonymizationPipeline

__version__ = aindo_version.__version__

__all__ = ["__version__", "Config", "AnonymizationPipeline"]
