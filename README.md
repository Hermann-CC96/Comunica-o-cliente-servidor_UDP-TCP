# Projeto: Comunicação TCP Cliente-Servidor – PING/PONG com RTT

## 📌 Descrição

Este projeto consiste em dois programas simples escritos em Python, utilizando **sockets TCP**, para estabelecer uma comunicação entre um **servidor** e um **cliente**. O objetivo principal é:

- O **cliente** enviar mensagens do tipo `PING`.
- O **servidor** responder com mensagens do tipo `PONG`.
- O **cliente** medir o **RTT (Round Trip Time)** de cada requisição‑resposta.

Esse projeto é útil como um exercício prático para entender como funciona a comunicação em **redes TCP**, o conceito de **round trip time**, e o uso de **sockets** em Python.

---

## 📂 Estrutura do Projeto

```text
.
├── server.py    # Código do servidor TCP
└── client.py    # Código do cliente TCP
