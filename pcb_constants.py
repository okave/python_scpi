#Variables for initialization of Modbus communication with measurement PCB

PCB_MODBUS_PARAMETERS  = {
    'USBPort' : 'COM10',
    'devId' : 10,
    'baudrate' : 115200,
    'bytesize' : 8,
    'parity' : 'N',
    'stopbits' : 1,
    'timeout' : 1}

PCB_PARAM = {
    "R1" : 499.0,
    "R2" : 30.0, 
    "R_SHUNT" : 100.0e-6, #100 uOhm
    "GAIN_AMP_1" : 100.0, #V/V
    "GAIN_AMP_2" : 1000.0, #V/V
    "U_REF" : 2.5, #V
    "ADC_RES" : 2**16, #Bits
    "ADC_RES_HALF" : (2**16)/2, #Bits
    "RANGE" : 250.0 # A
}


MULT_FACTORS = {
    "Voltage_S1": (2*PCB_PARAM["R1"]/PCB_PARAM["R2"]),
    "Current_high_S1": 1/PCB_PARAM["GAIN_AMP_1"]/PCB_PARAM["R_SHUNT"]*PCB_PARAM["U_REF"]/PCB_PARAM["ADC_RES_HALF"],
    "Current_low_S1": 1/PCB_PARAM["GAIN_AMP_2"]/PCB_PARAM["R_SHUNT"]*PCB_PARAM["U_REF"]/PCB_PARAM["ADC_RES_HALF"],
    "Voltage_S2": (2*PCB_PARAM["R1"]/PCB_PARAM["R2"]),
    "Current_high_S2": 1/PCB_PARAM["GAIN_AMP_1"]/PCB_PARAM["R_SHUNT"]*PCB_PARAM["U_REF"]/PCB_PARAM["ADC_RES_HALF"],
    "Current_low_S2": 1/PCB_PARAM["GAIN_AMP_2"]/PCB_PARAM["R_SHUNT"]*PCB_PARAM["U_REF"]/PCB_PARAM["ADC_RES_HALF"],
    "Voltage_ocv": PCB_PARAM["U_REF"]/PCB_PARAM["ADC_RES_HALF"],
    "Temp" : 1
}


# for r in MULT_FACTORS:
#     print(f"Multiplication Factor {r} = {MULT_FACTORS[r]}")

PCB_MB_REGISTERS = [
    {"name": "FW_Vers_Number", "address": 0, "multiplicator" : 1},
    {"name": "MB_Vers_Number", "address": 1, "multiplicator" : 1},
    {"name": "unused", "address": 2, "multiplicator" : 1},
    {"name": "unused", "address": 3, "multiplicator" : 1},
    {"name": "unused", "address": 4, "multiplicator" : 1},
    {"name": "MB_Heartbeat", "address": 5, "multiplicator" : 1},
    {"name": "unused", "address": 6,    "multiplicator" : 1},
    {"name": "unused", "address": 7, "multiplicator" : 1},
    {"name": "unused", "address": 8, "multiplicator" : 1},
    {"name": "unused", "address": 9, "multiplicator" : 1},
    
    {"name": "Voltage_S1", "address": 10, "multiplicator" : MULT_FACTORS["Voltage_S1"]},
    {"name": "Current_high_S1", "address": 11, "multiplicator" : MULT_FACTORS["Current_high_S1"]},
    {"name": "Current_low_S1", "address": 12, "multiplicator" : MULT_FACTORS["Current_low_S1"]},
    {"name": "Voltage_S2", "address": 13, "multiplicator" : MULT_FACTORS["Voltage_S2"]},
    {"name": "Current_high_S2", "address": 14, "multiplicator" : MULT_FACTORS["Current_high_S1"]},
    {"name": "Current_low_S2", "address": 15, "multiplicator" : MULT_FACTORS["Current_low_S2"]},
    {"name": "Voltage_ocv", "address": 16, "multiplicator" : MULT_FACTORS["Voltage_ocv"]},
    
    {"name": "unused", "address": 17, "multiplicator" : 1},
    #------------------------------------------------#
    # Number of Temp sensors varies, adjust if needed
    {"name": "Temp1_Bank1", "address": 18, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp2_Bank1", "address": 19, "multiplicator" : MULT_FACTORS["Temp"] },
    {"name": "Temp3_Bank1", "address": 20, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp4_Bank1", "address": 21, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp5_Bank1", "address": 22, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp6_Bank1", "address": 23, "multiplicator" : MULT_FACTORS["Temp"]},

    {"name": "Temp1_Bank2", "address": 24, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp2_Bank2", "address": 25, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp3_Bank2", "address": 26, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp4_Bank2", "address": 27, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp5_Bank2", "address": 28, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp6_Bank2", "address": 29, "multiplicator" : MULT_FACTORS["Temp"]},

    {"name": "Temp1_Bank3", "address": 30, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp2_Bank3", "address": 31, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp3_Bank3", "address": 32, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp4_Bank3", "address": 33, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp5_Bank3", "address": 34, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp6_Bank3", "address": 35, "multiplicator" : MULT_FACTORS["Temp"]},

    {"name": "Temp1_Bank4", "address": 36, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp2_Bank4", "address": 37, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp3_Bank4", "address": 38, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp4_Bank4", "address": 39, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp5_Bank4", "address": 40, "multiplicator" : MULT_FACTORS["Temp"]},
    {"name": "Temp6_Bank4", "address": 41, "multiplicator" : MULT_FACTORS["Temp"]},

    {"name": "unused", "address": 42, "multiplicator" : 1},
    {"name": "unused", "address": 43, "multiplicator" : 1},
    {"name": "unused", "address": 44, "multiplicator" : 1},
    {"name": "unused", "address": 45, "multiplicator" : 1},
    {"name": "unused", "address": 46, "multiplicator" : 1},
    {"name": "unused", "address": 47, "multiplicator" : 1},
    {"name": "unused", "address": 48, "multiplicator" : 1},
    {"name": "unused", "address": 49, "multiplicator" : 1},

    {"name": "S1_PCB_Value_neg120A", "address": 50, "multiplicator" : 1},
    {"name": "S1_ref_Value_neg120A", "address": 51, "multiplicator" : 1},
    {"name": "S1_PCB_Value_neg80A", "address": 52, "multiplicator" : 1},
    {"name": "S1_ref_Value_neg80A", "address": 53, "multiplicator" : 1},
    {"name": "S1_PCB_Value_neg40A", "address": 54, "multiplicator" : 1},
    {"name": "S1_ref_Value_neg40A", "address": 55, "multiplicator" : 1},
    {"name": "S1_PCB_Value_0A", "address": 56, "multiplicator" : 1},
    {"name": "S1_ref_Value_0A", "address": 57, "multiplicator" : 1},
    {"name": "S1_PCB_Value_pos40A", "address": 58, "multiplicator" : 1},
    {"name": "S1_ref_Value_pos40A", "address": 59, "multiplicator" : 1},
    {"name": "S1_PCB_Value_pos80A", "address": 60, "multiplicator" : 1},
    {"name": "S1_ref_Value_pos80A", "address": 61, "multiplicator" : 1},
    {"name": "S1_PCB_Value_pos120A", "address": 62, "multiplicator" : 1},
    {"name": "S1_ref_Value_pos120A", "address": 63, "multiplicator" : 1},

    {"name": "S2_PCB_Value_neg120A", "address": 64, "multiplicator" : 1},
    {"name": "S2_ref_Value_neg120A", "address": 65, "multiplicator" : 1},
    {"name": "S2_PCB_Value_neg80A", "address": 66, "multiplicator" : 1},
    {"name": "S2_ref_Value_neg80A", "address": 67, "multiplicator" : 1},
    {"name": "S2_PCB_Value_neg40A", "address": 68, "multiplicator" : 1},
    {"name": "S2_ref_Value_neg40A", "address": 69, "multiplicator" : 1},
    {"name": "S2_PCB_Value_0A", "address": 70, "multiplicator" : 1},
    {"name": "S2_ref_Value_0A", "address": 71, "multiplicator" : 1},
    {"name": "S2_PCB_Value_pos40A", "address": 72, "multiplicator" : 1},
    {"name": "S2_ref_Value_pos40A", "address": 73, "multiplicator" : 1},
    {"name": "S2_PCB_Value_pos80A", "address": 74, "multiplicator" : 1},
    {"name": "S2_ref_Value_pos80A", "address": 75, "multiplicator" : 1},
    {"name": "S2_PCB_Value_pos120A", "address": 76, "multiplicator" : 1},
    {"name": "S2_ref_Value_pos120A", "address": 77, "multiplicator" : 1},

]

print(f"{PCB_MB_REGISTERS[5].get("multiplicator")}, {PCB_MB_REGISTERS[5].get("name")}, {PCB_MB_REGISTERS[5].get("address")}")

PCB_NAME_MULT = {reg["name"]:reg["multiplicator"] for reg in PCB_MB_REGISTERS}
# for r in PCB_NAME_MULT:
#     print(f"{r}, {PCB_NAME_MULT[r]}")

PCB_REG_NAME_TO_ADDRESS = {reg["name"]: reg["address"] for reg in PCB_MB_REGISTERS}

# for r in PCB_REG_NAME_TO_ADDRESS:
#     print(f"{r}, {PCB_REG_NAME_TO_ADDRESS[r]}")

PCB_REG_ADRESS_TO_NAME = {reg["address"]: reg["name"] for reg in PCB_MB_REGISTERS}

# for r in PCB_REG_ADRESS_TO_NAME:
#     print(f"{r}, {PCB_REG_ADRESS_TO_NAME[r]}")
