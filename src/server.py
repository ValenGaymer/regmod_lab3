import socket
import pickle
import pandas as pd
import threading
import dash
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
import sys
from pprint import pprint
from scipy import stats
import seaborn as sns
import numpy as np
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import statistics as stats2

HOST = '10.20.2.22'
PORT = 65000

client_dataframes = []
sensores_lista = []
lock = threading.Lock()
EXPECTED_SENSORS = 1
global df_f
df_f = {}

SOCKET_SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_SERVIDOR.bind((HOST, PORT))
SOCKET_SERVIDOR.listen()
print(f"Esperando {HOST}:{PORT}")

def handle_client(conn):

    try:
        client_df = pd.DataFrame()
        while len(client_df) < 30:

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

while len(client_dataframes) != EXPECTED_SENSORS:
    print('esperando')
    print(len(client_dataframes))
    pass

print('cerró')

final_dataframe = pd.concat(client_dataframes, axis=1)
print(final_dataframe)
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
analisis = 'Pruebas de Normalidad'

# Normalidad ...
for columna in df_f.columns:
      if df_f[columna].dtype in ['int64', 'float64']:
            data = df_f[columna]
            stat, p = stats.shapiro(data)
            analisis = analisis + f"\n\nColumna: {columna}"
            analisis = analisis + "\nEstadístico de prueba: "+ str(stat)
            analisis = analisis + "\nValor p: "+ str(p)
            alpha = 0.05
            if p > alpha:
                analisis = analisis + f"\nLa variable {columna.lower()} sigue una distribución normal\n"
                normals+=1
            else:
                analisis = analisis + f"\nLa variable {columna.lower()} no siguen una distribución normal\n"
                no_normals+=1


# Correlación
analisis = analisis + "\nCorrelación\n"
dependiente = "Temperatura"
numeric_columns = df_f.select_dtypes(include=['int64', 'float64'])
correlation_matrix = np.corrcoef(numeric_columns, rowvar=False)
correlation_df = pd.DataFrame(correlation_matrix, columns=numeric_columns.columns, index=numeric_columns.columns)

for column in df_f.columns:
  if df_f[column].dtype in ['int64', 'float64'] and column!=dependiente:
    val=correlation_df[dependiente][column]
    if abs(val)==val:
      analisis  = analisis + f"\nLas variables {column} y {dependiente} tienen un coeficiente de correlación positivo ({val}). Esto quiere decir que a mayor {column.lower()} mayor {dependiente.lower()}"
      print("\n")
    else:
      analisis = analisis + f"\nLas variables {column} y {dependiente} tienen un coeficiente de correlación negativo ({val}). Esto quiere decir que a mayor {column.lower()} menor {dependiente.lower()}"

print(analisis)

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
   if df_f[columna].dtype in ['int64', 'float64'] and columna != dependiente:
      variables_respuesta+=([df_f[columna]])

print(variables_respuesta)

reg_m=reg_m(y, variables_respuesta)
reg = pickle.dumps(reg_m.summary())

for conn in client_connections:
        try:
            conn.sendall(len(reg).to_bytes(4, byteorder='big'))
            conn.sendall(reg)
        except Exception as e:
            print(f"Error al enviar datos al cliente: {e}") 

SOCKET_SERVIDOR.close()