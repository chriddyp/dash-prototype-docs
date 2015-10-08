from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='/' + const['layout'])

complaint_text = "Each week thousands of consumers' complaints about financial products are sent to companies for response."

import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/chriddyp/'
                 'messin/master/examples/consumer_complaints_50k.csv',
                 index_col='Date sent to company', parse_dates=True)
most_common_complaints = df['Company'].value_counts()

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
    h2("designing the layout of your app"),
    h4("how dash abstracts HTML"),

    b('quickstart'),

    Highlight('\n'.join([
        'from dash import Dash',
        'from dash.components import div, h5',
        '',
        'dash = Dash(__name__)',
        '',
        'dash.layout=div([h5("hello world")])',
        '',
        'if __name__ == "__main__":',
        '    dash.server.run(debug=True)'
    ]), className="python",),

    hr(),

    div([
        p(['''The first part of a Dash app is the ''',
        code('dash.layout'),
        ''', and this is assignment describes what the page will look like.
        The layout is rendered as HTML and each HTML element
        has an associated class in ''', code('dash.components'),
            '''with a matching name.''']),
    ], className='row'),

    div([
        div([
            b('dash code in python'),
            Highlight('\n'.join([
                'dash.layout = div([',
                '   h5("consumer complaints"),',
                '   div("Each week thousands of consumers\' complaints "',
                '       "about financial products are "',
                '       "sent to companies for response.")'
                '])'
            ]), style={'overflowY': 'scroll'}, className="python"),


        ], className='six columns'),

        div([
            b('HTML code that is generated'),
            Highlight(['\n'.join([
                '<div>',
                '   <h5>consumer complaints</h5>',
                '   <div>{}</div>'.format(complaint_text),
                '</div>'])
            ], style={"whiteSpace": "pre-wrap"}, className="html")
        ], className='six columns')
    ], className='row'),

    div([
        hr(),
        p(['HTML attributes, like ', code('style'), ', ', code('id'), ', and ',
            a('many more',
              href="https://facebook.github.io/react/docs/"
                   "tags-and-attributes.html#html-attributes"),
            ', are specified as keyword arguments in the ',
            code('dash.components'),
            ' classes and translated to HTML.'])
    ], className='row'),

    div([
        div([
            b('dash code in python'),
            Highlight('\n'.join([
                'dash.layout = div([',
                '   h5("consumer complaints"),',
                '   div("Each week thousands of consumers\' complaints "',
                '       "about financial products are "',
                '       "sent to companies for response.", ',
                '       style={{"borderLeft": "lightgrey solid"}})',
                '], id="container", className="python")'
            ]))
        ], className='six columns'),

        div([
            b('HTML code that is generated'),
            Highlight(['\n'.join([
                '<div id="container">',
                '   <h5>consumer complaints</h5>',
                '   <div style="border-left: lightgrey solid;">',
                '   {}'.format(complaint_text),
                '   </div>',
                '</div>'])
            ], style={"whiteSpace": "pre-wrap"}, className="html")
        ], className='six columns'),
    ], className='row'),

    div([
        hr(),
        p(['The translation from Python from ', code('dash.components'),
            'classes to HTML is 1-1 with two exceptions: ']),
        ul([
            li(['Use the keyword argument ', code('className'), 'instead of ',
                code('class'),
                'to specify HTML\'s ', code('class'),
                ' attribute. For example',
                Highlight('div("my div", className="tiny") # rendered as: <div class="tiny">my div</div>', className="python")]),
            li([
                'Specify HTML\'s inline ', code('style'), ' with a ',
                code('dict'), '. ', 'CSS style attributes, like ',
                code('color'), code('border-left'), code('font-size'),
                ', are specified with their hyphen\'s removed and camelCased. '
                'For example, ',
                Highlight('div("my div", style={"color": "blue", '
                    '"borderLeft": "thin grey solid", "fontSize": 12})', className="python"),
                p(' is translated to HTML as: '),
                Highlight('<div style="color: blue; border-left: thin grey solid; '
                    'font-size: 12px">my div</div>', className="html")
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
            Highlight(repr(component), className="python"),
            component,
            hr()
        ]) for component in component_list
    ]),

    div([
        p(['The first named argument of every component is ', code('content'),
           ' and this describes the content of the HTML element. The ', code('content'),
           ' can be a string, another element, or a list of elements and/or strings.']),

        Highlight('''div('my text')      # rendered as: <div>my text</div>
div(p('my text'))   # TODO: does this actually work? rendered as: <div><p>my text<p></div>
div(['my text'])    # rendered as: <div>my text</div>
div([h1('my title'), h4('subtitle')])               # rendered as: <div><h1>my title</h1><h4>subtitle</h4></h1></div>
div([h1('my title'), h4('subtitle'), 'body text'])  # rendered as <div><h1>my title</h1><h4>subtitle</h4></h1>body text</div>
''', className="python"),

        p(['Like the rest of the attributes, ', code('content'), ' is a named argument. Since it is the first named argument',
            ' it is often specified implicitly without a name. These call signatures are all equivalent: ']),

        Highlight('''div('my text', className='row')         # rendered as: <div class="row">my text</div>
div(content='my text', className='row') # rendered as: <div class="row">my text</div>
div(className='row', content='my text') # rendered as: <div class="row">my text</div>''',
className="python")
    ]),

    hr(),

    h5('example'),


    div([Highlight("""
from dash import Dash
from dash.components import div, h2, blockquote

dash = Dash(__name__)

import pandas as pd
df = pd.read_csv('/Users/chriddyp/Repos/reactworld'
                 '/examples/consumer_complaints_50k.csv',
                 index_col='Date sent to company', parse_dates=True)
most_common_complaints = df['Company'].value_counts()

dash.layout = {sample_app_string}

if __name__ == "__main__":
    dash.server.run(port=5000, debug=True)
""", id='sample-app-pre', className="python")], className='row'),

    div([
        'To run this app: ',
        pre('\n'.join([
            '$ pip install dash.ly --upgrade',
            '$ git clone -b skeleton https://github.com/chriddyp/messin.git',
            '$ cd messin',
            '$ pip install -r requirements.txt',
            '$ cd helloworld'
        ]), className="bash"),
        'then save this file as e.g.', code('myapp.py'), ' and run ',
        pre('\n'.join([
            '$ python myapp.py',
            ' * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)']), className="bash")
    ]),
    div([
        p('Visit http://127.0.0.1:5000/ in your browser '
          'and you should see something like: '),
        hr(),
        div(id='sample-app')], className='row')

], className='container')


sample_app_string = """div([
    h2('Consumer Complaints'),

    blockquote([
        ('''
         Each week we send thousands of consumers' complaints about
         financial products and services to companies for response.
         Complaints are listed in the database after the company responds
         or after they\'ve had the complaint for 15 calendar days,
         whichever comes first.
         '''),
        br(),
        ('''
         We publish the consumer\'s description of what happened if the
         consumer opts to share it and after taking steps to remove
         personal information. See our '''),
        a('Scrubbing Standard',
          href="http://files.consumerfinance.gov/a/assets/"
               "201503_cfpb_Narrative-Scrubbing-Standard.pdf",
          target="_blank"),
        (''' for more details.
         We don\'t verify all the facts alleged in these complaints,
         but we take steps to confirm a commercial relationship.
         We may remove complaints if they don\'t meet all of the
         publication criteria. Data is refreshed nightly.'''),
        br(),
        a('More about the Consumer Complaint Database',
          href="http://www.consumerfinance.gov/complaintdatabase/",
          target="_blank")
    ], style={'borderLeft': 'thick lightgrey solid',
              'paddingLeft': '20px', 'fontStyle': 'italic'}),

    hr(),

    div(className='row', content=[h5('Complaints by Company')]),

    div(className='row', content=[
        div(className='twelve columns', content=[
            PlotlyGraph(
                id='company-complaint-graph',
                figure={
                    'data': [{
                        'x': most_common_complaints.index,
                        'y': most_common_complaints,
                        'type': 'bar'
                    }],
                    'layout': {
                        'yaxis': {
                            'type': 'log',
                        },
                        'xaxis': {
                            'range': [-1, 50],
                            'tickangle': 40
                        },
                        'margin': {'t': 5, 'r': 0, 'l': 40, 'b': 200}
                    }
                }
            )
        ])
    ])
])"""

exec("dash.layout['sample-app'].content = [" + sample_app_string + "]")
dash.layout['sample-app-pre'].content = \
    dash.layout['sample-app-pre'].content.format(
        sample_app_string=sample_app_string)
