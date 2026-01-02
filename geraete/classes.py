import time
import pyvisa

class tcp_scpi_appliance:
    CURR_MAX = 0.00 # Ampere
    VOLT_MAX = 0.00 # Volt
    POW_MAX = 0.00 # Watt

    def __init__(self, ip:str, port:int | None = None, resource_template: str  | None = None):
        rm = pyvisa.ResourceManager('@py')
        if resource_template:
            resource = resource_template.format(ip=ip,port=port)
        else:
            resource = f"TCPIP::{ip}::{port}::SOCKET"
        print("Opening Connection...")
        try:
            self.inst = rm.open_resource(resource)
        except Exception as exc:
            raise ConnectionError(f"SCPI connect failed: {resource}") from exc
        self.inst.timeout = 5000
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        

    def write_scpi(self, command:str):
        self.inst.write(command)

    def read_scpi(self):
        return self.inst.read()

    def query_scpi(self, command:str):
        return self.inst.query(command)
    
    def identify(self):
        return self.inst.query("*IDN?")

    def set_curr(self, value:float):
        if 0 <= value <= self.CURR_MAX:
            self.inst.write(f"CURR {value}")
            return self.inst.query("CURR?")
        print("Current out of range. Range is 0 to ", self.CURR_MAX)
        return None

    def set_volt(self, value:float):
        if 0 <= value <= self.VOLT_MAX:
            self.inst.write(f"VOLT {value}")
            return self.inst.query("VOLT?")
        print("Voltage out of range. Range is 0 to ", self.VOLT_MAX)
        return None

    def set_pow(self, value:float):
        if 0 <= value <= self.POW_MAX:
            self.inst.write(f"POW {value}")
            return self.inst.query("POW?")
        print("Power out of range. Range is 0 to ", self.POW_MAX)
        return None
    
    def preset_zero(self):
        self.set_curr(0)
        self.set_volt(0)
        self.set_pow(0)
    
    def meas_volt_dc(self):
        return float(self.inst.query("MEAS:VOLT:DC?"))
    
    def close(self):
        self.inst.close()
  
class ea_ps(tcp_scpi_appliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 40.00 # Volt
    POW_MAX = 3000.00 # Watt

    def setup(self):
        print("ID:", self.inst.query("*IDN?"))
        self.inst.write("*RST")
        self.inst.write("SOUR:VOLT:LEV 0")
        print("Preset Voltage:", self.inst.query("SOUR:VOLT:LEV?"))
        self.inst.write("SOUR:CURR:LEV 0")
        print("Preset Current:", self.inst.query("SOUR:CURR:LEV?"))
        self.inst.write("SOUR:POW:LEV 0")
        print("Preset Power:", self.inst.query("SOUR:POW:LEV?"))
        self.inst.write("SYST:LOCK:STAT 1")
        time.sleep(1)
        print("Access: ", self.inst.query("SYST:LOCK:OWN?"))

class ea_el(tcp_scpi_appliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 80.00 # Volt
    POW_MAX = 2400.00 # Watt
    R_MIN = 5.00 # Ohm
    R_MAX = 100.00 # Ohm

    def setup(self):
        print("ID:", self.inst.query("*IDN?"))
        self.inst.write("*RST")
        time.sleep(1)
        print("Access: ", self.inst.query("SYST:LOCK:OWN?"))

class rigol_dmm(tcp_scpi_appliance):
    def __init__(self, ip:str):
        super().__init__(ip=ip, resource_template="TCPIP0::{ip}::INSTR")

    # def __init__(self, ip:str):
    #     rm = pyvisa.ResourceManager('@py')
    #     resource = f"TCPIP0::{ip}::INSTR"
    #     print("Opening Connection...")
    #     try:
    #         self.inst = rm.open_resource(resource)
    #         self.inst.timeout = 5000
    #         self.inst.write_termination = '\n'
    #         self.inst.read_termination = '\n'
    #     except Exception as exc:
    #         raise ConnectionError(f"SCPI connect failed: {resource}") from exc
    #     # resource = f"TCPIP0::192.168.0.103::INSTR"

    def setup(self):
        print("ID:", self.inst.query("*IDN?"))
        self.inst.write("*RST")
        time.sleep(1)
        print("Command Set:", self.inst.query("CMDset?"))
        print("SCPI Version:", self.inst.query("SYSTem:VERSion?"))


    def identify(self):
        return {
            "id": self.inst.query("*IDN?"),
            "ip": self.inst.query("UTIL:INTE:LAN:IP?"),
            "subnet_mask": self.inst.query("UTIL:INTE:LAN:MASK?"),
            "cmdset": self.inst.query("CMDset?"),
            "scpi_vers": self.inst.query("SYSTem:VERSion?")
        }
