# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

import logging
from pathlib import Path

from mkdocs.config import Config

logger = logging.getLogger("mkdocs.plugin")
DOCS_DIR = Path(__file__).parent
PROJECT_ROOT = DOCS_DIR.parent


def on_pre_build(config: Config) -> None:
    """Before the build starts."""
    add_changelog()


def add_changelog() -> None:
    changelog_file = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    new_file = DOCS_DIR / "developers" / "changelog.md"

    # avoid writing file unless the content has changed to avoid infinite build loop
    if not new_file.is_file() or new_file.read_text(encoding="utf-8") != changelog_file:
        new_file.write_text(changelog_file, encoding="utf-8")
