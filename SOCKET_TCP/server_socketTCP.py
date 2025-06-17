import socket
import datetime
import time
 
PORT = 5000
HOST = '200.135.94.239'

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)
print(f"Servidor TCP escutando em {HOST}:{PORT}")


while True:
    print("Aguardando por uma conexão...")
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexão estabelecida com {addr}")
    
    try:
        while True:
            message = connectionSocket.recv(1024) # Tamanho do buffer
            if not message: # Se não houver mais dados, a conexão foi fechada pelo cliente
                break
            decoded_message = message.decode()
            print(f"Recebido '{decoded_message}' de {addr}")
            response_message = f"PONG {decoded_message.split('PING ')[1]}"
            connectionSocket.send(response_message.encode())
            print(f"Enviado '{response_message}' para {addr}")

    except Exception as e:
        print(f"Erro na comunicação com {addr}: {e}")
    finally:
        # Fechar o socket de conexão com o cliente
        connectionSocket.close()