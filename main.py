"""
TODO: Übergabe der Grenzwerte aus IDs.py implementieren.
"""

# import pyvisa
import time
import argparse

from numpy import int16, uint16
from geraete import classes,IDs
import csv
from datetime import datetime
from pymodbus.client.serial import ModbusSerialClient
from pcb_constants import PCB_MODBUS_PARAMETERS, PCB_MB_REGISTERS, PCB_PARAM, PCB_REG_NAME_TO_ADDRESS, PCB_REG_ADRESS_TO_NAME, PCB_NAME_MULT

hw_variants = [
    "S1_Pos",
    "S1_Neg",
    "S2_Pos", 
    "S2_Neg",
]

CURRENT_SETPOINTS = []

dmm = classes.rigol_dmm(IDs.RIGOL_DMM_IP)
dmm.setup()
ps = classes.ea_ps(IDs.EA_PS_IP,IDs.EA_PS_PORT)
ps.setup()
el = classes.ea_el(IDs.EA_EL_IP,IDs.EA_EL_PORT)
el.setup()
pcbClient = ModbusSerialClient(
    port=PCB_MODBUS_PARAMETERS['USBPort'], 
    baudrate=PCB_MODBUS_PARAMETERS['baudrate'], 
    bytesize=PCB_MODBUS_PARAMETERS['bytesize'], 
    parity=PCB_MODBUS_PARAMETERS['parity'], 
    stopbits=PCB_MODBUS_PARAMETERS['stopbits'], 
    timeout=PCB_MODBUS_PARAMETERS['timeout']
    )
pcbClient.connect()

def float_to_uint16(value: float) -> uint16:
    if value >= 0:
        x = round(value/(PCB_PARAM["RANGE"]/(PCB_PARAM["ADC_RES_HALF"]-1)))
    else:
        x = (value + 2*PCB_PARAM["RANGE"]) / (PCB_PARAM["RANGE"]/PCB_PARAM["ADC_RES_HALF"])    
    x = uint16(x)
    return x

def wait_for_user_confirmation(message: str):
    while True:
        print("\n" + message)
        answer = input("Please confirm switch configuration. [y/n]: ").strip().lower()
        if answer == "y":
            return
        elif answer == "n":
            print("Please change hardware configuration and confirm.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def get_current_key(hw_variant:str, set_current:float) ->str:
    if hw_variant.startswith("S1"):
        stack = "S1"
    elif hw_variant.startswith("S2"):
        stack = "S2"
    else:
        raise ValueError(f"Invalid hw_variant: {hw_variant}")
    level = "low" if set_current < 10.0 else "high"
    return f"Current_{level}_{stack}"

def output_off_zero():
    """ Turn off all appliances safely. """
    ps.write_scpi("OUTP OFF")
    time.sleep(5) # wait for power supply to discharge
    el.write_scpi("INP OFF")
    ps.preset_zero()
    el.preset_zero()

def run_test_cycle(
        testpoints_ampere:list[float],
        hw_variant:str="S1_Pos",
        dwell_s:float=3.0,
        sample_per_point:int=10,
        sample_interval_s:float=0.5,
        export_csv_path=None
    ): 
    """
    Run a test cycle with given testpoints in ampere. Timestamp, set current, measured voltage and calculated current are recorded and returned. CSV Export ist possible. 
    
    :param testpoints_ampere: Testpoints in ampere limited to electronic load current limits. 
    :type testpoints_ampere: list[float]
    :param dwell_s: Time to dwell on each testpoint in seconds
    :type dwell_s: float
    :param sample_per_point: Number of samples to take per testpoint
    :type sample_per_point: int
    :param sample_interval_s: Time interval between samples in seconds
    :type sample_interval_s: float
    :param export_csv_path: Path to export CSV file, or None to skip export
    :type export_csv_path: str | None
    """
    results = []
    pcb_mean_values = []
    ref_mean_values = []
    mb_reg_start = PCB_REG_NAME_TO_ADDRESS["Voltage_S1"]
    mb_reg_end = PCB_REG_NAME_TO_ADDRESS["Voltage_ocv"]
    mb_reg_count = mb_reg_end - mb_reg_start + 1
    first = True

    # Set electronic load to max power to avoid power limit issues
    el.set_curr(el.CURR_MAX)
    el.set_pow(el.POW_MAX)
    # Set power supply to max power to avoid power limit issues
    ps.set_volt(ps.VOLT_MAX)
    ps.set_pow(ps.POW_MAX)
    

    for set_current in testpoints_ampere:  
        
        current_key = get_current_key(hw_variant, set_current)
        # samples = {
        #    "calc_current_a": [],
        #     current_key: [] 
        # }
        samples_pcb_current = []
        samples_ref_current = []
        # load defines maximum current
        if set_current < 0 or set_current > el.CURR_MAX:
            set_current = 0 if set_current < 0 else el.CURR_MAX
        ps.set_curr(set_current)
        if first:
            time.sleep(1)
            el.write_scpi("INP ON")
            ps.write_scpi("OUTP ON")
            first = False
        time.sleep(dwell_s)
        for _ in range(sample_per_point):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            meas_volt = dmm.meas_volt_dc()
            calc_curr = meas_volt / PCB_PARAM["R_SHUNT"]
            read_reg_values = pcbClient.read_holding_registers(address=mb_reg_start, count=mb_reg_count, device_id=PCB_MODBUS_PARAMETERS['devId'])
            values = read_reg_values.registers
            modbus_values = {}
            for address in range(mb_reg_start, mb_reg_end + 1):
                reg_mult = PCB_MB_REGISTERS[address].get("multiplicator")
                reg_name = PCB_MB_REGISTERS[address].get("name")
                reg_value = int16(uint16(values[address - mb_reg_start]))*reg_mult # type: ignore
                modbus_values[reg_name] = reg_value

            row = {
                "timestamp": ts,
                "set_current_a": f"{set_current:.2f}",
                "meas_voltage_v": f"{meas_volt:.7f}",
                "calc_current_a": f"{calc_curr:.7f}",
            }
            row.update(modbus_values)
            results.append(row)
            samples_ref_current.append(calc_curr)
            samples_pcb_current.append(modbus_values[current_key])

            print(f"{ts} | set {set_current:.2f} A | U = {meas_volt:.7f} V | I = {calc_curr:.5f} A")
            time.sleep(sample_interval_s)
        
        means = my_mean(samples_ref_current)
        ref_mean_values.append(means)
        means = my_mean(samples_pcb_current)
        pcb_mean_values.append(means)

    ref_values = ref_mean_values + pcb_mean_values 
    output_off_zero()
    if export_csv_path:
        fieldnames = ["timestamp", "set_current_a", "meas_voltage_v", "calc_current_a"]
        fieldnames.extend(modbus_values.keys())
        with open(export_csv_path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(results)
    return results, ref_values

def my_mean(values:list[float]) -> float:
    return sum(values)/len(values) if values else 0.0

def run_sweep(
        curr_start:float=0,
        curr_end:float=10,
        step_curr:float=1.0,
        volt_start:float=0,
        volt_end:float=10,
        step_volt:float=1.0,
        export_csv_path=None):
    """
    Run sweep with given current and voltage ranges. If no value is given run standard sweep. Timestamp, set and measured values are recorded and returned. CSV Export ist possible.
    
    :param curr_start: Current start value in Ampere
    :type curr_start: float
    :param curr_end: Current end value in Ampere
    :type curr_end: float
    :param step_curr: Current step between two setpoints in Ampere
    :type step_curr: float
    :param volt_start: Voltage start value in Volt
    :type volt_start: float
    :param volt_end: Voltage end value in Volt
    :type volt_end: float
    :param step_volt: Voltage step between two setpoints in Volt
    :type step_volt: float
    :param export_csv_path: Path to export CSV file, or None to skip export
    :type export_csv_path: str | None
    """
    results = []
    testpoints_amp = []
    testpoints_volt = []
    first = True
    set_curr_el = el.set_curr(curr_end)
    set_pow_el = el.set_pow(el.POW_MAX)
    set_pow_ps = ps.set_pow(el.POW_MAX)

    current = curr_start
    if curr_start < 0:
        curr_start = 0
    if curr_end > ps.CURR_MAX:
        curr_end = ps.CURR_MAX
    if step_curr != 0:
        while current <= curr_end:
            testpoints_amp.append(round(current, 2))
            current += step_curr
    else:
        testpoints_amp.append(round(curr_start, 2))

    voltage = volt_start
    if volt_start < 0:
        volt_start = 0
    if volt_end > ps.VOLT_MAX:
        volt_end = ps.VOLT_MAX
    if step_volt != 0:    
        while voltage <= volt_end:
            testpoints_volt.append(round(voltage, 2))
            voltage += step_volt
    else:
        testpoints_volt.append(round(volt_start, 2))

    

    for a_setpoint in testpoints_amp:
        set_curr_ps = ps.set_curr(a_setpoint)
        if first:
            time.sleep(1)
            el.write_scpi("INP ON")
            ps.write_scpi("OUTP ON")
            first = False
        for v_setpoint in testpoints_volt:
            # power = a_setpoint * v_setpoint + 20
            # if power > el.POW_MAX:
            #     power = el.POW_MAX
            set_volt_ps = ps.set_volt(v_setpoint)
            # set_pow_ps = ps.set_pow(2400)
            # set_pow_el = el.set_pow(2400)
            time.sleep(1) # wait for settings to be safe
            el.write_scpi("INP ON")
            ps.write_scpi("OUTP ON")
            time.sleep(1)
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            row = {
                "timestamp": ts,
                "set_curr_ps": set_curr_ps,
                "set_volt_ps": set_volt_ps,
                "set_pow_ps": set_pow_ps,
                "set_curr_el": set_curr_el,
                "set_pow_el": set_pow_el,
                "meas_curr_ps": ps.meas_curr(),
                "meas_volt_ps": ps.meas_volt(),
                "meas_pow_ps": ps.meas_pow(),
                "meas_curr_el": el.meas_curr(),
                "meas_volt_el": el.meas_volt(),
                "meas_pow_el": el.meas_pow(),
            }
            results.append(row)
            print(f"sweep in progress | {ts} | I_set {a_setpoint:.2f} A | U_set = {set_volt_ps:.7f} V")
    output_off_zero()
    if export_csv_path:
        fieldnames = [
            "timestamp",
            "set_curr_ps", "set_volt_ps", "set_pow_ps",
            "set_curr_el", "set_pow_el",
            "meas_curr_ps", "meas_volt_ps", "meas_pow_ps",
            "meas_curr_el", "meas_volt_el", "meas_pow_el",
        ]
        with open(export_csv_path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(results)

    return results
            
def parse_args():
    parser = argparse.ArgumentParser(
        description="SCPI Test- und Sweep-Tool"
    )

    subparsers = parser.add_subparsers(dest="mode", required=True)

    # -------- Sweep --------
    sweep = subparsers.add_parser("sweep", help="Strom/Spannungs-Sweep")
    sweep.add_argument("--curr-start", type=float, default=0)
    sweep.add_argument("--curr-end", type=float, default=120)
    sweep.add_argument("--step-curr", type=float, default=20)
    sweep.add_argument("--volt-start", type=float, default=40)
    sweep.add_argument("--volt-end", type=float, default=40)
    sweep.add_argument("--step-volt", type=float, default=0)

    # -------- Test Cycle --------
    cycle = subparsers.add_parser("cycle", help="Testzyklus")
    cycle.add_argument(
        "--testpoints",
        type=float,
        nargs="+",
        required=True,
        help="Strom-Testpunkte in Ampere"
    )
    cycle.add_argument("--dwell", type=float, default=3.0)
    cycle.add_argument("--samples", type=int, default=10)
    cycle.add_argument("--interval", type=float, default=0.5)

    return parser.parse_args()

def ref_to_pcb(start_adress:int, values:list[uint16]):
    pcbClient.write_registers(address=start_adress, values=values, device_id=PCB_MODBUS_PARAMETERS['devId'])
    return 0

def run_test_with_user_steps():

    for run_index, variant in enumerate(hw_variants, start=1):
        print(f"\n===== TESTCYCLE {run_index}/4 =====")

        wait_for_user_confirmation(variant)

        run_test_cycle(
            testpoints_ampere=[10, 20],
            hw_variant=variant,
            dwell_s=2.0,
            sample_per_point=3,
            sample_interval_s=3.0,
            export_csv_path=f"test_cycle_run_{hw_variants[run_index-1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )


def main():
    # args = parse_args()

    dmm.write_scpi("MEAS MANU")
    dmm.write_scpi("MEAS:VOLT:DC 0")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        # if args.mode == "cycle":
        #     run_test_cycle(
        #         testpoints_ampere=args.testpoints,
        #         dwell_s=args.dwell,
        #         sample_per_point=args.samples,
        #         sample_interval_s=args.interval,
        #         export_csv_path=f"test_cycle_results_{timestamp}.csv"
        #     )
        # elif args.mode == "sweep":
        #     run_sweep(
        #         curr_start=args.curr_start,
        #         curr_end=args.curr_end,
        #         step_curr=args.step_curr,
        #         volt_start=args.volt_start,
        #         volt_end=args.volt_end,
        #         step_volt=args.step_volt,
        #         export_csv_path=f"sweep_{timestamp}.csv"
        #     )
        # """
        
        # run_test_with_user_steps()
        
        x,y = run_test_cycle(
            testpoints_ampere=[10, 20],
            # testpoints_ampere=[0, 40, 80, 120],
            dwell_s=2.0,
            sample_per_point=1,
            sample_interval_s=3.0,
            export_csv_path=f"test_cycle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        ref_values = []
        for i in range(len(y)):
            ref_values.append(float_to_uint16(y[i]))
        
        ref_to_pcb(PCB_REG_NAME_TO_ADDRESS["S1_PCB_Value_1"], ref_values)
        ref_values_read = pcbClient.read_holding_registers(address=PCB_REG_NAME_TO_ADDRESS["S1_PCB_Value_1"], count=len(ref_values), device_id=PCB_MODBUS_PARAMETERS['devId'])
        ref_values_read = ref_values_read.registers
        print("Reference values written to PCB and read back:")
        for i in range(len(ref_values)):
            print(f"Ref {y[i]:.7f} A -> UInt16: {ref_values[i]} -> Read back: {ref_values_read[i]}")
            
        # run_sweep(
        #     curr_start=0,
        #     curr_end=120,
        #     step_curr=20,
        #     volt_start=40,
        #     volt_end=40,
        #     step_volt=0,
        #     export_csv_path=f"sweep_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        # )
        # """
                
        # for r in y:
        #     print(f"Referenzwerte @ {r} A:")
        #     for k, v in y[r].items():
        #         print(f"  {k}: {v:.6f}")

    finally:
        output_off_zero()
        time.sleep(1)
        ps.close()
        el.close()
        dmm.close()



if __name__ == "__main__":
    main()

