#### Modbus Rtu Python实现  
##### 库
：pyserial， pymodbus
##### 基本串口测试  
test00.py 发送信息  
test01.py 接收信息  
##### Modbus实现
client_sync.py 同步客户端（主站）  
server_async.py 异步服务器（从站）  
test_sync.py 测试程序，检查服务器能否正常连接  
parity="E"，采用偶校验