import serial
import constants
import operations
ser = serial.Serial()


def start_serial():
    ser.port = constants.serial_name
    ser.baudrate = constants.rate
    try:
        ser.open()
    except Exception as e:
        print(e)
        print("something went wrong")
        return False
    main()


def main():
    while 1:
        if ser.in_waiting > 0:
            req = ser.readline().decode('utf-8')
            operation = req[req.find('[') + 1:req.find(']')]
            data = req[req.find(']') + 1:req.find('\r\n')]
            data = format_data(data)
            if operation == 'stop':
                exit(0)
            res = operations.run_operation(operation, data)
            ser.write(res.encode('utf-8'))
            operations.play_queue()


def format_data(data):
    res = {}
    data = str(data)
    data = data.split(',')
    for a in data:
        a = a.split(':')
        print(a)
        res[a[0]] = a[1]
    return res


start_serial()
