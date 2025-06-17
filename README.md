# Projeto: Comunicação TCP Cliente-Servidor – PING/PONG com RTT

## 📌 Descrição

Este projeto consiste em dois programas simples escritos em Python, utilizando **sockets TCP**, para estabelecer uma comunicação entre um **servidor** e um **cliente**. O objetivo principal é:

- O **cliente** enviar mensagens do tipo `PING`.
- O **servidor** responder com mensagens do tipo `PONG`.
- O **cliente** medir o **RTT (Round Trip Time)** de cada requisição‑resposta.

Esse projeto é útil como um exercício prático para entender como funciona a comunicação em **redes TCP**, o conceito de **round trip time**, e o uso de **sockets** em Python.

---

## 📂 Estrutura do Projeto
.
├── serversocketUDP.py    # Código do servidor UDP
├── clientsocketUDP.py    # Código do cliente UDP
├── serversocketTCP.py    # Código do servidor TCP
└── clientsocketTCP.py    # Código do cliente TCP
```

## ▶️ Executar

Para executar cada uma das aplicações (UDP ou TCP), você precisará de dois terminais abertos no diretório do projeto.

### Aplicação UDP

1.  **Inicie o Servidor UDP**: Em um terminal, execute o script do servidor. O servidor ficará aguardando o recebimento de mensagens.
    `python serversocketUDP.py`

2.  **Inicie o Cliente UDP**: Em outro terminal, execute o script do cliente. O cliente enviará 10 pings, exibindo o RTT para as respostas recebidas ou uma mensagem de pacote perdido caso o tempo de 1 segundo seja excedido.
    `python clientsocketUDP.py`

### Aplicação TCP

1.  **Inicie o Servidor TCP**: Em um terminal, execute o script do servidor. O servidor aguardará uma conexão ser estabelecida.
    `python serversocketTCP.py`

2.  **Inicie o Cliente TCP**: Em outro terminal, execute o script do cliente. O cliente se conectará ao servidor e iniciará a troca de 10 mensagens, exibindo o RTT de cada uma.
    `python clientsocketTCP.py`

---

##  dissected_code: Explicação dos Códigos

### Protocolo UDP

#### Servidor (serversocketUDP.py)

**1. Configurações**
- **`socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`**: Esta linha cria o objeto de socket.
  - **`socket.AF_INET`**: Indica que usaremos o protocolo de endereço IPv4.
  - **`socket.SOCK_DGRAM`**: Especifica que o socket será do tipo **UDP** (User Datagram Protocol), que é um protocolo sem conexão e baseado em pacotes (datagramas).
- **`server_socketUDP.bind(('', PORT))`**: Esta é uma etapa crucial para o servidor.
  - **`bind()`**: Associa o socket a um endereço de rede e uma porta.
  - **`''`**: O endereço em branco permite que o servidor aceite conexões em **todas as interfaces de rede** disponíveis na máquina (ex: Wi-Fi, Ethernet).

**2. Loop de Recebimento e Processamento de Mensagens**
- **`server_socketUDP.recvfrom(1024)`**: Este é um comando **bloqueante**. O servidor para aqui e espera até que um pacote UDP chegue.
  - **`1024`**: Tamanho do buffer, ou seja, o número máximo de bytes que ele pode receber de uma vez.
  - **`message`**: Contém os dados brutos recebidos (em bytes).
  - **`address`**: É uma tupla contendo o endereço IP e a porta do cliente que enviou a mensagem.
- **`random.random() < 0.3`**: Cria uma chance de 30% de "perder" a resposta, pulando o resto do código no loop com `continue`.
- **Lógica PING/PONG**: O servidor verifica se a mensagem é um "PING", extrai seu conteúdo, monta uma resposta "PONG" e a envia de volta para o endereço de origem usando `server_socketUDP.sendto()`.

**3. Finalização (Tratamento de Erros)**
- **`try...except`**: Captura possíveis erros durante a execução, evitando que o servidor pare inesperadamente.

#### Cliente (clientsocketUDP.py)

**1. Configurações**
- **`HOST_IP`**: **Ponto crucial**. Você deve substituir pelo endereço IP real da máquina onde o servidor está executando.
- **`client_sock.settimeout(1)`**: Configuração mais importante do cliente UDP. Define um **tempo limite de 1 segundo** para operações de recebimento. Se o cliente não receber uma resposta do servidor nesse tempo, ele levanta uma exceção `socket.timeout`, indicando que o pacote foi perdido.

**2. Loop de Envio do Ping e Medição do RTT**
- **`for i in range(1, 11)`**: Cria um loop que envia 10 PINGs.
- **`time.time()`**: Usado para registrar o tempo exato antes de enviar (`send_time`) e depois de receber (`rec_time`).
- **`rtt = (rec_time - send_time) * 1000`**: Calcula o Round-Trip Time (RTT) em milissegundos.

**3. Tratamento de Erros, Timeout e Finalização**
- **`except socket.timeout`**: Bloco executado se a resposta não chegar em 1 segundo, indicando perda de pacote.
- **`client_sock.close()`**: Após o loop, o socket do cliente é fechado para liberar os recursos.

---

### Protocolo TCP

#### Servidor (serversocketTCP.py)

**1. Configuração do Server Socket**
- **`socket.SOCK_STREAM`**: Especifica que este é um socket **TCP** (orientado a fluxo e conexão).
- **`serverSocket.listen(1)`**: Coloca o socket em modo de escuta, pronto para aceitar conexões. O `1` indica que no máximo 1 conexão pode ficar na fila de espera.

**2. Loop Principal e Aceite de Conexão**
- **`serverSocket.accept()`**: Chamada **bloqueante**. O programa pausa aqui até que um cliente se conecte. Quando a conexão é feita, ele retorna:
  - **`connectionSocket`**: Um novo objeto socket para a comunicação com aquele cliente específico.
  - **`addr`**: O endereço do cliente.

**3. Troca de Mensagens e Finalização**
- **`connectionSocket.recv(1024)`**: Lê dados vindos do cliente através do socket de conexão.
- **`connectionSocket.send()`**: Envia a resposta "PONG" de volta ao cliente.
- **`try...finally`**: Garante que `connectionSocket.close()` seja sempre chamado, fechando a conexão com o cliente atual antes de esperar por um novo.

#### Cliente (clientsocketTCP.py)

**1. Configuração do Socket e Conexão**
- **`clientSocket.connect(...)`**: Estabelece uma conexão com o endereço e a porta do servidor. Diferente do UDP, esta é uma etapa obrigatória antes da troca de dados.

**2. Loop de Envio, Recebimento e Encerramento**
- A lógica de envio (`send`), recebimento (`recv`) e cálculo de RTT é similar à do UDP, mas ocorre sobre a conexão já estabelecida.
- **`finally: clientSocket.close()`**: Garante que o socket do cliente seja fechado ao final, encerrando a conexão de forma limpa.

---

## 🔬 Análise da Implementação

### Comunicação com UDP
A comunicação UDP foi implementada utilizando sockets do tipo `SOCK_DGRAM`. O cliente utiliza `sendto()` para enviar datagramas diretamente ao IP e porta do servidor. Para cumprir o requisito de tolerância a falhas, o socket do cliente foi configurado com `settimeout(1)`, garantindo que o programa não espere indefinidamente por uma resposta.

### Comunicação com TCP
Para a versão TCP, foram utilizados sockets do tipo `SOCK_STREAM`. A comunicação é orientada à conexão, exigindo que o servidor utilize `listen()` e `accept()` para receber conexões e que o cliente utilize `connect()` para se conectar antes da troca de dados. Esta abordagem garante a entrega confiável das mensagens "ping" e "pong", eliminando a necessidade de um timeout no nível da aplicação para tratar a perda de pacotes.
```
