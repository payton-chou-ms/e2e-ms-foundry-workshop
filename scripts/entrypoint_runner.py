"""Helpers for public wrapper scripts that delegate to existing workshop CLIs."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence


SCRIPT_DIR = Path(__file__).resolve().parent


def build_passthrough_command(
    target_script: str,
    fixed_args: Sequence[str] | None = None,
    forwarded_args: Sequence[str] | None = None,
) -> list[str]:
    args = list(fixed_args or [])
    args.extend(list(forwarded_args or []))
    return [sys.executable, os.fspath(SCRIPT_DIR / target_script), *args]


def run_command(command: Sequence[str]) -> int:
    completed = subprocess.run(list(command))
    return completed.returncode


def print_deprecation_notice(legacy_script: str, replacement: str) -> None:
    print(f"警告：scripts/{legacy_script} 已 deprecated，請改用 scripts/{replacement}")