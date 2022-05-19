#!/usr/bin/env python3

import numpy as np
from scipy import signal
from pydantic import validate_arguments

from ..spectrum import Spectrum
from ramanchada2.misc.spectrum_deco import (add_spectrum_method,
                                            add_spectrum_filter)


@add_spectrum_method
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def find_peaks(
        spe: Spectrum, /,
        prominence: float = 1e-2,
        width: int = 1):
    """
    Find peaks in spectrum.

    Parameters
    ----------
    prominence : float, optional
        the minimal net amplitude for a peak to be considered, by default 1e-2
    width : int, optional
        the minimal width of the peaks, by default 1

    Returns
    -------
    _type_
        _description_
    """
    loc, data = signal.find_peaks(spe.y, prominence=prominence, width=width)
    w = data['widths']
    bounds = np.stack((data['left_ips'] - 2*w,
                       data['right_ips'] + 2*w
                       ), axis=-1).astype(int)
    ampl = data['prominences']
    return dict(amplitudes=ampl,
                locations=loc,
                widths=w,
                bounds=bounds)


@add_spectrum_filter
@validate_arguments(config=dict(arbitrary_types_allowed=True))
def find_peaks_filter(
        old_spe: Spectrum,
        new_spe: Spectrum, /,
        *args, **kwargs):
    res = old_spe.find_peaks(*args, **kwargs)  # type: ignore
    new_spe.result = {k: v.tolist() for k, v in res.items()}
