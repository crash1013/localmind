# validate_sqlite_type.py

import re
from typing import Literal

StorageClass = Literal["null", "integer", "real", "text", "blob", "numeric"]

# Canonical SQLite storage classes (lowercase for normalization)
STORAGE_CLASSES: set[str] = {"null", "integer", "real", "text", "blob", "numeric"}

# Curated list of common declared types people actually use (lowercase keys).
# This is only used when strict=True; otherwise any declared type is accepted and mapped by affinity rules.
COMMON_DECLARED_TYPES: set[str] = {
    # integer-ish
    "int", "tinyint", "smallint", "mediumint", "bigint", "unsigned big int", "int2", "int8",
    # text-ish
    "character", "varchar", "varying character", "nchar", "native character", "nvarchar", "text", "clob",
    # real-ish
    "real", "double", "double precision", "float",
    # numeric-ish
    "numeric", "decimal", "boolean", "date", "datetime",
    # blob
    "blob",
}

_PARAM_RE = re.compile(r"\s*\([^)]*\)")        # parenthesized chunk e.g. "(255)" or "(10,2)"
_WHITESPACE_RE = re.compile(r"\s+")
_BASE_RE = re.compile(r"^[a-z0-9_ ]+$")        # mild sanity check on characters


def normalize_declared_type(data_type: str) -> str:
    """
    Normalize a declared type: lowercase, strip params (e.g., varchar(255) -> varchar),
    collapse internal whitespace, trim ends.
    """
    s = data_type.strip().lower()
    s = _PARAM_RE.sub("", s)                   # drop the first parenthesized group (SQLite ignores it for affinity)
    s = _WHITESPACE_RE.sub(" ", s).strip()     # collapse spaces for things like "double precision"
    return s


def sqlite_affinity(data_type: str) -> StorageClass:
    """
    Compute SQLite affinity according to documented rules:
      1) contains "int"                -> "integer"
      2) contains "char"|"clob"|"text" -> "text"
      3) contains "blob" or empty      -> "blob"
      4) contains "real"|"floa"|"doub" -> "real"
      5) otherwise                     -> "numeric"
    """
    s = normalize_declared_type(data_type)

    if "int" in s:
        return "integer"
    if any(k in s for k in ("char", "clob", "text")):
        return "text"
    if s == "" or "blob" in s:
        return "blob"
    if any(k in s for k in ("real", "floa", "doub")):
        return "real"
    return "numeric"


def is_valid_sqlite_type(data_type: str, *, strict: bool = False) -> bool:
    """
    Validate a SQLite declared type.
    - strict=False (default): Always True if it parses to sane characters; SQLite will accept it,
      and we can compute an affinity with `sqlite_affinity`.
    - strict=True: Only accept canonical storage classes OR a curated list of common declared types
      (ignoring length/precision params).
    """
    if not data_type or not isinstance(data_type, str):
        return False

    # quick sanity on character set (letters/digits/underscores/spaces and optional params)
    raw = data_type.strip().lower()
    raw_no_params = _PARAM_RE.sub("", raw).strip()
    if raw_no_params and not _BASE_RE.match(raw_no_params):
        return False

    if not strict:
        # SQLite accepts any declared type; we just ensure we can compute an affinity.
        # (We already sanitized characters; affinity always resolves.)
        return True

    # strict path
    base = normalize_declared_type(data_type)
    if base in STORAGE_CLASSES:
        return True
    if base in COMMON_DECLARED_TYPES:
        return True
    # Also accept exact storage class with params removed (e.g., "text(255)" normalizes to "text")
    # Already covered by `base in STORAGE_CLASSES`.
    return False


def canonical_storage_class(data_type: str) -> StorageClass:
    """
    Return the canonical storage class (lowercase) for the given declared type.
    This is often what you actually need for schema auditing.
    """
    return sqlite_affinity(data_type)

