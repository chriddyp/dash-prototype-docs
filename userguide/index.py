import requests

from dash import Dash
from dash.components import *

from userguide import app

dash = Dash(server=app, url_namespace='')

dash.layout = div([
    h1('dash'),

    blockquote('''
        dash is a framework for creating interactive web-applications
        in pure python.'''),

    h3('quickstart'),

    pre('\n'.join([
        '$ pip install dash.ly --upgrade',
        '$ git clone -b skeleton https://github.com/chriddyp/messin.git',
        '$ cd messin',
        '$ pip install -r requirements.txt',
        '$ cd messin/helloworld',
        '$ python helloworld.py',
        ' * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)'])),

    hr(),

    div(className="row", content=[
        div(className='six columns', content=[
            b('helloworld.py'),
            pre(
                id="helloworld",
                # TODO: cache
                content=requests.get(
                    'https://raw.githubusercontent.com/chriddyp/messin/'
                    'skeleton/helloworld/helloworld.py').content)
        ]),

        div(className='six columns', content=[
            div([
                iframe(
                    src="http://127.0.0.1:8080/",
                    width='100%',
                    height='100%',
                    style={'border': 'none'})
            ], style={
                'padding-left': '20px',
                'border-left': 'thin lightgrey solid'
            })
        ])

    ]),

    h5('tutorials'),
    ol([
        li([a(link[0], href="/{}".format(link[1]))]) for link in [
            ('part 1 - creating html with dash', 'hello-world')]
    ])

], className='container')
