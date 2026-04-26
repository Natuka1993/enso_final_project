# ENSO / CESM Ocean Temperature Analysis

## 1. Project Overview
This project develops a Python-based toolkit to analyze ocean temperature variability using CESM2 Large Ensemble data hosted on AWS. The focus is on extracting surface temperature fields and building ENSO-relevant diagnostics (climatology, anomalies, and index-based metrics).

---

## 2. Data

- Dataset: CESM2 Large Ensemble (AWS S3)
- Variable: Ocean potential temperature (TEMP)
- Grid: POP ocean grid (nlat, nlon)
- Depth: Surface layer (z_t = 0)
- Time range (current test): 1990–1991

---

## 3. Methods

### 3.1 Data Access
- Used `grab-cesm` package to access CESM data
- Extracted surface layer:

### 3.2 Processing

#### Monthly Climatology

#### Monthly Anomalies


## 4. Current Results

- Successfully accessed CESM ocean data from AWS
- Built reusable Python package (`enso_toolkit`)
- Computed:
  - Surface temperature fields
  - Monthly climatology
  - Monthly anomalies

---

## 5. Issues / Limitations

- Ocean grid is curvilinear (nlat/nlon, not lat/lon)
- `grab-cesm` does not expose TLAT/TLONG → limits spatial subsetting
- Current analysis uses full grid (no Niño 3.4 region yet)

---

## 6. Next Steps

- Implement ENSO index (Niño 3.4 or proxy)
- Improve spatial subsetting for ocean grid
- Add time series visualization
- Compare with observational datasets (optional)

---

## 7. Future Directions

- Extend analysis to longer CESM time series
- Evaluate ENSO variability across ensemble members
- Integrate remote sensing datasets

---

## 8. Key Tools

- Python
- xarray
- zarr
- AWS S3 (cloud-hosted data)
- matplotlib