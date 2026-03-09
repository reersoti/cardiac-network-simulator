# Cardiac Network Simulator

A Python-based simulator of signal propagation in a graph-based cardiac network with graphical visualization.

## Overview

This project models how an excitation signal propagates through a connected network of nodes.  
The idea is inspired by simplified cardiac conduction and other excitable dynamic systems, where local interactions between connected elements lead to visible global behavior.

The simulator provides a graphical interface that allows the user to observe the network and track how the signal spreads over time.  
It is designed as an educational project for studying graph-based simulations, propagation logic, and visual representation of dynamic processes.

## Features

- graph-based simulation of signal propagation
- interactive desktop interface
- configurable input data
- node state transitions over time
- visual representation of network dynamics
- educational model of excitation propagation

## Simulation Idea

The system consists of nodes connected by edges.  
Each node may change its state depending on:

- its current condition
- incoming activity from neighboring nodes
- propagation rules defined by the model

This makes it possible to simulate simplified pulse transmission across a structured network.

## Project Structure

```text
.
├── cardiac_network_simulator/
│   ├── __init__.py
│   ├── gui.py
│   ├── main.py
│   └── model.py
├── data/
│   └── input.txt
├── tests/
│   └── test_model.py
├── run.py
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

## Input Data

The simulator reads configuration data from `data/input.txt`.  
By modifying this file, different graph structures and initial conditions can be tested.

## Educational Value

This project can be useful for:

- studying graph-based dynamic systems
- understanding propagation processes in networks
- visualizing state transitions
- learning how simulation logic can be separated from graphical representation

## What This Project Demonstrates

- Python application structure
- modeling of dynamic graph processes
- separation of simulation and GUI layers
- structured input handling
- interactive visualization of algorithmic behavior

## Possible Improvements

- editable graph creation directly from the GUI
- richer propagation and recovery rules
- export of simulation states
- multiple preset scenarios
- improved validation of input data
- stronger automated test coverage

## Tech Stack

- Python
- Tkinter
- graph-based simulation logic

## Notes

This project is a simplified educational simulator and is not intended to be a biologically accurate cardiac model.
