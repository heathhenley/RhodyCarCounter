import datetime
import pandas as pd
import plotly.express as px
import requests


API = r"https://rhodycarcounter-production.up.railway.app/api/"

def main():
  # Get all the cameras: 
  cameras = requests.get(API + "cameras/").json()
  timeseries = {}
  for camera in cameras:
    # Get the latest datapoints for each camera:
    datapoints = requests.get(
      API + f"cameras/{camera['id']}/datapoints?limit=150").json()
    datapoints.reverse()
    timeseries[camera['id']] = datapoints
  cameras_dict = {camera['id']: camera for camera in cameras}
  data = []
  for camera_id, datapoints in timeseries.items():
    # Get lat and lon for each camera:
    lat = cameras_dict[camera_id]['latitude']
    lon = cameras_dict[camera_id]['longitude']
    for datapoint in datapoints:
      # Get timestamp and vehicles: 
      timestamp = datetime.datetime.strptime(
        datapoint["timestamp"], "%Y-%m-%dT%H:%M:%S")
      timestamp = timestamp - datetime.timedelta(hours=4)
      vehicles = datapoint['vehicles']
      data.append([camera_id, lat, lon, timestamp, vehicles])
  df = pd.DataFrame(data, columns=['Camera', 'Latitude', 'Longitude', 'Timestamp', 'Vehicles'])
  print(df.head())
  df.sort_values(by=['Timestamp'], inplace=True)
  df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %I:%M %p")
  fig = px.density_mapbox(
            df, lat='Latitude', lon='Longitude', z='Vehicles', animation_frame='Timestamp', animation_group='Camera',
            radius=30, center=dict(lat=41.8258, lon=-71.41058), zoom=12,
            range_color=[0, 20], mapbox_style="open-street-map",
            title="Providence, RI Traffic Density Map",
            opacity=0.75)
  fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
  fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
  fig.layout.updatemenus[0].buttons[0].args[1]["automargin"] = False
  fig.layout.updatemenus[0].buttons[0].args += ({"automargin" : False},)
  fig.layout.updatemenus[0].buttons[1].args += ({"automargin" : False},)
  fig.layout.updatemenus[0].buttons[1].args[1]["automargin"] =  False

  for step in fig.layout.sliders[0]['steps']:
    #print(step['args'])
    step['args'] += ({"automargin": False},)
  fig.update_xaxes(automargin=False)
  fig.update_yaxes(automargin=False)
  fig.update_coloraxes(showscale=False)
  fig.write_html("heatmap.html")
  fig.show()
  return 0


if __name__ == '__main__':
  main()