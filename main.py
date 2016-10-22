import time
import bluetooth
from client import ThreadedClient


def main():
    msg = message(b'\x18',[b'\x00'])
    print(msg)
    client = ThreadedClient()
    client.message.write.append(msg)
    time.sleep(10)
    client.close()


def message(command, parameters):
    header = b'\xFB\xBF'
    end = b'\xED'
    parameter = b''.join(parameters)
    # len(header + length + command +parameters + check)
    length = len(parameters) + 5
    min_parameter = min([ord(x) for x in parameters])
    check = bytes([sum([ord(command), length, min_parameter])])
    return header+bytes([length])+command+parameter+check+end

if __name__ == '__main__':
    main()
