import socket
import binascii
import struct


def AplicacaoReceptora():
    # Procedimento que representa a aplicacao receptora
    message = CamadaDeAplicacaoReceptora() # Recebe mensagem

    #Imprime mensagem
    print(f"Você recebeu a mensagem: {message}")


def CamadaDeAplicacaoReceptora() -> str:
    # Recebe os bits da mensagem da camada de enlace 
    # e a retorna pra aplicação:
    message = CamadeDeEnlace().decode('utf-8')

    # Retorna a string que corresponde a mensagem
    return message


def CamadaDeEnlace() -> bytearray:
    # Verifica se os bits recebidos são consistentes
    frames = MeioDeComunicacao()
    message_bits = bytearray(b"")

    for frame in frames:
        e1 = CheckEvenBitParity(frame)
        e2 = CheckOddBitParity(frame)
        e3 = CheckCRC32(frame)

        if e1:
            raise RuntimeError("Paridade de bit par está inconsistente")
        elif e2:
            raise RuntimeError("Paridade de bit ímpar está inconsistente")
        elif e3:
            raise RuntimeError("Teste de CRC-32 está inconsistentes")


def MeioDeComunicacao() -> list:





if __name__ == '__main__':
    AplicacaoReceptora()