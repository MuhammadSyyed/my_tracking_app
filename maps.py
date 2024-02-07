import folium
from datetime import datetime
from geopy.geocoders import Nominatim


def get_lat_lon(location_name):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.geocode(location_name)
    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return None


def generate_map(coordinates, location_name):
    if coordinates:
        lat = coordinates[0]
        long = coordinates[1]
        map = folium.Map(location=[lat, long], zoom_start=150)

        # create an iframe pop-up for the marker
        popup_html = f"<b>Date:</b> 10th October, 2023<br/>"
        popup_html += f"<b>Location:</b> Department of Maths <br/>"
        popup_html += f"<b>Time:</b> {datetime.now()}<br/>"
        popup_html += '<b><a href="{}" target="_blank">Event Page</a></b>'.format(
            "Testing Map"
        )
        popup_iframe = folium.IFrame(width=200, height=110, html=popup_html)

        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(popup_iframe),
            icon=folium.Icon(color="red"),
        ).add_to(map)
        points = [(24.94411, 67.08085), (24.9443, 67.0793), (24.94351, 67.08298)]
        folium.PolyLine(points, color="red", weight=5, opacity=0.85).add_to(map)

        map.save("map.html")
    else:
        print(
            f"Location not found for {location_name}. Please check the spelling or provide more details."
        )


if __name__ == "__main__":
    location_name = input("Enter a location name: ")
    # coordinates = get_lat_lon(location_name)

    coordinates = (24.94411, 67.08085)
    generate_map(coordinates, location_name)
