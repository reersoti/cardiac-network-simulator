from pathlib import Path
import unittest

from cardiac_network_simulator.model import CardiacNetwork, parse_input_file


class CardiacNetworkModelTests(unittest.TestCase):
    def test_parse_input_file(self) -> None:
        refractory_period, node_count, neighbors = parse_input_file(
            Path("data/input.txt")
        )
        self.assertEqual(refractory_period, 3)
        self.assertEqual(node_count, 7)
        self.assertEqual(neighbors[0], [1, 6])

    def test_build_network_and_tick(self) -> None:
        network = CardiacNetwork.from_file(Path("data/input.txt"))
        self.assertEqual(network.size, 7)

        network.tick([1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(network.state_snapshot()[0], 3)

        network.tick([0, 0, 0, 0, 0, 0, 0])
        snapshot = network.state_snapshot()
        self.assertGreaterEqual(snapshot[1], 3)
        self.assertGreaterEqual(snapshot[6], 3)


if __name__ == "__main__":
    unittest.main()
