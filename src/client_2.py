import socket
import pickle
import random
import pandas as pd
import time
import numpy as np
import webbrowser

HOST = '10.20.2.21'
PORT = 65000
num_rows = 10
random.seed(42)
df = pd.DataFrame({})

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    for i in range(10):
            ps = np.random.uniform(0, 90, num_rows)
            data = {
                'Presión superficial': ps
            }
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
    client_socket.close()

    
