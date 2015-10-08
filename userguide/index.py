import requests

from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='')

dash.layout = div([
    h1('dash'),

    blockquote('''
        dash is a framework for creating interactive web-applications
        in pure python.'''),

    h3('quickstart'),

    Highlight('\n'.join([
        '$ pip install dash.ly --upgrade',
        '$ git clone -b skeleton https://github.com/chriddyp/messin.git',
        '$ cd messin',
        '$ pip install -r requirements.txt',
        '$ cd helloworld',
        '$ python helloworld.py',
        ' * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)']),
        className="bash"),

    hr(),

    div(className="row", content=[
        div(className='six columns', content=[
            b('helloworld.py'),
            Highlight(
                id="helloworld",
                className="python",
                # TODO: cache
                content=requests.get(
                    'https://raw.githubusercontent.com/chriddyp/messin/'
                    'skeleton/helloworld/helloworld.py').content)
        ]),

        div(className='six columns', content=[
            div([
                iframe(
                    src="https://morning-dawn-5773.herokuapp.com/",
                    width='100%',
                    height='100%',
                    style={'border': 'none'})
            ], style={
                'padding-left': '20px',
                'border-left': 'thin lightgrey solid'
            })
        ])

    ]),

    hr(),

    h5('examples'),
    ul([
        li([a(link[0],
              target="_blank",
              href="/{}".format(link[1]))]) for link in [
            ('updating graphs with sliders', const['slider-example'])]
    ]),

    h5('user guide'),
    ol([
        li([a(link[0], href="/{}".format(link[1]))]) for link in [
            ('designing the layout of your app or, '
             'how dash abstracts HTML', const['layout']),

            ('making your apps interactive or, '
             'binding python callbacks to user inputs',
                const['dash.react'])]
    ])

], className="container", style={'width': '95%'})
