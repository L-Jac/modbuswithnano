from pymodbus.server import ModbusSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# 创建数据存储区
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),
    co=ModbusSequentialDataBlock(0, [17]*100),
    hr=ModbusSequentialDataBlock(0, [17]*100),
    ir=ModbusSequentialDataBlock(0, [17]*100))

# 创建服务器上下文
context = ModbusServerContext(slaves=store, single=True)

serial1 = "dev/ttyS0"
serial2 = "COM7"
# 创建服务器
server = ModbusSerialServer(context, port=serial1, baudrate=115200)

# 启动服务器
server.serve_forever()

from pymodbus.server import ModbusSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# 创建数据存储区
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),
    co=ModbusSequentialDataBlock(0, [17]*100),
    hr=ModbusSequentialDataBlock(0, [17]*100),
    ir=ModbusSequentialDataBlock(0, [17]*100))

# 创建服务器上下文
context = ModbusServerContext(slaves=store, single=True)

# 创建服务器
server = ModbusSerialServer(context, port='/dev/ttyS0', baudrate=115200)

# 启动服务器
server.serve_forever()

