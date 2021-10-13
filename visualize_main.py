import os
import sys

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


dataframe = pd.read_csv('monitored_archive/' + sys.argv[1] + '.csv', names=['time', 'upvotes', 'ratio'], header=None)

figure = make_subplots(specs=[[{"secondary_y": True}]])

figure.add_trace(
    go.Scatter(x=dataframe['time'], y=dataframe['upvotes'], name='upvotes'),
    secondary_y=False
)
figure.add_trace(
    go.Scatter(x=dataframe['time'], y=dataframe['ratio'], name='ratio'),
    secondary_y=True
)

figure.update_layout(
    title_text='Retrieved vote data for reddit post <b><a href = \'https://reddit.com/' + sys.argv[1] + '\'>' + sys.argv[1] + '</a></b>'
)

figure.update_xaxes(title_text="Time")
figure.update_yaxes(title_text="Upvotes", secondary_y=False)
figure.update_yaxes(title_text="Upvote ratio", secondary_y=True)

figure.show()

if not os.path.exists('images'):
    os.mkdir('images')
figure.write_image('images/' + sys.argv[1] + '.svg')