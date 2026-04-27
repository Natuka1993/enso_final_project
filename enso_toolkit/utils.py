"""
Utility functions for enso_toolkit.
"""


def validate_dataarray(da, required_dims=None):
    """
    Validate that input is an xarray DataArray-like object.
    """
    if da is None:
        raise ValueError("Input data cannot be None.")

    if not hasattr(da, "dims"):
        raise TypeError("Input must be an xarray DataArray or DataArray-like object.")

    if required_dims is not None:
        missing = [dim for dim in required_dims if dim not in da.dims]
        if missing:
            raise ValueError(
                f"Input data is missing required dimensions: {missing}. "
                f"Available dimensions are: {da.dims}"
            )