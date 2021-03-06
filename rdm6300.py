import serial
# RDM6300 module
#  _____________________________________________
#  |0x02| DATA(10 ascii chars) | CHECKSUM | 03 |
#  =============================================
# params: 96008n1

from enum import Enum


class RdmHdr(Enum):
    start_offset = 2
    end_offset = 3
    data_size = 20


class Rdm6300:
    baud_rate = 9600

    def __init__(self, serial_port: str):
        self.serial_port = serial_port

    @staticmethod
    def __verify_checksum(data, checksum):
        try:
            result = int(data[0:2], 16) \
                     ^ int(data[2:4], 16) \
                     ^ int(data[4:6], 16) \
                     ^ int(data[6:8], 16) \
                     ^ int(data[8:10], 16)
            result = format(result, 'x')

        except ValueError:
            return False

        if result.lower() != checksum.lower():
            return False
        return True

    @staticmethod
    def __fix_zeros(data):
        return data.replace(' ', '0')

    def __read_sequence(self, serial_connection):
        tag_string = ''
        byte_read = serial_connection.read()

        if int(ord(byte_read)) != RdmHdr.start_offset:
            return False

        expected_len = 12
        while expected_len is not 0:

            expected_len -= 1
            byte_read = serial_connection.read()

            if int(ord(byte_read)) == RdmHdr.start_offset:
                expected_len = 12
                continue

            if ord(byte_read) != RdmHdr.end_offset:
                tag_string += chr(ord(byte_read))
                continue
            break

        data = tag_string[0:len(tag_string) - 2]
        checksum = tag_string[len(tag_string) - 2:len(tag_string)]
        checksum_ok = self.__verify_checksum(data, checksum)

        if not checksum_ok:
            return False
        return self.__fix_zeros(data)

    def do_work(self):
        serial_connection = ''
        try:
            serial_connection = serial.Serial(self.serial_port, baudrate=self.baud_rate)

            while True:
                data = self.__read_sequence(serial_connection)

                if data is False:
                    continue

                print(data)

                serial_connection.flushInput()

        except KeyboardInterrupt:
            print('Killed. Serial port was safely closed.')
            serial_connection.close()


if __name__ == '__main__':
    serial_port = '/dev/ttyS0'
    rdm6300_reader = Rdm6300(serial_port)
    rdm6300_reader.do_work()
