import serial
import crcmod
import time
import struct
from modbus_tk import modbus_rtu


# CRC16校验，返回整型数
def crc16(data):
    if not data:
        return
    crc16_return = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    return crc16_return(data)


# 校验数据帧的CRC码是否正确
def checkcrc(data):
    if not data:
        return False
    if len(data) <= 2:
        return False
    nocrcdata = data[:-2]
    oldcrc16 = data[-2:]
    oldcrclist = list(oldcrc16)
    crcres = crc16(nocrcdata)
    crc16byts = crcres.to_bytes(2, byteorder="little", signed=False)
    # print("CRC16:", crc16byts.hex())
    crclist = list(crc16byts)
    if oldcrclist[0] != crclist[0] or oldcrclist[1] != crclist[1]:
        return False
    return True


# Modbus-RTU协议的03或04读取保存或输入寄存器功能
# 主->从命令帧
def modbus_master(server, start, number_read, function_code=3):
    # 判断从站地址是否超限，开始寄存器地址是否超限，寄存器个数是否超限，功能号是否正确
    if server < 0 or server > 0xFF or start < 0 or start > 0xFFFF or number_read < 1 or number_read > 0x7D:
        print("Error: parameter error")
        return
    if function_code != 3 and function_code != 4:
        print("Error: parameter error")
        return
    message = (server.to_bytes(1, byteorder="big", signed=False) +
               function_code.to_bytes(1, byteorder="big", signed=False) +
               start.to_bytes(2, byteorder="big", signed=False) +
               number_read.to_bytes(2, byteorder="big", signed=False))
    crc_check = crc16(message)
    crc16_bytes = crc_check.to_bytes(2, byteorder="little", signed=False)
    message_send = message + crc16_bytes
    return message_send


# Modbus-RTU协议的03或04读取保持或输入寄存器功能
# 从->主的数据帧解析（浮点数2,1,4,3格式，16位短整形（定义正负数））
def modbus_server(data_back, value_format=1, mod=False):
    # value_format:寄存器中值的格式，
    # 0代表用2个寄存器4个字节表示一个单精度浮点数，
    # 1代表1个寄存器（2字节）存放1个16位整形值，
    # mod：当寄存器数据值格式是整形时，true则按照有符号整形转换，false则按无符号整形转换。
    if not data_back:
        print("Error: data error")
        return
    if not checkcrc(data_back):
        print("Error: crc error")
        return
    data_list = list(data_back)
    if data_list[1] != 0x3 and data_list[1] != 0x4:
        print("Error: recv data function_code error")
        return
    byte_nums = data_list[2]
    if byte_nums % 2 != 0:
        print("Error: recv data reg data error")
        return
    data_return = []
    if value_format == 0:
        float_nums = byte_nums / 4
        print("float nums: ", str(float_nums))
        float_list = [0, 0, 0, 0]
        for i in range(int(float_nums)):
            float_list[1] = data_list[3 + i * 4]
            float_list[0] = data_list[4 + i * 4]
            float_list[3] = data_list[5 + i * 4]
            float_list[2] = data_list[6 + i * 4]
            byte_float_data = bytes(float_list)
            [fvalue] = struct.unpack('f', byte_float_data)
            data_return.append(fvalue)
            print(f'Data{i + 1}: {fvalue:.3f}')
    elif value_format == 1:
        int_nums = byte_nums / 2
        print("short int nums: ", str(int_nums))
        for i in range(int(int_nums)):
            temp = data_back[3 + i * 2:5 + i * 2]
            value_short = int.from_bytes(temp, byteorder="big", signed=mod)
            data_return.append(value_short)
            print(f"Data{i + 1}: {value_short}")
    return data_return


if __name__ == '__main__':
    slave = 8
    begin = 0
    number = 40
    send_data = modbus_master(slave, begin, number)
    print("send data : ", send_data.hex())
    serial_master = serial.Serial("/dev/ttyS1", 115200, timeout=0.8, bytesize=8, parity='E', stopbits=1)
    start_time = time.time()
    serial_master.write(send_data)
    recv_data = serial_master.read(number * 2 + 5)
    end_time = time.time()
    if len(recv_data) > 0:
        print("recv: ", recv_data.hex())
    print(f"used time: {end_time - start_time:.3f}")
    serial_master.close()
    modbus_server(recv_data)
