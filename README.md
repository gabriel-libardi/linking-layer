# Linking Layer

Simulação da camada de enlace usando unix sockets. Esse trabalho é de autoria do grupo:
- Gabriel Franceschi Libardi - NUSP: 11760739
- Mateus Santos Messias - NUSP: 12548000
- Guilherme Castanon Silva Pereira - NUSP: 1801140
- Matheus Pereira Dias - NUSP: 11207752

Para executar o código, primeiro coloque execute a aplicação receptora:

```
python3 src_getmsg/main.py
```

Agora configure a variável global error_type para escolher o tipo de 
problema na camada física de transmissão:
- error_type = 0: Erro na CRC-32 em Lorem Ipsum.
- error_type = 1: Erro na paridade de bit par
- error_type = 2: Erro na paridade de bit ímpar em lorem ipsum
- error_type = 3: 1% de chance de se flipar um bit da mensagem

Por fim, rode a aplicação transmissora com o seguinte código:
```
python3 src_transmit/main.py
```