from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='/{}'.format(const['click-and-hover']))

dash.layout = div([
    div(id="app"),
    hr(),
    Highlight(id="code", className="python")
], style={'width': '90%'}, className="container")

app_template = '''from dash import Dash
from dash.components import Dropdown, div, pre
{}

dash = Dash(__name__)
dash.layout = {}

{}

if __name__ == "__main__":
    dash.server.run(debug=True)
'''

preamble = '''import plotly.plotly as py
from copy import deepcopy
import json

# Download the contour plot from https://plot.ly
fig = py.get_figure("https://plot.ly/~chris/5496")
margin = {'l': 20, 'r': 20, 'b': 20, 't': 20}
fig['layout'].update({'margin': margin})

figmain = deepcopy(fig)
figmain['layout'].update({'width': 500, 'height': 500})
figmain['data'][0]['showscale'] = False

figx = {'data': [], 'layout': {'width': 200, 'height': 500}}
figy = {'data': [], 'layout': {'width': 500, 'height': 200}}
'''

layout = '''div([
    h5('click events'),
    p('click on a heatmap cell to view an x, y slice through your cursor'),
    div([
        PlotlyGraph(
            id='yslice',
            width=figy['layout']['width'], height=figy['layout']['height'],
            figure=figy),
        div([
            PlotlyGraph(
                id='heatmap', bindClick=True,
                width=figmain['layout']['width'], height=figmain['layout']['height'],
                figure=figmain),
        ], style={"display": "inline-block"}),
        div([
            PlotlyGraph(
                id='xslice',
                width=figx['layout']['width'], height=figx['layout']['height'],
                figure=figx),
        ], style={"display": "inline-block"})
    ], className="row"),

    div([
        b('click callback'),
        pre(id="event-info", style={"overflowY": "scroll"})
    ])
])'''

callbacks = '''
@dash.react('event-info', ['heatmap'])
def display_graph_event_info(heatmap):
    """Display the click object in the <pre id="event-info">.
    This function gets called when the user hovers over or clicks on
    points in the heatmap. To assign click events to graphs, set
    bindClick=True in the PlotlyGraph component.
    """
    click = ''
    if hasattr(heatmap, 'click'):
        click = json.dumps(heatmap.click, indent=4)

    return {
        'content': repr(heatmap)+'\\nclick: '+click
    }

@dash.react('yslice', ['heatmap'])
def plot_yslice(heatmap_graph):
    """ Update the "yslice" graph with the slice of data that the user has
    clicked on.
    This function gets called on click events fired from the
    "heatmap" graph.
    """
    event_data = getattr(heatmap_graph, 'click')
    point = event_data['points'][0]['pointNumber']
    rowNumber = point[1]
    trace = heatmap_graph.figure['data'][0]
    row = trace['z'][rowNumber]
    x = trace.get('y', range(len(trace['z'][0])))
    return {
        'figure': {
            'data': [{
                'x': x,
                'y': row
            }],
            'layout': {
                'margin': margin
            }
        }
    }

@dash.react('xslice', ['heatmap'])
def plot_xslice(heatmap_graph):
    """ Update the "xslice" graph with the slice of data that the user has
    clicked on.
    This function gets called on click events fired from the
    "heatmap" graph.
    """
    event_data = getattr(heatmap_graph, 'click')
    point = event_data['points'][0]['pointNumber']
    colNumber = point[0]
    trace = heatmap_graph.figure['data'][0]
    column = [zi[colNumber] for zi in trace['z']]
    y = trace.get('y', range(len(trace['z'])))
    return {
        'figure': {
            'data': [{
                'x': column,
                'y': y
            }],
            'layout': {
                'margin': margin
            }
        }
     }
'''

dash.layout['code'].content = app_template.format(
    preamble,
    layout,
    callbacks)
exec(preamble)
exec("dash.layout['app'].content = [{}]".format(layout))
exec(callbacks)
