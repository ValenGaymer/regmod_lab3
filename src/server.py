import threading
import pandas as pd
import socket
import pickle

HOST = '192.168.101.82'
PORT = 8253

client_dataframes = {}
sensores_lista = []
lock = threading.Lock()

def handle_client(conn):
    try:
        client_df = pd.DataFrame()  # Crear un DataFrame para el cliente actual
        while len(client_df) < 30:  # Esperar a recibir 10 dataframes

            data_size_bytes = conn.recv(4)
            if not data_size_bytes:
                break
            
            data_size = int.from_bytes(data_size_bytes, byteorder='big')
            data = b""
            while len(data) < data_size:
                more_data = conn.recv(data_size - len(data))
                if not more_data:
                    raise Exception("Recibido menos datos de lo esperado")
                data += more_data
                print(data)
            df = pickle.loads(data)
            
            client_df = pd.concat([client_df, df], axis=0, ignore_index=True)
            print(f'client_Df:     {client_df}')
        

        sensores_lista.append("sensor")

        while len(sensores_lista) < 3:
            print(f'TAMAÑO LISTAA {len(sensores_lista)}\n')
            pass

        with lock:
            client_dataframes[threading.current_thread().ident] = client_df
            print(f'wlock:    {client_dataframes[threading.current_thread().ident]}')
            final_dataframe = pd.concat(client_dataframes, axis=1)

        print(final_dataframe)
        conn.send(len(pickle.dumps(final_dataframe)).to_bytes(4, byteorder='big'))
        conn.send(pickle.dumps(final_dataframe))
    except Exception as e:
        print(f"Error al manejar cliente: {e}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Esperando {HOST}:{PORT}")
