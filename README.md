# ENSO Toolkit: CESM Ocean Temperature Analysis

This project builds a lightweight Python package (`enso_toolkit`) for analyzing CESM ocean model output, with a focus on ENSO-related variability.

---

## Overview

CESM ocean model output is large and not immediately analysis-ready.  
This toolkit simplifies a typical workflow:

- Load CESM ocean temperature data
- Extract surface temperature
- Compute climatology and anomalies
- Generate time series diagnostics
- Approximate Niño 3.4 index

---

## Package Structure

```
enso_final_project/
├── enso_toolkit/
│   ├── core.py      # main analysis functions
│   ├── io.py        # data loading
│   ├── utils.py     # validation helpers
├── examples/
│   ├── quickstart.py
│   ├── exploration.ipynb   # exploratory analysis notebook
├── slides.qmd
├── README.md
└── pyproject.toml
```

---

## Notebooks

- `examples/exploration.ipynb` — exploratory analysis used during development  
  (includes intermediate calculations and testing before packaging into functions)

---

## Installation

```bash
pip install -e .
```

---

## Example Usage

```python
from enso_toolkit import (
    open_cesm_temp_surface,
    compute_global_mean_anomaly,
    compute_nino34_index,
)

da = open_cesm_temp_surface()

global_anom = compute_global_mean_anomaly(da)
nino = compute_nino34_index(da)
```

---

## Results

This workflow produces:

- Global surface temperature map  
- Spatial mean anomaly time series  
- Approximate Niño 3.4 index  

---

## Scientific Context

ENSO (El Niño–Southern Oscillation) is a dominant mode of interannual climate variability.

This project provides a foundation for:

- analyzing ENSO signals in CESM output  
- comparing with machine-learning-based models (e.g., CAMulator)  
- integrating with satellite observations  

---

## Data Sources

- CESM model output   
- (Future work) satellite datasets: MODIS, TRMM, ASCAT  

---

## Future Work

- Implement true Niño 3.4 region (lat/lon masking)  
- Extend to longer time periods  
- Add ensemble members  
- Compare CESM with CAMulator output  
- Improve visualization tools  

---

## Author

Natalia Jorbenadze