import pyvisa
import time

from geraete import ps, el, IDs
# from geraete import el
# from geraete import IDs

# explizit pyvisa-py Backend benutzen
rm = pyvisa.ResourceManager('@py')

def main():
    rm = pyvisa.ResourceManager('@py')
    resource = f"TCPIP0::192.168.0.103::INSTR"
    print("Opening Connection...")
    dmm = rm.open_resource(resource)
    dmm.timeout = 5000
    dmm.write_termination = '\n'
    dmm.read_termination = '\n'
    time.sleep(2)
    print("ID:",dmm.query("*IDN?"))
    # print("ID:",dmm.query("UTIL:INTE:LAN:IP?"))
    # print("ID:",dmm.query("UTIL:INTE:LAN:MASK?"))
    dmm.write("MEAS:VOLT:DC 1")

    i = 0
    new_meas = False

    while i < 10:
        new_meas = dmm.query("MEAS?")
        print(new_meas)
        if new_meas == 'TRUE':
            print("Voltage:", dmm.query("MEAS:VOLT:DC?"))
        else:
            time.sleep(1)
        i += 1
    
    print("Programm beendet...")
    

main()


