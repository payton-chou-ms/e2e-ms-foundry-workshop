"""Deprecated shim for the old internal preload entrypoint."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, print_deprecation_notice, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command("internal/preload_scenarios.py", forwarded_args=argv)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    print_deprecation_notice("00_admin_preload_scenarios.py", "admin_prepare_shared_demo.py")
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())
