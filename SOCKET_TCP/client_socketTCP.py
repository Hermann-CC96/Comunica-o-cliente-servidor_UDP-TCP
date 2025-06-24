import socket
import time
import datetime


SERVER_IP = '127.0.0.1' 
PORT = 5000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar ao servidor
    clientSocket.connect((SERVER_IP, PORT))
    print(f"Conectado ao servidor TCP em {SERVER_IP}:{PORT}")

    # Enviar 10 mensagens ping
    for i in range(1, 11):
        send_time = time.time()
        message = f"PING {i} {datetime.datetime.now()}"

        try:
            # Enviar a mensagem
            clientSocket.send(message.encode())
            print(f"Ping {i} enviado: {message}")
            
            data = clientSocket.recv(1024) # Tamanho do buffer
            receive_time = time.time()
            rtt = (receive_time - send_time) * 1000 # RTT em milissegundos

            decoded_data = data.decode()
            print(f"Pong {i} recebido: {decoded_data}")
            print(f"RTT para Ping {i}: {rtt:.2f} ms")

            time.sleep(1) # Pequena pausa entre os pings

        except socket.timeout:
            # No TCP, timeouts geralmente indicam problemas de conexão, não perda de pacotes individuais
            print(f"Ping {i} tempo esgotado: Conexão inativa ou problema de rede.")
        except Exception as e:
            print(f"Erro na comunicação TCP para Ping {i}: {e}")
            break # Sair do loop se houver um erro grave de conexão

finally:
    # Fechar o socket do cliente
    clientSocket.close()
    print("Cliente TCP finalizado.")