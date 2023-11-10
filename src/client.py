import socket
import pickle
import pandas as pd
import time
import random

HOST = '10.20.62.105'
PORT = 8081
num_rows = 3
while True:
    data = {
        'Velocidad del viento km/h niccc': [random.randint(100, 150) for _ in range(num_rows)],
        'Precipitación % nicc': [random.randint(0, 50) for _ in range(num_rows)],
        'Temp_max nicc': [random.uniform(20, 35) for _ in range(num_rows)],
        'Tempnicc': [random.uniform(10, 25) for _ in range(num_rows)]
    }

    df = pd.DataFrame(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        data_to_send = pickle.dumps(df)
        client_socket.send(data_to_send)
        print(df)
        print("DataFrame enviado al servidor. nic <3")
    
    time.sleep(7)

    print("DataFrame enviado al servidor.")
    time.sleep(10)