from dash import Dash, html, dash_table, dcc
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import statsmodels.api as sm

df_f = {}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    
        html.Div(className='row', children='Modelo de estudio',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

        dcc.Store(id='contenido-1', data=True),
        html.Div(className='row', children=[

            html.Div(id='data',className='six columns', children=[
                dash_table.DataTable(data=df_f.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
            ]),
            html.Div(id='hist',className='six columns', children=[
                dcc.Graph(figure=px.histogram(df_f, x='Var4', histfunc='avg', width=800, height=400), id='histo-chart-final')
            ]),
            html.Div(id='cor',className='six columns', children=[
            dcc.Graph(figure = px.scatter_matrix(df_f, dimensions=['Var1','Var2','Var3','Var4'], height=700))
            ])
        ], id="content-1-container"),

        dcc.Store(id='contenido-2',data=False),
        html.Div(className='row', children=[
            html.H1('Se muestra el modelo'),
        ],
         
        id="content-2-container"),
        html.Div([
                html.Button("modeloo", id="show-content-button"),
            ], style={'position': 'absolute', 'top': '20px', 'left': '20px', 'background-color': 'lightblue'}),
])
        
@app.callback(
    [Output("content-1-container", "style"),
     Output("content-2-container", "style")],
    Input("show-content-button", "n_clicks"),
    [Input("contenido-1", "data"),
     Input("contenido-2", "data")]
)
def show_content(n_clicks, content_1_visible, content_2_visible):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == "show-content-button":
                content_1_visible = not content_1_visible
                content_2_visible = not content_2_visible
        style_content_1 = {"display": "block" if content_1_visible else "none"}
        style_content_2 = {"display": "block" if content_2_visible else "none"}
        
        return style_content_1, style_content_2

app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

while True:
     pass