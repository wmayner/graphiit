import numpy as np
import pytest

from graphiit import Graph
from graphiit.example_graphs import oizumi2014_fig4
from graphiit.mechanisms import NOT, XOR
from graphiit.utils import (
    NodeConfig,
    convert_be_tpm_to_le,
    format_node_tokens_by_state,
    parse_graph_config,
    parse_state_config,
    pretty_print_tpm,
)


def test_format_node_tokens_by_state(fig4_graph):
    state = (1, 0, 0)
    fore = format_node_tokens_by_state(fig4_graph.node_tokens, state, mode="fore")
    print("Tokens formatted by foreground color, should be cyan:red:red")
    print(":".join(fore))
    back = format_node_tokens_by_state(fig4_graph.node_tokens, state, mode="back")
    print("Tokens formatted by background color, should be white:black:black")
    print(":".join(back))
    fore_and_back = format_node_tokens_by_state(fore, state, mode="back")
    print("Tokens formatter by both FG and BG.")
    print(":".join(fore_and_back))


def test_pretty_print_tpm(fig4_graph):
    print("Pretty printing figure 4 TPM")
    pretty_print_tpm(fig4_graph.node_tokens, fig4_graph.tpm)


def test_be_tpm_to_le():
    be_tpm = np.array(
        [
            [0, 0, 0],
            [1, 0, 0],
            [1, 0, 1],
            [1, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 0],
        ]
    )
    true_le_tpm = np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ]
    )
    computed_le_tpm = convert_be_tpm_to_le(be_tpm)
    assert np.all(computed_le_tpm == true_le_tpm)


def test_parse_graph_config():
    config = [["A", "XOR", "B", "A"], ["B", "NOT", "A"]]
    assert parse_graph_config(config) == [
        NodeConfig("A", XOR, ["B", "A"]),
        NodeConfig("B", NOT, ["A"]),
    ]

    # Input 'D' is not actually specified as a node
    config = [["A", "XOR", "B", "C"], ["B", "NOT", "D"]]
    with pytest.raises(ValueError):
        parse_graph_config(config)

    # Duplicate specification of node 'A'
    config = [["A", "NOT", "A"], ["A", "COPY", "A"]]
    with pytest.raises(ValueError):
        parse_graph_config(config)


def test_parse_state_config():
    graph = Graph(oizumi2014_fig4.graph_config)

    # State too large
    with pytest.raises(ValueError):
        parse_state_config(graph, (0, 1, 0, 1))

    config = (0, 1, 0)
    assert np.array_equal(parse_state_config(graph, config), (0, 1, 0))

    config = [0, 1, 0]
    assert np.array_equal(parse_state_config(graph, config), (0, 1, 0))

    config = {"on": ["B"]}
    assert np.array_equal(parse_state_config(graph, config), (0, 1, 0))

    config = {"off": ["A", "C"]}
    assert np.array_equal(parse_state_config(graph, config), (0, 1, 0))

    # Can't specify both on and off states
    with pytest.raises(ValueError):
        config = {"off": ["A", "C"], "on": ["B"]}
        parse_state_config(graph, config)
