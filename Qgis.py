import os
from qgis.core import QgsRasterLayer, QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterMinMaxOrigin, QgsProject, QgsColorRamp

# 1. Define the name of the solar radiation layer in your Layers Panel
LAYER_NAME = "insolation_output" 

# 2. Define the desired color ramp (e.g., 'Plasma', 'Viridis', 'Inferno', 'YlOrRd')
COLOR_RAMP_NAME = "Plasma"

# Get the layer by name
layer = QgsProject.instance().mapLayersByName(LAYER_NAME)

if not layer:
    print(f"Error: Layer '{LAYER_NAME}' not found in the project.")
else:
    # We assume the name is unique, so we take the first match
    raster_layer = layer[0]
    
    if raster_layer.type() == QgsRasterLayer.RasterType and raster_layer.bandCount() >= 1:
        
        # --- 3. Calculate Min/Max values for better styling ---
        # Note: This step can be computationally heavy for large rasters.
        stats = raster_layer.dataProvider().bandStatistics(
            1, # Band number (1 for the first/only band)
            QgsRasterBandStats.All, 
            QgsRasterMinMaxOrigin.Estimated
        )
        
        min_val = stats.minimumValue
        max_val = stats.maximumValue
        
        # --- 4. Create the Color Ramp and Renderer ---
        
        # Fetch the predefined color ramp
        color_ramp = QgsStyle.defaultStyle().colorRamp(COLOR_RAMP_NAME)
        if not color_ramp:
            print(f"Error: Color ramp '{COLOR_RAMP_NAME}' not found.")
        else:
            # Create a list of color entries for the ramp
            ramp_entries = [
                QgsColorRampShader.ColorRampItem(min_val, QColor.fromRgb(255, 255, 255), "Low Insolation"), # Example low color
                QgsColorRampShader.ColorRampItem(max_val, QColor.fromRgb(255, 0, 0), "High Insolation"),  # Example high color
            ]
            
            # Use the fetched color ramp for the shader (more standard approach)
            shader = QgsColorRampShader()
            shader.setColorRampType(QgsColorRampShader.Interpolated)
            shader.setClassificationMode(QgsColorRampShader.Continuous)
            # Apply a predefined ramp for smoother, professional look
            shader.setColorRamp(color_ramp) 
            
            # Create the pseudocolor renderer
            renderer = QgsSingleBandPseudoColorRenderer(raster_layer.bandName(1), shader)
            renderer.setMinimumValue(min_val)
            renderer.setMaximumValue(max_val)

            # --- 5. Apply the Renderer to the Layer ---
            raster_layer.setRenderer(renderer)
            raster_layer.triggerRepaint()
            
            print(f"Successfully styled layer '{LAYER_NAME}' with '{COLOR_RAMP_NAME}' ramp.")

    else:
        print(f"Layer '{LAYER_NAME}' is not a single-band raster layer.")
