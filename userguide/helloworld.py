from dash import Dash
from dash.components import div, h1

from userguide import app

dash2 = Dash(server=app, url_namespace='/chapter-1')

dash2.layout = div([
    h1('chapter 1')
])
