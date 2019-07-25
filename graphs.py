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
