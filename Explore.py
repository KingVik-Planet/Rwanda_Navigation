import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import openrouteservice

# Function to perform the search
def search_location(query):
    geolocator = Nominatim(user_agent="my_search_app")
    location = geolocator.geocode(query)

    if location:
        return [location.latitude, location.longitude]
    else:
        return None

# Function to calculate ETA and draw route
def calculate_and_draw_route(start, end, map_object):
    # Set up OpenRouteService client
    client = openrouteservice.Client(key='YOUR_OPENROUTESERVICE_API_KEY')

    # Check if start and end coordinates are valid
    if not start or not end:
        st.warning("Invalid start or end location. Please enter valid locations.")
        return

    try:
        # Find the nearest routable points for start and end
        start_nearest = client.pelias_search(start, number=1)['features'][0]['geometry']['coordinates']
        end_nearest = client.pelias_search(end, number=1)['features'][0]['geometry']['coordinates']

        # Calculate route
        route = client.directions(coordinates=[start_nearest, end_nearest], profile='driving-car', format='geojson')

        # Draw the route on the map
        folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']],
                        color='blue').add_to(map_object)

        # Calculate ETA
        duration = route['features'][0]['properties']['segments'][0]['duration']
        st.write(f"Estimated Time of Arrival (ETA): {duration} seconds")
    except openrouteservice.exceptions.ApiError as e:
        st.warning(f"Error calculating route: {e}")


# Streamlit app
st.title("Rwanda Navigation")

# User input for start and end locations
start_query = st.text_input("Enter Start Location:")
end_query = st.text_input("Enter End Location:")

# Check if both queries are not empty
if start_query and end_query:
    # Search for the start and end locations
    start_location = search_location(start_query)
    end_location = search_location(end_query)

    # Determine the center of the map
    if start_location and end_location:
        map_center = [(start_location[0] + end_location[0]) / 2, (start_location[1] + end_location[1]) / 2]
    elif start_location:
        map_center = start_location
    elif end_location:
        map_center = end_location
    else:
        st.warning("Start and end locations not found. Please enter valid locations.")
        map_center = [0, 0]

    # Display the map centered at the determined center
    result_map = folium.Map(location=map_center, zoom_start=12)

    # Add a marker for the start location
    if start_location:
        folium.Marker(
            location=start_location,
            popup="Start: " + start_query,
            icon=folium.Icon(color='green')
        ).add_to(result_map)

    # Add a marker for the end location
    if end_location:
        folium.Marker(
            location=end_location,
            popup="End: " + end_query,
            icon=folium.Icon(color='red')
        ).add_to(result_map)

        # Calculate and draw the route
        calculate_and_draw_route(start_location, end_location, result_map)

        # Display the result map using folium_static
        st.write("Route from", start_query, "to", end_query)
        folium_static(result_map)
    else:
        st.warning("End location not found. Please enter a valid location.")
else:
    st.warning("Please enter both start and end locations.")
