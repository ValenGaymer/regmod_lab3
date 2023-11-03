import socket
import pickle

HOST = '10.20.62.105'
PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Esperando{HOST}:{PORT}")
    conn, addr = server_socket.accept()

    with conn:
        print(f"Nueva conexión desde {addr}")
        while True:
            data = conn.recv(4096)
            if data:
                df = pickle.loads(data)
                print("Df recibido")
                print(df)