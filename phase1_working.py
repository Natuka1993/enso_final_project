from grab_cesm import open_cesm2le

def open_cesm_temp_surface():
    """
    Open CESM ocean temperature and return the surface layer.
    """
    temp = open_cesm2le(
        "TEMP",
        component="ocn",
        scenario="historical",
        forcing="cmip6",
        time_slice=("1990-01", "1991-12"),
        members=0,
    )
    return temp.isel(z_t=0)

if __name__ == "__main__":
    temp_surface = open_cesm_temp_surface()
    print(temp_surface)
    print(temp_surface.dims)
    print(temp_surface.sizes)

    tiny = temp_surface.isel(time=0).load()
    tiny.plot()