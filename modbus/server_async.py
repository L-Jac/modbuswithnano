import asyncio
from pymodbus.server import ModbusSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer


async def main():
    print("# 创建数据存储区")
    store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [17] * 100))

    print("# 创建服务器上下文")
    context = ModbusServerContext(slaves=store, single=True)

    serial1 = "/dev/ttyS1"
    serial2 = "COM7"
    print("# 创建服务器")
    server = ModbusSerialServer(context,
                                port=serial2,
                                framer=ModbusRtuFramer,
                                baudrate=115200,
                                bytesize=8,
                                parity="E",
                                stopbits=1,
                                )

    print("# 启动服务器")
    await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
