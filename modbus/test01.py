"""
接收端nmap -p 22 192.168.2.0/24
"""
import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB1',  # 串口号，根据实际情况修改
    baudrate=9600,  # 波特率
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

while True:
    # print("get?")
    l = ser.read()
    if l:
        print(hex(l[0]))
    print("---------------------")

