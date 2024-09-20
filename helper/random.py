import numpy as np
import core.constants as core_consts


def get_random_size(sizes: list[str]) -> str:
    """Select a random size based on defined probabilities."""

    size_prob = list(core_consts.DEFECT_SIZES.values())

    if not all(x == y for x, y in zip(sizes, list(core_consts.DEFECT_SIZES.keys()))):
        default_size_prob = [core_consts.DEFECT_SIZES[size] for size in sizes]
        size_prob = [
            round(prob / sum(default_size_prob), 3) for prob in default_size_prob[:-1]
        ]
        size_prob.append(round(1 - sum(size_prob), 3))

    return np.random.choice(sizes, p=size_prob)
