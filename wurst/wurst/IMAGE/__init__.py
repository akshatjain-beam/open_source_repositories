import json
import os

IMAGE_TOPOLOGY = json.load(
    open(os.path.join(os.path.dirname(__file__), "metadata", "region-topolgy.json"))
)


def load_regions_from_json():
    """Load regions from a JSON file."""
    with open(os.path.join(os.path.dirname(__file__), "metadata", "region-topolgy.json"), 'r') as file:
        regions_data = json.load(file)
    
    regions = []
    for region, countries in regions_data.items():
        regions.append(region)
    
    return regions

# Call the function to load regions from the JSON file
REGIONS = load_regions_from_json()