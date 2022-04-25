#!/usr/bin/env python3

from io import TextIOBase

import pandas as pd
from pydantic import validate_arguments


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def lines_from_crystal_dat(data_in: TextIOBase) -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            lin.split()
            for lin in data_in.readlines()
            if not lin.startswith('#')
        ],
        columns=[
            'FREQUENCIES', 'I_tot', 'I_par', 'I_perp',
            'I_xx', 'I_xy', 'I_xz', 'I_yy', 'I_yz', 'I_zz'
        ],
        dtype=float)
