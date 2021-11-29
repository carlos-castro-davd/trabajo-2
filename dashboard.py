import numpy as np
from pandas.io.formats import style
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

level_count = pd.DataFrame(df_listings["room_type"].value_counts()).reset_index(
).rename(columns={"index": "room_type", "room_type": "count"})
level_count = level_count.sort_values("room_type").reset_index(drop=True)

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
    'margin-left': 80,
    'margin-right': 80
}
style_texto_2 = {
    'font-family': 'verdana',
    'size': 9
}
style_input = {
    'font-family': 'verdana',
    'margin-left': 80,
    'width': 390
}
dropdown_style = {
    'font-family': 'verdana',
    'padding-left': 80,
    'width': 500
}
dropdown_style_2 = {
    'font-family': 'verdana',
    'padding-left': 80,
    'width': 400
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
                    html.Br(),
                    html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),

                    # distribucion del precio
                    html.Div([
                        html.Br(),
                        html.P('Distribución del precio', style=style_texto),
                        dcc.Dropdown(
                            id='my-dropdown',
                            value=300,
                            style=dropdown_style,
                            options=[
                                {'label': 'Rango Completo', 'value': 10000},
                                {'label': 'Rango (0,300)', 'value': 300},
                                {'label': 'Rango (0,200)', 'value': 200},
                                {'label': 'Rango (0,100)', 'value': 100}
                            ],
                            searchable=False
                        ),
                        dcc.Graph(
                            id='my-graph'
                        ),
                    ]),

                    html.Br(),
                    html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),

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

                    html.Br(),
                    html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),

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
                    ),

                    html.Br(),
                    html.Br(),
                    html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),

                    html.Div(
                        children=[
                            dcc.Graph(
                                id='pie-chart',
                                figure=px.pie(
                                    level_count,
                                    values="count",
                                    names="room_type",
                                    color="room_type",
                                    color_discrete_map={
                                        "Private room": "lightblue",
                                        "Entire home/apt": "mediumseagreen",
                                        "Shared room": "gold",
                                        "Hotel room": "darkorange",
                                    }
                                )
                            )
                        ],
                        style={
                            'padding-left': '4%', 'width': '46%',
                            'display': 'inline-block'}
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='box-plot',
                                figure=go.Figure(
                                    data=[
                                        go.Box(
                                            y=df_listings[df_listings["neighbourhood_group"]
                                                          == "San Blas - Canillejas"]["price"],
                                            marker_color="steelblue",
                                            name="Precio",
                                            boxmean=True
                                        )
                                    ],
                                    layout=go.Layout(
                                        yaxis_title="Precio",
                                        xaxis_title="Saludos"
                                    )
                                )
                            )
                        ],
                        style={
                            'padding-left': '6%', 'width': '44%',
                            'display': 'inline-block'}
                    )
                ]),

        # Pestaña de resultados del modelo y app
        dcc.Tab(
            label='Modelo',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                dcc.Tabs(
                    vertical=True,
                    children=[
                        dcc.Tab(
                            label='Resultados',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            children=[
                                html.Br(),
                                html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),
                                html.Div(
                                    children=[

                                    ]
                                )
                            ]
                        ),
                        dcc.Tab(
                            label='App',
                            style=tab_style,
                            selected_style=tab_selected_style,
                            children=[
                                html.Br(),
                                html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),
                                html.Div(
                                    style={
                                        'width': '20%', 'display': 'inline-block'},
                                    children=[
                                        html.P("Superhost:",
                                               style=style_texto),
                                        dcc.Dropdown(
                                            id='app-input-superhost',
                                            value='No',
                                            style=dropdown_style_2,
                                            options=[
                                                {'label': 'Yes', 'value': 'Yes'},
                                                {'label': 'No', 'value': 'No'}
                                            ],
                                            searchable=False
                                        ),
                                        html.P('Neighbourhood:',
                                               style=style_texto),
                                        dcc.Dropdown(
                                            id='app-input-neighbourhood',
                                            style=dropdown_style_2,
                                            options=[
                                                {'label': 'Chamartín',
                                                    'value': 'Chamartín'},
                                                {'label': 'Latina',
                                                    'value': 'Latina'},
                                                {'label': 'Arganzuela',
                                                    'value': 'Arganzuela'},
                                                {'label': 'Centro',
                                                    'value': 'Centro'},
                                                {'label': 'Salamanca',
                                                    'value': 'Salamanca'},
                                                {'label': 'Fuencarral - El Pardo',
                                                    'value': 'Fuencarral - El Pardo'},
                                                {'label': 'Puente de Vallecas',
                                                    'value': 'Puente de Vallecas'},
                                                {'label': 'Ciudad Lineal',
                                                    'value': 'Ciudad Lineal'},
                                                {'label': 'Chamberí',
                                                    'value': 'Chamberí'},
                                                {'label': 'Villaverde',
                                                    'value': 'Villaverde'},
                                                {'label': 'Hortaleza',
                                                    'value': 'Hortaleza'},
                                                {'label': 'Moncloa - Aravaca',
                                                    'value': 'Moncloa - Aravaca'},
                                                {'label': 'Carabanchel',
                                                    'value': 'Carabanchel'},
                                                {'label': 'Tetuán',
                                                    'value': 'Tetuán'},
                                                {'label': 'Retiro',
                                                    'value': 'Retiro'},
                                                {'label': 'San Blas - Canillejas',
                                                    'value': 'San Blas - Canillejas'},
                                                {'label': 'Villa de Vallecas',
                                                    'value': 'Villa de Vallecas'},
                                                {'label': 'Barajas',
                                                    'value': 'Barajas'},
                                                {'label': 'Usera',
                                                    'value': 'Usera'},
                                                {'label': 'Moratalaz',
                                                    'value': 'Moratalaz'},
                                                {'label': 'Vicálvaro',
                                                    'value': 'Vicálvaro'}
                                            ],
                                            searchable=True
                                        ),
                                        html.P("Longitude:",
                                               style=style_texto),
                                        dcc.Input(
                                            id='app-input-longitude',
                                            placeholder='Enter a value...',
                                            type='text',
                                            value='',
                                            style=style_input
                                        ),
                                        html.P("Latitude:", style=style_texto),
                                        dcc.Input(
                                            id='app-input-latitude',
                                            placeholder='Enter a value...',
                                            type='text',
                                            value='',
                                            style=style_input
                                        )
                                    ]
                                ),
                                html.Div(
                                    style={
                                        'width': '20%', 'display': 'inline-block'},
                                    children=[
                                        html.P("Room Type:",
                                               style=style_texto),
                                        dcc.Dropdown(
                                            id='app-input-room-type',
                                            value='',
                                            style=dropdown_style_2,
                                            options=[
                                                {'label': 'Entire home/apt',
                                                    'value': 'Entire home/apt'},
                                                {'label': 'Private room',
                                                    'value': 'Private room'},
                                                {'label': 'Shared room',
                                                    'value': 'Shared room'},
                                                {'label': 'Hotel room',
                                                    'value': 'Hotel room'}
                                            ],
                                            searchable=False
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                )
            ]
        )
    ])
])

# -----------------------------------------------------------------------------------------
# Callback


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropdown', component_property='value')
)
def update_graph(v):

    data_x = df_listings['price'][df_listings['price'] <= v]

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
