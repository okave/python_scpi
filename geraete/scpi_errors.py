# scpi_errors.py
from __future__ import annotations
from dataclasses import dataclass
import re

_SCPI_ERROR_RE = re.compile(
    r"""
    ^\s* # Anfang, beliebig viel Whitespace
    (?P<code>[+-]?\d+)  # Fehlercode, vorangestelltes +,- oder nichts davon, eine oder mehrere Ziffern
    \s* # beliebig viel Whitespace
    (?:[,:\-]\s*|\s+)? # Trenner: , oder : oder - mit beliebig viel Whitespace drumrum, oder einfach nur Whitespace, separator optional
    (?P<msg>.*) # Fehlermeldung bis zum Ende, inklusive Leerzeichen
    $ # Ende
    """, # 
    re.VERBOSE
)

@dataclass(frozen=True)
class SCPIErrorEntry:
    code: int
    message: str


class SCPIError(Exception):
    """
    Exception, die eine komplette SCPI-Error-Queue enthält.
    """
    def __init__(self, errors: list[SCPIErrorEntry], command: str | None = None):
        self.errors = errors
        self.command = command
        super().__init__(self.format())

    def format(self) -> str:
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
    resp = resp.strip()
    m = _SCPI_ERROR_RE.match(resp)
    if not m:
        raise ValueError(f"Unparseable SCPI error response: {resp}")

    code = int(m.group("code"))
    msg = m.group("msg").strip().strip('"')

    if code == 0:
        return None

    return SCPIErrorEntry(code=code, message=msg)
