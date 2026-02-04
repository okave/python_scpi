#Variables for initialization of Modbus communication with measurement PCB

PCB_MODBUS_PARAMETERS  = {
    'USBPort' : 'COM10',
    'devId' : 10,
    'baudrate' : 115200,
    'bytesize' : 8,
    'parity' : 'N',
    'stopbits' : 1,
    'timeout' : 1}
"""

PCB_MB_REGISTERS = {
    "FW_Vers_Number": 0,
    "MB_Vers_Number": 1,
    "MB_Heartbeat": 5,
    "Voltage_S1": 10,
    "Current_high_S1": 11,
    "Current_low_S1": 12,
    "Voltage_S2": 13,
    "Current_high_S2": 14,
    "Current_low_S2": 15,
    "Voltage_ocv": 16,
    #------------------------------------------------#
    # Number of Temp sensors varies, adjust if needed
    "Temp1_Bank1": 18,
    "Temp2_Bank1": 19,
    "Temp3_Bank1": 20,
    "Temp4_Bank1": 21,
    "Temp5_Bank1": 22,
    "Temp6_Bank1": 23,
    
    "Temp1_Bank2": 24,
    "Temp2_Bank2": 25,
    "Temp3_Bank2": 26,
    "Temp4_Bank2": 27,
    "Temp5_Bank2": 28,
    "Temp6_Bank2": 29,
    
    "Temp1_Bank3": 30,
    "Temp2_Bank3": 31,
    "Temp3_Bank3": 32,
    "Temp4_Bank3": 33,
    "Temp5_Bank3": 34,
    "Temp6_Bank3": 35,

    "Temp1_Bank4": 36,
    "Temp2_Bank4": 37,
    "Temp3_Bank4": 38,
    "Temp4_Bank4": 39,
    "Temp5_Bank4": 40,
    "Temp6_Bank4": 41,

}
"""
"""
 Modbus register mapping for the measurement PCB
PCB_MB_REGISTERS = {0: "FW_Vers_Number",
    1: "MB_Vers_Number",
    5: "MB_Heartbeat",
    10: "Voltage_S1",
    11: "Current_high_S1",
    12: "Current_low_S1",
    13: "Voltage_S2",
    14: "Current_high_S2",
    15: "Current_low_S2",
    16: "Voltage_ocv",
    #------------------------------------------------#
    # Number of Temp sensors varies, adjust if needed
    18: "Temp1_Bank1",
    19: "Temp2_Bank1",
    20: "Temp3_Bank1",
    21: "Temp4_Bank1",
    22: "Temp5_Bank1",
    23: "Temp6_Bank1",
    
    24: "Temp1_Bank2",
    25: "Temp2_Bank2",
    26: "Temp3_Bank2",
    27: "Temp4_Bank2",
    28: "Temp5_Bank2",
    29: "Temp6_Bank2",

    30: "Temp1_Bank3",
    31: "Temp2_Bank3",
    32: "Temp3_Bank3",
    33: "Temp4_Bank3",
    34: "Temp5_Bank3",
    35: "Temp6_Bank3",
    
    36: "Temp1_Bank4",
    37: "Temp2_Bank4",
    38: "Temp3_Bank4",
    39: "Temp4_Bank4",
    40: "Temp5_Bank4",
    41: "Temp6_Bank4",
}
"""

PCB_PARAM = {
    "R1" : 499.0,
    "R2" : 30.0, 
    "R_SHUNT" : 100.0e-6, #100 uOhm
    "GAIN_AMP_1" : 100.0, #V/V
    "GAIN_AMP_2" : 1000.0, #V/V
    "U_REF" : 2.5, #V
    "ADC_RES" : 2**16, #Bits
    "ADC_RES_HALF" : (2**16)/2 #Bits
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

# """
PCB_MB_REGISTERS = [
    {"name": "FW_Vers_Number", "address": 0, "multiplicator" : 1},
    {"name": "MB_Vers_Number", "address": 1, "multiplicator" : 1},
    {"name": "MB_Heartbeat", "address": 5, "multiplicator" : 1},
    {"name": "Voltage_S1", "address": 10, "multiplicator" : MULT_FACTORS["Voltage_S1"]},
    {"name": "Current_high_S1", "address": 11, "multiplicator" : MULT_FACTORS["Current_high_S1"]},
    {"name": "Current_low_S1", "address": 12, "multiplicator" : MULT_FACTORS["Current_low_S1"]},
    {"name": "Voltage_S2", "address": 13, "multiplicator" : MULT_FACTORS["Voltage_S2"]},
    {"name": "Current_high_S2", "address": 14, "multiplicator" : MULT_FACTORS["Current_high_S1"]},
    {"name": "Current_low_S2", "address": 15, "multiplicator" : MULT_FACTORS["Current_low_S2"]},
    {"name": "Voltage_ocv", "address": 16, "multiplicator" : MULT_FACTORS["Voltage_ocv"]},
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
]
# """

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
