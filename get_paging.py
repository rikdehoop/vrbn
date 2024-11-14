import requests
import geopandas as gpd
import tempfile
import logging
import os
from shapely.geometry import shape

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the vector grid into a GeoDataFrame
gdf_grid = gpd.read_file("vrbn_master/vrbn_grid.gpkg")

# Define the WFS base URL
base_url = "https://service.pdok.nl/lv/bag/wfs/v2_0"

# Create an empty GeoDataFrame to hold the combined data for all features
all_combined_gdf = gpd.GeoDataFrame()

# Iterate over each feature and extract its bounding box
for idx, feature in gdf_grid.iterrows():
    # Extract the bounding box (minx, miny, maxx, maxy)
    bbox = feature.geometry.bounds
    minx, miny, maxx, maxy = bbox
    logging.info(f"Processing feature {idx} Bounding Box: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")

    # Define the parameters for the WFS request
    params = {
        "REQUEST": "GetFeature",
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "OUTPUTFORMAT": "application/gml+xml; version=3.2",
        "BBOX": f"{minx},{miny},{maxx},{maxy}",
        "srsName": "EPSG:28992",
        "TYPENAMES": "bag:pand",
        "count": 500  # Number of records per page
    }

    # Initialize a GeoDataFrame to store data for the current feature
    combined_gdf = gpd.GeoDataFrame()

    # Loop to handle paging for WFS requests
    for page in range(1000):  # Set high limit if many pages are expected
        params["startindex"] = page * params["count"]

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp_file:
                tmp_file.write(response.content)
                temp_file_path = tmp_file.name

            # Read the response content into a GeoDataFrame
            try:
                gpd_data = gpd.read_file(temp_file_path, driver='GML', layer="pand")
            except Exception as e:
                logging.error(f"Failed to read data for page {page}: {e}")
                break

            # Append the new data to the combined GeoDataFrame
            if not gpd_data.empty:
                combined_gdf = combined_gdf._append(gpd_data, ignore_index=True)
                logging.info(f"Page {page} data retrieved.")
            else:
                logging.info(f"No more data found for page {page}. Ending pagination.")
                break

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve data for page {page}: {e}")
            break  # Stop the loop on network errors

        finally:
            # Clean up the temporary file after reading
            os.remove(temp_file_path)

    # Add the combined data for the current feature to the main GeoDataFrame
    all_combined_gdf = all_combined_gdf._append(combined_gdf, ignore_index=True)

# Drop duplicate geometries
all_combined_gdf.set_geometry('geometry', inplace=True)
all_combined_gdf = all_combined_gdf.drop_duplicates(subset='geometry', keep='first')

# Ensure the CRS is set
if all_combined_gdf.crs is None:
    all_combined_gdf.set_crs("EPSG:28992", allow_override=True, inplace=True)

# Remove any invalid geometries
all_combined_gdf = all_combined_gdf[all_combined_gdf.is_valid]
all_combined_gdf = all_combined_gdf[all_combined_gdf['geometry'].notnull()]

# Save the combined data for all features to a GeoPackage
all_combined_gdf.to_file("combined_bag.gpkg", driver="GPKG")
logging.info("All data successfully saved to 'combined_bag.gpkg'.")
