import time
from numpy import int16, uint16
import pymodbus.client
# from pymodbus.client.sync import ModbusSerialClient
# from pymodbus.client import ModbusSerialClient
from pymodbus.client.serial import ModbusSerialClient
from pcb_constants import PCB_MODBUS_PARAMETERS, PCB_MB_REGISTERS, PCB_REG_NAME_TO_ADDRESS, PCB_REG_ADRESS_TO_NAME


MbRegisterNames = ["U_stack",
    "I_high1",
    "I_low1",
    "U_stack2",
    "I_high2",
    "I_low2",
    "U_ocv",
    "U_ocv2"]

unidAddr = 10
mb_reg_start = PCB_REG_NAME_TO_ADDRESS["Voltage_S1"]
mb_reg_end = PCB_REG_NAME_TO_ADDRESS["Voltage_ocv"]
mb_reg_count = mb_reg_end - mb_reg_start + 1

#client = ModbusClient(method='ascii', port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
client = ModbusSerialClient(port='COM10', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

client.connect()
if client.connected:
    print("Modbus connected")

while True:
    # client.write_registers(50, [0,1,2,3,4,5,6,7,8,9], device_id=unidAddr)  # Beispiel: Schreibe 1 in Register 50 und 0 in Register 51
    # read = client.read_holding_registers(address=50, count=10, device_id=unidAddr)
    # if not read.isError():
    #     for r in read.registers:
    #         print(r)
    #     time.sleep(2)
    # client.write_registers(50, [9,8,7,6,5,4,3,2,1,0], device_id=unidAddr)  
    # read = client.read_holding_registers(address=50, count=10, device_id=unidAddr)
    # if not read.isError():
    #     for r in read.registers:
    #         print(r)
    #     time.sleep(2)

    read_reg_values = client.read_holding_registers(address=mb_reg_start, count=mb_reg_count, device_id=unidAddr)
    if not read_reg_values.isError():
        values = read_reg_values.registers
        for address in range(mb_reg_start, mb_reg_end + 1):
            reg_name = PCB_REG_ADRESS_TO_NAME[address]
            reg_mult = PCB_MB_REGISTERS[address].get("multiplicator")
            reg_value = int16(uint16(values[address - mb_reg_start]))
            reg_value = reg_value * reg_mult # type: ignore
            print(f"Register {reg_name} (Addr {address})(Mult {reg_mult}): {reg_value:.4f}")
        time.sleep(2)

    # read=client.read_holding_registers(address = 11, count = 8, device_id=unidAddr)
    # if not read.isError():
    #     s = ''
    #     for r in read.registers:
    #                       s+=f"{MbRegisterNames[read.registers.index(r)]}: {r} "
    #     print(s)
    #     time.sleep(2)
    #     for data in read.registers:
    #                print(data) #printing value read in above line

    else:
        print("error: {}".format(read_reg_values))
        exit()     
