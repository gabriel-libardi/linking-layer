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

    # Verificar erros de transmissão da camada física
    for frame in frames:
        if not CheckEvenBitParity(frame):
            raise RuntimeError("Paridade de bit par está inconsistente")

        elif not CheckOddBitParity(frame):
            raise RuntimeError("Paridade de bit ímpar está inconsistente")
            
        elif not CheckCRC32(frame):
            raise RuntimeError("Teste de CRC-32 está inconsistentes")
        
        message_bits += frame[:-5]
    
    # Remover o código de controle e outros trailing zeros
    ff_index = message_bits.find(b"\xff")
    if ff_index != -1:
        message_bits = message_bits[:ff_index]

    # Retorna os bits da mensagem para a camada de aplicacao:
    return message_bits


def CheckEvenBitParity(frame) -> bool:
    # Calcula a paridade dos bits pares no array:
    parity = 0
    
    for byte in range(len(frame)):
        for shift in range(byte_size):
            parity ^= (~frame[byte] >> shift)%2
    
    # Verifica se a paridade de bits pares está consistente
    passed_test = (parity == (frame[-1] >> 6)%2)
    return passed_test


def CheckOddBitParity(frame) -> bool:
    # Calcula a paridade dos bits ímpares no array:
    parity = 0
    
    for byte in range(len(frame) - 1):
        for shift in range(byte_size):
            parity ^= (frame[byte] >> shift)%2
    
    # Verifica se a paridade de bits ímpares está consistente
    passed_test = (parity == (frame[-1] >> 7)%2)
    return passed_test


def CheckCRC32(frame) -> bool:
    # Verifica se CRC-32 do frame está consistente
    checkcrc = frame[-5:-1]
    frame[-5:-1] = "\b00"*4
    current_crc = bytearray(struct.pack('>I', binascii.crc32(frame[0:-1])))

    # Verificar se os dois são os mesmos
    passed_test = (checkcrc == current_crc)
    return passed_test


def MeioDeComunicacao() -> list:
    # Esse programa recebe os quadros da camada física
    frames = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as medium:
        medium.bind(('localhost', 58763))
        medium.listen()

        while True:
            connection, addr = medium.accept()
            with connection:
                frame = connection.recv(188)
                frames.append(frame)

                if b"\xff" in frame:
                    break
    
    return frames


if __name__ == '__main__':
    AplicacaoReceptora()