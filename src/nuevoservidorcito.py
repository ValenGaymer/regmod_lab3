import socket
import pickle
import pandas as pd
import threading

HOST = '10.20.2.38'
PORT = 8081
client_dataframes = {}
lock = threading.Lock()

def handle_client(conn):
    try:
        client_df = pd.DataFrame()  # Crear un DataFrame para el cliente actual
        entries_received = 0  # Contador de entradas recibidas para el cliente
        
        while entries_received < 10:  # Detenerse después de recibir 10 entradas
            data_size_bytes = conn.recv(4)
            if not data_size_bytes:
                break
            
            data_size = int.from_bytes(data_size_bytes, byteorder='big')
            data = conn.recv(data_size)
            if not data:
                break   
            df = pickle.loads(data)
            print("DataFrame recibido para el cliente")
            print(df)
            
            # Concatenar el DataFrame del cliente actual con el nuevo DataFrame
            client_df = pd.concat([client_df, df], axis=0)
            entries_received += 1
        
        # Almacenar el DataFrame del cliente en el diccionario
        with lock:
            client_dataframes[threading.current_thread().ident] = client_df
    except Exception as e:
        print(f"Error al manejar cliente: {e}")
    finally:
        conn.close()

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Esperando {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Nueva conexión desde {addr}")
    client_thread = threading.Thread(target=handle_client, args=(conn,))
    client_thread.start()
