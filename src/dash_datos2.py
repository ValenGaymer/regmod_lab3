# Import packages
from dash import Dash, html, dash_table, dcc
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import statsmodels.api as sm

# Incorporate data

y=[10,11,11,13,10,11,10,11,4,2,7,10,9,9,6,5,5,5,6,4,3,3,4,10,6,8,2,0]
x1=[2113,2003,2957,2285,2971,2309,2528,2147,1689,2566,2363,2109,2295,1932,2213,1722,1498,1873,2118,1775,1904,1929,2080,2301,2040
        ,2447,1416,1503]
x2=[1985,2855,1737,2905,1666,2927,2341,2737,1414,1838,1480,2191,2229,2204,2140,1730,2072,2929,2268,1983,1792,1606,1492,2835
        ,2416,1638,2649,1503]
x3=[38.9,38.8,40.1,41.6,39.2,39.7,38.1,37.0,42.1,42.3,37.3,39.5,37.4,35.1,38.8,36.6,35.3,41.1,38.6,39.3,39.7,39.7,35.5,35.3
        ,38.7,39.9,37.4,39.3]
x4=[64.7,61.3,60.0,45.3,53.8,74.1,65.4,78.3,47.6,54.2,48.0,51.9,53.6,71.4,58.3,52.6,59.3,55.3,69.6,78.3,38.1,68.8,68.8,74.1,50.0
        ,57.1,56.3,47.0]
x6=[868,615,914,957,836,786,754,797,714,797,984,819,1037,986,819,791,776,789,582,901,734,627,722,683,576,848,684,875]
x7=[59.7,55.0,65.6,61.4,66.1,61.0,66.1,58.9,57.0,58.9,68.5,59.2,58.8,58.6,59.2,54.4,49.6,54.3,58.7,51.7,61.9,52.7,57.8,59.7,54.9
        ,65.3,43.8,53.5]
x8=[2205,2096,1847,1903,1457,1848,1564,2476,2577,2476,1984,1901,1761,1709,1901,2288,2072,2861,2411,2289,2203,2592,2053,1979,2048
        ,1786,2876,2560]
x9=[1917,1575,2175,2476,1866,2339,2092,2254,2001,2254,2217,1686,2032,2025,1686,1835,1914,2496,2670,2202,1988,2324,2550,2110,2628
        ,1776,2524,2241]

df=pd.DataFrame({'y':y,'x1':x1,'x2':x2,'x3':x3,'x4':x4,'x6':x6,'x7':x7,'x8':x8,'x9':x9})

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()

    return results

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
app.layout = html.Div([
    
        html.Div(className='row', children='Modelo de estudio',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

        dcc.Store(id='contenido-1', data=True),
        html.Div(className='row', children=[

            html.Div(id='data',className='six columns', children=[
                dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
            ]),
            html.Div(id='hist',className='six columns', children=[
                dcc.Graph(figure=px.histogram(df, x='x1', histfunc='avg', width=800, height=400), id='histo-chart-final')
            ]),
            html.Div(id='cor',className='six columns', children=[
            dcc.Graph(figure = px.scatter_matrix(df, dimensions=["y", "x1", "x2", "x3","x4","x6","x7","x8","x9"], height=700))
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
        
        # Determinar cuál contenido mostrar u ocultar
        if triggered_id == "show-content-button":
                content_1_visible = not content_1_visible
                content_2_visible = not content_2_visible
        
        # Establecer estilos para la visibilidad de los contenedores
        style_content_1 = {"display": "block" if content_1_visible else "none"}
        style_content_2 = {"display": "block" if content_2_visible else "none"}
        
        return style_content_1, style_content_2

        
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
