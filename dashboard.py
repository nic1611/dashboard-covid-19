import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go 

import numpy as np
import pandas as pd
import json

# df = pd.read_csv('HIST_PAINEL_COVIDBR_2021_Parte1_29set2021.csv', sep=';')
# df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())]
# df_brasil = df[df['regiao'] == 'Brasil']

# df_states.to_csv('df_states.csv')
# df_brasil.to_csv('df_brasil.csv')

df_states = pd.read_csv('df_states.csv')
df_brasil = pd.read_csv('df_brasil.csv')

brazil_states = json.load(open('brazil_geo.json', 'r'))
df_data = df_states[df_states['estado']=='RJ']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(data_frame=df_states, locations="estado", 
                        geojson=brazil_states, center={"lat": -16.95, "lon": -47.78}, zoom=3, color="casosNovos", 
                        color_continuous_scale="Redor", opacity=0.4)

fig.update_layout(
    paper_bgcolor='#242424',
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10),
    showlegend=False,
    mapbox_style='carto-darkmatter'
)

fig2 = go.Figure(layout={'template':'plotly_dark'})
fig2.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig2.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-graph', figure=fig2)
        ]), 
        dbc.Col([
            dcc.Graph(id='choropleth-map', figure=fig)
        ])
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)
