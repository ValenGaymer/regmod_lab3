import socket
import pickle

HOST = '10.20.2.38'
PORT = 8081

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Esperando {HOST}:{PORT}")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Nueva conexión desde {addr}")
            while True:
                data_size_bytes = conn.recv(4)
                if not data_size_bytes:
                    break
                
                data_size = int.from_bytes(data_size_bytes, byteorder='big')
                data = conn.recv(data_size)
                if not data:
                    break
                
                df = pickle.loads(data)
                print("DataFrame recibido")
                print(df)
