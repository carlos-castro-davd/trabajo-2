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

# df_calendar = pd.read_csv("/Users/diegoma/kaggle/calendar.csv")
#df_listings = pd.read_csv("/Users/diegoma/kaggle/listings.csv")
#df_neighbourhoods = pd.read_csv("/Users/diegoma/kaggle/neighbourhoods.csv")
# df_reviews = pd.read_csv("/Users/diegoma/kaggle/reviews.csv")
# df_reviews_det = pd.read_csv("/Users/diegoma/kaggle/reviews_detailed.csv")
# df_listings_det = pd.read_csv("/Users/diegoma/kaggle/listings_detailed.csv")


#Jaime
df_listings = pd.read_csv("/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/listings.csv")
df_neighbourhoods = pd.read_csv("/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/neighbourhoods.csv")
modelo = joblib.load("/Users/jaime/Documents/ICAI/Quinto/Desarrollo Apps de Visualización/Trabajo/DataFinal/modelo_RF.pkl")

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model_nlp = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
multilang_classifier = pipeline("sentiment-analysis", 
                                model=model_nlp, tokenizer = tokenizer)

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
                    html.Br(),
                    html.P("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.", style=style_texto),

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

                html.H3( 
                    children = [
                        "Prediccion de precio"
                    ],
                    id = "subtituloModelo",
                    style ={
                        "text-align": "center",
                        "font-family": "verdana",
                        "display": "block"
                    }
                ),
                html.P(
                    "A continuacion, se ofrece la posibilidad de predecir el precio de una publicacion de Airbnb ficticia, introduciendo los datos pertinentes",
                    style ={
                        "text-align": "center",
                        "font-family": "verdana",
                        "display": "block"
                    }
                ),
                html.Div(
                    children = [
                        html.Div(
                            children=[
                                html.H5(
                                    "Es usted superhost:"
                                ),
                                html.Br(),
                                dcc.RadioItems(
                                    id="superhost",
                                    options=[{'label': 'Si', 'value': 'True'},{'label':'No','value': 'False'}],
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
                                    options = options_neigh,
                                    placeholder = "Selecciona barrio",
                                    id = "dropdown_neighb",
                                    style = {
                                        "display": "block",
                                        "width": "300px",
                                        "margin-left": "10px"
                                    }
                                ),
                            ],
                            style = {
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
                                    options = options_room,
                                    placeholder = "Selecciona el tipo de habitación",
                                    id = "dropdown_room",
                                    style = {
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
                                    min = 1,
                                    max = 20
                                )
                            ],
                            style = {
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
                                    min = 1,
                                    max = 20
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
                                    min = 1,
                                    max = 20
                                ),
                            ],
                            style = {
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
                                    min = 0,
                                    max = 30
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
                                    min = 0,
                                    max = 365
                                ),
                            ],
                            style = {
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
                                    min = 1,
                                    max = 800
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
                                    min = 1,
                                    max = 300
                                ),
                            ],
                            style = {
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
                                    value = "",
                                    style={'width': '500px', 'height': "100px", "margin": "auto"}
                                )
                            ],
                            style = {
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
                        "margin" : "20px"
                        
                    }
                ),
                html.Div(
                    children=[
                        html.Br(),
                        html.Button('Enviar',id='Submit_button',n_clicks=0)
                    ],
                    style={
                        "text-align": "center"
                    }
                ),
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

##### A la funcion esta le tiene que entrar lo que sale del dash del modelo; Devuelve un dataframe, haces modelo.predict(el dataframe)[0] y es el precio
@app.callback(
    
)
def getPredDataFrame(superhost, accomodates, beds, bath, nights, availab, reviews, listings, review, neigh, room):
    
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

    neigh_key = 'neighbourhood_group_cleansed_' + neigh
    room_key = 'room_type_' + room
    dat[neigh_key] = 1
    dat[room_key] = 1

    dataf = pd.DataFrame(data = dat, index = [0])
    return dataf



# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
