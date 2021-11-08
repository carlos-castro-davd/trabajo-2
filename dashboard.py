import numpy as np
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

# --------------------------------------------------------------------
# Dashboard Ini
app = dash.Dash(__name__)

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

    html.Br()

])

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
