
# kill_llama_server(timeout: float = 5.0) -> list[str]:

import psutil
from logging import Logger

from localmind.utils.initLogger import init_logger

def get_llama_server_procs() -> list[psutil.Process]:
    servers: list[psutil.Process] = []

    for proc in psutil.process_iter(["name"]):
        try:
            name = (proc.info["name"] or "").lower()

            if name in ("llama-server", "llama-server.exe"):
                servers.append(proc)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return servers

def kill_llama_servers(timeout: float = 2.0, logger: Logger | None = None) -> list[int]:
    servers: list[psutil.Process] = []

    for proc in psutil.process_iter(["name"]):
        try:
            name = (proc.info["name"] or "").lower()

            if name in ("llama-server", "llama-server.exe"):
                servers.append(proc)
                proc.terminate()
                if logger:
                    logger.info(f"Terminated llama-server process: {proc.pid}")

        except psutil.NoSuchProcess:
            continue

        except psutil.AccessDenied as exc:
            if logger:
                pid = getattr(proc, "pid", "unknown")
                logger.warning(f"Permission denied terminating process {pid}: {exc}")
            continue

    if not servers:
        return []
    
    gone, alive = psutil.wait_procs(servers, timeout=timeout)

    for proc in alive:
        try:
            proc.kill()
            if logger:
                logger.warning(f"Force killed stubborn llama-server process: {proc.pid}")
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied as exc:
            if logger:
                pid = getattr(proc, "pid", "unknown")
                logger.error(f"Failed to force kill process {pid} (Access Denied): {exc}")        
    if alive:
        psutil.wait_procs(alive, timeout=timeout)

    return [proc.pid for proc in servers]


if __name__ == "__main__":
    pids = kill_llama_servers()

    if pids:
        print(f"Stopped llama-server processes: {pids}")
    else:
        print("No running llama-server processes found.")