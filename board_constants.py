#Variables for initialization of Modbus communication with measurement PCB

BOARD_MODBUS_PARAMETERS  = {
    'USBPort' : 'COM10',
    'devId' : 11,
    'baudrate' : 115200,
    'bytesize' : 8,
    'parity' : 'N',
    'stopbits' : 1,
    'timeout' : 1}

BOARD_PARAM = {
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


FACTORS = {
"Voltage_S1": (2*BOARD_PARAM["R1"]/BOARD_PARAM["R2"]),
    "Current_high_S1": 1/BOARD_PARAM["GAIN_AMP_1"]/BOARD_PARAM["R_SHUNT"]*BOARD_PARAM["U_REF"]/BOARD_PARAM["ADC_RES_HALF"],
    "Current_low_S1": 1/BOARD_PARAM["GAIN_AMP_2"]/BOARD_PARAM["R_SHUNT"]*BOARD_PARAM["U_REF"]/BOARD_PARAM["ADC_RES_HALF"],
    "Voltage_S2": (2*BOARD_PARAM["R1"]/BOARD_PARAM["R2"]),
    "Current_high_S2": 1/BOARD_PARAM["GAIN_AMP_1"]/BOARD_PARAM["R_SHUNT"]*BOARD_PARAM["U_REF"]/BOARD_PARAM["ADC_RES_HALF"],
    "Current_low_S2": 1/BOARD_PARAM["GAIN_AMP_2"]/BOARD_PARAM["R_SHUNT"]*BOARD_PARAM["U_REF"]/BOARD_PARAM["ADC_RES_HALF"],
    "Voltage_ocv": BOARD_PARAM["U_REF"]/BOARD_PARAM["ADC_RES_HALF"],
    "Temp" : 1
}


# for r in FACTORS:
#     print(f"Multiplication Factor {r} = {FACTORS[r]}")

BOARD_MB_REGISTERS = [
    {"name": "FW_Vers_Number", "address": 0, "factor" : 1},
    {"name": "MB_Vers_Number", "address": 1, "factor" : 1},
    {"name": "unused", "address": 2, "factor" : 1},
    {"name": "unused", "address": 3, "factor" : 1},
    {"name": "unused", "address": 4, "factor" : 1},
    {"name": "MB_Heartbeat", "address": 5, "factor" : 1},
    {"name": "unused", "address": 6,    "factor" : 1},
    {"name": "unused", "address": 7, "factor" : 1},
    {"name": "unused", "address": 8, "factor" : 1},
    {"name": "unused", "address": 9, "factor" : 1},
    
    {"name": "Voltage_S1", "address": 10, "factor" : FACTORS["Voltage_S1"]},
    {"name": "Current_high_S1", "address": 11, "factor" : FACTORS["Current_high_S1"]},
    {"name": "Current_low_S1", "address": 12, "factor" : FACTORS["Current_low_S1"]},
    {"name": "Voltage_S2", "address": 13, "factor" : FACTORS["Voltage_S2"]},
    {"name": "Current_high_S2", "address": 14, "factor" : FACTORS["Current_high_S1"]},
    {"name": "Current_low_S2", "address": 15, "factor" : FACTORS["Current_low_S2"]},
    {"name": "Voltage_ocv", "address": 16, "factor" : FACTORS["Voltage_ocv"]},
    
    {"name": "unused", "address": 17, "factor" : 1},
    #------------------------------------------------#
    # Number of Temp sensors varies, adjust if needed
    {"name": "Temp1_Bank1", "address": 18, "factor" : FACTORS["Temp"]},
    {"name": "Temp2_Bank1", "address": 19, "factor" : FACTORS["Temp"] },
    {"name": "Temp3_Bank1", "address": 20, "factor" : FACTORS["Temp"]},
    {"name": "Temp4_Bank1", "address": 21, "factor" : FACTORS["Temp"]},
    {"name": "Temp5_Bank1", "address": 22, "factor" : FACTORS["Temp"]},
    {"name": "Temp6_Bank1", "address": 23, "factor" : FACTORS["Temp"]},

    {"name": "Temp1_Bank2", "address": 24, "factor" : FACTORS["Temp"]},
    {"name": "Temp2_Bank2", "address": 25, "factor" : FACTORS["Temp"]},
    {"name": "Temp3_Bank2", "address": 26, "factor" : FACTORS["Temp"]},
    {"name": "Temp4_Bank2", "address": 27, "factor" : FACTORS["Temp"]},
    {"name": "Temp5_Bank2", "address": 28, "factor" : FACTORS["Temp"]},
    {"name": "Temp6_Bank2", "address": 29, "factor" : FACTORS["Temp"]},

    {"name": "Temp1_Bank3", "address": 30, "factor" : FACTORS["Temp"]},
    {"name": "Temp2_Bank3", "address": 31, "factor" : FACTORS["Temp"]},
    {"name": "Temp3_Bank3", "address": 32, "factor" : FACTORS["Temp"]},
    {"name": "Temp4_Bank3", "address": 33, "factor" : FACTORS["Temp"]},
    {"name": "Temp5_Bank3", "address": 34, "factor" : FACTORS["Temp"]},
    {"name": "Temp6_Bank3", "address": 35, "factor" : FACTORS["Temp"]},

    {"name": "Temp1_Bank4", "address": 36, "factor" : FACTORS["Temp"]},
    {"name": "Temp2_Bank4", "address": 37, "factor" : FACTORS["Temp"]},
    {"name": "Temp3_Bank4", "address": 38, "factor" : FACTORS["Temp"]},
    {"name": "Temp4_Bank4", "address": 39, "factor" : FACTORS["Temp"]},
    {"name": "Temp5_Bank4", "address": 40, "factor" : FACTORS["Temp"]},
    {"name": "Temp6_Bank4", "address": 41, "factor" : FACTORS["Temp"]},

    {"name": "unused", "address": 42, "factor" : 1},
    {"name": "unused", "address": 43, "factor" : 1},
    {"name": "unused", "address": 44, "factor" : 1},
    {"name": "unused", "address": 45, "factor" : 1},
    {"name": "unused", "address": 46, "factor" : 1},
    {"name": "unused", "address": 47, "factor" : 1},
    {"name": "unused", "address": 48, "factor" : 1},
    {"name": "MB_CURRENT_CALIBRATED", "address": 49, "factor" : 1},

    {"name": "S1_PCB_Value_1", "address": 50, "factor" : 1},
    {"name": "S1_ref_Value_1", "address": 51, "factor" : 1},
    {"name": "S1_PCB_Value_2", "address": 52, "factor" : 1},
    {"name": "S1_ref_Value_2", "address": 53, "factor" : 1},
    {"name": "S1_PCB_Value_3", "address": 54, "factor" : 1},
    {"name": "S1_ref_Value_3", "address": 55, "factor" : 1},
    {"name": "S1_PCB_Value_4", "address": 56, "factor" : 1},
    {"name": "S1_ref_Value_4", "address": 57, "factor" : 1},
    {"name": "S1_PCB_Value_5", "address": 58, "factor" : 1},
    {"name": "S1_ref_Value_5", "address": 59, "factor" : 1},
    {"name": "S1_PCB_Value_6", "address": 60, "factor" : 1},
    {"name": "S1_ref_Value_6", "address": 61, "factor" : 1},
    {"name": "S1_PCB_Value_7", "address": 62, "factor" : 1},
    {"name": "S1_ref_Value_7", "address": 63, "factor" : 1},

    {"name": "S2_PCB_Value_1", "address": 64, "factor" : 1},
    {"name": "S2_ref_Value_1", "address": 65, "factor" : 1},
    {"name": "S2_PCB_Value_2", "address": 66, "factor" : 1},
    {"name": "S2_ref_Value_2", "address": 67, "factor" : 1},
    {"name": "S2_PCB_Value_3", "address": 68, "factor" : 1},
    {"name": "S2_ref_Value_3", "address": 69, "factor" : 1},
    {"name": "S2_PCB_Value_4", "address": 70, "factor" : 1},
    {"name": "S2_ref_Value_4", "address": 71, "factor" : 1},
    {"name": "S2_PCB_Value_5", "address": 72, "factor" : 1},
    {"name": "S2_ref_Value_5", "address": 73, "factor" : 1},
    {"name": "S2_PCB_Value_6", "address": 74, "factor" : 1},
    {"name": "S2_ref_Value_6", "address": 75, "factor" : 1},
    {"name": "S2_PCB_Value_7", "address": 76, "factor" : 1},
    {"name": "S2_ref_Value_7", "address": 77, "factor" : 1},

]

# print(fPOARDCB_MB_REGISTERS[5].get("factor")},POARDCB_MB_REGISTERS[5].get("name")},POARDCB_MB_REGISTERS[5].get("address")}")

BOARD_NAME_FACTOR = {reg["name"]:reg["factor"] for reg in BOARD_MB_REGISTERS}
# for r in BOARD_NAME_FACTOR:
#     print(f"{r}, {BOARD_NAME_FACTOR[r]}")

BOARD_REG_NAME_TO_ADDRESS = {reg["name"]: reg["address"] for reg in BOARD_MB_REGISTERS}

# for r in BOARD_REG_NAME_TO_ADDRESS:
#     print(f"{r}, {BOARD_REG_NAME_TO_ADDRESS[r]}")

BOARD_REG_ADRESS_TO_NAME = {reg["address"]: reg["name"] for reg in BOARD_MB_REGISTERS}

# for r in BOARD_REG_ADRESS_TO_NAME:
#     print(f"{r}, {BOARD_REG_ADRESS_TO_NAME[r]}")
