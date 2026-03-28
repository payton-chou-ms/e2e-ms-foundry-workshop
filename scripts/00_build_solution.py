"""Deprecated shim for the old build pipeline entrypoint."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, print_deprecation_notice, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command("internal/build_solution.py", forwarded_args=argv)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    print_deprecation_notice("00_build_solution.py", "internal/build_solution.py")
    print("常用公開入口：admin_prepare_docs_data_demo.py；若仍需要 --only / --skip-* 等進階旗標，請直接執行 internal/build_solution.py")
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())
