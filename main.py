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
    
    # Set electronic load to max power to avoid power limit issues
    set_curr_el = el.set_curr(el.CURR_MAX)
    set_pow_el = el.set_pow(el.POW_MAX)
    # Set power supply to max power to avoid power limit issues
    set_volt_ps = ps.set_volt(ps.VOLT_MAX)
    set_pow_ps = ps.set_pow(ps.POW_MAX)


    for set_current in testpoints_ampere:
        first = True
        # Last gibt Maximalwerte vor
        if set_current < 0 or set_current > el.CURR_MAX:
            set_current = 0 if set_current < 0 else el.CURR_MAX
        ps.set_curr(set_current)
        # ps.set_volt(ps.VOLT_MAX)
        # if set_current * ps.VOLT_MAX + 20 > el.POW_MAX:
        #     ps.set_pow(el.POW_MAX)
        # else:
        #     ps.set_pow(set_current*ps.VOLT_MAX+20)
        
        # el.set_curr(set_current)
        # if set_current * el.VOLT_MAX + 20 > el.POW_MAX:
        #     el.set_pow(el.POW_MAX)
        # else:
        #     el.set_pow(set_current*el.VOLT_MAX+20)
         # wait for settings to be safe
        if first:
            time.sleep(1)
            el.write_scpi("INP ON")
            ps.write_scpi("OUTP ON")
            first = False
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
    time.sleep(5) # wait for power supply to discharge
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

def run_sweep(
        curr_start:float=0,
        curr_end:float=10,
        step_curr:float=1.0,
        volt_start:float=0,
        volt_end:float=10,
        step_volt:float=1.0,
        export_csv_path=None):
    results = []
    testpoints_amp = []
    testpoints_volt = []

    set_curr_el = el.set_curr(curr_end)
    set_pow_el = el.set_pow(2400)
    set_pow_ps = ps.set_pow(2400)

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
    ps.write_scpi("OUTP OFF")
    time.sleep(5) # wait for power supply to discharge
    el.write_scpi("INP OFF")
    ps.preset_zero()
    el.preset_zero()
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
        
    

def main():
    dmm.write_scpi("MEAS MANU")
    dmm.write_scpi("MEAS:VOLT:DC 0")

    try:
        # run_test_cycle(
        #     testpoints_ampere=[10, 20, 30, 40],
        #     dwell_s=2.0,
        #     sample_per_point=3,
        #     sample_interval_s=1.0,
        #     export_csv_path=f"test_cycle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        # )
        run_sweep(
            curr_start=0,
            curr_end=120,
            step_curr=20,
            volt_start=40,
            volt_end=40,
            step_volt=0,
            export_csv_path=f"sweep_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
    finally:
        ps.write_scpi("OUTP OFF")
        ps.preset_zero()
        time.sleep(1)
        ps.close()
        time.sleep(5) # wait for power supply to discharge
        el.write_scpi("INP OFF")
        el.preset_zero()
        time.sleep(1)
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

