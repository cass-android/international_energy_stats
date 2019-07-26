import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import urllib, json

from dash.dependencies import Input, Output, State
from prep import * 
from graphs import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'dbc.themes.BOOTSTRAP']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# DROPDOWN MENU OPTIONS
# years
year_values = sorted(list(df.Year.unique()))[1:-1]
year_labels = [str(x) for x in year_values]

years = []
for n in range(len(year_values)):
    years.append(dict([('label',year_labels[n]), 
        ('value',year_values[n])]))

# measures
measure_values = ['TJ_per_capita', 'TJ_per_USD_GDP','Quantity_TJ']
measure_labels = ['Per Capita','Per GDP ','Total']

measures = []
for n in range(len(measure_values)):
    measures.append(dict([('label',measure_labels[n]), 
        ('value',measure_values[n])]))

# countries
country_values = sorted(list(df['Country or Area'].unique()))[1:-1]
country_labels = [str(x) for x in country_values]

countries = []
for n in range(len(country_values)):
    countries.append(dict([('label',country_labels[n]), 
        ('value',country_values[n])]))

# LAYOUT

app.layout = html.Div([
    html.H1('Canada\'s International Energy Presence', style={
            'textAlign': 'center', 
            'margin': '14px 10', 
            'fontFamily': 'system-ui',
            }),
    html.Div([
        html.Div([
            dcc.Markdown( "Energy Quantified:"),
            ], style={'width': '30%', 
            'font-size':'150%',
            'display':'inline-block', 
            'vertical-align': 'middle',
            'horizontal-align': 'middle',
            'text-align':'right',
            'margin-right':'10px'}
            ),

        html.Div([
            dcc.Dropdown(
            id='measure_dropdown',
            options=measures,
            value='TJ_per_capita'
                ),
            ], style={'width': '20%',
            'display':'inline-block', 
            'font-size':'150%',
            'vertical-align': 'middle',
            'horizontal-align': 'middle',
            'text-align':'left'}
            ),
        ], style={
        'margin-left':'25%'
        }),

    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Country Rankings', 
            children=[               
                html.Div(
                    id='columns',
                    children=[
                        html.Div(
                            id='g0',
                            className='one-fourth column',
                            children=[
                                html.Div([
                                    dcc.Markdown(''), # text for 'Year' - removed:
                                    ],
                                     style={
                                    'width': '50px', 
                                    'font-size':'150%',
                                    'display':'inline-block', 
                                    'vertical-align': 'middle',
                                    'margin-left':'10px',
                                    'text-align':'left',
                                            }
                                        ),
                                html.Div([
                                    dcc.Dropdown(
                                    id='year_dropdown',
                                    options=years,
                                    value=2016
                                    )],
                                     style={
                                    'width': '100px',
                                    'font-size':'130%',
                                    'vertical-align': 'middle',
                                    'display':'inline-block',
                                    'text-align':'left',
                                            }
                                        ),
                                    ],
                            style={
                            'width':'10%',
                            'padding': '0px',
                            'margin':'0px',
                            'background-color':'#FFFFFF',
                            'height':'1000px'
                            }
                        ),

                        html.Div(
                            id='g1',
                            className='one-fourth column',
                            style={
                            'width':'30%',
                            'padding': '0px',
                            'margin':'0px'
                            }),
                        html.Div(
                            id='g2',
                            className='one-fourth column',
                             style={
                             'width':'30%',
                            'padding': '0px',
                            'margin':'0px'
                            }),
                        html.Div(
                            id='g3',
                            className='one-fourth column',
                            style={
                            'width':'30%',
                            'padding': '0px',
                            'margin':'0px'
                            })
                        ], 
                    className='row'

                    )
                ],
            style={
            'background-color':'#FFFFFF'
            }
            ),

        dcc.Tab(label='1990-2016 Trends', 
            children=[
                html.Div([
                    dcc.Dropdown(
                    id='country_dropdown',
                    options=countries,
                    value='United States',
                    style={
                    'background-color': 'white',
                    'width': '50%', 
                    'font-size':'130%'
                    }
                            ),
                        ],                     
                        style={
                        'background-color': 'white'
                        }),
                    html.Div(
                        id='graph4-container'
                        ),
                    html.Div(
                        id='graph5-container'
                        ),
                    html.Div(
                        id='graph6-container'
                        )],
                )
        ], style={
        'background-color':'#FFFFFF'}
            ),
    ], style={
        'background-color': '#CCE5FF'
    })

# CALLBACKS

@app.callback(
    dash.dependencies.Output('g1', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph1(input_year, input_measure):

    largest = totals_con[totals_con['Year']==input_year
    ].nlargest(50, input_measure)
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
            id='Consumption',
            figure={
                'data': [
                    {'x': largest_and_smallest[input_measure],
                     'y': largest_and_smallest['Country or Area'],
                    'type': 'bar', 
                    'orientation':'h',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'x',
                        'order': 'ascending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Consumption',
                    'height':'1000',
                    'margin': go.layout.Margin(
                        l=160,
                        r=10,
                        b=100,
                        t=100,
                        pad=0
                    ),
                }
            }
        ),
    ]


@app.callback(
    dash.dependencies.Output('g2', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph2(input_year, input_measure):

    largest = totals_imp[totals_imp['Year']==input_year
    ].nlargest(50, input_measure)
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
            id='Imports',
            figure={
                'data': [
                    {'x': largest_and_smallest[input_measure],
                     'y': largest_and_smallest['Country or Area'], 
                    'type': 'bar', 
                    'orientation':'h',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'x',
                        'order': 'ascending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Imports',
                    'height':'1000',
                    'margin': go.layout.Margin(
                        l=160,
                        r=10,
                        b=100,
                        t=100,
                        pad=0
                    ),
                }
            }
        ),
    ]

@app.callback(
    dash.dependencies.Output('g3', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph3(input_year, input_measure):

    largest = totals_exp[totals_exp['Year']==input_year
    ].nlargest(50, input_measure)
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
            id='Exports',
            figure={
                'data': [
                    {'x': largest_and_smallest[input_measure], 
                     'y': largest_and_smallest['Country or Area'],
                    'type': 'bar', 
                    'orientation':'h',
                    'name': 'Annual Energy',
                    'transforms': [{
                        'type': 'sort',
                        'target': 'x',
                        'order': 'ascending'
                        }],
                    'marker': dict(color=list(map(set_color,
                        largest_and_smallest['Country or Area'])))
                    },
                ],
                'layout': {
                    'title': 'Exports',
                    'height':'1000',
                    'margin': go.layout.Margin(
                        l=160,
                        r=10,
                        b=100,
                        t=100,
                        pad=0
                    ),
                }
            }
        ),
    ]
@app.callback(
    dash.dependencies.Output('graph4-container', 'children'),
    [dash.dependencies.Input('country_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph4(input_country, input_measure):
    
    x = totals_con[totals_con['Country or Area']==input_country].sort_values(by='Year')['Year']
    y = totals_con[totals_con['Country or Area']==input_country].sort_values(by='Year')[input_measure]

    x2 = totals_con[totals_con['Country or Area']=='Canada'].sort_values(by='Year')['Year']
    y2 = totals_con[totals_con['Country or Area']=='Canada'].sort_values(by='Year')[input_measure]

    return [
        dcc.Graph(
            id='Energy Consumption Trends',
            figure={
                'data': [
                    {'x': x,
                     'y': y, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Selected Country\'s Consumption',
                    },
                    {'x': x2,
                    'y': y2, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Canada\'s Consumption',
                    },
                ],
                'layout': {
                    'title': 'Energy Consumption'
                }
            }
        ),
    ]

@app.callback(
    dash.dependencies.Output('graph5-container', 'children'),
    [dash.dependencies.Input('country_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph5(input_country, input_measure):

    x = totals_imp[totals_imp['Country or Area']==input_country].sort_values(by='Year')['Year']
    y = totals_imp[totals_imp['Country or Area']==input_country].sort_values(by='Year')[input_measure]

    x2 = totals_imp[totals_imp['Country or Area']=='Canada'].sort_values(by='Year')['Year']
    y2 = totals_imp[totals_imp['Country or Area']=='Canada'].sort_values(by='Year')[input_measure]

    return [
        dcc.Graph(
            id='Energy Imports Trends',
            figure={
                'data': [
                    {'x': x,
                     'y': y, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Selected Country\'s Imports',
                    },
                    {'x': x2,
                    'y': y2, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Canada\'s Imports',
                    },
                ],
                'layout': {
                    'title': 'Energy Imports'
                }
            }
        ),
    ]

@app.callback(
    dash.dependencies.Output('graph6-container', 'children'),
    [dash.dependencies.Input('country_dropdown', 'value'),
    dash.dependencies.Input('measure_dropdown', 'value')]
    )

def update_graph6(input_country, input_measure):

    x = totals_exp[totals_exp['Country or Area']==input_country].sort_values(by='Year')['Year']
    y = totals_exp[totals_exp['Country or Area']==input_country].sort_values(by='Year')[input_measure]

    x2 = totals_exp[totals_exp['Country or Area']=='Canada'].sort_values(by='Year')['Year']
    y2 = totals_exp[totals_exp['Country or Area']=='Canada'].sort_values(by='Year')[input_measure]

    return [
        dcc.Graph(
            id='Energy Exports Trends',
            figure={
                'data': [
                    {'x': x,
                     'y': y, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Selected Country\'s Exports',
                    },
                    {'x': x2,
                    'y': y2, 
                    'type': 'scatter', 
                    'orientation':'v',
                    'name': 'Canada\'s Exports',
                    },
                ],
                'layout': {
                    'title': 'Energy Exports'
                }
            }
        ),
    ]
# LAUNCH APP
if __name__ == '__main__':
    app.run_server(debug=True)
