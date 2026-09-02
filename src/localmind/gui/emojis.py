# emojis.py

from typing import TypedDict, Dict
from enum import IntEnum

class StatusValues(IntEnum):
    STATUS_UNKNOWN = 0
    STATUS_OK = 1
    STATUS_ERROR = 2
    STATUS_X_MARK = 3
    STATUS_CHK_MARK = 4
    STATUS_UNKNOWN_A = 5
    STATUS_OK_A = 6
    STATUS_ERROR_A = 7
    STATUS_X_MARK_A = 8
    STATUS_CHK_MARK_A = 9

class StatusCharacter(TypedDict):
    state: StatusValues
    character: str

STATUS_CHARACTER_MAP: Dict[StatusValues, str] = {
    StatusValues.STATUS_UNKNOWN: "🟡",
    StatusValues.STATUS_OK: "🟢",
    StatusValues.STATUS_ERROR: "🔴",
    StatusValues.STATUS_X_MARK: "❌",
    StatusValues.STATUS_CHK_MARK: "✅",
    StatusValues.STATUS_UNKNOWN_A: "⚠️",
    StatusValues.STATUS_OK_A: " ✅",
    StatusValues.STATUS_ERROR_A: "🚨",
    StatusValues.STATUS_X_MARK_A: "✖️",
    StatusValues.STATUS_CHK_MARK_A: "✔️",
}
