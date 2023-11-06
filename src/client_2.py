import socket
import pickle
import random
import pandas as pd
import time

HOST = '192.168.101.82'
PORT = 8253
num_rows = 3

response_df = pd.DataFrame({})

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)  # Aumentar el tamaño del búfer
    for i in range(10):
            data = {
                'Var3': [random.randint(100, 150) for _ in range(num_rows)],
                'Var4': [random.randint(0, 50) for _ in range(num_rows)]
            }

            df = pd.DataFrame(data)

            data_to_send = pickle.dumps(df)  # Serialize DataFrame using pickle
            data_size = len(data_to_send)
            client_socket.send(data_size.to_bytes(4, byteorder='big'))  # Envía el tamaño de los datos
            client_socket.send(data_to_send)
            print(df)
            print("DataFrame enviado al servidor.")

        # Espera la respuesta del servidor
    response_size_bytes = client_socket.recv(4)
    response_size = int.from_bytes(response_size_bytes, byteorder='big')
    response_data = client_socket.recv(response_size)
    response_df = pickle.loads(response_data)  # Deserialize using pickle
    print("DataFrame final recibido del servidor:")
    print(response_df)
    time.sleep(5)

    
