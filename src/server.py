import socket
import pickle
import pandas as pd
import threading
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from scipy import stats
import numpy as np
import plotly.express as px
import pandas as pd
import numpy as np
import webbrowser
import random

HOST = '10.20.2.21'
PORT = 65000

client_dataframes = []
sensores_lista = []
lock = threading.Lock()
EXPECTED_SENSORS = 3
global df_f
df_f = {}

SOCKET_SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_SERVIDOR.bind((HOST, PORT))
SOCKET_SERVIDOR.listen()
print(f"Esperando {HOST}:{PORT}")

def handle_client(conn):

    try:
        client_df = pd.DataFrame()
        while len(client_df) < 100:

            tamaño_data = conn.recv(4)
            if not tamaño_data:
                break
            
            data_size = int.from_bytes(tamaño_data, byteorder='big')
            data = b""
            while len(data) < data_size:
                more_data = conn.recv(data_size - len(data))
                if not more_data:
                    raise Exception("Recibido menos datos de lo esperado")
                data += more_data
            df = pickle.loads(data)
            
            client_df = pd.concat([client_df, df], axis=0, ignore_index=True)
        
        with lock:
            client_dataframes.append(client_df)    
        #conn.send(len(pickle.dumps(final_dataframe)).to_bytes(4, byteorder='big'))
        #conn.send(pickle.dumps(final_dataframe))

    except Exception as e:
        print(f"Error al manejar cliente: {e}")

client_connections = []

while len(sensores_lista)<=EXPECTED_SENSORS - 1:
    print(client_dataframes)
    conn, addr = SOCKET_SERVIDOR.accept()
    print(f"Nueva conexión desde {addr}")
    client_connections.append(conn)
    client_thread = threading.Thread(target=handle_client, args=(conn,))
    sensores_lista.append("sensor")
    client_thread.start()

print("Pasó primer while")

print("Segundo while")
while len(client_dataframes) != EXPECTED_SENSORS:
    print('esperando')
    print(len(client_dataframes))
    pass

print('cerró')

final_dataframe = pd.concat(client_dataframes, axis=1)
df_f = final_dataframe

data_to_send = pickle.dumps(df_f)
size = len(data_to_send).to_bytes(4, byteorder='big')

for conn in client_connections:
        try:
            conn.sendall(size)
            conn.sendall(data_to_send)
        except Exception as e:
            print(f"Error al enviar datos al cliente: {e}") 


# Normalidad
normals=0
no_normals=0
analisis = '<strong>Pruebas de Normalidad</strong>'
print(df_f.dtypes)

# Normalidad ...
for columna in df_f.columns:
      print(columna)
      if df_f[columna].dtype in ['int32', 'float32']:
            print('numérica')
            data = df_f[columna]
            stat, p = stats.shapiro(data)
            analisis = analisis + f"<br /><br />Variable: {columna}"
            analisis = analisis + "<br />Estadístico de prueba: "+ str(stat)
            analisis = analisis + "<br />Valor p: "+ str(p)
            alpha = 0.05
            if p > alpha:
                analisis = analisis + f"<br />La variable {columna.lower()} sigue una distribución normal<br />"
                normals+=1
            else:
                analisis = analisis + f"<br />La variable {columna.lower()} no siguen una distribución normal<br />"
                no_normals+=1

print(f'analisis de noramlidad: {analisis}')
# Correlación
analisis = analisis + "<br /><strong>Correlación</strong><br />"
dependiente = "Temperatura"
numeric_columns = df_f.select_dtypes(include=['int32', 'float64'])
correlation_matrix = np.corrcoef(numeric_columns, rowvar=False)
correlation_df = pd.DataFrame(correlation_matrix, columns=numeric_columns.columns, index=numeric_columns.columns)

for column in df_f.columns:
  if df_f[column].dtype in ['int32', 'float64'] and column!=dependiente:
    val=correlation_df[dependiente][column]
    if abs(val)==val:
      analisis  = analisis + f"<br />Las variables {column} y {dependiente} tienen un coeficiente de correlación positivo ({val}). Esto quiere decir que a mayor {column.lower()} mayor {dependiente.lower()}"
      print("<br />")
    else:
      analisis = analisis + f"<br />Las variables {column} y {dependiente} tienen un coeficiente de correlación negativo ({val}). Esto quiere decir que a mayor {column.lower()} menor {dependiente.lower()}"

print(f'analisis completo: {analisis}')

data_to_send = analisis.encode('utf-8')
size = len(data_to_send).to_bytes(4, byteorder='big')

for conn in client_connections:
    try:
        conn.sendall(size)
        conn.sendall(data_to_send)
    except Exception as e:
        print(f"Error al enviar datos al cliente: {e}")

# MODELO DE REGRESIÓN:
def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

variables_respuesta=[]
y = df_f[dependiente]
for columna in df_f.columns:
   if df_f[columna].dtypes in ['int32', 'float64'] and columna != dependiente:
      variables_respuesta+=([df_f[columna]])

print(variables_respuesta)
reg_m = reg_m(y, variables_respuesta)
print(f'MODELO: {reg_m.summary()}')
reg = pickle.dumps(reg_m.summary())

for conn in client_connections:
        try:
            conn.sendall(len(reg).to_bytes(4, byteorder='big'))
            conn.sendall(reg)
        except Exception as e:
            print(f"Error al enviar datos al cliente: {e}") 

# HTML

num_rows = 3
df = df_f

color_palette = ["#de6e4b", "#7fd1b9", "#7fd1b9", "#7a6563", "#E56399"]
correlation_matrix = df.corr()
fig_corr = px.imshow(correlation_matrix.values,
                     labels=dict(color="Correlación"),
                     x=df.columns,
                     y=df.columns,
                     title="Diagrama de Correlación Múltiple", height=500, width=1000,
                     color_continuous_scale = ["#7FD1B9", "#de6e4b"])

reg_summary = str(reg_m.summary())
reg_summary_html = reg_summary.replace('\n', '<br>')
reg_summary_html = reg_summary_html.replace('Notes: <\br>[1] Standard Errors assume that the covariance matrix of the errors is correctly specified..', '<br>')


with open('histogramas.html', 'w', encoding='utf-8') as f:
    f.write('<html>')
    f.write('<head><meta charset="UTF-8"><style>')
    f.write('.toc-container { position: fixed; top: 110px; right: 0; padding: 10px; background-color: #fff; border; font-family: Arial, sans-serif; }')
    f.write('.toc-title { font-size: 18px; color: rgb(229, 99, 153); margin-bottom: 10px; }')
    f.write('.toc-list { list-style-type: none; padding: 0; margin: 0; }')
    f.write('.toc-item { margin-bottom: 5px; }')
    f.write('.toc-link { text-decoration: none; color: #333; font-weight: bold; }')
    f.write('.toc-link:hover { color: rgb(229, 99, 153); }')
    f.write('</style></head>')
    f.write('<body style="background-color: #ffffff;">')

    f.write('<h1 style="text-align: left; font-family: Arial, sans-serif; padding: 30px; color: white; background-color: rgb(127, 209, 185);">RESUMEN ESTADÍSTICO</h1>')

    f.write('<h2 id = "histogramas" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(229, 99, 153);">Histogramas</h2>')
    for i, variable in enumerate(df.columns, start=1):
        fig_hist_variable = px.histogram(df, x=variable, marginal="box", nbins=30, title=f"Histograma de {variable}", height=500, width=600, color_discrete_sequence=[color_palette[i % len(color_palette)]])
        f.write(fig_hist_variable.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write('<h2 id = "correlacion" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(222, 110, 75);">Correlación</h2>') 
    f.write(fig_corr.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write('<h2 id = "modelo" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(127, 209, 185);">Modelo de regresión lineal</h2>') 
    f.write(f'<p style = "text-align: center; font-size: 18px; color: #333; padding: 20px; background-color: #f0f0f0; border-radius: 10px; font-family: Arial, sans-serif;">{reg_summary_html}.</p>')
    f.write('<h2 id = "analisis" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(127, 209, 185);">Análisis</h2>')
    f.write(f'<p style = "text-align: center; font-size: 18px; color: #333; padding: 20px; background-color: #f0f0f0; border-radius: 10px; font-family: Arial, sans-serif;">{analisis}.</p>')

    f.write('<div class="toc-container">')
    f.write('<h2 class="toc-title">Tabla de Contenidos</h2>')
    f.write('<ul class="toc-list">')
    f.write('<li class="toc-item"><a class="toc-link" href="#histogramas">Histogramas</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#correlacion">Correlación</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#modelo">Modelo de regresión lineal</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#analisis">Análisis</a></li>')
    f.write('</ul>')
    f.write('</div>')

    f.write('</body>')
    f.write('</html>')

with open('histogramas.html', 'rb') as f:
    html_content = f.read()

for conn in client_connections:
        try:
            conn.sendall(len(html_content).to_bytes(4, byteorder='big'))
            conn.sendall(html_content)
        except Exception as e:
            print(f"Error al enviar datos al cliente: {e}") 
SOCKET_SERVIDOR.close()