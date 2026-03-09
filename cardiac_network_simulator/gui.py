from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog

import networkx as nx

from .model import CardiacNetwork


class CardiacNetworkGUI:
    """Tkinter GUI to render the graph and step the simulation."""

    def __init__(self, network: CardiacNetwork) -> None:
        self.network = network
        self.root = tk.Tk()
        self.root.title("Cardiac Network Simulator")

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            frame,
            width=900,
            height=650,
            bg="white",
            scrollregion=(0, 0, 2400, 1600),
        )
        self.hbar = tk.Scrollbar(frame, orient="horizontal", command=self.canvas.xview)
        self.vbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(
            xscrollcommand=self.hbar.set,
            yscrollcommand=self.vbar.set,
        )

        self.hbar.pack(side="bottom", fill="x")
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.root.bind("<space>", self._step_simulation)
        self.canvas.bind("<Button-1>", self._on_click)

        self._text_items: dict[int, int] = {}
        self._node_coords: dict[int, tuple[float, float]] = {}
        self._node_radius = 18

    def run(self) -> None:
        self._draw_network()
        self.root.mainloop()

    def _draw_network(self) -> None:
        graph = nx.Graph()
        graph.add_nodes_from(range(self.network.size))
        graph.add_edges_from(self.network.edge_list())

        if graph.number_of_nodes() == 0:
            return

        is_planar, _ = nx.check_planarity(graph)
        positions = nx.planar_layout(graph) if is_planar else nx.spring_layout(graph, seed=42)
        self._node_coords = self._scale_positions(positions)

        self.canvas.delete("all")
        self._text_items.clear()

        for source, target in graph.edges():
            x1, y1 = self._node_coords[source]
            x2, y2 = self._node_coords[target]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        for node_id, (x, y) in self._node_coords.items():
            self.canvas.create_oval(
                x - self._node_radius,
                y - self._node_radius,
                x + self._node_radius,
                y + self._node_radius,
                fill="lightblue",
                outline="black",
                width=2,
            )
            text_item = self.canvas.create_text(
                x,
                y,
                text=str(self.network.neurons[node_id].refractory_timer),
                font=("Arial", 14, "bold"),
            )
            self._text_items[node_id] = text_item

        self._refresh_labels()

    def _scale_positions(
        self,
        positions: dict[int, tuple[float, float]],
    ) -> dict[int, tuple[float, float]]:
        xs = [value[0] for value in positions.values()]
        ys = [value[1] for value in positions.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        margin = 60
        width = 900 - 2 * margin
        height = 650 - 2 * margin

        def scale(value: float, min_value: float, max_value: float, out_min: float, out_max: float) -> float:
            if max_value - min_value == 0:
                return (out_min + out_max) / 2
            return out_min + (value - min_value) * (out_max - out_min) / (max_value - min_value)

        return {
            node_id: (
                scale(x, min_x, max_x, margin, margin + width),
                scale(y, min_y, max_y, margin, margin + height),
            )
            for node_id, (x, y) in positions.items()
        }

    def _on_click(self, event: tk.Event[tk.Misc]) -> None:
        clicked_node = self._find_clicked_node(event.x, event.y)
        if clicked_node is None:
            return

        value = simpledialog.askinteger(
            "Set refractory timer",
            f"Enter value (1–{self.network.refractory_period}):",
            minvalue=1,
            maxvalue=self.network.refractory_period,
            parent=self.root,
        )
        if value is None:
            return

        try:
            self.network.activate_node(clicked_node, value)
        except ValueError as exc:
            messagebox.showerror("Invalid value", str(exc), parent=self.root)
            return

        self._refresh_labels()

    def _find_clicked_node(self, x: float, y: float) -> int | None:
        for node_id, (node_x, node_y) in self._node_coords.items():
            if (x - node_x) ** 2 + (y - node_y) ** 2 <= self._node_radius ** 2:
                return node_id
        return None

    def _step_simulation(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        self.network.tick()
        self._refresh_labels()

    def _refresh_labels(self) -> None:
        for node_id, text_item in self._text_items.items():
            timer_value = self.network.neurons[node_id].refractory_timer
            self.canvas.itemconfigure(text_item, text=str(timer_value))
