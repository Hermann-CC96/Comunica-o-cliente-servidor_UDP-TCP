import socket
import datetime
import time

#define a porta de conexão TCP
#Define o endereço IP do host que ouve em todas as interfaces disponíveis
 
PORT = 5000
HOST = '127.0.0.1' 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular o socket ao endereço e porta
serverSocket.bind((HOST, PORT))

# Começar a ouvir por conexões (máximo de 1 conexão pendente)
serverSocket.listen(1)
print(f"Servidor TCP escutando em {HOST}:{PORT}")

while True:
    print("Aguardando por uma conexão...")
    # Aceitar a conexão do cliente
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexão estabelecida com {addr}")

    try:
        while True:
            # Receber dados do cliente
            # O TCP recebe um fluxo de bytes, não datagramas discretos
            message = connectionSocket.recv(1024) # Tamanho do buffer
            if not message: # Se não houver mais dados, a conexão foi fechada pelo cliente
                break
            
            decoded_message = message.decode()
            print(f"Recebido '{decoded_message}' de {addr}")

            # Processar a mensagem (adicionar "PONG")
            response_message = f"PONG {decoded_message.split('PING ')[1]}"

            # Enviar resposta de volta ao cliente
            connectionSocket.send(response_message.encode())
            print(f"Enviado '{response_message}' para {addr}")

    except Exception as e:
        print(f"Erro na comunicação com {addr}: {e}")
    finally:
        # Fechar o socket de conexão com o cliente
        connectionSocket.close()
        print(f"Conexão com {addr} encerrada.")