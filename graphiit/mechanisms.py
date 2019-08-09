# Lambdas avoided for easier debugging

from toolz import curry
import numpy as np


def AND(inputs):
    return sum(inputs) == len(inputs)


def NAND(inputs):
    return not AND(inputs)


def OR(inputs):
    return sum(inputs) >= 1


def COPY(inputs):
    assert len(inputs) <= 1, "COPY gates cannot have multiple inputs"
    return OR(inputs)


def NOR(inputs):
    return not OR(inputs)


def NOT(inputs):
    assert len(inputs) <= 1, "NOT gates cannot have multiple inputs"
    return NOR(inputs)


def XOR(inputs):
    return sum(inputs) % 2 == 1


def MAJORITY(inputs):
    return sum(inputs) > len(inputs)/2


MAJ = MAJORITY


def MINORITY(inputs):
    return sum(inputs) <= len(inputs)/2

MIN = MINORITY


def PARITY(inputs):
    return sum(inputs) % 2 == 0


def PAR(inputs):
    return PARITY(inputs)


@curry
def NAKA_RUSHTON(threshold, exponent, weights, inputs):
    input_strength = np.sum(np.array(weights) * np.array(inputs))**exponent
    return input_strength / (threshold**exponent + input_strength)


MAP = {
    'AND': AND,
    'NAND': NAND,
    'OR': OR,
    'NOR': NOR,
    'COPY': COPY,
    'NOT': NOT,
    'XOR': XOR,
    'MAJORITY': MAJORITY,
    'MAJ': MAJ,
    'MINORITY': MINORITY,
    'MIN': MIN,
    'PARITY': PARITY,
    'PAR': PAR,
    'NAKA_RUSHTON': NAKA_RUSHTON,
}
