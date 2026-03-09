# Cardiac Network Simulator

Небольшой Python-проект для моделирования распространения импульса по графу, который можно интерпретировать как упрощённую сеть проводящей системы сердца.

## Что умеет

- загружает граф из текстового файла;
- отображает сеть в `Tkinter`;
- считает шаги симуляции по нажатию `Space`;
- позволяет вручную активировать вершины кликом мыши;
- использует `networkx` для построения layout графа.

## Структура проекта

```text
cardiac-network-simulator/
├── cardiac_network_simulator/
│   ├── __init__.py
│   ├── gui.py
│   ├── main.py
│   └── model.py
├── data/
│   └── input.txt
├── tests/
│   └── test_model.py
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Формат входного файла

```text
<refractory_period>
<number_of_nodes>
<neighbors for node 0>
<neighbors for node 1>
...
```

Пример:

```text
3
7
1 6
0 2
1 3
2 4
3 5
4 6
0 5
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python run.py
```

или

```bash
python -m cardiac_network_simulator.main
```

Можно передать свой файл:

```bash
python -m cardiac_network_simulator.main --input data/input.txt
```

## Управление

- `Space` — следующий шаг симуляции
- клик по вершине — ручная активация нейрона

## Идея модели

Каждая вершина хранит:
- состояние активности;
- таймер рефрактерности;
- список соседей.

На каждом шаге активные вершины распространяют сигнал соседям, затем таймеры обновляются.

## Что можно улучшить дальше

- добавить цветовую индикацию активных / рефрактерных узлов;
- вынести параметры симуляции в панель управления;
- добавить сохранение состояния и сценарии тестирования;
- покрыть модель более подробными тестами.
