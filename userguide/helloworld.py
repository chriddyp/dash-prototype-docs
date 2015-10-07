from dash import Dash
from dash.components import *

from userguide import app

dash = Dash(server=app, url_namespace='/hello-world')

complaint_text = "Each week thousands of consumers' complaints about financial products are sent to companies for response."

component_list = [
    Dropdown(id='dropdown',
             options=[{'val': v, 'label': l} for (v, l) in [
                ('oranges', 'Oranges'),
                ('apples', 'Apples'),
                ('pineapple', 'Pineapple')]
             ]),

    TextInput(
        id='textinput',
        label='Name',
        placeholder='James Murphy'
    ),

    Slider(id='slider', min=-5, max=5, value=3, step=0.2, label='time'),

    PlotlyGraph(
        id='graph',
        figure={
            'data': [{'x': [1, 2, 3], 'y': [3, 1, 5]}],
            'layout': {'title': 'hobbs murphy experiment'}
        }
    )
]

dash.layout = div([
    h2("so what makes up a dash app?"),

    b('setup'),

    pre('\n'.join([
        'from dash import Dash',
        'dash = Dash(__name__)',
        'from dash.components import div, h5'
    ])),

    hr(),

    div([
        p(['''Dash apps are composed of two parts.
        The layout describes what the page will look like.
        The layout is rendered as HTML and each HTML element
        has an associated class in ''', code('dash.components'),
            '''with a matching name.''']),
    ], className='row'),

    div([
        div([
            b('dash code in python'),
            pre('\n'.join([
                'dash.layout = div([',
                '   h5("consumer complaints"),',
                '   div("Each week thousands of consumers\' complaints "',
                '       "about financial products are "',
                '       "sent to companies for response.")'
                '])'
            ]), style={'overflowY': 'scroll'}),


        ], className='six columns'),

        div([
            b('HTML code that is generated'),
            pre(['\n'.join([
                '<div>',
                '   <h5>consumer complaints</h5>',
                '   <div>{}</div>'.format(complaint_text),
                '</div>'])
            ], style={"whiteSpace": "pre-wrap"})
        ], className='six columns')
    ], className='row'),

    div([
        hr(),
        p(['HTML attributes, like ', code('style'), ', ', code('id'), ', and ',
            a('many more',
              href="https://facebook.github.io/react/docs/"
                   "tags-and-attributes.html#html-attributes"),
            ' are specified as keyword arguments in ', code('dash.components'),
            ' and translated to HTML.'])
    ], className='row'),

    div([
        div([
            b('dash code in python'),
            pre('\n'.join([
                'dash.layout = div([',
                '   h5("consumer complaints"),',
                '   div("Each week thousands of consumers\' complaints "',
                '       "about financial products are "',
                '       "sent to companies for response.", ',
                '       style={{"borderLeft": "lightgrey solid"}})',
                '], id="container")'
            ]))
        ], className='six columns'),

        div([
            b('HTML code that is generated'),
            pre(['\n'.join([
                '<div id="container">',
                '   <h5>consumer complaints</h5>',
                '   <div style="border-left: lightgrey solid;">',
                '   {}'.format(complaint_text),
                '   </div>',
                '</div>'])
            ], style={"whiteSpace": "pre-wrap"})
        ], className='six columns'),
    ], className='row'),

    div([
        hr(),
        p('The translation from Python to HTML is 1-1 with a two exceptions: '),
        ul([
            li(['Use the keyword argument ', code('className'), 'instead of ',
                code('class'),
                'to specify HTML\'s ', code('class'),
                ' attribute. For example',
                pre('div("my div", className="tiny") # rendered as: <div class="tiny">my div</div>')]),
            li([
                'Specify HTML\'s inline ', code('style'), ' with a ',
                code('dict'), '. ', 'CSS style attributes, like ',
                code('color'), code('border-left'), code('font-size'),
                ', are specified with their hyphen\'s removed and camelCased. '
                'For example, ',
                pre('div("my div", style={"color": "blue", '
                    '"borderLeft": "thin grey solid", "fontSize": 12})'),
                p(' is translated to HTML as: '),
                pre('<div style="color: blue; border-left: thin grey solid; '
                    'font-size: 12px">my div</div>')
            ])
        ])
    ], className='row'),

    div([
        div([
            hr(),
            p([code('dash.components'),
               ' also includes more complex, higher level components, like ',
               'controls and graphs.']),
        ], className='twelve columns')
    ], className='row'),

    div([
        div(className="row", content=[
            pre(repr(component)),
            component,
            hr()
        ]) for component in component_list
    ])

], className='container')
