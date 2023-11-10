import socket
import pickle
import random
import pandas as pd
import time

HOST = '10.20.2.22'
PORT = 65000
num_rows = 3
response_df = pd.DataFrame({})
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    for i in range(10):
            data = {
                'Temperatura': [random.randint(100, 150) for _ in range(num_rows)],
                'Humedad': [random.randint(0, 50) for _ in range(num_rows)]
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
    print(dataframe)

