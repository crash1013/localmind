# validate_mssql_type.py

import re
from typing import Optional, TypedDict, Literal

ParamMode = Literal["none", "optional", "required"]

class TypeRule(TypedDict):
    mode: ParamMode
    pattern: Optional[str]  # regex for the parenthesized params, if present

VALID_MSSQL_TYPES: dict[str, TypeRule] = {
    # Length REQUIRED
    "char":        {"mode": "required",  "pattern": r"^\(\s*\d{1,4}\s*\)$"},
    "nchar":       {"mode": "required",  "pattern": r"^\(\s*\d{1,4}\s*\)$"},
    "binary":      {"mode": "required",  "pattern": r"^\(\s*\d{1,4}\s*\)$"},

    # Length OPTIONAL (no params => default; or explicit (n) / (max))
    "varchar":     {"mode": "optional",  "pattern": r"^\(\s*(max|\d{1,4})\s*\)$"},
    "nvarchar":    {"mode": "optional",  "pattern": r"^\(\s*(max|\d{1,4})\s*\)$"},
    "varbinary":   {"mode": "optional",  "pattern": r"^\(\s*(max|\d{1,4})\s*\)$"},

    # Precision/scale OPTIONAL (no params => default 18,0)
    "decimal":     {"mode": "optional",  "pattern": r"^\(\s*\d{1,2}\s*,\s*\d{1,2}\s*\)$"},
    "numeric":     {"mode": "optional",  "pattern": r"^\(\s*\d{1,2}\s*,\s*\d{1,2}\s*\)$"},

    # Precision OPTIONAL for float (no params => 53); real is an alias for float(24)
    "float":       {"mode": "optional",  "pattern": r"^\(\s*\d{1,2}\s*\)$"},
    "real":        {"mode": "none",      "pattern": None},

    # Fractional seconds precision OPTIONAL 0–7 (no params => 7)
    "time":            {"mode": "optional",  "pattern": r"^\(\s*[0-7]\s*\)$"},
    "datetime2":       {"mode": "optional",  "pattern": r"^\(\s*[0-7]\s*\)$"},
    "datetimeoffset":  {"mode": "optional",  "pattern": r"^\(\s*[0-7]\s*\)$"},

    # No params allowed
    "int": {"mode": "none", "pattern": None},
    "bigint": {"mode": "none", "pattern": None},
    "smallint": {"mode": "none", "pattern": None},
    "tinyint": {"mode": "none", "pattern": None},
    "bit": {"mode": "none", "pattern": None},
    "money": {"mode": "none", "pattern": None},
    "smallmoney": {"mode": "none", "pattern": None},
    "date": {"mode": "none", "pattern": None},
    "datetime": {"mode": "none", "pattern": None},
    "smalldatetime": {"mode": "none", "pattern": None},
    "text": {"mode": "none", "pattern": None},
    "ntext": {"mode": "none", "pattern": None},
    "image": {"mode": "none", "pattern": None},
    "uniqueidentifier": {"mode": "none", "pattern": None},
    "xml": {"mode": "none", "pattern": None},
    "cursor": {"mode": "none", "pattern": None},
    "sql_variant": {"mode": "none", "pattern": None},
    "table": {"mode": "none", "pattern": None},
    "hierarchyid": {"mode": "none", "pattern": None},
    "geography": {"mode": "none", "pattern": None},
    "geometry": {"mode": "none", "pattern": None},
    "real": {"mode": "none", "pattern": None},
}

def is_valid_mssql_type(data_type: str) -> bool:
    """
    Validates both base MSSQL type and optional parameters.
    Examples that pass:
      varchar, varchar(50), varchar(max)
      nvarchar, nvarchar(100)
      varbinary, varbinary(max)
      decimal, decimal(10,2)
      numeric, numeric(5,0)
      float, float(24)
      time, time(3)
      datetime2, datetimeoffset(7)
      int, date, uniqueidentifier
    """
    normalized = data_type.strip().lower()
    m = re.match(r'^([a-z0-9_]+)(\s*\(.*\))?$', normalized)
    if not m:
        return False

    base = m.group(1)
    params = (m.group(2) or "").strip()

    rule = VALID_MSSQL_TYPES.get(base)
    if not rule:
        return False

    mode = rule["mode"]
    pattern = rule["pattern"]

    if mode == "none":
        return params == ""

    if mode == "optional":
        if params == "":
            return True  # accept omitted params
        return pattern is not None and re.match(pattern, params) is not None

    # mode == "required"
    if params == "":
        return False
    return pattern is not None and re.match(pattern, params) is not None
