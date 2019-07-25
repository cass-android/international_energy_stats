import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import urllib, json

from dash.dependencies import Input, Output, State
from prep import * 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# for dropdown menu - years
values = sorted(list(df.Year.unique()))[1:-1]
labels = [str(x) for x in values]

options = []
for n in range(len(values)):
    options.append(dict([('label',labels[n]), ('value',values[n])]))

# for dropdown menu - measures
values2 = ['Quantity_TJ','TJ_per_capita', 'TJ_per_USD_GDP']
labels2 = ['Total Energy','Per Capita', 'Per GDP (USD)']

options2 = []
for n in range(len(values2)):
    options2.append(dict([('label',labels2[n]), ('value',values2[n])]))


app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),
    html.H1('International Energy Scoreboard', style={
            'textAlign': 'center', 'margin': '16px 10', 'fontFamily': 'system-ui'
            }),

    html.Div(
        [dcc.Dropdown(
        id='year_dropdown',
        options=options,
        value=2016
        ),
    ]),

    html.Div(
        [dcc.Dropdown(
        id='measure_dropdown',
        options=options2,
        value='Quantity_TJ'
        ),
    ]),


    html.Div(
        id='graph1-container'
        ),

    html.Div(
        id='graph2-container'
        ),

    html.Div(
        id='graph3-container'
        ),
    ])

@app.callback(
    dash.dependencies.Output(component_id='my-div', component_property='children'),
    [dash.dependencies.Input(component_id='my-id', component_property='value')]
    )

def test(value):
    return(str(type(df['Year'][0])))

@app.callback(
    dash.dependencies.Output('graph1-container', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph1(input_year, input_measure):

    largest = totals_con[totals_con['Year']==input_year
    ].nlargest(40, input_measure)
    smallest = totals_con[totals_con['Year']==input_year
    ].nsmallest(5, input_measure)
    largest_and_smallest = pd.concat(objs = [largest, smallest])

    def set_color(x):
        if(x == 'Canada'):
            return "red"
        else:
            return "blue"

    return [
        dcc.Graph(
            id='Energy Consumption',
            figure={
                'data': [
                    {'x': largest_and_smallest['Country or Area'],
                     'y': largest_and_smallest[input_measure], 
                    'type': 'bar', 
                    'orientation':'v',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'y',
                        'order': 'descending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Energy Consumption (TJ)'
                }
            }
        ),
    ]

@app.callback(
    dash.dependencies.Output('graph2-container', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph2(input_year, input_measure):

    largest = totals_imp[totals_imp['Year']==input_year
    ].nlargest(40, input_measure)
    smallest = totals_imp[totals_imp['Year']==input_year
    ].nsmallest(5, input_measure)
    largest_and_smallest = pd.concat(objs = [largest, smallest])

    def set_color(x):
        if(x == 'Canada'):
            return "red"
        else:
            return "blue"

    return [
        dcc.Graph(
            id='Energy Imports',
            figure={
                'data': [
                    {'x': largest_and_smallest['Country or Area'],
                     'y': largest_and_smallest[input_measure], 
                    'type': 'bar', 
                    'orientation':'v',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'y',
                        'order': 'descending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Energy Imports (TJ)'
                }
            }
        ),
    ]

@app.callback(
    dash.dependencies.Output('graph3-container', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph3(input_year, input_measure):

    largest = totals_exp[totals_exp['Year']==input_year
    ].nlargest(40, input_measure)
    smallest = totals_exp[totals_exp['Year']==input_year
    ].nsmallest(5, input_measure)

    largest_and_smallest = pd.concat(objs = [largest, smallest])

    def set_color(x):
        if(x == 'Canada'):
            return "red"
        else:
            return "blue"

    return [
        dcc.Graph(
            id='Energy Exports',
            figure={
                'data': [
                    {'x': largest_and_smallest['Country or Area'],
                     'y': largest_and_smallest[input_measure], 
                    'type': 'bar', 
                    'orientation':'v',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'y',
                        'order': 'descending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Energy Exports (TJ)'
                }
            }
        ),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
