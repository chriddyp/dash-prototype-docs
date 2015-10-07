from dash import Dash
from dash.components import div, h1

from userguide import app

dash1 = Dash(server=app, url_namespace='')

dash1.layout = div([
    h1('welcome to the user guide')
])
