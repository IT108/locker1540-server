import serial
from console_service import constants

ser = serial.Serial()


def start_serial():
    ser.port = constants.telemetry_serial
    ser.baudrate = constants.telemetry_serial_rate
    try:
        ser.open()
        return True
    except Exception as e:
        print(e)
        print("something went wrong")
        return False


def request_status():
    res = constants.GET_STATUS_OPERATION + '\r\n'
    print(res)
    ser.write(res.encode('utf-8'))
