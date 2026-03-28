"""Public admin entrypoint for preparing the shared workshop demo environment."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, run_command


def build_command(argv: list[str]) -> list[str]:
    forwarded_args = list(argv)
    with_fabric = False

    if "--with-fabric" in forwarded_args:
        forwarded_args = [arg for arg in forwarded_args if arg != "--with-fabric"]
        with_fabric = True

    fixed_args: list[str] = []
    if not with_fabric and "--skip-fabric" not in forwarded_args:
        fixed_args.append("--skip-fabric")

    return build_passthrough_command(
        "internal/prepare_demo.py",
        fixed_args=fixed_args,
        forwarded_args=forwarded_args,
    )


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())