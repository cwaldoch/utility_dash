# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:59:38 2019

@author: .3
"""

import pdb
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_excel(r'https://www.eia.gov/electricity/data/eia860m/xls/august_generator2019.xlsx',
                   sheet_name='Operating',header=1)

def df_wavg(df, weights, values):
    return (df[values]*df[weights]).sum()/df[weights].sum()


#
app = dash.Dash(__name__)

#df = df[df['Sector'] == 'Electric Utility']
keepCols = ['Entity Name', 'Plant Name', 'Nameplate Capacity (MW)',
            'Technology', 'Energy Source Code', 'Prime Mover Code',
            'Operating Month', 'Operating Year', 'Plant State']

emDict = {'WAT':0, 'NG':0.059, 'BIT':0.1, 'DFO':0.08, 'NUC':0, 'LIG':0.1,
          'SUB':0.1, 'RC':0.1, 'WND':0, 'SUN':0,
           'GEO':0, 'LFG':0.059, 'MWH':0, 'WDS':0.07, 'RFO':0.08, 'JF':0.08,
           'SGC':0.1, 'KER':0.08, 'PC':0.08, 'MSW':0.07,
           'WO':0.08, 'PG':0.08, 'SGP':0.08, 'OBL':0.08, 'OTH':0.06,
           'WH':0, 'OBG':0.059, 'OG':0.059, 'WC':0.1, 'BLQ':0.08, 'BFG':0.059,
           'PUR':0, 'WDL':0.08, 'AB':0.08, 'TDF':0.1, 'OBS':0.08}

fuels = emDict.keys()

dfKeep = df[keepCols]
dfKeep = dfKeep[dfKeep['Energy Source Code'].notnull()]

dfKeep['Age'] = 2019 - dfKeep['Operating Year']

dfKeep['emmR'] = [emDict[x] for x in dfKeep['Energy Source Code'].values]
dfKeep['emmF'] = dfKeep['emmR'] * dfKeep['Nameplate Capacity (MW)']
utilities = dfKeep['Entity Name'].unique()
results = []
for utility in utilities:
    
    #uFuelDict = {}
    dfU = dfKeep[dfKeep['Entity Name'] == utility]
    
    utilityMW = np.sum(dfU['Nameplate Capacity (MW)'])
    utilityAge = df_wavg(dfU, 'Nameplate Capacity (MW)', 'Age')
    utilityEm = df_wavg(dfU, 'Nameplate Capacity (MW)', 'emmR')
    
    for fuel in fuels:
        dfUF = dfU[dfU['Energy Source Code'] == fuel]
        if len(dfUF) > 0:
            fuelMW = np.sum(dfUF['Nameplate Capacity (MW)'])
            fuelAge = df_wavg(dfUF, 'Nameplate Capacity (MW)', 'Age')
        else:
            fuelMW = 0
            fuelAge = 0
            
            
        results.append([utility, utilityAge, utilityEm, fuel, fuelMW, fuelAge])
        
dfResults = pd.DataFrame(results, columns = ['Utility', 'MW-Age', 'Utility-Em',
                                         'Fuel', 'Fuel-MW', 'Fuel-Age'])
    
dfResults.to_csv('utility_fuels.csv', index=False)

uResults = []
for utility in utilities:
    dfRU = dfResults[dfResults['Utility'] == utility]
    
    totalMW = dfRU['Fuel-MW'].sum()
    ageCap = dfRU['MW-Age'].mean()
    emFU = dfRU['Utility-Em'].mean()
    
    uResults.append([utility, totalMW, ageCap, emFU])
    

dfUResults = pd.DataFrame(uResults, columns = ['Utility', 'Total MW', 'Weighted Age',
                                               'Utility-Em'])
    
dfUResults.to_csv('utility_stats.csv', index=False)
#available_indicators = 