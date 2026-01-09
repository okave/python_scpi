import time
import pyvisa
from geraete.scpi_errors import SCPIError, SCPIErrorEntry, parse_scpi_error


class tcp_scpi_appliance:
    CURR_MAX = 0.00 # Ampere
    VOLT_MAX = 0.00 # Volt
    POW_MAX = 0.00 # Watt
    ERROR_FLAG = 0b00000100

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
    
    def check_error_flag(self) -> bool:
        stb = self.inst.query("*STB?").strip()
        return bool(int(stb) & self.ERROR_FLAG)

    def _query_error_line(self) -> str:
        return self.inst.query("ERR:NEXT?")

    def read_error(self) -> list[SCPIErrorEntry]:
        """
        Liest die komplette Error-Queue aus und gibt eine Liste zurück.
        """
        errors: list[SCPIErrorEntry] = []
        while True:
            resp = self._query_error_line()
            try:
                entry = parse_scpi_error(resp)
            except SCPIError:
                # Unparseable -> als Fehler aufnehmen und abbrechen
                errors.append(SCPIErrorEntry(-1, f"Unparseable error response: {resp.strip()}"))
                break

            if entry is None:
                break  # 0,"No error" -> fertig
            errors.append(entry)

        return errors

    def check_and_print_errors(self, command: str | None = None, raise_on_error: bool = False):
        """
        Prüft ob Fehler vorliegen und gibt sie aus.
        Optional: Exception werfen.
        """
        # STB als schneller Vorfilter – kann bei manchen Geräten unzuverlässig sein,
        # deshalb bei STB-Problemen lieber direkt Queue prüfen.
        # for _ in range(3):
        #     try:
        #         has_flag = self.check_error_flag()
        #     except Exception:
        #         has_flag = True
        #     if has_flag:
        #         break
        #     time.sleep(0.1)
        # # try:
        # #     has_flag = self.check_error_flag()
        # # except Exception:
        # #     has_flag = True

        # if not has_flag:
        #     return

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
        return float(scpi_str.split(' ')[0])

    def write_scpi(self, command:str):
        self.inst.write(command)
        time.sleep(0.1)
        self.check_and_print_errors(command=command, raise_on_error=True)

    def read_scpi(self):
        return self.inst.read()

    def query_scpi(self, command:str):
        read_param = self.inst.query(command)
        time.sleep(0.1)
        self.check_and_print_errors(command=command, raise_on_error=True)
        return read_param

    def identify(self):
        return self.query_scpi("*IDN?")

    def set_curr(self, value:float):
        if 0 <= value <= self.CURR_MAX:
            self.write_scpi(f"CURR {value}")
            return self.scpi_str_to_float(self.query_scpi("CURR?"))
        print("Current out of range. Range is 0 to ", self.CURR_MAX)
        return None

    def set_volt(self, value:float):
        if 0 <= value <= self.VOLT_MAX:
            self.write_scpi(f"VOLT {value}")
            return self.scpi_str_to_float(self.query_scpi("VOLT?"))
        print("Voltage out of range. Range is 0 to ", self.VOLT_MAX)
        return None

    def set_pow(self, value:float):
        if 0 <= value <= self.POW_MAX:
            self.write_scpi(f"POW {value}")
            return self.scpi_str_to_float(self.query_scpi("POW?"))
        print("Power out of range. Range is 0 to ", self.POW_MAX)
        return None
    
    def meas_curr(self):
        return self.scpi_str_to_float(self.query_scpi("MEAS:CURR?"))
    
    def meas_volt(self):
        return self.scpi_str_to_float(self.query_scpi("MEAS:VOLT?"))

    def meas_pow(self):
        return self.scpi_str_to_float(self.query_scpi("MEAS:POW?"))

    def preset_zero(self):
        self.set_curr(0)
        time.sleep(0.1)
        self.set_volt(0)
        time.sleep(0.1)
        self.set_pow(0)
        time.sleep(0.1)
    
    def meas_volt_dc(self):
        return float(self.query_scpi("MEAS:VOLT:DC?"))
    
    def close(self):
        self.inst.close()
  
class ea_ps(tcp_scpi_appliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 40.00 # Volt
    POW_MAX = 3000.00 # Watt

    def setup(self):
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

class ea_el(tcp_scpi_appliance):
    CURR_MAX = 120.00 # Ampere
    VOLT_MAX = 80.00 # Volt
    POW_MAX = 2400.00 # Watt
    R_MIN = 5.00 # Ohm
    R_MAX = 100.00 # Ohm

    def setup(self):
        print("ID:", self.query_scpi("*IDN?"))
        self.write_scpi("*RST")
        time.sleep(1)
        print("Access: ", self.query_scpi("SYST:LOCK:OWN?"))
    
    def preset_zero(self):
        self.set_curr(0)
        time.sleep(0.1)
        self.set_pow(0)
        time.sleep(0.1)

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
        print("ID:", self.query_scpi("*IDN?"))
        self.write_scpi("*RST")
        time.sleep(1)
        print("Command Set:", self.query_scpi("CMDset?"))
        print("SCPI Version:", self.query_scpi("SYSTem:VERSion?"))

    def identify(self):
        return {
            "id": self.query_scpi("*IDN?"),
            "ip": self.query_scpi("UTIL:INTE:LAN:IP?"),
            "subnet_mask": self.query_scpi("UTIL:INTE:LAN:MASK?"),
            "cmdset": self.query_scpi("CMDset?"),
            "scpi_vers": self.query_scpi("SYSTem:VERSion?")
        }
    
    def _query_error_line(self) -> str:
        return self.inst.query("SYST:ERR?")