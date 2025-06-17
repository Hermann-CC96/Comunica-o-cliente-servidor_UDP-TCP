# Projeto: Comunicação TCP Cliente-Servidor – PING/PONG com RTT

## 📌 Descrição

Este projeto consiste em dois programas simples escritos em Python, utilizando **sockets TCP**, para estabelecer uma comunicação entre um **servidor** e um **cliente**. O objetivo principal é:

- O **cliente** enviar mensagens do tipo `PING`.
- O **servidor** responder com mensagens do tipo `PONG`.
- O **cliente** medir o **RTT (Round Trip Time)** de cada requisição‑resposta.

Esse projeto é útil como um exercício prático para entender como funciona a comunicação em **redes TCP**, o conceito de **round trip time**, e o uso de **sockets** em Python.

---
.

├── serversocketUDP.py    # Código do servidor UDP

└── clientsocketUDP.py    # Código do cliente UDP

├── serversocketTCP.py    # Código do servidor TCP

└── clientsocketTCP.py    # Código do cliente TCP



**Executar**

Para executar cada uma das aplicações (UDP ou TCP), você precisará de dois terminais abertos no diretório do projeto.



Aplicação UDP

Inicie o Servidor UDP: Em um terminal, execute o script do servidor.



O servidor ficará aguardando o recebimento de mensagens.



Inicie o Cliente UDP: Em outro terminal, execute o script do cliente.



O cliente enviará os 10 pings, exibindo o RTT para as respostas recebidas ou uma mensagem de pacote perdido caso o tempo de

1 segundo seja excedido.



Aplicação TCP

Inicie o Servidor TCP: Em um terminal, execute o script do servidor.

O servidor aguardará uma conexão ser estabelecida.



Inicie o Cliente TCP: Em outro terminal, execute o script do cliente.



O cliente se conectará ao servidor e iniciará a troca de 10 mensagens, exibindo o RTT de cada uma.



**Explicação do Código do Server (serversocketTCP.py)**

1.  Configurações



![image](https://github.com/user-attachments/assets/cacaac8d-ba9d-4615-b674-8902dcc1dd7b)



socket.socket(socket.AF_INET, socket.SOCK_DGRAM): Esta linha cria o objeto de socket.

socket.AF_INET: Indica que usaremos o protocolo de endereço IPv4.

socket.SOCK_DGRAM: Especifica que o socket será do tipo UDP (User Datagram Protocol), que é um protocolo sem conexão e baseado em pacotes (datagramas).

server_socketUDP.bind(('', PORT)): Esta é uma etapa crucial para o servidor.

bind(): Associa o socket a um endereço de rede e uma porta.

'': O endereço em branco permite que o servidor aceitas conexões em todas as interfaces de rede disponíveis na máquina (ex: Wi-Fi, Ethernet).



2. Loop de Recebimento e Processamento de Mensagens



![image](https://github.com/user-attachments/assets/108f2171-713e-451f-ae07-2763f7e46a91)



server_socketUDP.recvfrom(1024): Este é um comando bloqueante. O servidor para aqui e espera até que um pacote UDP chegue.

1024: Tamanho do buffer, ou seja, o número máximo de bytes que ele pode receber de uma vez.

message: Contém os dados brutos recebidos (em bytes).

address: É uma tupla contendo o endereço IP e a porta do cliente que enviou a mensagem.

message.decode(): Converte os dados brutos (bytes) em uma string legível.

random.random(): Gera um número decimal entre 0.0 e 1.0.

A condição if ... < 0.3 tem 30% de chance de ser verdadeira.

continue: Se a condição for verdadeira, o comando continue pula para a próxima iteração do loop while,

ignorando todo o código abaixo. Na prática, isso simula que o servidor recebeu a mensagem, mas "perdeu" a resposta.

if decoded_message.upper().startswith("PING "): O servidor verifica se a mensagem recebida, convertida para maiúsculas,

começa com "PING ". Isso torna a verificação robusta.

parts = decoded_message.split('PING ', 1): Divide a mensagem no primeiro "PING " que encontrar. Por exemplo, "PING 1: data"

se torna ['', '1: data'].

content_after_ping = parts[1]: Pega o conteúdo que veio após "PING ".

response_message = f"PONG {content_after_ping}": Cria a mensagem de resposta, prefixando o conteúdo original com "PONG". Isso é

conhecido como "ecoar" (echo) o conteúdo.

server_socketUDP.sendto(...): Envia a resposta de volta.

response_message.encode(): Converte a string de resposta de volta para bytes.

address: Usa o endereço do cliente (que foi obtido no recvfrom) como destino.



Finalização:



![image](https://github.com/user-attachments/assets/b1004737-daf2-4193-8098-0b17671d6b16)



try...except: É uma boa prática para capturar possíveis erros que possam ocorrer durante a execução, evitando que o servidor "quebre" inesperadamente.





Explicação do Código do Cliente (clientsocketUDP.py)

1. Configurações



![image](https://github.com/user-attachments/assets/bb2180d9-c49b-49ce-849e-279cfda531a7)



time: Essencial para medir o tempo de envio e recebimento para calcular o RTT.

HOST_IP: Ponto crucial de configuração. Você deve substituir "192.168.0.103" pelo endereço IP real

da máquina onde o servidor está sendo executado.

PORT: Deve ser a mesma porta que o servidor está usando (4000). socket.socket(...): Cria o socket do cliente,

da mesma forma que o servidor. Note que o cliente não usa bind(), pois o sistema operacional atribui uma porta

de origem aleatória para ele quando o primeiro pacote é enviado.

client_sock.settimeout(1): Esta é a configuração mais importante do cliente. Ela define um tempo limite de 1

segundo para operações de socket bloqueantes (como recvfrom). Se o cliente não receber uma resposta do servidor

em 1 segundo, ele levantará uma exceção socket.timeout. É assim que a "perda de pacote" é detectada.



2. Loop de Envio do Ping e Medição do RTT



![image](https://github.com/user-attachments/assets/a9511663-438a-4508-bf8f-50ebe439719e)



for i in range(1, 11):: Cria um loop que executa 10 vezes (para i de 1 a 10), enviando um PING em cada iteração.

send_time = time.time(): Grava o carimbo de tempo exato antes de enviar a mensagem. É o início da medição do RTT.

mensagen = f"PING {i}: ...": Monta a mensagem de PING, incluindo o número da sequência (i) e a data/hora atual.

client_sock.sendto(...): Envia a mensagem (convertida para bytes) para o IP e porta do servidor.

data, server_enddress = client_sock.recvfrom(1024): O cliente para aqui e espera por uma resposta. Graças ao settimeout(1),

ele só esperará por no máximo 1 segundo.

rec_time = time.time(): Se uma resposta chegar, ele grava o tempo de recebimento.

rtt = (rec_time - send_time) * 1000: Calcula o RTT subtraindo o tempo de envio do tempo de recebimento. O resultado

(em segundos) é multiplicado por 1000 para ser exibido em milissegundos (ms).


3. Tratamento de Erros e Timeout e finalização

![image](https://github.com/user-attachments/assets/679eb543-8cad-4b83-b921-e8075ee96377)

except socket.timeout:: Este bloco é executado se a chamada recvfrom demorar mais de 1 segundo. É a indicação de que o

PONG não foi recebido a tempo, seja porque o PING original se perdeu, seja porque a resposta PONG do servidor se perdeu.

except Exception as e:: Captura quaisquer outros erros que possam ocorrer.

client_sock.close(): Após o loop terminar, o socket do cliente é fechado para liberar os recursos de rede.

O servidor é responsável por aguardar e gerenciar as conexões.

Configuração do Server Socket:

![image](https://github.com/user-attachments/assets/95a49a69-ec74-4c3a-b677-66e98c45d534)

socket.AF_INET: Indica que estamos usando o protocolo de endereço IPv4.

socket.SOCK_STREAM: Especifica que este é um socket TCP (orientado a fluxo).

serverSocket.bind(): Associa o socket ao endereço IP e porta especificados.

serverSocket.listen(1): Coloca o socket em modo de escuta, aceitando no máximo 1 conexão na fila de espera.

Loop Principal e Aceite de Conexão:

![image](https://github.com/user-attachments/assets/d9152832-cdcb-421d-860c-adee949cd477)

O serverSocket.accept() é uma chamada bloqueante: o programa pausa aqui até que um cliente se conecte.

Quando uma conexão é feita, ele retorna um novo objeto socket (connectionSocket) para a comunicação com

aquele cliente específico, e o endereço (addr) do cliente.

Troca de Mensagens:

![image](https://github.com/user-attachments/assets/f5f5e1e2-7b12-4f45-a0dc-ca0a34d1811f)

connectionSocket.recv(1024): Lê até 1024 bytes de dados vindos do cliente através do socket de conexão.

.decode(): Converte os bytes recebidos em uma string Python.

A resposta PONG é construída e depois convertida de volta para bytes com .encode() antes de ser enviada pelo connectionSocket.send().

Finalização:

![image](https://github.com/user-attachments/assets/cb3e0e92-e149-43f4-a0e4-54fac2a4401b)

O bloco try...finally garante que o connectionSocket.close() seja sempre chamado, fechando a conexão com o cliente atual,

mesmo que ocorra um erro. Isso libera os recursos e permite que o servidor volte a aguardar uma nova conexão.

Cliente (client.py)

O cliente inicia a comunicação com o servidor.

Configuração do Socket e Conexão:

![image](https://github.com/user-attachments/assets/521c4756-678d-4fcf-b3c8-9562356d7939)

O socket do cliente é criado da mesma forma, mas em vez de bind e listen, ele usa clientSocket.connect() para estabelecer

uma conexão com o endereço e a porta do servidor.

Loop de Envio e Recebimento:

![image](https://github.com/user-attachments/assets/8a4a36b3-95eb-44b4-b2dc-d7b446f8f8bc)

Um loop for executa a lógica de ping 10 vezes.

time.time() é chamado antes de enviar e depois de receber para capturar os timestamps necessários para o cálculo do RTT.

A lógica de envio (send) e recebimento (recv) é similar à do servidor, mas iniciada pelo cliente.

Encerramento do Socket:

![image](https://github.com/user-attachments/assets/73676ffa-b1d4-4fd2-9c2a-dbfe1dfd9d1c)

Após o loop (ou em caso de erro), o finally garante que o socket do cliente seja fechado, finalizando a

conexão com o servidor de forma limpa.


Análise da Implementação

Comunicação com UDP

A comunicação UDP foi implementada utilizando sockets do tipo SOCK_DGRAM. O cliente utiliza sendto() para enviar datagramas

diretamente ao IP e porta do servidor. Para cumprir o requisito de tolerância a falhas, o socket do cliente foi configurado

com settimeout(1), garantindo que o programa não espere indefinidamente por uma resposta.



Comunicação com TCP

Para a versão TCP, foram utilizados sockets do tipo SOCK_STREAM. A comunicação é orientada à conexão, exigindo que o servidor

utilize listen() e accept() para receber conexões e que o cliente utilize connect() para se conectar antes da troca de dados.

Esta abordagem garante a entregaconfiável das mensagens "ping" e "pong", eliminando a necessidade de um timeout no nível da

aplicação para tratar a perda de pacotes, como foi exigido na adaptação para TCP.
