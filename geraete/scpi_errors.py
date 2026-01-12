# scpi_errors.py
from __future__ import annotations
from dataclasses import dataclass
import re

_SCPI_ERROR_RE = re.compile(
    """ Regex for parsing various formats of SCPI error responses."""
    r"""
    ^\s* # Beginning, variable amount of whitespace
    (?P<code>[+-]?\d+)  # Errorcode, leading +,- or none followed by one or more digits
    \s* # variable amount of whitespace
    (?:[,:\-]\s*|\s+)? # Separator: , or : or - with variable amount of whitespace around it, or just whitespace, separator optional
    (?P<msg>.*) # Error message until end, including spaces
    $ # End
    """, 
    re.VERBOSE # Allow verbose regex with comments
)

@dataclass(frozen=True)
class SCPIErrorEntry:
    code: int
    message: str


class SCPIError(Exception):
    """
    Class for SCPI errors returned by instruments.
    """
    def __init__(self, errors: list[SCPIErrorEntry], command: str | None = None):
        self.errors = errors
        self.command = command
        super().__init__(self.format())

    def format(self) -> str:
        """ Format the error message. """
        body = "; ".join(f"{e.code}: {e.message}" for e in self.errors)
        if self.command:
            return f'SCPI error after "{self.command}": {body}'
        return f"SCPI error: {body}"


# def parse_scpi_error(resp: str) -> SCPIErrorEntry | None:
#     """
#     Erwartet typ. SCPI-Format:
#       -200,"Execution error"
#        0,"No error"
#     so die Theorie... 
#     Gibt None zurück, wenn code == 0.
#     """
#     resp = resp.strip()

#     code_str, msg = resp.split(",", 1)
#     code = int(code_str.strip())
#     msg = msg.strip().strip('"')
#     if code == 0:
#         return None
#     return SCPIErrorEntry(code=code, message=msg)

def parse_scpi_error(resp: str) -> SCPIErrorEntry | None:
    """
    Parse a SCPI error response string into a SCPIErrorEntry or None if no error. Uses regex for parsing.
    :param resp: Description
    :type resp: str
    :return: SCPIErrorEntry or None if no error.
    :rtype: SCPIErrorEntry | None
    """
    resp = resp.strip()
    m = _SCPI_ERROR_RE.match(resp)
    if not m:
        raise ValueError(f"Unparseable SCPI error response: {resp}")

    code = int(m.group("code"))
    msg = m.group("msg").strip().strip('"')

    if code == 0:
        return None

    return SCPIErrorEntry(code=code, message=msg)
