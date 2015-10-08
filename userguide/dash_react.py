from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='/{}'.format(const['dash.react']))

dash.layout = div([
    h2('making dash apps interactive'),
    h4('binding python callbacks to user inputs'),

    div([
        p([
            'Some ', code('dash.components'),
            ' objects respond to user input. ',
            'Dash provides a callback API to bind custom interactivity to ',
            'these changes in user input. '
            'This is exposed as a function decorator: ',
            code('dash.react(id_of_component_to_update, list_of_component_ids_to_respond_to)'),
            '. ',
            p(["Let's look at a simple example. ",
               'When you update the user dropdown, the ',
                code('<pre id="display-dropdown-value"></pre>'),
                ' on the page updates with the value of the selected item.'])
        ]),
        hr()
    ]),
    div([
        div([
            pre(id='layout-1', style={'overflowY': 'scroll'})
        ], className="eight columns",
            style={'borderRight': 'thin lightgrey solid'}),
        div([
            div(id='layout-1-rendered')
        ], className="four columns")
    ], className="row"),


    div([
        hr(),
        p([
            'The decorated function (in this case',
            code('display_dropdown_value'),
            ' must return a ', code('dict'),
            ' with ', i('any'),
            ' of the ', code('component_to_update'), ' attributes. ',
            "In this case, we're just updating the ", code('content'),
            "of the ", code('<pre>'), '.',
            p(["Let's look at another example, where one dropdown ",
               "updates the options of the second dropdown by returning new ",
               code('options'), '.'])
        ])
    ], className="row"),
    hr(),
    div(id='layout-2-rendered'), hr(),
    div([
        div([
            pre(id='layout-2', style={'overflowY': 'scroll'})
        ], className="twelve columns")
    ], className="row"),

    hr(),

    div([
        p("Let's look at another example, with a slider and a graph.")
    ], className="row"),
    hr(),
    div(id='layout-3-rendered'), hr(),
    div([
        div([
            pre(id='layout-3', style={'overflowY': 'scroll'})
        ], className="twelve columns")
    ], className="row"),

], className="container")

app_template = '''from dash import Dash
from dash.components import Dropdown, div, pre
dash = Dash(__name__)
{}
dash.layout = {}

{}

if __name__ == "__main__":
    dash.server.run(debug=True)
'''

layout_1 = '''div([
    Dropdown(
        options=[
            {'label': 'Oranges', 'val': 'oranges'},
            {'label': 'Apples', 'val': 'apples'},
            {'label': 'Mangoes', 'val': 'mangoes'},
        ], id='fruit-dropdown'),
    pre(id='display-dropdown-value')
])'''

callbacks_1 = '''
@dash.react('display-dropdown-value', ['fruit-dropdown'])
def display_dropdown_value(fruit_dropdown):
    return {
        'content': 'value: ' + fruit_dropdown.selected
    }
'''

dash.layout['layout-1'].content = app_template.format(
    '',
    layout_1,
    callbacks_1)
exec("dash.layout['layout-1-rendered'].content = [{}]".format(layout_1))
exec(callbacks_1)


preample_2 = '''
primary_options = [
    {'label': 'Fruits', 'val': 'fruits'},
    {'label': 'Vegetables', 'val': 'vegetables'}
]

secondary_options = {
    'fruits': [
        {'label': 'Oranges', 'val': 'oranges'},
        {'label': 'Apples', 'val': 'apples'},
        {'label': 'Mangoes', 'val': 'mangoes'}
    ],
    'vegetables': [
        {'label': 'Rutabagas', 'val': 'rutabaga'},
        {'label': 'Asparagus', 'val': 'asparagus'}
    ]
}
'''
layout_2 = '''div([
    Dropdown(options=primary_options, id='primary-dropdown'),
    Dropdown(options=secondary_options['fruits'], id='secondary-dropdown'),
    pre(id='display-dropdown-values')
])'''
callbacks_2 = '''
@dash.react('secondary-dropdown', ['primary-dropdown'])
def update_secondary_dropdown(primary_dropdown):
    """ When the "primary-dropdown" changes, this function is called.
    Update the "options" and the "selected" value of the secondary dropdown.
    """
    return {
        'options': secondary_options[primary_dropdown.selected],
        'selected': secondary_options[primary_dropdown.selected][0]['val']
    }


@dash.react('display-dropdown-values', ['primary-dropdown', 'secondary-dropdown'])
def display_dropdown_value(primary_dropdown, secondary_dropdown):
    """ When *either* the "primary-dropdown" or the "secondary-dropdown"
    changes, this function is called. Then, update the "content" of the
    <pre id="display-dropdown-values"></pre> with the selected value of
    the dropdowns.
    """
    return {
        'content': '\\n'.join([
            'primary dropdown selected: ' + primary_dropdown.selected,
            'secondary dropdown selected: ' + secondary_dropdown.selected
        ])
    }
'''
dash.layout['layout-2'].content = app_template.format(
    preample_2,
    layout_2,
    callbacks_2)
exec(preample_2)
exec("dash.layout['layout-2-rendered'].content = [{}]".format(layout_2))
exec(callbacks_2)

preample_3 = '''from dash.components import Slider
import numpy as np
'''
layout_3 = '''div([
    h5('3d sine wave'),
    Slider(label='Frequency', min=0, max=3, value=1, step=0.05, id="frequency-slider"),
    PlotlyGraph(id="3d-sine-wave")
])'''
callbacks_3 = '''
x = y = np.arange(-5, 5, 0.1)
yt = x[:, np.newaxis]
@dash.react('3d-sine-wave', ['frequency-slider'])
def update_graph(slider):
    frequency = slider.value
    return {
        'figure': {
            'data': [{
                'z': np.cos(x*yt*(frequency+1)/100)+np.sin(x*yt*(frequency+1/100)),
                'type': 'surface'
            }],
            'layout': {
                'title': 'waaaves',
                'height': '600px',
                'margin': {'b': 10, 'l': 10}
            }
        }
    }
'''
dash.layout['layout-3'].content = app_template.format(
    preample_3,
    layout_3,
    callbacks_3)
exec(preample_3)
exec("dash.layout['layout-3-rendered'].content = [{}]".format(layout_3))
exec(callbacks_3)
