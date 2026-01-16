# import pyvisa
import time
from geraete import classes,IDs
import csv
from datetime import datetime
from geraete.scpi_errors import SCPIError, SCPIErrorEntry, parse_scpi_error
# shunt_resistance = 0.0001  # Ohm

# dmm = classes.rigol_dmm(IDs.RIGOL_DMM_IP)
# dmm.setup()
# ps = classes.ea_ps(IDs.EA_PS_IP,IDs.EA_PS_PORT)
# ps.setup()
# el = classes.ea_el(IDs.EA_EL_IP,IDs.EA_EL_PORT)
# el.setup()

# ps.write_scpi("curr ")  # invalid command
# el.set_volt(24)  # invalid command
time.sleep(0.5)

tests = [
    # '0,"No error"',
    # '0,"No error"'
    '0 - No error',
    '-200,"Execution error"',
    '-200 - Execution error',
    '-200-Execution error',
    '-222 Data out of range',
    '0,"No error"',
    "0,No error",
    "0 - No error",
    "   0 - No error   ",
    '-200,"Execution error"',
    "-200,Execution error",
    "-200 - Execution error", 
    "-200-Execution error",
    "-222 Data out of range",
    # Nur Code (kommt selten vor, aber besser robust sein)
    "-113",
    # +Code (auch selten, aber parser kann's)
    "+100,Something"
    
]

for t in tests:
    print(t, "->", parse_scpi_error(t))