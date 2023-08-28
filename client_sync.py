#!/usr/bin/env python3

from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import (
    ModbusRtuFramer,
    ModbusSocketFramer,
)


def run_client(port, baud_rate, order, value=None, framer=ModbusSocketFramer):

    pymodbus_apply_logging_config("DEBUG")

    print("连接客户端")

    client = ModbusSerialClient(
        port,
        framer=ModbusRtuFramer,
        # timeout=10,
        # retries=3,
        # retry_on_empty=False,
        # close_comm_on_error=False,
        # strict=True,
        baudrate=baud_rate,
        bytesize=8,
        parity="E",
        stopbits=1,
        # handle_local_echo=False,
    )

    print("连接服务器")
    client.connect()

    print("获取并验证数据")
    if order == "read":
        try:

            result = client.read_holding_registers(1, 1, slave=1)
            # 第一个参数是要读取的寄存器的地址，第二个参数是要读取的寄存器的数量，第三个参数是从属设备的地址。
        except ModbusException as exc:
            print(f"收到 ModbusException 异常{exc}")
            client.close()
            return
        if result.isError():  # pragma no cover
            print(f"收到Modbus 异常({result})")
            client.close()
            return
        if isinstance(result, ExceptionResponse):  # pragma no cover
            print(f"收到Modbus 异常({result})")
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            client.close()
    elif order == "write":
        client.write_register(1, value, unit=1)
        # 第一个参数是要写入的寄存器的地址，第二个参数是要写入的值，第三个参数是从属设备的地址
    else:
        print("无效命令")

    print("关闭客户端")
    client.close()


serial1 = "dev/ttyS0"
serial2 = "COM7"
command = "read"
if __name__ == "__main__":
    run_client(serial2, 115200, command)
