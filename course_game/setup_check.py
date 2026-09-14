"""Read-only diagnostics: no commits, pushes, credential writes or fallback passes."""

import argparse
import json
import subprocess
import sys

from .narrator import LIVE_PROVIDERS, narrate
from .world import World


def command_ok(label: str, command: list[str], timeout: int = 30) -> bool:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"FAIL {label}: {type(error).__name__}")
        return False
    if result.returncode:
        print(f"FAIL {label}: rerun {' '.join(command)} locally for details.")
        return False
    print(f"PASS {label}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--offline", action="store_true", help="Fixture only; partial setup verification")
    mode.add_argument("--provider", choices=LIVE_PROVIDERS, help="Explicitly authorize one live model request")
    parser.add_argument("--headless", action="store_true", help="Engine test without opening a window")
    args = parser.parse_args()
    checks = [sys.version_info >= (3, 11)]
    print(f"{'PASS' if checks[0] else 'FAIL'} Python {sys.version.split()[0]}")
    checks.append(command_ok("Git", ["git", "--version"]))
    checks.append(command_ok("GitHub CLI authentication", ["gh", "auth", "status"]))
    engine = [sys.executable, "-m", "course_game.engine_check"]
    if args.headless:
        engine.append("--headless")
    checks.append(command_ok("Pyxel engine", engine))
    checks.append(command_ok("deterministic tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]))
    provider = "fixture" if args.offline else args.provider
    try:
        result = narrate(World().observe(), "look", provider)
        print(f"PASS {'scripted fixture (no live call)' if args.offline else 'live model response'}")
        # Metadata only: no prompts, player text, credentials or identifying data.
        print(json.dumps({
            "provider": result.provider, "model": result.model,
            "elapsed_seconds": round(result.elapsed_seconds, 3),
            "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens,
            "cost": "not estimated; use the dated price for your approved model",
        }))
        checks.append(True)
    except Exception as error:
        print(f"FAIL live model response: {type(error).__name__}. Check the README access steps.")
        checks.append(False)
    if not all(checks):
        print("SETUP INCOMPLETE. No failed check was replaced with an offline pass.")
        return 1
    if args.offline:
        print("OFFLINE CHECKS PASS. Partial Setup Verification: a live local call and CI evidence are still required.")
    else:
        print("LIVE CHECKS PASS. Keep this result and the setup workflow run as Setup Verification evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
