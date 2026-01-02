# import pyvisa
import time
from geraete import classes,IDs
import csv
from datetime import datetime

shunt_resistance = 0.0001  # Ohm

dmm = classes.rigol_dmm(IDs.RIGOL_DMM_IP)
dmm.setup()
ps = classes.ea_ps(IDs.EA_PS_IP,IDs.EA_PS_PORT)
ps.setup()
el = classes.ea_el(IDs.EA_EL_IP,IDs.EA_EL_PORT)
el.setup()    

def run_test_cycle(
        testpoints_ampere,
        dwell_s:float=3.0,
        sample_per_point:int=10,
        sample_interval_s:float=0.5,
        export_csv_path=None
    ):
    results = []
    for set_current in testpoints_ampere:
        ps.set_curr(set_current)
        ps.set_volt(ps.VOLT_MAX)
        ps.set_pow(set_current*ps.VOLT_MAX+20)
        el.set_curr(set_current)
        el.set_pow(set_current*ps.VOLT_MAX+20)
        time.sleep(1) # wait for settings to be safe
        el.write_scpi("INP ON")
        ps.write_scpi("OUTP ON")
        time.sleep(dwell_s)
        for _ in range(sample_per_point):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            meas_volt = dmm.meas_volt_dc()
            calc_curr = meas_volt / shunt_resistance
            row = {
                "timestamp": ts,
                "set_current_a": f"{set_current:.2f}",
                "meas_voltage_v": f"{meas_volt:.7f}",
                "calc_current_a": f"{calc_curr:.7f}",
            }
            results.append(row)
            print(f"{ts} | set {set_current:.2f} A | U = {meas_volt:.7f} V | I = {calc_curr:.5f} A")
            time.sleep(sample_interval_s)

    ps.write_scpi("OUTP OFF")
    el.write_scpi("INP OFF")
    ps.preset_zero()
    el.preset_zero()
    if export_csv_path:
        fieldnames = ["timestamp", "set_current_a", "meas_voltage_v", "calc_current_a"]
        with open(export_csv_path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(results)
    return results


def main():
    dmm.write_scpi("MEAS MANU")
    dmm.write_scpi("MEAS:VOLT:DC 0")

    try:
        run_test_cycle(
            testpoints_ampere=[10, 20, 30, 40],
            dwell_s=2.0,
            sample_per_point=3,
            sample_interval_s=1.0,
            export_csv_path="test_cycle_results.csv"
    )
    finally:
        ps.write_scpi("OUTP OFF")
        ps.preset_zero()
        ps.close()
        el.write_scpi("INP OFF")
        el.preset_zero()
        el.close()
        dmm.close()

'''''       
    # print("Set Power:", el.set_pow(100))
    # el.write_scpi("INP ON")

    # print("Set Current:", ps.set_curr(1))
    # print("Set Voltage:", ps.set_volt(40))
    # print("Set Power:", ps.set_pow(100))
    # ps.write_scpi("OUTP ON")
    # i = 0

    # for i in range(10):
    #     meas_volt = dmm.query_scpi("MEAS:VOLT:DC?")
    #     calc_curr = float(meas_volt)*shunt_resistance
    #     print("Voltage:", meas_volt)
    #     print("Current:", calc_curr)
    #     time.sleep(1)
    #     i += 1 

    while True:
        meas_volt = dmm.meas_volt_dc()
        calc_curr = float(meas_volt)/shunt_resistance
        print(f"Voltage: {float(meas_volt):.7f} V")
        print(f"Voltage: {float(meas_volt)*1000:.3f} mV")
        print(f"Current: {calc_curr:.4f} A")
        time.sleep(3)
'''


if __name__ == "__main__":
    main()

