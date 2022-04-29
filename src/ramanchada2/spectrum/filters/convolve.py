#!/usr/bin/env python3

from typing import Literal, Union, Callable

import numpy as np
from numpy.typing import NDArray
from scipy import signal
import lmfit
from pydantic import validate_arguments

from ramanchada2.misc.spectrum_deco import spectrum_algorithm_deco
from ..spectrum import Spectrum


@spectrum_algorithm_deco
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def convolve(
        old_spe: Spectrum,
        new_spe: Spectrum,
        lineshape: Union[Callable[[Union[float, NDArray]], float],
                         Literal[
                              'gaussian', 'gaussian2d', 'lorentzian',
                              'voigt', 'pvoigt', 'moffat',
                              ]],
        **kwargs):
    if callable(lineshape):
        shape_fun = lineshape
    else:
        shape_fun = getattr(lmfit.lineshapes, lineshape)

    leny = len(old_spe.y)
    x = np.arange(-(leny-1)//2, (leny+1)//2, dtype=float)
    shape_val = shape_fun(x, **kwargs)
    new_spe.y = signal.convolve(old_spe.y, shape_val, mode='same')
