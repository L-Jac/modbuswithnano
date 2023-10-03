from pymodbus.client.serial import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer


def test_server():
    # 创建客户端
    client = ModbusSerialClient(port='COM7', framer=ModbusRtuFramer,
                                baudrate=115200,
                                bytesize=8,
                                parity="E",
                                stopbits=1,)

    # 连接到服务器
    client.connect()

    # 发送读取保持寄存器的请求
    result = client.read_holding_registers(1, 1, unit=1)

    # 检查响应
    if not result.isError():
        print('服务器正在运行并能够正常响应客户端的请求')
    else:
        print('服务器无法正常响应客户端的请求')

    # 关闭连接
    client.close()


test_server()
