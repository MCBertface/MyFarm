import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to add a marker to the map
def add_marker(map_object, latitude, longitude, popup):
    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=folium.Icon(icon='cloud'),
    ).add_to(map_object)

# Streamlit app
st.title("Interactive 2D Map with Streamlit and Folium")

# User inputs for latitude, longitude, and popup text
latitude = st.number_input("Enter Latitude", value=39.8283, format="%f")
longitude = st.number_input("Enter Longitude", value=-98.5795, format="%f")
popup = st.text_input("Enter Popup Text", value="New Marker")

# Button to add marker
if st.button("Add Marker"):
    # Create a map centered around the user input coordinates
    map_object = folium.Map(location=[latitude, longitude], zoom_start=4)
    
    # Add the marker
    add_marker(map_object, latitude, longitude, popup)
    
    # Display the map
    folium_static(map_object)

# Initial map display
if not st.button("Add Marker"):
    # Create a default map centered around the USA
    map_object = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    folium_static(map_object)
