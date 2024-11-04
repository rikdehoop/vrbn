import requests
import geopandas as gpd
import pandas as pd


# Define the parameters for the WFS request
base_url = "https://service.pdok.nl/lv/bag/wfs/v2_0"
params = {
    "REQUEST": "GetFeature",
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "OUTPUTFORMAT": "application/gml+xml; version=3.2",
    "BBOX": "143182.85288681273232214,411015.42059764923760667,154668.9596401458256878,412900.32016742700943723",
    "srsName": "EPSG:28992",
    "TYPENAMES": "bag:pand",
    "count": 500  # Number of records per page
}



# Create an empty GeoDataFrame to hold the combined data
combined_gdf = gpd.GeoDataFrame()

# Loop to handle paging
for page in range(1000):  # Adjust this if you expect more pages
    params["startindex"] = page * params["count"]  # Set startindex for the current page
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Read the response content into a GeoDataFrame
        gpd_data = gpd.read_file(response.content, driver='GML', layer="pand")
        
        # Append the new data to the combined GeoDataFrame
        combined_gdf = pd.concat([combined_gdf, gpd_data], ignore_index=True)
        
        # Optional: Print the current page data
        print(f"Page {page} data:")
        print(gpd_data)
    if gpd_data.empty:
        break
    elif response.status_code != 200:
        print(f"Failed to retrieve data for page {page}: {response.status_code}")

# After the loop, you can check the combined GeoDataFrame
print("Combined GeoDataFrame:")
print(combined_gdf)
combined_gdf.to_file("combined_bag.gpkg", driver="GPKG")
# insert_gpkg_to_existing_schema("geo", "geo", "iELo3Y9/OZDE", "geo.vrbn.nl", "5432", "interne_data", "combined_bag.gpkg")
