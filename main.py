import datetime as dt
import socket
import serial

filename = "program"
SET_PROGRAM = b'set_program'

DAYS = 1
HOURS = 2
MINUTES = 3
TS_STATE = 4
SETTED_T = 5
LIGHT_STATE = 8
LIGTH_R = 10
LIGTH_G = 11
LIGTH_B = 12


class Connecter():
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10001)

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
            index = dt.datetime.strptime(text[0], "%Y-%m-%d %H-%M")
            index_next = dt.datetime.strptime(text_next[0], "%Y-%m-%d %H-%M")
            if index.timestamp() < dt.datetime.now().timestamp() < index_next.timestamp():
                print(text[1])
                return text[1]

    @staticmethod
    def write_program(data: list):
        program = ""
        next_timedelta = dt.timedelta()
        last_duration = None
        for item in data:
            if item and item != SET_PROGRAM:
                separated_items = item.decode().split(";")

                phase = ""

                # Початок виконання фази
                duration = dt.datetime.now()
                duration += next_timedelta

                phase += duration.strftime("%Y-%m-%d %H-%M") + "; "

                # Збереження часу початку останньої фази для розрахунку часу кінця програми
                last_duration = duration

                # Час закінчення виконання фази
                next_timedelta += dt.timedelta(days=int(separated_items[DAYS]))
                next_timedelta += dt.timedelta(hours=int(separated_items[HOURS]))
                next_timedelta += dt.timedelta(minutes=int(separated_items[MINUTES]))

                phase += separated_items[TS_STATE] + "; "
                phase += separated_items[SETTED_T] + "; "
                phase += separated_items[LIGHT_STATE] + "; "
                phase += separated_items[LIGTH_R] + "; "
                phase += separated_items[LIGTH_G] + "; "
                phase += separated_items[LIGTH_B] + ";\n"

                program += phase

        # записування кінця виконання програми
        program += (last_duration + next_timedelta).strftime("%Y-%m-%d %H-%M") + "; end_program;"

        # запис програми в файл
        with open(filename, "w") as f:
            f.write(program)

    def send_data(self):
        pass
        self.serial(set_data=True, data=self.parser())

    def do(self):
        connection, client_address = self.sock.accept()
        try:
            while True:
                data = connection.recv(2048)
                separated_data = data.split(b"\n")
                if separated_data[0] == SET_PROGRAM:
                    self.write_program(separated_data)

                if data:
                    # d = self.serial()
                    # print(separated_data)
                    # connection.sendall(d)
                    # print(f'::: {data.decode()}')
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





