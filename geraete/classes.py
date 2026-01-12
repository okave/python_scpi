import time
import pyvisa
from geraete.scpi_errors import SCPIError, SCPIErrorEntry, parse_scpi_error
from pyvisa import MessageBasedResource


class TcpScpiAppliance:
    CURR_MAX = 0.00 # Ampere
    VOLT_MAX = 0.00 # Volt
    POW_MAX = 0.00 # Watt

    def __init__(self, ip:str, port:int | None = None, resource_template: str  | None = None):
        """
        Initialize a TcpScpiAppliance instance. 
        
        :param ip: IP address of the appliance.
        :type ip: str
        :param port: Port number of the appliance.
        :type port: int | None
        :param resource_template: Template for the resource string. If None, a default TCPIP template is used.
        :type resource_template: str | None
        """
#TODO: Check if works
        self.inst: MessageBasedResource
        rm = pyvisa.ResourceManager('@py')
        if resource_template:
            resource = resource_template.format(ip=ip,port=port)
        else:
            resource = f"TCPIP::{ip}::{port}::SOCKET"
        print("Opening Connection...")
# TODO: Check if works as intended with resource_pyclass
        try:
            if resource_template:
                self.inst = rm.open_resource(resource_name=resource,resource_pyclass=pyvisa.resources.TCPIPInstrument) 
            self.inst = rm.open_resource(resource_name=resource, resource_pyclass=pyvisa.resources.TCPIPSocket) # defeats the purpose? 
        except Exception as exc:
            raise ConnectionError(f"SCPI connect failed: {resource}") from exc
        self.inst.timeout = 5000
        self.inst.write_termination = '\n' 
        self.inst.read_termination = '\n'


    def query_error_line(self) -> str:
        """ Return the next error line from the SCPI error queue """
        return self.inst.query("ERR:NEXT?") 


    def read_error(self) -> list[SCPIErrorEntry]:
        """ Return the complete SCPI error queue as a list of SCPIErrorEntry."""
        errors: list[SCPIErrorEntry] = []
        while True:
            resp = self.query_error_line()
            try:
                entry = parse_scpi_error(resp)
            except SCPIError:
                errors.append(SCPIErrorEntry(-1, f"Unparseable error response: {resp.strip()}"))
                break

            if entry is None:
                break  
            errors.append(entry)
        return errors


    def check_and_print_errors(self, command: str | None = None, raise_on_error: bool = False):
        """
        Read SCPI error queue and throw SCPIError if raise_on_error. 
        
        :param command: Command after which errors are checked.
        :type command: str | None
        :param raise_on_error: If true, raise SCPIError-Excepetion on any error found.
        :type raise_on_error: bool
        :raises SCPIError: If raise_on_error is True and any error found.
        """
        errors = self.read_error()
        if not errors:
            return
        # header = f'[SCPI ERROR after "{command}"]' if command else "[SCPI ERROR]"
        # print(header)
        # for e in errors:
        #     print(f"  {e.code}: {e.message}")
        if raise_on_error:
            raise SCPIError(errors, command=command)


    def scpi_str_to_float(self, scpi_str:str) -> float:
        """ Return the float value from a scpi_str without suffixes"""
        return float(scpi_str.split(' ')[0])

    def write_scpi(self, command:str):
        """ Send a SCPI command and check for errors. """
        self.inst.write(command)
        time.sleep(0.1)
        self.check_and_print_errors(command=command, raise_on_error=True)

    def read_scpi(self):
        """ Read a SCPI response or value"""
        return self.inst.read()

    def query_scpi(self, command:str):
        """ Query a SCPI command and check for errors. """
        read_param = self.inst.query(command)
        time.sleep(0.1)
        self.check_and_print_errors(command=command, raise_on_error=True)
        return read_param

    def identify(self):
        """ Return identification string of the appliance. """
        return self.query_scpi("*IDN?")

    def set_curr(self, value:float):
        """
        Set current of the appliance. Returns the set value on success, None if value is out of range.
        
        :param value: Value to set in Ampere
        :type value: float
        :return: Value actually set in Ampere, or None if out of range
        :rtype: float | None
        """
        if 0 <= value <= self.CURR_MAX:
            self.write_scpi(f"CURR {value}")
            return self.scpi_str_to_float(self.query_scpi("CURR?"))
        print("Current out of range. Range is 0 to ", self.CURR_MAX)
        return None

    def set_volt(self, value:float):
        """
        Set voltage of the appliance. Returns the set value on success, None if value is out of range.
        
        :param value: Value to set in Volt
        :type value: float
        :return: Value actually set in Volt, or None if out of range
        :rtype: float | None
        """
        if 0 <= value <= self.VOLT_MAX:
            self.write_scpi(f"VOLT {value}")
            return self.scpi_str_to_float(self.query_scpi("VOLT?"))
        print("Voltage out of range. Range is 0 to ", self.VOLT_MAX)
        return None

    def set_pow(self, value:float):
        """
        Set power of the appliance. Returns the set value on success, None if value is out of range.
        
        :param value: Value to set in Watt
        :type value: float
        :return: Value actually set in Watt, or None if out of range
        :rtype: float | None
        """
        if 0 <= value <= self.POW_MAX:
            self.write_scpi(f"POW {value}")
            return self.scpi_str_to_float(self.query_scpi("POW?"))
        print("Power out of range. Range is 0 to ", self.POW_MAX)
        return None
    
    def meas_curr(self):
        """ Return measured current in Ampere as float. """
        return self.scpi_str_to_float(self.query_scpi("MEAS:CURR?"))
    
    def meas_volt(self):
        """ Return measured voltage in Volt as float. """
        return self.scpi_str_to_float(self.query_scpi("MEAS:VOLT?"))

    def meas_pow(self):
        """ Return measured power in Watt as float. """
        return self.scpi_str_to_float(self.query_scpi("MEAS:POW?"))

    def preset_zero(self):
        """ Set current, voltage and power to zero. """
        self.set_curr(0)
        time.sleep(0.1)
        self.set_volt(0)
        time.sleep(0.1)
        self.set_pow(0)
        time.sleep(0.1)
    
    def meas_volt_dc(self):
        """ Return measured DC voltage in Volt as float. """
        return float(self.query_scpi("MEAS:VOLT:DC?"))
    
    def close(self):
        """ Close the SCPI connection. """
        self.inst.close()
  
class ea_ps(TcpScpiAppliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 40.00 # Volt
    POW_MAX = 3000.00 # Watt

    def setup(self):
        """ Setup the power supply for operation. Print identification, reset the appliance and set voltage, current and power to zero. Set access to remote. """
        print("ID:", self.query_scpi("*IDN?"))
        self.write_scpi("*RST")
        self.write_scpi("SOUR:VOLT:LEV 0")
        print("Preset Voltage:", self.query_scpi("SOUR:VOLT:LEV?"))
        self.write_scpi("SOUR:CURR:LEV 0")
        print("Preset Current:", self.query_scpi("SOUR:CURR:LEV?"))
        self.write_scpi("SOUR:POW:LEV 0")
        print("Preset Power:", self.query_scpi("SOUR:POW:LEV?"))
        self.write_scpi("SYST:LOCK:STAT 1")
        time.sleep(1)
        print("Access: ", self.query_scpi("SYST:LOCK:OWN?"))

class ea_el(TcpScpiAppliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 80.00 # Volt
    POW_MAX = 2400.00 # Watt
    R_MIN = 5.00 # Ohm
    R_MAX = 100.00 # Ohm

    def setup(self):
        """ Setup the electronic load for operation. Print identification and reset the appliance. Set access to remote. """
        print("ID:", self.query_scpi("*IDN?"))
        self.write_scpi("*RST")
        time.sleep(1)
        print("Access: ", self.query_scpi("SYST:LOCK:OWN?"))
    
    def preset_zero(self):
        """ Set current and power to zero. """
        self.set_curr(0)
        time.sleep(0.1)
        self.set_pow(0)
        time.sleep(0.1)

class rigol_dmm(TcpScpiAppliance):
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
        """ Setup the DMM for operation. Print identification, reset the appliance and print command set and SCPI version. """
        print("ID:", self.query_scpi("*IDN?"))
        self.write_scpi("*RST")
        time.sleep(1)
        print("Command Set:", self.query_scpi("CMDset?"))
        print("SCPI Version:", self.query_scpi("SYSTem:VERSion?"))

    def identify(self):
        """ Return identification and network information of the DMM. """
        return {
            "id": self.query_scpi("*IDN?"),
            "ip": self.query_scpi("UTIL:INTE:LAN:IP?"),
            "subnet_mask": self.query_scpi("UTIL:INTE:LAN:MASK?"),
            "cmdset": self.query_scpi("CMDset?"),
            "scpi_vers": self.query_scpi("SYSTem:VERSion?")
        }
    
    def _query_error_line(self) -> str:
        """ Return the next error line from the SCPI error queue """
        return self.inst.query("SYST:ERR?")