# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import hashlib
import hmac
import secrets
from base64 import b64encode
from typing import Any, ClassVar

import pandas as pd

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique


class KeyHashing(BaseSingleColumnTechnique):
    """Implements key-based hashing.

    Data values are hashed using HMAC with a cryptographic key and the chosen hashing algorithm
    (defaults to SHA-256). The resulting hash is then encoded using Base64.
    The de-identified values have always a uniform length.

    Attributes:
        key: The cryptographic key used for hashing.
        salt: An optional salt that can be added to the value before hashing. Defaults to None.
        hash_name: The hashing algorithm to use, compatible with `hashlib.new()`. Defaults to "sha256".
    """

    preserve_type: ClassVar[bool] = False

    key: str
    salt: str | None = None
    hash_name: str = "sha256"

    def __init__(self, key: str, salt: str | None = None, hash_name: str = "sha256") -> None:
        super().__init__()
        self.key = key
        self.salt = salt
        self.hash_name = hash_name

        if hash_name not in hashlib.algorithms_available:
            raise ValueError(f"Algorithm '{hash_name}' not available")

        _salt: str = salt or ""
        self._base_hmac_obj: hmac.HMAC = hmac.new(key.encode(), _salt.encode(), hashlib.sha256)

    def _compute_hash(self, value: Any) -> str:
        hmac_obj = self._base_hmac_obj.copy()
        hmac_obj.update(str(value).encode() if not isinstance(value, bytes) else value)
        return b64encode(hmac_obj.digest()).decode()

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([self._compute_hash(value) for value in col], dtype="str")

    @classmethod
    def generate_salt(cls) -> str:
        return secrets.token_hex(16)
