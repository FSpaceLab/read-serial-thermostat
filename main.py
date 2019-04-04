
import socket
import serial


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
        # self.ser = serial.Serial('COM6', 9600)

    def serial(self, set_data=False, data=''):
        if not set_data:
            self.ser.reset_input_buffer()
            return self.ser.readline().decode()

        elif set_data and data:
            self.ser.write(data.encode())

    def get_data(self):
        pass

    def set_data(self):
        pass

    def parser(self, data):
        pass

    def do(self):
        connection, client_address = self.sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    connection.sendall(self.parser(data).encode())
                    print(f'::: {data.decode()}')

                    # print('sending data back to the client')
                    # connection.sendall(serial_data.encode())
                    # connection.sendall("response".encode())
                else:
                    break

        finally:
            # Clean up the connection
            connection.close()





if __name__ == "__main__":
    connecter = Connecter()
    while True:
        connecter.do()


