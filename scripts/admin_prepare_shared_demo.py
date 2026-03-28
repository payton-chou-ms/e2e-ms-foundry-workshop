"""Public admin entrypoint for preparing the shared workshop demo environment."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command("internal/prepare_demo.py", forwarded_args=argv)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())