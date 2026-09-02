from __future__ import annotations

from dataclasses import dataclass, asdict
import os
import platform
import socket
import uuid

import psutil


@dataclass(slots=True)
class HostInfo:
    host_name: str
    fqdn: str
    os_name: str
    os_version: str
    os_release: str
    platform_string: str
    machine: str
    processor: str
    physical_cpu_cores: int | None
    logical_cpu_cores: int | None
    ram_bytes: int
    python_version: str
    user_name: str | None
    machine_id: str | None


def get_machine_id() -> str | None:
    """
    Best-effort stable machine identifier.

    This intentionally avoids being too clever. It is useful for distinguishing
    hosts when hostname changes, but should not be treated as security-sensitive.
    """
    try:
        return hex(uuid.getnode())
    except Exception:
        return None


def get_host_info() -> HostInfo:
    vm = psutil.virtual_memory()

    return HostInfo(
        host_name=socket.gethostname(),
        fqdn=socket.getfqdn(),
        os_name=platform.system(),
        os_version=platform.version(),
        os_release=platform.release(),
        platform_string=platform.platform(),
        machine=platform.machine(),
        processor=platform.processor(),
        physical_cpu_cores=psutil.cpu_count(logical=False),
        logical_cpu_cores=psutil.cpu_count(logical=True),
        ram_bytes=int(vm.total),
        python_version=platform.python_version(),
        user_name=os.environ.get("USERNAME") or os.environ.get("USER"),
        machine_id=get_machine_id(),
    )


def get_host_info_dict() -> dict[str, object]:
    return asdict(get_host_info())