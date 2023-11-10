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

analisis = ''

# Normalidad ...
for columna in df_f.columns:
      if df_f[columna].dtype in ['int64', 'float64']:
            data = df_f[columna]
            stat, p = stats.shapiro(data)
            analisis = analisis + f"\n\nColumna: {columna}"
            analisis = analisis + ("\nEstadístico de prueba:", stat)
            analisis = analisis + ("\nValor p:", p)
            alpha = 0.05
            if p > alpha:
                print(f"La variable {columna} sigue una distribución normal")
                normals+=1
            else:
                print(f"La variable {columna} no siguen una distribución normal")
                no_normals+=1
            print("\n")

# Correlación
for column in df_f.columns:
  if df_f[column].dtype in ['int64', 'float64'] and column!=dependiente:
    val=correlation_df[dependiente][column]
    if abs(val)==val:
      print("\n")
      print(f"las variables {column} & {dependiente}")
      print("se tiene una correlacion positiva, O sea una pendiente positiva en la grafica de dispersion ")
      print("con un valor de :", val)
      print("\n")
    else:
      print("\n")
      print(f"las variables {column} & {dependiente}")
      print(f"se tiene una correlacion negativa, O sea una pendiente negativa en la grafica de dispersion. A medida que aumenta {column} disminuye {dependiente} ")
      print("con un valor de :", val)
      print("\n")