"""Deprecated shim for the old prepare entrypoint."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, print_deprecation_notice, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command("internal/prepare_demo.py", forwarded_args=argv)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    print_deprecation_notice("00_admin_prepare_demo.py", "admin_prepare_shared_demo.py")
    print("常用新入口：admin_prepare_docs_demo.py / admin_prepare_foundry_iq_demo.py / admin_prepare_docs_data_demo.py")
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())
