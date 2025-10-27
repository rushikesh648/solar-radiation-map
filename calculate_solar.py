import os
import sys
import subprocess
from grass.script import core as gcore
from grass.pygrass.gis import Mapset

def setup_grass_environment():
    """Sets up the GRASS GIS environment variables required to run r.sun."""
    # NOTE: Replace 'C:/OSGeo4W/apps/grass/grass78' with your actual GRASS path.
    grass_dir = 'C:/OSGeo4W/apps/grass/grass78' 
    os.environ['GISBASE'] = grass_dir
    sys.path.append(os.path.join(os.environ['GISBASE'], 'etc', 'python'))
    
    # Initialize GRASS session (Conceptual setup for running GRASS tools)
    # In a real setup, you would use grass.script.setup
    
    # This is often done by sourcing a shell script or using a full setup function
    # For simplicity, we just check the path:
    if not os.path.exists(os.environ['GISBASE']):
        print(f"Error: GRASS GIS not found at {grass_dir}. Please correct the path.")
        sys.exit(1)
        
    print("GRASS GIS environment variables set successfully.")

def run_solar_analysis(input_dem, output_solar_map, day_of_year=172):
    """
    Calculates the Global Solar Radiation (Insolation) using r.sun.
    
    Args:
        input_dem (str): Name of the input DEM raster file in the GRASS mapset.
        output_solar_map (str): Name for the output Global Radiation raster.
        day_of_year (int): Day number (1-365) for which to calculate radiation. 
                           Default 172 is the Summer Solstice (approx. June 21).
    """
    # 1. Set the computational region and resolution to match the input DEM
    gcore.run_command('g.region', raster=input_dem, flags='p')
    
    print(f"Starting solar radiation calculation for Day {day_of_year}...")
    
    # 2. Run r.sun to calculate the global radiation (glob_rad)
    # The 'r.sun' module calculates direct, diffuse, and reflected radiation.
    # It requires an elevation map, aspect, and slope, but can derive them 
    # internally or use an existing DEM if properly configured.
    # We use a simplified call here.
    
    gcore.run_command(
        'r.sun',
        elevation=input_dem,
        glob_rad=output_solar_map,
        day=day_of_year,
        step=0.5, # Time step in hours (0.5 for 30-min intervals)
        albedo=0.2, # Typical albedo for grass/soil
        flags='s' # s flag for saving solar parameters to map history
    )
    
    print(f"\nSolar radiation map '{output_solar_map}' created successfully.")

if __name__ == '__main__':
    # --- Configuration ---
    # Replace these placeholders with your actual GRASS setup (location and mapset)
    GISDBASE = 'C:/GIS_Projects/Solar_Repo_Data'
    LOCATION_NAME = 'MyLocation'
    MAPSET_NAME = 'PERMANENT'
    
    # Replace 'my_city_dem' with the name of your DEM file that you've imported into GRASS.
    INPUT_DEM_RASTER = 'my_city_dem' 
    OUTPUT_SOLAR_RASTER = 'annual_solar_insolation_whm2'

    # --- Execution ---
    # This part is highly dependent on how your GRASS is integrated with Python
    # This block represents the conceptual steps you would automate:
    
    try:
        # 1. Setup the environment
        # NOTE: This step is often done automatically when running a script 
        # inside a QGIS/GRASS environment or using a GRASS start script.
        setup_grass_environment()
        
        # 2. Check if the necessary input DEM exists (conceptual check)
        # In a real setup, you'd use a GRASS command like gcore.find_file
        if not Mapset(MAPSET_NAME, LOCATION_NAME, GISDBASE).find_file(INPUT_DEM_RASTER, 'raster'):
             print(f"Error: Input raster '{INPUT_DEM_RASTER}' not found in GRASS mapset.")
             sys.exit(1)
             
        # 3. Run the core analysis
        run_solar_analysis(INPUT_DEM_RASTER, OUTPUT_SOLAR_RASTER)
        
    except ImportError:
        print("\nFATAL ERROR: The 'grass' Python library is not installed or the environment is not set correctly.")
        print("Please ensure you are running this script from within a configured GRASS GIS or QGIS environment.")
    except Exception as e:
        print(f"\nAn error occurred during GIS processing: {e}")
