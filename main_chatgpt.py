import time
from datetime import datetime
import csv
from geraete import classes, IDs

shunt_resistance = 0.0001  # Ohm

dmm = classes.rigol_dmm(IDs.RIGOL_DMM_IP)
dmm.setup()
el = classes.ea_el(IDs.EA_EL_IP, IDs.EA_EL_PORT)
el.setup()
el.write_scpi("INP ON")

# ps = classes.ea_ps(IDs.EA_PS_IP, IDs.EA_PS_PORT)
# ps.setup()

def measure_voltage():
    return float(dmm.query_scpi("MEAS:VOLT:DC?"))


def run_test_cycle(
    points_a,
    dwell_s=3.0,
    samples_per_point=1,
    sample_interval_s=0.5,
    export_csv_path=None,
):
    results = []
    for set_current in points_a:
        el.set_curr(set_current)
        time.sleep(dwell_s)
        for _ in range(samples_per_point):
            ts = datetime.now().isoformat(timespec="seconds")
            meas_volt = measure_voltage()
            calc_curr = meas_volt / shunt_resistance
            row = {
                "timestamp": ts,
                "set_current_a": set_current,
                "meas_voltage_v": meas_volt,
                "calc_current_a": calc_curr,
            }
            results.append(row)
            print(
                f"{ts} | set {set_current:.2f} A | "
                f"U={meas_volt:.7f} V | I={calc_curr:.4f} A"
            )
            if samples_per_point > 1:
                time.sleep(sample_interval_s)

    if export_csv_path:
        fieldnames = ["timestamp", "set_current_a", "meas_voltage_v", "calc_current_a"]
        with open(export_csv_path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    return results


def main():
    dmm.write_scpi("MEAS MANU")
    dmm.write_scpi("MEAS:VOLT:DC 0")

    points_a = [0, 40, 80, 120]
    run_test_cycle(points_a, dwell_s=3.0, export_csv_path="messungen.csv")


if __name__ == "__main__":
    try:
        main()
    finally:
        el.write_scpi("INP OFF")
        el.close()
        dmm.close()