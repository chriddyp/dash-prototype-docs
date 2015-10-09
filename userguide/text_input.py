from dash import Dash
from dash.components import *

from userguide import app, const

dash = Dash(server=app, url_namespace='/{}'.format(const['text-input']))

dash.layout = div([
    div(id="app"),
    hr(),
    Highlight(id="code", className="python")
], className="container")

app_template = '''from dash import Dash
from dash.components import *
{}

dash = Dash(__name__)
dash.layout = {}

{}

if __name__ == "__main__":
    dash.server.run(debug=True)
'''

preamble = '''import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import traceback

# list of tickers
df_companies = pd.read_csv('https://raw.githubusercontent.com/'
                           'plotly/dash/master/companylist.csv')
tickers = [s.lower() for s in list(df_companies['Symbol'])]

# convenience function for creating tables
def gen_table(rows, header=[]):
    tbl = table([
        thead([
            tr([
                th(str(h)) for h in header
            ])
        ]),
        tbody([
            tr([
                td(str(cell)) for cell in row
            ]) for row in rows
        ])
    ])
    return tbl'''

layout = '''div([
    h5('yahoo finance explorer'),
    div([
        div([
            TextInput(
                id='stock-ticker-input', value='',
                label='ticker', placeholder='COKE',
                className='u-full-width'),
            table(id='ticker-table')
        ], className="four columns"),
        div([
            PlotlyGraph(id='graph')
        ], className="eight columns")
    ], className="row")
])'''

callbacks = '''
@dash.react('graph', ['stock-ticker-input'])
def update_graph(stock_ticker_input):
    """ This function is called whenever the input
    'stock-ticker-input' changes.
    Query yahoo finance with the ticker input and update the graph
    'graph' with the result.
    """
    ticker = stock_ticker_input.value.lower()
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2014, 1, 1),
                        dt.datetime(2015, 4, 15))
    return {
        'figure': {
            'data': [{
                'x': df.index,
                'y': df['Close']
            }],
            'layout': {
                'title': ticker,
                'yaxis': {'title': 'Close'},
                'margin': {'b': 50, 'r': 10, 'l': 60}
            }
        }
    }

@dash.react('ticker-table', ['stock-ticker-input'])
def filter_tickers(stock_ticker_input):
    """ This function is called whenever the input
    'stock-ticker-input' changes.
    Search the available tickers and update the table
    'ticker-table' with the results.
    """
    ticker = stock_ticker_input.value.lower()
    filtered_df = df_companies[
        df_companies.Name.str.contains(ticker, case=False) |
        df_companies.Symbol.str.contains(ticker, case=False)]
    rows = zip(list(filtered_df.Name), list(filtered_df.Symbol))
    if len(rows) > 7:
        # only show 7 rows. provide an indication that there
        # are more rows by setting the last row to '...'
        rows = rows[:6] + [('...', '')]
    return {
        'content': gen_table(
            rows, header=['name', 'ticker']).content
    }
'''

dash.layout['code'].content = app_template.format(
    preamble,
    layout,
    callbacks)
exec(preamble)
exec("dash.layout['app'].content = [{}]".format(layout))
exec(callbacks)
