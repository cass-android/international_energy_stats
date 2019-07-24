import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

data = pd.read_csv('~/code/intenergy/all_energy_statistics_2019.csv')

# just for testing! have to convert units!
totals1990 = pd.DataFrame(data[data['Year']==1990].groupby(by=['Country or Area'])['Quantity'].sum())
totals2016 = pd.DataFrame(data[data['Year']==2016].groupby(by=['Country or Area'])['Quantity'].sum())


import urllib, json


app.layout = html.Div([
    html.H1('International Energy Statistics', style={
            'textAlign': 'center', 'margin': '16px 10', 'fontFamily': 'system-ui'}),
	html.Div([
	    dcc.Graph(
	        id='example-graph',
	        figure={
	            'data': [
	                {'x': totals1990.index, 'y': totals1990['Quantity'], 'type': 'bar', 'name': '1990 Total Energy'},
	                {'x': totals2016.index, 'y': totals2016['Quantity'], 'type': 'bar', 'name': '2016 Total Energy'},
	            ],
	            'layout': {
	                'title': 'Example Graph - Total Energy 1990 vs 2016 (units tbd)'
                }
            }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)