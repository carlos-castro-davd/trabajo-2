import numpy as np
import pandas as pd
from pandas.io.formats import style
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_daq as daq
from dash import html
from dash import dcc
import joblib
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# --------------------------------------------------------------------
# Datos

#df_calendar = pd.read_csv("/Users/diegoma/kaggle/calendar.csv")
#df_listings = pd.read_csv("/Users/diegoma/kaggle/listings.csv")
#df_neighbourhoods = pd.read_csv("/Users/diegoma/kaggle/neighbourhoods.csv")
#df_reviews = pd.read_csv("/Users/diegoma/kaggle/reviews.csv")
#df_reviews_det = pd.read_csv("/Users/diegoma/kaggle/reviews_detailed.csv")
#df_listings_det = pd.read_csv("/Users/diegoma/kaggle/listings_detailed.csv")


# Jaime
df_listings = pd.read_csv(
    "/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/listings.csv")
df_neighbourhoods = pd.read_csv(
    "/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/neighbourhoods.csv")
df_modelo = pd.read_csv(
    "/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/DataFinal/datos_modelo.csv")

modelo = joblib.load(
    "/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/DataFinal/modelo_RF.pkl")

#modelo = joblib.load("/Users/diegoma/modelo_RF.pkl")
tokenizer = AutoTokenizer.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment")
model_nlp = AutoModelForSequenceClassification.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment")
multilang_classifier = pipeline(
    "sentiment-analysis", model=model_nlp, tokenizer=tokenizer)

# --------------------------------------------------------------------
# Dashboard Ini
app = dash.Dash(__name__)

# --------------------------------------------------------------------
# Tool variables
count_neigh = len(df_neighbourhoods["neighbourhood_group"].unique())
unique_neigh = df_neighbourhoods["neighbourhood_group"].unique()
neigh_count = {}

options_neigh = []
for i in unique_neigh:
    options_neigh.append({'value': i, 'label': i})

unique_room = df_listings["room_type"].unique()
options_room = []
for i in unique_room:
    options_room.append({'value': i, 'label': i})


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
    'font-family': 'verdana',
    'background-color': 'snow'
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
        'font-family': 'verdana',
        "border-style": "outset",
        'border-color': "lightgrey",
        "background-color": "lightgrey",
        "height": "60px"
    }),
    html.H3("por Diego Martinez de Aspe Martín y Jaime Reglero García", style={
        'text-align': 'center',
        'font-family': 'verdana'
    }),

    html.Br(),

    dcc.Tabs([

        # Pestaña de Análisis Exploratorio
        dcc.Tab(label='Análisis Exploratorio', style=tab_style,
                selected_style=tab_selected_style, children=[

                    # Aquí empiezan los plots del exploratorio de datos:
                    html.Br(),
                    html.P("A lo largo de este dashboard se tratarán de desarrollar los principales factores de influencia del precio en publicaciones de Airbnb, con el objetivo de poder realizar una predicción razonable. El análisis viene de un conjunto de datos de considerable extensión y numerosas variables, desde los comentarios en la publicación hasta el número de habitaciones. Se comenzarán analizando las variables que se han considerado de mayor importancia o interés, para posteriormente proceder a la elaboración del modelo, en la cual el usuario podrá comprobar en primera persona el precio de una publicación con las carácterísticas que el usuario indique.", style=style_texto),

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
                    html.P("En primer lugar, analizamos la distribución del precio. Dado que el precio es la principal variable a predecir, su distribución temporal es de gran importancia. A simple vista, podemos ver que si nos fijamos en el rango completo, existe un gran numero de outliers, siendo mucho más representativa la distribución para el rango 0 - 300.", style=style_texto),

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
                    html.P("En este caso, podemos comprobar, en primer lugar, que la inmensa mayoría de publicaciones, alrededor del 45%, abarcan el distrito Centro, el gran núcleo turístico de la ciudad. Por otro lado, en cuanto al precio podemos distinguir tres categorías: en primer lugar, una primera categoría formada por Salamanca y San Blás, con un precio de alrededor de 76€. Por otro lado, una segunda categoría con precios entre 55€ y 65€, formada por barrios como Chamberí o Chamartín. Finalmente, una tercera categoría con precios entre 25€ y 40€ formada por barrios como Moratalaz o Villaverde, entre otros.", style=style_texto),

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
                    html.P("De nuevo, podemos comprobar la influencia del barrio en el precio de la publicacion, existiendo claramente ditritos o barrios en los cuales existe una mayor demanda, y por ende un mayor precio. Claro ejemplo de ello son el barrio de Chueca, Malasaña o Barrio de las Letras. Además, podemos comprobar la densidad en cada barrio, incluso filtrando por precio. En este caso, comprobamos de nuevo que la gran mayoría de oferta reside en el distrito centro, en gran parte pos su atractivo turistico.", style=style_texto),

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
                            ),
                            html.H5(
                                "Escoja el tipo de habitación: ", style=style_texto
                            ),
                            html.Br(),
                            dcc.Dropdown(
                                options=options_room,
                                value='Hotel room',
                                placeholder="Selecciona el tipo de habitación",
                                id="room_exploratorio",
                                style=dropdown_style,
                                searchable=False
                            ),
                            dcc.Graph(
                                id='box-plot_room'
                            ),
                            html.P("Otro factor importante a tener en cuenta será el tipo de habitación que se ofrezca, pudiendo ser una habitación privada, un apartamento, habitación compartida, o habitación de hotel. En este caso, la mayoría de publicaciones corresponden a habitaciones privadas o apartamentos enteros. Además, podemos comprobar que en los casos de las habitaciones de hotel o apartamentos privados, el precio tiende a ser mucho mayor, como es de esperar.", style=style_texto),
                            html.H4(
                                "Análisis de las reviews: ", style=style_texto
                            ),
                            html.Br(),
                            dcc.Graph(
                                id="puntuacion_precio",
                                figure=px.scatter(
                                    x=df_modelo['puntuacion'][df_modelo["price"] < 1000],
                                    y=df_modelo["price"][df_modelo["price"] < 1000],
                                )
                            ),
                            html.P("Otra de las grandes variables a analizar será la puntuacion de las reviews. Como es de esperar, a mayor puntuacion media se presupone que existirá una mayor demanda para dicha publicación. Esto lo podemos comprobar en el gráfico, existiendo una tendencia ascendente a medida que aumenta la puntuacion media de la publicacion.", style=style_texto),
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id="box_superhost",
                                        figure=go.Figure(
                                            data=[
                                                go.Box(
                                                    y=df_modelo[(df_modelo["host_is_superhost"]
                                                                == True) & (df_modelo["price"]
                                                                < 500)]["price"],
                                                    marker_color="steelblue",
                                                    name="Precio",
                                                    boxmean=True
                                                )
                                            ],
                                            layout=go.Layout(
                                                yaxis_title="Precio",
                                                xaxis_title="Distribución de precios para superhosts"
                                            )
                                        )
                                    ),
                                    dcc.Graph(
                                        id="box_superhost_false",
                                        figure=go.Figure(
                                            data=[
                                                go.Box(
                                                    y=df_modelo[(df_modelo["host_is_superhost"]
                                                                == False) & (df_modelo["price"]
                                                                < 500)]["price"],
                                                    marker_color="steelblue",
                                                    name="Precio",
                                                    boxmean=True
                                                )
                                            ],
                                            layout=go.Layout(
                                                yaxis_title="Precio",
                                                xaxis_title="Distribución de precios para no superhosts"
                                            )
                                        )
                                    ),
                                ],
                                style={
                                    'text-align': 'center'
                                }
                            )
                        ]
                    ),
                ]),

        # Pestaña de resultados del modelo y app
        dcc.Tab(
            label='Modelo',
            style=tab_style,
            selected_style=tab_selected_style,
            children=[
                html.Br(),
                html.Br(),
                html.H3(
                    children=[
                        "Prediccion de precio"
                    ],
                    id="subtituloModelo",
                    style={
                        "text-align": "center",
                        "font-family": "verdana",
                        "display": "block"
                    }
                ),
                html.P(
                    "A continuacion, se ofrece la posibilidad de predecir el precio de una publicacion de Airbnb ficticia, introduciendo los datos pertinentes",
                    style={
                        "text-align": "center",
                        "font-family": "verdana",
                        "display": "block"
                    }
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H5(
                                    "Es usted superhost:"
                                ),
                                html.Br(),
                                dcc.RadioItems(
                                    id="superhost",
                                    options=[{'label': 'Si', 'value': 'True'}, {
                                        'label': 'No', 'value': 'False'}],
                                    labelStyle={'display': 'inline-block'}
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(
                                    "Escoja el barrio correspondiente: "
                                ),
                                html.Br(),
                                dcc.Dropdown(
                                    options=options_neigh,
                                    placeholder="Selecciona barrio",
                                    id="dropdown_neighb",
                                    style={
                                        "display": "block",
                                        "width": "300px",
                                        "margin-left": "10px"
                                    }
                                ),
                            ],
                            style={
                                "width": "300px",
                                "height": "200px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5(
                                    "Escoja el tipo de habitación: "
                                ),
                                html.Br(),
                                dcc.Dropdown(
                                    options=options_room,
                                    placeholder="Selecciona el tipo de habitación",
                                    id="dropdown_room",
                                    style={
                                        "display": "block",
                                        "width": "300px",
                                        "margin-left": "10px"
                                    }
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(
                                    "Introduzca el número de personas que acomoda: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="AccomInput",
                                    type="number",
                                    min=1,
                                    max=20
                                )
                            ],
                            style={
                                "width": "300px",
                                "height": "200px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5(
                                    "Introduzca el número de dormitorios: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="BedroomsInput",
                                    type="number",
                                    min=1,
                                    max=20
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(
                                    "Introduzca el número de baños: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="BathInput",
                                    type="number",
                                    min=1,
                                    max=20
                                ),
                            ],
                            style={
                                "width": "300px",
                                "height": "200px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5(
                                    "Introduzca el número de noches minimas: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="MinNights",
                                    type="number",
                                    min=0,
                                    max=30
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(
                                    "Introduzca el número de noches disponibles en un año: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="Availab365",
                                    type="number",
                                    min=0,
                                    max=365
                                ),
                            ],
                            style={
                                "width": "300px",
                                "height": "200px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5(
                                    "Introduzca el número de reviews: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="numberReviews",
                                    type="number",
                                    min=1,
                                    max=800
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(
                                    "Introduzca el número de publicaciones del host: "
                                ),
                                html.Br(),
                                dcc.Input(
                                    id="numberListings",
                                    type="number",
                                    min=1,
                                    max=300
                                ),
                            ],
                            style={
                                "width": "300px",
                                "height": "300px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5(
                                    "Introduzca una review: "
                                ),
                                html.Br(),
                                dcc.Textarea(
                                    id="review",
                                    placeholder="Introduzca review",
                                    value="",
                                    style={'width': '300px',
                                           'height': "100px", "margin": "auto"}
                                )
                            ],
                            style={
                                "width": "300px",
                                "height": "300px",
                                "display": "inline-block",
                                "margin": "30px"
                            }
                        )
                    ],
                    style={
                        "text-align": "center",
                        "border-style": "outset",
                        "border-color": "snow",
                        "border-width": "5px",
                        "background-color": "snow ",
                        'font-family': 'verdana',
                        "margin": "20px"

                    }
                ),
                html.Div(
                    children=[
                        html.Br(),
                        html.Button('Enviar',
                                    id='submit-button',
                                    n_clicks=0,
                                    style={
                                        "border-radius": "15px",
                                        "cursor": "pointer",
                                        "padding": "15px 25px",
                                        "text-family": "verdana"
                                    }
                                    ),
                        html.Br(),
                        html.P(id='app-text-output',
                               style={

                               },
                               children='Texto Previo'
                               )
                    ],
                    style={
                        "text-align": "center"
                    }
                )
            ]
        )
    ])
])

# -----------------------------------------------------------------------------------------
# Callback


@app.callback(
    Output(component_id='app-text-output', component_property='children'),
    Input(component_id='submit-button', component_property='n_clicks'),
    Input(component_id='superhost', component_property='value'),
    Input(component_id='dropdown_neighb', component_property='value'),
    Input(component_id='dropdown_room', component_property='value'),
    Input(component_id='AccomInput', component_property='value'),
    Input(component_id='BedroomsInput', component_property='value'),
    Input(component_id='BathInput', component_property='value'),
    Input(component_id='MinNights', component_property='value'),
    Input(component_id='Availab365', component_property='value'),
    Input(component_id='numberReviews', component_property='value'),
    Input(component_id='numberListings', component_property='value'),
    Input(component_id='review', component_property='value')
)
def update_model(n_clicks, superhost, neighb, room, accomodates, beds, bath, nights, availab, reviews, listings, review):
    if(n_clicks > 0):
        print(bool(superhost == 'True'))
        dataf = getDataFrame(bool(superhost == 'True'), neighb, room, accomodates,
                             beds, bath, nights, availab, reviews, listings, review)
        prediction = modelo.predict(dataf)[0]
        return 'El precio esperado es de "{}" '.format(
            int(prediction)
        )
    else:
        return ''


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


@app.callback(
    Output(component_id='box-plot_room', component_property='figure'),
    Input(component_id='room_exploratorio', component_property='value')
)
def update_boxplot(v):

    figure = go.Figure(
        data=[
            go.Box(
                y=df_listings[(df_listings["room_type"]
                              == v) & (df_listings["price"] < 1000)]["price"],
                marker_color="steelblue",
                name="Precio",
                boxmean=True
            )
        ],
        layout=go.Layout(
            yaxis_title="Precio",
            xaxis_title="Distribución de precios para habitaciones de tipo " +
            str(v)
        )
    )

    return figure


# A la funcion esta le tiene que entrar lo que sale del dash del modelo; Devuelve un dataframe, haces modelo.predict(el dataframe)[0] y es el precio
# @app.callback(
#
# )
def getDataFrame(superhost, neighb, room, accomodates, beds, bath, nights, availab, reviews, listings, review):
    puntuacion = float(multilang_classifier(review)[0]['label'].split(' ')[0])

    dat = {
        'host_is_superhost': superhost, 'latitude': 40.42051, 'longitude': -3.69506, 'accommodates': accomodates, 'bathrooms': bath, 'bedrooms': beds,
        'minimum_nights': nights, 'availability_365': availab, 'number_of_reviews': reviews, 'calculated_host_listings_count': listings, 'puntuacion': puntuacion,
        'neighbourhood_group_cleansed_Arganzuela': 0, 'neighbourhood_group_cleansed_Barajas': 0, 'neighbourhood_group_cleansed_Carabanchel': 0,
        'neighbourhood_group_cleansed_Centro': 0, 'neighbourhood_group_cleansed_Chamartín': 0, 'neighbourhood_group_cleansed_Chamberí': 0,
        'neighbourhood_group_cleansed_Ciudad Lineal': 0, 'neighbourhood_group_cleansed_Fuencarral - El Pardo': 0, 'neighbourhood_group_cleansed_Hortaleza': 0, 'neighbourhood_group_cleansed_Latina': 0,
        'neighbourhood_group_cleansed_Moncloa - Aravaca': 0, 'neighbourhood_group_cleansed_Moratalaz': 0, 'neighbourhood_group_cleansed_Puente de Vallecas': 0, 'neighbourhood_group_cleansed_Retiro': 0,
        'neighbourhood_group_cleansed_Salamanca': 0, 'neighbourhood_group_cleansed_San Blas - Canillejas': 0, 'neighbourhood_group_cleansed_Tetuán': 0,
        'neighbourhood_group_cleansed_Usera': 0, 'neighbourhood_group_cleansed_Vicálvaro': 0, 'neighbourhood_group_cleansed_Villa de Vallecas': 0,
        'neighbourhood_group_cleansed_Villaverde': 0, 'room_type_Entire home/apt': 0, 'room_type_Hotel room': 0, 'room_type_Private room': 0, 'room_type_Shared room': 0
    }
    neigh_key = 'neighbourhood_group_cleansed_' + neighb
    room_key = 'room_type_' + room
    dat[neigh_key] = 1
    dat[room_key] = 1

    dataf = pd.DataFrame(data=dat, index=[0])
    return dataf


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
