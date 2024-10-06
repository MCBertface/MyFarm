import folium
from streamlit_folium import folium_static
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import climateserv
import pandas as pd
import os

# Initialize the geocoder
geolocator = Nominatim(user_agent="streamlit_app")

# Function to get coordinates from an address
def get_coordinates(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None

# Function to make the ClimateSERV API call and retrieve data
def request_climateserv_data(x, y, outfile='out.csv'):
    GeometryCoords = [[x - 0.01, y + 0.01], [x + 0.01, y + 0.01],
                      [x + 0.01, y - 0.01], [x - 0.01, y - 0.01], [x - 0.01, y + 0.01]]
    DatasetType = 40
    OperationType = 'Average'
    EarliestDate = '01/03/2018'
    LatestDate = '03/16/2018'
    SeasonalEnsemble = ''  # Leave empty when using the new integer dataset IDs
    SeasonalVariable = ''  # Leave empty when using the new integer dataset IDs

    climateserv.api.request_data(DatasetType, OperationType,
                                 EarliestDate, LatestDate, GeometryCoords,
                                 SeasonalEnsemble, SeasonalVariable, outfile)

# Streamlit app layout
st.title("Interactive Map with Address Input")

# Input field for the address
address = st.text_input("Enter an address:")

# Create a Folium map centered on a default location
default_location = [20, 0]
zoom_level = 2

if address:
    coordinates = get_coordinates(address)
    if coordinates:
        st.write(f"Coordinates for {address}: {coordinates}")
        # Update the map center and zoom level
        default_location = coordinates
        zoom_level = 14

        # Request ClimateSERV data
        x, y = coordinates[1], coordinates[0]
        outfile = 'out.csv'
        request_climateserv_data(x, y, outfile)

        # Display the map with a marker
        world_map = folium.Map(location=default_location, zoom_start=zoom_level)
        folium.Marker(coordinates, popup=address).add_to(world_map)
        folium_static(world_map)

        # Display the CSV file content
        if os.path.exists(outfile):
            df = pd.read_csv(outfile)
            st.write("ClimateSERV Data:")
            st.dataframe(df)
        else:
            st.write("No data available for the specified location.")
    else:
        st.write("Address not found. Showing default location.")
else:
    # Display the default map
    world_map = folium.Map(location=default_location, zoom_start=zoom_level)
    folium_static(world_map)
