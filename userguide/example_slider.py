from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='/{}'.format(const['slider-example']))

dash.layout = div([
    div(id="app"),
    hr(),
    Highlight(id="code", className="python")
], className="container")

app_template = '''from dash import Dash
from dash.components import Dropdown, div, pre
{}

dash = Dash(__name__)
dash.layout = {}

{}

if __name__ == "__main__":
    dash.server.run(debug=True)
'''

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
                'height': '650px',
                'margin': {'b': 10, 'l': 10}
            }
        }
    }
'''

dash.layout['code'].content = app_template.format(
    preample_3,
    layout_3,
    callbacks_3)
exec(preample_3)
exec("dash.layout['app'].content = [{}]".format(layout_3))
exec(callbacks_3)
