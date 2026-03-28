"""Deprecated shim for the old workshop-agent test entrypoint."""

from __future__ import annotations

import sys

from entrypoint_runner import build_passthrough_command, print_deprecation_notice, run_command


def build_command(argv: list[str]) -> list[str]:
    return build_passthrough_command("pipelines/agents/test_workshop_agent.py", forwarded_args=argv)


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    replacement = "participant_validate_docs.py" if "--foundry-only" in effective_argv else "participant_validate_docs_data.py"
    print_deprecation_notice("08_test_foundry_agent.py", replacement)
    return run_command(build_command(effective_argv))


if __name__ == "__main__":
    raise SystemExit(main())
