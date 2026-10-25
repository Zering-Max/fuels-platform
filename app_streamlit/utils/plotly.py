
from pandas import DataFrame
import plotly.graph_objects as go
from typing import List

def change_zoom(radius:int) -> int:
  if (radius == 10):
    return 11
  elif (radius == 25):
    return 9
  elif (radius == 50):
    return 8
  elif(radius > 50):
    return 7

def create_map(
    df:DataFrame,
    coord_center:List[float],
    height:int = 500,
    width:int = 400,
    color_points:List[str] = ["#1BC258","#E4DD1E", '#E28B1A'] + ["crimson", ]*7,
    zoom:int=11,
):
  fig = go.Figure()
  fig.add_trace(
    go.Scattermap(
        lat=df["latitude"],
        lon=df["longitude"],
        mode = "markers+text",
        marker=dict(
                  size=8,
                  color=color_points,
                  ),
        text = ["1er", "2ème", "3ème"],
        textposition = "middle right",
        textfont = dict(size=10, color="black", family="Metropolis Extra Bold", weight=700),
        customdata=df,
        hovertemplate= """%{customdata[2]}, %{customdata[3]} %{customdata[4]}<br>""" + \
        """Economies nettes : %{customdata[8]} €""" + \
        """<extra></extra>"""
        ,
      )
    )
  fig.update_layout(
      # Centrer la map autour d'un "point" (endroit map monde) particulier
      map=dict(
          bearing=0,
          center=dict(
              lat=coord_center[0],
              lon=coord_center[1]
          ),
          zoom=zoom,
          style="basic"
      ),
      margin=dict(
        l=30,
        r=30,
        t=30,
        b=20
      ),
      # augmenter la taille de vision de la fenêtre
      height=height,
      width=width
    )
  return fig