from typing import Union

import numpy as np
from pydantic import validate_arguments


def metric(s):
    """
    https://doi.org/10.48550/arXiv.2401.09196
    """

    m = [np.abs(-s[i-1]-s[i+1]+2*s[i]) - np.abs(s[i+1]-s[i-1]) for i in range(1, len(s)-1)]
    m = np.pad(m, [1, 1], mode='edge')
    m[:2] = 0
    m[-2:] = 0
    return m


@validate_arguments()
def indices(s, threshold: Union[None, float] = None):
    if threshold is None:
        threshold = 12
    return np.where(metric(s) > threshold)[0]
