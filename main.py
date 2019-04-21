from datetime import datetime
import socket
import serial

filename = "program"


class Connecter():
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)

        # Bind the socket to the port
        self.sock.bind(self.server_address)
        print('starting up on {} port {}'.format(*self.server_address))

        # Listen for incoming connections
        self.sock.listen(1)

        # Connect to Serial
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)


    def serial(self, set_data=False, data=''):
        if not set_data:
            data = self.ser.readline()
            self.ser.reset_input_buffer()
            return data

        elif set_data and data:
            self.ser.write(data.encode())

    def read_program(self):
        line_list = [line.rstrip('\n') for line in open(filename)]
        return line_list

    def get_data(self):
        pass

    def parser(self):
        p = self.read_program()
        p.reverse()
        len_p = len(p)

        while len_p:
            len_p -= 1
            text = p[len_p].split(":")
            text_next = p[len_p - 1].split(":")
            index = datetime.strptime(text[0], "%Y-%m-%d %H-%M")
            index_next = datetime.strptime(text_next[0], "%Y-%m-%d %H-%M")
            if index.timestamp() < datetime.now().timestamp() < index_next.timestamp():
                print(text[1])
                return text[1]

    def send_data(self):
        self.serial(set_data=True, data=self.parser())

    def do(self):
        connection, client_address = self.sock.accept()
        try:
            while True:
                data = connection.recv(2048)
                if data:
                    d = self.serial()
                    print(d)
                    connection.sendall(d)
                    print(f'::: {data.decode()}')
                    self.send_data()

                else:
                    break

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    connecter = Connecter()
    while True:
        connecter.do()





