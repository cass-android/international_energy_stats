import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import urllib, json

from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

df = pd.read_csv('~/code/intenergy/all_energy_statistics_2019_V2.csv')

values = sorted(list(df.Year.unique()))[1:-1]
labels = [str(x) for x in values]

options = []
for n in range(len(values)):
    options.append(dict([('label',labels[n]), ('value',values[n])]))


app.layout = html.Div([
    html.H1('International Energy Statistics', style={
            'textAlign': 'center', 'margin': '16px 10', 'fontFamily': 'system-ui'}),

    html.Div(
        [dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=2016
        ),
    ]),

    html.Div(
        id='output-container',
        )
    ])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
    )


def update_output(value):
    

    largest = pd.DataFrame(
    df[
        (df['Year']==value) &
        (df['Flow_Category']=='Final consumption')
        ].groupby(by=['Country or Area'])['Quantity_TJ'].sum()
        ).nlargest(30,'Quantity_TJ')

    smallest = pd.DataFrame(
    df[
        (df['Year']==value) &
        (df['Flow_Category']=='Final consumption')
        ].groupby(by=['Country or Area'])['Quantity_TJ'].sum()
        ).nsmallest(5,'Quantity_TJ')

    canada = pd.DataFrame(
    df[
        (df['Year']==value) &
        (df['Flow_Category']=='Final consumption') &
        (df['Country or Area']=='Canada')
        ].groupby(by=['Country or Area'])['Quantity_TJ'].sum()
        )
    
    totals= pd.concat(objs = [largest, smallest])

    def set_color(x):
        if(x == 'Canada'):
            return "red"
        else:
            return "blue"

    return [dcc.Graph(
            id='Total Energy Consumption By Year',
            figure={
                'data': [
                    {'x': totals.index,
                     'y': totals['Quantity_TJ'], 
                    'type': 'bar', 
                    'orientation':'v',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'y',
                        'order': 'descending'
                        }],
                    'marker': dict(color=list(map(set_color,totals.index)))
                    },
                ],
                'layout': {

                    'title': 'Total Energy Consumption (TJ)'
                }
            }
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
