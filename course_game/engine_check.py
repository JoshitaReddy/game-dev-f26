"""Draw one frame, inspect its pixels and advance the Pyxel engine."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    import pyxel

    pyxel.init(128, 64, title="Course engine check", headless=args.headless)
    pyxel.cls(1)
    pyxel.pset(0, 0, 7)
    if pyxel.pget(0, 0) != 7:
        raise RuntimeError("Pyxel did not draw the expected pixel.")
    pyxel.text(8, 24, "The engine runs.", 7)
    for _ in range(2 if args.headless else 30):
        pyxel.flip()
    print("PASS Pyxel initialized, drew and advanced frames.")


if __name__ == "__main__":
    main()
