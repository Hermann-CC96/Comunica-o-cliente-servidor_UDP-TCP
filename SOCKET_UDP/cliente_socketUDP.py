import socket
import datetime
import time

HOST_IP = "192.168.0.102"
PORT = 5000

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(1)

for i in range(1,11):
    send_time = time.time()
    mensagen = f"PING {1}: {datetime.datetime.now()}"
    try:
        
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