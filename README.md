# Solar Radiation Map Generator (r.sun Automation)

This repository contains Python code to automate the creation of a solar radiation (insolation) map using the powerful **GRASS GIS** engine, which is integrated into QGIS.

## Prerequisites

1.  **QGIS with GRASS GIS:** You must have QGIS installed, as it bundles the necessary GRASS GIS tools (`r.sun`).
2.  **Digital Elevation Model (DEM) Data:** A GeoTIFF file (`.tif`) for your area of interest. This file is required for the terrain analysis.
3.  **Python Environment:** A Python environment configured to run GRASS commands (typically achieved by running the script from within the QGIS Python console or a GRASS shell).

## 🚀 Setup and Execution

### Step 1: Import DEM into GRASS

Before running the script, you must import your DEM file into a GRASS location/mapset.

1.  Open QGIS.
2.  Go to **Processing > Toolbox**.
3.  Search for **`r.in.gdal`** (under GRASS).
4.  Set your input DEM file and import it into your desired GRASS **Location** and **Mapset**. Note the name you assign to the raster (e.g., `my_city_dem`).

### Step 2: Configure `calculate_solar.py`

Open the `calculate_solar.py` file and modify the following variables to match your GRASS setup and data:

| Variable | Description |
| :--- | :--- |
| `GISDBASE` | The path to your main GRASS database directory. |
| `LOCATION_NAME` | The name of your GRASS Location. |
| `MAPSET_NAME` | The name of your GRASS Mapset (usually `PERMANENT`). |
| `INPUT_DEM_RASTER` | The name of the DEM raster *inside* the GRASS mapset (e.g., `'my_city_dem'`). |

### Step 3: Run the Script

Execute the script from your command line after ensuring your path is correctly configured for the GRASS environment:

```bash
python calculate_solar.py
