import socket
import random
import binascii
import struct


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
Primeiro particionamos a mensagem para ser transmitida
em quadros de 1498 bits, e usamos uma aproximação do protocolo de Ethernet.
Implementaremos CRC-32, bit de paridade par e bit de paridade
ímpar em cada quadro, então cada quadro terá 1464 bits de dados.
Os outros campos de um quadro transmitido por Ethernet serão
omitidos desta simulação, pois estes seriam redundantes
(esses seriam os 64 bits de preâmbulo, o endereço de destino e o
endereço de origem).
"""
def CamadaDeEnlace(frame_bits:bytes):
    frame_data_length = 1464     # 1464 bits de dados por frame
    frames = []                  # Array de frames a serem transmitidos.

    # Divide a mensagem em frames de 1498 bits
    frame_bits += b"\xff"        # Adiciona código de controle na mensagem
    bits_remaining = len(frame_bits)*byte_size
    frame_index = 0
    while bits_remaining > 0:
        frame = bytearray(b"\x00"*(frame_data_length//8 + 5))

        if bits_remaining//frame_data_length >= 1:
            frame[0:frame_data_length//8] = frame_bits[(frame_data_length//8)*frame_index:
                                                       (frame_data_length//8)*(frame_index + 1)]
            bits_remaining -= frame_data_length
            frame_index += 1
        
        else:
            frame[0:bits_remaining//8] = frame_bits[(frame_data_length//8)*frame_index:]
            bits_remaining = 0

        frames.append(frame)

    for frame in frames:
        # Append error correcting codes:
        frame = CRC32Check(frame)
        frame = OddBitParity(frame)
        frame = EvenBitParity(frame)

        # Passa o quadro para a camada física, na qual a transmissão acontece.
        MeioDeComunicacao(frame)


def CRC32Check(frame:bytearray) -> bytearray:
    # Calcula o código de detecção de erro CRC-32 de Ethernet.
    frame[-5:-1] = bytearray(struct.pack('>I', binascii.crc32(frame[0:-1])))

    # Retorna o frame para o procedimento da camada de enlace.
    return frame


def OddBitParity(frame:bytearray) -> bytearray:
    # Calcula a paridade dos bits ímpares noo array:
    parity = 0
    
    for byte in range(len(frame) - 1):
        for shift in range(byte_size):
            parity ^= (frame[byte] >> shift)%2
    
    # Penúltimo bit é de paridade ímpar
    frame[-1] ^= parity << 7 

    return frame   # Retorna quadro com checksum


def EvenBitParity(frame) -> bytearray:
    # Calcula a paridade dos bits pares no array:
    parity = 0
    
    for byte in range(len(frame)):
        for shift in range(byte_size):
            parity ^= (~frame[byte] >> shift)%2
    
    # Último bit é de paridade par
    frame[-1] ^= parity << 6

    return frame   # Retorna quadro com checksum


"""
O meio de comunicação é simulado com uma unix socket padrão, a qual 
não geraria nenhum erro de transmissão. Para se obter erros de transmissão
esperados nessa capada, foi inserido um erro aleatório: um bit pode ser
flipado com 1% de chance. Essa chance é muito grande comparada aos guias
de onda para os quais o protocolo de enquadramento usado é feito, mas ajuda
a ilustrar o funcionamento dos algoritmos de detecção de erros.
"""
def MeioDeComunicacao(frame:bytearray):
    """
    # Simular erro aleatório do meio físico de transmissão
    if random.randint(0, 100) == 42:
        bit_flipped = random.randint(0, 1497)     # Um dos 1498 bits é invertido
        index = bit_flipped//byte_size            # Byte cujo bit é invertido
        bit_position = 7 - bit_flipped%byte_size  # Posição do bit a inverter

        frame[index] ^= 1 << bit_position         # Inverte o bit
    """
    error_type = 0
    if error_type == 0:
        frame = ForceCRC32Error(frame)
    elif error_type == 1:
        frame = ForceEvenBitPartityError(frame)
    elif error_type == 2:
        frame = ForceOddBitParityError(frame)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as medium:
            medium.connect(('localhost', 58763))
            medium.sendall(frame)
    except Exception as e:
        print(f"Problem ocurred during transmission: {e}")


def ForceCRC32Error(frame):
    posicao = random.randint(0, len(frame) - 1)
    frame[posicao] ^= 0b10101100
    
    return frame


def ForceEvenBitParityError(frame):
    for _ in range(num_errors):
        byte_index = random.randint(0, len(frame) - 1)
        bit_index = random.randint(0, 7)
        frame[byte_index] ^= 1 << bit_index

    return frame

if __name__ == '__main__':
    main()