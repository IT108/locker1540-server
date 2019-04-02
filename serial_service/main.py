import serial
import serial_service.constants as constants
import serial_service.operations as operations
ser = serial.Serial()


def start_serial():
    ser.port = constants.serial_name
    ser.baudrate = constants.rate
    try:
        ser.open()
        main()
    except Exception:
        return False


def main():
    while 1:
        if ser.in_waiting > 0:
            req = ser.readline().decode('utf-8')
            operation = req[req.find('[') + 1:req.find(']')]
            data = req[req.find(']') + 1:req.find('\r\n')]
            data = format_data(data)
            if operations == 'stop':
                exit(0)
            res = operations.run_operation(operation, data)
            ser.write(res)
            operations.play_queue()


def format_data(data):
    res = {}
    data = str(data)
    data = data.split(',')
    for a in data:
        a = a.split(':')
        res[a[0]] = res[a[1]]
    return res
