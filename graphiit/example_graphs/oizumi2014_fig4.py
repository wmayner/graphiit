import graphiit
from graphiit.mechanisms import AND, OR, XOR

graph_conf = [
    ("A", OR, "B", "C"), 
    ("B", AND, "A", "C"), 
    ("C", XOR, "A", "B"),
]

state1 = {"on": ["A"]}
