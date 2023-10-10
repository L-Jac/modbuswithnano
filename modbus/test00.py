import serial
import time
ser = serial.Serial(
    port='COM3',  # 串口号，根据实际情况修改
    baudrate=9600,        # 波特率
)
# b'\x01\x03\x00\x09\x00\x01\x84\x0a'
message = [0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x84, 0x09]


while True:
    time.sleep(1)
    print("write")
    # b = message.encode("utf-8")
    b = bytes(message)
    ser.write(b)
