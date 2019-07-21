import dash
import dash_core_components as dcc
import dash_html_components as html
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

app.layout = html.Div([
    html.H1('International Energy Statistics', style={
            'textAlign': 'center', 'margin': '16px 10', 'fontFamily': 'system-ui'}),
    dcc.Tabs(id="tabs", children=[
    	dcc.Tab(label='Tab one', children=[
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
        ]),
        dcc.Tab(label='Tab two', children=[
            html.Div([
                html.H1("This is the content in tab 2"),
                html.P("A graph here would be nice!")
            ])
        ]),
        dcc.Tab(label='Tab three', children=[
            html.Div([
                html.H1("This is the content in tab 3"),
            ])
        ]),
    ],
        style={
        'fontFamily': 'system-ui'
    },
        content_style={
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '44px'
    },
        parent_style={
        'maxWidth': '1500px',
        'margin': '0 auto'
    }
    )
])        

if __name__ == '__main__':
    app.run_server(debug=True)