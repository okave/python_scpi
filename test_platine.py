import time
import pymodbus.client
# from pymodbus.client.sync import ModbusSerialClient
# from pymodbus.client import ModbusSerialClient
from pymodbus.client.serial import ModbusSerialClient

unidAddr = 11

#client = ModbusClient(method='ascii', port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
client = ModbusSerialClient(port='COM10', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

client.connect()

while True:
              #read=client.read_input_registers(address = 10, count = 7, unit=unidAddr) 
              read=client.read_holding_registers(address = 6, count = 22, device_id=unidAddr) 
              if not read.isError():
                            s = ''
                            for r in read.registers:
                                          s+=f"{r:6d} "
                            print(s)
                            time.sleep(0.5)
              #for data in read.registers:
              #            print(data) #printing value read in above line

              else:
                            print("error: {}".format(read))
                            exit()     
