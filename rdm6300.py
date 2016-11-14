import serial
# RDM6300 module
#  _____________________________________________
#  |0x02| DATA(10 ascii chars) | CHECKSUM | 03 |
#  =============================================
# params: 96008n1

class RDM6300:
    SERIAL_PORT = ''
    BAUDRATE = 9600

    RDM_START = 2
    RDM_END = 3
    RDM_DATA_SZ = 20

    def __init__(self, serial_port):
        self.SERIAL_PORT = serial_port

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

        if int(ord(byte_read)) != self.RDM_START:
            return False

        expected_len = 12
        while expected_len is not 0:

            expected_len -= 1
            byte_read = serial_connection.read()

            if int(ord(byte_read)) == self.RDM_START:
                expected_len = 12
                continue

            if ord(byte_read) != self.RDM_END:
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
            serial_connection = serial.Serial(self.SERIAL_PORT, baudrate=self.BAUDRATE)

            while True:
                data = self.__read_sequence(serial_connection)

                if data is False:
                    continue

                print data

                serial_connection.flushInput()

        except KeyboardInterrupt:
            print "\nKilled. Serial port was safely closed."
            serial_connection.close()

if __name__ == "__main__":
    rdm6300_reader = RDM6300('/dev/ttyS0')
    rdm6300_reader.do_work()