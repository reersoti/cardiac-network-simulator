from __future__ import annotations

import argparse
from pathlib import Path

from .gui import CardiacNetworkGUI
from .model import CardiacNetwork


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cardiac network simulator")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "input.txt",
        help="Path to the input graph file",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    network = CardiacNetwork.from_file(args.input)
    gui = CardiacNetworkGUI(network)
    gui.run()


if __name__ == "__main__":
    main()
