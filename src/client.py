import socket
import pickle
import random
import pandas as pd
import time
import numpy as np
import webbrowser


HOST = '10.20.2.12'
PORT = 65000
num_rows = 10
random.seed(42)

import pandas as pd

df_o = pd.read_csv("src/clima_dataset.csv")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    i = 0
    while i < 110:
            data = {
                'Temperatura': df_o['Temp'][i:i+5],
                'Ozono': df_o['Ozone'][i:i+5]
            }

            i = i + 5
            df = pd.DataFrame(data)
            data_to_send = pickle.dumps(df)
            data_size = len(data_to_send)
            client_socket.send(data_size.to_bytes(4, byteorder='big'))
            client_socket.send(data_to_send)
            print(df)
            print("DataFrame enviado al servidor.")
            time.sleep(1)

    tamaño_data = client_socket.recv(4)
    data_size = int.from_bytes(tamaño_data, byteorder='big')
    data = b""
    while len(data) < data_size:
        more_data = client_socket.recv(data_size - len(data))
        if not more_data:
            raise Exception("Recibido menos datos de lo esperado")
        data += more_data
    dataframe = pickle.loads(data)
    print(f'Dataframe recibido: {dataframe}')

    tamaño_data = client_socket.recv(4)
    data_size = int.from_bytes(tamaño_data, byteorder='big')
    data = b""
    while len(data) < data_size:
        more_data = client_socket.recv(data_size - len(data))
        if not more_data:
            raise Exception("Recibido menos datos de lo esperado")
        data += more_data

    print(data.decode('utf-8'))

    length_data = client_socket.recv(4)
    length = int.from_bytes(length_data, byteorder='big')
    summary_data = b""
    while len(summary_data) < length:
        more_data = client_socket.recv(length - len(summary_data))
        if not more_data:
            raise Exception("Recibido menos datos de lo esperado")
        summary_data += more_data
    summary = pickle.loads(summary_data)
    print(summary)

    html_size_bytes = client_socket.recv(4)
    html_size = int.from_bytes(html_size_bytes, byteorder='big')

    html_content = b""
    while len(html_content) < html_size:
        data = client_socket.recv(html_size - len(html_content))
        if not data:
            break
        html_content += data
    html_file_path = 'received_html.html'
    with open(html_file_path, 'wb') as f:
        f.write(html_content)

    webbrowser.open(html_file_path, new=2)

    while True:
        print("¿Desea organizar alguna columna del dataframe de manera ascendente?")
        columna = input(f"¿Cuál columna? El dataframe tiene las siguientes: {dataframe.columns}")
        client_socket.sendall(columna.encode('utf-8'))
        tamaño_data = client_socket.recv(4)
        data_size = int.from_bytes(tamaño_data, byteorder='big')
        data = b""
        while len(data) < data_size:
            more_data = client_socket.recv(data_size - len(data))
            if not more_data:
                raise Exception("Recibido menos datos de lo esperado")
            data += more_data
        vector = pickle.loads(data)
        text = ''
        for i in vector:
            text = f'{text + str(i)} '
        print(columna)
        print(text)