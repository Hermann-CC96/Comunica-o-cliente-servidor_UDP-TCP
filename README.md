# Projeto: Comunicação (UDP e TCP) Cliente-Servidor – PING/PONG com RTT

Este projeto é uma implementação de uma aplicação cliente-servidor do tipo "Ping-Pong" em Python, desenvolvida como parte de uma atividade acadêmica. A solução inclui duas versões distintas: uma utilizando o protocolo UDP e outra utilizando TCP, para demonstrar e comparar as características de cada protocolo de transporte

## 📌 Descrição

Este projeto consiste em dois programas simples escritos em Python, utilizando **sockets TCP**, para estabelecer uma comunicação entre um **servidor** e um **cliente**. O objetivo principal é:

- O **cliente** enviar mensagens do tipo `PING`.
- O **servidor** responder com mensagens do tipo `PONG`.
- O **cliente** medir o **RTT (Round Trip Time)** de cada requisição‑resposta.

# Sockets de Comunicação: UDP e TCP

Este documento descreve a estrutura, execução e funcionamento de aplicações cliente/servidor implementadas com os protocolos UDP e TCP.

---

## 📂 Estrutura do Projeto

├── serversocketUDP.py    # Código do servidor UDP

└── clientsocketUDP.py    # Código do cliente UDP

├── serversocketTCP.py    # Código do servidor TCP

└── clientsocketTCP.py    # Código do cliente TCP



## Executar

Para executar cada uma das aplicações (UDP ou TCP), você precisará de dois terminais abertos no diretório do projeto.

### Aplicação UDP

1.  **Inicie o Servidor UDP**: Em um terminal, execute o script do servidor.
    `python serversocketUDP.py`

2.  **Inicie o Cliente UDP**: Em outro terminal, execute o script do cliente.
    `python clientsocketUDP.py`

### Aplicação TCP

1.  **Inicie o Servidor TCP**: Em um terminal, execute o script do servidor.
    `python serversocketTCP.py`

2.  **Inicie o Cliente TCP**: Em outro terminal, execute o script do cliente.
    `python clientsocketTCP.py`

**Explicação do Código do Server (serversocketTCP.py)**

1.  Configurações
##  dissected_code: Explicação do Código UDP

### Servidor (serversocketUDP.py)

- **Configurações**: O socket é criado com `socket.AF_INET` para usar o protocolo **IPv4** e `socket.SOCK_DGRAM` para especificar que é **UDP**. O comando `bind()` associa o servidor a uma porta específica em todas as interfaces de rede da máquina (`''`), permitindo que ele "escute" por mensagens.
  
![image](https://github.com/user-attachments/assets/cacaac8d-ba9d-4615-b674-8902dcc1dd7b)

- **Loop e Recebimento**: O servidor entra em um loop infinito (`while True`). O comando `recvfrom()` é **bloqueante**—ele pausa o programa e espera até que uma mensagem chegue. Ao receber, ele obtém a mensagem e o endereço de quem enviou.

![image](https://github.com/user-attachments/assets/108f2171-713e-451f-ae07-2763f7e46a91)

- **Simulação de Perda e Resposta**: Para simular uma rede real, há **30% de chance** (`random.random() < 0.3`) de que o servidor ignore a mensagem recebida e simplesmente pule para a próxima iteração (`continue`). Caso contrário, ele verifica se a mensagem é um "PING", constrói uma resposta "PONG" e a envia de volta ao remetente.

![image](https://github.com/user-attachments/assets/b1004737-daf2-4193-8098-0b17671d6b16)


### Cliente (clientsocketUDP.py)

- **Configurações**: O ponto mais importante é `client_sock.settimeout(1)`. Isso configura um **tempo limite de 1 segundo**. Se o cliente enviar um PING e não receber uma resposta nesse tempo, ele gera um erro de `socket.timeout`.

![image](https://github.com/user-attachments/assets/bb2180d9-c49b-49ce-849e-279cfda531a7)

- **Loop e Medição de RTT**: O cliente envia 10 PINGs em um loop. Antes de enviar cada um, ele grava o tempo (`send_time`). Ao receber uma resposta, ele grava o tempo novamente (`rec_time`). A diferença entre os dois tempos (`rec_time - send_time`) é o **Round-Trip Time (RTT)**, ou tempo de ida e volta.

![image](https://github.com/user-attachments/assets/a9511663-438a-4508-bf8f-50ebe439719e)

- **Tratamento de Perda**: O bloco `try...except` é usado para lidar com o `socket.timeout`. Se o erro ocorrer, significa que a resposta não chegou em 1 segundo, e o cliente imprime uma mensagem de "pacote perdido".

![image](https://github.com/user-attachments/assets/679eb543-8cad-4b83-b921-e8075ee96377)


##  dissected_code: Explicação do Código TCP

### Servidor (serversocketTCP.py)

- **Configurações**: O socket é criado com `socket.SOCK_STREAM` para especificar o protocolo **TCP**. Diferente do UDP, o servidor usa `listen()` para se preparar para aceitar conexões, em vez de apenas receber pacotes.

![image](https://github.com/user-attachments/assets/95a49a69-ec74-4c3a-b677-66e98c45d534)

- **Conexão e Aceitação**: O comando `accept()` é **bloqueante** e faz o servidor esperar até que um cliente tente se conectar. Quando isso acontece, ele estabelece uma conexão e cria um **novo socket** (`connectionSocket`) dedicado exclusivamente à comunicação com aquele cliente específico.

![image](https://github.com/user-attachments/assets/d9152832-cdcb-421d-860c-adee949cd477)

- **Troca de Mensagens Confiável**: A comunicação ocorre através do novo socket. Como o TCP é um protocolo confiável e orientado à conexão, não há necessidade de simular perdas ou usar timeouts no nível da aplicação. O envio (`send`) e recebimento (`recv`) são garantidos pelo próprio protocolo.

![image](https://github.com/user-attachments/assets/f5f5e1e2-7b12-4f45-a0dc-ca0a34d1811f)

- **Finalização da Conexão**: Ao final da troca de mensagens, `connectionSocket.close()` fecha a conexão com o cliente atual, e o servidor volta a esperar por uma nova conexão com o `accept()`.

![image](https://github.com/user-attachments/assets/cb3e0e92-e149-43f4-a0e4-54fac2a4401b)

### Cliente (clientsocketTCP.py)

- **Estabelecendo a Conexão**: A principal diferença no cliente TCP é o uso de `clientSocket.connect()`. Este comando inicia o processo de "handshake" de três vias para estabelecer uma conexão formal com o servidor antes que qualquer dado seja trocado.

![image](https://github.com/user-attachments/assets/521c4756-678d-4fcf-b3c8-9562356d7939)

- **Comunicação**: Uma vez conectado, o cliente usa `send()` e `recv()` para trocar dados com o servidor de forma confiável. O RTT é calculado da mesma forma que no UDP, medindo o tempo entre o envio de uma mensagem e o recebimento da resposta.

![image](https://github.com/user-attachments/assets/8a4a36b3-95eb-44b4-b2dc-d7b446f8f8bc)

- **Encerramento**: Ao final do processo, `clientSocket.close()` encerra a conexão com o servidor.

![image](https://github.com/user-attachments/assets/73676ffa-b1d4-4fd2-9c2a-dbfe1dfd9d1c)


## Análise da Implementação

### Comunicação com UDP
A implementação UDP demonstra a natureza **não confiável** e sem conexão do protocolo. Foi necessário implementar um mecanismo de **timeout** no lado do cliente para lidar com a possibilidade de pacotes perdidos, um cenário comum em UDP. É um protocolo rápido, ideal para aplicações onde a velocidade é mais crítica que a garantia de entrega (como streaming de vídeo ou jogos online).

### Comunicação com TCP
A versão TCP mostra um protocolo **confiável** e orientado à conexão. O "handshake" inicial (`connect` e `accept`) estabelece um canal de comunicação seguro. A entrega de pacotes é garantida e ordenada pelo próprio protocolo, eliminando a complexidade de tratar perdas na aplicação. É a escolha padrão para aplicações onde a integridade dos dados é essencial (como transferência de arquivos, e-mails e navegação na web).

