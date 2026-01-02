import pyvisa
import time
from geraete import classes,IDs

# rm = pyvisa.ResourceManager('@py')

def main():
    # dmm = classes.rigol_dmm(IDs.RIGOL_DMM_IP)
    # time.sleep(2)
    # info = dmm.identify()
    # print(info)
    ps = classes.ea_ps(IDs.EA_PS_IP,IDs.EA_PS_PORT)
    # ps.setup()
    ps.preset_zero()
    print("Set current:", ps.query_scpi("CURR?"))
    print("Set voltage:", ps.query_scpi("VOLT?"))
    print("Set power:", ps.query_scpi("POW?"))
    ps.close()


    # el = classes.ea_el(IDs.EA_EL_IP,IDs.EA_EL_PORT)
    # el.set_curr(-1)
    # el.set_curr(10)
    # el.set_curr(1000)
    # el.close()

    print("Programm beendet...")
    

main()


