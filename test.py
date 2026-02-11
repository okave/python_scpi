# import pyvisa
import time

from matplotlib.pylab import int16, uint16
from geraete import classes,IDs
import csv
from datetime import datetime
from geraete.scpi_errors import SCPIError, SCPIErrorEntry, parse_scpi_error
from pcb_constants import PCB_MB_REGISTERS, PCB_PARAM

# bits = 2**15
# bit_value_pos = 250/(bits-1)
# bit_value_neg = 250/bits

# # x = 9.88508549
# x = 250.0
def float_to_uint16(value: float) -> uint16:
    if value >= 0:
        x = round(value/(PCB_PARAM["RANGE"]/(PCB_PARAM["ADC_RES_HALF"]-1)))
    else:
        x = (value + 2*PCB_PARAM["RANGE"]) / (PCB_PARAM["RANGE"]/PCB_PARAM["ADC_RES_HALF"])    
    x = uint16(x)
    return x

# for r in range(-250,250,10):
#     print(f"Float {r} -> UInt16: {float_to_uint16(r)}")

# float_to_uint16(250.0)
# float_to_uint16(-250.0)
# float_to_uint16(-0.001)
# float_to_uint16(9.88508549)
# float_to_uint16(0.0)
# # float_to_uint16(1000.0)

# def my_mean(values:list[float]) -> float:
#     return sum(values)/len(values) if values else 0.0

# list_of_values = [1.0, 2.0, 3.0]
# print(my_mean(list_of_values))

x1 = {10: [10.1318359375, 9.886662600000001], 20: [20.34759521484375, 19.757816], -10: [-10.31494140625, -9.91457935], -20: [-20.51544189453125, -19.7805602]}
x2 = {10: [10.101318359375, 9.885281919999999], 20: [20.233154296875, 19.757605899999998], -10: [-10.25390625, -9.9086843], -20: [-20.3857421875, -19.780119799999998]}



x1_list = refs_sorted_to_u16_list(x1)
x2_list = refs_sorted_to_u16_list(x2)
print(x1_list)
print(x2_list)
x1 = sorted(x1)
print(x1)
x2 = sorted(x2.keys())
print(x2)