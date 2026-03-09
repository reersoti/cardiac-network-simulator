from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(slots=True)
class Neuron:
    """Single node in the cardiac conduction graph."""

    neuron_id: int
    neighbors: set[int] = field(default_factory=set)
    refractory_timer: int = 0
    is_active: bool = False
    cooldown: bool = False

    def try_activate(self, refractory_value: int) -> None:
        """Activate neuron if it is not in the final refractory phase.

        This preserves the original project logic where a neuron can be re-triggered
        only when its timer is sufficiently low.
        """
        if self.refractory_timer < refractory_value - 1:
            self.is_active = True
            self.refractory_timer = refractory_value

    def force_activate(self, refractory_value: int) -> None:
        """Manual activation from the GUI."""
        if not self.is_active:
            self.is_active = True
            self.refractory_timer = refractory_value

    def tick(self) -> None:
        """Advance neuron state by one simulation step."""
        if self.is_active:
            self.is_active = False
            return

        if self.refractory_timer > 0:
            self.refractory_timer -= 1
            if self.refractory_timer == 0:
                self.cooldown = True
            return

        if self.cooldown:
            self.cooldown = False


class CardiacNetwork:
    """Graph-based heart pulse propagation model."""

    def __init__(self, refractory_period: int, neurons: list[Neuron]) -> None:
        if refractory_period < 1:
            raise ValueError("refractory_period must be >= 1")
        self.refractory_period = refractory_period
        self.neurons = neurons

    @property
    def size(self) -> int:
        return len(self.neurons)

    @classmethod
    def from_neighbors(cls, refractory_period: int, neighbors: Sequence[Sequence[int]]) -> "CardiacNetwork":
        neurons = [Neuron(neuron_id=index) for index in range(len(neighbors))]

        for index, relation_ids in enumerate(neighbors):
            for neighbor_id in relation_ids:
                if neighbor_id == index:
                    continue
                if not 0 <= neighbor_id < len(neurons):
                    raise ValueError(f"neighbor id {neighbor_id} is out of range")
                neurons[index].neighbors.add(neighbor_id)
                neurons[neighbor_id].neighbors.add(index)

        return cls(refractory_period=refractory_period, neurons=neurons)

    @classmethod
    def from_file(cls, path: str | Path) -> "CardiacNetwork":
        refractory_period, node_count, neighbors = parse_input_file(path)
        if len(neighbors) != node_count:
            raise ValueError(
                f"expected {node_count} neighbor rows, got {len(neighbors)}"
            )
        return cls.from_neighbors(refractory_period, neighbors)

    def tick(self, external_pulses: Sequence[int] | None = None) -> None:
        """Run one simulation step.

        1. All currently active neurons stimulate their neighbors.
        2. Timers are decremented.
        3. External pulses are applied.
        """
        if external_pulses is None:
            external_pulses = [0] * self.size
        if len(external_pulses) != self.size:
            raise ValueError("external_pulses length must match number of neurons")

        currently_active = [neuron.is_active for neuron in self.neurons]

        for neuron_index, is_active in enumerate(currently_active):
            if not is_active:
                continue
            for neighbor_id in self.neurons[neuron_index].neighbors:
                self.neurons[neighbor_id].try_activate(self.refractory_period + 1)

        for neuron in self.neurons:
            neuron.tick()

        for index, pulse in enumerate(external_pulses):
            if pulse:
                self.neurons[index].try_activate(self.refractory_period)

    def state_snapshot(self) -> list[int]:
        """Return current timers for display/logging."""
        return [neuron.refractory_timer for neuron in self.neurons]

    def activate_node(self, node_id: int, timer_value: int) -> None:
        if not 0 <= node_id < self.size:
            raise IndexError("node_id out of range")
        if not 1 <= timer_value <= self.refractory_period:
            raise ValueError(
                f"timer_value must be between 1 and {self.refractory_period}"
            )
        self.neurons[node_id].force_activate(timer_value)

    def edge_list(self) -> list[tuple[int, int]]:
        edges: set[tuple[int, int]] = set()
        for neuron in self.neurons:
            for neighbor_id in neuron.neighbors:
                edges.add(tuple(sorted((neuron.neuron_id, neighbor_id))))
        return sorted(edges)


def parse_input_file(path: str | Path) -> tuple[int, int, list[list[int]]]:
    """Read project input format.

    Format:
        line 1: refractory period
        line 2: number of neurons
        next N lines: neighbor ids for each neuron
    """
    file_path = Path(path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    if len(lines) < 2:
        raise ValueError("input file must contain at least two lines")

    refractory_period = int(lines[0].strip())
    node_count = int(lines[1].strip())
    neighbor_lines = lines[2:]

    neighbors: list[list[int]] = []
    for line in neighbor_lines:
        stripped = line.strip()
        neighbors.append(list(map(int, stripped.split())) if stripped else [])

    return refractory_period, node_count, neighbors
