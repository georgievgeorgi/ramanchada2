#!/usr/bin/env python3

from typing import Dict, List, Literal, Union

import numpy as np
import numpy.typing as npt
from lmfit import lineshapes
from pydantic import validate_arguments

from ramanchada2.misc.spectrum_deco import add_spectrum_constructor

from ..spectrum import Spectrum


@add_spectrum_constructor()
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def from_theoretical_lines(
        shapes: List[Literal[lineshapes.functions]],  # type: ignore
        params: List[Dict],
        x: Union[int, npt.NDArray[np.float64]] = 2000):
    """
    Generate spectrum from `lmfit` shapes.

    Parameters
    ----------
    shapes : list of str
        the shapes to be used for spectrum generation
    params : list of dicts
        shape parameters to be applied to be used with shapes
    x : Union[int, npt.NDArray[np.float64]], optional
        array with x values, by default np.array(2000)
    """
    spe = Spectrum(x=x)
    x = spe.x
    y = np.zeros_like(x, dtype=float)
    for shape_name, pars in zip(shapes, params):
        shape = getattr(lineshapes, shape_name)
        y += shape(x=x, **pars)
    spe.y = y
    return spe
