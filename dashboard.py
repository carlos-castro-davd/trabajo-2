import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_daq as daq
from dash import html
from dash import dcc

import pandas as pd

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# --------------------------------------------------------------------
# Datos

# df_calendar = pd.read_csv("/Users/diegoma/kaggle/calendar.csv")
df_listings = pd.read_csv("/Users/diegoma/kaggle/listings.csv")
df_neighbourhoods = pd.read_csv("/Users/diegoma/kaggle/neighbourhoods.csv")
# df_reviews = pd.read_csv("/Users/diegoma/kaggle/reviews.csv")
# df_reviews_det = pd.read_csv("/Users/diegoma/kaggle/reviews_detailed.csv")
# df_listings_det = pd.read_csv("/Users/diegoma/kaggle/listings_detailed.csv")


# --------------------------------------------------------------------
# Dashboard Ini
app = dash.Dash(__name__)

# --------------------------------------------------------------------
# Tool variables
count_neigh = len(df_neighbourhoods["neighbourhood_group"].unique())
unique_neigh = df_neighbourhoods["neighbourhood_group"].unique()
neigh_count = {}

for i in range(count_neigh):
    neigh_count[unique_neigh[i]] = df_listings["neighbourhood_group"][df_listings["neighbourhood_group"]
                                                                      == unique_neigh[i]].count()

ordered_keys = []
ordered_values = []

for w in sorted(neigh_count, key=neigh_count.get):
    ordered_keys.append(w)
    ordered_values.append(neigh_count[w])

median_neigh = {}
for i in range(count_neigh):
    median_neigh[unique_neigh[i]] = round(
        df_listings[df_listings["neighbourhood_group"] == unique_neigh[i]]["price"].median(), 3)

# --------------------------------------------------------------------
# Style variables
tab_style = {
    'font-family': 'verdana'
}
tab_selected_style = {
    'font-family': 'verdana'
}
style_texto = {
    'font-family': 'verdana',
    'margin-left': 80
}
style_texto_2 = {
    'font-family': 'verdana',
    'size': 9
}
dropdown_style = {
    'font-family': 'verdana',
    'padding-left': 80,
    'width': 500
}
colorines = ["aliceblue", "antiquewhite", "aqua", "beige", "bisque", "black", "blueviolet", "cornsilk", "darkkhaki", "darkgrey", "darkgreen",
             "firebrick", "gainsboro", "ivory", "crimson", "darkslategray", "indigo", "mediumaquamarine", "olivedrab", "peachpuff", "mediumspringgreen"]

# --------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Dashboard Airbnb", style={
        'text-align': 'center',
        'font-family': 'verdana'
    }),
    html.H3("por Diego Martinez de Aspe Martín", style={
        'text-align': 'center',
        'font-family': 'verdana'
    }),
    html.H6("y la colaboracion de Jaime R.", style={
        'text-align': 'center',
        'font-family': 'verdana',
        'color': 'gray'
    }),

    html.Br(),

    dcc.Tabs([

        # Pestaña de Análisis Exploratorio
        dcc.Tab(label='Análisis Exploratorio', style=tab_style,
                selected_style=tab_selected_style, children=[

                    # Aquí empiezan los plots del exploratorio de datos:

                    # distribucion del precio
                    html.Div([
                        html.Br(),
                        html.P('Distribución del precio', style=style_texto),
                        dcc.Dropdown(
                            id='my-dropdown',
                            value='RC',
                            style=dropdown_style,
                            options=[
                                {'label': 'Rango Completo', 'value': 'RC'},
                                {'label': 'Rango (0,300)', 'value': 'R300'}
                            ],
                            searchable=False
                        ),
                        dcc.Graph(
                            id='my-graph'
                        ),
                    ]),

                    html.Div(
                        children=[
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Bar(
                                            x=ordered_values,
                                            y=ordered_keys,
                                            opacity=0.6,
                                            orientation='h',
                                            marker_color='firebrick')
                                    ],
                                    layout=go.Layout(
                                        xaxis_title='Número de publicaciones',
                                        yaxis_title='Barrio'
                                    )
                                ),
                                id='graph-2',
                                style={'height': 720}
                            ),
                        ],
                        style={'width': '50%',
                               'display': 'inline-block', 'height': 720}
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Bar(
                                            x=list(median_neigh.keys()),
                                            y=list(median_neigh.values()),
                                            opacity=0.6,
                                            name="Median price per neighbourhood",
                                            marker_color=colorines
                                        )
                                    ],
                                    layout=go.Layout(
                                        xaxis_title='Barrio',
                                        yaxis_title='Precio Medio por noche'
                                    ),
                                ),
                                style={'height': 720}
                            )
                        ],
                        style={'width': '50%', 'display': 'inline-block'}
                    ),

                    # mapa múltiple
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='my-map'
                            ),
                        ],
                        style={'width': '70%', 'display': 'inline-block'}
                    ),
                    # selector combinado del mapa múltiple
                    html.Div(
                        children=[
                            daq.ToggleSwitch(
                                id='toggle-switch-mapa',
                                value=False,
                                label={'label': 'Show offer density',
                                       'style': style_texto_2}
                            ),
                            html.Br(),
                            dcc.RangeSlider(
                                id='range-slider-precio',
                                min=0,
                                max=10000,
                                value=[0, 10000],
                                allowCross=False,
                                tooltip={"placement": "bottom",
                                         "always_visible": True}
                            )
                        ],
                        style={'padding-left': '4%', 'width': '62%',
                               'display': 'inline-block'}
                    )


                ]),

        # Pestaña de resultados del modelo y app
        dcc.Tab(label='Modelo', style=tab_style,
                selected_style=tab_selected_style, children=[])
    ])
])

# -----------------------------------------------------------------------------------------
# Callback


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropdown', component_property='value')
)
def update_graph(v):

    if(v == 'R300'):
        data_x = df_listings['price'][df_listings['price'] <= 300]
    else:
        data_x = df_listings['price']

    fig = go.Figure(
        data=[
            go.Histogram(
                x=data_x,
                opacity=0.6,
                name="Precio"
            )
        ],
        layout=go.Layout(
            xaxis_title="Precio",
            yaxis_title="Frecuencia",
            barmode="overlay"
        )
    )

    return fig


@app.callback(
    Output(component_id='my-map', component_property='figure'),
    Input(component_id='toggle-switch-mapa', component_property='value'),
    State(component_id='range-slider-precio', component_property='value')
)
def update_map(toogle, range):

    # nos quedamos con el dataframe que queremos
    valor_ini = range[0]
    print(valor_ini)
    valor_fin = range[1]
    print(valor_fin)
    df_tool = df_listings[df_listings['price'].between(valor_ini, valor_fin)]

    if(toogle == False):
        fig = px.density_mapbox(
            data_frame=df_tool,
            lat=df_tool['latitude'],
            lon=df_tool['longitude'],
            z=df_tool['price'],
            radius=15,
            center=dict(lat=40.43, lon=-3.68),
            zoom=11.5,
            mapbox_style="carto-positron",
            labels={"price": "Price", "latitude": "Latitude",
                    "longitude": "Longitude", "neighbourhood": "Neighbourhood"},
            hover_data=["price", "latitude", "longitude",
                        df_tool['neighbourhood']],
            height=800
        )
    elif(toogle == True):
        fig = go.Figure()
        fig = px.scatter_mapbox(
            data_frame=df_tool,
            lat=df_tool['latitude'],
            lon=df_tool['longitude'],
            mapbox_style='carto-positron',
            color=df_tool['neighbourhood_group'],
            center=dict(lat=40.43, lon=-3.68),
            zoom=11.5,
            height=800
        )

    return fig


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
