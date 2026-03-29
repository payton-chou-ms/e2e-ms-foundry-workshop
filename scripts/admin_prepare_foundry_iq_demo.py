"""Deprecated shim for the Foundry-native IQ demo path."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, print_deprecation_notice, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command(
        "admin_prepare_shared_demo.py",
        fixed_args=["--mode", "foundry-iq"],
        forwarded_args=argv,
    )


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    print_deprecation_notice("admin_prepare_foundry_iq_demo.py", "admin_prepare_shared_demo.py --mode foundry-iq")
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())