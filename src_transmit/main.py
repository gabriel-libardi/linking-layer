


def main():
    # Main apenas chama a aplicação transmissora
    AplicacaoTransmissora()


def AplicacaoTransmissora():
    # Usuário passa a mensagem a ser transmitida
    message = input("Digite a sua mensagem: ")

    # Chama a próxima camada
    CamadaDeAplicacaoTransmissora(message)


def CamadaDeAplicacaoTransmissora(message:str):
    # Converte a string para um array de bytes.
    # Mas vamos trabalhar com a mensagem bit a bit.
    frame_bits = message.encode()
    print(frame_bits)

    # Passa os bits a serem transmitidos para a camada de Enlace
    CamadaDeEnlace(frame_bits)


def CamadaDeEnlace()


if __name__ == '__main__':
    main()