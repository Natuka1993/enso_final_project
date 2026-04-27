"""
Input/output utilities for enso_toolkit.
"""

from grab_cesm import open_cesm2le


def open_cesm_temp(
    time_slice=("1990-01", "1991-12"),
    member=0,
):
    """
    Open CESM ocean potential temperature data.
    """
    return open_cesm2le(
        "TEMP",
        component="ocn",
        scenario="historical",
        forcing="cmip6",
        time_slice=time_slice,
        members=member,
    )