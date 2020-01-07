import serial
from console_service import constants
import operations, api_operations
ser = serial.Serial()
api_ser = serial.Serial()


def start_serial():
    ser.port = constants.serial_name
    ser.baudrate = constants.rate
    try:
        ser.open()
    except Exception as e:
        print(e)
        print("something went wrong")
        return False
    start_api_serial()


def start_api_serial():
    api_ser.port = constants.api_serial
    api_ser.baudrate = constants.api_rate
    try:
        api_ser.open()
    except Exception as e:
        print(e)
        print("api serial not opened, running without api serial")
    main()


def main():
    while 1:
        if ser.in_waiting > 0:
            req = ser.readline().decode('utf-8')
            if req.find('[') == -1:
                print(req)
                pass
            req = separate_data(req)
            operation = req[0]
            data = req[1]
            data = format_data(data)
            if operation == 'stop':
                exit(0)
            res = operations.run_operation(operation, data)
            print(res.encode('utf-8'))
            ser.write(res.encode('utf-8'))
            operations.process_sounds(constants.sounds)
            operations.play_queue()
        if not api_ser:
            pass
        if api_ser.in_waiting > 0:
            req = api_ser.readline().decode('utf-8')
            print(req)
            if req.find('[') == -1:
                print(req)
                pass
            req = separate_data(req)
            operation = req[0]
            data = req[1]
            data = format_data(data)
            if operation == 'stop':
                exit(0)
            res = api_operations.run_operation(operation, data)
            print(res.encode('utf-8'))
            ser.write(res.encode('utf-8'))
            operations.process_sounds(constants.sounds)
            operations.play_queue()


def format_data(data):
    res = {}
    data = str(data)
    data = data.split(',')
    if data[0] == '':
        return data
    for a in data:
        if len(a) > 0:
            a = a.split(':')
            print(a)
            res[a[0]] = a[1]
    return res


def separate_data(a):
    res = ['', '']
    res[0] = a[a.find('[') + 1:a.find(']')]
    res[1] = a[a.find(']') + 1:a.find('\r\n')]
    return res


start_serial()
