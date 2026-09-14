import argparse

from .narrator import LIVE_PROVIDERS, narrate
from .world import World


def main() -> None:
    parser = argparse.ArgumentParser(description="The Garden Door: an original starter game")
    parser.add_argument("--provider", choices=["fixture", *LIVE_PROVIDERS], default="fixture")
    args = parser.parse_args()
    world = World()
    live_calls = 0
    print("The Garden Door. Commands: look, east, west, take key, unlock door, north, quit.")
    print("Ask the narrator with: ask <question>. Live narration is limited to five calls.")
    print(f"Narrator mode: {args.provider}. Fixture mode uses no model or cloud credits.")
    print(world.act("look"))
    while True:
        try:
            command = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if command.lower() == "quit":
            break
        if command.lower().startswith("ask "):
            if args.provider in LIVE_PROVIDERS and live_calls >= 5:
                print("Live-call budget reached. " + world.act("look"))
                continue
            if args.provider in LIVE_PROVIDERS:
                live_calls += 1  # Failed requests also consume the attempt budget.
            try:
                result = narrate(world.observe(), command[4:], args.provider)
                print(result.text)
                print(f"[{result.provider}; {result.model}; {result.elapsed_seconds:.2f}s; "
                      f"total tokens: {result.total_tokens}; facts: {result.fact_ids}]")
            except Exception as error:
                # Provider errors can contain request details. Keep output free of credentials.
                print(f"Narration unavailable ({type(error).__name__}); showing game state.")
                print(world.act("look"))
        else:
            print(world.act(command))


if __name__ == "__main__":
    main()
