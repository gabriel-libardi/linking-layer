import socket
import random


byte_size = 8


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

"""
Primeiro particionamos a mensagem para esta ser transmitida
em quadros de 1500 bits, como no protocolo Ethernet de legado.
Implementaremos CRC-32, bit de paridade par e bit de paridade
ímpar em cada quadro, então cada quadro terá 1466 bits de dados.
Os outros campos de um quadro transmitido por Ethernet serão
omitidos desta simulação, pois estes seriam redundantes
(esses seriam os 64 bits de preâmbulo, o endereço de destino e o
endereço de origem).
"""
def CamadaDeEnlace(frame_bits:bytes):
    frame_data_length = 1466     # 1466 bits de dados por frame
    frames = []                  # Array de frames a serem transmitidos.

    for frame in frames:
        # Passa o quadro para a camada física, na qual a transmissão acontece.
        MeioDeComunicacao(frame)

"""
O meio de comunicação é simulado com uma unix socket padrão, a qual 
não geraria nenhum erro de transmissão. Para se obter erros de transmissão
esperados nessa capada, foi inserido um erro aleatório: um bit pode ser
flipado com 1% de chance. Essa chance é muito grande comparada aos guias
de onda para os quais o protocolo de enquadramento usado é feito, mas ajuda
a ilustrar o funcionamento dos algoritmos de detecção de erros.
"""
def MeioDeComunicacao(frame:bytearray):
    # Simular erro aleatório do meio físico de transmissão
    if random.randint(0, 100) == 42:
        bit_flipped = random.randint(0, 1499)     # Um dos 1500 bits é invertido
        index = bit_flipped//byte_size            # Byte cujo bit é invertido
        bit_position = 7 - bit_flipped%byte_size  # Posição do bit a inverter

        frame[index] ^= 1 << bit_position         # Inverte o bit

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as medium:
            medium.connect(('localhost', 58763))
            medium.sendall(frame)
        except Exception as e:
            print(f"Problem ocurred during transmission: {e}")


if __name__ == '__main__':
    main()