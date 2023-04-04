#!/usr/bin/env python3

from typing import Union

import numpy as np
from pydantic import validate_arguments, PositiveFloat

from ramanchada2.misc.spectrum_deco import add_spectrum_filter
from ..spectrum import Spectrum


@add_spectrum_filter
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def add_gaussian_noise(
        old_spe: Spectrum,
        new_spe: Spectrum, /,
        sigma: PositiveFloat,
        rng_seed: Union[int, None] = None):
    r"""
    Add gaussian noise to the spectrum.
    Random number i.i.d. $N(0, \sigma)$ is added to every sample

    Parameters
    ----------
    sigma : float
        sigma of the gaussian noise
    rng_seed : int, optional
        seed for the random generator
    """
    rng = np.random.default_rng(rng_seed)
    dat = old_spe.y + rng.normal(0., sigma, size=len(old_spe.y))
    if any(dat < 0):
        dat += abs(dat.min())
    new_spe.y = np.array(dat)
