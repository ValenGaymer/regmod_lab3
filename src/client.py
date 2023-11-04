import socket
import pickle
import pandas as pd
import time
import random

HOST = '192.168.101.82'
PORT = 8253
num_rows = 3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    for i in range(10):
        data = {
            'Velocidad del viento km/h': [random.randint(100, 150) for _ in range(num_rows)],
            'Precipitación %': [random.randint(0, 50) for _ in range(num_rows)],
            'Temp_max': [random.uniform(20, 35) for _ in range(num_rows)],
            'Temp': [random.uniform(10, 25) for _ in range(num_rows)]
        }

        df = pd.DataFrame(data)

        data_to_send = pickle.dumps(df)
        data_size = len(data_to_send)
        client_socket.send(data_size.to_bytes(4, byteorder='big'))  # Envía el tamaño de los datos
        client_socket.send(data_to_send)
        print(df)
        print("DataFrame enviado al servidor.")

        time.sleep(1)
        