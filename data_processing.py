# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:59:38 2019

@author: .3
"""

import pdb
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_excel(r'https://www.eia.gov/electricity/data/eia860m/xls/august_generator2019.xlsx',
                   sheet_name='Operating',header=1)
#
app = dash.Dash(__name__)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = df[df['Sector'] == 'Electric Utility']
keepCols = ['Entity Name', 'Plant Name', 'Nameplate Capacity (MW)',
            'Technology', 'Energy Source Code', 'Prime Mover Code',
            'Operating Month', 'Operating Year', 'Plant State']

emDict = {'WAT':0, 'NG':0.059, 'BIT':0.1, 'DFO':0.08, 'NUC':0, 'LIG':0.1,
          'SUB':0.1, 'RC':0.1, 'WND':0, 'SUN':0,
           'GEO':0, 'LFG':0.059, 'MWH':0, 'WDS':0.07, 'RFO':0.08, 'JF':0.08,
           'SGC':0.1, 'KER':0.08, 'PC':0.08, 'MSW':0.07,
           'WO':0.08, 'PG':0.08, 'SGP':0.08, 'OBL':0.08, 'OTH':0.06,
           'WH':0, 'OBG':0.059, 'OG':0.059}

dfKeep = df[df[keepCols]]
dfKeep['Age'] = 2019 - dfKeep['Operating Year']

dfKeep['emmF'] = [emDict[x] for x in dfKeep['Energy Source Code'].values]
utilities = dfKeep['Entity Name'].unique()
for utility in utilities:
    dfU = dfKeep[dfKeep['Entity Name'] == utility]
    

#available_indicators = 