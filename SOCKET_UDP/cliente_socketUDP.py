import socket
import datetime
import time


#Defini o IP do servidor
#Defini a porta de comunicação UPD para cliente
HOST_IP = "200.135.94.199"
PORT = 12000

#Cria socket UDP do clientev 
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Defini timeout de 1s para o socket
client_sock.settimeout(1)

for i in range(1,11):
    send_time = time.time()
    mensagen = f"PING {1}: {datetime.datetime.now()}"
    try:
        # Cria dategrame com IP do servidor e port
        # Invia Mensagem via client_socket
        client_sock.sendto(mensagen.encode(),(HOST_IP, PORT))
        print(f"Ping {i} enviado: {mensagen}")
        
        data, server_enddress = client_sock.recvfrom(1024)
        rec_time = time.time()
        rtt = (rec_time - send_time)*1000
        
        
        decoded_data = data.decode()
        print(f"Pong {i} recebido: {decoded_data} de {server_enddress}")
        print(f"RTT para Ping {i}: {rtt:.2f} ms")


    except socket.timeout:
        print(f"Ping {i} tempo esgotado: pacote perdido (nenhuma resposta recebidae em 1s)")
    
    except Exception as e:
        print(f"Erro no cliente para Ping {i}: {e}")

client_sock.close()
print("Cliente UDP finalizado")