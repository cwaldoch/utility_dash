# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:44:34 2019

@author: .3
"""

import dash, pdb, webbrowser
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

dfFuels = pd.read_csv('utility_fuels.csv')
dfStats = pd.read_csv('utility_stats.csv')
dfColors = pd.read_csv('fuel_colors.csv')

colorDict = dict(zip(dfColors['fuel'].values, dfColors['color'].values))

mwMax = dfStats['Total MW'].max()
mwMin = dfStats['Total MW'].min()

mwCeiling = mwMax
mwCeiling -= mwCeiling % -500

available_indicators = ['Total MW', 'Weighted Age', 'Utility-Em']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Total MW'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Weighted Age'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Alabama Power Co'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-mw-slider',
        min=mwMin,
        max=mwMax,
        value=dfStats['Total MW'].max(),
        marks={str(mwVal): str(mwVal) for mwVal in range(0, int(mwCeiling), 2000)},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 25px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-mw-slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 mw_value):
    dff = dfStats[dfStats['Total MW'] >= mw_value]
    
    return {
        'data': [dict(
            x=dff[xaxis_column_name],
            y=dff[yaxis_column_name],
            text=dff['Utility'],
            customdata=dff[yaxis_column_name],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title, colName):
    
    dff2 = dff[dff['Fuel-MW'] >0]
    outlineDict = {'color':'black', 'width':1.5}
    barColor = {'color':[colorDict[x] for x in dff2['Fuel'].values], 'line':outlineDict}
    return {
        'data': [{
            'x':dff2['Fuel'],
            'y':dff2[colName],
            'type':'bar','marker':barColor,
        }],
        'layout': {
            'height': 225,
            'margin': {'l': 40, 'b': 30, 'r': 10, 't': 20},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    utility_v = hoverData['points'][0]['text']    
    dff = dfFuels[dfFuels['Utility'] == utility_v]
    title = str(utility_v)+': Fuel-MW'
    return create_time_series(dff, axis_type, title, 'Fuel-MW')


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    utility_name = hoverData['points'][0]['text']
    dff = dfFuels[dfFuels['Utility'] == utility_name]
    title = utility_name+': Fuel-Age'
    return create_time_series(dff, axis_type, title, 'Fuel-Age')


webbrowser.open_new('http://127.0.0.1:9899/')
if __name__ == '__main__':
    app.run_server(port=9899)