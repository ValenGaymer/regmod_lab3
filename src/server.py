import socket
import pickle
import pandas as pd
import threading
import dash
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import statsmodels.api as sm
import sys

HOST = '10.20.2.22'
PORT = 65000

client_dataframes = []
sensores_lista = []
lock = threading.Lock()
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


while len(sensores_lista)<=1:
    print(client_dataframes)
    conn, addr = SOCKET_SERVIDOR.accept()
    print(f"Nueva conexión desde {addr}")
    client_thread = threading.Thread(target=handle_client, args=(conn,))
    sensores_lista.append("sensor")
    client_thread.start()

while len(client_dataframes) <=1:
    print('esperando')
    print(len(client_dataframes))
    pass

print('cerró')

final_dataframe = pd.concat(client_dataframes, axis=1)
print(final_dataframe)
df_f = final_dataframe

data_to_send = pickle.dumps(df_f)
size = len(data_to_send).to_bytes(4, byteorder='big')
conn.sendall(size)
conn.sendall(data_to_send)