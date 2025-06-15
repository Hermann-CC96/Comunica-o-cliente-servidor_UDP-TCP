import socket
import datetime
import random

#Definindo a porta de comunicação UDP
PORT = 4000

#criando um socket UDP
#AF_INET PARA IPv4 e SOCK_DGRAM para UDP
server_socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Vinculando o socket ao endereço IP de servidor e a porta
server_socketUDP.bind(('',PORT))

print(f" Servidor UDP pronto para receber em {socket.gethostbyname(socket.gethostname())}:{PORT}")

while True:
    try:
        message, address = server_socketUDP.recvfrom(1024)
        decoded_message = message.decode()
        print(f"Recebido '{decoded_message}' de {address}")

        # Simular uma pequena perda de pacotes (opcional para testes)
        # 
        if random.random() < 0.3: # 30% de chance de "perder" a resposta
            print(f"Simulando perda de resposta para {address}")
            continue

        # --- CORREÇÃO AQUI ---
        # Verifique se a mensagem começa com 'PING ' (ignorando maiúsculas/minúsculas)
        if decoded_message.upper().startswith("PING "):
            # Divide a mensagem a partir de "PING " e pega o resto
            # O split('PING ')[1] funciona porque agora garantimos que 'PING ' está no início.
            # Também pode ser útil usar replace para normalizar a string se houver variações.
            try:
                # O split divide a string em uma lista. Se a string for "PING 123", resultará em ['', '123'].
                # Se a mensagem for exatamente "PING ", o split resultará em ['', '']
                # Precisa garantir que haja pelo menos dois elementos na lista após o split
                parts = decoded_message.split('PING ', 1) # Divide apenas uma vez
                if len(parts) > 1:
                    content_after_ping = parts[1]
                    response_message = f"PONG {content_after_ping}"
                    server_socketUDP.sendto(response_message.encode(), address)
                    print(f"Enviado '{response_message}' para {address}")
                else:
                    print(f"Formato 'PING ' inválido após prefixo para {address}: '{decoded_message}'")
            except IndexError:
                # Isso captura casos onde 'PING ' existe, mas não há conteúdo após ele (ex: apenas "PING ")
                print(f"Mensagem PING malformada (sem conteúdo após 'PING '): '{decoded_message}'")
            except Exception as inner_e:
                print(f"Erro ao processar mensagem PING: {inner_e} para '{decoded_message}'")
        else:
            print(f"Mensagem não é um PING esperado: '{decoded_message}' de {address}")
            # Você pode optar por ignorar ou registrar mensagens de outros formatos
            
    except Exception as e:
        print(f"Erro geral no servidor: {e}")