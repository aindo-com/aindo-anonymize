# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import numpy as np
import pytest

from aindo.anonymize.techniques.common import AlphaProbability, Seeder


def test_seeder():
    s = Seeder()
    assert hasattr(s, "generator")
    assert isinstance(s.generator, np.random.Generator)


@pytest.mark.parametrize("alpha", [-0.1, 1.1])
def test_alphaprobability_validation(alpha: float):
    with pytest.raises(ValueError, match="alpha must be between 0 and 1."):
        AlphaProbability(alpha)
